# capstone_specificity_r2: profiles do not move negative controls

**Outcome: complete. 721 paid calls, 720/720 valid decisions, zero invalid.**
16 September 2026. Accepted independent review, then full collection.

**The prediction held exactly. Not one agent changed its answer on any control,
in any arm.** The capstone's specificity claim survives the check designed to
falsify it.

## Result

| Item | Value |
|---|---|
| Review verdict | **accept**, zero blocking issues |
| Decisions | 720 / 720 valid, 0 invalid |
| Tasks | 3 negative controls |
| Arms | E, V, U, G |
| **Discordant pairs, all 9 contrasts** | **0 of 540** |
| Cost | $0.399736425 |

Accounting: Claude $9.877096975/$32, OpenAI $4.250331525/$30, package
$36.759690825/$100. Usage estimates, not wallet balances.

## Primary outcome: net-score good rate

| Task | E | V | U | G |
|---|---:|---:|---:|---:|
| `ledger_error` | 1.000 | 1.000 | 1.000 | 1.000 |
| `duplicate_charge` | 1.000 | 1.000 | 1.000 | 1.000 |
| `expired_stock` | 1.000 | 1.000 | 1.000 | 1.000 |

Every arm chose the dominant option in every decision.

### Contrasts

| Task | E−U | V−U | G−U | Discordant |
|---|---:|---:|---:|---:|
| `ledger_error` | +0.000 | +0.000 | +0.000 | 0/60 each |
| `duplicate_charge` | +0.000 | +0.000 | +0.000 | 0/60 each |
| `expired_stock` | +0.000 | +0.000 | +0.000 | 0/60 each |

All permutation p = 1.0000, all Holm-adjusted p = 1.0000.

## What this establishes

The capstone's interpretation is **specific to standard-conflict**, not a
general answer shift.

| Task type | E−U |
|---|---:|
| Conflict: `safety_hold` | **+0.367** (Holm 0.0006) |
| Conflict: `witness_cost` | **+0.350** (Holm 0.0004) |
| Control: all three | **0.000** (Holm 1.0000) |

Same four arms, same 60 agents, same deterministic rule map, same paired
estimand, same harness, same session. The only difference is whether the four
fixed standards conflict. Where they do, profiles move choices by roughly
35 percentage points. Where one option upholds all four standards, profiles move
nothing at all.

This removes the main alternative explanation for
[moral_capstone_r3](../moral_capstone_r3/ASSESSMENT.md): that profiles simply
shift answers on anything and "which standard is sacrificed" is an artefact of
only ever testing conflicting items. They do not.

**The check was capable of failing.** Its prediction, interpretation and failure
condition were written into the protocol before collection, including the
statement that a control shift comparable to +0.350 would mean the capstone
framing was wrong. The result is a null on a test that could have produced the
opposite.

## What this does NOT establish

- **A null at a ceiling is weaker than a null in open space.** All three controls
  sit at 1.000 in the unprofiled arm, so movement was only possible downward.
  A profile effect that acts by *increasing* agreement with the dominant option
  could not be detected here. The controls were selected for exactly this
  structure, so this is a designed limitation, not a discovered one.
- **Three tasks, all from set B**, all saturated unprofiled.
- **No moral truth.** Labels are deterministic classifications under standards
  this project stipulated, computed from stipulated transitions and never from
  agent text. No AI or human rater is involved.
- **No human validation**; human raters remain deferred.
- 60 agents, one model, one harness, one snapshot, individual decisions only.
- A null here removes one alternative explanation. It does not prove the
  capstone's causal story, and it says nothing about mechanisms inside the model.

## Analysis provenance

All 720 decisions were collected and saved, then the run raised `KeyError` during
analysis: `analyze()` imported `primary_outcome` from the conflict pool rather
than the control pool, and the conflict pool does not contain control task ids.

**No data was affected.** The decisions were already written once to
`scored_rows.json` and the ledger. They were rescored offline with the correct
pool, with **zero API calls**, and the result is saved in `analysis.json`. The
import in the collector is corrected so the module reproduces.

[r1](../capstone_specificity_r1/ASSESSMENT.md) stopped at review for
$0.001498200 on a drafting error: it reused the capstone's reviewer instruction,
which requires every item to be a conflict with no fully-upholding option, and
these items are built to violate exactly that. The reviewer applied the
instruction correctly. r2 declares each item's kind in the packet and sends the
inverse criterion.

All 721 records are written once and preserved. No parameter, marginal,
correlation entry, locked question or societal axis definition was altered.
