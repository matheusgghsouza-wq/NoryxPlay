# NoryxPlay — esteira automática de testes de criativos (Meta Ads)

Você manda os vídeos **uma vez** num grupo do Telegram. O sistema baixa, sobe em todas as
contas de anúncio e em todos os números de cada conta pela **API oficial da Meta**, e monta o
teste do mesmo jeito que você faz na mão: uma cópia da campanha modelo de cada número
(bid cap, R$100/dia) com um anúncio por criativo. Ex.: 10 contas × 5 números = 50 campanhas
de teste a partir de um único envio no grupo.
Depois ele acompanha: o criativo que valida fica ativo e os outros são pausados.
Tudo é reportado no próprio grupo. Roda num servidor, então sua internet cair não afeta nada.

```
Grupo Telegram ──► collect ──► upload ──► Meta Ads (cópia da campanha modelo,
                                              │            1 anúncio por criativo)
                         relatório ◄── rules ◄┘  (valida o bom, pausa os outros)
```

## 1. Preparar

1. **Bot do Telegram:** fale com o `@BotFather`, crie um bot e copie o token. Adicione o bot ao
   seu grupo de criativos e, no BotFather, desative o *Group Privacy* (`/setprivacy` → Disable)
   para ele ler as mensagens. Para descobrir o ID do grupo, mande uma mensagem lá e abra
   `https://api.telegram.org/bot<TOKEN>/getUpdates`.
2. **Token da Meta:** no Business Manager → Configurações → Usuários do sistema, crie um usuário
   do sistema e dê acesso às contas de anúncio e páginas. Gere um token com `ads_management`,
   `ads_read` e `pages_read_engagement`.
3. **Rastreio de compra:** o sistema decide pelo custo por compra que aparece no seu gerenciador.
   O evento de compra precisa estar chegando na Meta (Pixel ou API de Conversões disparando quando o
   pagamento é confirmado). Se no gerenciador a coluna de compras está preenchida, já está certo.
4. **Campanha modelo por número:** para cada número, crie na conta dele uma campanha pausada do
   jeito que você testa hoje (bid cap, orçamento de R$100, destino WhatsApp daquela página) com
   **um conjunto e nenhum anúncio**. Cada lote de criativos vira uma cópia dela. Anote o ID da
   campanha e o ID da página no `config.yaml`, em `accounts → numbers`.

## 2. Instalar

```bash
python -m venv .venv && source .venv/bin/activate   # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                 # preencha os tokens
cp config.example.yaml config.yaml   # preencha contas, produtos e regras
```

## 3. Usar

No grupo, mande o vídeo com a legenda `#produto descrição`, por exemplo `#dorama gancho final 2`.
Sem hashtag, ele usa o `default_product`.

```bash
python main.py collect   # baixa os vídeos novos do grupo
python main.py upload    # sobe e cria os testes
python main.py rules     # valida o criativo bom e pausa os outros
python main.py run       # faz tudo em loop a cada 15 min (--interval para mudar)
python main.py retry     # tenta de novo os uploads que deram erro
```

**Comece com `dry_run: true`** no `config.yaml`: ele mostra tudo o que faria sem criar nada.
Quando estiver certo, mude para `false`. Se quiser que o sistema só suba os criativos e você
continue validando e pausando na mão, use `auto_rules: false`. Com `test_status: PAUSED`, os testes nascem pausados
pra você revisar antes; com `ACTIVE`, já entram rodando.

## Regras (config.yaml → `rules`)

Valem só para as campanhas criadas pelo sistema; suas campanhas manuais não são tocadas.
Os números contam desde que a campanha de teste foi criada.

| Situação | Ação |
|---|---|
| Pelo menos `validate_min_results` compras a no máximo `target_cost` cada (padrão: 3 compras a até R$5) | 🏆 Validou: fica ativo e você é avisado |
| Custo por compra entre `target_cost` e `max_cost` (R$5 a R$6) | Continua rodando |
| Gastou `kill_spend_no_result` sem nenhuma compra (padrão: R$10) | Pausa |
| Já gastou `kill_min_spend` e o custo por compra passou de `max_cost` (padrão: R$6) | Pausa |
| Outro criativo da mesma campanha validou (`pause_others_on_validate`) | Pausa |

## Limitações atuais

- A Bot API do Telegram em nuvem só baixa arquivos de **até 20 MB**. Vídeos maiores: comprima ou
  rode um servidor local da Bot API.
- Ainda não tem painel web. Por enquanto o acompanhamento é pelo relatório no grupo.
- A versão da Graph API (`graph_version`) deve ser conferida com a versão atual no site da Meta.
