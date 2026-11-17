"""Bot do Telegram: coleta vídeos enviados no grupo e envia relatórios."""
from __future__ import annotations

import logging
import re
import sqlite3
from pathlib import Path

import requests

from . import db
from .config import Settings

log = logging.getLogger(__name__)
API = "https://api.telegram.org"
# A Bot API em nuvem só baixa arquivos de até 20 MB. Para vídeos maiores,
# rode um servidor local da Bot API e aponte TELEGRAM_API_URL para ele.
MAX_CLOUD_DOWNLOAD = 20 * 1024 * 1024


def parse_caption(caption: str, products: dict, default_product: str) -> tuple[str, str]:
    """'#produtox gancho 2' -> ('produtox', 'gancho 2'). Sem hashtag usa o produto padrão."""
    caption = (caption or "").strip()
    match = re.search(r"#(\w+)", caption)
    if match and match.group(1).lower() in {k.lower() for k in products}:
        key = next(k for k in products if k.lower() == match.group(1).lower())
        variant = (caption[: match.start()] + caption[match.end():]).strip()
        return key, variant
    return default_product, caption


class Telegram:
    def __init__(self, settings: Settings, api_url: str = API):
        self.s = settings
        self.base = f"{api_url}/bot{settings.telegram_token}"
        self.file_base = f"{api_url}/file/bot{settings.telegram_token}"

    def _call(self, method: str, **params):
        r = requests.post(f"{self.base}/{method}", json=params, timeout=60)
        data = r.json()
        if not data.get("ok"):
            raise RuntimeError(f"Telegram {method}: {data}")
        return data["result"]

    def send(self, text: str) -> None:
        if not self.s.telegram_chat_id:
            log.info("Sem TELEGRAM_CHAT_ID; relatório:\n%s", text)
            return
        for i in range(0, len(text), 4000):  # limite de mensagem do Telegram
            self._call("sendMessage", chat_id=self.s.telegram_chat_id, text=text[i:i + 4000])

    def collect(self, conn: sqlite3.Connection) -> list[int]:
        """Lê mensagens novas do grupo, baixa os vídeos e registra no banco."""
        offset = int(db.get_kv(conn, "tg_offset", "0"))
        updates = self._call("getUpdates", offset=offset, timeout=0,
                             allowed_updates=["message", "channel_post"])
        new_ids: list[int] = []
        videos_dir = self.s.data_dir / "videos"
        videos_dir.mkdir(exist_ok=True)

        for upd in updates:
            offset = upd["update_id"] + 1
            msg = upd.get("message") or upd.get("channel_post") or {}
            if self.s.telegram_chat_id and str(msg.get("chat", {}).get("id")) != self.s.telegram_chat_id:
                continue
            video = msg.get("video") or _video_document(msg)
            if not video:
                continue

            uid = video["file_unique_id"]
            if conn.execute("SELECT 1 FROM creatives WHERE tg_file_unique_id = ?", (uid,)).fetchone():
                continue
            if video.get("file_size", 0) > MAX_CLOUD_DOWNLOAD and API in self.base:
                self.send(f"⚠️ Vídeo da mensagem {msg['message_id']} tem mais de 20 MB; "
                          "comprima ou configure o servidor local da Bot API.")
                continue

            product_key, variant = parse_caption(msg.get("caption", ""), self.s.products, self.s.default_product)
            path = self._download(video["file_id"], videos_dir / f"{uid}.mp4")
            cur = conn.execute(
                "INSERT INTO creatives (tg_file_unique_id, tg_message_id, caption, product_key, variant, local_path)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                (uid, msg.get("message_id"), msg.get("caption", ""), product_key, variant, str(path)),
            )
            new_ids.append(cur.lastrowid)
            log.info("Criativo %s recebido (%s / %s)", cur.lastrowid, product_key, variant or "-")

        conn.commit()
        db.set_kv(conn, "tg_offset", str(offset))
        return new_ids

    def _download(self, file_id: str, dest: Path) -> Path:
        info = self._call("getFile", file_id=file_id)
        with requests.get(f"{self.file_base}/{info['file_path']}", stream=True, timeout=300) as r:
            r.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)
        return dest


def _video_document(msg: dict) -> dict | None:
    """Vídeo enviado como arquivo (sem compressão) chega como 'document'."""
    doc = msg.get("document")
    if doc and str(doc.get("mime_type", "")).startswith("video/"):
        return doc
    return None
