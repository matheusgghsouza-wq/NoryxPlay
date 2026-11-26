# Gera o HTML do Kit Matemática Pronta BNCC (129 folhas + gabarito).
import random, sys, math
from blocos_ex import *
from desenhos import deco, crianca

ANOS = {1: ('#e84a3c', '#f59a90', '#fde5e2'), 2: ('#f2b316', '#f8d77a', '#fff4d4'), 3: ('#27a85a', '#86d1a4', '#e0f4e8'),
        4: ('#2f7fe0', '#8cbcf0', '#e1edfb'), 5: ('#8e52c9', '#c4a2e6', '#efe5f8')}
L = lambda f, *a, **k: (lambda r: f(r, *a, **k))
TEMAS = [
 # 1º ano
 (1, 'Contagem de quantidades', 'EF01MA02', [L(contar, 9), L(contar, 12), L(sequencia, 1, 3, [1]), L(ordenar, 1, 20), L(comparar, 1, 20)]),
 (1, 'Antecessor e sucessor', 'EF01MA04', [L(ant_suc, 1, 50), L(reta, 1, 40), L(ant_suc, 20, 99), L(sequencia, 10, 60, [1]), L(ordenar, 10, 99)]),
 (1, 'Maior, menor ou igual', 'EF01MA05', [L(comparar, 1, 30), L(ordenar, 1, 50), L(comparar, 10, 99), L(contar, 10), L(reta, 1, 30)]),
 (1, 'Dezenas e unidades', 'EF01MA07', [L(blocos_num), L(tabela_valor, 2), L(blocos_num), L(decompor, 2), L(contar, 12)]),
 (1, 'Adição até 20', 'EF01MA06', [L(contas, '+', 1, 9), L(contar, 8), L(contas, '+', 2, 10), L(problemas, 'soma', 2, 10), L(sequencia, 0, 4, [2])]),
 (1, 'Subtração até 20', 'EF01MA08', [L(contas, '-', 1, 20), L(contas, '-', 5, 20), L(problemas, 'sub', 3, 20), L(reta, 1, 10), L(comparar, 1, 20)]),
 (1, 'Sequências e padrões', 'EF01MA10', [L(sequencia, 1, 10, [1, 2]), L(sequencia, 0, 20, [5, 10]), L(reta, 2, 10), L(sequencia, 20, 40, [1, 2], desc=True), L(ordenar, 1, 60)]),
 (1, 'Figuras planas', 'EF01MA14', [L(figuras), L(contar, 9), L(comparar, 1, 20), L(sequencia, 1, 10, [1])]),
 # 2º ano
 (2, 'Números até 999', 'EF02MA01', [L(tabela_valor, 3), L(ant_suc, 100, 999), L(comparar, 100, 999), L(ordenar, 100, 999), L(extenso_ex, 100, 999)]),
 (2, 'Centenas, dezenas e unidades', 'EF02MA04', [L(blocos_num, True), L(decompor, 3), L(tabela_valor, 3), L(blocos_num, True), L(reta, 10, 300)]),
 (2, 'Adição até 100', 'EF02MA05', [L(contas, '+', 10, 50, armada=True), L(contas, '+', 10, 45), L(problemas, 'soma', 10, 45), L(reta, 10, 20)]),
 (2, 'Subtração até 100', 'EF02MA06', [L(contas, '-', 20, 99, armada=True), L(contas, '-', 10, 99), L(problemas, 'sub', 15, 99), L(comparar, 10, 99)]),
 (2, 'Multiplicação com grupos', 'EF02MA07', [L(grupos, 4, 5), L(tabuada, 2), L(problemas, 'mult', 2, 5, 2, 5), L(tabuada, 3)]),
 (2, 'Dobro e metade', 'EF02MA08', [L(dobro_metade, 2, 20), L(parte_de), L(dobro_metade, 10, 40), L(grupos, 2, 6)]),
 (2, 'Horas no relógio', 'EF02MA19', [L(relogios), L(desenhe_ponteiros, (0, 30)), L(relogios), L(desenhe_ponteiros, (0, 30))]),
 (2, 'Cédulas e moedas', 'EF02MA20', [L(dinheiro, (2, 5, 10)), L(troco, 10), L(dinheiro, (2, 5, 10, 20)), L(troco, 20)]),
 (2, 'Sequências numéricas', 'EF02MA09', [L(sequencia, 0, 50, [2, 5, 10]), L(reta, 5, 50), L(sequencia, 50, 100, [3, 5], desc=True), L(ordenar, 50, 500)]),
 # 3º ano
 (3, 'Números até 9.999', 'EF03MA01', [L(tabela_valor, 4), L(extenso_ex, 1000, 9999), L(comparar, 1000, 9999), L(ordenar, 1000, 9999), L(ant_suc, 1000, 9999)]),
 (3, 'Decomposição de números', 'EF03MA02', [L(decompor, 4), L(tabela_valor, 4), L(decompor, 3), L(reta, 100, 2000)]),
 (3, 'Adição e subtração armadas', 'EF03MA05', [L(contas, '+', 100, 899, armada=True), L(contas, '-', 200, 999, armada=True), L(problemas, 'soma', 100, 500), L(problemas, 'sub', 200, 900)]),
 (3, 'Tabuadas do 2, 3, 4, 5 e 10', 'EF03MA03', [L(tabuada, 2), L(tabuada, 3), L(tabuada, 4), L(tabuada, 5), L(tabuada, 10), L(contas, '×', 2, 10, lo2=2, hi2=5)]),
 (3, 'Multiplicação', 'EF03MA07', [L(grupos, 5, 6), L(contas, '×', 11, 40, armada=True, lo2=2, hi2=5), L(problemas, 'mult', 3, 9, 2, 6), L(contas, '×', 2, 10, lo2=2, hi2=10)]),
 (3, 'Divisão exata', 'EF03MA08', [L(partilha), L(contas, '÷', 2, 10, lo2=2, hi2=5), L(problemas, 'div', 2, 9, 2, 5), L(partilha)]),
 (3, 'Metade, terça e quarta parte', 'EF03MA09', [L(parte_de), L(fracao_desenho, (2, 3, 4)), L(parte_de), L(fracao_desenho, (2, 3, 4), tipo='barra')]),
 (3, 'Leitura de horas', 'EF03MA23', [L(relogios, (0, 15, 30, 45)), L(desenhe_ponteiros), L(duracao), L(relogios, (0, 10, 20, 40, 50))]),
 (3, 'Dinheiro e troco', 'EF03MA24', [L(dinheiro, (2, 5, 10, 20, 50), (50, 25, 10)), L(troco, 50), L(dinheiro, (5, 10, 20, 50)), L(troco, 30)]),
 # 4º ano
 (4, 'Números até 99.999', 'EF04MA01', [L(tabela_valor, 5), L(extenso_ex, 10000, 99999), L(comparar, 10000, 99999), L(ordenar, 10000, 99999), L(ant_suc, 10000, 99999)]),
 (4, 'Adição e subtração', 'EF04MA03', [L(contas, '+', 1000, 9999, armada=True), L(contas, '-', 2000, 9999, armada=True), L(problemas, 'soma', 1000, 5000), L(problemas, 'sub', 2000, 9999)]),
 (4, 'Multiplicação', 'EF04MA06', [L(contas, '×', 12, 99, armada=True, lo2=3, hi2=9), L(mult_10), L(problemas, 'mult', 12, 30, 3, 9), L(tabuada, 6), L(tabuada, 7)]),
 (4, 'Divisão com resto', 'EF04MA07', [L(divisao_resto), L(contas, '÷', 11, 30, lo2=2, hi2=9), L(problemas, 'div', 11, 25, 3, 8), L(divisao_resto, 3, 9)]),
 (4, 'Frações unitárias', 'EF04MA09', [L(fracao_desenho, (2, 3, 4, 5, 6, 8)), L(parte_de), L(fracao_desenho, (4, 5, 6, 8, 10), tipo='barra'), L(comparar_frac)]),
 (4, 'Décimos e centésimos', 'EF04MA10', [L(decimal_grade), L(decimal_escrita), L(comparar, 100, 999, dec_=True), L(decimal_grade)]),
 (4, 'Dinheiro com centavos', 'EF04MA10', [L(dinheiro, (2, 5, 10, 20, 50), (50, 25, 10, 5)), L(troco, 50), L(contas_dec, '+'), L(troco, 100)]),
 (4, 'Medidas de tempo', 'EF04MA22', [L(relogios, (0, 5, 10, 20, 25, 35, 40, 50, 55)), L(duracao), L(desenhe_ponteiros, (5, 20, 35, 50)), L(duracao)]),
 # 5º ano
 (5, 'Números até 999.999', 'EF05MA01', [L(tabela_valor, 6), L(extenso_ex, 100000, 999999), L(comparar, 100000, 999999), L(ordenar, 100000, 999999), L(decompor, 6)]),
 (5, 'Números decimais', 'EF05MA02', [L(decimal_grade), L(decimal_escrita), L(comparar, 100, 999, dec_=True), L(decimal_grade)]),
 (5, 'Frações', 'EF05MA03', [L(fracao_desenho, (3, 4, 5, 6, 8)), L(fracao_desenho, (5, 6, 8, 10), tipo='barra'), L(comparar_frac), L(parte_de)]),
 (5, 'Frações equivalentes', 'EF05MA04', [L(equivalentes), L(equivalentes), L(comparar_frac), L(fracao_desenho, (4, 6, 8), tipo='barra')]),
 (5, 'Porcentagem', 'EF05MA06', [L(porcent_grade), L(porcent_de), L(porcent_grade), L(decimal_grade)]),
 (5, 'Adição e subtração com decimais', 'EF05MA07', [L(contas_dec, '+'), L(contas_dec, '-'), L(dinheiro, (5, 10, 20, 50, 100), (50, 25, 10, 5)), L(troco, 100)]),
 (5, 'Multiplicação por 2 algarismos', 'EF05MA08', [L(contas, '×', 12, 99, armada=True, lo2=11, hi2=35), L(mult_10), L(problemas, 'mult', 12, 45, 11, 25), L(contas, '×', 11, 30, lo2=11, hi2=20)]),
 (5, 'Divisão e problemas', 'EF05MA08', [L(divisao_resto, 3, 12), L(contas, '÷', 12, 40, lo2=6, hi2=15), L(problemas, 'div', 12, 40, 6, 15), L(problemas, 'mult', 15, 60, 12, 25)]),
 (5, 'Problemas de adição e subtração', 'EF05MA07', [L(problemas, 'soma', 1000, 50000), L(problemas, 'sub', 5000, 90000), L(contas, '+', 10000, 99999, armada=True), L(contas, '-', 20000, 99999, armada=True)]),
]
TIPOS = ['Fixação', 'Revisão', 'Avaliação']
DECOS = ['sol', 'borboleta', 'lapis', 'maca', 'lampada', 'livros', 'estrela']

