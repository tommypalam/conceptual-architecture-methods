# crossmodel_recognition_r1: stopped on a mis-sized request

**Outcome: stopped on the first probe. 961 records, one failed slot preserved at
full reservation.** 15 September 2026. Superseded by the exploratory pilots
[crossmodel_pilot_r1](../crossmodel_pilot_r1/ASSESSMENT.md) and
[crossmodel_pilot_asch_r1](../crossmodel_pilot_asch_r1/ASSESSMENT.md), which
measured what this attempt assumed.

| Item | Value |
|---|---|
| Failed slot | `crossmodel_recognition_r1/probe/asch/alternative/claude-haiku-4-5-20251001/9` |
| Cost of the failed call | $0.116619800 |
| Probes completed | 0 |

## Cause: two errors in request construction, both mine

1. **Stimuli were JSON-dumped into a single string** instead of passed as
   content blocks, which is what the frozen `probe_request` in
   `phase3_recognition.py` does. Asch carries 18 image blocks, so serialising
   them as JSON text produced a request of **81,266 input tokens**.
2. **`max_tokens` was 128**, inherited from the frozen screen whose answers were
   capped at 35 words. These models write longer, the answer was truncated at
   `max_tokens`, and the truncated text failed validation.

The model's behaviour was not at fault. The write-once and no-retry rules
behaved exactly as specified: the failed slot and its full charge are retained
and are inherited by name in the pilots that followed.

## What the pilots then established

Passed correctly as content blocks, probes cost **$0.00156-$0.00363** each on
text-only families and **$0.00530** on Asch, roughly five times cheaper than the
estimate this attempt was sized against. All 36 pilot probes succeeded.

A real cross-model study is therefore affordable, but two repairs are required
first: the OpenAI request path must carry Asch's images rather than flattening
content to text, and `max_tokens` must be raised. Neither is a limitation to
disclose; both are defects to fix.

## Scope

No recognition rate was estimated and no cross-model claim was made or is
implied by this designation.
