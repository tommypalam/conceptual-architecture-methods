# The second item family — scope and plan

**Status: proposal. Nothing authored, nothing frozen, no API call.**
This is blocker 2 of [PROJECT_SPLIT.md](../../docs/PROJECT_SPLIT.md): the
limitation a reviewer will name, and the one addition that changes the paper's
ceiling from workshop to main conference.

## What the objection actually is

Not "seven items". The seven vary across four families — property, bodily,
scheduling, allocative — and that variation is already reported. The objection is
that the **situation type never varies**. Every item is:

> a workplace resource, one party holds it and has said they want to keep it,
> two payoff vectors frozen at `[1, -4]` against `[2, -5]`, totals tied at −3.

A reviewer writes: *the effect may be a property of this scenario schema.* Nothing
in the existing data answers that, and §6.3's invented fields — Status-quo
Preference, Stated-Wish Deference — are named after features of **this schema**,
which sharpens rather than blunts the objection.

## What must be held, and what must change

**Held, or the measurement breaks:**

- Totals tied (−3 both options), so welfare-maximising, minimax and best-case
  reasoning are indifferent by construction. This is what makes the parameter,
  not the arithmetic, the operative variable.
- One clean option and one single-violation option, flags declared in source.
- The three-level authoring criterion (`verify_items`): matched non-unit
  consequence text, no asymmetric violation label, no asymmetric obligatory or
  transgressive modals.
- Deterministic classification from the action identifier. No moral label is ever
  read from model text.

**Changed, or the family is not a second family:**

- **The holder relationship.** Currently a party *already holds* the resource in
  every item. The second family should include cases with no incumbent — a
  prospective allocation among parties with equal standing.
- **The setting.** Out of the workplace. Candidates: civic (a permit, a queue for
  a service), domestic (a shared household resource), or informational (who is
  told what, when).
- **What the stated expectation is.** Currently always a *stated wish to keep*.
  The second family should carry expectations of other kinds — a promise made, a
  turn taken, a published criterion.

## Why this is expensive and has failed before

Seventeen wordings died at the dispersion screen across
[defeasibility_screen_r1](defeasibility_screen_r1/ASSESSMENT.md) and
[r2](defeasibility_screen_r2/ASSESSMENT.md), and five designs died at the same
gate in earlier phases. The failure mode is consistent: **items that read as
clearly resolvable to a human saturate on the model**, and the direction of
saturation is not predictable from the wording. The two screens also produced a
finding that bears directly here — an unprofiled floor is *not* a floor under
profile, so a screen's baseline does not bound the profiled range and screening
may reject items that would have worked.

Realistic expectation: **author 12–16 candidates to obtain 6–7 usable ones.**

## Sequence and cost

| Step | What | Calls | Cost | Gate |
|---|---|---:|---:|---|
| 1 | Author 14 candidates against `verify_items` | 0 | $0 | mechanical criterion must pass |
| 2 | Independent review, new material | 1 | ~$0.03 | **hard gate**: anything but accept stops |
| 3 | Dispersion screen, 24 per item, both orders | 336 | ~$0.15 | ≥6 items usable: pooled share in [0.10, 0.90] **and** order gap ≤ 0.20 |
| 4 | PD pinned 0.10/0.90 on the survivors, 40 agents | ~560 | ~$0.42 | replication: does the §6.1 effect appear on a different schema? |
| 5 | Gloss reversal (FLIP) on the same items | ~560 | ~$0.42 | the actual test: does reversal reverse it here too? |

**Total: about 1,460 calls and $1.02** against $17.36 of OpenAI headroom. The cost
is not money. It is that steps 1–3 have a substantial chance of ending the
attempt, and that is the honest reason this has not been done already.

## What each outcome buys

- **The effect replicates and FLIP reverses on a second schema.** The
  generalisation objection is answered directly, and the paper's central claim
  becomes schema-independent within the tested range. This is the outcome worth
  $1.
- **The effect replicates but FLIP does not reverse.** The strongest possible
  qualification: meaning-tracking is schema-dependent, which is a genuine finding
  and a much more interesting limitation than "one item family".
- **The effect does not replicate.** The §5 and §6 results are bounded to the
  workplace-resource schema. That is a real result, it must be reported as such,
  and it is exactly what the paper's method is built to be able to return.
- **The screen stops it.** The seventh consecutive failure at this gate. Reported
  as the boundary of what this harness can measure, and the paper keeps its
  current limitation honestly stated.

## What this does not become

Not a new phase and not a new framework claim. It is one designation chain
testing whether an established result survives a change of situation type. **No
new parameter, no new coordinate, no revision to the ten.** If it succeeds it
strengthens §6; if it fails it sharpens §9.

## Decision needed before step 1

The authoring criterion forbids inventing parameter-to-behaviour mappings without
review, and new items are new material requiring an accepted review gate. What is
**not** yet decided, and needs the researcher:

1. **Which setting** — civic, domestic or informational. One, not three: a second
   family with three settings inside it reproduces the original problem at
   smaller scale.
2. **Whether to keep the tied-payoff structure.** Holding it keeps comparability
   with §5–§6 and keeps the arithmetic non-operative. Relaxing it would test
   something else and is a different project.

Recommendation: **civic, tied payoffs held.** Civic settings supply
non-incumbent allocations and published criteria naturally, which changes the
holder relationship and the expectation type together, while the frozen payoff
pair keeps every existing control intact.
