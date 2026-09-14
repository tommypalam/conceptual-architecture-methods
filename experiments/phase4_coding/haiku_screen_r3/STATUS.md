# haiku_screen_r3 — stopped after its review; re-designated as r4

**One review call, completed, $0.003896200. Zero screen probes.**
16 September 2026.

## What r3 achieved

**The dispatcher fix worked.** r1 and r2 both died on the review call — each
having fixed one half of a two-part routing problem. r3's review call completed,
parsed and charged cleanly. That failure mode is closed.

## Why r3 stopped

Two defects in r3's own collector, both in reading the response rather than
obtaining it:

1. **Verdict key.** Haiku returned `overall_verdict`; `_shape` looked only for
   `verdict`. The prompt asked for "an overall verdict", so the key the model
   chose was a reasonable reading of the instruction. My wording invited it.
2. **Advisory rule not applied.** The collector stopped on `verdict != accept`,
   but under the 16 September amendment a review of already-accepted material is
   advisory, not a gate.

Correcting either means editing a collector whose hash is pinned by r3's own
release. `verify()` refused the edit, correctly. The write-once rule forbids
overwriting a frozen artifact, so the correction goes in a new designation.

## The review verdict is preserved and NOT re-run

r3's review returned **`reject`** with six blocking issues and two limits. It is
recorded in the ledger exactly as returned and is read from there by r4.

**The review is not re-dispatched.** Re-running a review to obtain a different
verdict is forbidden and has not occurred. r4 changes no task, threshold,
estimand or gate; it changes only the reading of a response already paid for.

## Accounting

One completed call, $0.003896200, charged and settled. Nothing pending, nothing
failed. Ledger after r3: Claude $12.276727100/$32, OpenAI $4.251449400/$30.
Usage estimates, not wallet balances.
