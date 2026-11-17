"""Regras automáticas: pausa testes ruins e escala os que batem a meta de CPA.

Só mexe nos conjuntos criados pelo próprio sistema (tabela uploads),
nunca nas suas campanhas manuais.
"""
from __future__ import annotations

import logging
import sqlite3
from dataclasses import dataclass
from datetime import date

from .config import Rules, Settings
from .meta import Meta

log = logging.getLogger(__name__)


@dataclass
class Decision:
    action: str  # pause | scale | keep
    reason: str
    new_budget_cents: int | None = None


def conversions(row: dict, action_type: str) -> float:
    return sum(float(a.get("value", 0)) for a in row.get("actions", []) if a.get("action_type") == action_type)


def decide(spend: float, convs: float, budget_cents: int | None, rules: Rules, scaled_today: bool) -> Decision:
    target = rules.target_cpa
    if convs == 0:
        if spend >= target * rules.kill_spend_multiplier:
            return Decision("pause", f"gastou R${spend:.2f} sem conversão")
        return Decision("keep", "aprendendo")

    cpa = spend / convs
    if cpa > target * rules.kill_cpa_multiplier:
        return Decision("pause", f"CPA R${cpa:.2f} acima do limite")
    if cpa <= target and convs >= rules.scale_min_conversions and not scaled_today and budget_cents:
        new = int(budget_cents * (1 + rules.scale_pct / 100))
        new = min(new, int(rules.max_daily_budget * 100))
        if new > budget_cents:
            return Decision("scale", f"CPA R${cpa:.2f} com {convs:.0f} conversões", new)
    return Decision("keep", f"CPA R${cpa:.2f}")


def run(conn: sqlite3.Connection, settings: Settings, meta: Meta) -> list[str]:
    today = date.today().isoformat()
    managed = {r["adset_id"]: r["account_key"] for r in
               conn.execute("SELECT adset_id, account_key FROM uploads WHERE status = 'done' AND adset_id IS NOT NULL")}
    if not managed:
        return []

    report = []
    for acc_key in sorted(set(managed.values())):
        acc = settings.accounts.get(acc_key)
        if not acc:
            continue
        for row in meta.adsets_insights(acc.ad_account_id, "today"):
            adset_id = row["adset_id"]
            if adset_id not in managed:
                continue
            info = meta.adset_info(adset_id)
            if info.get("effective_status") != "ACTIVE":
                continue
            scaled_today = conn.execute(
                "SELECT 1 FROM actions WHERE adset_id = ? AND action = 'scale' AND day = ?", (adset_id, today)
            ).fetchone() is not None
            budget = int(info["daily_budget"]) if info.get("daily_budget") else None
            d = decide(float(row.get("spend", 0)), conversions(row, settings.rules.conversion_action),
                       budget, settings.rules, scaled_today)

            if d.action == "pause":
                meta.pause(adset_id)
                report.append(f"⏸️ {row['adset_name']}: {d.reason}")
            elif d.action == "scale":
                meta.set_daily_budget(adset_id, d.new_budget_cents)
                report.append(f"🚀 {row['adset_name']}: {d.reason} → R${d.new_budget_cents / 100:.2f}/dia")
            else:
                continue
            if not meta.dry_run:
                conn.execute("INSERT INTO actions (adset_id, action, detail, day) VALUES (?, ?, ?, ?)",
                             (adset_id, d.action, d.reason, today))
                conn.commit()
    return report
