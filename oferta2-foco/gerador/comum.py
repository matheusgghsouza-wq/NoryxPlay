# Peças compartilhadas pelos geradores de PDF (ícones, cabeçalho ondulado, página).
import html

TINTA = "#1b2232"
ICONES = {
 'estrela':  '<polygon points="50,6 61,37 94,38 68,58 78,92 50,72 22,92 32,58 6,38 39,37" fill="#ffd34d"/>',
 'coracao':  '<path d="M50 88 C22 68 7 52 7 33 A21 21 0 0 1 50 24 A21 21 0 0 1 93 33 C93 52 78 68 50 88Z" fill="#ff9db0"/>',
 'circulo':  '<circle cx="50" cy="50" r="40" fill="#9fd8ff"/>',
 'quadrado': '<rect x="12" y="12" width="76" height="76" rx="7" fill="#aee8a6"/>',
 'triangulo':'<polygon points="50,9 92,87 8,87" fill="#ffbb7a"/>',
 'losango':  '<polygon points="50,6 91,50 50,94 9,50" fill="#cdb0ff"/>',
 'lua':      '<path d="M60 8 A42 42 0 1 0 93 64 A33 33 0 1 1 60 8Z" fill="#fff0a0"/>',
 'sol':      '<g><line x1="50" y1="4" x2="50" y2="18"/><line x1="50" y1="82" x2="50" y2="96"/><line x1="4" y1="50" x2="18" y2="50"/><line x1="82" y1="50" x2="96" y2="50"/><line x1="17" y1="17" x2="27" y2="27"/><line x1="73" y1="73" x2="83" y2="83"/><line x1="17" y1="83" x2="27" y2="73"/><line x1="73" y1="27" x2="83" y2="17"/></g><circle cx="50" cy="50" r="23" fill="#ffd34d"/>',
 'flor':     '<circle cx="50" cy="24" r="16" fill="#ffb3d1"/><circle cx="75" cy="42" r="16" fill="#ffb3d1"/><circle cx="66" cy="72" r="16" fill="#ffb3d1"/><circle cx="34" cy="72" r="16" fill="#ffb3d1"/><circle cx="25" cy="42" r="16" fill="#ffb3d1"/><circle cx="50" cy="50" r="13" fill="#ffd34d"/>',
 'peixe':    '<path d="M8 50 Q38 16 70 50 Q38 84 8 50Z" fill="#86dccf"/><polygon points="68,50 94,28 94,72" fill="#86dccf"/><circle cx="27" cy="46" r="4.5" fill="#1b2232" stroke="none"/>',
 'maca':     '<path d="M50 30 C34 18 10 26 12 52 C14 76 32 94 50 86 C68 94 86 76 88 52 C90 26 66 18 50 30Z" fill="#ff8a7a"/><path d="M50 30 Q48 16 56 8"/><path d="M54 20 Q70 6 80 16 Q66 28 54 20Z" fill="#aee8a6"/>',
 'nuvem':    '<path d="M24 78 A18 18 0 0 1 22 42 A22 22 0 0 1 62 30 A20 20 0 0 1 80 78Z" fill="#e3f1ff"/>',
 'gota':     '<path d="M50 6 C50 6 18 46 18 64 A32 32 0 0 0 82 64 C82 46 50 6 50 6Z" fill="#9fd8ff"/>',
 'casa':     '<polygon points="50,8 92,46 8,46" fill="#ff8a7a"/><rect x="18" y="46" width="64" height="46" fill="#fff0a0"/><rect x="42" y="62" width="16" height="30" fill="#ffbb7a"/>',
 'arvore':   '<rect x="42" y="58" width="16" height="36" fill="#d9a066"/><circle cx="50" cy="38" r="32" fill="#aee8a6"/>',
 'bola':     '<circle cx="50" cy="50" r="40" fill="#ffffff"/><path d="M12 40 Q50 58 88 40"/><path d="M30 14 Q46 50 30 86"/>',
 'gato':     '<polygon points="16,40 22,8 44,28" fill="#ffd9a8"/><polygon points="84,40 78,8 56,28" fill="#ffd9a8"/><circle cx="50" cy="56" r="36" fill="#ffd9a8"/><circle cx="37" cy="52" r="4.5" fill="#1b2232" stroke="none"/><circle cx="63" cy="52" r="4.5" fill="#1b2232" stroke="none"/><path d="M44 66 Q50 72 56 66"/>',
 'carro':    '<path d="M6 64 V50 L24 46 L34 28 H66 L78 46 L94 50 V64Z" fill="#9fd8ff"/><circle cx="28" cy="68" r="11" fill="#ffffff"/><circle cx="72" cy="68" r="11" fill="#ffffff"/>',
 'guarda':   '<path d="M8 50 A42 42 0 0 1 92 50Z" fill="#cdb0ff"/><path d="M50 50 V82 A8 8 0 0 1 34 82"/>',
 'folha':    '<path d="M14 86 C10 40 40 12 88 12 C88 60 60 90 14 86Z" fill="#aee8a6"/><path d="M14 86 L64 36"/>',
}
NOMES = {'estrela':'estrela','coracao':'coração','circulo':'círculo','quadrado':'quadrado','triangulo':'triângulo','losango':'losango','lua':'lua','sol':'sol','flor':'flor','peixe':'peixe','maca':'maçã','nuvem':'nuvem','gota':'gota','casa':'casa','arvore':'árvore','bola':'bola','gato':'gato','carro':'carro','guarda':'guarda-chuva','folha':'folha'}

