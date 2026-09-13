// Run against a local replay server; no research API requests are made.
// node tests/check_theatre3d.cjs <playwright module path> [http://127.0.0.1:8766]
const assert = require('node:assert/strict');
const fs = require('node:fs');
const crypto = require('node:crypto');
const { chromium } = require(process.argv[2] || 'playwright');
const base = process.argv[3] || 'http://127.0.0.1:8766';

(async () => {
  const manifest = JSON.parse(fs.readFileSync('viewer/assets/manifest.json'));
  for (const file of ['council', 'boardroom', 'laboratory', 'agent']) {
    const data = fs.readFileSync(`viewer/assets/${file}.glb`);
    assert.equal(data.readUInt32LE(0), 0x46546c67);
    const gltf = JSON.parse(data.subarray(20, 20 + data.readUInt32LE(12)).toString());
    assert.equal(gltf.scenes.length, 1, `${file}: only its intended Blender scene`);
    assert.equal(gltf.scenes[0].name.toLowerCase(), `paria_${file}`);
    // Asset bytes are locked by their local manifest.
    assert.ok(JSON.stringify(manifest).includes(crypto.createHash('sha256').update(data).digest('hex')));
  }
  const browser = await chromium.launch({headless:true});
  try {
    const page = await browser.newPage({viewport:{width:1440,height:1000}});
    const errors = [], remote = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', m => {if(m.type()==='error')errors.push(m.text());});
    page.on('request', r => {if(!r.url().startsWith(base))remote.push(r.url());});
    await page.addInitScript(() => {
      window.frameCount = 0;
      const original = window.requestAnimationFrame;
      window.requestAnimationFrame = fn => original.call(window, t => {window.frameCount++;fn(t);});
    });
    async function ready(id) {
      await page.waitForFunction(id => location.hash === '#'+id && !document.body.classList.contains('busy') && document.querySelector('#error').hidden, id);
    }
    async function example(id) {await page.locator(`[data-run="${id}"]`).click();await ready(id);}
    async function step(n) {await page.locator(`[data-round="${n}"]`).click();}
    await page.goto(base+'/lab');await ready('C1-1-00100-E');
    assert.equal(await page.locator('#world-a .agent-label').count(),5);
    await step(1);
    assert.match(await page.locator('#tally-a').textContent(),/1Package A4Package B/);
    await page.locator('#world-a [data-agent="140"]').click();
    assert.equal(await page.locator('#agent-title').textContent(),'Agent 140');
    assert.match(await page.locator('.response').textContent(),/VOTE: PACKAGE_A/);
    await page.locator('.record-details summary').first().click();
    assert.match(await page.locator('.record-details').first().textContent(),/No previous rounds/);
    await page.locator('[data-tab="profile"]').click();
    assert.equal(await page.locator('.parameter').count(),10);
    const before = await page.locator('#world-a [data-agent="140"]').evaluate(e=>e.style.left+e.style.top);
    await page.locator('#top-camera').click();await page.waitForTimeout(350);
    assert.notEqual(await page.locator('#world-a [data-agent="140"]').evaluate(e=>e.style.left+e.style.top),before);
    await page.locator('#reset-camera').click();
    await page.locator('#compare-toggle').click();await ready('C1-1-00100-E');
    assert.equal(await page.locator('#world-b .agent-label').count(),5);
    assert.match(await page.locator('#tally-b').textContent(),/Ended after 1 round/);
    await step(3);
    await page.locator('#world-b [data-agent="140"]').click();
    assert.match(await page.locator('.notice').textContent(),/NOT supplied/);
    await page.locator('[data-tab="response"]').click();
    assert.match(await page.locator('.response-note').textContent(),/Round 1 \/ final recorded response/);
    await page.screenshot({path:'output/theatre3d_compare.png',fullPage:true});
    await page.locator('#compare-toggle').click();await ready('C1-1-00100-E');
    await example('C2-1-neutral-B');await step(2);
    assert.equal(await page.locator('#world-a .agent-label').count(),6);
    assert.match(await page.locator('#round-note').textContent(),/CEO votes are excluded/);
    assert.match(await page.locator('#shared-body').textContent(),/0 adopted at round start; 1 adopted by round end/);
    assert.match(await page.locator('#shared-body').textContent(),/R1A39 \/ Adopted this round/);
    await page.locator('[data-tab="knowledge"]').click();
    assert.match(await page.locator('#inspector').textContent(),/None. The original proposal/);
    await step(3);
    assert.match(await page.locator('#inspector').textContent(),/R1A39/);
    await page.screenshot({path:'output/theatre3d_boardroom.png',fullPage:true});
    await example('C3-1-00100-E');await step(1);
    assert.equal(await page.locator('#world-a .agent-label').count(),4);
    assert.match(await page.locator('#inspector').textContent(),/Same-round disclosures from others were not yet visible/);
    assert.match(await page.locator('#shared-body').textContent(),/Public at round start \/ 0/);
    assert.match(await page.locator('#events').textContent(),/5 newly disclosed for next round/);
    await step(2);
    assert.match(await page.locator('#shared-body').textContent(),/Public at round start \/ 5/);
    await page.locator('#brief-open').click();
    assert.equal(await page.locator('#brief').evaluate(e=>e.open),true);
    assert.match(await page.locator('#brief-text').textContent(),/outside lab/);
    await page.locator('#brief-close').click();
    await page.locator('[data-tab="response"]').click();
    await page.waitForTimeout(2200);
    await page.screenshot({path:'output/theatre3d_lab.png',fullPage:true});
    const idleFrames = await page.evaluate(()=>window.frameCount);
    await page.waitForTimeout(500);
    assert.equal(await page.evaluate(()=>window.frameCount),idleFrames,'Rendering stops when idle');
    await page.locator('#group').selectOption('5');await ready('C3-5-00100-E');
    await page.locator('#condition').selectOption('neutral-B');await ready('C3-5-neutral-B');
    await step(4);await page.locator('#agent-selector [data-agent="96"]').click();
    assert.match(await page.locator('#agent-vote').textContent(),/Invalid vote/);
    assert.match(await page.locator('.response').textContent(),/VOTE: CONTINUE[\s\S]*VOTE: CONTINUE/);
    await example('C1-1-00100-E');await step(1);
    await page.locator('[data-tab="profile"]').click();
    await page.waitForTimeout(2200);
    await page.screenshot({path:'output/theatre3d_desktop.png',fullPage:true});
    await page.locator('#speed').selectOption('1800');await page.locator('#play').click();
    await page.waitForFunction(()=>document.querySelector('[data-round="5"]').getAttribute('aria-current')==='step');
    assert.equal(await page.locator('#play').textContent(),'Play');
    await page.setViewportSize({width:390,height:844});await page.waitForTimeout(500);
    await page.screenshot({path:'output/theatre3d_mobile.png',fullPage:true});
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'No mobile overflow');
    assert.ok((await page.locator('#world-a').boundingBox()).height<420,'Mobile canvas stays compact');
    assert.ok(await page.locator('#world-a .agent-label').evaluateAll(labels=>{
      const boxes=labels.filter(e=>!e.hidden).map(e=>e.getBoundingClientRect());
      return boxes.every((a,i)=>boxes.slice(i+1).every(b=>a.right<=b.left||a.left>=b.right||a.bottom<=b.top||a.top>=b.bottom));
    }),'Projected mobile labels do not overlap');
    await page.locator('#compare-toggle').click();await ready('C1-1-00100-E');
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'No mobile comparison overflow');
    await page.screenshot({path:'output/theatre3d_mobile_compare.png',fullPage:true});
    await page.emulateMedia({reducedMotion:'reduce'});await step(0);await page.waitForTimeout(300);
    const reducedBefore=await page.evaluate(()=>window.frameCount);
    await step(1);await page.waitForTimeout(300);
    assert.ok((await page.evaluate(()=>window.frameCount))-reducedBefore<=4,'Reduced motion avoids sustained animation');
    for(const route of ['/data/raw/anything','/assets/../../AGENTS.md','/build_assets.py'])assert.equal((await page.request.get(base+route)).status(),404);
    assert.equal((await page.request.post(base+'/api/run/C1-1-00100-E')).status(),501);
    assert.deepEqual(errors,[]);assert.deepEqual(remote,[]);
    const fallback=await browser.newPage();
    await fallback.route('**/assets/*.glb',r=>r.abort());
    await fallback.goto(base+'/lab');await fallback.locator('#error').waitFor({state:'visible'});
    assert.equal(await fallback.locator('#error a').getAttribute('href'),'/');
    const report={passed:true,browser_errors:errors,remote_requests:remote,asset_scenes:4,viewport_widths:[1440,390],checks:['model isolation and hashes','agent selection','exact prompt','ten profile coordinates','camera controls','matched comparison and early ending','CEO exclusion','adoption boundary','evidence boundary','invalid vote retention','playback completion','mobile layout','idle rendering','reduced motion','read-only routes','asset failure fallback']};
    fs.writeFileSync('output/theatre3d_browser_checks.json',JSON.stringify(report,null,2));
    console.log('3D theatre checks passed: four isolated assets, desktop/mobile, recorded state, comparison, idle rendering and fallback.');
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
