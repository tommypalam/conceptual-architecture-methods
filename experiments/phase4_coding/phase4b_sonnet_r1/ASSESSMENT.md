# phase4b_sonnet_r1: halted at 240/421, and the power analysis says do not rerun

**Outcome: halted mid-collection. 240 of 421 calls, one preserved failure, zero
completed profiled analysis.** 16 September 2026. Review **accept**, zero
blocking issues; screen gate passed on all four items.

Ledger after this designation: Claude $19.642945/$32, OpenAI $4.566823/$30.
This designation charged $2.156873400 across 240 calls. Usage estimates, not
wallet balances.

## What happened

1. **Review accepted**, zero blocking issues — the seventh consecutive clean
   hard gate.
2. **Screen gate passed**: all four items usable on fresh probes
   (0.96/0.80/0.92/0.04 against the `grand_r1` screen's 0.88/0.92/0.92/0.04).
3. **The process was killed** when the previous session ended, at 124/421. The
   exclusive lock was left stale, holding PID 5152 and this designation's release
   hash. The PID was verified dead and the last record was ~11 hours old before
   the lock was cleared; a copy is preserved as `stale_lock_removed.json`.
4. **Resumed cleanly** — the write-once ledger replayed the 124 completed calls
   without re-charging — and then **halted at 240** when one reply was truncated
   mid-JSON.

## The truncation

`phase4b_sonnet_r1/profiled/E/17/ward_transfer`, `stop_reason: max_tokens`, 768
output tokens, cut at `{"`:

> "…Given equal aggregates, I'll side with reducing the concentrated asymmetry —
> two people suffering in a corridor feels less acceptable than one person losing
> room preference.\n\n`{"`

**The guard is correct.** The answer genuinely does not exist in that reply, and
a truncated response is not trusted even if a choice object appears before the
cut. Preserved at full reservation ($0.027423000), not retried.

Measured across r1's 239 sonnet replies: **median 427 output tokens, p90 578,
max 768, and 1.7% over 700.** The 768 budget was inherited from the haiku design
and is simply too tight for sonnet's longer reasoning.

## Why there is no r2

A rerun was prepared at a 1536-token budget — double the observed maximum, chosen
on measurement rather than guesswork. It was **not run**, because a power
analysis performed before spending showed the design cannot do its job.

**Power to declare an effect under the prespecified rule, 10 seeds, effect
applied against each item's measured baseline:**

| Agents | d = 0.15 | d = 0.25 | d = 0.35 |
|---:|---:|---:|---:|
| 36 | 2/10 | 3/10 | 5/10 |
| 40 | 2/10 | 3/10 | 5/10 |
| 48 | 2/10 | 4/10 | 5/10 |
| 56 | 2/10 | 4/10 | 4/10 |

**More agents do not help.** The binding constraint is headroom, not sample size.

| Model | Mean headroom (min of good-rate, 1 − good-rate) |
|---|---:|
| haiku, six profiled items | **0.293** |
| sonnet, four profiled items | **0.080** |

Haiku's items sat near 0.5, where a shift in either direction is visible.
Sonnet's sit at 0.88–0.96 and 0.04, where only one direction has room and that
room is 0.04–0.12.

**An earlier power check reported 8/8 and was misleading.** It applied a fixed
effect probability uniformly rather than against each item's measured baseline,
which manufactured headroom the items do not have. The corrected simulation is
the one above.

## My error, stated plainly

I flagged the ceiling as a caveat in the protocol and then recommended running
anyway. The caveat was correct and I under-weighted it. Spending $12.93 on a
design with 50% power at a generous effect size, and then reporting whatever came
out, would have produced an uninterpretable result — a null that means nothing
and a positive that could not be trusted.

The protocol's own words were: *"a null is therefore weaker evidence than a null
on haiku's near-even cells would have been."* The power analysis quantifies that
as: the test is a coin flip.

## What this establishes

**A measured constraint on cross-model replication in this design.** The Phase 4B
effect cannot be tested on `claude-sonnet-4-6` with these items, because sonnet's
baselines on every item that disperses at all sit within 0.12 of a bound. This is
a property of the model's measured behaviour, not a budget or engineering limit.

**A measured output-budget constraint.** 768 tokens, calibrated on haiku,
truncates roughly 0.4% of sonnet replies and 1.7% run within 70 tokens of the
limit. Any future sonnet designation needs at least 1536.

**The screen protocol worked again.** The four items were selected on sonnet's own
dispersion rather than haiku's, which is what prevented a repeat of
`capstone_model2_r4`. The saturated eight were excluded by measurement.

## What this does NOT establish

- **Nothing about whether the Phase 4B effect transfers.** No completed profiled
  contrast. The locked prediction is **untested**, not failed — the same status
  as the two PD designations, and it must not later be presented as either.
- **Not evidence that the effect is haiku-specific.** It is evidence that this
  item set cannot ask the question on sonnet.
- **Not a claim that sonnet is insensitive to profiles.** Untested.

## What a working cross-model test would need

Items screened to sit **near 0.5 on the second model**, not merely below 1.00.
`phase4b_grand_r1` screened twelve items on sonnet and the best available was
0.88; none approached an even split. Reaching one would mean building and
screening a new pool against sonnet's baselines specifically — a new designation,
with no guarantee that such items exist for that model.

That is the honest next step, and nothing here authorises it.

## Provenance

Review returned **accept**, zero blocking issues, two non-blocking limits, both
recorded. 240 calls dispatched, 239 valid, one preserved failure. The stale lock
was cleared only after verifying PID 5152 was dead and that the lock's release
hash matched this designation; the original is preserved alongside this
assessment.

`phase4b_screen_r2`'s earlier lost probe remains inherited, preserved and
unrecovered. No frozen source was edited.
