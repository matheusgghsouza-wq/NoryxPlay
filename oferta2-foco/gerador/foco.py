# Gera o HTML do produto "Foco sem Tela" (impresso em PDF pelo imprimir.js).
import random, math, sys
from comum import *

W, H = 182, 199  # área do quadro em mm
MARCA = "Foco sem Tela · 10 minutos por dia"
R = random.Random(2027)
CORES = {  # cor forte, cor da segunda onda, fundo claro
 'caca': ('#e4572e', '#f39a7d', '#fdeae3'), 'lab': ('#2b7fd6', '#86b8ec', '#e4effb'),
 'trilha': ('#25a065', '#82cfa6', '#e2f4ea'), 'copie': ('#8b46b0', '#c39ad8', '#f1e7f7'),
 'seq': ('#e0930c', '#f2c56d', '#fdf1d9'), 'igual': ('#d6457a', '#ec9dbb', '#fce6ee'),
 'dif': ('#14918f', '#7cc9c7', '#e0f3f2'), 'mem': ('#5a5fd1', '#a5a8ec', '#e9e9fb'),
 'conte': ('#c2410c', '#ea9a73', '#fbe8df'), 'setas': ('#3b8f2f', '#93c98a', '#e6f3e3'),
}
N1, N2 = "Nível 1 · 4 a 6 anos", "Nível 2 · 7 a 10 anos"
paginas, gabarito, mapa = [], [], []

def add(html_):
    paginas.append(html_)
    return len(paginas)

def svg(inner, vb=f"0 0 {W} {H}"):
    return f'<svg viewBox="{vb}" preserveAspectRatio="xMidYMid meet">{inner}</svg>'

def txt(x, y, t, tam=6, peso=800, cor=TINTA, anc="middle", fam="Nunito"):
    return f'<text x="{x:.2f}" y="{y:.2f}" font-family="{fam}" font-weight="{peso}" font-size="{tam}" fill="{cor}" text-anchor="{anc}" dominant-baseline="central">{esc(str(t))}</text>'

def ativ(chave, cat, titulo, nivel, minutos, instr, inner, resposta=None):
    c = CORES[chave]
    n = add(pagina_atividade(len(paginas)+1, MARCA, cat, titulo, nivel, minutos, instr, svg(inner), *c))
    if resposta is not None:
        gabarito.append((n, cat, resposta))
    return n

