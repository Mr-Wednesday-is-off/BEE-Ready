const { chromium } = require('playwright');
(async () => {
  const [,, html, outDir] = process.argv;
  const b = await chromium.launch();
  for (const [name, size] of [['icon-512.png',512],['icon-maskable-512.png',512],['icon-192.png',192],['apple-touch-icon.png',180]]) {
    const p = await b.newPage({ viewport: { width: size, height: size }, deviceScaleFactor: 1 });
    await p.goto('file://' + html);
    await p.evaluate(s => { const e = document.getElementById('icon'); e.setAttribute('width', s); e.setAttribute('height', s); }, size);
    await (await p.$('#icon')).screenshot({ path: outDir + '/' + name, omitBackground: true });
    await p.close();
  }
  await b.close();
})();
