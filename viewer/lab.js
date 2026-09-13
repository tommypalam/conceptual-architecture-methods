import { World } from '/world.js';

const $ = selector => document.querySelector(selector);
const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const names = {C1:'Resource council',C2:'Restructuring board',C3:'Research lab'};
const descriptions = {C1:'Five members. Two resource packages. One shared decision.',C2:'Five board members and a CEO. Follow the working plan.',C3:'Four founders. Private evidence. A shared scientific decision.'};
const rules = {
  C1:'Each round is binding. Unanimous agreement by five members ends the council early. Otherwise the fifth round’s majority decides.',
  C2:'The CEO participates but their vote is not counted. Proposals register only through a valid amendment action. The CEO can adopt earlier proposals in rounds 2–4. The five board members’ round 5 vote is binding.',
  C3:'Founders receive private evidence across rounds. Authenticated disclosures become public in the next round. Round 6 is binding; a 2–2 tie uses the recorded seeded random tie-break. Evidence provenance does not validate an interpretation.'
};
const labels={PACKAGE_A:'Package A',PACKAGE_B:'Package B',APPROVE:'Approve',REJECT:'Reject',CONTINUE:'Continue',PIVOT:'Pivot'};
const endpoints={LL:['External warrant','Internal endorsement'],CS:['Low sensitivity','High sensitivity'],RT:['Tolerant','Hair-trigger'],MoR:['Reflective','Confrontational'],RE:['Abstract-person','Role-sensitive'],PD:['Outcome-dominant','Process-dominant'],TfA:['Egalitarian','Hierarchical'],ID:['Surface compliance','Genuine endorsement'],MS:['Local / role-bound','Broad moral scope'],AW:['Deliberative','Affective']};
const pretty = vote => labels[vote] || 'Invalid vote';
const arm = run => ({E:'Encoded profile',U:'Context only',B:'Neutral / no profile'}[run.arm]);
const condition = run => `${arm(run)} / ${run.config}`;
const cache=new Map();
let index, primary, secondary, worldA, worldB, selected, round=0, tab='response', side='a', comparing=false, timer=null, version=0;
const active=()=>side==='b'&&comparing?secondary:primary;
const current=run=>round&&run?run.rounds[Math.min(round,run.rounds.length)-1]:null;
const maximum=()=>Math.max(primary?.rounds.length||0,comparing?secondary?.rounds.length||0:0);
const kind=(vote,run)=>vote===run.labels[0]?'a':vote===run.labels[1]?'b':'missing';
const badge=(vote,run)=>`<span class="vote-badge ${kind(vote,run)}">${escape(pretty(vote))}</span>`;
async function json(url){const response=await fetch(url);if(!response.ok)throw Error(`The recording could not be loaded (${response.status}).`);return response.json();}
async function getRun(id){if(!cache.has(id))cache.set(id,await json(`/api/run/${encodeURIComponent(id)}`));return cache.get(id);}
function stop(){clearInterval(timer);timer=null;$('#play').textContent='Play';}
function error(message){stop();$('#error').hidden=false;$('#error').replaceChildren(document.createTextNode(message+' '));const link=document.createElement('a');link.href='/';link.textContent='Open the classic viewer';$('#error').append(link);}
function idFromControls(){return `${$('#problem').value}-${$('#group').value}-${$('#condition').value}`;}
async function load(id,preserve=false){
  stop();const token=++version,previousRound=round;
  document.body.classList.add('busy');$('#error').hidden=true;
  try{
    const next=await getRun(id);
    if(token!==version)return;
    let other=null;
    if(comparing)other=await getRun(`${next.problem}-${next.group}-${$('#compare-condition').value}`);
    if(token!==version)return;
    // Finish asset loads before committing visible replay state.
    await Promise.all([worldA.setRun(next),...(comparing?[worldB.setRun(other)]:[])]);
    if(token!==version)return;
    primary=next;secondary=other;round=preserve?Math.min(previousRound,maximum()):0;
    if(!primary.agents.some(a=>a.agent_id===selected))selected=primary.agents[0].agent_id;
    $('#problem').value=primary.problem;$('#group').value=primary.group;$('#condition').value=`${primary.config}-${primary.arm}`;
    $('#title').textContent=names[primary.problem];$('#subtitle').textContent=descriptions[primary.problem];
    $('#study-label').textContent=`Phase 2 / Group ${String(primary.group).padStart(2,'0')} / Recorded simulation`;
    $('#verified').textContent=`Verified replay · ${index.seed} seed · ${index.runs.length} group runs available`;
    $('#brief-title').textContent=names[primary.problem];$('#brief-text').textContent=primary.scenario;$('#brief-rules').textContent=rules[primary.problem];
    $('#caption-a').textContent=condition(primary);$('#caption-b').textContent=secondary?condition(secondary):'';
    history.replaceState(null,'',`/lab#${primary.id}`);
    render(false);
  }catch(e){if(token===version)error(e.message);}
  finally{if(token===version)document.body.classList.remove('busy');}
}
function choose(agent,where='a'){
  if(!primary||document.body.classList.contains('busy'))return;
  selected=agent;side=where;render(false);
  if(innerWidth<=760)$('.details').scrollIntoView({block:'start',behavior:'instant'});
}
function play(){
  if(!primary||document.body.classList.contains('busy'))return;
  if(timer){stop();return;}
  if(round>=maximum())round=0;
  round++;render(true);
  if(round>=maximum())return;
  $('#play').textContent='Pause';
  timer=setInterval(()=>{round++;render(true);if(round>=maximum())stop();},Number($('#speed').value));
}
function step(next){if(!primary||document.body.classList.contains('busy'))return;stop();const forward=next===round+1;round=Math.max(0,Math.min(maximum(),next));render(forward);}
async function toggleComparison(){
  if(!primary)return;
  stop();comparing=!comparing;side='a';
  if(comparing){
    $('#compare-condition').value=primary.arm==='E'?`${primary.config}-U`:primary.arm==='U'?`${primary.config}-E`:'00100-E';
    $('#world-b').hidden=false;
    try{worldB??=new World($('#world-b'),id=>choose(id,'b'));}catch(e){comparing=false;error('This browser could not open a second 3D view.');}
  }
  $('#world-b').hidden=!comparing;$('#compare-controls').hidden=!comparing;$('#tally-b').hidden=!comparing;
  $('#compare-toggle').setAttribute('aria-pressed',comparing);$('#compare-toggle').textContent=comparing?'Single room':'Compare conditions';
  document.body.classList.toggle('comparing',comparing);
  await load(primary.id,true);
}
function outcome(run){
  const state=current(run),ended=round>=run.rounds.length;
  const title=!state?'Before round 1':ended?pretty(run.result.outcome):`Round ${round}`;
  const detail=!state?'Press play to begin':ended?`Ended after ${run.rounds.length} ${run.rounds.length===1?'round':'rounds'}${run.result.consensus?' / unanimous':''}${run.result.tie_break?' / seeded tie-break':''}`:'Recorded votes / leans';
  return `<div class="outcome-heading"><h3>${escape(title)}</h3><small>${escape(detail)}</small></div><div class="vote-totals">${run.labels.map((label,i)=>`<span class="${i?'b':''}"><b>${state?state.tally[label]:'–'}</b>${escape(pretty(label))}</span>`).join('')}${state?.tally.missing?`<span class="missing">${state.tally.missing} invalid</span>`:''}</div>`;
}
function render(animate){
  if(!primary)return;
  worldA.update(round,side==='a'?selected:null,animate&&round<=primary.rounds.length);
  if(comparing&&secondary)worldB.update(round,side==='b'?selected:null,animate&&round<=secondary.rounds.length);
  $('#tally-a').innerHTML=outcome(primary);if(comparing&&secondary)$('#tally-b').innerHTML=outcome(secondary);
  $('#timeline').innerHTML=Array.from({length:maximum()+1},(_,n)=>`<button data-round="${n}" class="${n===round?'current':n<round?'past':''}" aria-label="${n?'Round '+n:'Before round 1'}" aria-current="${n===round?'step':'false'}">${n||'Start'}</button>`).join('');
  $('#round-position').textContent=round?`Round ${round} of ${maximum()}`:'Before round 1';
  $('#previous').disabled=round===0;$('#next').disabled=round===maximum();
  $('#round-note').textContent=`${primary.problem==='C2'?'CEO votes are excluded. Round 5 is binding.':primary.problem==='C3'?'Round 6 is binding. New disclosures become public next round.':'Unanimity ends the council; otherwise round 5’s majority decides.'} Responses within each round are simultaneous.${comparing?' An early-ending conversation holds its final state.':''}`;
  renderEvents();renderInspector();
}
function eventDescriptions(run){
  const state=current(run);if(!state)return [];
  if(round>run.rounds.length)return ['Conversation already complete'];
  const events=[];
  const changed=state.responses.filter(r=>r.changed);
  if(changed.length)events.push(`${changed.length} ${changed.length===1?'agent changed':'agents changed'} vote`);
  if(state.tally.missing)events.push(`${state.tally.missing} invalid vote preserved`);
  if(run.problem==='C2'){
    const added=Object.keys(state.proposals_after).filter(id=>!(id in state.proposals_before));
    const adopted=state.adopted_after.filter(id=>!state.adopted_before.includes(id));
    if(added.length)events.push(`${added.length} new ${added.length===1?'proposal':'proposals'}`);
    if(adopted.length)events.push(`Adopted: ${adopted.join(', ')}`);
  }
  if(run.problem==='C3'){
    const added=state.public_after.filter(id=>!state.public_before.includes(id));
    events.push(`${state.public_before.length} evidence items public at round start`);
    if(added.length)events.push(`${added.length} newly disclosed for next round`);
  }
  if(!events.length)events.push(round===1?'First recorded positions':'No valid adjacent-round vote changes');
  return events;
}
function renderEvents(){
  const list=round?eventDescriptions(primary):['Choose a figure to inspect its profile. Press play when you’re ready.'];
  $('#events').innerHTML=list.map(text=>`<span class="event-chip">${escape(comparing?'Left: '+text:text)}</span>`).join('');
  if(comparing&&secondary&&round)$('#events').innerHTML+=eventDescriptions(secondary).map(text=>`<span class="event-chip">Right: ${escape(text)}</span>`).join('');
}
function evidenceList(ids,run){return ids.length?ids.map(id=>`<div class="item"><b>${escape(id)}</b><p>${escape(run.evidence.find(e=>e.item_id===id)?.content||'No supplied item with this ID.')}</p></div>`).join(''):'<p class="fine">None at this point.</p>';}
function renderInspector(){
  const run=active();if(!run)return;
  const state=current(run),response=state?.responses.find(r=>r.agent===selected),agent=run.agents.find(a=>a.agent_id===selected);
  $('#agent-title').textContent=`Agent ${selected}`;
  $('#agent-vote').innerHTML=response?badge(response.vote,run):'';
  $('#role').textContent=`${selected===run.ceo?'CEO / vote not counted':run.problem==='C3'?'Founder / voting participant':'Member / voting participant'}${comparing?' / '+condition(run):''}`;
  $('#agent-selector').innerHTML=run.agents.map(a=>`<button data-agent="${a.agent_id}" aria-label="Inspect agent ${a.agent_id}" aria-pressed="${a.agent_id===selected}">${a.agent_id}${a.agent_id===run.ceo?' ★':''}</button>`).join('');
  document.querySelectorAll('[data-tab]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.tab===tab));
  let html='';
  if(tab==='response'){
    html=response?`<p class="response-note">Round ${state.number}${round>run.rounds.length?' / final recorded response':''}${response.changed?' / changed from '+escape(pretty(response.previous_vote)):''}${response.vote?'':' / invalid or ambiguous vote'}</p><div class="response">${escape(response.text)}</div><details class="record-details"><summary>Exact incoming prompt</summary><p class="fine">Peers received structured excerpts from earlier rounds. This is the exact input to this response.</p>${response.messages.map(m=>`<pre>${escape(m.role.toUpperCase()+'\n\n'+m.content)}</pre>`).join('')}</details><details class="record-details"><summary>Record provenance</summary><pre>${escape(response.record+'\nSHA-256: '+response.record_hash+'\nField errors: '+JSON.stringify(response.field_errors))}</pre></details>`:'<div class="empty">You have a seat at the table.<br>Press play to reveal the first round, then select any agent to read its complete response.</div>';
  }else if(tab==='profile'){
    html=`<div class="notice ${run.arm==='E'?'':'absent'}">${run.arm==='E'?'This fixed ten-coordinate profile was supplied before every response.':'Matched profile only. These values were NOT supplied in this condition.'}</div>`;
    html+=index.parameters.map(p=>`<div class="parameter" title="${escape('0: '+p.endpoint_0+'\n1: '+p.endpoint_1)}"><div class="parameter-top"><span><strong>${escape(p.name)}</strong>${escape(p.label)}</span><span class="parameter-value">${agent.parameters[p.name].toFixed(4)}</span></div><div class="parameter-bar"><i style="width:${agent.parameters[p.name]*100}%"></i></div><div class="parameter-ends"><span>${escape(endpoints[p.name][0])}</span><span>${escape(endpoints[p.name][1])}</span></div></div>`).join('');
  }else if(!response){html='<div class="empty">Advance to a round to inspect the information this agent had when responding.</div>';}
  else if(run.problem==='C3'){
    html=`<div class="notice">Information available when this response was generated. Same-round disclosures from others were not yet visible.</div><h3 class="section-title">Directly held / ${response.held.length}</h3>${evidenceList(response.held,run)}<h3 class="section-title">Public at round start / ${state.public_before.length}</h3>${evidenceList(state.public_before,run)}`;
  }else if(run.problem==='C2'){
    html=`<div class="notice">The original proposal, earlier-round transcript and authoritative working plan were supplied.</div><h3 class="section-title">Adopted before this round</h3>${state.adopted_before.length?state.adopted_before.map(id=>`<div class="item"><b>${escape(id)}</b><p>${escape(state.proposals_before[id])}</p></div>`).join(''):'<p class="fine">None. The original proposal was still the working plan.</p>'}<p class="fine">Response → Exact incoming prompt includes the proposal list and transcript.</p>`;
  }else{html=`<div class="notice">The locked dilemma and ${state.number-1} earlier rounds of structured transcript were available. This task has no private evidence packets.</div><p class="fine">Response → Exact incoming prompt shows the actual input.</p>`;}
  $('#inspector').innerHTML=html;
  $('#round-label').textContent=state?`Round ${state.number}${round>run.rounds.length?' / ended':''}`:'Before round 1';
  $('#messages').innerHTML=state?state.responses.map(r=>`<button class="message ${selected===r.agent?'selected':''}" data-agent="${r.agent}" data-response="true"><div class="message-head"><b>Agent ${r.agent}${r.agent===run.ceo?' / CEO':''}</b>${badge(r.vote,run)}</div><p>${escape(r.fields.REASONING||r.text)}</p>${r.changed?`<small>${escape(pretty(r.previous_vote))} → ${escape(pretty(r.vote))}</small>`:''}</button>`).join(''):'<p class="fine">The discussion will appear here. Every round is revealed together.</p>';
  $('#shared').hidden=run.problem==='C1';
  if(run.problem==='C3'){
    const before=state?.public_before||[],after=state?.public_after||[];
    $('#shared-body').innerHTML=`<h3 class="section-title">Public at round start / ${before.length}</h3>${evidenceList(before,run)}<h3 class="section-title">Newly disclosed / available next round</h3>${evidenceList(after.filter(id=>!before.includes(id)),run)}<p class="fine">Arcs illustrate authenticated disclosures. They do not establish semantic accuracy or causal influence.</p>`;
  }else if(run.problem==='C2'){
    const proposals=state?.proposals_after||{},adopted=state?.adopted_after||[];
    $('#shared-body').innerHTML=`<p class="fine">${state?.adopted_before.length||0} adopted at round start; ${adopted.length} adopted by round end.</p>`+(Object.keys(proposals).length?Object.entries(proposals).map(([id,text])=>`<div class="item"><b>${escape(id)} / ${adopted.includes(id)?'Adopted':'Proposed only'}${adopted.includes(id)&&!state.adopted_before.includes(id)?' this round':''}</b><p>${escape(text)}</p></div>`).join(''):'<p class="fine">No registered proposals yet.</p>');
  }
}

$('#fullscreen').hidden=!document.fullscreenEnabled;
$('#fullscreen').addEventListener('click',async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{ $('#fullscreen').textContent='Use F11'; }});
document.addEventListener('fullscreenchange',()=>{$('#fullscreen').textContent=document.fullscreenElement?'Exit full screen':'Full screen';});

