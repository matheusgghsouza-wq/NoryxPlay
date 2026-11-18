"""Banco de criativos com reposição automática.

Tudo que chega no grupo vai para o banco. A cada ciclo, cada número é conferido:
se ele não tem nenhum anúncio vivo (o sistema ou você pausou tudo), o sistema puxa
os próximos criativos do banco e solta uma campanha nova nele (cópia da campanha
modelo do número, um anúncio por criativo). Criativo que validou em outro número
tem prioridade. Se o banco acabar, você é avisado no grupo.
"""
from __future__ import annotations

import logging
import sqlite3
from datetime import date
from pathlib import Path

from . import db
from .config import Account, Settings
from .meta import MetaPool

log = logging.getLogger(__name__)

# Anúncio com status ACTIVE mas nesses estados não está rodando de verdade
DEAD_EFFECTIVE = {"DISAPPROVED", "WITH_ISSUES", "DELETED", "ARCHIVED"}


def is_alive(ad: dict) -> bool:
    """Vivo = você ou o sistema não pausou e a Meta não reprovou.
    Campanha recém-criada pausada para revisão conta como viva (não dispara reposição)."""
    return ad.get("status") == "ACTIVE" and ad.get("effective_status") not in DEAD_EFFECTIVE


def chunks(items: list, size: int) -> list[list]:
    size = max(1, size)
    return [items[i:i + size] for i in range(0, len(items), size)]


def number_is_idle(conn: sqlite3.Connection, pool: MetaPool, acc_key: str, num_key: str) -> bool:
    """True se o número não tem nenhum anúncio vivo nas campanhas criadas pelo sistema."""
    campaigns = [r["campaign_id"] for r in conn.execute(
        "SELECT DISTINCT campaign_id FROM uploads WHERE account_key = ? AND number_key = ? "
        "AND status = 'done' AND campaign_id IS NOT NULL", (acc_key, num_key))]
    for campaign_id in campaigns:
        if db.get_kv(conn, f"closed:{campaign_id}"):
            continue  # já sabemos que essa campanha não tem nada vivo
        if any(is_alive(a) for a in pool[acc_key].campaign_ads(campaign_id)):
            return False
        if not pool.dry_run:
            db.set_kv(conn, f"closed:{campaign_id}", "1")
    return True


def pick_creatives(conn: sqlite3.Connection, settings: Settings, acc_key: str, num_key: str,
                   limit: int) -> list[sqlite3.Row]:
    """Próximos criativos do banco para o número: primeiro os que já validaram em
    outro lugar, depois os mais antigos que ainda não foram testados nele."""
    validated = {r["creative_id"] for r in conn.execute(
        "SELECT DISTINCT u.creative_id FROM actions a JOIN uploads u ON u.ad_id = a.object_id "
        "WHERE a.action = 'validate'")}
    used = {r["creative_id"] for r in conn.execute(
        "SELECT creative_id FROM uploads WHERE account_key = ? AND number_key = ?", (acc_key, num_key))}
    candidates = []
    for c in conn.execute("SELECT * FROM creatives ORDER BY id").fetchall():
        product = settings.products.get(c["product_key"])
        if not product or c["id"] in used:
            continue
        if product.accounts and acc_key not in product.accounts:
            continue
        candidates.append(c)
    candidates.sort(key=lambda c: (c["id"] not in validated, c["id"]))
    return candidates[:limit]


def bank_size(conn: sqlite3.Connection, settings: Settings) -> int:
    """Quantos criativos ainda não foram testados em pelo menos um número."""
    total = 0
    for acc_key, acc in settings.accounts.items():
        for num_key in acc.numbers:
            total += len(pick_creatives(conn, settings, acc_key, num_key, 10**6))
    return total


def upload_all(conn: sqlite3.Connection, settings: Settings, pool: MetaPool) -> list[str]:
    report: list[str] = []
    empty: list[str] = []
    plan: dict[str, dict[str, list[sqlite3.Row]]] = {}

    for acc_key, acc in settings.accounts.items():
        for num_key in acc.numbers:
            if not number_is_idle(conn, pool, acc_key, num_key):
                continue
            picks = pick_creatives(conn, settings, acc_key, num_key, settings.max_ads_per_campaign)
            if picks:
                plan.setdefault(acc_key, {})[num_key] = picks
            else:
                empty.append(f"{acc_key}/{num_key}")

    for acc_key, numbers in plan.items():
        report.extend(_upload_account(conn, settings, pool, settings.accounts[acc_key], numbers))

    # aviso de banco vazio: no máximo uma vez por dia para o mesmo conjunto de números
    if empty:
        key = f"empty_alert:{date.today().isoformat()}"
        signature = ",".join(sorted(empty))
        if db.get_kv(conn, key) != signature:
            report.append(f"⚠️ {len(empty)} número(s) parado(s) sem criativo novo pra testar: "
                          f"{', '.join(empty)}. Manda mais criativos no grupo.")
            if not pool.dry_run:
                db.set_kv(conn, key, signature)
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
