# Dispatch blocked pending exact approval

2026-09-12. Runner/protocol/preview committed in7ba71943; three tests passed.
Automatic approval review rejected the attempted process launch before execution.
Reason: sending private research prompts and historical-seed-derived requests
to OpenAI requires explicit authorisation of this exact40-call payload and
destination; general continued-probing authority was not accepted as sufficient.

No process launched, API call sent, dispatch intent written or record created.
Prior source calls remain intact. Expected full reservation$0.2562; hard cap$0.30.
The existing dispatch_authorization.json records the general authority basis
used for the rejected attempt, not a subsequent exact approval.

An exact approval question is pending: send request_preview.json's40 frozen
GPT-5.4 mini research requests to OpenAI within a$0.30 cap, or stay offline.
Do not launch until exact approval arrives. No workaround or indirect dispatch.
Remaining tracked allowance$3.79170675; no new spending from this probe.

## Resolution

Researcher replied "approved" to the exact40-call OpenAI/$0.30 approval request.
The prior block is resolved by this explicit approval; launch may proceed within
the frozen scope. Approval recorded in dispatch_authorization.json.

## Completed

40/40 approved calls completed with valid responses for$0.0452325. No pending
requests; source-paired verification and raw ZIP checks passed. See
[interpretation](analysis/INTERPRETATION.md). No further run allocated.
