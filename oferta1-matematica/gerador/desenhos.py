# Desenhos em SVG usados nas folhas de matemática.
import math
T = "#1b2232"

def svg(vb, inner, w=None, h=None, extra=""):
    st = ";".join(x for x in [f"width:{w}" if w else "", f"height:{h}" if h else ""] if x)
    return f'<svg viewBox="{vb}" style="{st}" {extra}>{inner}</svg>'

def relogio(h, m, tam="30mm", ponteiros=True):
    s = '<circle cx="50" cy="50" r="46" fill="#fff" stroke="#1b2232" stroke-width="3"/>'
    for i in range(60):
        a = math.radians(i*6); r1 = 41 if i % 5 else 37
        s += f'<line x1="{50+44*math.sin(a):.1f}" y1="{50-44*math.cos(a):.1f}" x2="{50+r1*math.sin(a):.1f}" y2="{50-r1*math.cos(a):.1f}" stroke="#1b2232" stroke-width="{1.8 if i%5==0 else .8}"/>'
    for n in range(1, 13):
        a = math.radians(n*30)
        s += f'<text x="{50+30*math.sin(a):.1f}" y="{50-30*math.cos(a):.1f}" font-size="9.5" font-weight="800" font-family="Nunito" text-anchor="middle" dominant-baseline="central" fill="#1b2232">{n}</text>'
    if ponteiros:
        ah = math.radians(((h % 12) + m/60)*30); am = math.radians(m*6)
        s += f'<line x1="50" y1="50" x2="{50+20*math.sin(ah):.1f}" y2="{50-20*math.cos(ah):.1f}" stroke="#2b5fd6" stroke-width="4.5" stroke-linecap="round"/>'
        s += f'<line x1="50" y1="50" x2="{50+32*math.sin(am):.1f}" y2="{50-32*math.cos(am):.1f}" stroke="#e23b3b" stroke-width="3" stroke-linecap="round"/>'
    s += '<circle cx="50" cy="50" r="3.5" fill="#1b2232"/>'
    return svg("0 0 100 100", s, tam, tam)

COR_NOTA = {2: ('#9fc3d9', '#4a7c99'), 5: ('#d4b5e0', '#7d4a99'), 10: ('#f2b09a', '#b5512f'), 20: ('#f5dc8a', '#a3801c'), 50: ('#e5c29f', '#8a5a2b'), 100: ('#a9cfe8', '#2b6a99'), 200: ('#cfd4d9', '#5d6670')}
def cedula(v, w="30mm"):
    c, e = COR_NOTA[v]
    s = (f'<rect x="1" y="1" width="118" height="58" rx="4" fill="{c}" stroke="{e}" stroke-width="2"/>'
         f'<rect x="6" y="6" width="108" height="48" rx="2" fill="none" stroke="{e}" stroke-width=".8" stroke-dasharray="2 1.5"/>'
         f'<circle cx="60" cy="30" r="15" fill="#fff" opacity=".55" stroke="{e}" stroke-width="1.2"/>'
         f'<path d="M53 37 Q53 25 60 22 Q67 25 67 37" fill="none" stroke="{e}" stroke-width="1.6"/><circle cx="60" cy="26" r="4.5" fill="none" stroke="{e}" stroke-width="1.6"/>'
         f'<text x="12" y="20" font-family="Baloo 2" font-weight="800" font-size="18" fill="{e}">{v}</text>'
         f'<text x="108" y="50" text-anchor="end" font-family="Baloo 2" font-weight="800" font-size="18" fill="{e}">{v}</text>'
         f'<text x="12" y="50" font-family="Nunito" font-weight="800" font-size="8" fill="{e}">REAIS</text>')
    return svg("0 0 120 60", s, w)

