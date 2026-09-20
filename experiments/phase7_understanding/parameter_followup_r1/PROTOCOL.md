# parameter_followup_r1 — protocol

**Status: prepared offline.** Programme: [../PROGRAMME.md](../PROGRAMME.md),
Stage 4a. Exploratory; not part of the submitted thesis.

## Question

Two of the ten framework parameters were never settled, and this designation pins
both at a sample size that can settle them.

| Code | Prior (sweep, 25 agents) | Status |
|---|---:|---|
| **AW** Affective Weighting | −0.036 | **never independently pinned** |
| **LL** Legitimacy Locus | −0.131, Holm 0.0008 | **withdrawn, unresolved** |

**AW is the substantive one.** Every swap control in the thesis puts the tested
level on AW's entry as the partner field. That rests on AW measuring −0.036 as a
by-product of `label_semantics_r1` — AW has never been pinned in its own right.
This is that test.

**LL has given three answers**: +0.271 post-hoc, −0.131 pinned at 25 agents,
−0.014 pinned at 40. It failed on the *larger* sample. A third pinned measurement
is reported as a third measurement; **it does not overturn the withdrawal by
majority vote.**

## Run statement (rule 4)

| | |
|---|---|
| Model | `gpt-5.4-mini-2026-03-17`, temperature 1, reasoning disabled |
| Configuration | NEUTRAL on all five axes |
| Agents | **80**, independent Beta marginals, seed **2026092022** |
| Cells | 2 coordinates x 2 levels = 4; 7 items; **2,240 calls** |
| Seeds | population 2026092022, schedule 2026092032, analysis 2026092033 |
| Cost | $10.984 reserved worst case; about $1.67 expected |

Design content hash `dc92b7ad958c008ec782b38bd8d746838072a9df0a0139688657c4122db94111`.

## Why 80 agents

Simulated against the measured gpt per-item baselines, Holm family 2, 20 seeds:

| Agents | \|0.10\| | \|0.15\| | \|0.20\| |
|---|---|---|---|
| 40 | **9/20** | 18/20 | 20/20 |
| **80** | **18/20** | 20/20 | 20/20 |

TfA and MoR (designation r2) sit at 0.10, and LL's largest measurement is 0.131.
**A 40-agent re-test would have been a coin flip on exactly the effects it was
built to settle** — which is how LL became unresolved in the first place.
False positives at 80 agents: 2/20.

## Design and analysis, fixed before collection

Each coordinate is pinned to 0.10 and 0.90 with the other nine drawn per agent and
held byte-identical between levels — the `pd_prospective_r1` design unchanged.
Verified for all 80 agents: the two levels differ on exactly one line, at that
coordinate's own entry, and are equal in length.

- **Two-sided for both.** Neither has a theory-derived direction on these items;
  adopting the sweep's sign after seeing it would be post-hoc confirmation.
- Paired sign test, Holm over the family of **2**, 4-of-7 item consistency, plus a
  95% unit-bootstrap interval and a 90% equivalence bound per coordinate.
- **No replication gate**: neither coordinate has an established effect to
  reproduce. That is the point of the designation.
- No coordinate re-run with more agents after results are seen.

**A null bounds the effect below about 0.10 on these items; it does not establish
zero,** and the assessment must say so.

## A defect caught before collection

The first population draw (seed …021) gave agent 76 an AW value rendering as one
of the two levels at the block's two decimals, which would have made that agent's
two arms byte-identical. `verify_construction` tests degeneracy at **rendered**
precision and blocked it. The seed was advanced by one before any call, on a
property of the draw alone — the same repair `label_semantics_r2` made for the
same defect.

## What no outcome establishes

Understanding, or that any coordinate is understood as a concept. That a
coordinate which moves the outcome is a **label** effect — that needs a swap
control, which this designation does not run. Anything beyond gpt-5.4-mini and
these seven items. **A null for AW supports the thesis's swap controls but does
not prove them:** it bounds AW's own effect, while the controls additionally
assume AW's entry is a fair partner for the tested field's entry.