$('#group').innerHTML=Array.from({length:20},(_,i)=>`<option value="${i+1}">${String(i+1).padStart(2,'0')}</option>`).join('');
for(const id of ['problem','group','condition'])$(`#${id}`).addEventListener('change',()=>load(idFromControls(),id==='condition'));
$('#play').addEventListener('click',play);$('#previous').addEventListener('click',()=>step(round-1));$('#next').addEventListener('click',()=>step(round+1));
$('#speed').addEventListener('change',stop);
$('#compare-toggle').addEventListener('click',toggleComparison);
$('#compare-condition').addEventListener('change',()=>load(primary.id,true));
$('#reset-camera').addEventListener('click',()=>{worldA?.reset();worldB?.reset();});
$('#top-camera').addEventListener('click',()=>{worldA?.reset(true);worldB?.reset(true);});
$('#brief-open').addEventListener('click',()=>{if(primary){stop();$('#brief').showModal();}});$('#brief-close').addEventListener('click',()=>$('#brief').close());
document.addEventListener('click',event=>{
  const agent=event.target.closest('.details [data-agent]'),roundButton=event.target.closest('[data-round]'),example=event.target.closest('[data-run]'),tabButton=event.target.closest('[data-tab]');
  if(agent){if(agent.dataset.response)tab='response';choose(Number(agent.dataset.agent),side);}
  if(roundButton)step(Number(roundButton.dataset.round));
  if(example)load(example.dataset.run);
  if(tabButton&&primary){tab=tabButton.dataset.tab;renderInspector();}
});
document.addEventListener('keydown',e=>{if(!primary||$('#brief').open||e.target.closest('button,select,input,summary,a,textarea'))return;if(e.code==='Space'){e.preventDefault();play();}if(e.code==='ArrowRight'){e.preventDefault();step(round+1);}if(e.code==='ArrowLeft'){e.preventDefault();step(round-1);}});
document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
(async()=>{
  try{
    index=await json('/api/index');
    await document.fonts.ready;
    worldA=new World($('#world-a'),id=>choose(id,'a'));
    const fragment=location.hash.slice(1),initial=index.runs.some(r=>r.id===fragment)?fragment:'C1-1-00100-E';
    await load(initial);
  }catch(e){error(`3D playback is unavailable: ${e.message}`);}
})();
