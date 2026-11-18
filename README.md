# NoryxPlay — esteira automática de testes de criativos (Meta Ads)

Você manda os vídeos **uma vez** pelo painel no celular (ou pelo grupo do Telegram). O sistema baixa, sobe em todas as
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

## 1. Preparar (uma vez só)

### 1.1 Bot do Telegram
1. No Telegram, fale com o `@BotFather` → `/newbot` → escolha um nome. Copie o **token**.
2. Ainda no BotFather: `/setprivacy` → escolha o bot → **Disable** (para ele ler o grupo).
3. Adicione o bot ao seu grupo de criativos.
4. Mande qualquer mensagem no grupo e abra `https://api.telegram.org/bot<TOKEN>/getUpdates`
   no navegador. O número em `"chat":{"id": -100...}` é o **ID do grupo**.

### 1.2 App no Meta for Developers
1. Acesse **developers.facebook.com** → **Meus apps** → **Criar app**.
2. Tipo/caso de uso: **Outro** → **Empresa** (Business). Dê um nome (ex.: "Noryx") e, em
   "Portfólio empresarial", escolha o **seu Business Manager**.
3. No painel do app, em **Adicionar produtos**, adicione **Marketing API**.
4. O app pode ficar no modo de desenvolvimento e **não precisa passar por revisão** para mexer nas
   contas do seu próprio Business Manager.

### 1.3 Usuário do sistema e token (não expira)
1. Acesse **business.facebook.com/settings** → **Usuários** → **Usuários do sistema** → **Adicionar**.
   Nome "noryx", função **Administrador**.
2. Selecione o usuário → **Atribuir ativos**:
   - **Contas de anúncios**: marque todas as que o sistema vai usar → controle total.
   - **Páginas**: marque as páginas dos números → controle total.
3. Ainda no usuário → **Gerar novo token** → escolha o app criado → validade **Nunca**. Marque:
   `ads_management`, `ads_read`, `business_management`, `pages_read_engagement`,
   `pages_show_list`.
4. Copie o token e cole no `.env` em `META_ACCESS_TOKEN=`. **Não mande esse token pra ninguém**:
   quem tem ele mexe nas suas contas.
5. Contas em outro Business Manager: repita 1.2 e 1.3 nele, coloque o token no `.env` com outro
   nome (ex.: `META_TOKEN_BM2=`) e, no `config.yaml`, use `token_env: META_TOKEN_BM2` nessas contas.

> Os nomes dos menus da Meta mudam de vez em quando. Se algo não bater, procure pelo mesmo
> conceito (app empresarial, usuário do sistema, atribuir ativos, gerar token).

### 1.4 Rastreio de compra
O sistema decide pelo custo por compra que aparece no seu gerenciador. O evento de compra precisa
estar chegando na Meta (Pixel ou API de Conversões disparando quando o pagamento é confirmado).
Se a coluna **Compras** está preenchida no gerenciador, já está certo.

### 1.5 Campanha modelo por número
Para cada número, crie na conta dele uma campanha **pausada** do jeito que você testa hoje
(bid cap, R$100/dia, destino WhatsApp daquela página) com **um conjunto e nenhum anúncio**.
Cada lote de criativos vira uma cópia dela.

Onde achar os IDs:
- **Conta de anúncio**: no gerenciador, no seletor de contas (número abaixo do nome). Use sem `act_`.
- **Campanha modelo**: na aba Campanhas, ative a coluna **ID da campanha** (Colunas → Personalizar).
- **Página**: na página → **Sobre** → **Transparência da página** (ou em business.facebook.com/settings → Páginas).

Preencha tudo no `config.yaml`, em `accounts → numbers`.

## 2. Instalar

### No seu computador (para testar)
```bash
python -m venv .venv && source .venv/bin/activate   # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                 # preencha os tokens
cp config.example.yaml config.yaml   # preencha contas, números, produtos e regras
python main.py check                 # confere se está tudo certo
```

