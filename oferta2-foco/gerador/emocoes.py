# Gera o HTML da oferta adicional "Emoções em Jogo".
import random, sys
from comum import *
R = random.Random(77)
MARCA = "Emoções em Jogo · Foco sem Tela"
EMO = {  # nome: (cor da pele do rosto, boca, olhos, sobrancelhas, cor)
 'alegria':  ('#ffd34d', 'M32 62 Q50 80 68 62', 'n', '', '#e0930c'),
 'tristeza': ('#9fd8ff', 'M34 72 Q50 60 66 72', 'n', 'M28 34 L40 30 M72 34 L60 30', '#2b7fd6'),
 'raiva':    ('#ff8a7a', 'M34 70 Q50 62 66 70', 'n', 'M28 30 L42 38 M72 30 L58 38', '#e4572e'),
 'medo':     ('#cdb0ff', 'M38 70 Q44 64 50 70 Q56 76 62 70', 'g', 'M28 30 Q34 24 42 30 M72 30 Q66 24 58 30', '#8b46b0'),
 'surpresa': ('#ffbb7a', 'O', 'g', 'M28 28 Q35 22 42 28 M72 28 Q65 22 58 28', '#c2410c'),
 'calma':    ('#aee8a6', 'M36 64 Q50 72 64 64', 'f', '', '#25a065'),
}
NOME_EMO = {'alegria':'Alegria','tristeza':'Tristeza','raiva':'Raiva','medo':'Medo','surpresa':'Surpresa','calma':'Calma'}
def rosto(e, tam="30mm", vazio=False):
    pele, boca, olhos, sob, _ = EMO[e]
    if vazio:
        return f'<svg viewBox="0 0 100 100" style="width:{tam};height:{tam}"><circle cx="50" cy="50" r="44" fill="#fff" stroke="{TINTA}" stroke-width="3"/></svg>'
    o = ''
    if olhos == 'n': o = '<circle cx="36" cy="44" r="5" fill="#1b2232"/><circle cx="64" cy="44" r="5" fill="#1b2232"/>'
    elif olhos == 'g': o = '<circle cx="36" cy="44" r="8" fill="#fff" stroke="#1b2232" stroke-width="3"/><circle cx="36" cy="45" r="3.5" fill="#1b2232"/><circle cx="64" cy="44" r="8" fill="#fff" stroke="#1b2232" stroke-width="3"/><circle cx="64" cy="45" r="3.5" fill="#1b2232"/>'
    else: o = '<path d="M29 45 Q36 51 43 45 M57 45 Q64 51 71 45" stroke="#1b2232" stroke-width="3.4" fill="none" stroke-linecap="round"/>'
    b = '<ellipse cx="50" cy="70" rx="7" ry="9" fill="#1b2232"/>' if boca == 'O' else f'<path d="{boca}" stroke="#1b2232" stroke-width="3.6" fill="none" stroke-linecap="round"/>'
    s = f'<path d="{sob}" stroke="#1b2232" stroke-width="3.4" fill="none" stroke-linecap="round"/>' if sob else ''
    bochecha = '<circle cx="26" cy="60" r="6" fill="#ff9db0" opacity=".6"/><circle cx="74" cy="60" r="6" fill="#ff9db0" opacity=".6"/>' if e in ('alegria','calma') else ''
    lagrima = '<path d="M66 54 Q62 62 66 66 Q70 62 66 54Z" fill="#2b7fd6"/>' if e == 'tristeza' else ''
    return f'<svg viewBox="0 0 100 100" style="width:{tam};height:{tam}"><circle cx="50" cy="50" r="44" fill="{pele}" stroke="{TINTA}" stroke-width="3"/>{bochecha}{o}{s}{b}{lagrima}</svg>'

paginas = []
def pag(titulo, cat, cor, corpo, nivel=None):
    n = len(paginas)+1
    dir_ = f'<div class="dir"><span class="pill">{esc(nivel)}</span></div>' if nivel else ''
    paginas.append(f'''<section class="page">{onda(cor, cor+"99")}<div class="cab"><div><div class="cat">{esc(cat)}</div><h1>{esc(titulo)}</h1></div>{dir_}</div>
<div class="corpo">{corpo}</div><div class="rod"><span>{esc(MARCA)}</span><span class="pg">{n}</span></div></section>''')

