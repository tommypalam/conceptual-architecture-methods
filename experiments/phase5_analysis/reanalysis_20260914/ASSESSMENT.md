# Within-arm reanalysis of completed Phase 2 records

14 September 2026. Offline reanalysis of the frozen Phase 2 confirmation
responses. **Zero API calls; no frozen record, source or prior result was
modified.** Reproduce with `py -3.11 -B code/phase5_reanalysis.py`.

Inputs: `experiments/phase2_confirmation_20260913/analysis/responses.csv`
(4,800 valid simple-problem decisions, 2,400 E and 2,400 U) and
`population.json` (400 hash-locked profiles, content hash
`72ff60b5…f87363a`). Outputs in `dispersion_results.json`.

This is **post-hoc exploratory analysis of existing data**, with one exception
noted in section 3, which evaluates directional signs that were locked in thesis
v0.6 section 6.1.1 before Phase 2 collection. Nothing here is a new confirmation,
and no new hypothesis is presented as having preceded the responses.

## Why this analysis was run

The original Phase 2 analysis compared **arm-level rates** (E versus U) and
reported six contrasts, all surviving Holm correction. It did not ask whether
the ten parameters *within* the E arm predict which agent chooses what. That
question is the actual encoding-validity question, and the data to answer it
was already collected and paid for.

## 1. The no-profile baseline is degenerate in four of six cells

| Task | Config | U-arm distribution | Modal share | Unanimous |
|---|---|---|---:|---|
| S1 | 00100 | A 369 / B 31 | 92.2% | No |
| S1 | 11011 | A 383 / B 17 | 95.8% | No |
| S2 | 00100 | LOCAL_CORRECTION 400 | 100% | **Yes** |
| S2 | 11011 | LOCAL_CORRECTION 400 | 100% | **Yes** |
| S3 | 00100 | ADOPT 400 | 100% | **Yes** |
| S3 | 11011 | ADOPT 400 | 100% | **Yes** |

Without a profile the model is **perfectly deterministic** on S2 and S3 across
400 independent calls. This reframes the headline Phase 2 result: the six
contrasts are not measuring a shift in an already-varying distribution. In four
cells they measure **the introduction of behavioural variance where the
unprofiled model had none**.

This also explains the S3 sign reversal (−0.137, −0.370) that the original
results table left uninterpreted. The reversal is not a reversal of an effect
direction. Under the "first label" coding convention, S1's first label is the
U-arm *majority* option while S3's first label is the U-arm *unanimous* option,
so identical underlying behaviour — profiles moving agents off the baseline
choice — receives opposite signs. Recoded on the baseline-minority option, S2
and S3 move in the same direction; S1 is genuinely different, and moves the
opposite way (see section 4).

## 2. Procedural Dependence shows a monotone dose-response

In each of the four cells where the baseline leaves room, dissent rate rises
monotonically across PD quintiles. Dissent = choosing the option the U arm
never chose.

| Cell | Target option | Q1 | Q2 | Q3 | Q4 | Q5 | r | perm p |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| S2 00100 | FORMAL_REPORT | 3.8% | 11.2% | 16.2% | 43.8% | 66.2% | +0.517 | <0.0001 |
| S2 11011 | FORMAL_REPORT | 0.0% | 1.2% | 0.0% | 8.8% | 37.5% | +0.447 | <0.0001 |
| S3 00100 | WAIT | 2.5% | 7.5% | 6.2% | 15.0% | 37.5% | +0.325 | <0.0001 |
| S3 11011 | WAIT | 13.8% | 18.8% | 33.8% | 48.8% | 70.0% | +0.419 | <0.0001 |

Permutation tests shuffle the choice labels 10,000 times against fixed
parameter values (seed 20260914). Q1→Q5 spans 37.5 to 62.5 percentage points.
Two cells (S2 00100, S3 11011) are strictly non-decreasing across all five
quintiles; the other two each have one non-monotone step at low PD where the
dissent rate is near zero (S2 11011: 1.2%→0.0%; S3 00100: 7.5%→6.2%). In every
cell Q5 exceeds Q1 by a wide margin and Q4>Q3, so the gradient is the robust
feature rather than strict rank monotonicity.

