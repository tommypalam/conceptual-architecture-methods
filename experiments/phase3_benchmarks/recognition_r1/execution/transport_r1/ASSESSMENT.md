# Recognition screen complete: all five alternatives rejected

All500 saved Sonnet4.6 recognition answers have two valid initial classifications,
one from Haiku4.5 and one from GPT-5.4 mini. The raters agreed exactly on all500
answers, with no ambiguity/refusal flags; no discussion was needed or charged.
Every canonical and alternative form was recognised in50/50 responses.

The five alternatives fail the frozen >15/50 recognition gate. They cannot be
used as accepted low-recognition controls under this protocol. This screening
stage is complete, but Phase3 remains open and population collection is not
released. The earlier structural accepts remain valid as text-level reviews;
structural fidelity did not produce low recognition in these candidates.

## Results

| Benchmark family | Canonical recognised | Alternative recognised | Unresolved in either cell | Alternative gate |
|---|---:|---:|---:|---|
| Milgram obedience | 50/50 | 50/50 | 0 | Reject |
| Asch conformity | 50/50 | 50/50 | 0 | Reject |
| Ultimatum game | 50/50 | 50/50 | 0 | Reject |
| Bystander effect | 50/50 | 50/50 | 0 | Reject |
| Psychological reactance | 50/50 | 50/50 | 0 | Reject |

Each cell has a nominal Wilson95% interval of92.87%–100%. These intervals describe
repeated model sampling under this prompt and do not establish human population
rates, cross-model generalisation, or independent variability across scenario
designs. There is one frozen scenario bundle per form, sampled50 times.
Canonical results are descriptive positive controls; no post-hoc numerical
positive-control threshold was introduced. See [results.json](results.json).

## What this means for the thesis

Under this elicitation, changing the surface domain while preserving a classic
experiment's structure did not conceal its identity from Sonnet. The result
supports rejecting these particular alternatives as low-recognition controls.
It does not establish whether the recognition arose from memorised training
examples or reasoning about shared structure. Recognition alone cannot identify
training-data contamination or behavioural imitation.

The main thesis questions remain untested by this screen: whether generation-time
ethical encoding changes decisions in a mechanism-specific way; whether agents
resemble humans; and whether their actions have good or bad outcomes. These500
calls were familiarity probes without LPM profiles, not population simulations.
Neither this result nor the previous structural accepts validates or refutes
intrinsic ethical understanding. All ten coordinates, Beta distributions and R
remain unchanged.

## Recovery and format amendment

The first attempt saved all500 probes and28 valid coding batches, then failed
when Haiku changed one character of an opaque answer ID. The single exact
replacement reproduced the same invalid ID. Both raw responses and their full
$0.031920900 reservations remain immutable; neither batch was partially salvaged.

The linked [transport protocol](PROTOCOL.md) prospectively replaced long arbitrary
IDs with strings1–10 within the same shuffled batches. Original answer text,
rubric, models, temperatures, order, batch membership and token limits stayed
unchanged. A frozen bijection maps valid returned IDs back to original records.
The original strict parser still rejects wrong, duplicate, missing or reordered
IDs. No original response was edited or model-generated ID silently repaired.

The remaining72 coding calls then completed successfully, reusing all500 probes
and28 valid batches. There are100 valid coding calls overall,1000 initial labels,
and500 dual-coded outcomes. The final study mixes long and short arbitrary coding
IDs. This is an explicit post-failure format amendment, not a completely unchanged
preregistered execution; no experiment established that formatting is inert.
Both raters are AI models, and the judge and one rater share a provider. Agreement
does not substitute for human validation. Batched coding also allows within-batch
dependence despite the independent shuffles and fresh calls.

## Cost and verification

| Accounting item | USD |
|---|---:|
| 500 probes | 5.337931500 |
| First28 valid coding calls | 0.112679600 |
| Two failed coding calls, full reservations retained | 0.063841800 |
| Final72 valid coding calls | 0.172739600 |
| Discussion | 0 |
| **Complete recognition screen** | **5.687192500** |
| **Additional cost during this CONTINUE turn** | **0.204660500** |
| All Phase3 work to date | 6.103591450 |
| Claude total / remaining under $15 cap | 5.949588700 / 9.050411300 |
| OpenAI total / remaining under $30 cap | 0.154002750 / 29.845997250 |
| Package including Phase2 / $100 cap | 29.009664475 / 100 |

Amounts are conservative usage accounting, not verified invoices or balances.
The screening finished well below its $14.067432500 maximum. No more paid work
is running or queued. Do not rerun the successful screen merely to resume.

Seven recovery/transport tests passed, including full simulated completion and
zero-call replay; seven existing parser/ledger/analysis checks also passed.
Final replay against real records made zero API calls and reproduced the exact
result, discussion eligibility and identifier mappings. Every historical record,
frozen source and request/cost link was checked. There are650 paid records in the
ledger and1,952 JSON/JSONL members in the verified local archive. See
[CHECKPOINT.json](CHECKPOINT.json). The earlier archives/checkpoints are retained.

Archive: `output/phase3_recognition_transport_r1_20260913.zip`.
SHA256: `cbc3e2d09723fd79fd7a10014733f4aa55722fecb9064b25f984390e03e7b2c9`.
Raw records and archives remain excluded from Git. Off-device backup is not verified.

## Next decision

Do not move these alternatives into a population run as if they passed. First
review the scenario-design strategy offline: cosmetic rewording has not achieved
the required separation here. A new candidate round would need a new designation,
mechanism-preserving structural review, and its own recognition screen. Keep the
current failed alternatives and results as evidence; do not loosen the threshold
after observing them or pool replacement candidates with this sample.

An inexpensive exploratory check could help reject obviously recognisable future
designs before paying for a full screen, but a small pilot would not satisfy the
specified N50 acceptance gate. No new candidate generation, pilot or population
collection is authorised automatically by this completed screen. Human benchmark
counterfactuals and modulators remain downstream; human moral validation is Phase4.

## Five-perspective review

Decision: close this screening as completed with five rejections and keep population gated.

- Linden: the failed recognition controls do not decide the ethical-understanding
  question, and recognition should not be relabelled proof of memorisation.
- Osei: repeated responses to one bundle do not constitute50 different scenarios;
  preserve domain/stakes limitations and the distinction from human benchmarks.
- Tanaka: all denominators and dual ratings are complete;50/50 clearly exceeds
  the frozen threshold. No discussion, imputation or post-hoc threshold change.
- Renna: the negative instrument result narrows the next design task without
  invalidating earlier encoding evidence or changing LPM commitments.
- Okafor: preserve both failed attempts, disclose the format amendment, and avoid
  spending on population collection before addressing the failed control gate.

The main tension is preserving a familiar experimental mechanism while making its
identity unfamiliar. Resolution: retain that tension as a design problem and
record the actual negative result. These are synthetic review perspectives, not
external expert assessment or the two independent coding passes.