NOMEDATA = '<div class="nd"><span>Nome:</span><span class="c">Data:</span></div>'
def instr(cor, t): return f'<div class="ins" style="background:{cor}22"><b style="background:{cor}">!</b><div>{t}</div></div>'

# capa
paginas.append(f'''<section class="page capa"><div class="faces">{''.join(rosto(e,"34mm") for e in EMO)}</div>
<div class="cbox"><div class="selo">Kit para imprimir</div><h1>Emoções<br>em Jogo</h1><p>Atividades para a criança dar nome ao que sente e aprender jeitos de se acalmar</p>
<div class="tags"><span>25 folhas de atividades</span><span>12 cartões da calma</span><span>4 a 10 anos</span></div></div></section>''')
pag("Como usar", "Emoções em Jogo", "#2b7fd6", '''<div class="lista">
<p><b>1. Faça junto.</b> Estas folhas funcionam melhor com um adulto por perto, conversando. Não existe resposta errada sobre o que alguém sente.</p>
<p><b>2. Uma por dia, em 10 minutos.</b> Combine com uma folha do kit Foco sem Tela, ou use sozinho.</p>
<p><b>3. Nomeie a emoção.</b> Dizer “você está com raiva porque…” ajuda a criança a reconhecer o que sente.</p>
<p><b>4. Toda emoção é permitida.</b> O que a gente aprende é o que fazer com ela. As páginas da calma ajudam nisso.</p>
<p><b>5. Imprima de novo.</b> O diário e o termômetro podem ser usados toda semana.</p></div>
<div class="aviso">Este é um material educativo e lúdico. Não é terapia e não substitui o acompanhamento de psicólogo ou outro profissional quando ele for necessário.</div>''')
# conheça
pag("Conheça as emoções", "Emoções em Jogo", "#e4572e", '<div class="g6">' + ''.join(f'<div class="cf">{rosto(e,"40mm")}<h3 style="color:{EMO[e][4]}">{NOME_EMO[e]}</h3></div>' for e in EMO) + '</div>')
# uma página por emoção
CORPO = {'alegria':['sorriso no rosto','vontade de pular','coração quentinho','vontade de abraçar'], 'tristeza':['vontade de chorar','corpo pesado','vontade de ficar quieto','aperto no peito'],
 'raiva':['rosto quente','mãos fechadas','vontade de gritar','coração acelerado'], 'medo':['barriga gelada','vontade de fugir','mãos suadas','coração acelerado'],
 'surpresa':['olhos arregalados','boca aberta','pulo de susto','vontade de contar para alguém'], 'calma':['respiração devagar','corpo leve','ombros soltos','vontade de descansar']}
for e in EMO:
    c = EMO[e][4]
    pag(f"Quando eu sinto {NOME_EMO[e].lower()}", "Minhas emoções", c, NOMEDATA + f'''<div class="emo1">{rosto(e,"42mm")}<div class="caixa grande"><b>Desenhe uma vez em que você sentiu {NOME_EMO[e].lower()}:</b></div></div>
<div class="caixa"><b>No meu corpo eu sinto… (marque)</b><div class="chk">{''.join(f'<span>☐ {x}</span>' for x in CORPO[e])}<span>☐ outra coisa: ______</span></div></div>
<div class="caixa"><b>{"O que me ajuda quando sinto isso:" if e not in ("alegria","calma","surpresa") else "Com quem eu gosto de dividir esse sentimento:"}</b><div class="linhas"><i></i><i></i></div></div>''')
# ligue
for k in range(4):
    es = R.sample(list(EMO), 5 if k < 2 else 6); ns = es[:]; R.shuffle(ns)
    pag("Ligue a carinha ao nome", "Reconhecer", "#d6457a", NOMEDATA + instr("#d6457a", "Ligue cada carinha ao nome da emoção. Depois, faça a mesma cara no espelho!") +
        '<div class="ligue"><div>' + ''.join(f'<div class="li">{rosto(e,"24mm")}<span class="pt"></span></div>' for e in es) + '</div><div>' +
        ''.join(f'<div class="li dir"><span class="pt"></span><b>{NOME_EMO[e]}</b></div>' for e in ns) + '</div></div>', "Nível 1" if k < 2 else "Nível 2")