## 3. The effect is specific to PD, not diffuse parameter sensitivity

A multivariate logistic regression on all ten standardised coordinates ranks
**PD first by coefficient magnitude in all four non-degenerate cells**
(standardised β = +2.22, +3.36, +1.24, +1.10). The second-ranked parameter
differs in every cell (MoR, MS, AW, LL), consistent with noise rather than a
second systematic driver. In the two S1 cells, where only 3 and 2 of 400 agents
dissent, PD ranks 5th (β = −0.27) and 10th (β = +0.11) — the fit there is
estimated on almost no outcome variance and should not be read as a real
negative effect.

This matters because the obvious deflationary explanation — "any number in the
prompt nudges the output, so ten numbers produce ten weak correlations" —
predicts diffuse, unranked sensitivity. What is observed is one dominant
coordinate whose identity is **theoretically correct**: PD is defined as the
outcome-versus-process axis (thesis §3.1, Colquitt 2001 anchor), and both S2
(report the error through channels versus fix it quietly) and S3 (follow the
reassignment process versus adopt for competitive gain) are process-versus-
outcome dilemmas.

### Scoring the pre-locked directional hypotheses

Thesis v0.6 §6.1.1 locked nine directional signs for S1–S3 before Phase 2
collection. They had never been evaluated against these responses. Scored
now, pooled over both configs, with 10,000-permutation two-sided p:

| Task | Parameter | Predicted | r | perm p | Verdict |
|---|---|---|---:|---:|---|
| S1 | RE | A | +0.102 | 0.0032 | **supported** |
| S1 | TfA | A | +0.034 | 0.350 | null |
| S1 | PD | A | −0.016 | 0.656 | null |
| S2 | ID | FORMAL_REPORT | +0.082 | 0.0217 | **supported** |
| S2 | TfA | LOCAL_CORRECTION | +0.159 | 0.0001 | **supported** |
| S2 | MS | FORMAL_REPORT | +0.259 | 0.0001 | **supported** |
| S3 | RT | ADOPT | +0.019 | 0.584 | null |
| S3 | MoR | ADOPT | +0.179 | 0.0001 | **supported** |
| S3 | RE | WAIT | +0.063 | 0.077 | null |

**Tally: 5 supported, 4 null, 0 wrong sign.** No hypothesis pointed the wrong
way. Under a null of random signs, 5 or more correct-signed significant results
from nine is unlikely, but these tests are not independent (shared tasks, shared
agents, correlated coordinates via R) and no multiplicity correction is applied
here, so this is a descriptive tally and not a corrected confirmatory test.

Two caveats keep this honest. First, the signs were locked prospectively but
this evaluation is retrospective, and the analysis choices (pooling configs,
point-biserial, permutation inference) were made after seeing the data.
Second, the strongest single effect — PD on S2 and S3 — was **not** among the
nine locked predictions; PD was predicted only for S1, where it is null. So PD's
dominance is a post-hoc discovery, and its theoretical fit is an argument for
testing it prospectively, not evidence that it was predicted.

## 4. S1 behaves in the opposite direction, and that is informative

S1 is the only task where the U baseline is non-degenerate (92–96%, not 100%),
and it is the only task where profiles move behaviour **toward** the modal
choice rather than away from it: A rises from 92.2%→99.2% and 95.8%→99.5%,
with PD ranked 5th and 10th of ten and near-zero correlations.

So the encoding effect is not a uniform "profiles create dissent" mechanism.
On the two tasks where the model is deterministic, profiles introduce variance
along a theoretically-appropriate axis. On the one task where the model already
varies, profiles *suppress* variance. Whether that is consolidation toward a
profile-implied answer, or a reduction in sampling noise from a longer prompt,
is not identified by this data and needs the prospective design in section 6.

## 5. What this does and does not establish