# ---------- 1. Caça-símbolos ----------
def caca(nivel, modo, alvo=None):
    if modo == 'icone':
        cols, rows = (7, 8) if nivel == 1 else (10, 12)
        pool = ['estrela','circulo','quadrado','triangulo','coracao','lua'] if nivel == 1 else ['estrela','flor','circulo','bola','quadrado','losango','gota','folha']
        alvo = alvo or R.choice(pool)
        cel = min(W/cols, (H-36)/rows)
        ox = (W - cel*cols)/2; oy = 22 + ((H-36) - cel*rows)/2
        itens = [alvo if R.random() < (0.22 if nivel == 1 else 0.14) else R.choice([p for p in pool if p != alvo]) for _ in range(cols*rows)]
        tot = itens.count(alvo)
        inner = icone(alvo, W/2 - 30, 3, 15) + txt(W/2 + 5, 10.5, "Ache este:", 6, anc="start") if False else ''
        inner += f'<rect x="{W/2-40}" y="3" width="80" height="16" rx="8" fill="#fdeae3"/>' + txt(W/2-14, 11, "Procure:", 6.2) + icone(alvo, W/2+4, 4.2, 13.5)
        for i, it in enumerate(itens):
            x = ox + (i % cols)*cel + cel*0.14; y = oy + (i//cols)*cel + cel*0.14
            inner += icone(it, x, y, cel*0.72)
        inner += txt(W-8, H-6, "Total: ____", 6.5, anc="end")
        return inner, f"{tot} × {NOMES[alvo]}", NOMES[alvo]
    if modo in ('letra', 'numero'):
        alvo, viz = ('b', 'dpqb') if modo == 'letra' else (alvo or '6', '6989' if (alvo or '6') == '6' else '9686')
        cols, rows = 12, 14
        cel = min(W/cols, (H-36)/rows)
        ox = (W - cel*cols)/2; oy = 22 + ((H-36) - cel*rows)/2
        itens = [alvo if R.random() < 0.18 else R.choice([v for v in viz if v != alvo]) for _ in range(cols*rows)]
        inner = f'<rect x="{W/2-40}" y="3" width="80" height="16" rx="8" fill="#fdeae3"/>' + txt(W/2-8, 11, "Procure a letra" if modo=='letra' else "Procure o número", 6) + txt(W/2+28, 11, alvo, 11, fam="Baloo 2")
        for i, it in enumerate(itens):
            inner += txt(ox + (i % cols)*cel + cel/2, oy + (i//cols)*cel + cel/2, it, cel*0.62, 700)
        inner += txt(W-8, H-6, "Total: ____", 6.5, anc="end")
        return inner, f"{itens.count(alvo)} × “{alvo}”", alvo

def gerar_caca():
    ini = len(paginas)+1
    for k in range(6):
        inner, resp, a = caca(1, 'icone')
        ativ('caca', 'Caça-símbolos', 'Ache todos iguais', N1, 5, f'Circule <b>todos</b> os desenhos iguais ao modelo. Vá linha por linha, da esquerda para a direita. Depois conte quantos achou.', inner, resp)
    for modo in ['icone', 'icone', 'letra', 'letra', 'numero', 'numero']:
        inner, resp, a = caca(2, modo, '9' if (modo == 'numero' and R.random() < .5) else None)
        ativ('caca', 'Caça-símbolos', 'Olho de águia', N2, 8, 'Circule <b>só</b> o modelo pedido. Cuidado: tem desenhos parecidos! Vá linha por linha, sem pular, e conte no final.', inner, resp)
    mapa.append(('Caça-símbolos', ini, len(paginas), 12))

# ---------- 2. Labirintos ----------
def labirinto(c, l):
    vis = [[False]*c for _ in range(l)]
    paredes_v = [[True]*(c+1) for _ in range(l)]   # parede à esquerda da célula (x)
    paredes_h = [[True]*c for _ in range(l+1)]     # parede acima da célula (y)
    pilha = [(0, 0)]; vis[0][0] = True
    while pilha:
        x, y = pilha[-1]
        viz = [(x+dx, y+dy, dx, dy) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)) if 0 <= x+dx < c and 0 <= y+dy < l and not vis[y+dy][x+dx]]
        if not viz: pilha.pop(); continue
        nx, ny, dx, dy = R.choice(viz)
        if dx == 1: paredes_v[y][x+1] = False
        if dx == -1: paredes_v[y][x] = False
        if dy == 1: paredes_h[y+1][x] = False
        if dy == -1: paredes_h[y][x] = False
        vis[ny][nx] = True; pilha.append((nx, ny))
    paredes_v[0][0] = False; paredes_v[l-1][c] = False
    return paredes_v, paredes_h

def gerar_lab():
    ini = len(paginas)+1
    pares = [('gato','peixe'),('carro','casa'),('gota','flor'),('bola','casa'),('peixe','estrela'),('gato','bola')]
    for k in range(12):
        nv = 1 if k < 6 else 2
        c, l = ((7, 8), (8, 9), (8, 9), (9, 10), (9, 10), (10, 11))[k] if nv == 1 else ((12, 13), (13, 14), (14, 15), (15, 17), (16, 18), (17, 19))[k-6]
        pv, ph = labirinto(c, l)
        cel = min((W-40)/c, (H-14)/l); ox = (W - cel*c)/2; oy = (H - cel*l)/2
        sw = 1.6 if nv == 1 else 1.2
        d = ''
        for y in range(l):
            for x in range(c+1):
                if pv[y][x]: d += f'M{ox+x*cel:.2f} {oy+y*cel:.2f}v{cel:.2f}'
        for y in range(l+1):
            for x in range(c):
                if ph[y][x]: d += f'M{ox+x*cel:.2f} {oy+y*cel:.2f}h{cel:.2f}'
        a, b = pares[k % 6]
        inner = f'<path d="{d}" stroke="{TINTA}" stroke-width="{sw}" stroke-linecap="round" fill="none"/>'
        inner += icone(a, ox-19, oy+cel/2-8, 16) + icone(b, ox+c*cel+3, oy+(l-0.5)*cel-8, 16)
        ativ('lab', 'Labirinto', 'Caminho certo' if nv == 1 else 'Labirinto desafio', N1 if nv == 1 else N2, 5 if nv == 1 else 8,
             f'Leve o(a) <b>{NOMES[a]}</b> até o(a) <b>{NOMES[b]}</b>. Use o dedo primeiro e depois o lápis. Tente não encostar nas paredes.', inner)
    mapa.append(('Labirintos', ini, len(paginas), 12))

# ---------- 3. Trilha dos números ----------
def pontos(n, raio, mx=12, my=12):
    pts = []
    while len(pts) < n:
        tent = 0
        while True:
            tent += 1
            p = (R.uniform(mx, W-mx), R.uniform(my, H-my))
            if all(math.dist(p, q) > raio*2.6 for q in pts): break
            if tent > 4000: return pontos(n, raio*0.95, mx, my)
        pts.append(p)
    return pts

def gerar_trilha():
    ini = len(paginas)+1
    letras = "ABCDEFGHIJKL"
    for k in range(10):
        if k < 4:
            n = 10 + k*2; rot = [str(i+1) for i in range(n)]; nv = 1
            ins = f'Ligue os números em ordem, do <b>1</b> até o <b>{n}</b>, sem tirar o lápis do papel.'
        elif k < 7:
            n = 20 + (k-4)*3; rot = [str(i+1) for i in range(n)]; nv = 2
            ins = f'Ligue do <b>1</b> até o <b>{n}</b> o mais rápido que conseguir, sem errar a ordem. Marque o tempo, se quiser.'
        else:
            m = 8 + (k-7)*2; rot = []
            for i in range(m): rot += [str(i+1), letras[i]]
            n = len(rot); nv = 2
            ins = 'Alterne número e letra: <b>1 → A → 2 → B → 3 → C</b>… até o fim. Concentre-se para não pular nenhum.'
        raio = 6.2 if n <= 16 else 5.4
        pts = pontos(n, raio)
        inner = ''
        for i, (p, r_) in enumerate(zip(pts, rot)):
            fill = '#e2f4ea' if i == 0 else '#fff'
            inner += f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{raio}" fill="{fill}" stroke="{TINTA}" stroke-width="1"/>' + txt(p[0], p[1]+.3, r_, raio*1.05)
        inner += txt(pts[0][0], pts[0][1]-raio-3.2, "início", 4.2, 700, '#25a065')
        ativ('trilha', 'Trilha dos números', 'Ligue em ordem' if nv == 1 else ('Trilha rápida' if k < 7 else 'Número e letra'), N1 if nv == 1 else N2, 5 if nv == 1 else 7, ins, inner)
    mapa.append(('Trilha dos números', ini, len(paginas), 10))

# ---------- 4. Copie o desenho ----------
def caminho(nn, passos):
    while True:
        x, y = R.randrange(nn), R.randrange(nn); usados = {(x, y)}; seq = [(x, y)]
        for _ in range(passos*3):
            op = [(x+dx, y+dy) for dx in (-1,0,1) for dy in (-1,0,1) if (dx or dy) and 0 <= x+dx < nn and 0 <= y+dy < nn and (x+dx, y+dy) not in usados]
            if not op: break
            x, y = R.choice(op); usados.add((x, y)); seq.append((x, y))
            if len(seq) > passos: break
        if len(seq) > passos: return seq

def grade_pontos(ox, oy, nn, passo):
    return ''.join(f'<circle cx="{ox+i*passo:.2f}" cy="{oy+j*passo:.2f}" r="1.05" fill="{TINTA}"/>' for i in range(nn) for j in range(nn))

def gerar_copie():
    ini = len(paginas)+1
    for k in range(12):
        nv = 1 if k < 6 else 2
        nn = 5 if nv == 1 else 7
        passos = (5 + k) if nv == 1 else (11 + (k-6)*2)
        cor = CORES['copie'][0]
        inner = ''
        # modelo em cima, espaço para copiar embaixo
        lado = 70 if nv == 1 else 72
        passo = lado/(nn-1)
        for bloco, oy, rot in ((0, 11, "Modelo"), (1, 108, "Sua cópia")):
            ox = (W - lado)/2
            inner += txt(W/2, oy-4.5, rot, 5.6, 800, cor)
            inner += f'<rect x="{ox-6}" y="{oy}" width="{lado+12}" height="{lado+12}" rx="4" fill="{"#f1e7f7" if bloco==0 else "#fff"}" stroke="{cor}" stroke-width=".8" stroke-dasharray="{"0" if bloco==0 else "2 1.6"}"/>'
            inner += grade_pontos(ox, oy+6, nn, passo)
            if bloco == 0:
                seq = caminho(nn, passos)
                pts = ' '.join(f'{ox+x*passo:.2f},{oy+6+y*passo:.2f}' for x, y in seq)
                inner += f'<polyline points="{pts}" fill="none" stroke="{cor}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>'
                inner += f'<circle cx="{ox+seq[0][0]*passo:.2f}" cy="{oy+6+seq[0][1]*passo:.2f}" r="2.4" fill="{cor}"/>'
        ativ('copie', 'Copie o desenho', 'Olhe e copie' if nv == 1 else 'Cópia de detetive', N1 if nv == 1 else N2, 6 if nv == 1 else 9,
             'Olhe o modelo com calma e faça <b>o mesmo desenho</b> na grade de baixo. Comece pela bolinha cheia e conte os pontinhos.', inner)
    mapa.append(('Copie o desenho', ini, len(paginas), 12))

# ---------- 5. Sequências ----------
PADROES = ['AB', 'ABC', 'AAB', 'ABB', 'AABB', 'ABCD', 'ABAC', 'ABBC']
def gerar_seq():
    ini = len(paginas)+1
    pool = ['estrela','coracao','circulo','quadrado','triangulo','lua','sol','flor','peixe','maca','gota','folha']
    for k in range(10):
        nv = 1 if k < 5 else 2
        linhas = 5
        inner = ''; resp = []
        alt = (H - 6) / linhas
        for li in range(linhas):
            pad = R.choice(PADROES[:4] if nv == 1 else PADROES[2:])
            esc_ = R.sample(pool, len(set(pad)))
            mp = dict(zip(sorted(set(pad)), esc_))
            tam = 6 if nv == 1 else 8
            seqv = [mp[pad[i % len(pad)]] for i in range(tam)]
            certo = mp[pad[tam % len(pad)]]
            y0 = 3 + li*alt
            inner += f'<rect x="4" y="{y0}" width="{W-8}" height="{alt-4}" rx="4" fill="{"#fdf1d9" if li % 2 == 0 else "#fff"}" stroke="#f2c56d" stroke-width=".7"/>'
            inner += txt(10, y0+(alt-4)/2, li+1, 7, fam="Baloo 2", cor=CORES['seq'][0])
            area = W - 70; s = min(area/(tam+1), alt-14)
            for i, it in enumerate(seqv):
                inner += icone(it, 18 + i*(area/(tam+1)), y0+(alt-4)/2 - s*0.42, s*0.84)
            qx = 18 + tam*(area/(tam+1))
            inner += f'<rect x="{qx:.2f}" y="{y0+(alt-4)/2 - s*0.48:.2f}" width="{s*0.96:.2f}" height="{s*0.96:.2f}" rx="2.5" fill="#fff" stroke="{TINTA}" stroke-width=".9" stroke-dasharray="2 1.4"/>' + txt(qx+s*0.48, y0+(alt-4)/2, "?", s*0.5, fam="Baloo 2", cor="#c9b48a")
            opcoes = R.sample([certo] + R.sample([p for p in esc_ if p != certo] + R.sample([p for p in pool if p not in esc_], 2), 2), 3)
            for j, op in enumerate(opcoes):
                bx = W - 50 + j*15.5
                inner += f'<circle cx="{bx+6.5:.2f}" cy="{y0+(alt-4)/2:.2f}" r="7.2" fill="#fff" stroke="#d8c8a0" stroke-width=".6"/>' + icone(op, bx+1.5, y0+(alt-4)/2-5, 10)
            resp.append(f"{li+1}) {NOMES[certo]}")
        ativ('seq', 'Sequências', 'O que vem depois?' if nv == 1 else 'Descubra a regra', N1 if nv == 1 else N2, 6 if nv == 1 else 8,
             'Descubra a regra de cada fileira. Circule à direita o desenho que <b>vem depois</b> e desenhe ele no quadradinho.', inner, '; '.join(resp))
    mapa.append(('Sequências', ini, len(paginas), 10))

# ---------- 6. Encontre o igual ----------
def gerar_igual():
    ini = len(paginas)+1
    pool = ['estrela','coracao','circulo','quadrado','triangulo','lua','sol','flor','peixe','maca','gota','folha','casa','arvore']
    for k in range(10):
        nv = 1 if k < 5 else 2
        tam = 3 if nv == 1 else 5
        nop = 4 if nv == 1 else 6
        modelo = R.sample(pool, tam)
        ops = set(); lista = []
        while len(lista) < nop-1:
            v = modelo[:]
            if R.random() < .5:
                i, j = R.sample(range(tam), 2); v[i], v[j] = v[j], v[i]
            else:
                v[R.randrange(tam)] = R.choice([p for p in pool if p not in modelo])
            if tuple(v) not in ops and v != modelo: ops.add(tuple(v)); lista.append(v)
        pos = R.randrange(nop); lista.insert(pos, modelo)
        cor = CORES['igual'][0]
        larg = tam*16 + 10
        inner = txt(W/2, 8, "Modelo", 5.6, 800, cor)
        inner += f'<rect x="{(W-larg)/2:.2f}" y="13" width="{larg}" height="24" rx="5" fill="#fce6ee" stroke="{cor}" stroke-width="1.2"/>'
        for i, it in enumerate(modelo): inner += icone(it, (W-larg)/2 + 5 + i*16 + 1, 17, 15)
        topo = 46; alt = (H - topo - 4) / ((nop+1)//2 if nv == 2 else nop) if nv == 2 else (H - topo - 4)/nop
        for j, v in enumerate(lista):
            if nv == 2:
                cx = 4 + (j % 2)*(W/2); cy = topo + (j//2)*alt; cw = W/2 - 8
            else:
                cx = (W - 120)/2; cy = topo + j*alt; cw = 120
            inner += f'<rect x="{cx:.2f}" y="{cy:.2f}" width="{cw:.2f}" height="{alt-5:.2f}" rx="4" fill="#fff" stroke="#ec9dbb" stroke-width=".8"/>'
            inner += txt(cx+7, cy+(alt-5)/2, "ABCDEF"[j], 7, fam="Baloo 2", cor=cor)
            s = min(13, (cw-20)/tam)
            for i, it in enumerate(v): inner += icone(it, cx+15 + i*s*1.05, cy+(alt-5)/2 - s/2, s*0.95)
        ativ('igual', 'Encontre o igual', 'Qual é igual?' if nv == 1 else 'Gêmeos perfeitos', N1 if nv == 1 else N2, 5 if nv == 1 else 7,
             'Só <b>uma</b> fileira é igualzinha ao modelo, na mesma ordem. Compare desenho por desenho e circule a letra certa.', inner, f"letra {'ABCDEF'[pos]}")
    mapa.append(('Encontre o igual', ini, len(paginas), 10))

# ---------- 7. Diferenças ----------
def gerar_dif():
    ini = len(paginas)+1
    pool = ['estrela','coracao','circulo','quadrado','triangulo','lua','sol','flor','peixe','maca','gota','folha','casa','arvore','nuvem','bola','gato','carro']
    for k in range(10):
        nv = 1 if k < 5 else 2
        nn = 4 if nv == 1 else 5; ndif = 3 if nv == 1 else 5
        base = [R.choice(pool) for _ in range(nn*nn)]
        mud = R.sample(range(nn*nn), ndif); nova = base[:]
        for m in mud: nova[m] = R.choice([p for p in pool if p != base[m]])
        lado = 82; cel = lado/nn; cor = CORES['dif'][0]
        inner = ''
        for g, (ox, lst, rot) in enumerate(((4, base, "Desenho A"), (W/2+5, nova, "Desenho B"))):
            oy = 22
            inner += txt(ox+lado/2+1.5, 13, rot, 6, 800, cor)
            inner += f'<rect x="{ox}" y="{oy}" width="{lado+3}" height="{lado+3}" rx="4" fill="#e0f3f2" stroke="{cor}" stroke-width="1"/>'
            for i, it in enumerate(lst):
                inner += icone(it, ox+1.5 + (i % nn)*cel + cel*.14, oy+1.5 + (i//nn)*cel + cel*.14, cel*.72)
        inner += f'<rect x="20" y="126" width="{W-40}" height="60" rx="5" fill="#fff" stroke="#7cc9c7" stroke-width=".8" stroke-dasharray="2 1.5"/>'
        inner += txt(W/2, 138, f"Achei {ndif} diferenças? Pinte uma estrela para cada uma:", 5.6, 700)
        for i in range(ndif): inner += icone('estrela', W/2 - ndif*10 + i*20 + 1, 148, 18)
        pos = '; '.join(f"linha {m//nn+1}, coluna {m % nn+1}" for m in sorted(mud))
        ativ('dif', 'Jogo das diferenças', f'Ache {ndif} diferenças', N1 if nv == 1 else N2, 6 if nv == 1 else 8,
             f'Os dois desenhos parecem iguais, mas têm <b>{ndif} diferenças</b>. Compare quadradinho por quadradinho e circule as diferenças no desenho B.', inner, pos)
    mapa.append(('Jogo das diferenças', ini, len(paginas), 10))

# ---------- 8. Observe e lembre ----------
def gerar_mem():
    ini = len(paginas)+1
    pool = list(ICONES.keys())
    for k in range(8):
        nv = 1 if k < 4 else 2
        nver = 5 if nv == 1 else 8; ntot = 10 if nv == 1 else 16
        vistos = R.sample(pool, nver)
        cor = CORES['mem'][0]
        cols = 3 if nv == 1 else 4
        cel = 46 if nv == 1 else 40
        rows = math.ceil(nver/cols)
        ox = (W - cols*cel)/2; oy = (H - rows*cel)/2 - 8
        inner = f'<rect x="{ox-6}" y="{oy-6}" width="{cols*cel+12}" height="{rows*cel+12}" rx="6" fill="#e9e9fb"/>'
        for i, it in enumerate(vistos):
            inner += icone(it, ox + (i % cols)*cel + cel*.15, oy + (i//cols)*cel + cel*.15, cel*.7)
        inner += txt(W/2, H-14, "Terminou de olhar? Vire a folha (ou peça para um adulto cobrir).", 5.6, 700, cor)
        ativ('mem', 'Observe e lembre', 'Foto na memória' if nv == 1 else 'Memória de elefante', N1 if nv == 1 else N2, 3,
             f'<b>Parte 1.</b> Olhe os {nver} desenhos por <b>30 segundos</b>. Tente guardar todos na cabeça, como uma foto.', inner)
        outros = R.sample([p for p in pool if p not in vistos], ntot - nver)
        todos = vistos + outros; R.shuffle(todos)
        cols2 = 4 if nv == 1 else 4; rows2 = math.ceil(ntot/cols2); cel2 = min(40, (H-20)/rows2)
        ox2 = (W - cols2*cel2)/2; oy2 = (H - rows2*cel2)/2
        inner2 = ''
        for i, it in enumerate(todos):
            x = ox2 + (i % cols2)*cel2; y = oy2 + (i//cols2)*cel2
            inner2 += f'<rect x="{x+1.5:.2f}" y="{y+1.5:.2f}" width="{cel2-3:.2f}" height="{cel2-3:.2f}" rx="4" fill="#fff" stroke="#a5a8ec" stroke-width=".7"/>' + icone(it, x + cel2*.2, y + cel2*.2, cel2*.6)
        n2 = ativ('mem', 'Observe e lembre', 'O que você viu?', N1 if nv == 1 else N2, 4,
             f'<b>Parte 2.</b> Sem espiar a folha anterior, circule os <b>{nver} desenhos</b> que você viu. Depois confira!', inner2,
             ', '.join(NOMES[v] for v in vistos))
    mapa.append(('Observe e lembre', ini, len(paginas), 8))

# ---------- 9. Conte e registre ----------
def gerar_conte():
    ini = len(paginas)+1
    pool = ['estrela','coracao','lua','sol','flor','peixe','maca','nuvem','gota','folha','bola','guarda']
    for k in range(10):
        nv = 1 if k < 5 else 2
        tipos = R.sample(pool, 3 if nv == 1 else 5)
        qtd = {t: R.randint(3, 7) if nv == 1 else R.randint(5, 12) for t in tipos}
        itens = [t for t in tipos for _ in range(qtd[t])]; R.shuffle(itens)
        area_h = 128
        tam = 15 if nv == 1 else 12
        pts = []
        for it in itens:
            for _ in range(5000):
                p = (R.uniform(6, W-6-tam), R.uniform(6, area_h-tam))
                if all(math.dist(p, q) > tam*1.08 for q in pts): break
            pts.append(p)
        inner = f'<rect x="3" y="3" width="{W-6}" height="{area_h}" rx="5" fill="#fbe8df"/>'
        for it, p in zip(itens, pts): inner += icone(it, p[0], p[1], tam, R.choice([0, 0, -12, 12]))
        ty = area_h + 10; cw = (W - 8)/len(tipos)
        for i, t in enumerate(tipos):
            x = 4 + i*cw
            inner += f'<rect x="{x+1:.2f}" y="{ty}" width="{cw-2:.2f}" height="50" rx="4" fill="#fff" stroke="{CORES["conte"][0]}" stroke-width=".9"/>'
            inner += icone(t, x + cw/2 - 8, ty+4, 16) + f'<rect x="{x + cw/2 - 11:.2f}" y="{ty+25}" width="22" height="18" rx="3" fill="#fff" stroke="{TINTA}" stroke-width=".9"/>'
        ativ('conte', 'Conte e registre', 'Quantos tem?' if nv == 1 else 'Contador atento', N1 if nv == 1 else N2, 6 if nv == 1 else 9,
             'Conte cada tipo de desenho. Dica: risque cada um que já contou para não contar duas vezes. Escreva o total no quadrinho.', inner,
             ', '.join(f"{NOMES[t]} {qtd[t]}" for t in tipos))
    mapa.append(('Conte e registre', ini, len(paginas), 10))

# ---------- 10. Siga as setas ----------
def gerar_setas():
    ini = len(paginas)+1
    pool = [p for p in ICONES if p not in ('sol',)]
    SETA = {(1,0): '→', (-1,0): '←', (0,1): '↓', (0,-1): '↑'}
    for k in range(8):
        nv = 1 if k < 4 else 2
        nn = 5 if nv == 1 else 6; npas = 5 if nv == 1 else 10
        grade = [R.choice(pool) for _ in range(nn*nn)]
        while True:
            x, y = R.randrange(nn), R.randrange(nn); sx, sy = x, y; mv = []
            for _ in range(npas):
                op = [(dx, dy) for (dx, dy) in SETA if 0 <= x+dx < nn and 0 <= y+dy < nn and not (mv and (dx, dy) == (-mv[-1][0], -mv[-1][1]))]
                dx, dy = R.choice(op); x += dx; y += dy; mv.append((dx, dy))
            if (x, y) != (sx, sy): break
        grade[sy*nn+sx] = 'estrela'
        lado = 118 if nv == 1 else 122; cel = lado/nn; ox = (W - lado)/2; oy = 5
        cor = CORES['setas'][0]
        inner = ''
        for i, it in enumerate(grade):
            cx, cy = ox + (i % nn)*cel, oy + (i//nn)*cel
            ini_ = i == sy*nn+sx
            inner += f'<rect x="{cx:.2f}" y="{cy:.2f}" width="{cel:.2f}" height="{cel:.2f}" fill="{"#e6f3e3" if ini_ else "#fff"}" stroke="{TINTA}" stroke-width=".8"/>' + icone(it, cx+cel*.17, cy+cel*.17, cel*.66)
        inner += txt(ox + sx*cel + cel/2, oy + sy*cel + 3.2, "COMECE", 3.4, 800, cor)
        sy0 = oy + lado + 10
        inner += f'<rect x="8" y="{sy0}" width="{W-16}" height="{H-sy0-30}" rx="5" fill="#e6f3e3"/>'
        lar = (W-28)/npas
        for i, m in enumerate(mv):
            inner += txt(14 + lar*i + lar/2, sy0 + (H-sy0-30)/2, SETA[m], 12 if nv == 1 else 10, 800, cor)
        inner += txt(W/2 - 20, H-12, "Onde você parou? Desenhe aqui →", 5.6, 700) + f'<rect x="{W/2+22}" y="{H-22}" width="20" height="20" rx="3" fill="#fff" stroke="{TINTA}" stroke-width=".9" stroke-dasharray="2 1.4"/>'
        ativ('setas', 'Siga as setas', 'Caminho das setas' if nv == 1 else 'Missão secreta', N1 if nv == 1 else N2, 5 if nv == 1 else 8,
             f'Comece na <b>estrela verde</b>. Ande uma casinha para cada seta, na ordem, com o dedo. Em que desenho você parou?', inner, NOMES[grade[y*nn+x]])
    mapa.append(('Siga as setas', ini, len(paginas), 8))

# ---------- Páginas especiais ----------
def capa():
    icones = ['estrela','coracao','sol','flor','peixe','maca','lua','gota','folha','gato','bola','nuvem','casa','carro']
    deco = ''
    for i in range(26):
        a = i/26*2*math.pi
        x = 105 + math.cos(a)*(88 + (i % 3)*6) - 9; y = 150 + math.sin(a)*(124 + (i % 2)*8) - 9
        deco += icone(icones[i % len(icones)], x, y, 18 - (i % 3)*3, (i*23) % 50 - 25)
    return f'''<section class="page capa"><svg class="fundo" viewBox="0 0 210 297">{deco}</svg>
<div class="capa-box"><div class="selo">Kit para imprimir</div>
<h1>Foco<br>sem Tela</h1><p class="sub">10 minutos por dia de atividades de atenção para crianças de 4 a 10 anos</p>
<div class="nums"><span><b>102</b>atividades</span><span><b>24</b>cartões de movimento</span><span><b>2</b>níveis</span></div>
<p class="extra">+ Plano de 4 semanas · Quadro de conquistas · Certificado · Gabarito</p></div></section>'''

def pag_texto(titulo, cor, corpo):
    return f'''<section class="page">{onda(cor, cor + "99")}
<div class="cab"><div><div class="cat">Foco sem Tela</div><h1>{esc(titulo)}</h1></div></div>
<div class="corpo">{corpo}</div><div class="rod"><span>{esc(MARCA)}</span><span class="pg">{len(paginas)+1}</span></div></section>'''

def como_usar():
    passos = [
      ("Escolha um horário fixo", "Depois do lanche, antes do banho ou antes de dormir. A rotina ajuda mais do que a duração."),
      ("Marque 10 minutos", "Use um relógio de cozinha ou ampulheta. Quando o tempo acabar, pare, mesmo que falte terminar."),
      ("Comece pelo nível certo", "Nível 1 para 4 a 6 anos, Nível 2 para 7 a 10 anos. Se ficar fácil demais, suba. Se frustrar, desça."),
      ("Uma folha + um cartão", "Faça uma atividade de papel e um cartão de movimento. O corpo também precisa participar."),
      ("Elogie o esforço", "Diga “você ficou bem concentrado” em vez de “você é inteligente”. Pinte uma estrela no quadro de conquistas."),
      ("Imprima de novo", "Quer repetir? Imprima outra vez ou coloque a folha num saquinho plástico e use canetinha de quadro branco."),
    ]
    corpo = '<div class="passos">' + ''.join(f'<div class="p"><b>{i+1}</b><div><h3>{esc(t)}</h3><p>{esc(d)}</p></div></div>' for i, (t, d) in enumerate(passos)) + '</div>'
    corpo += '<div class="aviso"><b>Importante:</b> este é um material de atividades lúdicas para treinar atenção em casa ou na escola. Ele não é tratamento e não substitui a avaliação de pediatra, psicólogo ou outro profissional de saúde. Cada criança tem seu ritmo.</div>'
    return pag_texto("Como usar este kit", "#2b7fd6", corpo)

def indice():
    cats = {'Caça-símbolos':'caca','Labirintos':'lab','Trilha dos números':'trilha','Copie o desenho':'copie','Sequências':'seq','Encontre o igual':'igual','Jogo das diferenças':'dif','Observe e lembre':'mem','Conte e registre':'conte','Siga as setas':'setas'}
    desc = {'Caça-símbolos':'atenção seletiva: achar o alvo no meio de muitos','Labirintos':'planejar o caminho antes de agir','Trilha dos números':'seguir uma ordem sem se perder','Copie o desenho':'observar detalhes e reproduzir','Sequências':'descobrir a regra e prever','Encontre o igual':'comparar com cuidado','Jogo das diferenças':'olhar atento, parte por parte','Observe e lembre':'memória visual de curto prazo','Conte e registre':'contar sem pular nem repetir','Siga as setas':'seguir instruções passo a passo'}
    linhas = ''
    for nome, a, b, q in mapa:
        c = CORES[cats[nome]][0]
        linhas += f'<div class="ix"><span class="b" style="background:{c}"></span><div><h3>{esc(nome)}</h3><p>{esc(desc[nome])} · {q} atividades</p></div><span class="pp">p. {a}–{b}</span></div>'
    linhas += f'<div class="ix"><span class="b" style="background:#1b2232"></span><div><h3>Cartões de foco em movimento</h3><p>24 desafios para o corpo, para recortar</p></div><span class="pp">p. {cartoes_pg[0]}–{cartoes_pg[1]}</span></div>'
    return linhas

def plano():
    cats_ordem = mapa
    corpo = '<p class="intro">Uma sugestão para as 4 primeiras semanas, 5 dias por semana. Cada dia: uma folha + um cartão de movimento. Use o Nível 1 ou o Nível 2, conforme a idade.</p><table class="plano"><tr><th></th><th>Seg</th><th>Ter</th><th>Qua</th><th>Qui</th><th>Sex</th></tr>'
    nomes_curto = ['Caça-símbolos','Labirinto','Trilha','Copie','Sequência','Igual','Diferenças','Memória','Conte','Setas']
    d = 0
    for s in range(4):
        corpo += f'<tr><th>Semana {s+1}</th>'
        for dia in range(5):
            i = (s*5 + dia) % 10
            nome, a, b, q = mapa[i]
            corpo += f'<td><b>{nomes_curto[i]}</b><span>p. {a}–{b}</span><i>+ cartão {s*5+dia+1}</i><em>☐</em></td>'
        corpo += '</tr>'
    corpo += '</table><p class="intro" style="margin-top:6mm">Depois da semana 4, repita a ordem com folhas que ainda não foram feitas ou suba de nível.</p>'
    return pag_texto("Plano de 4 semanas", "#25a065", corpo)

def quadro():
    ic = ['estrela','coracao','sol','flor','lua','peixe','maca','folha','gota','bola']
    cel = ''
    for i in range(30):
        cel += f'<div class="dia"><span>Dia {i+1}</span>{icone_svg(ic[i % len(ic)], "15mm")}</div>'
    return pag_texto("Meu quadro de foco", "#e0930c", f'<p class="intro">A cada dia de foco, pinte o desenho. Quando completar uma fileira, comemore!</p><div class="quadro-c">{cel}</div>')

CARTOES = [
 ("Estátua", "Fique parado como estátua por 20 segundos. Nem um dedinho mexe!"),
 ("Flamingo", "Fique em um pé só e conte até 10. Agora troque de pé."),
 ("Palma secreta", "Um adulto fala várias palavras. Bata palma só quando ouvir “bola”."),
 ("Respiração da flor", "Cheire uma flor imaginária (puxe o ar) e sopre uma vela (solte o ar). 5 vezes."),
 ("Espelho", "Copie os movimentos de um adulto, como se fosse o espelho dele."),
 ("Seu mestre mandou", "Faça só o que vier depois de “seu mestre mandou”. Atenção!"),
 ("Contagem do sapo", "Pule como sapo contando de 1 a 10. Agora de 10 até 1."),
 ("Ouvido de coruja", "Feche os olhos por 30 segundos. Quantos sons diferentes você ouviu?"),
 ("Ao contrário", "Quando o adulto disser “alto”, abaixe. Quando disser “baixo”, fique na ponta dos pés."),
 ("Caminho do equilibrista", "Ande em linha reta, um pé na frente do outro, até a porta."),
 ("Cores da casa", "Encontre 5 coisas azuis dentro de casa em 1 minuto."),
 ("Balão na barriga", "Deite, coloque a mão na barriga e respire devagar, enchendo como um balão. 6 vezes."),
 ("Bate e conta", "Bata palmas 3 vezes, pise 2 vezes, repita. Agora o adulto inventa outro ritmo."),
 ("Pedra, papel e foco", "Jogue 5 rodadas e diga quem ganhou antes de mostrar a mão de novo."),
 ("Robô obediente", "O adulto dá 3 ordens seguidas, ex.: pule, gire, sente. Faça na ordem certa."),
 ("Olhos de lince", "Olhe a sala por 20 segundos. Feche os olhos e diga 5 coisas que viu."),
 ("Câmera lenta", "Ande, sente e levante em câmera lenta, bem devagar."),
 ("Telefone sem fio", "O adulto fala uma frase baixinho. Repita igualzinho."),
 ("Mão na cabeça", "Toque cabeça, ombro, joelho, pé, cada vez mais rápido sem errar."),
 ("Silêncio do ninja", "Leve um copo de plástico de um lado ao outro da sala sem fazer barulho."),
 ("Número no ar", "O adulto escreve um número no ar. Adivinhe qual foi."),
 ("Torre de 10", "Empilhe 10 objetos (blocos, potes, livros) sem derrubar."),
 ("Conta-carneirinho", "Feche os olhos e conte devagar até 20, respirando entre os números."),
 ("Detetive do som", "Um adulto esconde um despertador ou celular tocando baixinho. Ache pelo som."),
]
def cartoes(parte):
    ic = ['estrela','coracao','sol','flor','lua','peixe','maca','folha','gota','bola','nuvem','gato']
    cores = ['#e4572e','#2b7fd6','#25a065','#8b46b0','#e0930c','#d6457a']
    html_ = '<div class="cartoes">'
    for i in range(12):
        j = parte*12 + i
        t, d = CARTOES[j]
        c = cores[j % len(cores)]
        html_ += f'<div class="ct" style="--c:{c}"><div class="ctt"><span>{j+1}</span>{esc(t)}</div><div class="ctb">{icone_svg(ic[j % len(ic)], "11mm")}<p>{esc(d)}</p></div></div>'
    html_ += '</div>'
    return pag_texto(f"Cartões de foco em movimento {parte+1}/2", "#1b2232", '<p class="intro">Recorte na linha tracejada. Sorteie um cartão por dia.</p>' + html_)

def certificado():
    return f'''<section class="page cert"><div class="borda">
<div class="topo-c">{icone_svg('estrela','16mm')}{icone_svg('sol','16mm')}{icone_svg('estrela','16mm')}</div>
<h1>Certificado de Foco</h1><p>Este certificado é de</p><div class="linha-n"></div>
<p>que completou <b>30 dias</b> de atividades de foco,<br>com esforço, paciência e muita atenção!</p>
<div class="ass"><div><span></span>Data</div><div><span></span>Assinatura do adulto</div></div></div></section>'''

def gab():
    blocos = []; atual = ''
    for i, (n, cat, r) in enumerate(gabarito):
        atual += f'<div class="g"><b>p. {n}</b><span class="gc">{esc(cat)}</span><span>{esc(r)}</span></div>'
        if (i+1) % 22 == 0: blocos.append(atual); atual = ''
    if atual: blocos.append(atual)
    out = []
    for k, b in enumerate(blocos):
        out.append(pag_texto(f"Gabarito {k+1}/{len(blocos)}", "#6a7384", f'<div class="gab">{b}</div>'))
        paginas.append(out[-1])
    return out

# ---------- Montagem ----------
paginas.append(capa())
paginas.append(None)  # índice, preenchido depois
paginas.append(como_usar())
paginas.append(None)  # plano
paginas.append(None)  # quadro
for g in (gerar_caca, gerar_lab, gerar_trilha, gerar_copie, gerar_seq, gerar_igual, gerar_dif, gerar_mem, gerar_conte, gerar_setas):
    g()
cartoes_pg = (len(paginas)+1, len(paginas)+2)
paginas.append(cartoes(0)); paginas.append(cartoes(1))
paginas.append(certificado())
gab()
# preenche as páginas com número fixo
salva = len(paginas)
paginas_tmp = paginas
def com_numero(n, f):
    global paginas
    paginas = paginas_tmp[:n-1]
    h = f()
    return h
paginas_tmp[1] = com_numero(2, lambda: pag_texto("O que tem no kit", "#e4572e", '<div class="indice">' + indice() + '</div>'))
paginas_tmp[3] = com_numero(4, plano)
paginas_tmp[4] = com_numero(5, quadro)
paginas = paginas_tmp

total_ativ = sum(m[3] for m in mapa)
CSS = CSS_BASE + """
.capa { background: #fff8ee; }
.capa .fundo { position: absolute; inset: 0; width: 210mm; height: 297mm; }
.capa-box { position: absolute; left: 30mm; right: 30mm; top: 62mm; background: #fff; border: 3px solid #1b2232; border-radius: 10mm; padding: 12mm 10mm; text-align: center; box-shadow: 0 3mm 0 #1b2232; }
.capa .selo { display: inline-block; background: #e4572e; color: #fff; font-weight: 800; font-size: 11pt; border-radius: 10mm; padding: 1.5mm 5mm; letter-spacing: .06em; text-transform: uppercase; }
.capa h1 { font-family: 'Baloo 2'; font-weight: 800; font-size: 64pt; line-height: .9; margin: 5mm 0 3mm; color: #1b2232; }
.capa .sub { font-size: 15pt; font-weight: 700; color: #3a4354; margin: 0 4mm; line-height: 1.3; }
.capa .nums { display: flex; justify-content: center; gap: 6mm; margin-top: 7mm; }
.capa .nums span { display: flex; flex-direction: column; font-weight: 700; font-size: 10pt; color: #3a4354; background: #fdf1d9; border-radius: 4mm; padding: 2.5mm 4mm; }
.capa .nums b { font-family: 'Baloo 2'; font-size: 26pt; line-height: 1; color: #e4572e; }
.capa .extra { font-size: 10.5pt; font-weight: 700; color: #6a7384; margin-top: 6mm; }
.corpo { position: absolute; left: 16mm; right: 16mm; top: 50mm; bottom: 18mm; }
.corpo .intro { font-size: 12.5pt; font-weight: 600; color: #3a4354; line-height: 1.4; margin: 0 0 6mm; }
.passos { display: flex; flex-direction: column; gap: 5mm; }
.passos .p { display: flex; gap: 5mm; align-items: flex-start; border: 2px solid #1b2232; border-radius: 5mm; padding: 4mm 5mm; }
.passos .p > b { font-family: 'Baloo 2'; font-size: 20pt; background: #2b7fd6; color: #fff; width: 12mm; height: 12mm; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex: none; }
.passos h3 { font-family: 'Baloo 2'; font-size: 15pt; margin: 0; line-height: 1.1; }
.passos p { margin: 1mm 0 0; font-size: 11.5pt; color: #3a4354; line-height: 1.35; }
.aviso { margin-top: 6mm; background: #fff8ee; border-radius: 4mm; padding: 4mm 5mm; font-size: 10pt; color: #3a4354; line-height: 1.4; }
.indice { display: flex; flex-direction: column; gap: 3.2mm; }
.ix { display: flex; align-items: center; gap: 4mm; border: 1.6px solid #ebe3d5; border-radius: 4mm; padding: 2.8mm 4mm; }
.ix .b { width: 7mm; height: 7mm; border-radius: 2mm; flex: none; }
.ix h3 { font-family: 'Baloo 2'; font-size: 13.5pt; margin: 0; line-height: 1.1; }
.ix p { margin: .5mm 0 0; font-size: 10pt; color: #6a7384; }
.ix .pp { margin-left: auto; font-weight: 800; font-size: 11pt; white-space: nowrap; }
.ix > div { flex: 1; }
table.plano { width: 100%; border-collapse: separate; border-spacing: 1.6mm; }
.plano th { font-family: 'Baloo 2'; font-size: 12pt; text-align: center; }
.plano tr th:first-child { text-align: left; width: 24mm; font-size: 11pt; }
.plano td { border: 2px solid #1b2232; border-radius: 3mm; padding: 2.5mm 2mm; text-align: center; vertical-align: top; height: 40mm; position: relative; }
.plano td b { display: block; font-size: 10.5pt; }
.plano td span { display: block; font-size: 9.5pt; color: #3a4354; margin-top: 1mm; }
.plano td i { display: block; font-size: 9pt; color: #6a7384; font-style: normal; margin-top: 1mm; }
.plano td em { position: absolute; bottom: 2mm; left: 0; right: 0; font-style: normal; font-size: 16pt; }
.quadro-c { display: grid; grid-template-columns: repeat(5, 1fr); gap: 3mm; }
.dia { border: 2px solid #1b2232; border-radius: 4mm; height: 34mm; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 1.5mm; }
.dia span { font-weight: 800; font-size: 10pt; }
.cartoes { display: grid; grid-template-columns: repeat(3, 1fr); grid-auto-rows: 53mm; gap: 0; border-top: 1.2px dashed #6a7384; border-left: 1.2px dashed #6a7384; }
.ct { border-right: 1.2px dashed #6a7384; border-bottom: 1.2px dashed #6a7384; padding: 2.5mm; display: flex; flex-direction: column; }
.ctt { background: var(--c); color: #fff; border-radius: 3mm 3mm 0 0; font-family: 'Baloo 2'; font-weight: 800; font-size: 12pt; padding: 1.2mm 3mm; display: flex; align-items: center; gap: 2mm; }
.ctt span { background: #fff; color: var(--c); border-radius: 50%; width: 6mm; height: 6mm; font-size: 9.5pt; display: flex; align-items: center; justify-content: center; flex: none; }
.ctb { border: 2px solid var(--c); border-top: 0; border-radius: 0 0 3mm 3mm; flex: 1; padding: 2mm 3mm; display: flex; flex-direction: column; align-items: center; gap: 1.5mm; text-align: center; }
.ctb p { margin: 0; font-size: 9.6pt; line-height: 1.28; font-weight: 600; }
.cert .borda { position: absolute; inset: 12mm; border: 4px solid #e0930c; border-radius: 8mm; outline: 2px dashed #e0930c; outline-offset: -9px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 15mm; gap: 5mm; }
.cert h1 { font-family: 'Baloo 2'; font-size: 40pt; margin: 0; color: #1b2232; }
.cert p { font-size: 15pt; margin: 0; color: #3a4354; line-height: 1.4; }
.topo-c { display: flex; gap: 5mm; }
.linha-n { width: 130mm; border-bottom: 2px solid #1b2232; height: 16mm; }
.ass { display: flex; gap: 20mm; margin-top: 20mm; font-size: 11pt; color: #6a7384; }
.ass div { display: flex; flex-direction: column; gap: 2mm; width: 60mm; }
.ass span { border-bottom: 1.6px solid #1b2232; height: 10mm; }
.gab { display: flex; flex-direction: column; gap: 1.6mm; font-size: 10pt; }
.g { display: grid; grid-template-columns: 14mm 34mm 1fr; gap: 3mm; border-bottom: 1px solid #ebe3d5; padding-bottom: 1.5mm; line-height: 1.3; }
.g .gc { color: #6a7384; font-weight: 700; }
"""
doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Foco sem Tela</title>{FONTES}<style>{CSS}</style></head><body>' + '\n'.join(paginas) + '</body></html>'
open(sys.argv[1], 'w').write(doc)
print("páginas:", len(paginas), "atividades:", total_ativ, "mapa:", mapa)
