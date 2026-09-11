# S3 evidence grounding: fixed development screen

Prepared before dispatch, 2026-09-11. This is a separate exploratory condition,
not a Phase 0 rerun, holdout, Phase 1.5 pass test or tool-injection experiment.

## Authority and cost

The researcher authorised exploration within Phase 0a/0b/0c boundaries, then
said: "lets go spend some money, I have 9 dollars though, so lets try and keep
it at that". This supersedes the earlier OpenAI spending stop for this work.
It is broad exploration/dispatch authority, not a claimed separate human
signature on every message. The prepared evidence wording was assessed against
the theory and locked source in the candidate review; no new theoretical
meaning, ethical scoring, dilemma facts or parameter mapping is introduced.

Allocate **$3 maximum** to this screen from the **$9 total new ceiling**.
All 450 calls reserve **$2.867265** using UTF-8 input bytes plus 512 framing
tokens and the full 600-token output allowance, without cache discounts.
This reservation is deliberately conservative, not an expected invoice.
Published rates: $0.75 input / $4.50 output per million tokens, checked against
[official model documentation](https://developers.openai.com/api/docs/models/gpt-5.4-mini)
on September 11. Actual provider billing remains authoritative. The local
ledger reports full-rate token estimates, which may exceed cached-input billing.
No other study runs concurrently; at least $6 is unallocated to this screen.

## Fixed design

GPT `gpt-5.4-mini-2026-03-17`, Chat Completions, temperature 1, maximum completion
tokens 600, schedule seed **20260915**. Independent single-decision calls, not a
sample of 450 distinct profiles. Each profile condition fixes PD=.8 and the
other nine parameters at their original source values in the neutral context.

**450 calls: 3 arms x 5 input conditions x 30 repeats.** Arms:

1. Original: the exact previously approved baseline messages.
2. Repetition: original messages plus the complete source reference, numbered
   E1-E6 in original order, without the grounding instruction.
3. Grounding: the same repetition plus the exact instruction in
   [the prepared candidate](../evidence_candidate_20260911/S3_OVERLAY_DRAFT.txt).

Four input conditions retain the distinct canonical/P1/P2/P3 profile system
messages. The fifth, **no_profile**, supplies no system message or parameter
profile. All fifteen complete messages are in [request_preview.json](request_preview.json)
and are pinned by [manifest.json](manifest.json). Source hashes are rechecked
before dispatch. No original file is edited, and no old response is pooled.

The addition goes after the unchanged dilemma body and before the unchanged
DECISION/REASONING output instruction. It is identical across profile wordings.
The no-profile conditions retain the same user message and response schema,
including its existing phrase "grounded in your profile and context", but supply
no profile. This is a matched no-supplied-profile control across overlay arms,
not the naked Phase 0c condition or a claim of completely unframed reasoning.
Removing the system message also removes normative context and agent framing;
profile-vs-no-profile differences cannot be attributed purely to parameter
values. Within-no-profile arm comparisons isolate the added-context contrast
under this fixed schema. No-profile neutrality cannot be established at this N.

Randomise each complete 15-cell block, collect 30 blocks, concurrency 3.
Unique requested per-call seeds are deterministic from arm/wording/index;
they do not guarantee independent or reproducible provider sampling. No outcome
inspection changes allocation or causes a favourable subset to expand.

## Stopping and preservation

One HTTP attempt per planned slot; SDK retries, seed fallback and token-parameter
fallback are disabled. Save a durable cost reservation before dispatch. Stop
after the active batch on an API/model/provenance/usage error. A crash with a
reservation but no response blocks automatic resume, avoiding a duplicate paid
request. Failures stay in the sample; no retries in place or replacements.

The $3 guard counts conservative reservations, not just successful reported
usage. Unreported billing on a failed request therefore does not become free
budget. Raw responses, IDs, seeds, exact messages, usage and hashes remain
write-once in local records. A checksum-indexed ZIP is verified byte-for-byte;
it is a same-computer backup, not remote protection. No publication is performed.

## Analysis frozen before collection

**Primary:** grounding-arm P2-minus-P3 ADOPT-rate difference. Two exact 97.5%
binomial intervals produce a conservative >=95% difference interval. Include
invalid/missing decisions through the full unknown-assignment envelope. A
complete, quality-eligible interval wholly outside [-.10, .10] detects a gross
remaining wording failure. Each cell must have >=98% valid responses (at N=30,
all 30) for the screen's quality condition. Saturation of all four profile
wordings at <=5% or >=95% makes the screen uninformative, not successful.

**Secondary, exploratory:** the other arms' P2/P3 gaps, differences between
those gaps, and grounding/original/repetition contrasts in the no-profile
conditions. Each reported contrast has a conservative >=95% interval using
Bonferroni across its contributing cells. These intervals are **not adjusted
across the family of secondary contrasts**. No multiplicity-controlled discovery
or mechanism identification is claimed. Other canonical/P1 rates are descriptive.

A reduced point gap or failure to reject at this N is not equivalence or a repair.
This screen has limited precision and cannot prove preserved parameter response:
it uses one profile on known S3 and does not replace prespecified PD/S1 gradients.
Fresh confirmation and the actual validity battery remain necessary for a
selected candidate. The prior Phase 0c naked baseline is not transplanted here.
The optional evidence tool is not registered or used; all calls remain ordinary
single-decision prompt delivery. Claude is not used for experimental decisions.

## Commands

```text
python -m pytest tests/test_validity_evidence_screen.py tests/test_research_evidence.py -q
python code/run_validity_evidence_screen.py --run-root experiments/phase1_5_encoding_validity/evidence_screen_20260911 --prepare-only
python code/run_validity_evidence_screen.py --run-root experiments/phase1_5_encoding_validity/evidence_screen_20260911 --yes
```

Credentials are supplied outside the repository. Preparation and tests make no
network requests. The final command spends within the frozen screen allocation.
