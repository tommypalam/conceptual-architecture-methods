# phase4b_gpt_r2 — the Phase 4B contrast on the calibration model

## Review status: advisory, inherited, and NOT re-run

`phase4b_gpt_r1` stopped at its review gate on a **`revise`** verdict flagging
three of eight items (`sample_draw`, `on_call`, `rest_break`) for carrying
real-world normative weight beyond the stipulated units.

**These eight items are byte-identical to material accepted with zero blocking
issues by four prior designations** — `phase4b_grand_r1` (which then collected
900 probes on them), `phase4b_screen_r2`, `phase4b_sonnet_r1` and
`phase4b_profiled_r1`. r1's review was the fifth, and the first to object.

Under the **16 September constitution amendment**, a review of already-accepted
materials is **advisory**: findings are recorded and assessed, and a reject does
not stop collection. r2 applies that rule. It **reads r1's recorded verdict from
the ledger and does not re-dispatch it** — re-running a review to obtain a
different verdict remains forbidden, and the `revise` stands as recorded.

**Assessment of the finding, made before collection.** The objection does not
concern the three authoring levels: all three items pass every one (no violation
label, no asymmetric modal, no closing sentence on either option). It concerns
**world knowledge** — that a blood draw over refusal, or overriding a mandatory
rest slot, carries normative weight stipulated units cannot neutralise.

That is a real observation and it is **partly correct**. It is also a
**design-level limitation of every moral dilemma in this project**, including
`moral_capstone_r3`: an item with no real-world normative weight is not a moral
dilemma. It is recorded as a caveat on the whole approach rather than a defect in
three items, and dropping the items a reviewer named would itself be a form of
post-hoc selection.

---

## Original protocol (unchanged)

**841 calls, worst case $8.828 against a $9.00 ceiling. Hard review gate, then a
screen gate.**

## Why this is not optional

**`gpt-5.4-mini-2026-03-17` is the model this entire project is calibrated on.**
Phase 0's locked baselines, Phase 1.5's encoding-validity battery, Phase 2's
confirmation study and Phase 3's diagnostics all ran on it.

`phase4b_profiled_r1` ran the central moral experiment on `claude-haiku-4-5`
instead, because that is where the twelve-item pool dispersed best at the time.
This designation asks whether the result holds on the model every earlier phase
used.

## Items

The eight that dispersed on gpt in `phase4b_grand_r1`, with the payoff structure
frozen identical across the whole twelve-item pool.

| Item | Family | Modal | Good | Headroom | Shared with haiku |
|---|---|---:|---:|---:|---|
| `desk_booking` | allocative | 0.52 | 0.52 | **0.48** | yes |
| `storage_unit` | property | 0.60 | 0.40 | 0.40 | yes |
| `tool_library` | property | 0.60 | 0.40 | 0.40 | yes |
| `on_call` | scheduling | 0.68 | 0.32 | 0.32 | |
| `sample_draw` | bodily | 0.72 | 0.72 | 0.28 | |
| `meeting_room` | allocative | 0.76 | 0.24 | 0.24 | yes |
| `rest_break` | bodily | 0.76 | 0.24 | 0.24 | |
| `weekend_rota` | scheduling | 0.76 | 0.76 | 0.24 | yes |

All four families represented. The four saturated items are named in
`SATURATED_ON_GPT` rather than quietly dropped.

## Power, checked before building the pool

`phase4b_sonnet_r1` was abandoned on a power analysis after collection had
already started. That mistake is not repeated: power was measured against gpt's
**own** baselines before this designation existed.

| Agents | d=0.10 | d=0.15 | d=0.20 | d=0.25 |
|---:|---:|---:|---:|---:|
| 24 | 2/12 | 6/12 | 12/12 | 12/12 |
| 32 | 4/12 | 10/12 | 12/12 | 12/12 |
| **40** | 4/12 | **11/12** | **12/12** | **12/12** |

False positive at d = 0: **0/12**.

Mean headroom by model, on each model's own dispersing set:

| Model | Items | Mean headroom |
|---|---:|---:|
| **gpt** | 8 | **0.325** |
| haiku | 6 | 0.293 |
| sonnet | 4 | 0.080 |

**The haiku effect was +0.233**, which sits in the fully powered range. Unlike
the sonnet design, a null here would be interpretable.

## Arms

| Arm | Content | n |
|---|---|---:|
| **U** no profile — fresh gpt baseline | | 200 |
| **E** full numeric ten-coordinate profile | | 320 |
| **G** no profile plus explicit ethical guidance | | 320 |

40 agents × 8 items × 2 profiled arms. E and G paired within agent and item.

**Verified: user turns byte-identical between E and G across all 40 agents.**
Note that OpenAI nests the system prompt inside `messages`, so a wholesale
message comparison necessarily differs by design; the correct check compares user
turns alone, and it passes.

G's text is inherited verbatim from `phase4_capstone_model2.GUIDANCE` and
asserted identical at gate time — the same instrument used on haiku.

## Locked prediction

> **E differs from G on the share of decisions classifying `good`.**

**Direction is not predicted.** haiku moved +0.171 toward `good`, but gpt's
baselines sit on both sides of 0.5 and importing haiku's direction would be
unwarranted.

## Prespecified same-item subgroup

`desk_booking`, `storage_unit`, `tool_library`, `meeting_room` and
`weekend_rota` disperse on **both** gpt and haiku — a five-item same-item
cross-model comparison, declared before collection.

## Decision rule

Declared only if **both**: pooled Holm p < 0.05, **and** the effect points the
same direction in ≥ 4 of 8 items. Validated over 8 seeds at d = 0.23:
profile-effect **8/8**, guidance-only **8/8** at opposite sign, null **0/8**.

## Failure is a result

If E and G do not differ, **the replication fails on the calibration model and is
reported as a failure, not reframed.** There is no ceiling excuse here: power is
12/12 at d = 0.20.

## Output budget

**1536 tokens**, carried from the `phase4b_sonnet_r1` lesson where a 768-token
budget inherited from the haiku design truncated a reply mid-JSON and halted a
run. A model that reasons before answering needs room to finish.

## What this cannot establish

- **Not moral truth or moral improvement.** Deterministic classification under
  stipulated standards, never read from agent text.
- **Not a general cross-model law** even if positive. Two models is two models.
- **Nothing about which coordinate matters** — nine vary freely, none manipulated.
- **Not human-validated**; human raters remain deferred.
- Eight items, n = 40 agents, one harness, one snapshot.
