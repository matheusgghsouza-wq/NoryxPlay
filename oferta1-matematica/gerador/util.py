# Formatação de números em português.
UN = "zero um dois três quatro cinco seis sete oito nove dez onze doze treze catorze quinze dezesseis dezessete dezoito dezenove".split()
DZ = "_ _ vinte trinta quarenta cinquenta sessenta setenta oitenta noventa".split()
CT = "_ cento duzentos trezentos quatrocentos quinhentos seiscentos setecentos oitocentos novecentos".split()
def _ate999(n):
    if n < 20: return UN[n]
    if n < 100: return DZ[n//10] + ("" if n % 10 == 0 else " e " + UN[n % 10])
    if n == 100: return "cem"
    return CT[n//100] + ("" if n % 100 == 0 else " e " + _ate999(n % 100))
def extenso(n):
    if n < 1000: return _ate999(n)
    m, r = divmod(n, 1000)
    pre = "mil" if m == 1 else _ate999(m) + " mil"
    if r == 0: return pre
    junta = " e " if (r < 100 or r % 100 == 0) else " "
    return pre + junta + _ate999(r)
def br(n):
    return f"{n:,}".replace(",", ".")
def dec(x, casas=2):
    return f"{x:.{casas}f}".replace(".", ",")
def reais(x):
    s = f"{x:,.2f}"
    return "R$ " + s.replace(",", "X").replace(".", ",").replace("X", ".")
