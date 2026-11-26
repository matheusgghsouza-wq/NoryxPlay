# Tipos de exercício. Cada função recebe um random.Random e devolve (largura, título, html, resposta).
import random, math
from desenhos import *
from util import *
CX = '<span class="cx"></span>'
CXP = '<span class="cx p"></span>'
LN = '<span class="ln"></span>'
OBJS = list(OBJ.keys())

def contar(r, maxn=9):
    tipos = r.sample(OBJS, 3); q = [r.randint(2, maxn) for _ in tipos]
    h = '<div class="lin3">' + ''.join(f'<div class="grp"><div class="objs">{"".join(obj(t, "7.5mm") for _ in range(n))}</div>{CX}</div>' for t, n in zip(tipos, q)) + '</div>'
    return 'f', 'Conte e escreva quantos tem:', h, ' · '.join(map(str, q))

def ant_suc(r, lo, hi, n=4):
    ns = r.sample(range(lo+1, hi), n)
    h = '<table class="tb"><tr><th>Antecessor</th><th>Número</th><th>Sucessor</th></tr>' + ''.join(f'<tr><td></td><td><b>{br(x)}</b></td><td></td></tr>' for x in ns) + '</table>'
    return 'h', 'Complete com o antecessor e o sucessor:', h, ' · '.join(f"{br(x-1)}, {br(x+1)}" for x in ns)

def comparar(r, lo, hi, n=4, dec_=False):
    pares = []
    for _ in range(n):
        a = r.randint(lo, hi); b = a if r.random() < .2 else r.randint(lo, hi); pares.append((a, b))
    f = (lambda x: dec(x/100)) if dec_ else br
    h = '<div class="lst">' + ''.join(f'<div class="cmp"><b>{f(a)}</b><span class="circ"></span><b>{f(b)}</b></div>' for a, b in pares) + '</div>'
    return 'h', 'Complete com &gt;, &lt; ou =:', h, ' · '.join('>' if a > b else '<' if a < b else '=' for a, b in pares)

def blocos_num(r, com_c=False):
    c = r.randint(1, 2) if com_c else 0; d = r.randint(1, 6 if com_c else 9); u = r.randint(0, 9)
    h = f'<div class="cen">{blocos(c, d, u, "24mm")}</div><div class="cen">Número: {CX}</div>'
    return 'h', 'Que número os blocos formam?', h, str(c*100+d*10+u)

def tabela_valor(r, ordens):
    cab = ['UM', 'C', 'D', 'U'][-ordens:] if ordens <= 4 else ['CM', 'DM', 'UM', 'C', 'D', 'U'][-ordens:]
    nomes = {'CM': 'Cent. milhar', 'DM': 'Dez. milhar', 'UM': 'Unid. milhar', 'C': 'Centenas', 'D': 'Dezenas', 'U': 'Unidades'}
    cores = {'CM': '#d9c6f2', 'DM': '#c6daf2', 'UM': '#c6f2d9', 'C': '#ffd1d9', 'D': '#fff0b3', 'U': '#c9f0c4'}
    ns = [r.randint(10**(ordens-1), 10**ordens - 1) for _ in range(2)]
    h = '<div class="duas">'
    for k, n in enumerate(ns):
        dig = str(n)
        h += '<div><table class="tb cdu"><tr>' + ''.join(f'<th style="background:{cores[c]}">{nomes[c] if ordens <= 3 else c}</th>' for c in cab) + '</tr><tr>' + \
             ''.join(f'<td>{d if k == 0 else ""}</td>' for d in dig) + f'</tr></table><div class="cen">{"Número: " + CX if k == 0 else "<b>" + br(n) + "</b>"}</div></div>'
    h += '</div>'
    return 'f', 'Complete o quadro de valor posicional:', h, f"{br(ns[0])} · quadro: {' | '.join(str(ns[1]))}"

