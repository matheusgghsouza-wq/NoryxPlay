# Kit de anúncios: Foco sem Tela (R$ 19,90 + adicional Emoções R$ 29,90)

## Estrutura do teste (R$ 80 em 3 dias)
- **Campanha:** Vendas · Conversão no site · Evento **Compra** (o Pixel do checkout Kiwify/Cakto precisa ser o mesmo da página).
- **Orçamento:** R$ 27/dia no conjunto (ABO), 3 dias.
- **Conjunto:** Brasil · 25 a 55 anos · Público Advantage+ aberto (sem interesses) · posicionamentos Advantage+.
  - Se a plataforma pedir sugestão de público, use: maternidade, educação infantil, atividades para crianças, Montessori.
- **Anúncios:** os 3 criativos (`criativos/`) no mesmo conjunto, cada um com os 5 textos principais e os 5 títulos abaixo (opções múltiplas de texto).
- **Link:** a página na Vercel, com `?utm_source=meta&utm_campaign=foco` no final.

### Quando cortar ou manter
| Momento | Sinal | O que fazer |
|---|---|---|
| Fim do dia 1 (R$ 27) | CTR no link abaixo de 0,8% ou CPC acima de R$ 2,50 | Pausar o criativo com pior CTR |
| Fim do dia 2 (R$ 54) | Nenhum início de checkout | Revisar página e preço antes de gastar o resto |
| Fim do dia 3 (R$ 80) | 2 ou mais vendas (CPA até ~R$ 40 com o adicional) | Duplicar o conjunto e subir para R$ 50/dia |
| Fim do dia 3 | 0 vendas, mas checkout iniciado | Testar checkout e oferta (ex.: R$ 14,90) antes de matar |

## Textos principais (Meta)
> Regra da Meta: não afirmar características da pessoa ou do filho ("seu filho tem dificuldade…"). Os textos abaixo já seguem isso.

**1. Rotina curta**
10 minutos por dia, sem tela. 🧩
O Kit Foco sem Tela traz 102 atividades de atenção para imprimir: labirintos, caça-símbolos, memória, sequências e muito mais.
✅ 4 a 10 anos, em 2 níveis
✅ 24 cartões de foco em movimento
✅ Plano de 4 semanas pronto
PDF por R$ 19,90. Chega no e-mail na hora.

**2. Troca da tela**
Que tal trocar 10 minutos de celular por um labirinto?
São 102 folhas coloridas para imprimir e fazer na mesa da cozinha, com o plano de cada dia já montado.
Imprima quantas vezes quiser. R$ 19,90, pagamento único.

**3. Para professoras**
Atividade de foco para começar a aula ou para quem termina antes.
102 folhas prontas para imprimir, de 4 a 10 anos, com gabarito.
Baixe hoje e use amanhã. R$ 19,90.

**4. Lista do que vem**
O que vem no Kit Foco sem Tela:
🧩 12 caça-símbolos
🌀 12 labirintos
🔢 10 trilhas dos números
✏️ 12 copie o desenho
🧠 8 desafios de memória
… e mais 48 atividades, 24 cartões de movimento, quadro de conquistas e certificado.
Tudo em PDF por R$ 19,90.

**5. Curto**
Foco se treina brincando. 102 atividades para imprimir, 10 minutos por dia, sem tela. R$ 19,90.

## Títulos
1. 102 atividades de foco para imprimir
2. 10 minutos por dia, sem tela
3. Kit Foco sem Tela por R$ 19,90
4. Labirintos, memória e muito mais
5. Baixe hoje, imprima agora

## Descrição
PDF para imprimir · 4 a 10 anos · Garantia de 7 dias

## Botão
Comprar agora

## Checkout (Kiwify ou Cakto)
- **Produto principal:** Kit Foco sem Tela · R$ 19,90 · entregar `produto/foco-sem-tela.pdf`.
- **Order bump:** Kit Emoções em Jogo · R$ 29,90 · entregar `produto/emocoes-em-jogo.pdf`.
  - Texto do bump: "Sim! Quero também o Kit Emoções em Jogo: 25 folhas e 12 cartões da calma para a criança dar nome ao que sente. De R$ 47 por R$ 29,90."
- Pixel: cadastre o mesmo Pixel da página no checkout, com o evento Compra.

## Pixel na página
Em `site/index.html`, procure `var PIXEL_ID = '';` e coloque o número do pixel entre as aspas. A página dispara PageView, ViewContent e InitiateCheckout (no clique do botão).

## Fotos realistas (Gemini / ChatGPT)
Gere em 1:1 (1080x1080) e me mande para eu colocar na galeria (no lugar de `5-imprima.jpg` e como 2ª e 3ª fotos):
1. *"Foto realista, luz natural de janela, mesa de cozinha de madeira clara, menina de 6 anos brasileira fazendo uma folha de atividade de labirinto colorida com lápis, vista de cima a 45 graus, ao lado um relógio de cozinha em forma de tomate, estilo foto de Instagram de mãe, sem rostos em close, sem texto."*
2. *"Foto realista vista de cima de várias folhas de atividades infantis coloridas espalhadas sobre uma mesa branca, com lápis de cor, um estojo e uma ampulheta, luz suave, estilo flat lay."*
3. *"Foto realista de mãe e filho de 8 anos sentados à mesa da sala fazendo juntos uma folha de atividades em papel, celular virado para baixo na mesa ao lado, luz quente de fim de tarde, ambiente brasileiro simples."*