def montar(r, pool, k):
    ordem = pool[k % len(pool):] + pool[:k % len(pool)]
    if k == 2: r.shuffle(ordem)
    sel = []; fulls = halves = 0
    for i in range(12):
        f = ordem[i % len(ordem)]
        w, t, h, a = f(r)
        nf, nh = fulls + (w == 'f'), halves + (w == 'h')
        if nf + math.ceil(nh/2) > 4 or len(sel) >= 6: continue
        sel.append([w, t, h, a]); fulls, halves = nf, nh
        if nf + math.ceil(nh/2) == 4 and nh % 2 == 0: break
    # agrupa em linhas: meias em pares
    linhas = []; pend = None
    for q in sel:
        if q[0] == 'f': linhas.append([q])
        elif pend: linhas.append([pend, q]); pend = None
        else: pend = q
    if pend: pend[0] = 'f'; linhas.append([pend])
    return linhas

paginas = []; gab = []; sumario = []
folha_n = 0
def onda_top(c1, c2):
    return (f'<svg class="ondat" viewBox="0 0 210 40" preserveAspectRatio="none"><path d="M0 0H210V31Q199 38 188 31T166 31T144 31T122 31T100 31T78 31T56 31T34 31T12 31T0 33Z" fill="{c2}"/>'
            f'<path d="M0 0H210V27Q199 34 188 27T166 27T144 27T122 27T100 27T78 27T56 27T34 27T12 27T0 29Z" fill="{c1}"/></svg>')
