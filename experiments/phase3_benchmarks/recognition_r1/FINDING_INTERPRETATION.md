# What the recognition screen found

14 September 2026. Interpretation note. **No record, result or frozen assessment
is changed by this document.** The
[completed screen](execution/transport_r1/ASSESSMENT.md) and its numbers stand
exactly as recorded.

## The result was filed as a failure; it is also a finding

The screen is recorded under "all five alternatives rejected", because its
operational purpose was to qualify low-recognition control stimuli and none
qualified. That disposition is correct and unchanged: the five alternatives
cannot serve as familiarity controls under this protocol.

But the *measurement itself* succeeded, and it is more informative than the
operational verdict suggests:

| Property | Value |
|---|---|
| Probes | 500 (50 per cell, 10 cells) |
| Cells | 5 benchmark families × {canonical, decanonised alternative} |
| Recognition rate | **50/50 in every one of the 10 cells** |
| Wilson 95% CI per cell | 92.87% – 100% |
| Independent raters | 2, from **different providers** (Haiku 4.5, GPT-5.4 mini) |
| Inter-rater agreement | **500/500 exact**, no ambiguity or refusal flags |
| Adjudication calls needed | 0 |

The five families are Milgram obedience, Asch conformity, the Ultimatum Game,
the bystander effect, and psychological reactance. Each alternative had already
passed an independent structural review confirming it preserved the original's
operational structure while changing surface domain
([variants_r3](../variants_r3/ASSESSMENT.md), five accepts).

## The claim this supports

**Structure-preserving domain substitution does not conceal a classic
social-psychology paradigm from a frontier model.** Re-skinning Milgram as
written reprimands, Asch as colour judgements, the Ultimatum Game as bonus
allocation, the bystander effect as a system incident, and reactance as a work
plan left all five identifiable at a rate indistinguishable from the canonical
originals.

This is a measured, cross-provider-adjudicated negative result about a
contamination-control strategy that the LLM-agent literature uses routinely and
usually does not test. It generalises beyond PARIA: any study that decanonises a
famous benchmark to control for training-data familiarity, and does not screen
recognition, may have no control at all.

## Limits, stated precisely

- **One frozen stimulus bundle per form**, sampled 50 times. The intervals
  describe repeated sampling under this prompt, not variability across scenario
  designs. A different decanonisation might succeed; this shows that structural
  fidelity is not sufficient for concealment, not that concealment is impossible.
- **Recognition ≠ contamination.** The probes cannot distinguish memorised
  training examples from reasoning about shared abstract structure. A model that
  infers "this is an obedience paradigm" from the escalation structure alone is
  recognising, not recalling. Either way the control fails, but the mechanism is
  unidentified.
- **Recognition ≠ behavioural imitation.** Naming a paradigm does not establish
  that behaviour in it is copied from the literature rather than generated.
- **One probed model** (Sonnet 4.6) and two AI raters, one sharing a provider
  with the probe. Agreement is not human validation.
- **Batched coding** permits within-batch dependence despite independent shuffles.
- **Post-failure format amendment.** The coding ID format changed from long
  arbitrary strings to 1–10 after two coding batches failed on a model-altered
  ID. Original responses, rubric, models, temperatures, order, batch membership
  and token limits were unchanged, and the strict parser still rejects wrong,
  duplicate, missing or reordered IDs. This is an explicit prospective amendment,
  not an unchanged preregistered execution; no experiment established that
  formatting is inert.

## Consequence for the thesis

Thesis §5.3 makes the **configuration counterfactual** the primary success
criterion precisely because all five benchmarks are famous. This screen confirms
that the alternative route — hiding the benchmark — is closed, so the
configuration counterfactual is not merely preferred but the only available
discriminator. That in turn makes the currently-confounded anchor design
(`00100` versus `11011` flips all five context bits together) the critical gap to
close, and raises the value of one-bit configuration contrasts.

It does not establish or refute encoding validity, ethical understanding, human
resemblance, or moral quality. No population collection is released by this note.

## Disposition

Keep the operational verdict (alternatives rejected, gate unmet) and report the
recognition rate as a substantive finding in its own right. Both are true and
they are not in tension: the strategy failed, and the failure is the result.
The five-perspective review recorded in the original assessment already noted
that recognition is separate from ethical understanding; nothing here revises it.
