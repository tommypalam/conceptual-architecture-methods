const assert=require('node:assert/strict');
const {chromium}=require('../output/viewer-checks/node_modules/playwright-core');
const base=process.argv[2]||'http://127.0.0.1:8770';
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.LOCAL_CHROME||'C:/Users/tpala/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe'});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[],remote=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(!r.url().startsWith(base))remote.push(r.url());});
  await page.goto(base+'/explore');await page.waitForSelector('#p-LL',{state:'attached'});await page.waitForSelector('#preview canvas');
  await page.screenshot({path:'output/explorer-desktop.png',fullPage:true});
  await page.locator('nav [data-page="profile"]').click();assert.equal(await page.locator('input[type=range]').count(),10);
  await page.locator('#p-LL').fill('90');assert.match(await page.locator('#profile-words').innerText(),/0.90/);
  await page.locator('#reset-profile').click();assert.equal(await page.locator('#p-LL').inputValue(),'50');
  await page.locator('nav [data-page="choices"]').click();await page.locator('[data-choice]').first().click();
  assert.equal(await page.locator('#choice-chart .chart-row').count(),4);assert.match(await page.locator('#choice-chart .chart-row').first().innerText(),/75.0%/);
  await page.locator('#study-version').selectOption('r3');assert.match(await page.locator('#choice-chart .chart-row').first().innerText(),/66.7%/);
  await page.locator('#metric').selectOption('strict_good_rate');assert.match(await page.locator('#choice-chart .chart-row').first().innerText(),/0.0%/);
  await page.locator('#dilemma').selectOption('safety_hold');assert.equal(await page.locator('#choice-reveal').isVisible(),false);
  await page.locator('[data-choice]').first().click();await page.locator('#metric').selectOption('net_good_rate');assert.match(await page.locator('#choice-chart .chart-row').first().innerText(),/86.7%/);
  await page.screenshot({path:'output/explorer-moral.png',fullPage:true});
  await page.locator('#contrast').click();assert.equal(await page.locator('#contrast').getAttribute('aria-pressed'),'true');
  await page.locator('nav [data-page="findings"]').click();await page.locator('#latest-view').waitFor();assert.match(await page.locator('#latest-chart').innerText(),/60.0%/);
  await page.locator('#latest-view').selectOption('desk_booking');assert.match(await page.locator('#latest-chart').innerText(),/-15.0/);
  await page.locator('#latest-view').selectOption('pooled');await page.screenshot({path:'output/explorer-findings.png',fullPage:true});
  await page.locator('#tour').click();for(let i=0;i<5;i++)await page.locator('#tour-next').click();assert.equal(await page.locator('#tour-bar').isVisible(),false);
  await page.locator('nav [data-page="rooms"]').click();const frame=page.frameLocator('#theatre');await frame.locator('#verified').filter({hasText:'Verified replay'}).waitFor();await frame.locator('#next').click();assert.match(await frame.locator('#round-position').innerText(),/Round 1/);
  await page.locator('[data-room="C3-1-00100-E"]').click();await frame.locator('#title').filter({hasText:'Research lab'}).waitFor();
  for(const path of ['/sources/capstone','/sources/replication','/sources/wording'])assert.equal((await page.request.get(base+path)).status(),200);
  await page.setViewportSize({width:390,height:844});await page.locator('nav [data-page="choices"]').click();
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));await page.screenshot({path:'output/explorer-mobile.png',fullPage:true});
  await page.emulateMedia({reducedMotion:'reduce'});await page.locator('nav [data-page="welcome"]').click();assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  assert.deepEqual(errors,[]);assert.deepEqual(remote,[]);console.log('PASS: desktop/mobile, 10 sliders, both studies, score switching, tour, rooms, local sources, no external requests or page errors.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
