"""Confere a configuração antes de rodar de verdade. Só lê; não cria nem altera nada.

Verifica: bot e grupo do Telegram, token de cada conta, se a conta de anúncio está
ativa, se cada página está acessível e se cada campanha modelo está do jeito certo
(na conta certa, com um conjunto e nenhum anúncio).
"""
from __future__ import annotations

import requests

from .config import Settings
from .meta import Meta, MetaError

ACCOUNT_STATUS = {1: "ativa", 2: "DESATIVADA", 3: "com pagamento pendente", 7: "em análise de risco",
                  8: "pendente de acerto", 9: "em período de carência", 100: "pendente de encerramento",
                  101: "ENCERRADA"}


def run(settings: Settings) -> bool:
    ok = True
    lines: list[str] = []

    def mark(good: bool, text: str):
        nonlocal ok
        ok = ok and good
        lines.append(f"{'✅' if good else '❌'} {text}")

    # ---------- Telegram ----------
    if not settings.telegram_token:
        mark(False, "TELEGRAM_BOT_TOKEN vazio no .env")
    else:
        base = f"https://api.telegram.org/bot{settings.telegram_token}"
        me = requests.get(f"{base}/getMe", timeout=30).json()
        mark(me.get("ok", False), f"Bot do Telegram: @{me.get('result', {}).get('username', '?')}"
             if me.get("ok") else f"Bot do Telegram: token inválido ({me.get('description')})")
        if not settings.telegram_chat_id:
            mark(False, "TELEGRAM_CHAT_ID vazio no .env (ID do grupo de criativos)")
        else:
            chat = requests.get(f"{base}/getChat", params={"chat_id": settings.telegram_chat_id}, timeout=30).json()
            mark(chat.get("ok", False), f"Grupo: {chat.get('result', {}).get('title', '?')}" if chat.get("ok")
                 else f"Grupo {settings.telegram_chat_id}: bot não está no grupo ou ID errado")

    # ---------- Meta ----------
    for acc_key, acc in settings.accounts.items():
        lines.append(f"\nConta {acc_key} (act_{acc.ad_account_id})")
        if not acc.token:
            mark(False, "  token da Meta vazio no .env")
            continue
        api = Meta(acc.token, settings.graph_version, dry_run=True)  # dry_run: só leitura
        try:
            info = api.get(f"act_{acc.ad_account_id}", fields="name,account_status,currency")
            status = ACCOUNT_STATUS.get(info.get("account_status"), str(info.get("account_status")))
            mark(info.get("account_status") == 1, f"  {info.get('name')} — {status} ({info.get('currency')})")
        except MetaError as e:
            mark(False, f"  sem acesso à conta: {e}")
            continue

        for num_key, num in acc.numbers.items():
            prefix = f"  número {num_key}:"
            try:
                page = api.get(num.page_id, fields="name")
                mark(True, f"{prefix} página {page.get('name')}")
            except MetaError as e:
                mark(False, f"{prefix} sem acesso à página {num.page_id}: {e}")
            try:
                camp = api.get(num.template_campaign_id, fields="name,account_id,bid_strategy,daily_budget")
                adsets = api.get(f"{num.template_campaign_id}/adsets", fields="id").get("data", [])
                ads = api.get(f"{num.template_campaign_id}/ads", fields="id").get("data", [])
                same_account = str(camp.get("account_id")) == acc.ad_account_id
                budget = f"R${int(camp['daily_budget']) / 100:.2f}/dia".replace(".", ",") if camp.get("daily_budget") else "orçamento no conjunto"
                mark(same_account, f"{prefix} campanha modelo '{camp.get('name')}' "
                     f"({camp.get('bid_strategy') or 'lance no conjunto'}, {budget})"
                     + ("" if same_account else " — ESTÁ EM OUTRA CONTA"))
                mark(len(adsets) == 1, f"{prefix} campanha modelo com {len(adsets)} conjunto(s) (precisa ter 1)")
                mark(len(ads) == 0, f"{prefix} campanha modelo com {len(ads)} anúncio(s) (precisa ter 0)")
            except MetaError as e:
                mark(False, f"{prefix} sem acesso à campanha modelo {num.template_campaign_id}: {e}")

    lines.append("")
    lines.append("Tudo certo! Pode rodar." if ok else "Corrija os itens com ❌ antes de rodar.")
    if ok and settings.dry_run:
        lines.append("Lembrete: dry_run está ligado (só simula). Mude para false no config.yaml quando quiser rodar de verdade.")
    print("\n".join(lines))
    return ok