def moeda(cent, w="12mm"):
    txt, sub = (("1", "REAL") if cent == 100 else (str(cent), "CENTAVOS" if cent > 1 else "CENTAVO"))
    cor = '#e8c45a' if cent in (100, 25, 10) else '#c9cdd2'
    borda = '#a88a2b' if cor == '#e8c45a' else '#7d838a'
    inner = '' if cent != 100 else f'<circle cx="30" cy="30" r="19" fill="#c9cdd2" stroke="{borda}" stroke-width="1"/>'
    s = (f'<circle cx="30" cy="30" r="27" fill="{cor}" stroke="{borda}" stroke-width="2.5"/>{inner}'
         f'<text x="30" y="29" text-anchor="middle" font-family="Baloo 2" font-weight="800" font-size="{20 if len(txt)<3 else 16}" fill="#1b2232">{txt}</text>'
         f'<text x="30" y="42" text-anchor="middle" font-family="Nunito" font-weight="800" font-size="6" fill="#1b2232">{sub}</text>')
    return svg("0 0 60 60", s, w, w)

def pizza(n, k, tam="24mm", cor="#b48ee0"):
    s = ''
    for i in range(n):
        a0 = math.radians(i*360/n - 90); a1 = math.radians((i+1)*360/n - 90)
        big = 1 if 360/n > 180 else 0
        if n == 1:
            s += f'<circle cx="50" cy="50" r="44" fill="{cor if k else "#fff"}" stroke="#1b2232" stroke-width="2.5"/>'; continue
        s += f'<path d="M50 50 L{50+44*math.cos(a0):.2f} {50+44*math.sin(a0):.2f} A44 44 0 {big} 1 {50+44*math.cos(a1):.2f} {50+44*math.sin(a1):.2f}Z" fill="{cor if i < k else "#fff"}" stroke="#1b2232" stroke-width="2.2" stroke-linejoin="round"/>'
    return svg("0 0 100 100", s, tam, tam)

def barra(n, k, w="40mm", cor="#7fc4f0"):
    lw = 100/n
    s = ''.join(f'<rect x="{1+i*lw*0.98:.2f}" y="1" width="{lw*0.98:.2f}" height="18" fill="{cor if i < k else "#fff"}" stroke="#1b2232" stroke-width="1.4"/>' for i in range(n))
    return svg("0 0 100 20", s, w)

def grade100(k, tam="30mm", cor="#7fd49b"):
    s = ''.join(f'<rect x="{1+(i%10)*9.8:.1f}" y="{1+(i//10)*9.8:.1f}" width="9.8" height="9.8" fill="{cor if i < k else "#fff"}" stroke="#1b2232" stroke-width=".7"/>' for i in range(100))
    return svg("0 0 100 100", s, tam, tam)

def blocos(c, d, u, h="20mm"):
    s = ''; x = 2
    for _ in range(c):
        s += f'<rect x="{x}" y="2" width="40" height="40" fill="#ffd34d" stroke="#1b2232" stroke-width="1.2"/>'
        s += ''.join(f'<line x1="{x+i*4}" y1="2" x2="{x+i*4}" y2="42" stroke="#1b2232" stroke-width=".5"/><line x1="{x}" y1="{2+i*4}" x2="{x+40}" y2="{2+i*4}" stroke="#1b2232" stroke-width=".5"/>' for i in range(1, 10))
        x += 45
    for _ in range(d):
        s += f'<rect x="{x}" y="2" width="4" height="40" fill="#7fd49b" stroke="#1b2232" stroke-width="1"/>' + ''.join(f'<line x1="{x}" y1="{2+i*4}" x2="{x+4}" y2="{2+i*4}" stroke="#1b2232" stroke-width=".5"/>' for i in range(1, 10))
        x += 7
    x += 3
    for i in range(u):
        s += f'<rect x="{x + (i % 5)*6}" y="{30 - (i//5)*7}" width="4.5" height="4.5" fill="#ff9d8a" stroke="#1b2232" stroke-width="1"/>'
    largura = x + 32
    return svg(f"0 0 {largura} 44", s, None, h)