def icone(nome, x, y, tam, rot=0):
    """Ícone em coordenadas do SVG pai (unidades do viewBox), canto superior esquerdo em x,y."""
    s = tam / 100
    r = f' rotate({rot} 50 50)' if rot else ''
    return (f'<g transform="translate({x:.2f} {y:.2f}) scale({s:.4f}){r}" stroke="{TINTA}" stroke-width="{max(3.2, 4.2/ max(s,0.6)):.1f}" '
            f'stroke-linejoin="round" stroke-linecap="round" fill="none">{ICONES[nome]}</g>')

def icone_svg(nome, tam_css="14mm"):
    return f'<svg viewBox="-4 -4 108 108" style="width:{tam_css};height:{tam_css}">{icone(nome,0,0,100)}</svg>'

def esc(t):
    return html.escape(t, quote=False)

def onda(cor, cor2):
    return (f'<svg class="onda" viewBox="0 0 210 46" preserveAspectRatio="none">'
            f'<path d="M0 0H210V38Q192 46 171 39T127 38T84 40T40 37T0 40Z" fill="{cor2}"/>'
            f'<path d="M0 0H210V32Q190 40 168 33T124 32T80 34T38 31T0 34Z" fill="{cor}"/></svg>')

def relogio(cor="#fff"):
    return (f'<svg viewBox="0 0 24 24" style="width:5mm;height:5mm"><circle cx="12" cy="13" r="8.5" fill="none" stroke="{cor}" stroke-width="2.2"/>'
            f'<path d="M12 9v4.5l3 2M9.5 2.5h5" stroke="{cor}" stroke-width="2.2" fill="none" stroke-linecap="round"/></svg>')

CSS_BASE = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { font-family: 'Nunito', sans-serif; color: #1b2232; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; position: relative; overflow: hidden; page-break-after: always; background: #fff; }
.onda { position: absolute; left: 0; top: 0; width: 210mm; height: 46mm; }
.cab { position: absolute; left: 14mm; right: 14mm; top: 7mm; color: #fff; display: flex; justify-content: space-between; align-items: flex-start; gap: 6mm; }
.cab .cat { font-weight: 800; font-size: 9.5pt; letter-spacing: .14em; text-transform: uppercase; opacity: .95; }
.cab h1 { font-family: 'Baloo 2', sans-serif; font-weight: 800; font-size: 25pt; line-height: 1.02; margin: 1mm 0 0; }
.cab .dir { display: flex; flex-direction: column; align-items: flex-end; gap: 2mm; flex: none; }
.pill { background: #fff; color: #1b2232; font-weight: 800; font-size: 9.5pt; border-radius: 20mm; padding: 1.2mm 3.6mm; white-space: nowrap; }
.tempo { display: flex; align-items: center; gap: 1.5mm; font-weight: 800; font-size: 10pt; }
.nome { position: absolute; left: 14mm; right: 14mm; top: 48mm; display: flex; gap: 8mm; font-weight: 700; font-size: 11pt; }
.nome span { flex: 1; border-bottom: 1.6px solid #1b2232; padding-bottom: .6mm; }
.nome span.curto { flex: .45; }
.instr { position: absolute; left: 14mm; right: 14mm; top: 58mm; display: flex; gap: 3.5mm; align-items: center; border-radius: 4mm; padding: 3mm 4.5mm; font-size: 12.5pt; font-weight: 700; line-height: 1.3; }
.instr b.n { font-family: 'Baloo 2'; font-size: 15pt; color: #fff; width: 9mm; height: 9mm; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex: none; }
.quadro { position: absolute; left: 14mm; right: 14mm; top: 78mm; bottom: 20mm; border: 2.4px solid #1b2232; border-radius: 6mm; overflow: hidden; }
.quadro > svg { width: 100%; height: 100%; display: block; }
.rod { position: absolute; left: 14mm; right: 14mm; bottom: 7mm; display: flex; justify-content: space-between; font-size: 9pt; color: #6a7384; font-weight: 700; }
.rod .pg { font-family: 'Baloo 2'; font-weight: 800; font-size: 11pt; color: #1b2232; }
"""

FONTES = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@400;600;700;800&display=block">'

def pagina_atividade(n, marca, cat, titulo, nivel, minutos, instrucao, conteudo_svg, cor, cor2, clara, extra_html=""):
    return f'''<section class="page">{onda(cor, cor2)}
<div class="cab"><div><div class="cat">{esc(cat)}</div><h1>{esc(titulo)}</h1></div>
<div class="dir"><span class="pill">{esc(nivel)}</span><span class="tempo">{relogio()} {minutos} min</span></div></div>
<div class="nome"><span>Nome:</span><span class="curto">Data:</span></div>
<div class="instr" style="background:{clara}"><b class="n" style="background:{cor}">!</b><div>{instrucao}</div></div>
<div class="quadro">{conteudo_svg}</div>{extra_html}
<div class="rod"><span>{esc(marca)}</span><span class="pg">{n}</span></div></section>'''
