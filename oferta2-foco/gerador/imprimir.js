// uso: node imprimir.js entrada.html saida.pdf [pasta_png paginas,separadas]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [entrada, saida, pastaPng, lista] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(entrada), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: saida, format: 'A4', printBackground: true, preferCSSPageSize: true });
  if (pastaPng) {
    const secs = await p.$$('section.page');
    const quais = lista ? lista.split(',').map(Number) : secs.map((_, i) => i + 1);
    for (const n of quais) await secs[n - 1].screenshot({ path: `${pastaPng}/p${String(n).padStart(3, '0')}.png` });
  }
  await b.close();
})();
