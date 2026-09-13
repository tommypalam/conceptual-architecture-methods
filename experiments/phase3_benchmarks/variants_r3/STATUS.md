# Repaired candidates awaiting independent reading

Five separately generated candidates were repaired locally with full before/after
provenance in candidates.json. See REPAIRS.md. Original generated texts remain
unchanged. All 48 Phase 3 tests pass; generation replay made zero new calls.

Five exact canonical/repaired-pair review requests are frozen in review_manifest.json.
Maximum combined reservation **$0.2901162**, charged to Claude within its $15 cap.
Each call concerns one benchmark and requests a concise structural verdict.
This is neither a retry of the truncated consultation nor recognition collection.

Automatic approval review rejected the dispatch before process launch because it
requires specific user approval to send these newly created private protocol
pairs to Anthropic. It did not accept the earlier private-packet approval as
covering these new pairs. Explicit approval has been requested and is pending.
Do not bypass the rejection. Once approval arrives, run the SAME frozen requests:

    py -3.11 -B code/phase3_repaired_candidates.py run --yes

Load the existing Anthropic user-environment key into the process without printing
it. No review request/reservation/charge was created by the rejected invocation.
Current total Phase 3 conservative accounting is $0.38508195: $0.3274722 Claude
and $0.05760975 OpenAI. Remaining provider room is $14.6725278/$29.94239025.
Package accounting is $23.291154975, within $100. These are not billing balances.

The verified 43-call archive is output/phase3_candidates_20260913.zip, 130 JSON
members, SHA256 53a2456db88622b0ddb7f749a825b3e169465d386c77b7aa15aea2128df0bcec.
The original failed consultation remains preserved and fully charged. New data
belongs to the linked continuation. Off-device backup is not verified.
