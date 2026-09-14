# crossmodel_coding_r2: the recognition finding generalises across providers

**Outcome: complete. 200/200 coding calls, 1000 probe answers coded, zero coding
failures.** 15 September 2026. Coding continuation for
[crossmodel_study_r1](../crossmodel_study_r1/ASSESSMENT.md), reusing its 1000
paid probe answers unchanged.

**Four of five decanonised paradigms were recognised at 100% by both models.
Reactance was not recognised by either, in either form.**

## Result

| Item | Value |
|---|---|
| Coding calls | 200 / 200, zero failures |
| Probe answers coded | 1000, none missing |
| Rater disagreements | 18 of 1000 (1.8%) |
| Flagged ambiguous or refusal | 2 |
| Cost | $0.574927375 |

Accounting: Claude $9.874679100/$32, OpenAI $3.850214775/$30, package
$36.358456200/$100. Usage estimates, not wallet balances.

## Recognition rate, both raters independently naming the family

Fifty probes per cell. Wilson 95% intervals.

| Family | Form | haiku-4.5 | gpt-5.4-mini |
|---|---|---|---|
| Milgram | canonical | **1.00** [0.929, 1.0] | **1.00** [0.929, 1.0] |
| Milgram | alternative | **1.00** [0.929, 1.0] | **1.00** [0.929, 1.0] |
| Asch | canonical | **1.00** [0.929, 1.0] | **1.00** [0.929, 1.0] |
| Asch | alternative | **1.00** [0.929, 1.0] | **1.00** [0.929, 1.0] |
| Ultimatum | canonical | **1.00** [0.929, 1.0] | **1.00** [0.929, 1.0] |
| Ultimatum | alternative | **1.00** [0.929, 1.0] | **1.00** [0.929, 1.0] |
| Bystander | canonical | **1.00** [0.929, 1.0] | **1.00** [0.929, 1.0] |
| Bystander | alternative | **1.00** [0.929, 1.0] | **1.00** [0.929, 1.0] |
| Reactance | canonical | 0.30 [0.191, 0.438] | 0.08 [0.032, 0.188] |
| Reactance | alternative | 0.02 [0.004, 0.105] | 0.00 [0.0, 0.071] |

### Canonical minus alternative, per model

| Model | Canonical | Alternative | Difference |
|---|---:|---:|---:|
| haiku-4.5 | 0.860 | 0.804 | **+0.056** |
| gpt-5.4-mini | 0.816 | 0.800 | **+0.016** |

Both differences are driven entirely by reactance. On the four other families the
difference is exactly zero on both models.

## What this establishes

**The single-model finding generalises.** The original
[recognition_r1](../recognition_r1/execution/transport_r1/ASSESSMENT.md) screen
probed one model and found all five decanonised variants identified at canonical
rates. On four of five families that now replicates exactly, on a second model
from a different provider, at 50 probes per cell: **1.00 in every one of sixteen
cells, canonical and alternative alike.**

Structure-preserving domain substitution does not conceal Milgram, Asch, the
Ultimatum Game or the bystander paradigm from either model. The claim is no
longer about one model.

**Cross-model agreement is near-total where recognition occurs.** Per-family
rate gaps between the two models are 0.00 on all eight non-reactance cells.

**Rater agreement is high.** 18 disagreements in 1000 answers (1.8%), 2 flagged
ambiguous or refusal, zero coding failures.

## The reactance exception, and why it is not a hole

Reactance behaves completely differently: 0.30 and 0.08 canonical, 0.02 and 0.00
alternative. **Its canonical form is barely recognised either**, which is the
key observation. This is not a case of decanonisation succeeding where it failed
elsewhere; the paradigm is weakly identified in the first place.

The exploratory pilots recorded what the misses look like: haiku named "the
Decoy Effect (or Attraction Effect)", gpt-5.4-mini named "the framing/
choice-reversal paradigm". Both described the option-restriction structure
accurately and attached a different label. Under the frozen rubric, naming a
different paradigm is not recognition of reactance, which is correct and is why
the rate is near zero.

Two readings are available and this study does not separate them: the Worchel &
Brehm reactance-restoration design may be less distinctive as a structure than
the other four, or the frozen reactance stimulus may be a weaker rendering of it.
The canonical rate of 0.30 and 0.08 is evidence for the first but does not
exclude the second.

## What this does NOT establish

- **Recognition is not contamination.** These probes cannot separate memorised
  training examples from inference over shared abstract structure. Either way a
  decanonised control fails, but the mechanism is unidentified.
- **Recognition is not behavioural imitation.** Naming a paradigm does not show
  that behaviour within it is copied from the literature.
- **Two models, two providers**, both mid-tier. Not a survey of the field, and
  the original screen's probe target was not re-probed here.
- **One frozen stimulus bundle per form.** A different decanonisation of the same
  paradigm might succeed; this shows structural fidelity is not sufficient for
  concealment in four of five cases.
- **The reactance result is about this stimulus**, and its low canonical rate
  means it cannot be read as decanonisation succeeding.
- Raters are AI models and each shares a provider with one probe target.
  Agreement is not human validation.
- No ethical understanding, human resemblance or moral quality, and no claim
  that either model is better than the other.

## Consequence for the project

Thesis section 5.3 makes the configuration counterfactual the primary success
criterion because all five benchmarks are famous. This study confirms across two
providers that the alternative route — concealing the benchmark by re-skinning
it — is closed for four of the five families, and that the fifth is not concealed
either, merely weakly identified in both forms.

## Provenance

All 200 coding records written once and preserved. The 1000 probe answers are
reused byte-unchanged from `crossmodel_study_r1`; no probe was re-collected.
Stimuli, recognition question, system prompt and coding rubric are the frozen
`recognition_r1` text.

[crossmodel_coding_r1](../crossmodel_coding_r1/) stopped after one dispatched
call: it re-parsed the shared ledger parser's already-validated output as text.
Its release pinned the pre-fix module hash, so that file was restored byte-exact
and the repair placed in a separate r2 module. One paid call is preserved.
