"""Sobe criativos pendentes: cada lote vira uma cópia da campanha modelo (bid cap)
com um anúncio por criativo, do jeito que você já testa na mão."""
from __future__ import annotations

import logging
import sqlite3
from datetime import date
from pathlib import Path

from .config import Settings
from .meta import Meta

log = logging.getLogger(__name__)


def pending(conn: sqlite3.Connection, settings: Settings) -> dict[str, list[sqlite3.Row]]:
    """Criativos ainda não subidos, agrupados por conta."""
    out: dict[str, list[sqlite3.Row]] = {}
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
                out.setdefault(acc_key, []).append(c)
    return out


def chunks(items: list, size: int) -> list[list]:
    size = max(1, size)
    return [items[i:i + size] for i in range(0, len(items), size)]


def upload_all(conn: sqlite3.Connection, settings: Settings, meta: Meta) -> list[str]:
    report = []
    for acc_key, creatives in pending(conn, settings).items():
        acc = settings.accounts[acc_key]
        for batch in chunks(creatives, settings.max_ads_per_campaign):
            report.extend(_upload_batch(conn, settings, meta, acc_key, acc, batch))
    return report


def _upload_batch(conn, settings, meta, acc_key, acc, batch) -> list[str]:
    report, ready = [], []

    # 1) sobe os vídeos e cria os criativos
    for c in batch:
        product = settings.products[c["product_key"]]
        name = f"{product.key} #{c['id']} {c['variant'] or ''}".strip()
        try:
            video_id = meta.upload_video(acc.ad_account_id, Path(c["local_path"]), name)
            meta.wait_video_ready(video_id)
            thumb = meta.video_thumbnail(video_id)
            creative_id = meta.create_video_creative(
                acc.ad_account_id, name, acc.page_id, video_id, thumb, product.message,
                product.headline, product.link, product.cta, acc.instagram_user_id,
            )
            ready.append((c, name, video_id, creative_id))
        except Exception as e:  # noqa: BLE001 - registra e segue para o próximo
            log.exception("Falha no criativo %s (conta %s)", c["id"], acc_key)
            _save(conn, meta, c["id"], acc_key, "error", error=str(e))
            report.append(f"❌ {name} → conta {acc_key}: {e}")
    if not ready:
        return report

    # 2) copia a campanha modelo e coloca um anúncio por criativo
    ids = ",".join(f"#{c['id']}" for c, *_ in ready)
    campaign_name = f"[TESTE] {date.today():%d/%m} {ids}"
    try:
        campaign_id, adset_id = meta.copy_campaign(acc.template_campaign_id, campaign_name, settings.test_status)
    except Exception as e:  # noqa: BLE001
        log.exception("Falha ao copiar campanha modelo (conta %s)", acc_key)
        for c, name, video_id, creative_id in ready:
            _save(conn, meta, c["id"], acc_key, "error", video_id, creative_id, error=str(e))
        return report + [f"❌ Campanha {campaign_name} → conta {acc_key}: {e}"]

    for c, name, video_id, creative_id in ready:
        try:
            ad_id = meta.create_ad(acc.ad_account_id, name, adset_id, creative_id, "ACTIVE")
            _save(conn, meta, c["id"], acc_key, "done", video_id, creative_id, campaign_id, adset_id, ad_id)
        except Exception as e:  # noqa: BLE001
            log.exception("Falha ao criar anúncio %s (conta %s)", c["id"], acc_key)
            _save(conn, meta, c["id"], acc_key, "error", video_id, creative_id, campaign_id, adset_id, error=str(e))
            report.append(f"❌ {name} → conta {acc_key}: {e}")
            continue
    ok = [name for c, name, *_ in ready]
    report.append(f"✅ {campaign_name} (conta {acc_key}): {len(ok)} criativo(s)")
    return report


def _save(conn, meta, creative_id, account_key, status, video_id=None, creative_meta_id=None,
          campaign_id=None, adset_id=None, ad_id=None, error=None):
    if meta.dry_run:
        return
    conn.execute(
        """INSERT INTO uploads (creative_id, account_key, status, video_id, creative_meta_id,
                                campaign_id, adset_id, ad_id, error)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(creative_id, account_key) DO UPDATE SET status = excluded.status,
             video_id = excluded.video_id, creative_meta_id = excluded.creative_meta_id,
             campaign_id = excluded.campaign_id, adset_id = excluded.adset_id,
             ad_id = excluded.ad_id, error = excluded.error""",
        (creative_id, account_key, status, video_id, creative_meta_id, campaign_id, adset_id, ad_id, error),
    )
    conn.commit()
