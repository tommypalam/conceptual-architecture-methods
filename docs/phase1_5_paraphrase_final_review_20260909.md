# Assistant review of the final Claude paraphrases

Subsequent status: Tommy approved all three exact templates; the 4,500-call
experiment is complete. See the [approval](../experiments/phase1_5_encoding_validity/claude_paraphrases_20260909_theory_r5/paraphrases_approved.json)
and [results](../experiments/phase1_5_encoding_validity/paraphrases_20260909_final/analysis/PARAPHRASE_REPORT.md).
The preparation-stage review below is retained chronologically. Its semantic
recommendation did not predict the observed behavioural invariance failure.

The user explicitly approved disclosure of thesis section 3.1 and the canonical
template to Anthropic after discussing API ownership, confidentiality, training
and retention. This approval covers that disclosure, not human approval of
templates that had yet to be generated.

All generation used `claude-haiku-4-5-20251001`, temperature 1, output cap 10,000.
Four one-call designations preserve the complete sequence, r2 through r5.
No behavioural outcomes were included in generation or candidate selection.

- r2: raw response preserved; uppercase MOR/TFA violated the exact schema;
  authority-only legitimacy, instrumental procedure, and uniform treatment
  also changed meanings. Not approved for behavioural use.
- r3: formatting and all lexical checks passed, but semantic errors persisted.
  Targeted feedback identified 24 endpoints. No assistant replacement wording
  was supplied; Claude generated the revisions.
- r4: main semantic problems were corrected. The operational guard stopped
  because three unflagged endpoints also changed (MS high in variant 2; RT low
  and high in variant 3). Those edits were reviewed in full rather than hidden.
  They remove absolute scope wording and action/norm narrowing. Two CS phrases
  still required revision: autonomy-specific restriction and a new moderate-
  magnitude qualifier. No r4 behavioural collection was authorised.
- r5: exactly those two endpoints changed. The model placed its final list in
  `corrected_variants`, alongside echoed request material. The original parser
  stopped; a separate offline extraction preserves the returned words exactly,
  verifies the changed-endpoint set, and assembles the canonical scaffold.
  No additional API call was needed for this formatting recovery.

## Final semantic assessment

Compared against thesis v0.6 section 3.1, the current canonical template, and
the accepted operational commitments recorded in AGENTS.md and meta.md.
This follows the implementation's reviewed-paraphrase requirement; it does not
undo existing binding-constraint amendments or introduce new theoretical rules.

| Parameter | Assessment across the three final variants |
|---|---|
| LL | Institutional/shared warrant versus inward personal judgment and endorsement retained; general validity is not narrowed to authority or social rank. |
| CS | Environmental construal versus sensitivity to mild pressure retained; no magnitude range or autonomous-action-only restriction remains. |
| RT | Large versus small deviations activating response retained. No necessary response speed or outward action is imposed. |
| MoR | Inward reassessment/self-adjustment versus outward challenge/confrontation retained. |
| RE | Abstract standalone person-model versus roles and interpersonal ties retained; descriptions concern construal, not a required biography. |
| PD | Results dominate while procedure retains lesser value; fair procedure has independent worth at the other pole. Pure instrumentalism removed. |
| TfA | Equality as default and suspicion of unequal standing versus justified/intelligible asymmetry retained. Hierarchy is permissible, not mandatory. |
| ID | Outward compliance versus sincere endorsement and value congruence retained; identification/fusion and possession are not substituted. |
| MS | Local and role-linked bounds versus generalisable extension across persons and cases retained. Broad scope does not require identical treatment. |
| AW | Deliberative thought versus feelings and intuition retained; no sensory modality, evidential superiority or necessary immediacy is added. |

All three pass structural checks and per-parameter Jaccard < .4; the largest
overlap is .381. The assistant recommends them for human semantic review.
This is a judgment about wording, not empirical equivalence or an automated
substitute for human sign-off. All human_review.approved fields remain false.

The [exact templates and side-by-side endpoint table](../experiments/phase1_5_encoding_validity/claude_paraphrases_20260909_theory_r5/HUMAN_REVIEW.md)
are ready. The 4,500-call behavioural test has not started. The existing source,
rotations, gradients and audit results remain unchanged, and Phase 1.5 is open.

Synthetic review: Linden requires preserved directions and conceptual scope;
Osei requires disclosure of all preparation rounds and no outcome-conditioned
wording selection; Tanaka distinguishes lexical compliance from equivalence;
Renna preserves the accepted operational template; Okafor requires raw records,
exact hashes, explicit parser recovery, and human approval before dispatch.
Resolution: retain all drafts and recommend the final three for exact-template
human review. No model change, theory departure or phase-gate pass is inferred.
