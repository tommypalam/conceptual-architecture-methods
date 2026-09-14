# Second-model capstone replication: protocol r3

**Revision of r2.** The blocker was never the model or the task: it was that the
shared response parser accepts only bare text under 1024 bytes or a strict
ratings schema, both of which encode one model's answering style.
`claude-haiku-4-5` answers correctly but reasons first, then emits the JSON.

**Output format is not part of the estimand.** The comparison is: same input,
same deterministic rule map, does the profile move the choice? How the answer is
packaged is measurement plumbing. Changing the *prompt* would confound the
comparison and remains refused; changing how a reply is *read* does not.

r3 introduces `phase4_crossmodel_dispatch`, which reuses the shared `Ledger`,
`write_once` and `charge` unchanged - exclusive lock, reservation identity,
write-once records, failure preservation, no retry, replay verification - and
replaces only the parse step with `extract_choice`.

`extract_choice` is **stricter** than what it replaces in the ways that matter:
it reads only a single unambiguous `{"choice": "..."}` object, never scans prose
for option names (a sampled reply named both options while choosing one),
rejects two or more objects even when they agree, rejects extra or duplicate
keys, and requires a declared action id. Truncated replies remain failures.

**Verified before use:** it reproduces all 956 valid `moral_capstone_r3`
decisions byte-identically, with zero differences and zero wrongly-rejected
responses. It changes nothing that already worked.

`max_tokens` is 768, set from the measured 424-token longest sampled reply.
Prompts remain identical to r3 across all four arms.

No frozen source was edited. Fresh seeds: 2026091620 / 2026091621 / 2026091622.

**Revision of r1**, which passed review and then stopped on its first
participant call. `max_tokens` was 64, inherited from a study whose model returns
bare JSON; `claude-haiku-4-5` writes its reasoning first and was truncated at
`stop_reason: max_tokens`. A real model difference, not a defect.

r2 raises `max_tokens` to 512 and changes **nothing else**. An earlier draft also
added a no-preamble instruction; it was reverted because it would have made the
prompt differ from `moral_capstone_r3`, and a cross-model comparison whose
prompts differ tests the prompt as much as the model. The prompts are verified
identical across all four arms. The larger output budget is the only difference
and is disclosed as a necessary accommodation.

Fresh seeds: 2026091613 / 2026091614 / 2026091615.

16 September 2026. Prospective. Phase 4B under implementation specification v0.2.

## 0. The question

Every profiled decision in Phase 4 has run on **one model**, `gpt-5.4-mini`. An
external review of this project identified single-model design as *"the common
ceiling"* on every thread, and the one investment that raises all of them.

This repeats [moral_capstone_r3](../moral_capstone_r3/ASSESSMENT.md) on
`claude-haiku-4-5-20251001`, a different provider, **changing nothing else**.

## 1. What is held fixed

| Item | Value |
|---|---|
| Tasks | 4, the eligible pool (`witness_cost`, `safety_hold`, `wage_disclosure`, `evidence_seal`) |
| Arms | E numeric, V matched prose, U none, G guidance only |
| Agents | 60 fresh, hash-locked |
| Decisions | 60 x 4 x 4 = **960** |
| Rule map | `conflict-rules-r1`, unchanged |
| Estimand | paired within-agent, permutation, Holm across tasks |
| Seeds | 2026091610 / 2026091611 / 2026091612 |

The only change is the participant model.

**A provider-shape defect was found and fixed before launch.** The inherited
request builder attached `response_format`, an OpenAI-only field, to every
request. Sent to an Anthropic model that is invalid. The field is now applied
only when the participant is an OpenAI model; the strict choice parser enforces
the JSON contract for both providers.

## 2. Prediction

If the capstone effect is a property of the encoding, `witness_cost` and
`safety_hold` should show positive E−U differences on this model too. The
r3 magnitudes were +0.350 and +0.367.

No specific magnitude is predicted. Models differ in baseline behaviour, and the
dispersion screen was run on gpt-5.4-mini, so these tasks may saturate or behave
differently here.

## 3. Interpretation, fixed in advance

**If both conflict tasks move positively**, the effect is not a property of one
model and the capstone claim generalises across providers.

**If neither moves**, the r3 result is bounded to `gpt-5.4-mini`. That does not
erase it — 956 decisions with Holm-corrected effects stand as recorded — but it
becomes a single-model finding and must be reported as one.

**If results are mixed**, the per-task pattern is reported without rounding
either way.

**A different baseline is not a failure.** If the unprofiled arm on this model
sits at a different rate, or if a task saturates here, that is reported as a
model difference rather than as evidence for or against the encoding.

**The sign of the result is not a success gate.**

## 4. What this cannot establish

- **Two models, two providers.** Not a survey, and both are mid-tier.
- **The tasks were screened on the other model.** Their dispersion on
  `claude-haiku-4-5` is unmeasured, so a saturated cell here is uninformative
  about profiles rather than evidence of no effect.
- **No moral truth.** Labels are deterministic classifications under stipulated
  standards, computed from stipulated transitions, never from agent text.
- **No human validation**; human raters remain deferred.
- 60 agents, one harness, one snapshot, individual decisions only.

## 5. Gates

Independent review of the task set and rule map, then collection. A non-accept
verdict stops this designation. No in-place retry; a revision is a new linked
designation.
