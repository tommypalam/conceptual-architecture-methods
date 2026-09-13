# Current status: all probes saved; coding stopped

The paid-disclosure approval was received and collection ran. All 500 probes
completed; 28 initial coding batches are valid and one failed on a changed item
ID. No retry occurred. OpenAI coding and discussion have not started, so there
is no formal recognition verdict. Phase 3 remains open.

See the [verified assessment](execution/ASSESSMENT.md),
[checkpoint](execution/CHECKPOINT.json) and [continuation handoff](execution/CONTINUATION.md).
This attempt used $5.482532000 conservatively. All evidence is locally archived;
verification made zero API calls. No collector is running or paid call queued.

## Earlier quotation checkpoint (superseded by execution status above)

# Quotation complete; paid screening not released

Current result: [ten completed free quotes and full cost assessment](QUOTATION_OUTCOME.md).
The disclosure approval was received and the exact approved token-count requests
succeeded. The full prospective bound is $14.06743250, including a bounded
same-two-rater discussion. It fits the $15 Claude/$30 OpenAI caps but exceeds the
original $7 screening/$10 validation allocations. No paid call or charge occurred.
The earlier third-AI-only adjudication proposal is superseded by the discussion
procedure in QUOTATION_OUTCOME.md. Paid runtime and allocation remain unreleased.

## Earlier preparation checkpoint (historical, superseded above)

2026-09-13, branch `phase3-preparation-20260913`. The researcher instructed
proceed after the five structural accepts. Preparation is complete for the ten
exact recognition inputs in [requests.json](requests.json). No recognition,
classification, population or token-count call has been dispatched in this stage.

All **54 Phase 3 tests passed**: the earlier 48 plus six new assembly/blinding
tests. These verify all 1,200 escalation states, all 216 perception turns and
36 original images, all 720 initial-ranking/branch combinations, isolated
allocation roles/offers and helping conditions. Historical scientific inputs,
all 48 existing API records and their local archive remain unchanged. See
[the assembly review](ASSEMBLY_REVIEW.md) and [protocol](PROTOCOL.md).

The planned workload is 500 Sonnet4.6 recognition outputs and 100 coding calls
(50 Haiku4.5 and 50 GPT-5.4 mini; ten independently labelled answers per call).
Coding alone has a conservative maximum of **$2.83531875**: $1.596045 Claude and
$1.23927375 OpenAI. This includes maximum valid answer length, JSON escaping,
framing and output limits. The complete screening bound is not yet established;
no paid collector is released or implemented by this preparation module.

Automatic approval review rejected the token-count command before process launch.
Its stated reason: the full private recognition bundles and 36 images are an
expanded payload for Anthropic's external token-counting endpoint, beyond the
earlier structural-pair approval. The command would make ten free token-count
requests, not generate research responses. No quote file or charge was created.
Do not bypass this rejection through another command, endpoint or provider.

After explicit approval of this disclosure, run the same frozen quote command:

    py -3.11 -B code/phase3_recognition.py quote

Load the existing Anthropic user-environment key into the process without
printing it. Then run `py -3.11 -B code/phase3_recognition.py plan` for the full
bound. Quotations are saved once and reused, not repeated on resume. If the bound
exceeds the $7 recognition allocation, do not start a partial screen or reset the
ledger. Resolve allocation against the existing provider/package caps first.

After costing, implement and offline-test the linked paid collector, parsers,
coding-order manifest, fixed-denominator analysis and adjudication records, then
freeze its exact runtime and release. Parser/runtime checks must enforce the
16-hex-character opaque coding IDs used in the input bound, prohibit non-whitespace
ASCII control characters, preserve invalid outputs and every original rating,
and reject missing/duplicate/changed slots before any network action. The proposed
local third-AI adjudicator differs from discussion between the two original
raters in spec section7.3. Before paid release, resolve that prospective design:
implement and cost the original two-rater discussion, or obtain an explicit
amendment. The current cost planner covers initial coding only; it is not a full
specification-compliant dispute-resolution quote. Neither approach constitutes
Phase 4 human gold review. No population release follows from preparation or quotation.

Current spending is unchanged: Phase 3 **$0.41639895**; Claude **$0.3587892**,
OpenAI **$0.05760975**; package **$23.322471975**. Remaining provider accounting
room is $14.6412108/$29.94239025. These are estimates, not verified balances.