def crianca(var=0, tam="20mm"):
    pele, cabelo, camisa = [('#f6c9a0', '#8a4b2a', '#ff9f43'), ('#d9a27a', '#2d1b12', '#54a0ff'), ('#f3d1b5', '#e0a23a', '#1dd1a1'), ('#a8714f', '#1b120d', '#ff6b9a')][var % 4]
    lacos = '<path d="M64 14 l10 -6 v14z M64 14 l-2 -9 l10 1z" fill="#ff6b9a"/>' if var % 4 == 3 else ''
    s = (f'<path d="M22 100 Q22 72 50 70 Q78 72 78 100Z" fill="{camisa}" stroke="#1b2232" stroke-width="2.5"/>'
         f'<circle cx="50" cy="44" r="24" fill="{pele}" stroke="#1b2232" stroke-width="2.5"/>'
         f'<path d="M26 42 Q24 16 50 16 Q78 16 74 42 Q68 28 52 28 Q40 30 26 42Z" fill="{cabelo}" stroke="#1b2232" stroke-width="2"/>{lacos}'
         f'<circle cx="41" cy="46" r="3" fill="#1b2232"/><circle cx="59" cy="46" r="3" fill="#1b2232"/>'
         f'<path d="M41 56 Q50 64 59 56" fill="none" stroke="#1b2232" stroke-width="2.5" stroke-linecap="round"/>'
         f'<circle cx="35" cy="54" r="3.5" fill="#ff9db0" opacity=".7"/><circle cx="65" cy="54" r="3.5" fill="#ff9db0" opacity=".7"/>')
    return svg("0 0 100 100", s, tam, tam)

