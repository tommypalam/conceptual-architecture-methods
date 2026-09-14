# Second-model capstone replication: protocol r1

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
