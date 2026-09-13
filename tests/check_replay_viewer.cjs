// Browser integration checks against the running local replay server.
// Usage: node tests/check_replay_viewer.cjs <path-to-playwright-or-playwright-core>
const assert = require('node:assert/strict');
const fs = require('node:fs');
const { chromium } = require(process.argv[2] || 'playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto('http://127.0.0.1:8765');
    await page.waitForFunction(() => document.querySelector('#provenance').textContent.includes('checks passed'));
    assert.equal(await page.locator('.seat').count(), 5);
    assert.equal(await page.locator('.parameter').count(), 10);
    assert.equal(await page.locator('#position').textContent(), '0 / 5');
    await page.locator('#next').click();
    assert.equal(await page.locator('.statement').count(), 5);
    assert.match(await page.locator('#tally').textContent(), /1Package A4Package B/);
    await page.locator('.statement').first().click();
    assert.match(await page.locator('.response-text').textContent(), /VOTE:/);
    await page.locator('.raw-prompt summary').first().click();
    assert.match(await page.locator('.raw-prompt').first().textContent(), /No previous rounds/);
    await page.locator('#condition').selectOption('00100-U');
    await page.waitForFunction(() => location.hash.endsWith('00100-U') && !document.body.classList.contains('loading'));
    assert.equal(await page.locator('#table-result').textContent(), 'Package A');
    await page.locator('[data-tab="profile"]').click();
    assert.match(await page.locator('.profile-note').textContent(), /NOT supplied/);
    await page.locator('[data-run="C2-1-neutral-B"]').click();
    await page.waitForFunction(() => location.hash === '#C2-1-neutral-B' && !document.body.classList.contains('loading'));
    await page.locator('#next').click();
    await page.locator('#next').click();
    assert.equal(await page.locator('.seat').count(), 6);
    assert.match(await page.locator('#round-note').textContent(), /excluded/);
    await page.locator('#shared summary').click();
    assert.match(await page.locator('#shared-body').textContent(), /R1A39 · ADOPTED THIS ROUND/);
    assert.match(await page.locator('#shared-body').textContent(), /round start had 0 adopted/);
    await page.locator('#next').click();
    assert.match(await page.locator('#shared-body').textContent(), /round start had 1 adopted/);
    await page.locator('[data-run="C3-1-00100-E"]').click();
    await page.waitForFunction(() => location.hash === '#C3-1-00100-E' && !document.body.classList.contains('loading'));
    await page.locator('#next').click();
    assert.match(await page.locator('#shared-count').textContent(), /^0 available at round start/);
    await page.locator('[data-tab="knowledge"]').click();
    assert.match(await page.locator('#inspector-body').textContent(), /Same-round disclosures/);
    await page.locator('.comparison summary').click();
    await page.locator('#compare').click();
    await page.waitForFunction(() => document.querySelectorAll('#comparison-body tbody tr').length === 5);
    assert.equal(await page.locator('#comparison-body tbody tr').count(), 5);
    await page.locator('#brief-button').click();
    assert.equal(await page.locator('#brief').evaluate(d => d.open), true);
    assert.match(await page.locator('#brief-text').textContent(), /outside lab/);
    await page.locator('#close-brief').click();
    // The known duplicate-marker vote stays missing; its evidence is not silently erased.
    const failed = await (await page.request.get('http://127.0.0.1:8765/api/run/C3-5-neutral-B')).json();
    const bad = failed.rounds[3].responses.find(r => r.agent === 96);
    assert.equal(bad.vote, null);
    assert.match(bad.text, /VOTE: CONTINUE[\s\S]*VOTE: CONTINUE/);
    assert.equal(failed.result.status, 'ok');
    assert.equal((await page.request.get('http://127.0.0.1:8765/api/run/nonexistent')).status(), 404);
    assert.equal((await page.request.get('http://127.0.0.1:8765/data/raw/anything')).status(), 404);
    assert.equal((await page.request.post('http://127.0.0.1:8765/api/run/C1-1-00100-E')).status(), 501);
    // Return to a useful explanatory view for screenshots.
    await page.locator('[data-run="C1-1-00100-E"]').click();
    await page.waitForFunction(() => location.hash === '#C1-1-00100-E' && !document.body.classList.contains('loading'));
    await page.locator('#next').click();
    await page.locator('[data-tab="profile"]').click();
    await page.screenshot({path:'output/replay_desktop.png', fullPage:true});
    await page.locator('#speed').selectOption('1500');
    await page.locator('#play').click();
    await page.waitForFunction(() => document.querySelector('#position').textContent === '5 / 5');
    assert.equal(await page.locator('#play').textContent(), '▶ Play');
    await page.setViewportSize({width:390,height:844});
    await page.screenshot({path:'output/replay_mobile.png', fullPage:true});
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), 'No mobile horizontal overflow');
    assert.deepEqual(errors, []);
    fs.writeFileSync('output/replay_browser_checks.json', JSON.stringify({passed:true, browser_errors:errors, viewport_widths:[1440,390], checks:['playback','profile omission','exact prompt','CEO exclusion','adoption barrier','evidence barrier','matched comparison','invalid vote preservation','allowlisted routes','mobile layout']},null,2));
    console.log('Replay browser checks passed (desktop + mobile; no browser errors).');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
