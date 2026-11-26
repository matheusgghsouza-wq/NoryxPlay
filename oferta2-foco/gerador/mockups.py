# Monta as imagens da página (1080x1080) e os criativos (1080x1350) a partir das páginas do PDF.
import sys, os
from comum import icone_svg, FONTES
P = os.path.abspath('pg')
def pg(n, e=False): return f'file://{P}/{"e" if e else ""}p{n:03d}.png'
BASE = FONTES + """<style>*{box-sizing:border-box}body{margin:0;font-family:Nunito,sans-serif;color:#1b2232}
.c{position:relative;overflow:hidden}.folha{position:absolute;border-radius:6px;box-shadow:0 18px 40px rgba(27,34,50,.28),0 2px 6px rgba(27,34,50,.15);background:#fff}
.t{font-family:'Baloo 2';font-weight:800;line-height:.98}.badge{position:absolute;background:#e4572e;color:#fff;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Baloo 2';font-weight:800;text-align:center;transform:rotate(-10deg);box-shadow:0 8px 20px rgba(0,0,0,.2)}
.pill{display:inline-block;background:#1b2232;color:#fff;font-weight:800;border-radius:40px;padding:10px 26px}</style>"""
def folha(n, x, y, w, rot=0, e=False, z=1):
    return f'<img class="folha" src="{pg(n,e)}" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);z-index:{z}">'
def deco(lista):
    return ''.join(f'<div style="position:absolute;left:{x}px;top:{y}px;transform:rotate({r}deg);opacity:{o}">{icone_svg(i, f"{s}px")}</div>' for i, x, y, s, r, o in lista)

IMGS = {}
# 0 capa: pilha de folhas com a capa na frente
IMGS['0-capa'] = (1080, 1080, f'''<div class="c" style="width:1080px;height:1080px;background:#fff3d6">
{deco([('estrela',60,70,90,-12,1),('coracao',930,90,80,10,1),('sol',900,880,100,0,1),('flor',70,900,90,0,1),('peixe',80,480,70,-10,.9),('maca',960,500,70,10,.9)])}
{folha(18,500,190,430,9,z=1)}{folha(6,470,170,430,4,z=2)}{folha(72,170,210,430,-7,z=2)}{folha(1,320,150,460,-1,z=3)}
<div class="badge" style="left:760px;top:720px;width:220px;height:220px;z-index:5"><span style="font-size:76px;line-height:.9">102</span><span style="font-size:26px">atividades</span></div></div>''')
# 1 por dentro: leque de 6 atividades
IMGS['1-por-dentro'] = (1080, 1080, f'''<div class="c" style="width:1080px;height:1080px;background:#e4effb">
<div style="position:absolute;top:56px;width:100%;text-align:center"><div class="t" style="font-size:66px">10 tipos de atividade</div><div style="font-size:30px;font-weight:700;color:#3a4354;margin-top:8px">para treinar a atenção brincando</div></div>
{folha(13,90,230,270,-8)}{folha(26,405,215,270,0)}{folha(52,720,230,270,8)}{folha(62,90,630,270,-4)}{folha(98,405,615,270,2)}{folha(108,720,630,270,6)}</div>''')
# 2 dois níveis
IMGS['2-niveis'] = (1080, 1080, f'''<div class="c" style="width:1080px;height:1080px;background:#e2f4ea">
<div style="position:absolute;top:56px;width:100%;text-align:center"><div class="t" style="font-size:66px">2 níveis de dificuldade</div><div style="font-size:30px;font-weight:700;color:#3a4354;margin-top:8px">cresce junto com a criança</div></div>
{folha(30,90,270,420,-4)}{folha(37,570,270,420,4)}
<div style="position:absolute;left:150px;top:900px" class="pill" ><span style="font-size:32px">Nível 1 · 4 a 6 anos</span></div>
<div style="position:absolute;left:620px;top:900px;background:#25a065" class="pill"><span style="font-size:32px">Nível 2 · 7 a 10 anos</span></div></div>''')
# 3 sem tela: cartões de movimento
IMGS['3-cartoes'] = (1080, 1080, f'''<div class="c" style="width:1080px;height:1080px;background:#fde9ef">
<div style="position:absolute;top:56px;width:100%;text-align:center"><div class="t" style="font-size:62px">+ 24 cartões de movimento</div><div style="font-size:30px;font-weight:700;color:#3a4354;margin-top:8px">foco também se treina com o corpo</div></div>
{folha(117,120,250,470,-5)}{folha(116,500,250,470,5)}</div>''')
# 4 plano e quadro
IMGS['4-plano'] = (1080, 1080, f'''<div class="c" style="width:1080px;height:1080px;background:#fdf1d9">
<div style="position:absolute;top:56px;width:100%;text-align:center"><div class="t" style="font-size:62px">Plano de 4 semanas pronto</div><div style="font-size:30px;font-weight:700;color:#3a4354;margin-top:8px">+ quadro de conquistas e certificado</div></div>
{folha(4,100,250,460,-4)}{folha(5,520,260,460,4)}</div>''')
# 5 imprima e reutilize: folha com "plástico" (brilho)
IMGS['5-imprima'] = (1080, 1080, f'''<div class="c" style="width:1080px;height:1080px;background:#f1e7f7">
<div style="position:absolute;top:56px;width:100%;text-align:center"><div class="t" style="font-size:62px">Imprima quantas vezes quiser</div><div style="font-size:30px;font-weight:700;color:#3a4354;margin-top:8px">ou use no saquinho plástico com canetinha</div></div>
<div style="position:absolute;left:290px;top:240px;width:500px;transform:rotate(-3deg)">{folha(40,0,0,500)}<div style="position:absolute;left:-14px;top:-14px;width:528px;height:735px;border-radius:14px;background:linear-gradient(120deg,rgba(255,255,255,.55) 0%,rgba(255,255,255,0) 30%,rgba(255,255,255,0) 62%,rgba(255,255,255,.4) 75%,rgba(255,255,255,0) 90%);border:3px solid rgba(255,255,255,.9);box-shadow:0 18px 40px rgba(0,0,0,.18);z-index:3"></div></div></div>''')
# 6 bônus emoções
IMGS['6-emocoes'] = (1080, 1080, f'''<div class="c" style="width:1080px;height:1080px;background:#fff8ee">
<div style="position:absolute;top:56px;width:100%;text-align:center"><div class="t" style="font-size:62px">Kit Emoções em Jogo</div><div style="font-size:30px;font-weight:700;color:#3a4354;margin-top:8px">25 folhas para dar nome ao que sente</div></div>
{folha(14,560,280,380,7,True)}{folha(20,140,290,380,-7,True)}{folha(1,350,240,400,0,True,3)}</div>''')