# situações
SIT = ["Ganhou um presente surpresa","O sorvete caiu no chão","O irmão pegou o brinquedo sem pedir","Ouviu um barulho forte no escuro","Terminou o desenho que queria","Deitou na rede depois de brincar",
 "O amigo não quis brincar","Foi chamado para o palco na escola","A vovó chegou para visitar","Perdeu o jogo","Achou o brinquedo que estava perdido","Ficou olhando as nuvens no céu",
 "Alguém riu do seu desenho","O cachorro latiu de repente","Foi ao parque com a família","Precisou esperar muito na fila","Recebeu um abraço apertado","Teve um pesadelo",
 "Ganhou um elogio da professora","Brincou de massinha em silêncio","Quebrou o brinquedo favorito","Foi dormir na casa do primo pela primeira vez","Viu um arco-íris","Não conseguiu montar o quebra-cabeça"]
for k in range(4):
    linhas = ''.join(f'<div class="sit"><p>{esc(SIT[k*6+i])}</p><div class="op">{"".join(rosto(e,"13mm") for e in EMO)}</div></div>' for i in range(6))
    pag("Como ele se sentiria?", "Situações", "#14918f", NOMEDATA + instr("#14918f", "Leia (ou escute) cada situação e circule a carinha de como a criança poderia se sentir. Pode ter mais de uma resposta!") + linhas)
# desenhe a carinha
for k in range(2):
    es = list(EMO) if k == 0 else ['alegria','raiva','surpresa','medo','tristeza','calma']
    pag("Desenhe a carinha", "Expressar", "#e0930c", NOMEDATA + instr("#e0930c", "Desenhe olhos, boca e sobrancelhas para mostrar cada emoção.") +
        '<div class="g6">' + ''.join(f'<div class="cf">{rosto(e,"44mm",True)}<h3>{NOME_EMO[e]}</h3></div>' for e in es) + '</div>')
# termômetro
pag("Termômetro das emoções", "Medir", "#e4572e", NOMEDATA + instr("#e4572e", "Pinte até onde está a sua emoção agora. Quanto mais alto, mais forte. No vermelho, é hora de usar uma técnica da calma.") +
    '<div class="termo"><div class="tubo">' + ''.join(f'<div class="nivel" style="background:{c}"><span>{n}</span><b>{t}</b></div>' for n, c, t in [(5,'#e4572e','Muito forte: preciso de ajuda para me acalmar'),(4,'#f39a7d','Forte: vou respirar fundo'),(3,'#f2c56d','Médio: posso contar como me sinto'),(2,'#aee8a6','Fraco: estou bem'),(1,'#9fd8ff','Tranquilo: estou calmo')]) + '</div></div>')
# semáforo
pag("Semáforo da calma", "Regular", "#25a065", NOMEDATA + '<div class="sema">' + ''.join(f'<div class="sl"><span class="luz" style="background:{c}"></span><div><h3>{t}</h3><p>{d}</p></div></div>' for c, t, d in [
    ('#e4572e', 'PARE', 'Percebi que a emoção ficou forte. Paro o que estou fazendo e não bato, não grito, não jogo nada.'),
    ('#f2a516', 'PENSE', 'Respiro fundo 3 vezes. Que emoção é essa? O que aconteceu?'),
    ('#25a065', 'SIGA', 'Escolho o que fazer: pedir ajuda, conversar, ir para o cantinho da calma ou tentar de novo.')]) + '</div><div class="caixa"><b>Uma vez em que eu usei o semáforo:</b><div class="linhas"><i></i><i></i><i></i></div></div>')
# cantinho da calma
TEC = [("Cheire a flor, sopre a vela","Puxe o ar pelo nariz como quem cheira uma flor e solte pela boca como quem apaga uma vela.","flor"),
 ("Respiração do quadrado","Puxe o ar contando 4, segure 4, solte 4, espere 4. Siga os lados de um quadrado com o dedo.","quadrado"),
 ("Abraço de urso","Abrace você mesmo bem forte e conte até 10 devagar.","coracao"),
 ("Conte até 10","Conte devagar até 10. Se precisar, conte de novo de 10 até 1.","estrela"),
 ("5 coisas que eu vejo","Olhe em volta e diga 5 coisas que você está vendo agora.","sol"),
 ("Beba água","Beba um copo de água em goles pequenos, bem devagar.","gota")]