def onda_bot(c1):
    return f'<svg class="ondab" viewBox="0 0 210 10" preserveAspectRatio="none"><path d="M0 10V5Q5.5 0 11 5T22 5T33 5T44 5T55 5T66 5T77 5T88 5T99 5T110 5T121 5T132 5T143 5T154 5T165 5T176 5T187 5T198 5T210 5V10Z" fill="{c1}"/></svg>'

R = random.Random(129)
for ti, (ano, tema, cod, pool) in enumerate(TEMAS):
    c1, c2, c3 = ANOS[ano]
    sumario.append((ano, tema, cod, folha_n + 1))
    for k in range(3):
        folha_n += 1
        linhas = montar(R, pool, k)
        n = 0; corpo = ''; resp = []
        for lin in linhas:
            corpo += '<div class="lin">'
            for w, t, h, a in lin:
                n += 1
                dz = deco(R.choice(DECOS), "9mm") if R.random() < .45 else ''
                corpo += f'<div class="q {w}"><div class="qt"><b style="background:{c1}">{n}</b><span>{t}</span>{dz}</div><div class="qc">{h}</div></div>'
                resp.append(f"{n}) {a}")
            corpo += '</div>'
        kid = crianca(R.randint(0, 3), "19mm")
        nota = '<span class="nota">Nota: ______</span>' if k == 2 else ''
        paginas.append(f'''<section class="page" style="--c1:{c1};--c2:{c2};--c3:{c3}">{onda_top(c1, c2)}
<div class="cab"><div class="kid">{kid}</div><div class="tit"><small>Matemática · {ano}º ano · {TIPOS[k]}</small><h1>{tema}</h1></div>
<div class="bncc"><span>BNCC</span><b>{cod}</b></div></div>
<div class="nd"><span>Nome:</span><span class="m">Turma:</span><span class="m">Data:</span>{nota}</div>
<div class="corpo">{corpo}</div>{onda_bot(c1)}<div class="rod">Matemática Pronta BNCC · Folha {folha_n}</div></section>''')
        gab.append((folha_n, ano, tema, TIPOS[k], resp))

