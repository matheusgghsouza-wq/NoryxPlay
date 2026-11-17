# NoryxPlay — esteira automática de testes de criativos (Meta Ads)

Você manda os vídeos num grupo do Telegram. O sistema baixa, sobe nas suas contas de
anúncio pela **API oficial da Meta**, cria um conjunto de teste para cada criativo e depois
pausa os ruins e escala os bons sozinho. Tudo é reportado no próprio grupo.

```
Grupo Telegram ──► collect ──► upload ──► Meta Ads (conjunto de teste por criativo)
                                              │
                         relatório ◄── rules ◄┘  (pausa / escala por CPA)
```

## 1. Preparar

1. **Bot do Telegram:** fale com o `@BotFather`, crie um bot e copie o token. Adicione o bot ao
   seu grupo de criativos e, no BotFather, desative o *Group Privacy* (`/setprivacy` → Disable)
   para ele ler as mensagens. Para descobrir o ID do grupo, mande uma mensagem lá e abra
   `https://api.telegram.org/bot<TOKEN>/getUpdates`.
2. **Token da Meta:** no Business Manager → Configurações → Usuários do sistema, crie um usuário
   do sistema e dê acesso às contas de anúncio e páginas. Gere um token com `ads_management`,
   `ads_read` e `pages_read_engagement`.
3. **Conjunto modelo:** em cada conta, crie uma campanha de teste (ABO) com **um conjunto modelo**
   já configurado (pixel, evento, público, posicionamentos, orçamento diário). Cada criativo novo
   vira uma cópia desse conjunto. Copie o ID dele.

## 2. Instalar

```bash
python -m venv .venv && source .venv/bin/activate   # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                 # preencha os tokens
cp config.example.yaml config.yaml   # preencha contas, produtos e regras
```

## 3. Usar

No grupo, mande o vídeo com a legenda `#produto descrição`, por exemplo `#produtox gancho dor 2`.
Sem hashtag, ele usa o `default_product`.

```bash
python main.py collect   # baixa os vídeos novos do grupo
python main.py upload    # sobe e cria os testes
python main.py rules     # aplica as regras de pausa/escala
python main.py run       # faz tudo em loop a cada 15 min (--interval para mudar)
python main.py retry     # tenta de novo os uploads que deram erro
```

**Comece com `dry_run: true`** no `config.yaml`: ele mostra tudo o que faria sem criar nada.
Quando estiver certo, mude para `false`. Com `test_status: PAUSED`, os testes nascem pausados
pra você revisar antes; com `ACTIVE`, já entram rodando.

## Regras (config.yaml → `rules`)

Valem só para os conjuntos criados pelo sistema; suas campanhas manuais não são tocadas.
Métricas do dia:

| Situação | Ação |
|---|---|
| Gastou `kill_spend_multiplier` × CPA alvo sem nenhuma venda | Pausa |
| CPA acima de `kill_cpa_multiplier` × CPA alvo | Pausa |
| CPA ≤ alvo e pelo menos `scale_min_conversions` vendas | +`scale_pct`% de orçamento (1× por dia, até `max_daily_budget`) |

## Limitações atuais

- A Bot API do Telegram em nuvem só baixa arquivos de **até 20 MB**. Vídeos maiores: comprima ou
  rode um servidor local da Bot API.
- Ainda não tem painel web. Por enquanto o acompanhamento é pelo relatório no grupo.
- A versão da Graph API (`graph_version`) deve ser conferida com a versão atual no site da Meta.
