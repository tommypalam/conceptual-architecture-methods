# capstone_model2_r3: review stop, and a fourth review verdict on the same task set

**Outcome: review_stop. One paid call ($0.014298900), zero participant
decisions.** 16 September 2026.

The provider-agnostic dispatcher worked: the review reply was 1,732 bytes of
fenced JSON, exactly the format that blocked r1 and the sizing probe, and it was
read without incident. **The blocker that stopped the previous three attempts is
solved.** This designation stopped for a different reason.

| Item | Value |
|---|---|
| Verdict | **reject** |
| Participant decisions | 0 |
| Cost | $0.014298900 |
| Dispatcher | worked as designed; long fenced reply parsed cleanly |

Ledger: Claude $9.908908900/$32, OpenAI $4.251449400/$30, package
$37.066431325/$100. Usage estimates, not wallet balances.

## The three findings, assessed

**Finding 1 — not accepted; the reviewer misread its own supplied structure.**
It claims `wage_disclosure/state_parity` "upholds all four standards" and that
the structure is internally inconsistent. The supplied structure marks that
option `deception_avoidance: False` **and** `unfairness_avoidance: False`, which
is exactly what the reviewer argues it should be. The packet and the item text
agree; the reading does not.

**Finding 2 — a real question, already answered prospectively.** Is
"omits Dana's error while stating nothing false" deception? This is a genuine
philosophical disagreement, not a clerical error. The project answered it before
any collection: the finite-rule manual treats a knowingly incomplete mandatory
disclosure as deceptive, and that standard is declared in advance rather than
applied case by case. A reviewer may reasonably disagree with the stipulation.
It is not a defect in the item, and it applies identically to every arm, so it
cannot generate an arm difference.

**Finding 3 — describes the design, and is the closest to a hit.** The reviewer
observes that the stipulated totals point strongly toward one option in three
tasks, and that this "may guide respondents". That is the intended structure:
the conflict exists *because* the honest option carries the lower total. The
reviewer itself notes "dispersion shows real choice". Recorded as a stated limit
rather than a repair.

## The awkward fact this designation surfaces

**This task set has now been reviewed four times, with three different
verdicts.** `moral_capstone_r3` accepted it and collected 956 decisions.
`capstone_model2_r1` accepted it again. This review rejects it, partly on a
misreading and partly on a stipulation it is entitled to dispute.

That is worth reporting plainly: **an AI design review is not a stable
instrument.** The project has treated an accepted review as a gate, and three of
four passes on identical material would have opened that gate. This one closed
it. Reviews of this kind are useful for catching specific drafting errors — they
have caught several here, correctly — but their verdict is not a reliable
property of the material.

No verdict is overridden. The gate is respected: zero participant decisions were
collected under this designation.

## What remains blocked, and what does not

**Solved:** the response-format constraint. `phase4_crossmodel_dispatch` reuses
the shared `Ledger`, `write_once` and `charge` unchanged and replaces only the
parse step with `extract_choice`, which was verified to reproduce all 956 valid
`moral_capstone_r3` decisions with zero differences and zero wrongly-rejected
responses before use. It read this 1,732-byte fenced reply without trouble.

**Not solved:** the second-model replication. No profiled decision has been
collected on `claude-haiku-4-5`, so `moral_capstone_r3` remains a single-model
result and is reported as one.

A further attempt would face the same unstable gate on the same material. Any
continuation should decide first whether a single AI review verdict is the right
gate for a replication whose materials have already been reviewed and accepted
twice — that is a protocol question, not something to resolve by re-rolling.

## Provenance

One failed review call preserved at full reservation under the no-retry rule. No
frozen source was edited. The prompts remained identical to `moral_capstone_r3`
across all four arms; only the output budget and the response reader differ, both
disclosed.
