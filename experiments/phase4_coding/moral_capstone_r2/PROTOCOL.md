# Phase 4 moral capstone: protocol r2

15 September 2026. Prospective replication and extension of
[r1](../moral_capstone_r1/ASSESSMENT.md). Phase 4B under implementation
specification v0.2.

## 0. Why r2

An external review identified the binding limitation on r1: it rested on **two
tasks, one of which showed no effect**, and would need "more tasks (ideally 4-6,
with some designed as negative controls)" before supporting a general claim.

r2 runs **four tasks spanning two independently screened sets**, each having
cleared the same two prespecified gates.

| Task | Set | Dispersion | Standards in tension |
|---|---|---:|---|
| `witness_cost` | A | 0.76 | deception, harm |
| `safety_hold` | A | 0.72 | deception, harm |
| `wage_disclosure` | B | 0.96 | deception, harm, unfairness |
| `evidence_seal` | B | 0.92 | coercion, deception, harm |

Set A's conflicts were concentrated on deception-vs-harm. Set B adds unfairness
and coercion, so a combined result does not rest on one kind of dilemma.

**Negative controls exist and behaved as designed.** Three control tasks with a
dominant option were screened in
[set B](../moral_conflict_screen_b2/ASSESSMENT.md) and all returned modal share
1.00. They are not in this study because a saturated task cannot discriminate;
their value is showing that the screen distinguishes constructed conflicts from
constructed non-conflicts.

**r1's result is not assumed.** `witness_cost` and `safety_hold` are re-run with
fresh agents and fresh seeds, so r2 is a replication for those two and a first
test for the other two.

## 0.1 Excluded despite dispersing

`quota_shortfall` (set A, 0.96) and `quarantine_notice` (set B, **0.52**, the
most contested task in the project) are excluded because their net-score primary
is constant across options: the outcome cannot move whatever agents choose. The
gate was written before collection and is applied as written rather than relaxed
to gain tasks.

## 1. Design

| Item | Value |
|---|---|
| Tasks | 4 (both gates passed) |
| Arms | E numeric profile, V matched prose, U no profile, G guidance only |
| Agents | 60 fresh, hash-locked |
| Decisions | 60 x 4 x 4 = **960** |
| Seeds | 2026091550 / 2026091551 / 2026091552 |

Pool content hash `cad0d2897aaa02a69f50f5ad19e2f353d3119a2ca60ee2d0264d4c5f5ccf15ab`.

`verify_pool()` re-checks before any batch is built that every pooled task is a
genuine conflict, has a discriminating net primary, and did not saturate.

## 2. Moral measurement, frozen before collection

Deterministic classification by `code/phase4_conflict_rules.py`, version
`conflict-rules-r1`. The same action always receives the same labels regardless
of arm, agent reasoning, or how persuasive its justification is. **No AI or human
rater assigns a moral label.** These are classifications under stipulated
standards, not moral truth.

**Primary outcome: the net-score headline.** Prespecified here, before any
profiled collection, because the strict-OR relative headline returns `not_good`
for eleven of twelve pairs on a conflicting task set and cannot discriminate.
Thesis v0.6 specifies net-score and 1.5-weighted aggregations for exactly this
case. Strict-OR, weighted and fixed-standard headlines are all reported
alongside; none substitutes for the primary.

Because no option upholds all four fixed standards, **every action is
fixed-standard `not_good` on at least one category by construction.** The study
measures which standard an agent privileges when it cannot satisfy all of them.

## 3. Design

| Item | Value |
|---|---|
| Tasks | 2 (`safety_hold`, `witness_cost`) |
| Arms | E numeric profile, V information-matched prose, U no profile, G no profile + ethical guidance |
| Agents | 60 fresh profiles, hash-locked |
| Decisions | 60 x 2 x 4 = **480** |
| Seeds | 2026091530 / 2026091531 / 2026091532 |

Each agent answers each task in each arm. Option order alternates
deterministically on agent and task, and is reconstructed from the frozen
requests during analysis to check that order does not drive the outcome, as in
the screen.

## 4. Estimands, fixed in advance

**Primary:** the proportion of decisions whose net-score headline is `good`,
per arm per task, and the E-U difference.

**Secondary, prespecified:** V-U and G-U differences; the same contrasts under
the weighted and strict-OR headlines; per-standard violation rates showing which
standard each arm privileges; and the fixed-standard headline distribution.

Inference is a paired permutation test within agent, 10,000 resamples, with Holm
correction across the primary contrasts. Every arm and task is reported whether
or not it moves.

## 5. Failure conditions, prespecified

1. **No arm difference.** Profiles do not change which standard is privileged on
   conflicting tasks.
2. **Difference in the harmful direction.** Profiled agents privilege standards
   in a way that lowers the net-score good rate.
3. **Collection saturates anyway.** Dispersion measured unprofiled does not
   persist under profiles.

Each is an informative, publishable outcome. **The sign of the result is not a
success gate**, and no result licenses a claim that encoded agents are morally
better.

## 6. What this cannot establish

- **No moral truth.** Labels are classifications under stipulated standards
  chosen by this project, not a neutral definition of goodness.
- **No human validation.** Human raters remain deferred by explicit instruction.
  No AI judgement substitutes for one; the classification here is deterministic
  and involves no rater at all.
- **No ethical understanding, human resemblance, or moral superiority.**
- **Two tasks, stylised, 60 agents, one model, one harness, one snapshot.** The
  narrow task base is a stated limit, not a repaired one.
- **No group or institutional evaluation.** Individual decisions only; the
  societal-axis confound is untouched.
- A persuasive justification is never scored as a realised benefit: labels come
  from the stipulated transition, not from agent text.

## 7. Gates before any paid call

1. Researcher authorisation.
2. Independent review of the rule map and task set, with the dispersion evidence
   supplied. A non-accept verdict stops this designation.
3. Offline checks passing, including clean-option verification, primary
   discrimination, and mocked collection.
4. Frozen manifest and exact cost bound.

A failed gate stops the designation. No in-place retry; a revision is a new
linked designation.
