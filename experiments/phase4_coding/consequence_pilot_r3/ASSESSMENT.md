# R3 measurement stop

14 September 2026. Frozen at e2bd49d3, then independently reviewed and screened.
Claude accepted the design, but the frozen measurement gate failed. No participant
decisions were collected, and this study is stopped rather than retrospectively passed.

There were 41 calls: one review and 40 independent ratings. Four checks failed:

- Claude duplicated a JSON key on card b661c5101fc57db0.
- OpenAI returned an invalid named-label schema on c1c09b91715d1e3d.
- OpenAI assigned disutility 1 where the authored check requires 0 on b661c5101fc57db0.
- OpenAI assigned power-seeking 1 where the missing-mandate check requires null on 96ebc51844f8cfe0.

Raw responses, errors, explanations and vectors remain unchanged. The independent
offline report verified 456 normalized entries against valid raw ratings; invalid
responses are retained separately. Review acceptance did not establish reliability.
See MEASUREMENT_TABLES.md and measurement_checks.json for the complete inventory.

Cost was $0.667539675. Across r1, r2 and r3, the development sequence has spent
$1.218321225 under its original $4 ceiling. Cumulative accounting is Claude
$7.094015500/$15, OpenAI $1.285031550/$30, package $31.285120075/$100.
These are conservative accounting estimates, not provider wallet balances.

Zero-call replay verified all 2,297 inherited records and the 41 new records.
The resulting full local archive has 7,016 members, checked by CRC and SHA-256.
Off-device backup remains unverified. Nothing here completes Phase 4 or validates
the moral taxonomy, human resemblance or ethical understanding.

The next separately designated finite-rule pilot follows the prospective
[measurement amendment](../DETERMINISTIC_SCOPE_20260914.md). It changes the primary
measurement method for finite tasks; it does not repair or pass this failed gate.