DECO = {
 'sol': '<circle cx="50" cy="50" r="22" fill="#ffd34d" stroke="#1b2232" stroke-width="2.5"/>' + ''.join(f'<line x1="{50+30*math.cos(math.radians(a)):.1f}" y1="{50+30*math.sin(math.radians(a)):.1f}" x2="{50+42*math.cos(math.radians(a)):.1f}" y2="{50+42*math.sin(math.radians(a)):.1f}" stroke="#f2a516" stroke-width="4" stroke-linecap="round"/>' for a in range(0, 360, 45)) + '<circle cx="43" cy="47" r="2.5" fill="#1b2232"/><circle cx="57" cy="47" r="2.5" fill="#1b2232"/><path d="M42 56 Q50 62 58 56" stroke="#1b2232" stroke-width="2.2" fill="none"/>',
 'borboleta': '<ellipse cx="32" cy="36" rx="20" ry="22" fill="#ffb84d" stroke="#1b2232" stroke-width="2.2"/><ellipse cx="68" cy="36" rx="20" ry="22" fill="#ffb84d" stroke="#1b2232" stroke-width="2.2"/><ellipse cx="36" cy="70" rx="15" ry="15" fill="#7fb8ff" stroke="#1b2232" stroke-width="2.2"/><ellipse cx="64" cy="70" rx="15" ry="15" fill="#7fb8ff" stroke="#1b2232" stroke-width="2.2"/><rect x="46" y="22" width="8" height="62" rx="4" fill="#1b2232"/>',
 'lapis': '<g transform="rotate(-35 50 50)"><rect x="18" y="38" width="56" height="24" fill="#ffd34d" stroke="#1b2232" stroke-width="2.2"/><rect x="10" y="38" width="10" height="24" fill="#ff8fa3" stroke="#1b2232" stroke-width="2.2"/><path d="M74 38 L94 50 L74 62Z" fill="#f6d9b5" stroke="#1b2232" stroke-width="2.2"/><path d="M88 46.5 L94 50 L88 53.5Z" fill="#1b2232"/></g>',
 'maca': '<path d="M50 30 C34 18 10 26 12 52 C14 76 32 94 50 86 C68 94 86 76 88 52 C90 26 66 18 50 30Z" fill="#ff5a4e" stroke="#1b2232" stroke-width="2.5"/><path d="M50 30 Q48 16 56 8" stroke="#1b2232" stroke-width="2.5" fill="none"/><path d="M54 20 Q70 6 80 16 Q66 28 54 20Z" fill="#7fd49b" stroke="#1b2232" stroke-width="2"/>',
 'lampada': '<circle cx="50" cy="40" r="26" fill="#ffd34d" stroke="#1b2232" stroke-width="2.5"/><rect x="38" y="64" width="24" height="16" rx="3" fill="#c9cdd2" stroke="#1b2232" stroke-width="2.2"/><path d="M42 40 Q50 52 58 40" stroke="#1b2232" stroke-width="2" fill="none"/>',
 'porquinho': '<ellipse cx="50" cy="56" rx="36" ry="28" fill="#ffb3c6" stroke="#1b2232" stroke-width="2.5"/><circle cx="82" cy="54" r="9" fill="#ff9db0" stroke="#1b2232" stroke-width="2.2"/><circle cx="79" cy="54" r="1.6" fill="#1b2232"/><circle cx="85" cy="54" r="1.6" fill="#1b2232"/><path d="M58 30 L66 18 L72 32Z" fill="#ffb3c6" stroke="#1b2232" stroke-width="2.2"/><circle cx="66" cy="46" r="2.8" fill="#1b2232"/><rect x="38" y="27" width="18" height="4" rx="2" fill="#1b2232"/><rect x="28" y="78" width="9" height="12" fill="#ffb3c6" stroke="#1b2232" stroke-width="2"/><rect x="62" y="78" width="9" height="12" fill="#ffb3c6" stroke="#1b2232" stroke-width="2"/>',
 'livros': '<rect x="14" y="62" width="72" height="14" rx="3" fill="#7fb8ff" stroke="#1b2232" stroke-width="2.2"/><rect x="20" y="48" width="64" height="14" rx="3" fill="#ffd34d" stroke="#1b2232" stroke-width="2.2"/><rect x="12" y="76" width="76" height="14" rx="3" fill="#b48ee0" stroke="#1b2232" stroke-width="2.2"/><circle cx="52" cy="36" r="11" fill="#ff5a4e" stroke="#1b2232" stroke-width="2.2"/>',
 'estrela': '<polygon points="50,6 61,37 94,38 68,58 78,92 50,72 22,92 32,58 6,38 39,37" fill="#ffd34d" stroke="#1b2232" stroke-width="2.5" stroke-linejoin="round"/>',
}
def deco(nome, tam="11mm"):
    return svg("0 0 100 100", DECO[nome], tam, tam)

OBJ = {  # objetos pequenos para contar
 'maca': DECO['maca'], 'estrela': DECO['estrela'],
 'bola': '<circle cx="50" cy="50" r="42" fill="#7fb8ff" stroke="#1b2232" stroke-width="3"/><path d="M10 44 Q50 62 90 44" stroke="#1b2232" stroke-width="3" fill="none"/>',
 'flor': ''.join(f'<circle cx="{50+22*math.cos(math.radians(a)):.1f}" cy="{50+22*math.sin(math.radians(a)):.1f}" r="17" fill="#ff9dc0" stroke="#1b2232" stroke-width="2.5"/>' for a in range(-90, 270, 72)) + '<circle cx="50" cy="50" r="13" fill="#ffd34d" stroke="#1b2232" stroke-width="2.5"/>',
 'peixe': '<path d="M6 50 Q38 14 72 50 Q38 86 6 50Z" fill="#6fd3c6" stroke="#1b2232" stroke-width="3"/><polygon points="70,50 96,26 96,74" fill="#6fd3c6" stroke="#1b2232" stroke-width="3" stroke-linejoin="round"/><circle cx="26" cy="46" r="5" fill="#1b2232"/>',
 'lapis': DECO['lapis'], 'borboleta': DECO['borboleta'],
}
def obj(nome, tam="8mm"):
    return svg("0 0 100 100", OBJ[nome], tam, tam)
