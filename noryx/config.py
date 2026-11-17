"""Carrega configuração (config.yaml) e segredos (.env)."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from dotenv import load_dotenv


@dataclass
class Product:
    """Um produto/oferta. O criativo enviado no grupo com '#chave' usa estes dados."""

    key: str
    message: str
    link: str = ""  # opcional quando o CTA é WHATSAPP_MESSAGE
    headline: str = ""
    cta: str = "WHATSAPP_MESSAGE"
    accounts: list[str] = field(default_factory=list)  # chaves de contas; vazio = todas


@dataclass
class Account:
    """Uma conta de anúncio do seu Business Manager."""

    key: str
    ad_account_id: str  # sem o prefixo act_
    page_id: str
    template_campaign_id: str  # campanha modelo (bid cap + orçamento) copiada a cada lote de teste
    instagram_user_id: str = ""


@dataclass
class Rules:
    # Resultado que conta (padrão: compra)
    result_action: str = "purchase"
    target_cost: float = 5.0  # custo por compra para o criativo validar
    max_cost: float = 6.0  # acima disso não compensa: pausa
    validate_min_results: int = 3  # compras mínimas para considerar validado
    kill_spend_no_result: float = 10.0  # pausa se gastou isso sem nenhuma compra
    kill_min_spend: float = 12.0  # só julga o custo depois de gastar isso
    pause_others_on_validate: bool = True  # quando um valida, pausa os que não validaram


@dataclass
class Settings:
    meta_token: str
    telegram_token: str
    telegram_chat_id: str
    graph_version: str
    dry_run: bool
    data_dir: Path
    accounts: dict[str, Account]
    products: dict[str, Product]
    default_product: str
    rules: Rules
    test_status: str  # ACTIVE ou PAUSED ao criar os testes
    max_ads_per_campaign: int


def load(path: str | Path = "config.yaml") -> Settings:
    load_dotenv()
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}

    accounts = {k: Account(key=k, **{kk: str(vv) for kk, vv in v.items()}) for k, v in raw.get("accounts", {}).items()}
    products = {k: Product(key=k, **v) for k, v in raw.get("products", {}).items()}
    if not accounts:
        raise ValueError("Configure ao menos uma conta em 'accounts' no config.yaml")
    if not products:
        raise ValueError("Configure ao menos um produto em 'products' no config.yaml")

    default_product = raw.get("default_product") or next(iter(products))
    data_dir = Path(raw.get("data_dir", "data"))
    data_dir.mkdir(parents=True, exist_ok=True)

    return Settings(
        meta_token=os.environ.get("META_ACCESS_TOKEN", ""),
        telegram_token=os.environ.get("TELEGRAM_BOT_TOKEN", ""),
        telegram_chat_id=str(os.environ.get("TELEGRAM_CHAT_ID", raw.get("telegram_chat_id", ""))),
        graph_version=raw.get("graph_version", "v23.0"),
        dry_run=bool(raw.get("dry_run", True)),
        data_dir=data_dir,
        accounts=accounts,
        products=products,
        default_product=default_product,
        rules=Rules(**raw.get("rules", {})),
        test_status=raw.get("test_status", "PAUSED").upper(),
        max_ads_per_campaign=int(raw.get("max_ads_per_campaign", 5)),
    )
