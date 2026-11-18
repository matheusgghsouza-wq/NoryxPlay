"""Números do painel, lidos só do banco local (não consulta a Meta)."""
from __future__ import annotations

import sqlite3
from datetime import date

from . import db
from .config import Settings

STATE_LABEL = {"rodando": "Rodando", "sem_criativo": "Parado · sem criativo", "aguardando": "Aguardando 1º ciclo"}


def overview(conn: sqlite3.Connection, settings: Settings) -> dict:
    numbers = []
    for acc_key, acc in settings.accounts.items():
        for num_key in acc.numbers:
            st = db.get_number_state(conn, acc_key, num_key)
            tested = conn.execute(
                "SELECT COUNT(*) FROM uploads WHERE account_key = ? AND number_key = ? AND status = 'done'",
                (acc_key, num_key)).fetchone()[0]
            numbers.append({"account": acc_key, "number": num_key, "state": st["state"],
                            "label": STATE_LABEL.get(st["state"], st["state"]), "at": st["at"],
                            "tested": tested})

    # no banco = ainda não subiu em nenhum número
    in_bank = conn.execute(
        "SELECT COUNT(*) FROM creatives c WHERE NOT EXISTS "
        "(SELECT 1 FROM uploads u WHERE u.creative_id = c.id AND u.status = 'done')").fetchone()[0]
    today = date.today().isoformat()
    validated_today = conn.execute(
        "SELECT COUNT(*) FROM actions WHERE action = 'validate' AND day = ?", (today,)).fetchone()[0]
    paused_today = conn.execute(
        "SELECT COUNT(*) FROM actions WHERE action = 'pause' AND day = ?", (today,)).fetchone()[0]

    recent_actions = [dict(r) for r in conn.execute(
        """SELECT a.action, a.detail, a.created_at, c.id AS creative_id, c.variant, c.product_key,
                  u.account_key, u.number_key
           FROM actions a
           LEFT JOIN uploads u ON u.ad_id = a.object_id
           LEFT JOIN creatives c ON c.id = u.creative_id
           ORDER BY a.id DESC LIMIT 15""")]
    recent_creatives = [dict(r) for r in conn.execute(
        """SELECT c.id, c.product_key, c.variant, c.received_at,
                  (SELECT COUNT(*) FROM uploads u WHERE u.creative_id = c.id AND u.status = 'done') AS numbers,
                  (SELECT COUNT(*) FROM uploads u JOIN actions a ON a.object_id = u.ad_id
                    WHERE u.creative_id = c.id AND a.action = 'validate') AS wins
           FROM creatives c ORDER BY c.id DESC LIMIT 15""")]

    return {
        "numbers": numbers,
        "total_numbers": len(numbers),
        "running": sum(n["state"] == "rodando" for n in numbers),
        "idle": sum(n["state"] == "sem_criativo" for n in numbers),
        "in_bank": in_bank,
        "validated_today": validated_today,
        "paused_today": paused_today,
        "recent_actions": recent_actions,
        "recent_creatives": recent_creatives,
    }
