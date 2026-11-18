"""Regras automáticas no seu método: dentro de cada campanha de teste (bid cap),
o criativo que valida pelo custo por compra fica ativo e os que não validaram são pausados.

Só mexe nas campanhas criadas pelo próprio sistema (tabela uploads),
nunca nas suas campanhas manuais.
"""
from __future__ import annotations

import logging
import sqlite3
from dataclasses import dataclass
from datetime import date

from .config import Rules, Settings
from .meta import MetaPool

log = logging.getLogger(__name__)


@dataclass
class AdStat:
    ad_id: str
    name: str
    spend: float
    results: float
    active: bool

    @property
    def cost(self) -> float | None:
        return self.spend / self.results if self.results else None


def results(row: dict, action_type: str) -> float:
    return sum(float(a.get("value", 0)) for a in row.get("actions", []) if a.get("action_type") == action_type)


def is_validated(ad: AdStat, rules: Rules) -> bool:
    return ad.results >= rules.validate_min_results and ad.cost is not None and ad.cost <= rules.target_cost


def decide_campaign(ads: list[AdStat], rules: Rules) -> list[tuple[AdStat, str, str]]:
    """Retorna [(anúncio, 'pause' | 'validate', motivo)] para uma campanha de teste."""
    active = [a for a in ads if a.active]
    validated = [a for a in active if is_validated(a, rules)]
    out = [(a, "validate", f"{a.results:.0f} compras a R${a.cost:.2f}") for a in validated]

    for a in active:
        if a in validated:
            continue
        if a.results == 0 and a.spend >= rules.kill_spend_no_result:
            out.append((a, "pause", f"gastou R${a.spend:.2f} sem compra"))
        elif a.cost and a.spend >= rules.kill_min_spend and a.cost > rules.max_cost:
            out.append((a, "pause", f"custo R${a.cost:.2f} por compra"))
        elif validated and rules.pause_others_on_validate:
            out.append((a, "pause", "outro criativo validou na campanha"))
    return out


def run(conn: sqlite3.Connection, settings: Settings, pool: MetaPool) -> list[str]:
    today = date.today().isoformat()
    campaigns = [(r["campaign_id"], r["account_key"]) for r in conn.execute(
        "SELECT DISTINCT campaign_id, account_key FROM uploads WHERE status = 'done' AND campaign_id IS NOT NULL")]

    report = []
    for campaign_id, acc_key in campaigns:
        if acc_key not in settings.accounts:
            continue
        api = pool[acc_key]
        statuses = {a["id"]: a for a in api.campaign_ads(campaign_id)}
        ads = []
        for row in api.ads_insights(campaign_id):
            info = statuses.get(row["ad_id"], {})
            ads.append(AdStat(row["ad_id"], row.get("ad_name", ""), float(row.get("spend", 0)),
                              results(row, settings.rules.result_action),
                              info.get("effective_status") == "ACTIVE"))

        for ad, action, reason in decide_campaign(ads, settings.rules):
            if action == "validate":
                # avisa só uma vez por anúncio
                if conn.execute("SELECT 1 FROM actions WHERE object_id = ? AND action = 'validate'",
                                (ad.ad_id,)).fetchone():
                    continue
                report.append(f"🏆 VALIDOU: {ad.name} ({reason})")
            else:
                api.pause(ad.ad_id)
                report.append(f"⏸️ {ad.name}: {reason}")
            if not pool.dry_run:
                conn.execute("INSERT INTO actions (object_id, action, detail, day) VALUES (?, ?, ?, ?)",
                             (ad.ad_id, action, reason, today))
                conn.commit()
    return report
