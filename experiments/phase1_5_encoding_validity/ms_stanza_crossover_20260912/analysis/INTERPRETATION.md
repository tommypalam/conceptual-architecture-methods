# MS crossover: the canonical control did not replicate

**160/160 valid responses collected for $0.1862505.** No API/parse failures,
retries, discarded records or pending requests. The result is not a wording
repair: the previously strong canonical MS endpoint effect did not repeat.

| Other-nine descriptions | MS description | Reports at MS=.1 | Reports at MS=.9 |
|---|---|---:|---:|
| Canonical | Canonical | 0/20 | 0/20 |
| Canonical | P2 | 0/20 | 2/20 |
| P2 | Canonical | 0/20 | 2/20 |
| P2 | P2 | 0/20 | 3/20 |

The four prespecified high-value comparisons all have Holm-adjusted p=1.
MS-stanza effects are +10pp and +5pp within canonical and P2 backgrounds;
background effects are also +10pp and +5pp within the two MS stanzas.
Their conservative nominal95 intervals include zero and substantial effects:
[-18.8,+34.9]pp and [-32.4,+40.2]pp respectively. Non-detection is not equivalence.
The secondary high-value interaction is -5pp, interval[-73.7,+65.3]pp.
All endpoint effects and intervals are in the [full report](REPORT.md).

## The repeat discrepancy changes the interpretation

The exact full-canonical MS=.9 control previously produced 14/20 formal reports;
it now produced 0/20. The post-result new-minus-old comparison is -70pp,
conservative nominal95 interval[-89.8,-23.0]pp. A diagnostic two-sided Fisher
comparison, Holm-adjusted across all four repeated endpoint controls, gives
p=0.00001336. This was not a prespecified primary and does not establish a cause.
It is strong evidence against explaining this discrepancy as ordinary
independent binomial sampling from one fixed response probability alone.

[The repeat audit](repeat_audit.json) checked 160 matching control records:
80 of the prior640 and80 of the new160, with no invalid-record exclusions.
Messages, all ten values, labels, provider, returned model identifier,
temperature and token limit match. The executor functions are identical in
Python syntax trees and use the same SDK client class. Provider payloads match
saved text and reparsed decisions. All160 IDs and requested seeds are unique.
Times, requested seeds and interleaved allocations differ by design; backend
fingerprints are absent in all160 responses. No verified local request or
parsing discrepancy was found. Backend drift, seed sensitivity or another
unobserved cause has not been demonstrated.

The fresh controls were essential. Had we reused the old14/20 canonical result,
we might have incorrectly attributed a between-run shift to a swapped stanza.
The original canonical/P2 difference is not reproduced here, so this run cannot
locate a stable mechanism behind that earlier gap. It neither shows that P2 was
fixed nor that all four compositions preserve effective MS encoding.

## Consequence for the phase

Keep all positive and negative results, with this failed canonical replication
prominent. The theoretical meaning of MS and the locked dilemma remain intact.
The next useful priority is reproducibility of identical requests across
collection blocks, before more wording repair or a larger validation sweep.
Start with existing archives to map repeated exact-request behaviour; any new
paid stability test requires its own frozen allocation, rather than continuing
until a favourable count appears. No additional calls are queued here.

Original Phase1.5 gate remains unmet (8/30 paraphrase equivalence cells;24
required), Phase2 remains held. This study does not establish internal ethical
understanding or refute the possibility of ethical encoding in other designs.

All160 current records and the raw archive were verified byte-for-byte. The
figure was visually checked. Local backup is on this computer; no off-device
backup claim. Remaining conservative tracked allowance **$3.79170675**;
provider balance unverified. Configuration neutral, N20 per condition,
seed20260927, model gpt-5.4-mini-2026-03-17.
