const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [dirSite, dirCri] = process.argv.slice(2);
  const d = JSON.parse(fs.readFileSync('mockups.json'));
  const b = await chromium.launch();
  for (const [k, [w, h, html]] of Object.entries(d)) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    fs.writeFileSync('/tmp/claude-0/-home-user-NoryxPlay/d371ccf5-98f6-579c-a8b3-c8a2765d49fe/scratchpad/m.html', html);
    await p.goto('file:///tmp/claude-0/-home-user-NoryxPlay/d371ccf5-98f6-579c-a8b3-c8a2765d49fe/scratchpad/m.html', { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    const dir = k.startsWith('criativo') ? dirCri : dirSite;
    await p.screenshot({ path: `${dir}/${k}.${k.startsWith('criativo') ? 'png' : 'jpg'}`, ...(k.startsWith('criativo') ? {} : { type: 'jpeg', quality: 84 }) });
    await p.close();
  }
  await b.close();
})();
