# Continue only the undelivered portion of the approved allocation

The parent run stopped on one `TimeoutError` after 339 attempt slots:
338 valid responses and one preserved failed attempt. No unresolved dispatch
intent lacks a local record. This is a transport interruption, not credit
exhaustion or an outcome-based stop.

The original 720-call allocation and $4.50 cap were explicitly approved.
This linked designation copies all 339 response and dispatch records byte for
byte, including the timeout. It sends only the **381 previously unsent**
requests in their original schedule, using their exact original messages,
seeds, model, temperature and output cap. No failed slot is retried and no
721st attempt is authorised. The parent's files and partial ZIP remain intact.

A separate continuation executor is pinned by hash in `continuation.json`.
The frozen experimental code and design are unchanged. The operational
exception permits manual continuation after the diagnosed timeout; it does
not change the original rule that an API failure invalidates the screen.
The combined analysis therefore remains `INVALID_SCREEN` if the remaining
requests succeed. This is explicitly diagnostic data, not a clean confirmation
or battery pass. Exact contrast envelopes retain the unknown timeout outcome.

All old reservations remain charged against the original cap. Known token
usage is reported separately from the timeout's unknown charge, conservatively
bounded by its full dispatch reservation. Any new failure or unresolved intent
stops continuation. No automatic retry or expansion follows.

Two tests cover a complete 381-request mock continuation and a second-failure
stop, verifying that the parent timeout is never resent or edited. The parent
study's primary/secondary questions, reporting limits and Phase 2 hold remain.