O `check` só lê, não cria nada. Ele mostra ✅ ou ❌ para o bot, o grupo, cada conta, cada página e
cada campanha modelo (se está na conta certa, com 1 conjunto e 0 anúncios).

### Na VPS (para rodar 24h)
Qualquer VPS Ubuntu/Debian pequena serve (1 vCPU, 1 GB de RAM). Como root, na VPS:
```bash
curl -O https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPO/main/deploy/instalar-vps.sh
bash instalar-vps.sh https://github.com/SEU_USUARIO/SEU_REPO.git
```
O script instala tudo em `/opt/noryx` e mostra os próximos passos: preencher `.env` e
`config.yaml`, rodar o `check` e ligar o serviço (`systemctl enable --now noryx`). O serviço
reinicia sozinho se cair ou se a VPS reiniciar. Para acompanhar: `journalctl -u noryx -f`.
Se o repositório for privado, clone com um token de acesso do GitHub.

## Painel (enviar vídeos pelo celular)

O jeito mais fácil de mandar criativo. Abra o painel no celular, toque em **Enviar criativos**,
escolha os vídeos da galeria (pode vários de uma vez) e pronto: eles vão para o banco.

Na tela inicial você vê:
- quantos números estão **rodando** e quantos estão **parados sem criativo**;
- quantos criativos estão no banco esperando vez;
- o que **validou** e o que foi **pausado**, com horário (de Brasília);
- os últimos criativos e em quantos números cada um está.

Para ligar: coloque uma senha em `PANEL_PASSWORD` no `.env` e rode `python main.py web`
(na VPS, o serviço `noryx-web` já faz isso). Acesse `http://IP_DA_VPS:8080`.
No celular, use **Adicionar à tela inicial** no menu do navegador para abrir como um aplicativo.

- Aceita MP4 e MOV de até 1 GB (no Telegram o limite é 20 MB).
- Para acesso com cadeado (HTTPS), aponte um domínio para a VPS e use o Caddy na frente do painel.

## 3. Usar

No grupo, mande o vídeo com a legenda `#produto descrição`, por exemplo `#dorama gancho final 2`.
Sem hashtag, ele usa o `default_product`.

```bash
python main.py check     # confere tokens, contas, páginas e campanhas modelo
python main.py collect   # baixa os vídeos novos do grupo
python main.py upload    # repõe criativos nos números sem anúncio ativo
python main.py rules     # valida o criativo bom e pausa os outros
python main.py run       # faz tudo em loop a cada 15 min (--interval para mudar)
python main.py retry     # tenta de novo os uploads que deram erro
```

**Comece com `dry_run: true`** no `config.yaml`: ele mostra tudo o que faria sem criar nada.
Quando estiver certo, mude para `false`. Se quiser que o sistema só suba os criativos e você
continue validando e pausando na mão, use `auto_rules: false`. Com `test_status: PAUSED`, os testes nascem pausados
pra você revisar antes; com `ACTIVE`, já entram rodando.

## Banco de criativos e reposição automática

Tudo que você manda no grupo vai para um **banco**. A cada ciclo (padrão: 15 min):

1. As regras rodam e pausam o que não vendeu (ou você pausa na mão, se usar `auto_rules: false`).
2. O sistema confere cada número. Se um número **não tem mais nenhum anúncio ativo**, ele pega os
   próximos criativos do banco que ainda não foram testados naquele número e solta uma campanha
   nova (cópia da campanha modelo do número).
3. Criativo que **validou em qualquer número** tem prioridade para ir aos outros.
4. Se não tiver criativo novo pra algum número parado, chega no grupo:
   `⚠️ 2 número(s) parado(s) sem criativo novo pra testar: conta1/n3, conta4/n1. Manda mais criativos no grupo.`
   (no máximo uma vez por dia para os mesmos números)

Campanha criada pausada esperando você ligar **não** conta como parada, então o sistema não fica
criando campanha em cima de campanha.

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
- A versão da Graph API (`graph_version`) deve ser conferida com a versão atual no site da Meta.
