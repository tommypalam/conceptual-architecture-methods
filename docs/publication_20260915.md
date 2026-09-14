# Publication record, 15 September 2026

The researcher authorised publishing the Phase 3 closure and the completed
Phase 4 moral capstone to `main`, preserving the previous published `main` as
`backup-3`.

## Branch targets

| Branch | Commit | Meaning |
|---|---|---|
| `backup` | `c8e7aa0b` | Original published main; retained unchanged |
| `backup-1` | `aaed0a8d` | Second published main; retained unchanged |
| `backup-2` | `470d5cb6` | Third published main; retained unchanged |
| `backup-3` | `674e76d1` | **New.** The published main immediately before this release |
| `main` | fast-forwarded | Now carries the Phase 3 closure and the Phase 4 capstone |
| `research-transfer-design-20260913` | development | Source branch; pushed for continuity |

`main` was an ancestor of the development branch, so the update is a
fast-forward. No history was rewritten, force-pushed or reset.

## What is published

### Phase 3, closed for a scoped objective

[Closure record](../experiments/phase3_benchmarks/PHASE3_CLOSURE_2026-09-14.md).
Phase 3 characterised the boundaries of the measurement approach rather than
delivering a benchmark pass. The original five-benchmark N200 study is not
released, Phase 3B human comparison was never attempted and is deferred as
infeasible, and neither is retrospectively passed.

The decisive evidence is
[pd_endpoint_r2](../experiments/phase3_benchmarks/pd_endpoint_r2/ASSESSMENT.md):
an accepted design review followed by 150 unprofiled decisions on six fresh
dilemmas, all six returning modal share 1.00 with presentation order irrelevant
(51.3%). Ambiguity certified by an independent reviewer does not produce
dispersion in the harness.

The PD gradient sequence (six designations, $0.093134250, zero profiled
decisions) is preserved with each stop and its findings, including two reviewer
findings recorded as errors rather than deferred to.

### Phase 4, first completed moral experiment

[moral_conflict_screen_r2](../experiments/phase4_coding/moral_conflict_screen_r2/ASSESSMENT.md)
produced the project's first non-saturated moral task set: three of six tasks
disperse, order irrelevant at 48.0%.

[moral_capstone_r1](../experiments/phase4_coding/moral_capstone_r1/ASSESSMENT.md)
then collected 480/480 valid decisions across four arms on the two tasks that
cleared both prespecified gates.

| Task | E | V | U | G |
|---|---:|---:|---:|---:|
| `witness_cost` | 0.750 | 0.900 | 0.233 | 0.417 |
| `safety_hold` | 0.750 | 0.767 | 0.717 | 0.533 |

`witness_cost` E−U = **+0.517**, paired permutation p = 0.0001, **Holm
p = 0.0002**; V−U = +0.667. `safety_hold` shows no effect (+0.033, p = 0.82).
Thirty-four agents moved from the deceptive option to the accurate one and three
moved the other way. Profiled arms deceive less and accept more harm; the
profiles changed **which** standard was sacrificed, not how many.

### Supporting work

The [Phase 5 reanalysis](../experiments/phase5_analysis/reanalysis_20260914/ASSESSMENT.md)
and [saturation diagnosis](../experiments/phase5_analysis/reanalysis_20260914/SATURATION_DIAGNOSIS.md)
were published in the previous release and are unchanged here.

## Verification before release

| Check | Result |
|---|---|
| Working tree | Clean; 11 commits ahead of `main` |
| Task and rule modules | Reproduce; conflict, clean-option and discrimination checks pass |
| Phase 5 reanalysis | Byte-identical on rerun, seed 20260914 |
| Offline tests | 56 passing in the suites touched by this work |
| Raw data in commits | None; `data/` and `output/` remain excluded |
| Secret scan on new code | No matches |
| `git diff --check` | Clean |
| Fast-forward | `main` is an ancestor of the development branch |

## Accounting

Claude $7.139674300/$15, OpenAI $1.783980000/$30, package $31.829727325/$100.
Usage estimates, not verified provider balances. No collector is running and no
paid batch is queued.

## Scope limits

Publication establishes no scientific claim beyond what each assessment records.

- Moral labels are deterministic classifications under standards this project
  stipulated, computed from stipulated transitions and never from agent text.
  **No moral truth, no human validation, and no AI rater.** A higher net-score
  good rate is not evidence that an agent is morally better.
- The capstone rests on **two stylised tasks, one of which showed no effect**,
  with 60 agents, one model, one harness, one snapshot, and individual decisions
  only. No group or institutional evaluation; the societal-axis confound is
  untouched.
- The guidance-arm comparison is one wording on two tasks and is suggestive, not
  a general claim about ethical instruction.
- The PD gradient remains untested prospectively. The Phase 5 reanalysis stands
  as recorded: post-hoc, on Phase 2 data.
- Phase 4 is **not complete**. The capstone is one individual experiment within
  it; group decisions and a broader task base remain open.
- No ethical understanding, human resemblance or moral superiority is
  established by any result here.

Raw per-call records and archives remain excluded from Git, so a clone is not the
dataset; off-device backup is still unverified. See the
[desktop handoff](desktop_handoff.md) for the separate data transfer.
