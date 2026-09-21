# precipitation_r1 — assessment

**HALTED by a network failure at call 294 of 840. No result.**
293 valid, one failed, $0.153410 charged. `gpt-5.4-mini-2026-03-17`,
22 September 2026. Protocol: [PROTOCOL.md](PROTOCOL.md). Design hash
`b75a407e4c0aa0575fe30aa00a158eee55c85a8921cdad8aa76bbacbf6146e11`.

The failed slot is `precipitation_r1/profiled/RULE/1/weekend_rota`, a
`TimeoutError` with no HTTP status — a transport failure, not a refusal or a
malformed request.

## This designation is closed and is not re-run

The project's rule is that a failed call is **preserved at full reservation and
never retried in place**, and that a halted designation is not resumed. The rule
exists so that a run cannot be quietly repeated until it yields a clean sweep,
and it applies here exactly as it applied to `coordinate_sweep_r1`, which halted
at 689 of 2,801 on the same error and whose 689 calls were never reused.

**The 293 collected decisions are not analysed.** They cover the INSTANCES arm
and part of RULE, with NEITHER untouched, so no contrast in the protocol can be
formed from them: every primary quantity is a within-unit difference requiring
all three arms on the same agent-item. Partial data with one arm missing would
invite exactly the post-hoc selection the design was built to avoid. They remain
in the ledger as settled records and are excluded from every analysis.

## What this costs, and what it does not

**The question is untouched.** Whether a boundary precipitates from instances is
neither answered nor bounded. The design is not implicated: it was refused three
times before collection on defects I introduced, and every one of those was
repaired and verified before this run began. This halt is a network event.

**The materials are undamaged and re-usable.** Exemplars are frozen
`pd_prospective_r1` records; the items are the reviewed twins. A successor
designation — new designation, new release, new seed — may use them. That is a
fresh designation and not a continuation of this one.

**Cost of the lesson: $0.153.**

## The four refusals before the halt, recorded because they are the real finding

This collector was derived from `phase7_inverse_inference_r1`, and three separate
inherited values were wrong. Each was caught by a different guard, and none
reached the wire:

| Refusal | Cause | Caught by |
|---|---|---|
| Stale parent | `PARENT` pointed at `parameter_followup_r2`, two designations back, so 2,360 existing reservations were absent from its `historical_keys` | ledger reservation check |
| Stale cap | `CAP` was $1.00, inherited from a 120-call collector, against a $3.162 reservation | `prepare()` size check |
| Non-JSON payload | `exemplars()` returned int keys and tuples; JSON round-trips them to strings and lists, so the object could never match its own checksum | `read_checked` at collect |

**The pattern is mine, not the guards'.** Deriving a collector by copying a
sibling carries its constants, and I did not audit what I inherited. Three
different guards caught three different consequences, which is the system working
— but the `check` subcommand reports worst-case cost **without enforcing `CAP`**
and does not exercise the save/load round-trip, so two of the three were
invisible until the freeze.

**Carried forward:** a derived collector's `PARENT`, `CAP`, `SEEDS`, `STUDY` and
payload shapes are audited against the new designation before the first freeze,
and `check` should exercise a save/load round-trip of every persisted object.

## Accounting

OpenAI $21.344140 → **$21.497550**/$40. Anthropic unchanged $22.268707/$32.
Package ≈ $43.766/$100. Usage estimates, not verified provider balances.