CAPA = f'''<section class="page capa">{onda_top('#e84a3c', '#f59a90')}
<div class="cbox"><div class="cubos">{''.join(f'<span style="background:{ANOS[a][0]}">{a}º</span>' for a in ANOS)}</div>
<h1>Matemática<br>Pronta BNCC</h1><p class="sub">129 atividades para imprimir do 1º ao 5º ano</p>
<div class="nums"><span><b>129</b>folhas</span><span><b>43</b>temas</span><span><b>5</b>anos</span></div>
<p class="ex">Código da BNCC em cada folha · Gabarito completo</p></div>
<div class="kids">{''.join(crianca(i, "28mm") for i in range(4))}</div>{onda_bot('#2f7fe0')}</section>'''

def pag_txt(titulo, cor, corpo):
    return f'<section class="page" style="--c1:{cor}">{onda_top(cor, cor + "88")}<div class="cab"><div class="tit"><small>Matemática Pronta BNCC</small><h1>{titulo}</h1></div></div><div class="txt">{corpo}</div>{onda_bot(cor)}</section>'

COMO = pag_txt("Como usar o kit", "#2f7fe0", '''
<div class="passos"><div><b>1</b><p><b>Cada ano tem uma cor.</b> 1º vermelho, 2º amarelo, 3º verde, 4º azul e 5º roxo. Imprima e separe no fichário por cor.</p></div>
<div><b>2</b><p><b>Cada tema tem 3 folhas.</b> Fixação (para aprender), Revisão (para praticar) e Avaliação (para verificar, com espaço para nota).</p></div>
<div><b>3</b><p><b>O código da BNCC fica no canto de cada folha.</b> Use no planejamento e no diário de classe.</p></div>
<div><b>4</b><p><b>Reutilize.</b> Coloque a folha num saquinho plástico ou plastifique e use canetinha de quadro branco.</p></div>
<div><b>5</b><p><b>Gabarito no final,</b> organizado pelo número da folha (rodapé de cada página).</p></div></div>
<p class="obs">Pode imprimir quantas vezes quiser para seus alunos e filhos. Não é permitido revender ou compartilhar o arquivo.</p>''')

