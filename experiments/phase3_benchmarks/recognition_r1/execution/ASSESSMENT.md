# Recognition collection saved; coding stopped

The approved run collected all 500 recognition responses, then stopped on an
invalid identifier in Claude's 29th coding response. No automatic retry occurred.
This is an incomplete recognition screen, not a scientific pass or rejection.
Phase 3 remains open and no agent population collection is released.

## Completed evidence

| Stage | Valid calls | Failed calls | Remaining |
|---|---:|---:|---|
| Sonnet recognition probes | 500 | 0 | None; all ten cells have 50 |
| Haiku initial coding | 28 | 1 | 21 undispatched batches and 10 unresolved items in the failed batch |
| OpenAI initial coding | 0 | 0 | 50 undispatched batches |
| Two-rater discussion | 0 | 0 | Not assembled; depends on complete initial ratings |

The 28 valid coding batches contain 280 initial labels from one rater. They are
not 280 dual-coded outcomes. Each canonical and alternative form still lacks a
complete second rating map; no cell can pass the frozen recognition gate.
The unchanged analysis requires both complete maps and retains unresolved
discussion outcomes as missing on the assigned denominator of 50.

As a descriptive spot check, the first saved response in each of the ten cells
explicitly names its intended benchmark family, including all five alternatives.
This raises concern that the structural analogues remain recognizable. It is
not a recognition-rate estimate or substitute for the required dual coding.
These probes assess familiarity with benchmark procedures; they do not test
ethical understanding, human-like behaviour, or good and bad outcomes.

## Exact failure

Slot `recognition_r1/coding/0/28` returned ten ratings with complete `end_turn`
termination. Its first ID was `4a33034c17c6a89c`; the frozen request expected
`4a33034c17c6a89a`. The other nine IDs matched in order. Offline parser replay
reproduced `ValueError: Missing, duplicate, reordered or extra coding IDs`.
The error was neither a timeout nor token truncation. The whole batch remains
failed under the frozen rule; even the nine matching rows were not silently
promoted to valid results. The original raw response and settlement are retained.

Failed record SHA256:
`953d184b61b0f17ef2bd74324fb4a758d6b2132a8ada92187a42f45cf275a60f`.

## Cost and integrity

| Accounting item | USD |
|---|---:|
| 500 probes | 5.337931500 |
| 28 successful coding calls | 0.112679600 |
| Failed coding call, full reservation retained | 0.031920900 |
| This screening attempt | **5.482532000** |
| All Phase 3 work to date | **5.898930950** |
| Claude total / remaining under $15 cap | 5.841321200 / 9.158678800 |
| OpenAI total / remaining under $30 cap | 0.057609750 / 29.942390250 |
| Package including Phase 2 / $100 cap | 28.805003975 / 100 |

These are conservative ledger estimates, not provider balances or invoices.
Unused room under the screening maximum is $8.584900500. It is not an automatic
retry allocation: the frozen release expressly excludes retries.

The independent local verifier checked exact requests, manifest links, successful
parser replay, all charges, frozen sources and historical evidence with zero new
API calls. There are 577 paid records in the ledger: 48 historical and 529 from
this attempt. No pending dispatch remains. The new archive contains 1,733 JSON
and JSONL members, each checked against the ledger, with CRC and SHA256 checks.
The previous 48-record archive and original scientific inputs remain unchanged.
See [CHECKPOINT.json](CHECKPOINT.json) and the separate
[500-probe checkpoint](PROBE_CHECKPOINT.json). Raw data and archives remain local
and excluded from Git; an off-device copy has not been verified.

Archive: `output/phase3_recognition_r1_20260913.zip`.
SHA256: `26793b9c3b25d9537eb4821eaaf2486ec3a094c839d591bd07d07d1603f4d03e`.
The 65 offline tests passed before the frozen collector launched; the new
verifier additionally passed against the actual stopped run. No frozen runtime
or classification rule was changed after observing the responses.

## Next step

Use the [continuation handoff](CONTINUATION.md). Preserve and reuse all 500 probes
and all 28 valid coding batches. Any recovery must be a separately designated,
tested continuation that retains the failed slot and its full charge. Do not
rerun the original collector, regenerate stimuli, or treat a missing second
rater as agreement. The current release cannot pay for replacement calls.

## Five-perspective review

Decision: retain the failure and incomplete status rather than repair a response ID.

- Linden: recognition of a familiar task is separate from ethical understanding;
  a screen failure or success would not establish the thesis's main claim.
- Osei: preserve the full visual/sequential probes and distinguish these model
  familiarity samples from human benchmark behaviour.
- Tanaka: one rater's partial map cannot determine the two-rater gate. Keep the
  denominator and missingness rules fixed.
- Renna: reuse the paid evidence; the ten coordinates, Beta distributions and R
  remain unchanged, and population work remains downstream.
- Okafor: the explicit ID makes the likely typo easy to diagnose, but silent
  repair would bypass the frozen parser. Require linked, tested recovery.

The tension is between inexpensive apparent clerical repair and strict item
identity. Resolution: keep the invalid batch intact and prepare transparent
recovery, with no new paid dispatch in this assessment. These are synthetic
review perspectives, not external reviewers or the two independent raters.
