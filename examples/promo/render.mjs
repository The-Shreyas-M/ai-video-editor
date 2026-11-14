// usage: node render.mjs cfg.json   -> writes frames_<name>/%05d.jpg then you encode with ffmpeg
import { createRequire } from 'module';
import os from 'os';
import fs from 'fs';
import path from 'path';
import { pathToFileURL } from 'url';
const require = createRequire(path.join(os.homedir(), '.claude/tools/claude-animation-skills/kit/'));
const { chromium } = require('playwright');
const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const frames = path.resolve(cfg.frames);
fs.mkdirSync(frames, { recursive: true });
const only = process.argv[3] ? process.argv[3].split(',').map(Number) : null; // optional frame times for a preview
const browser = await chromium.launch({ channel: 'chrome' });
const page = await browser.newPage({ viewport: { width: cfg.width, height: cfg.height } });
await page.addInitScript(c => { window.CFG = c; }, cfg);
await page.goto(pathToFileURL(path.resolve('promo.html')).href);
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(400);
if (only) {
  for (const t of only) { await page.evaluate(x => window.setTime(x), t); await page.screenshot({ path: path.join(frames, `p_${t}.jpg`), type: 'jpeg', quality: 85 }); }
} else {
  const n = Math.round(cfg.total * cfg.fps);
  for (let i = 0; i < n; i++) {
    await page.evaluate(x => window.setTime(x), i / cfg.fps);
    await page.screenshot({ path: path.join(frames, String(i).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 88 });
    if (i % 300 === 0) console.log(`frame ${i}/${n}`);
  }
}
await browser.close();
console.log('done');