def sumario_pags():
    out = []
    por_ano = {a: [s for s in sumario if s[0] == a] for a in ANOS}
    grupos = [[1, 2, 3], [4, 5]]
    for g in grupos:
        corpo = ''
        for a in g:
            c = ANOS[a][0]
            corpo += f'<h2 style="color:{c}">{a}º ano</h2><div class="sum">' + ''.join(f'<div><span class="b" style="background:{c}"></span>{t}<i>{cd}</i><b>folhas {f}–{f+2}</b></div>' for _, t, cd, f in por_ano[a]) + '</div>'
        out.append(pag_txt("Sumário", "#1b2232", corpo))
    return out

def gabarito_pags():
    out = []; blocos = []; atual = []; tam = 0
    for f, ano, tema, tipo, resp in gab:
        item = f'<div class="g"><b style="color:{ANOS[ano][0]}">Folha {f}</b> <span>{ano}º · {tema} · {tipo}</span><p>{" &nbsp; ".join(resp)}</p></div>'
        peso = 1.4 + sum(len(x) for x in resp)/110
        if tam + peso > 34: blocos.append(atual); atual = []; tam = 0
        atual.append(item); tam += peso
    if atual: blocos.append(atual)
    for i, b in enumerate(blocos):
        out.append(pag_txt(f"Gabarito {i+1}/{len(blocos)}", "#6a7384", '<div class="gab">' + ''.join(b) + '</div>'))
    return out

CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
body { margin: 0; font-family: 'Nunito', sans-serif; color: #1b2232; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; position: relative; overflow: hidden; page-break-after: always; background: #fff; }
.ondat { position: absolute; top: 0; left: 0; width: 210mm; height: 40mm; }
.ondab { position: absolute; bottom: 0; left: 0; width: 210mm; height: 9mm; }
.cab { position: absolute; top: 4mm; left: 10mm; right: 10mm; height: 24mm; display: flex; align-items: center; gap: 4mm; color: #fff; }
.kid { background: #fff; border-radius: 50%; width: 22mm; height: 22mm; display: flex; align-items: center; justify-content: center; flex: none; border: 2px solid #1b2232; overflow: hidden; }
.tit { flex: 1; } .tit small { font-weight: 800; font-size: 10pt; letter-spacing: .04em; opacity: .95; }
.tit h1 { font-family: 'Baloo 2'; font-weight: 800; font-size: 23pt; line-height: 1.02; margin: .5mm 0 0; text-shadow: 0 .6mm 0 rgba(0,0,0,.15); }
.bncc { background: #fff; color: #1b2232; border-radius: 3mm; padding: 1.5mm 3mm; text-align: center; border: 2px solid #1b2232; flex: none; }
.bncc span { display: block; font-size: 8pt; font-weight: 800; letter-spacing: .14em; color: var(--c1); } .bncc b { font-family: 'Baloo 2'; font-size: 14pt; line-height: 1; }
.nd { position: absolute; top: 40mm; left: 10mm; right: 10mm; display: flex; gap: 5mm; font-weight: 800; font-size: 10.5pt; align-items: flex-end; }
.nd span { flex: 1; border-bottom: 1.5px solid #1b2232; padding-bottom: .5mm; } .nd .m { flex: .32; }
.nd .nota { flex: .4; border: 2px solid var(--c1); border-radius: 2mm; padding: 1mm 2mm; }
.corpo { position: absolute; top: 49mm; bottom: 15mm; left: 10mm; right: 10mm; display: flex; flex-direction: column; gap: 3.2mm; }
.lin { flex: 1; display: flex; gap: 3.2mm; min-height: 0; }
.q { flex: 1; border: 2px solid #1b2232; border-radius: 4mm; padding: 2.5mm 3.5mm; display: flex; flex-direction: column; min-width: 0; position: relative; background: #fff; }
.qt { display: flex; align-items: center; gap: 2.2mm; font-weight: 800; font-size: 11pt; text-transform: uppercase; letter-spacing: .01em; line-height: 1.15; }
.qt b { color: #fff; width: 6.5mm; height: 6.5mm; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex: none; font-family: 'Baloo 2'; font-size: 11pt; }
.qt span { flex: 1; } .qt svg { flex: none; }
.qc { flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 2mm; font-size: 12.5pt; font-weight: 700; min-height: 0; }
.cx { display: inline-block; width: 15mm; height: 8.5mm; border: 1.6px solid var(--c1); border-radius: 1.8mm; vertical-align: middle; background: #fff; }
.cx.p { width: 10mm; } .cx.g { width: 24mm; height: 10mm; flex: none; }
.ln { display: block; border-bottom: 1.4px solid #9aa2b1; height: 7mm; }
.lst { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm 4mm; } .ch { white-space: nowrap; } .ch.sm { font-size: 10.5pt; white-space: normal; }
.q.h .lst { grid-template-columns: 1fr; gap: 2.4mm; }
.cen { display: flex; justify-content: center; align-items: center; gap: 2mm; text-align: center; } .col { flex-direction: column; } .pq { font-size: 11pt; }
.duas { display: flex; justify-content: space-around; align-items: center; gap: 3mm; }
.lin3 { display: flex; justify-content: space-around; gap: 3mm; } .lin4 { display: flex; justify-content: space-around; }
.grp { display: flex; flex-direction: column; align-items: center; gap: 2mm; } .objs { display: flex; flex-wrap: wrap; gap: 1mm; justify-content: center; max-width: 52mm; }
.tb { border-collapse: collapse; width: 100%; text-align: center; } .tb th { background: var(--c3); font-size: 9.5pt; text-transform: uppercase; }
.tb th, .tb td { border: 1.5px solid #1b2232; padding: 1mm; height: 8mm; } .tb td { font-size: 13pt; font-family: 'Baloo 2'; }
.cdu td { height: 11mm; font-size: 17pt; }
.cmp { display: flex; align-items: center; gap: 3mm; justify-content: center; } .circ { width: 9mm; height: 9mm; border: 1.6px solid var(--c1); border-radius: 50%; display: inline-block; vertical-align: middle; }
.seq { display: flex; justify-content: center; gap: 2mm; flex-wrap: wrap; } .sq { min-width: 15mm; height: 10mm; padding: 0 1.5mm; border: 1.6px solid #1b2232; border-radius: 2mm; display: flex; align-items: center; justify-content: center; font-family: 'Baloo 2'; font-size: 12.5pt; background: var(--c3); }
.sq.v { background: #fff; border-color: var(--c1); border-style: dashed; }
.fg { display: flex; flex-direction: column; align-items: center; gap: 1mm; width: 38mm; } .fg .ln { width: 100%; height: 6mm; } .fg small { font-size: 10pt; }
.gps { display: flex; flex-wrap: wrap; justify-content: center; gap: 3mm; } .gp { border: 1.6px dashed var(--c1); border-radius: 50%; padding: 2.5mm; display: flex; flex-wrap: wrap; width: 26mm; justify-content: center; gap: .6mm; }
.tab { display: grid; grid-template-columns: 1fr; gap: 1.4mm; font-size: 13pt; }
.arm { display: flex; justify-content: space-around; } .ca { display: flex; flex-direction: column; align-items: flex-end; font-family: 'Baloo 2'; font-size: 16pt; line-height: 1.1; min-width: 26mm; }
.ca i { font-style: normal; color: var(--c1); margin-right: 2mm; } .ca .tr { border-bottom: 2px solid #1b2232; width: 100%; } .ca .vz { height: 9mm; width: 100%; border: 1.4px dashed var(--c2); border-radius: 1.5mm; margin-top: 1mm; }
.din { display: flex; align-items: center; justify-content: center; gap: 2mm; flex-wrap: wrap; } .din .op { font-family: 'Baloo 2'; font-size: 18pt; }
.pb { margin: 0; font-size: 11.5pt; font-weight: 700; line-height: 1.3; }
.pr { display: flex; align-items: center; gap: 4mm; justify-content: space-between; }
.fr { display: inline-flex; flex-direction: column; align-items: center; gap: .8mm; } .fr i { width: 12mm; border-top: 2px solid #1b2232; } .fr .cx { height: 7mm; }
.hr { font-family: 'Baloo 2'; font-size: 15pt; color: var(--c1); }
.rod { position: absolute; bottom: 9.5mm; left: 0; right: 0; text-align: center; font-size: 8.5pt; font-weight: 800; color: #6a7384; }
.capa { background: #fff8ee; }
.cbox { position: absolute; top: 50mm; left: 25mm; right: 25mm; background: #fff; border: 3px solid #1b2232; border-radius: 10mm; padding: 12mm 8mm; text-align: center; box-shadow: 0 3mm 0 #1b2232; }
.cubos { display: flex; justify-content: center; gap: 3mm; } .cubos span { width: 15mm; height: 15mm; border-radius: 3mm; color: #fff; font-family: 'Baloo 2'; font-weight: 800; font-size: 16pt; display: flex; align-items: center; justify-content: center; border: 2px solid #1b2232; }
.cbox h1 { font-family: 'Baloo 2'; font-size: 54pt; line-height: .95; margin: 7mm 0 3mm; } .sub { font-size: 15pt; font-weight: 700; color: #3a4354; margin: 0; }
.nums { display: flex; justify-content: center; gap: 5mm; margin-top: 7mm; } .nums span { background: #fff4d4; border-radius: 4mm; padding: 2.5mm 5mm; font-weight: 700; display: flex; flex-direction: column; } .nums b { font-family: 'Baloo 2'; font-size: 26pt; line-height: 1; color: #e84a3c; }
.ex { font-weight: 800; color: #6a7384; margin: 6mm 0 0; }
.kids { position: absolute; bottom: 22mm; left: 0; right: 0; display: flex; justify-content: center; gap: 8mm; }
.txt { position: absolute; top: 40mm; left: 15mm; right: 15mm; bottom: 16mm; }
.passos { display: flex; flex-direction: column; gap: 5mm; } .passos > div { display: flex; gap: 5mm; align-items: center; border: 2px solid #1b2232; border-radius: 5mm; padding: 4mm 5mm; }
.passos > div > b { font-family: 'Baloo 2'; font-size: 20pt; color: #fff; background: #2f7fe0; width: 12mm; height: 12mm; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex: none; }
.passos p { margin: 0; font-size: 12.5pt; line-height: 1.4; } .obs { margin-top: 8mm; font-size: 11pt; color: #6a7384; }
.txt h2 { font-family: 'Baloo 2'; font-size: 18pt; margin: 2mm 0 1.5mm; }
.sum > div { display: flex; align-items: center; gap: 3mm; border-bottom: 1px solid #ebe3d5; padding: 1.6mm 0; font-weight: 700; font-size: 11.5pt; }
.sum .b { width: 4mm; height: 4mm; border-radius: 1mm; flex: none; } .sum i { font-style: normal; color: #6a7384; font-size: 10pt; margin-left: 2mm; } .sum > div > b { margin-left: auto; font-size: 10.5pt; }
.gab { display: flex; flex-direction: column; gap: 1.6mm; font-size: 9.2pt; } .g { border-bottom: 1px solid #ebe3d5; padding-bottom: 1.2mm; } .g span { color: #6a7384; font-weight: 700; } .g p { margin: .5mm 0 0; line-height: 1.35; }
"""
from comum_fontes import FONTES
docs = [CAPA, COMO] + sumario_pags() + paginas + gabarito_pags()
open(sys.argv[1], 'w').write(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Matemática Pronta BNCC</title>{FONTES}<style>{CSS}</style></head><body>' + '\n'.join(docs) + '</body></html>')
print('temas', len(TEMAS), 'folhas', folha_n, 'páginas', len(docs), {a: sum(1 for t in TEMAS if t[0] == a) for a in ANOS})