def contas(r, op, lo, hi, n=4, armada=False, lo2=None, hi2=None):
    itens = []; resp = []
    for _ in range(n):
        a = r.randint(lo, hi); b = r.randint(lo2 or lo, hi2 or hi)
        if op == '-' and b > a: a, b = b, a
        if op == '÷':
            b = r.randint(lo2, hi2); q = r.randint(lo, hi); a = b*q
        res = {'+': a+b, '-': a-b, '×': a*b, '÷': a//b if op == '÷' else 0}[op]
        itens.append((a, b)); resp.append(br(res))
    if armada:
        h = '<div class="arm">' + ''.join(f'<div class="ca"><span>{br(a)}</span><span><i>{op}</i>{br(b)}</span><span class="tr"></span><span class="vz"></span></div>' for a, b in itens) + '</div>'
        return 'f', 'Arme e efetue:' if False else 'Resolva as contas:', h, ' · '.join(resp)
    h = '<div class="lst">' + ''.join(f'<div class="ch">{br(a)} {op} {br(b)} = {CX}</div>' for a, b in itens) + '</div>'
    return 'h', 'Resolva:', h, ' · '.join(resp)

def contas_dec(r, op, n=4):
    itens = []; resp = []
    for _ in range(n):
        a = r.randint(110, 999)/100; b = r.randint(110, 999)/100
        if op == '-' and b > a: a, b = b, a
        itens.append((a, b)); resp.append(dec(a+b if op == '+' else a-b))
    h = '<div class="arm">' + ''.join(f'<div class="ca"><span>{dec(a)}</span><span><i>{op}</i>{dec(b)}</span><span class="tr"></span><span class="vz"></span></div>' for a, b in itens) + '</div>'
    return 'f', 'Resolva (alinhe a vírgula):', h, ' · '.join(resp)

def sequencia(r, ini_lo, ini_hi, passos, desc=False, n=8):
    p = r.choice(passos); a = r.randint(ini_lo, ini_hi)
    if desc: a += p*n
    seq = [a - i*p if desc else a + i*p for i in range(n)]
    vazios = sorted(r.sample(range(1, n), 3))
    h = '<div class="seq">' + ''.join(f'<span class="sq{" v" if i in vazios else ""}">{"" if i in vazios else br(x)}</span>' for i, x in enumerate(seq)) + '</div>'
    h += f'<div class="cen pq">Regra: {"diminui" if desc else "aumenta"} de {CXP} em {CXP}</div>'
    return 'f', 'Complete a sequência:', h, ', '.join(br(seq[i]) for i in vazios) + f" (de {p} em {p})"

FIG = [('quadrado', '<rect x="15" y="15" width="70" height="70" fill="#ffd1d9" stroke="#1b2232" stroke-width="3"/>', 4),
       ('triângulo', '<polygon points="50,12 90,86 10,86" fill="#fff0b3" stroke="#1b2232" stroke-width="3" stroke-linejoin="round"/>', 3),
       ('círculo', '<circle cx="50" cy="50" r="38" fill="#c6daf2" stroke="#1b2232" stroke-width="3"/>', 0),
       ('retângulo', '<rect x="6" y="28" width="88" height="46" fill="#c9f0c4" stroke="#1b2232" stroke-width="3"/>', 4)]
def figuras(r):
    fs = FIG[:]; r.shuffle(fs)
    h = '<div class="lin4">' + ''.join(f'<div class="fg">{svg("0 0 100 100", s, "17mm", "17mm")}{LN}<small>lados: {CXP}</small></div>' for _, s, _ in fs) + '</div>'
    return 'f', 'Escreva o nome de cada figura e quantos lados ela tem:', h, ' · '.join(f"{n} ({l})" for n, _, l in fs)

def grupos(r, maxg=5, maxp=5):
    g = r.randint(2, maxg); p = r.randint(2, maxp); t = r.choice(OBJS)
    h = '<div class="gps">' + ''.join(f'<div class="gp">{"".join(obj(t, "5.5mm") for _ in range(p))}</div>' for _ in range(g)) + '</div>'
    h += f'<div class="cen">{CXP} grupos de {CXP} = {CXP} &nbsp; ou &nbsp; {CXP} × {CXP} = {CXP}</div>'
    return 'f', 'Observe os grupos e complete:', h, f"{g} grupos de {p} = {g*p}; {g} × {p} = {g*p}"

def dobro_metade(r, lo=2, hi=20):
    ns = r.sample([x for x in range(lo, hi+1) if x % 2 == 0], 4)
    h = '<table class="tb"><tr><th>Número</th><th>Dobro</th><th>Metade</th></tr>' + ''.join(f'<tr><td><b>{x}</b></td><td></td><td></td></tr>' for x in ns) + '</table>'
    return 'h', 'Complete com o dobro e a metade:', h, ' · '.join(f"{x}: {2*x}, {x//2}" for x in ns)

def hora_str(h, m): return f"{h}h" if m == 0 else f"{h}h{m:02d}"
def relogios(r, minutos=(0, 30)):
    hs = [(r.randint(1, 12), r.choice(minutos)) for _ in range(2)]
    h = '<div class="duas">' + ''.join(f'<div class="cen col">{relogio(a, b, "27mm")}{CX}</div>' for a, b in hs) + '</div>'
    return 'h', 'Que horas o relógio marca?', h, ' · '.join(hora_str(a, b) for a, b in hs)

def desenhe_ponteiros(r, minutos=(0, 15, 30, 45)):
    hs = [(r.randint(1, 12), r.choice(minutos)) for _ in range(2)]
    h = '<div class="duas">' + ''.join(f'<div class="cen col">{relogio(0, 0, "27mm", False)}<b class="hr">{hora_str(a, b)}</b></div>' for a, b in hs) + '</div>'
    return 'h', 'Desenhe os ponteiros:', h, 'ponteiro pequeno na hora, grande nos minutos'

def duracao(r):
    h1 = r.randint(7, 16); m1 = r.choice([0, 15, 30]); d = r.choice([30, 45, 60, 75, 90, 120])
    t2 = h1*60 + m1 + d
    ativ = r.choice(['O filme', 'A aula de natação', 'O passeio', 'A festa', 'O jogo'])
    h = f'<p class="pb">{ativ} começou às <b>{hora_str(h1, m1)}</b> e terminou às <b>{hora_str(t2//60, t2 % 60)}</b>. Quanto tempo durou?</p><div class="cen">{CX} minutos</div>'
    return 'h', 'Quanto tempo passou?', h, f"{d} minutos"

def dinheiro(r, notas=(2, 5, 10, 20), moedas=()):
    ns = sorted(r.choices(notas, k=r.randint(2, 3)), reverse=True); ms = sorted(r.choices(moedas, k=r.randint(1, 3)), reverse=True) if moedas else []
    itens = [cedula(v, "33mm") for v in ns] + [moeda(c, "14mm") for c in ms]
    tot = sum(ns) + sum(ms)/100
    h = '<div class="din">' + ' <b class="op">+</b> '.join(itens) + f' <b class="op">=</b> R$ {CX}</div>'
    return 'f', 'Calcule o valor total:', h, reais(tot)

def troco(r, maxp=50):
    pago = r.choice([v for v in (5, 10, 20, 50, 100) if v <= maxp*2 and v > 2])
    preco = r.randint(1, pago*100 - 50)/100 if maxp > 20 else r.randint(1, pago-1)
    item = r.choice(['um caderno', 'um lanche', 'um brinquedo', 'um livro', 'uma bola', 'um estojo'])
    h = f'<div class="din">{cedula(pago, "30mm")}</div><p class="pb">Paguei <b>{item}</b> que custa <b>{reais(preco)}</b> com esta nota. Quanto recebi de troco?</p><div class="cen">R$ {CX}</div>'
    return 'h', 'Calcule o troco:', h, reais(pago - preco)

def tabuada(r, t):
    ini = r.choice([1, 6]) if t > 1 else 1
    h = '<div class="tab">' + ''.join(f'<div>{t} × {i} = {CXP}</div>' for i in range(ini, ini+5)) + '</div>'
    return 'h', f'Resolva a tabuada do {t}:', h, ' · '.join(str(t*i) for i in range(ini, ini+5))

def divisao_resto(r, n=3, dmax=9):
    itens = []
    for _ in range(n):
        b = r.randint(2, dmax); q = r.randint(3, 15); rs = r.randint(0, b-1); itens.append((b*q+rs, b, q, rs))
    h = '<div class="lst">' + ''.join(f'<div class="ch">{a} ÷ {b} = {CXP} resto {CXP}</div>' for a, b, q, rs in itens) + '</div>'
    return 'h', 'Divida e diga o resto:', h, ' · '.join(f"{q} r{rs}" for a, b, q, rs in itens)

def partilha(r):
    p = r.randint(2, 4); q = r.randint(2, 5); t = r.choice(OBJS)
    h = f'<div class="objs">{"".join(obj(t, "6.5mm") for _ in range(p*q))}</div><p class="pb">Divida igualmente entre <b>{p} crianças</b>. Quantos cada uma recebe?</p><div class="cen">{p*q} ÷ {p} = {CX}</div>'
    return 'h', 'Divida em partes iguais:', h, str(q)

def fracao_desenho(r, dens=(2, 3, 4), n=2, tipo='pizza'):
    itens = []
    for _ in range(n):
        d = r.choice(dens); k = r.randint(1, d-1) if d > 1 else 1; itens.append((d, k))
    cor = r.choice(['#b48ee0', '#7fb8ff', '#7fd49b', '#ffb84d'])
    des = (lambda d, k: pizza(d, k, "27mm", cor)) if tipo == 'pizza' else (lambda d, k: barra(d, k, "40mm", cor))
    h = '<div class="duas">' + ''.join(f'<div class="cen col">{des(d, k)}<span class="fr"><span class="cx p"></span><i></i><span class="cx p"></span></span></div>' for d, k in itens) + '</div>'
    return 'h', 'Escreva a fração pintada:', h, ' · '.join(f"{k}/{d}" for d, k in itens)

def parte_de(r):
    pares = [('metade', 2), ('terça parte', 3), ('quarta parte', 4), ('quinta parte', 5), ('décima parte', 10)]
    sel = r.sample(pares[:3] if r.random() < .7 else pares, 3)
    itens = [(nm, d, d*r.randint(2, 9)) for nm, d in sel]
    h = '<div class="lst">' + ''.join(f'<div class="ch">A {nm} de {x} é {CX}</div>' for nm, d, x in itens) + '</div>'
    return 'h', 'Calcule:', h, ' · '.join(str(x//d) for nm, d, x in itens)

def equivalentes(r):
    base = r.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (2, 5)]); m = r.choice([2, 3])
    h = f'<div class="cen col">{barra(base[1], base[0], "60mm", "#7fb8ff")}{barra(base[1]*m, base[0]*m, "60mm", "#7fd49b")}</div>'
    h += f'<div class="cen ch">{base[0]}/{base[1]} = {CXP} / {base[1]*m}</div>'
    outra = r.choice([(1, 2, 4), (1, 3, 6), (2, 4, 8), (3, 5, 10), (1, 5, 10)])
    h += f'<div class="cen ch">{outra[0]}/{outra[1]} = {CXP} / {outra[2]}</div>'
    return 'h', 'Complete as frações equivalentes:', h, f"{base[0]*m} · {outra[0]*outra[2]//outra[1]}"

def comparar_frac(r):
    d = r.choice([4, 5, 6, 8]); a, b = r.sample(range(1, d), 2)
    h = f'<div class="cen col">{barra(d, a, "50mm", "#ffb84d")}<b>{a}/{d}</b>{barra(d, b, "50mm", "#b48ee0")}<b>{b}/{d}</b></div><div class="cen ch">{a}/{d} <span class="circ"></span> {b}/{d}</div>'
    return 'h', 'Qual fração é maior? Use &gt; ou &lt;:', h, '>' if a > b else '<'

def decimal_grade(r):
    k = r.randint(5, 95)
    h = f'<div class="cen col">{grade100(k, "36mm")}<span>Parte pintada: {CX} (decimal) ou {CXP}/100</span></div>'
    return 'h', 'Escreva a parte pintada:', h, f"{dec(k/100)} · {k}/100"

def decimal_escrita(r):
    itens = [(r.randint(0, 9), r.randint(1, 9), None) for _ in range(2)] + [(r.randint(0, 20), r.randint(1, 9), r.randint(1, 9))]
    def txt(i, d, c):
        s = f"{i} inteiro{'s' if i != 1 else ''} e {d} décimo{'s' if d > 1 else ''}"
        if c is not None: s = f"{i} inteiro{'s' if i != 1 else ''}, {d} décimo{'s' if d > 1 else ''} e {c} centésimo{'s' if c > 1 else ''}"
        return s
    h = '<div class="lst">' + ''.join(f'<div class="ch sm">{txt(*x)} = {CX}</div>' for x in itens) + '</div>'
    return 'h', 'Escreva o número decimal:', h, ' · '.join(f"{i},{d}" + (str(c) if c is not None else '') for i, d, c in itens)

def porcent_grade(r):
    k = r.choice(range(10, 95, 5))
    h = f'<div class="cen col">{grade100(k, "36mm", "#ffb84d")}<span>Pintado: {CX} %</span></div>'
    return 'h', 'Que porcentagem está pintada?', h, f"{k}%"

def porcent_de(r):
    itens = [(10, r.choice([50, 80, 120, 200, 300])), (50, r.choice([30, 60, 90, 140])), (25, r.choice([40, 80, 100, 200])), (r.choice([20, 30]), r.choice([50, 100, 200]))]
    r.shuffle(itens)
    h = '<div class="lst">' + ''.join(f'<div class="ch">{p}% de {v} = {CX}</div>' for p, v in itens) + '</div>'
    return 'h', 'Calcule:', h, ' · '.join(str(p*v//100) for p, v in itens)

def decompor(r, ordens):
    n = r.randint(10**(ordens-1), 10**ordens - 1)
    partes = [int(d) * 10**(len(str(n))-1-i) for i, d in enumerate(str(n))]
    h = f'<div class="ch">{br(n)} = ' + ' + '.join(CXP for _ in partes) + '</div>'
    m = r.randint(10**(ordens-1), 10**ordens - 1)
    p2 = [int(d) * 10**(len(str(m))-1-i) for i, d in enumerate(str(m))]
    h += f'<div class="ch">{" + ".join(br(p) for p in p2)} = {CX}</div>'
    return 'f', 'Decomponha e componha:', h, ' + '.join(br(p) for p in partes) + f" · {br(m)}"

def extenso_ex(r, lo, hi):
    a = r.randint(lo, hi); b = r.randint(lo, hi)
    h = f'<p class="pb">Escreva por extenso: <b>{br(a)}</b></p>{LN}{LN}<p class="pb">Escreva com algarismos: <b>{extenso(b)}</b></p><div class="cen">{CX}</div>'
    return 'h', 'Leia e escreva:', h, f"{extenso(a)} · {br(b)}"

def ordenar(r, lo, hi, n=5):
    ns = r.sample(range(lo, hi), n)
    h = '<div class="seq">' + ''.join(f'<span class="sq">{br(x)}</span>' for x in ns) + '</div><p class="pb">Do menor para o maior:</p><div class="seq">' + ''.join('<span class="sq v"></span>' for _ in ns) + '</div>'
    return 'f', 'Coloque em ordem crescente:', h, ', '.join(br(x) for x in sorted(ns))

def reta(r, passo, ini_max):
    a = r.randint(0, ini_max)//passo*passo; n = 9
    vals = [a + i*passo for i in range(n)]; vaz = sorted(r.sample(range(1, n-1), 4))
    s = '<line x1="4" y1="20" x2="196" y2="20" stroke="#1b2232" stroke-width="1.6"/><polygon points="196,16 200,20 196,24" fill="#1b2232"/>'
    for i, v in enumerate(vals):
        x = 10 + i*22.5
        s += f'<line x1="{x}" y1="15" x2="{x}" y2="25" stroke="#1b2232" stroke-width="1.6"/>'
        s += f'<rect x="{x-9}" y="29" width="18" height="10" rx="2" fill="#fff" stroke="#1b2232" stroke-width=".8" stroke-dasharray="1.6 1"/>' if i in vaz else f'<text x="{x}" y="35" text-anchor="middle" font-family="Nunito" font-weight="800" font-size="7" fill="#1b2232">{br(v)}</text>'
    return 'f', 'Complete a reta numérica:', svg("0 0 200 42", s, "100%"), ', '.join(br(vals[i]) for i in vaz)

PROB = {
 'soma': ["{nome} tinha {a} figurinhas e ganhou mais {b}. Com quantas ficou?", "Na turma há {a} meninos e {b} meninas. Quantas crianças há ao todo?", "Uma loja vendeu {a} bolas de manhã e {b} à tarde. Quantas vendeu no dia?"],
 'sub': ["{nome} tinha {a} balas e deu {b} para o irmão. Quantas sobraram?", "Um ônibus levava {a} pessoas e desceram {b}. Quantas ficaram?", "A escola tem {a} livros e {b} estão emprestados. Quantos estão na estante?"],
 'mult': ["Cada caixa tem {b} lápis. Quantos lápis há em {a} caixas?", "Uma sala tem {a} fileiras com {b} cadeiras cada. Quantas cadeiras há?", "{nome} lê {b} páginas por dia. Quantas páginas lê em {a} dias?"],
 'soma_g': ["Um estádio recebeu {a} pessoas no sábado e {b} no domingo. Quantas pessoas foram ao estádio?", "Uma fábrica produziu {a} garrafas em março e {b} em abril. Quantas garrafas produziu?", "Uma biblioteca tinha {a} livros e recebeu {b} de doação. Quantos livros tem agora?"],
 'sub_g': ["Uma cidade tinha {a} árvores e {b} foram cortadas. Quantas árvores restaram?", "Uma loja tinha {a} peças no estoque e vendeu {b}. Quantas peças sobraram?", "Faltavam {a} quilômetros para o fim da viagem. Já foram percorridos {b}. Quantos faltam agora?"],
 'div': ["{a} figurinhas foram divididas igualmente entre {b} amigos. Quantas cada um recebeu?", "A professora formou grupos de {b} alunos com {a} alunos. Quantos grupos formou?", "{a} ovos serão guardados em caixas de {b}. Quantas caixas serão usadas?"],
}
NOMES = ['Luíza', 'Pedro', 'Ana', 'Davi', 'Júlia', 'Miguel', 'Helena', 'Arthur', 'Alice', 'Gael', 'Laura', 'Théo']
def problemas(r, tipo, lo, hi, lo2=None, hi2=None):
    out = []; resp = []
    chave = tipo + '_g' if tipo in ('soma', 'sub') and hi > 100 else tipo
    for t in r.sample(PROB[chave], 2):
        a = r.randint(lo, hi); b = r.randint(lo2 or lo, hi2 or hi)
        if tipo == 'sub' and b >= a: a, b = b + 1, a
        if tipo == 'div': q = a; a = q*b
        res = {'soma': a+b, 'sub': a-b, 'mult': a*b, 'div': a//b}[tipo]
        out.append(t.format(nome=r.choice(NOMES), a=br(a), b=br(b))); resp.append(br(res))
    h = ''.join(f'<div class="pr"><p class="pb">{chr(97+i)}) {txt}</p><span class="cx g"></span></div>' for i, txt in enumerate(out))
    return 'f', 'Resolva os problemas:', h, ' · '.join(resp)

def mult_10(r):
    itens = [(r.randint(2, 99), r.choice([10, 100, 1000])) for _ in range(4)]
    h = '<div class="lst">' + ''.join(f'<div class="ch">{a} × {b} = {CX}</div>' for a, b in itens) + '</div>'
    return 'h', 'Multiplique por 10, 100 e 1.000:', h, ' · '.join(br(a*b) for a, b in itens)
