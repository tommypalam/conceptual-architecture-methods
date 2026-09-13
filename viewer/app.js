"use strict";
const $ = (selector) => document.querySelector(selector);
const names = {C1:"Resource council", C2:"Restructuring board", C3:"Scientific approach"};
const rules = {
  C1:"Five voting members choose Package A or B. Each round is binding. Unanimity ends the discussion early; otherwise round 5's majority decides.",
  C2:"Five board members vote; the CEO participates but their vote is excluded. Only the CEO can adopt previously registered amendments in rounds 2–4. The board's round 5 vote is binding. A proposal is not an adopted safeguard.",
  C3:"Four founders receive private evidence over time. Authenticated disclosures become public for the next round. Round 6 is binding; a 2–2 tie uses the recorded seeded random tie-break. Evidence provenance does not guarantee a faithful interpretation."
};
const labels = {PACKAGE_A:"Package A",PACKAGE_B:"Package B",APPROVE:"Approve",REJECT:"Reject",CONTINUE:"Continue",PIVOT:"Pivot"};
const endpoints = {LL:["External warrant","Internal endorsement"],CS:["Low sensitivity","High sensitivity"],RT:["Tolerant","Hair-trigger"],MoR:["Reflective","Confrontational"],RE:["Abstract-person","Role-sensitive"],PD:["Outcome-dominant","Process-dominant"],TfA:["Egalitarian","Hierarchical"],ID:["Surface compliance","Genuine endorsement"],MS:["Local / role-bound","Broad moral scope"],AW:["Deliberative","Affective"]};
let index, run, round = 0, selected, activeTab = "profile", timer = null, loadVersion = 0;
const cache = new Map();
const esc = (value) => String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const label = value => labels[value] || "Invalid vote";
const current = () => round ? run.rounds[round - 1] : null;
const choiceClass = vote => vote === run.labels[0] ? "a" : vote === run.labels[1] ? "b" : "missing";
const armName = arm => ({E:"Encoded profile",U:"Context only",B:"Neutral · no profile"}[arm]);
async function fetchJSON(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Cannot load this recording (${response.status}). Check the local server and raw data; no replacement data will be generated.`);
  return response.json();
}
async function getRun(id) {
  if (!cache.has(id)) cache.set(id, await fetchJSON(`/api/run/${encodeURIComponent(id)}`));
  return cache.get(id);
}
function stop() { clearInterval(timer); timer = null; $("#play").textContent = "▶ Play"; }
function play() {
  if (!run) return;
  if (timer) { stop(); return; }
  if (round === run.rounds.length) round = 0;
  round++; render();
  if (round === run.rounds.length) return;
  $("#play").textContent = "Ⅱ Pause";
  timer = setInterval(() => { round++; render(); if (round >= run.rounds.length) stop(); }, Number($("#speed").value));
}
function step(value) { if (!run) return; stop(); round = Math.max(0, Math.min(run.rounds.length, value)); render(); }
async function load(id, preserveRound = false) {
  stop(); const version = ++loadVersion; const priorRound = round;
  document.body.classList.add("loading"); $("#error").hidden = true;
  try {
    const nextRun = await getRun(id);
    if (version !== loadVersion) return;
    run = nextRun; round = preserveRound ? Math.min(priorRound, run.rounds.length) : 0;
    if (!run.agents.some(a => a.agent_id === selected)) selected = run.agents[0].agent_id;
    $("#problem").value = run.problem; $("#group").value = run.group;
    $("#condition").value = `${run.config}-${run.arm}`;
    $("#comparison-body").replaceChildren(); $("#compare").disabled = false;
    $("#compare").textContent = "Load five recorded outcomes";
    history.replaceState(null, "", `#${id}`);
    $("#scene-title").textContent = names[run.problem];
    $("#scene-kicker").textContent = `${run.problem} / GROUP ${String(run.group).padStart(2,"0")} / ${armName(run.arm).toUpperCase()}`;
    $("#brief-title").textContent = names[run.problem]; $("#brief-text").textContent = run.scenario; $("#brief-rules").textContent = rules[run.problem];
    $("#context").innerHTML = ["Freedom","Justice","Authority","Care","Loyalty"].map((name,i) => `<span class="axis ${run.config[i] === "1" ? "high" : ""}">${name}<b>${run.config === "neutral" ? "·" : run.config[i] === "1" ? "↑" : "↓"}</b></span>`).join("");
    $("#provenance").textContent = `300 recorded runs · request & state checks passed for this replay. Seed ${index.seed}.`;
    $("#scrub").max = run.rounds.length;
    render();
  } catch (error) { if (version === loadVersion) showError(error); }
  finally { if (version === loadVersion) document.body.classList.remove("loading"); }
}
function showError(error) { $("#error").hidden = false; $("#error").textContent = error.message; }
function render() {
  const state = current(); const end = round === run.rounds.length;
  $("#scrub").value = round; $("#position").textContent = `${round} / ${run.rounds.length}`;
  $("#previous").disabled = round === 0; $("#next").disabled = end;
  $("#round-caption").textContent = round ? `ROUND ${round} · ${end ? "FINAL" : "DELIBERATION"}` : "BEFORE ROUND 1";
  $("#table-result").textContent = end ? label(run.result.outcome) : round ? "In discussion" : "Take your seat";
  $("#tally").innerHTML = state ? run.labels.map((v,i) => `<span class="choice-${i ? "b" : "a"}"><strong>${state.tally[v]}</strong>${esc(label(v))}</span>`).join("") + (state.tally.missing ? `<br>${state.tally.missing} invalid vote` : "") : "Press play to reveal the first round.";
  let note = "Each step reveals one complete round. Agents only saw earlier rounds.";
  if (round) note = run.problem === "C2" ? "CEO lean is shown but excluded from the tally. Only the five board members cast binding votes in round 5." : run.problem === "C3" ? "Votes before round 6 are provisional. New public disclosures become available to agents next round." : "Each round is binding. Unanimity ends the council; otherwise the fifth round’s majority decides.";
  if (end) note += run.result.consensus ? " This council ended in unanimous agreement." : run.result.tie_break ? " Final result uses the recorded random tie-break." : " The recorded conversation is complete.";
  $("#round-note").textContent = note;
  const n = run.agents.length;
  const positions = n === 4 ? [[50,17],[83,50],[50,83],[17,50]] : n === 5 ? [[50,17],[82,40],[72,81],[28,81],[18,40]] : [[30,18],[70,18],[85,50],[70,81],[30,81],[15,50]];
  $("#seats").innerHTML = run.agents.map((agent,i) => {
    const r = state?.responses.find(x => x.agent === agent.agent_id);
    const ceo = agent.agent_id === run.ceo;
    return `<button class="seat ${r ? choiceClass(r.vote) : ""} ${selected === agent.agent_id ? "selected" : ""} ${r?.changed ? "changed" : ""}" style="left:${positions[i][0]}%;top:${positions[i][1]}%" data-agent="${agent.agent_id}" aria-label="Inspect agent ${agent.agent_id}${ceo ? ", CEO" : ""}" aria-pressed="${selected === agent.agent_id}"><span class="avatar">${String(agent.agent_id).padStart(3,"0")}</span><span class="name">Agent ${agent.agent_id}${ceo ? " · CEO" : ""}</span><span class="vote">${r ? `${r.changed ? "↻ " : ""}${label(r.vote)}${ceo ? " (lean)" : ""}` : "Awaiting round"}</span></button>`;
  }).join("");
  $("#discussion-title").textContent = round ? `What they said · round ${round}` : "Around the table";
  const changed = state?.responses.filter(r => r.changed).length || 0;
  $("#change-count").textContent = state ? `${changed} adjacent-round vote ${changed === 1 ? "change" : "changes"}` : "Select an agent to inspect";
  $("#discussion").innerHTML = !state ? `<div class="empty">${run.agents.length} agents. ${run.rounds.length} recorded ${run.rounds.length === 1 ? "round" : "rounds"}. One shared decision.<br>Press play, or use the arrow controls to move at your own pace.</div>` : state.responses.map(r => `<button class="statement ${selected === r.agent ? "selected" : ""}" data-agent="${r.agent}" data-open-response="true"><div class="statement-head"><span>Agent ${r.agent}${r.agent === run.ceo ? " · CEO" : ""}</span><span class="vote-label ${choiceClass(r.vote)}">${esc(label(r.vote))}</span></div><p>${esc(r.fields.REASONING || r.text)}</p><div class="event">${r.changed ? `↻ ${esc(label(r.previous_vote))} → ${esc(label(r.vote))} · ` : ""}${r.agent === run.ceo ? "Non-voting role · " : ""}Read full response ↗</div></button>`).join("");
  renderShared(); renderInspector();
}
function evidenceList(ids) {
  return ids.length ? ids.map(id => `<div class="item"><b>${esc(id)}</b><p>${esc(run.evidence.find(e => e.item_id === id)?.content || "No supplied item with this ID.")}</p></div>`).join("") : `<p class="fine">None at this point.</p>`;
}
function renderShared() {
  const state = current();
  $("#shared").hidden = run.problem === "C1";
  if (run.problem === "C3") {
    const before = state?.public_before || [], after = state?.public_after || [];
    const added = after.filter(id => !before.includes(id));
    $("#shared-count").textContent = `${before.length} available at round start · ${added.length} newly disclosed`;
    $("#shared-body").innerHTML = `<h4>Public at the start of this round</h4>${evidenceList(before)}<h4>Newly disclosed in this round</h4><p class="fine">Available from the next round, if one follows. These are authenticated IDs, not a semantic accuracy rating.</p>${evidenceList(added)}`;
  } else if (run.problem === "C2") {
    const proposals = state?.proposals_after || {}, adopted = state?.adopted_after || [];
    $("#shared-count").textContent = `${Object.keys(proposals).length} registered · ${adopted.length} adopted by round end`;
    $("#shared-body").innerHTML = `<p class="fine">The working plan at round start had ${(state?.adopted_before || []).length} adopted amendments. New adoptions become visible next round. Suggestions outside a valid amendment action do not register.</p>` + (Object.keys(proposals).length ? Object.entries(proposals).map(([id,text]) => `<div class="item"><b>${esc(id)} · ${adopted.includes(id) ? "ADOPTED" : "PROPOSED ONLY"}${adopted.includes(id) && !state.adopted_before.includes(id) ? " THIS ROUND" : ""}</b><p>${esc(text)}</p></div>`).join("") : `<p class="fine">No registered amendments yet.</p>`);
  }
}
function renderInspector() {
  const agent = run.agents.find(a => a.agent_id === selected), r = current()?.responses.find(x => x.agent === selected);
  $("#agent-heading").innerHTML = `<h2>Agent ${selected}</h2><div class="role">${selected === run.ceo ? "CEO · non-voting participant" : run.problem === "C3" ? "Founder · voting participant" : "Member · voting participant"}</div>`;
  document.querySelectorAll("[data-tab]").forEach(b => b.setAttribute("aria-selected", b.dataset.tab === activeTab));
  let html = "";
  if (activeTab === "profile") {
    html = `<div class="profile-note ${run.arm !== "E" ? "absent" : ""}">${run.arm === "E" ? "This fixed LPM profile was supplied before every response. Values stay unchanged across rounds." : "This is the matched profile only. These values were NOT supplied to the agent in this condition."}</div>`;
    html += index.parameters.map(p => `<div class="parameter" title="${esc(`0: ${p.endpoint_0}\n1: ${p.endpoint_1}`)}"><div class="parameter-top"><span><b>${esc(p.name)}</b>${esc(p.label)}</span><span>${agent.parameters[p.name].toFixed(4)}</span></div><div class="bar"><i style="width:${agent.parameters[p.name]*100}%"></i></div><div class="parameter-ends"><span>${esc(endpoints[p.name]?.[0] || p.endpoint_0)}</span><span>${esc(endpoints[p.name]?.[1] || p.endpoint_1)}</span></div></div>`).join("");
  } else if (activeTab === "response") {
    html = r ? `<span class="vote-label ${choiceClass(r.vote)}">${esc(label(r.vote))}</span><p class="fine">Round ${round} · ${esc(r.status)}${r.changed ? ` · changed from ${esc(label(r.previous_vote))}` : ""}</p><div class="prewrap response-text">${esc(r.text)}</div><details class="raw-prompt"><summary>Exact incoming prompt</summary><p class="fine">What this agent actually received. Peer reasoning was shown as structured excerpts; the full responses above are for your inspection.</p>${r.messages.map(m => `<h4>${esc(m.role)}</h4><pre>${esc(m.content)}</pre>`).join("")}</details><details class="raw-prompt"><summary>Source & parser details</summary><p class="fine record-path">${esc(r.record)}<br>SHA-256: ${esc(r.record_hash)}</p><pre>${esc(JSON.stringify(r.field_errors,null,2))}</pre></details>` : `<p class="fine">Advance to a round to read the agent’s complete recorded response and the exact prompt it received.</p>`;
  } else {
    if (!r) html = `<p class="fine">Advance to a round to inspect the information available to this agent.</p>`;
    else if (run.problem === "C3") html = `<div class="profile-note">Available when this response was generated. Same-round disclosures from other agents were not yet visible.</div><span class="knowledge-count">${r.held.length}</span><h3>Directly held evidence</h3>${evidenceList(r.held)}<span class="knowledge-count">${current().public_before.length}</span><h3>Public evidence at round start</h3>${evidenceList(current().public_before)}`;
    else if (run.problem === "C2") html = `<div class="profile-note">The original dilemma, earlier-round transcript and the authoritative plan at round start were supplied.</div><h3>Adopted before this round</h3>${current().adopted_before.length ? current().adopted_before.map(id => `<div class="item"><b>${esc(id)}</b><p>${esc(current().proposals_before[id])}</p></div>`).join("") : '<p class="fine">None. The working plan was the original proposal.</p>'}<p class="fine">See Response → Exact incoming prompt for all proposals and the transcript this agent saw.</p>`;
    else html = `<p class="fine">This member saw the locked resource dilemma and the structured transcript of ${round - 1} earlier ${round === 2 ? "round" : "rounds"}. There are no separate private evidence packets in this task.</p><p class="fine">See Response → Exact incoming prompt to inspect the full input.</p>`;
  }
  $("#inspector-body").innerHTML = html;
}
async function compare() {
  if (!run) return;
  const version = loadVersion, base = `${run.problem}-${run.group}`;
  $("#compare").disabled = true; $("#compare").textContent = "Checking recorded outcomes…";
  try {
    const rows = await Promise.all(["00100-E","00100-U","11011-E","11011-U","neutral-B"].map(c => getRun(`${base}-${c}`)));
    if (version !== loadVersion) return;
    $("#comparison-body").innerHTML = `<table><thead><tr><th>Condition</th><th>Final choice</th><th>Votes</th><th>Rounds</th></tr></thead><tbody>${rows.map(r => `<tr><td><button data-run="${r.id}">${esc(armName(r.arm))}<br>${r.config}</button></td><td>${esc(label(r.result.outcome))}</td><td>${r.labels.map(l => r.result.final_tally[l]).join(" / ")}</td><td>${r.rounds.length}</td></tr>`).join("")}</tbody></table><p class="fine">Vote columns follow the two choices in the scenario. These five examples do not replace the study’s paired statistical analysis.</p>`;
    $("#compare").textContent = "Five outcomes verified";
  } catch(error) { if (version === loadVersion) { showError(error); $("#compare").disabled = false; } }
}
$("#group").innerHTML = Array.from({length:20},(_,i) => `<option value="${i+1}">Group ${String(i+1).padStart(2,"0")}</option>`).join("");
for (const id of ["problem","group","condition"]) $(`#${id}`).addEventListener("change", () => load(`${$("#problem").value}-${$("#group").value}-${$("#condition").value}`, id === "condition"));
document.addEventListener("click", event => {
  const agent = event.target.closest("[data-agent]"), tour = event.target.closest("[data-run]"), tab = event.target.closest("[data-tab]");
  if (agent && run) {
    selected = Number(agent.dataset.agent);
    if (agent.dataset.openResponse) activeTab = "response";
    render();
    if (innerWidth <= 1150) $(".inspector").scrollIntoView({behavior:"instant", block:"start"});
  }
  if (tour) load(tour.dataset.run);
  if (tab && run) { activeTab = tab.dataset.tab; renderInspector(); }
});
$("#play").addEventListener("click", play);
$("#previous").addEventListener("click", () => step(round-1));
$("#next").addEventListener("click", () => step(round+1));
$("#scrub").addEventListener("input", event => step(Number(event.target.value)));
$("#speed").addEventListener("change", () => { if (timer) stop(); });
$("#compare").addEventListener("click", compare);
$("#brief-button").addEventListener("click", () => { if (run) { stop(); $("#brief").showModal(); } });
$("#close-brief").addEventListener("click", () => $("#brief").close());
document.addEventListener("keydown", event => {
  if (!run || $("#brief").open || event.target.closest("input,select,button,summary,a,textarea")) return;
  if (event.code === "Space") { event.preventDefault(); play(); }
  if (event.code === "ArrowRight") { event.preventDefault(); step(round+1); }
  if (event.code === "ArrowLeft") { event.preventDefault(); step(round-1); }
});
document.addEventListener("visibilitychange", () => { if (document.hidden) stop(); });
(async () => {
  try { index = await fetchJSON("/api/index"); const id = location.hash.slice(1); await load(index.runs.some(r => r.id === id) ? id : "C1-1-00100-E"); }
  catch(error) { showError(error); }
})();
