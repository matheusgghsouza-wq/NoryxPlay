"""Sobe criativos pendentes em cada conta e monta os anúncios de teste."""
from __future__ import annotations

import logging
import sqlite3
from datetime import date
from pathlib import Path

from .config import Settings
from .meta import Meta

log = logging.getLogger(__name__)


def pending(conn: sqlite3.Connection, settings: Settings) -> list[tuple[sqlite3.Row, str]]:
    """Pares (criativo, conta) que ainda não foram subidos com sucesso."""
    out = []
    for c in conn.execute("SELECT * FROM creatives ORDER BY id").fetchall():
        product = settings.products.get(c["product_key"])
        if not product:
            continue
        for acc_key in (product.accounts or list(settings.accounts)):
            if acc_key not in settings.accounts:
                continue
            # Erros não são repetidos sozinhos (evita duplicar anúncios); use "python main.py retry".
            row = conn.execute("SELECT 1 FROM uploads WHERE creative_id = ? AND account_key = ?",
                               (c["id"], acc_key)).fetchone()
            if not row:
                out.append((c, acc_key))
    return out


def upload_all(conn: sqlite3.Connection, settings: Settings, meta: Meta) -> list[str]:
    report = []
    for c, acc_key in pending(conn, settings):
        acc = settings.accounts[acc_key]
        product = settings.products[c["product_key"]]
        name = f"[TESTE] {product.key} #{c['id']} {c['variant'] or ''} {date.today():%d/%m}".strip()
        try:
            video_id = meta.upload_video(acc.ad_account_id, Path(c["local_path"]), name)
            meta.wait_video_ready(video_id)
            thumb = meta.video_thumbnail(video_id)
            creative_id = meta.create_video_creative(
                acc.ad_account_id, name, acc.page_id, video_id, thumb, product.message,
                product.headline, product.link, product.cta, acc.instagram_user_id,
            )
            adset_id = meta.copy_adset(acc.template_adset_id, name, settings.test_status)
            ad_id = meta.create_ad(acc.ad_account_id, name, adset_id, creative_id, settings.test_status)
            if not meta.dry_run:
                _save(conn, c["id"], acc_key, "done", video_id, creative_id, adset_id, ad_id)
            report.append(f"✅ {name} → conta {acc_key}")
        except Exception as e:  # noqa: BLE001 - registra e segue para o próximo
            log.exception("Falha ao subir criativo %s na conta %s", c["id"], acc_key)
            if not meta.dry_run:
                _save(conn, c["id"], acc_key, "error", error=str(e))
            report.append(f"❌ {name} → conta {acc_key}: {e}")
    return report


def _save(conn, creative_id, account_key, status, video_id=None, creative_meta_id=None,
          adset_id=None, ad_id=None, error=None):
    conn.execute(
        """INSERT INTO uploads (creative_id, account_key, status, video_id, creative_meta_id, adset_id, ad_id, error)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(creative_id, account_key) DO UPDATE SET status = excluded.status,
             video_id = excluded.video_id, creative_meta_id = excluded.creative_meta_id,
             adset_id = excluded.adset_id, ad_id = excluded.ad_id, error = excluded.error""",
        (creative_id, account_key, status, video_id, creative_meta_id, adset_id, ad_id, error),
    )
    conn.commit()