pag("Cantinho da calma", "Regular", "#5a5fd1", instr("#5a5fd1", "Recorte e cole no lugar da casa onde a criança vai para se acalmar.") + '<div class="tec">' + ''.join(f'<div class="t">{icone_svg(i,"16mm")}<div><h3>{esc(a)}</h3><p>{esc(b)}</p></div></div>' for a, b, i in TEC) + '</div>')
# cartões
CART = ["Respire como um balão: encha devagar e esvazie devagar","Aperte uma almofada bem forte e solte","Faça 5 pulinhos e depois fique parado","Desenhe como você se sente agora",
 "Conte para alguém o que aconteceu","Escute uma música calma de olhos fechados","Faça carinho em um bicho de pelúcia","Lave o rosto com água fresquinha",
 "Sopre bolhas de sabão imaginárias","Espreguice como um gato","Diga: eu estou com ___ e vai passar","Peça um abraço"]
cores = ['#e4572e','#2b7fd6','#25a065','#8b46b0','#e0930c','#d6457a']
pag("Cartões da calma", "Regular", "#1b2232", '<p class="int">Recorte e guarde num potinho. Quando precisar, sorteie um cartão.</p><div class="cartoes">' +
    ''.join(f'<div class="ct" style="--c:{cores[i%6]}"><div class="ctt"><span>{i+1}</span>Calma</div><div class="ctb">{rosto("calma","14mm")}<p>{esc(t)}</p></div></div>' for i, t in enumerate(CART)) + '</div>')
# roda das emoções
import math
fatias = ''
for i, e in enumerate(EMO):
    a0 = i*60 - 90; a1 = a0 + 60
    x0, y0 = 100+90*math.cos(math.radians(a0)), 100+90*math.sin(math.radians(a0)); x1, y1 = 100+90*math.cos(math.radians(a1)), 100+90*math.sin(math.radians(a1))
    am = math.radians(a0+30); tx, ty = 100+62*math.cos(am), 100+62*math.sin(am)
    fatias += f'<path d="M100 100 L{x0:.1f} {y0:.1f} A90 90 0 0 1 {x1:.1f} {y1:.1f}Z" fill="{EMO[e][0]}" stroke="{TINTA}" stroke-width="1.5"/><text x="{tx:.1f}" y="{ty:.1f}" text-anchor="middle" font-family="Baloo 2" font-weight="800" font-size="12" fill="{TINTA}">{NOME_EMO[e]}</text>'
pag("Roda das emoções", "Medir", "#8b46b0", instr("#8b46b0", "Recorte a roda e a seta. Prenda a seta no meio com um colchete. Gire para mostrar como você está se sentindo.") +
    f'<div class="roda"><svg viewBox="0 0 200 200" style="width:150mm;height:150mm">{fatias}<circle cx="100" cy="100" r="6" fill="#fff" stroke="{TINTA}" stroke-width="1.5"/></svg>'
    f'<svg viewBox="0 0 30 100" style="width:12mm;height:45mm"><path d="M15 4 L27 30 H19 V96 H11 V30 H3Z" fill="#fff" stroke="{TINTA}" stroke-width="1.6" stroke-dasharray="3 2"/></svg></div>')
# diário semanal
for k in range(2):
    dias = ['Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo']
    pag("Diário das emoções", "Semana", "#2b7fd6", NOMEDATA + instr("#2b7fd6", "Todo dia, circule a carinha de como foi seu dia e escreva ou desenhe por quê.") +
        '<div class="diario">' + ''.join(f'<div class="dl"><b>{d}</b><div class="op">{"".join(rosto(e,"9mm") for e in EMO)}</div><span></span></div>' for d in dias) + '</div>')
# memória
pag("Jogo da memória das emoções", "Jogar", "#d6457a", '<p class="int">Imprima duas vezes, recorte as cartas e jogue. Quando achar um par, faça a cara da emoção!</p><div class="mem">' +
    ''.join(f'<div class="mc">{rosto(e,"30mm")}<b>{NOME_EMO[e]}</b></div>' for e in list(EMO)*2) + '</div>')