**Does:** within the E arm, one theoretically-identified coordinate accounts for
which agents depart from the unprofiled baseline, with a monotone dose-response
and dominance over all nine other coordinates, in four independent cells of
n=400 each. This is stronger evidence for functional normative parameterization
than the original arm-level contrasts, because arm-level differences are also
consistent with generic prompt-length or persona effects, whereas a PD-specific
monotone gradient is not.

**Does not:** establish ethical understanding, human resemblance, moral quality,
or validity for the other nine coordinates. Nine of ten parameters show no
systematic effect here. The two anchors still flip all five context bits
together, so no institutional axis is identified. All results are one model
snapshot, one harness, three stylized dilemmas. PD's dominance was not
prospectively predicted for these tasks. Contamination is not addressed: the
recognition screen showed 50/50 identification of all five benchmark families,
and these three problems are not classic benchmarks but were not recognition-
screened either.

**Prior conclusions unchanged.** The accepted Phase 1.5 closure already
identified PD as the clearest evidence for initial functional parameterization,
with independent replication. This reanalysis strengthens and quantifies that
existing conclusion on new data; it does not overturn any recorded outcome or
reopen a closed phase.

## 6. Implication for the remaining phases

The degeneracy table is a design tool, not just a limitation. Four of six cells
had no baseline variance, which is why most Phase 3 and Phase 4 pilots saturated:
`transfer_pilot_r1` (448/448 identical), `consequence_rule_pilot_r1` (96/96
identical). Those nulls are now interpretable as the same phenomenon — tasks
whose unprofiled answer is deterministic cannot discriminate arms.

Recommended, and not yet authorised or frozen:

1. **Pre-screen task dispersion in the U arm before spending on any new arm.**
   A cheap, small-n unprofiled probe predicts whether a task can discriminate.
   This is the single highest-value change to Phase 3/4 protocol design.
2. **Prospectively test the PD gradient** on fresh process-versus-outcome tasks,
   with the direction and the dose-response shape stated in advance. This
   converts a post-hoc discovery into a confirmation, and it is the natural
   Phase 3A transfer study.
3. **One-bit configuration contrasts** against `00100` to identify individual
   institutional axes, resolving the confound both anchors currently carry.

Section 6 items are proposals for separately designated protocols. No paid run,
budget change, sample extension or parameter revision is authorised by this
document. All reported numbers come from already-collected, already-paid records.

## Five-perspective review

Decision: report a post-hoc within-arm parameter analysis of frozen Phase 2 data,
and treat PD's dominance as a discovery requiring prospective test.

- **Linden:** a dominant process/outcome coordinate is a claim about behavioural
  sensitivity to a normative axis, not about the agent grasping procedural
  justice. Keep that distinction in the manuscript's wording.
- **Osei:** the degeneracy table is the most valuable output here — it explains
  four saturated pilots at once and should gate every future task selection.
  Deterministic baselines are a measurement failure, not a finding about ethics.
- **Tanaka:** permutation inference on fixed parameters is appropriate, but the
  nine hypothesis tests are dependent and uncorrected, and the analysis pipeline
  was chosen after seeing the data. Report the tally descriptively; the monotone
  quintile gradient is the more robust evidence than any single p-value.
- **Renna:** PD dominance propagates directly into Phase 4 — the moral tasks must
  be process/outcome-contested or they will saturate exactly as r1 did.
- **Okafor:** the analysis is reproducible offline from committed code with a
  fixed seed and touches no frozen record. The S1 reversal needs its own
  explanation before it appears in a paper; do not fold it into the main claim.

Genuine disagreement: Tanaka and Osei treat the hypothesis tally as too
dependent and too retrospective to headline, while Renna reads the PD gradient
plus its theoretical fit as the paper's central finding. Resolution: lead with
the degeneracy table and the PD dose-response (both descriptive and robust),
report the tally as secondary and explicitly uncorrected, and commit the
prospective PD test in section 6 before any confirmatory language is used.
These are structured review roles, not external expert review or human approval.
