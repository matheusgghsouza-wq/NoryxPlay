"""Sobe criativos pendentes em todas as contas e números.

Para cada conta, cada vídeo é enviado uma vez só. Depois, para cada número (página)
da conta, o lote vira uma cópia da campanha modelo daquele número, com um anúncio
por criativo, do jeito que você já testa na mão.
"""
from __future__ import annotations

import logging
import sqlite3
from datetime import date
from pathlib import Path

from .config import Account, Settings
from .meta import MetaPool

log = logging.getLogger(__name__)


def pending(conn: sqlite3.Connection, settings: Settings) -> dict[tuple[str, str], list[sqlite3.Row]]:
    """Criativos ainda não subidos, agrupados por (conta, número)."""
    out: dict[tuple[str, str], list[sqlite3.Row]] = {}
    for c in conn.execute("SELECT * FROM creatives ORDER BY id").fetchall():
        product = settings.products.get(c["product_key"])
        if not product:
            continue
        for acc_key in (product.accounts or list(settings.accounts)):
            acc = settings.accounts.get(acc_key)
            if not acc:
                continue
            for num_key in acc.numbers:
                # Erros não são repetidos sozinhos (evita duplicar anúncios); use "python main.py retry".
                done = conn.execute(
                    "SELECT 1 FROM uploads WHERE creative_id = ? AND account_key = ? AND number_key = ?",
                    (c["id"], acc_key, num_key)).fetchone()
                if not done:
                    out.setdefault((acc_key, num_key), []).append(c)
    return out


def chunks(items: list, size: int) -> list[list]:
    size = max(1, size)
    return [items[i:i + size] for i in range(0, len(items), size)]


def upload_all(conn: sqlite3.Connection, settings: Settings, pool: MetaPool) -> list[str]:
    report: list[str] = []
    by_account: dict[str, dict[str, list[sqlite3.Row]]] = {}
    for (acc_key, num_key), creatives in pending(conn, settings).items():
        by_account.setdefault(acc_key, {})[num_key] = creatives

    for acc_key, numbers in by_account.items():
        report.extend(_upload_account(conn, settings, pool, settings.accounts[acc_key], numbers))
    return report


def _upload_account(conn, settings: Settings, pool: MetaPool, acc: Account,
                    numbers: dict[str, list[sqlite3.Row]]) -> list[str]:
    api = pool[acc.key]
    report: list[str] = []

    # 1) cada vídeo sobe uma vez na conta, mesmo que vá para vários números
    videos: dict[int, tuple[str, str]] = {}  # creative_id -> (video_id, thumb)
    all_creatives = {c["id"]: c for cs in numbers.values() for c in cs}
    for cid, c in all_creatives.items():
        name = _ad_name(settings, c)
        try:
            video_id = api.upload_video(acc.ad_account_id, Path(c["local_path"]), name)
            api.wait_video_ready(video_id)
            videos[cid] = (video_id, api.video_thumbnail(video_id))
        except Exception as e:  # noqa: BLE001 - registra e segue para o próximo
            log.exception("Falha ao subir vídeo %s (conta %s)", cid, acc.key)
            for num_key, cs in numbers.items():
                if any(x["id"] == cid for x in cs):
                    _save(conn, pool, cid, acc.key, num_key, "error", error=str(e))
            report.append(f"❌ {name} → conta {acc.key}: {e}")

    # 2) para cada número, uma campanha por lote
    for num_key, creatives in numbers.items():
        ready = [c for c in creatives if c["id"] in videos]
        for batch in chunks(ready, settings.max_ads_per_campaign):
            report.extend(_upload_batch(conn, settings, pool, acc, num_key, batch, videos))
    return report


def _upload_batch(conn, settings, pool, acc, num_key, batch, videos) -> list[str]:
    api = pool[acc.key]
    number = acc.numbers[num_key]
    report, ready = [], []
    where = f"conta {acc.key} / número {num_key}"

    for c in batch:
        product = settings.products[c["product_key"]]
        name = _ad_name(settings, c)
        video_id, thumb = videos[c["id"]]
        try:
            creative_id = api.create_video_creative(
                acc.ad_account_id, name, number.page_id, video_id, thumb, product.message,
                product.headline, product.link, product.cta, number.instagram_user_id,
            )
            ready.append((c, name, video_id, creative_id))
        except Exception as e:  # noqa: BLE001
            log.exception("Falha no criativo %s (%s)", c["id"], where)
            _save(conn, pool, c["id"], acc.key, num_key, "error", video_id, error=str(e))
            report.append(f"❌ {name} → {where}: {e}")
    if not ready:
        return report

    ids = ",".join(f"#{c['id']}" for c, *_ in ready)
    campaign_name = f"[TESTE] {date.today():%d/%m} {acc.key}/{num_key} {ids}"
    try:
        campaign_id, adset_id = api.copy_campaign(number.template_campaign_id, campaign_name, settings.test_status)
    except Exception as e:  # noqa: BLE001
        log.exception("Falha ao copiar campanha modelo (%s)", where)
        for c, name, video_id, creative_id in ready:
            _save(conn, pool, c["id"], acc.key, num_key, "error", video_id, creative_id, error=str(e))
        return report + [f"❌ {campaign_name} → {where}: {e}"]

    ok = 0
    for c, name, video_id, creative_id in ready:
        try:
            ad_id = api.create_ad(acc.ad_account_id, name, adset_id, creative_id, "ACTIVE")
            _save(conn, pool, c["id"], acc.key, num_key, "done", video_id, creative_id, campaign_id, adset_id, ad_id)
            ok += 1
        except Exception as e:  # noqa: BLE001
            log.exception("Falha ao criar anúncio %s (%s)", c["id"], where)
            _save(conn, pool, c["id"], acc.key, num_key, "error", video_id, creative_id, campaign_id, adset_id,
                  error=str(e))
            report.append(f"❌ {name} → {where}: {e}")
    report.append(f"✅ {campaign_name} ({where}): {ok} criativo(s)")
    return report


def _ad_name(settings: Settings, c: sqlite3.Row) -> str:
    product = settings.products[c["product_key"]]
    return f"{product.key} #{c['id']} {c['variant'] or ''}".strip()


def _save(conn, pool, creative_id, account_key, number_key, status, video_id=None, creative_meta_id=None,
          campaign_id=None, adset_id=None, ad_id=None, error=None):
    if pool.dry_run:
        return
    conn.execute(
        """INSERT INTO uploads (creative_id, account_key, number_key, status, video_id, creative_meta_id,
                                campaign_id, adset_id, ad_id, error)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(creative_id, account_key, number_key) DO UPDATE SET status = excluded.status,
             video_id = excluded.video_id, creative_meta_id = excluded.creative_meta_id,
             campaign_id = excluded.campaign_id, adset_id = excluded.adset_id,
             ad_id = excluded.ad_id, error = excluded.error""",
        (creative_id, account_key, number_key, status, video_id, creative_meta_id, campaign_id, adset_id, ad_id,
         error),
    )
    conn.commit()