# certificado
paginas.append(f'''<section class="page cert"><div class="borda"><div class="faces2">{''.join(rosto(e,"16mm") for e in EMO)}</div>
<h1>Certificado<br>Expert em Emoções</h1><p>Este certificado é de</p><div class="linha-n"></div><p>que aprendeu a dar nome ao que sente<br>e a cuidar das próprias emoções!</p>
<div class="ass"><div><span></span>Data</div><div><span></span>Assinatura do adulto</div></div></div></section>''')

CSS = CSS_BASE + """
.corpo { position:absolute; left:15mm; right:15mm; top:46mm; bottom:17mm; display:flex; flex-direction:column; gap:4mm; }
.nd { display:flex; gap:8mm; font-weight:700; font-size:11pt; } .nd span { flex:1; border-bottom:1.6px solid #1b2232; padding-bottom:.6mm; } .nd .c { flex:.45; }
.ins { display:flex; gap:3.5mm; align-items:center; border-radius:4mm; padding:3mm 4.5mm; font-size:12pt; font-weight:700; line-height:1.3; }
.ins > b { font-family:'Baloo 2'; color:#fff; width:9mm; height:9mm; border-radius:50%; display:flex; align-items:center; justify-content:center; flex:none; font-size:14pt; }
.capa { background:#fff8ee; } .capa .faces { position:absolute; top:16mm; left:0; right:0; display:flex; flex-wrap:wrap; justify-content:center; gap:6mm 10mm; padding:0 25mm; }
.cbox { position:absolute; left:26mm; right:26mm; top:120mm; background:#fff; border:3px solid #1b2232; border-radius:10mm; padding:11mm 9mm; text-align:center; box-shadow:0 3mm 0 #1b2232; }
.cbox .selo { display:inline-block; background:#8b46b0; color:#fff; font-weight:800; font-size:11pt; border-radius:10mm; padding:1.5mm 5mm; text-transform:uppercase; letter-spacing:.06em; }
.cbox h1 { font-family:'Baloo 2'; font-size:58pt; line-height:.9; margin:5mm 0 3mm; } .cbox p { font-size:14pt; font-weight:700; color:#3a4354; margin:0; line-height:1.3; }
.tags { display:flex; justify-content:center; gap:3mm; margin-top:6mm; } .tags span { background:#f1e7f7; color:#8b46b0; font-weight:800; border-radius:4mm; padding:2mm 3.5mm; font-size:11pt; }
.lista p { font-size:12.5pt; line-height:1.45; margin:0 0 4mm; color:#3a4354; } .lista b { color:#1b2232; }
.aviso { background:#fff8ee; border-radius:4mm; padding:4mm 5mm; font-size:10.5pt; color:#3a4354; }
.g6 { display:grid; grid-template-columns:1fr 1fr; gap:6mm; flex:1; }
.cf { border:2px solid #1b2232; border-radius:6mm; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:2mm; }
.cf h3 { font-family:'Baloo 2'; font-size:20pt; margin:0; }
.emo1 { display:flex; gap:5mm; align-items:stretch; } .emo1 > svg { flex:none; align-self:center; }
.caixa { border:2px solid #1b2232; border-radius:5mm; padding:4mm 5mm; font-size:12pt; } .caixa.grande { flex:1; height:96mm; }
.chk { display:grid; grid-template-columns:1fr 1fr; gap:3mm; margin-top:3mm; font-size:12pt; font-weight:600; }
.linhas i { display:block; border-bottom:1.4px solid #9aa2b1; height:13mm; }
.ligue { display:flex; justify-content:space-between; flex:1; padding:2mm 8mm; } .ligue > div { display:flex; flex-direction:column; justify-content:space-around; }
.li { display:flex; align-items:center; gap:6mm; } .li .pt { width:4mm; height:4mm; border-radius:50%; background:#1b2232; } .li b { font-family:'Baloo 2'; font-size:20pt; }
.sit { border:2px solid #1b2232; border-radius:5mm; padding:3mm 4mm; display:flex; flex-direction:column; gap:2mm; } .sit p { margin:0; font-weight:800; font-size:12.5pt; }
.op { display:flex; gap:4mm; }
.termo { flex:1; display:flex; justify-content:center; } .tubo { width:150mm; display:flex; flex-direction:column; gap:2mm; }
.nivel { border:2px solid #1b2232; border-radius:5mm; height:30mm; display:flex; align-items:center; gap:5mm; padding:0 6mm; }
.nivel span { font-family:'Baloo 2'; font-size:30pt; font-weight:800; width:14mm; height:14mm; background:#fff; border-radius:50%; display:flex; align-items:center; justify-content:center; border:2px solid #1b2232; } .nivel b { font-size:13pt; }
.sema { display:flex; flex-direction:column; gap:5mm; } .sl { display:flex; gap:6mm; align-items:center; border:2px solid #1b2232; border-radius:6mm; padding:5mm; }
.luz { width:30mm; height:30mm; border-radius:50%; flex:none; border:3px solid #1b2232; } .sl h3 { font-family:'Baloo 2'; font-size:24pt; margin:0; } .sl p { margin:0; font-size:12pt; color:#3a4354; }
.tec { display:grid; grid-template-columns:1fr 1fr; gap:4mm; flex:1; } .t { border:2px dashed #5a5fd1; border-radius:5mm; padding:4mm; display:flex; flex-direction:column; align-items:center; text-align:center; gap:2mm; }
.t h3 { font-family:'Baloo 2'; font-size:15pt; margin:0; line-height:1.1; } .t p { margin:1mm 0 0; font-size:11pt; color:#3a4354; }
.int { font-size:12pt; font-weight:600; color:#3a4354; margin:0; }
.cartoes { display:grid; grid-template-columns:repeat(3,1fr); grid-auto-rows:53mm; border-top:1.2px dashed #6a7384; border-left:1.2px dashed #6a7384; }
.ct { border-right:1.2px dashed #6a7384; border-bottom:1.2px dashed #6a7384; padding:2.5mm; display:flex; flex-direction:column; }
.ctt { background:var(--c); color:#fff; border-radius:3mm 3mm 0 0; font-family:'Baloo 2'; font-weight:800; font-size:12pt; padding:1.2mm 3mm; display:flex; gap:2mm; align-items:center; }
.ctt span { background:#fff; color:var(--c); border-radius:50%; width:6mm; height:6mm; font-size:9.5pt; display:flex; align-items:center; justify-content:center; }
.ctb { border:2px solid var(--c); border-top:0; border-radius:0 0 3mm 3mm; flex:1; padding:2mm 3mm; display:flex; flex-direction:column; align-items:center; gap:1.5mm; text-align:center; } .ctb p { margin:0; font-size:10.5pt; font-weight:600; line-height:1.3; }
.roda { display:flex; align-items:center; justify-content:center; gap:8mm; flex:1; }
.diario { display:flex; flex-direction:column; gap:2.5mm; } .dl { border:2px solid #1b2232; border-radius:4mm; padding:2mm 4mm; display:grid; grid-template-columns:24mm auto 1fr; gap:4mm; align-items:center; height:24mm; }
.dl b { font-family:'Baloo 2'; font-size:13pt; } .dl > span { border-bottom:1.4px solid #9aa2b1; height:12mm; } .dl .op { gap:1.5mm; }
.mem { display:grid; grid-template-columns:repeat(3,1fr); grid-auto-rows:54mm; border-top:1.2px dashed #6a7384; border-left:1.2px dashed #6a7384; }
.mc { border-right:1.2px dashed #6a7384; border-bottom:1.2px dashed #6a7384; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:2mm; } .mc b { font-family:'Baloo 2'; font-size:15pt; }
.cert .borda { position:absolute; inset:12mm; border:4px solid #8b46b0; border-radius:8mm; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:15mm; gap:5mm; }
.cert h1 { font-family:'Baloo 2'; font-size:36pt; margin:0; line-height:1.05; } .cert p { font-size:15pt; margin:0; color:#3a4354; line-height:1.4; } .faces2 { display:flex; gap:3mm; }
.linha-n { width:130mm; border-bottom:2px solid #1b2232; height:16mm; } .ass { display:flex; gap:20mm; margin-top:16mm; font-size:11pt; color:#6a7384; } .ass div { display:flex; flex-direction:column; gap:2mm; width:60mm; } .ass span { border-bottom:1.6px solid #1b2232; height:10mm; }
"""
open(sys.argv[1], 'w').write(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Emoções em Jogo</title>{FONTES}<style>{CSS}</style></head><body>' + '\n'.join(paginas) + '</body></html>')
print("páginas:", len(paginas))
