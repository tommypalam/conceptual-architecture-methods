# Corrected context diagnostic verified; disclosure approval pending

Four offline tests passed, including saved-file request reconstruction, complete
mock collection and zero-call replay, paired/missing-data analysis, review stops,
and preserved transport failure/no retry. The full current freeze passed the
zero-network [prelaunch checkpoint](PRELAUNCH_CHECKPOINT.json); all 660 inherited
records and the previous archive remain intact. No paid call or charge occurred.

Automatic approval review blocked the original launch pending specific approval
of protocol/synthetic payload disclosure to Anthropic and OpenAI. That restriction
still applies. See [DISCLOSURE.md](DISCLOSURE.md) and exact [requests](requests.json).
No collector is running. Do not bypass the block or regenerate this package.

Schedule: one Sonnet 4.6 review, then only if accepted, 576 GPT-5.4 mini decisions:
24 profiles/replicate blocks, both justice contexts, E/U and six roles/offers.
Population seed 2026091313, schedule 2026091314 plus block ID, analysis 2026091315.
Maximum new conservative accounting $4.200345600 under the $4.30 local ceiling
and existing provider/package caps. Formal Phase 3 gates remain open.

Release SHA-256: `96abf1505662916c36f960ec34f263df29ce43fabffc90f473f2a7e18f180c91`.
The first no-spend freeze is retained in [revision 1](../context_diagnostic_r1/STATUS.md).
This revision changes reviewer serialization, adds its correction note and tests,
and uses new source/slot IDs. Participant texts and the scientific design are unchanged.

After specific approval run `py -3.11 -B code/phase3_context_diagnostic_r2.py run --yes`.
Do not repeat unchanged preparation or tests. After completion, verify with
`py -3.11 -B code/phase3_context_diagnostic_r2.py verify`.
