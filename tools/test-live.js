const { chromium } = require('C:/Users/HUAWEI/.workbuddy/binaries/node/workspace/node_modules/playwright-core');
const BASE = 'https://yjj0339.github.io/tanchishe-3d/';
(async () => {
  const errors = [];
  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:/Users/HUAWEI/.agent-browser/browsers/chrome-150.0.7871.115/chrome.exe',
    args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox', '--disable-gpu-sandbox']
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
  page.on('response', r => { if (r.status() >= 400) errors.push('HTTP ' + r.status() + ' ' + r.url()); });
  await page.goto(BASE, { waitUntil: 'load' });
  await page.waitForFunction(() => window.__game && document.getElementById('playBtn').textContent === '开 战', null, { timeout: 30000 });
  console.log('LIVE MENU OK, snakes:', await page.evaluate(() => window.__game.snakes.length));
  await page.evaluate(() => window.__game.start('线上测试', 0x00c853));
  await page.waitForTimeout(8000);
  const stats = await page.evaluate(() => window.__game.stats());
  console.log('LIVE PLAY:', JSON.stringify(stats));
  await page.screenshot({ path: 'shots/live_desktop.png' });

  const mob = await browser.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  mob.on('pageerror', e => errors.push('MOB PAGEERROR: ' + e.message));
  await mob.goto(BASE, { waitUntil: 'load' });
  await mob.waitForFunction(() => window.__game && document.getElementById('playBtn').textContent === '开 战', null, { timeout: 30000 });
  await mob.evaluate(() => window.__game.start('手机蛇', 0xff9800));
  await mob.waitForTimeout(5000);
  const overflow = await mob.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
  console.log('LIVE MOBILE:', JSON.stringify(await mob.evaluate(() => window.__game.stats())), 'h-overflow:', overflow);
  await mob.screenshot({ path: 'shots/live_mobile.png' });
  console.log('ERRORS:', errors.length ? errors.join('\n') : 'CLEAN');
  await browser.close();
  process.exit(errors.length ? 1 : 0);
})().catch(e => { console.error('FATAL', e.message); process.exit(2); });
