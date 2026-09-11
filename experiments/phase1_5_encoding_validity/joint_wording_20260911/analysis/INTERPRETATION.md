# Joint-profile wording screen: a large local failure

**480/480 valid responses; no API, model or usage failures.** The fixed,
approved allocation completed for an estimated$0.5156505. All original
records remain write-once; no retries, replacements or historical pooling.

| PD | MoR | Canonical ADOPT /30 | P1 /30 | P2 /30 | P3 /30 |
|---|---|---|---|---|---|
| .1 | .1 | 26 | 30 | 20 | 27 |
| .1 | .9 | 30 | 30 | 30 | 30 |
| .9 | .1 | 2 | 0 | 4 | 1 |
| .9 | .9 | 8 | 21 | 29 | 25 |

## Primary result

At PD=.9/MoR=.9, paraphrase2 minus canonical changes ADOPT by **+.700**.
Its simultaneous95% interval is **[+.193,+.923]**, entirely beyond the.10
margin. This meets the frozen criterion for **GROSS_LOCAL_WORDING_FAILURE_DETECTED**.
The family-wide bounds account for all16 cells and24 wording-pair contrasts;
this is not a favourable pair selected under an unadjusted interval.

One of24 pair intervals establishes a difference beyond.10. The remaining23
do not establish equivalence: the screen has limited precision. In particular,
all30/30 responses at PD=.1/MoR=.9 are ceiling agreement, not evidence that
the model is faithfully distinguishing the whole profile. All three approved
wordings are retained; none is selected as the new canonical implementation.

This is a local stress test, not the original30-cell battery. It does not
change the original8/30 equivalence count or gate. All ten endpoint descriptions
vary together across the approved templates; the failure cannot be assigned
to PD wording or MoR wording alone. The locked dilemma remains unchanged.
See [full numerical report](WORDING_REPORT.md) and [all16 rates](fig_01_joint_wording.png).

## A separate canonical repeat discrepancy

The high-PD/high-MoR canonical cell was23/30 ADOPT in the immediately preceding
PD interaction diagnostic and8/30 in this fresh screen. The other three
canonical endpoint comparisons were25→26,30→30 and3→2, each out of30.
This discrepancy must accompany, rather than be hidden behind, the new
within-run wording result.

A post-score [provenance audit](canonical_repeat_audit.json) checked all240
matching canonical endpoint records across the two runs. Message bytes,
profiles, declared model snapshot, temperature, output cap and transport
settings match. All240 API IDs and requested seeds are distinct; raw response
payload text matches saved text and reparsed decisions. No request/profile/
parse mismatch was found in these checks. The exact source renderer and
single-attempt client also retain their frozen hashes.

The runs used different requested seeds, schedules, times and surrounding
experimental allocations. Both sets of responses lack a backend fingerprint.
This audit therefore cannot identify the cause or establish a backend change,
seed effect, hidden coupling, or absence of every possible implementation bug.
The difference is a reproducibility concern, not a new proven mechanism.
The earlier result remains reported as collected; it is not a stable canonical
effect size we can assume transfers unchanged. No repeated calls were made
to resolve this discrepancy, and the two runs are not pooled.

## What remains supported and what does not

Numerical profiles influence decisions in these selected conditions, and
some endpoint directions recur across wordings. However, their magnitude and
the high-PD/high-MoR decision distribution are not stable across the tested
wordings. The current canonical high-minus-low-PD MoR endpoint-effect contrast
is+.067, with conservative nominal interval[-.527,+.635]; the stronger previous
interaction cannot be presented as cleanly reproduced by these endpoints.

P1/P3 have positive nominal secondary endpoint-interaction intervals, but those
are not family-adjusted across secondary contrasts, are not a five-value curve
test, and cannot select a winning template or repair the primary failure.
No internal ethical understanding, moral correctness, smooth graded encoding,
capacity estimate, or general impossibility result follows.

## Decision and spending

Bank the diagnostic outcomes without launching another full sweep or promoting
a favourable paraphrase. The new evidence identifies an unresolved high-PD/
high-MoR condition and adds an exact-prompt reproducibility concern. A further
scientific claim about that condition needs a separately frozen stability or
mechanism study, not another selected positive slope. No such run is queued.
The900-call representation confirmation remains paused; Phase2 remains on hold.
All five concepts, ten parameters, original definitions and phase gates remain.

Known cumulative usage$3.8945805; conservative charge including the earlier
unknown timeout reservation$3.89954775, leaving$5.10045225 from the latest$9
allowance. No pending calls; provider balance unverified. Raw archives and
report/figure bundles are verified locally, which is not an off-device backup.