# Criativos 1080x1350
def crt(bg, inner): return f'<div class="c" style="width:1080px;height:1350px;background:{bg}">{inner}</div>'
CTA = lambda t: f'<div style="position:absolute;left:0;right:0;bottom:60px;text-align:center"><span style="display:inline-block;background:#e4572e;color:#fff;font-weight:800;font-size:40px;border-radius:20px;padding:22px 46px;box-shadow:0 8px 0 #b9401d">{t}</span></div>'
IMGS['criativo-1-10min'] = (1080, 1350, crt('#fff3d6', f'''
<div style="position:absolute;top:70px;left:60px;right:60px;text-align:center"><div class="t" style="font-size:98px">10 minutos<br>por dia,<br><span style="color:#e4572e">sem tela</span></div>
<div style="font-size:36px;font-weight:700;color:#3a4354;margin-top:20px">Atividades de atenção para imprimir<br>· 4 a 10 anos ·</div></div>
{folha(26,110,640,340,-9)}{folha(6,630,640,340,9)}{folha(1,370,600,350,0,z=3)}
<div class="badge" style="left:810px;top:520px;width:200px;height:200px;z-index:5"><span style="font-size:30px">só</span><span style="font-size:52px;line-height:.9">R$19,90</span></div>
{CTA("Baixe e imprima hoje")}'''))
IMGS['criativo-2-102'] = (1080, 1350, crt('#e4effb', f'''
<div style="position:absolute;top:60px;left:40px;right:40px;text-align:center"><div class="t" style="font-size:86px"><span style="color:#2b7fd6">102</span> atividades<br>de foco para imprimir</div>
<div style="font-size:34px;font-weight:700;color:#3a4354;margin-top:14px">labirintos · caça-símbolos · memória · sequências</div></div>
{''.join(folha(n, 105 + (i%3)*305, 330 + (i//3)*295, 255, [-4,2,5,3,-3,-5,4,-2,3][i]) for i, n in enumerate([13,26,40,52,62,72,82,98,108]))}
<div style="position:absolute;left:0;right:0;bottom:46px;text-align:center;z-index:10"><span style="display:inline-block;background:#1b2232;color:#fff;font-weight:800;font-size:38px;border-radius:20px;padding:20px 40px">PDF por R$ 19,90 · acesso na hora</span></div>'''))
IMGS['criativo-3-troca'] = (1080, 1350, crt('#ffffff', f'''
<div style="position:absolute;top:60px;left:50px;right:50px;text-align:center"><div class="t" style="font-size:90px">Troque 10 minutos<br>de tela por isto</div></div>
<div style="position:absolute;left:60px;top:380px;width:420px;height:700px;border-radius:30px;background:#f3f4f6;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:30px">
<svg viewBox="0 0 100 160" style="width:180px"><rect x="8" y="6" width="84" height="148" rx="14" fill="#1b2232"/><rect x="16" y="20" width="68" height="114" rx="4" fill="#6a7384"/><circle cx="50" cy="144" r="5" fill="#6a7384"/><path d="M4 30 L96 132" stroke="#e4572e" stroke-width="10" stroke-linecap="round"/></svg>
<div style="font-size:40px;font-weight:800;color:#6a7384">mais tela</div></div>
<div style="position:absolute;left:520px;top:380px;width:500px;height:700px;border-radius:30px;background:#e2f4ea"></div>
{folha(18,580,410,380,-3,z=2)}
<div style="position:absolute;left:520px;top:1012px;width:500px;text-align:center;font-size:40px;font-weight:800;color:#25a065;z-index:3">foco no papel</div>
{CTA("Kit Foco sem Tela · R$ 19,90")}'''))

os.makedirs(sys.argv[1], exist_ok=True)
import json
json.dump({k: [w, h, f'<!doctype html><html><head><meta charset="utf-8">{BASE}</head><body>{body}</body></html>'] for k, (w, h, body) in IMGS.items()}, open('mockups.json', 'w'))
