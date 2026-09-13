# Consequential pilot r1: measurement gate failed

13 September 2026 · Prelaunch freeze `fe2a44bc` · No participant collection

## Outcome

The independent Claude design review accepted the protocol, but the subsequent
measurement screen failed its prospective gate. All 32 coding responses were
collected; **zero participant decisions were collected**. This is evidence about
the rating interface and its limitations, not evidence about agent moral behavior.

There were 13 recorded check failures: seven OpenAI schema failures, five OpenAI
diagnostic failures and one Claude diagnostic failure. The seven schema-invalid
ratings were not evaluated further against the diagnostic criteria; the counts
therefore do not establish that all other semantic content was correct.

| Failure | Count | Meaning |
|---|---:|---|
| OpenAI known numeric values accompanied by an unknown_reason | 7 ratings | Invalid under the frozen schema; no automatic cleanup |
| OpenAI fixed harm code contradicts recorded negative third-party deltas | 4 ratings | Required factual check failed |
| OpenAI ethical-violation code on threat-backed participation | 1 rating | Failed authored development check |
| Claude appropriate-authority code when mandate is unknown | 1 rating | Returned 0 where the diagnostic required null |

The review's acceptance did not predict measurement success. It was methodological
screening, not validation. The gate prevented collecting decisions on an unaccepted
measurement pipeline, and no threshold was lowered after inspection.

## Diagnosis from retained evidence

For OpenAI's `disclosure_2/falsify`, the harm-avoidance explanation states that
negative third-party credits violate the fixed standard, while the separate
fixed-standard vector places 1 in that category. In the threat check its explanation
identifies a consent-rule breach while the ethical-violation vector contains 0.
These are observable representation inconsistencies; explanations are not used
to overwrite the original numeric labels or retrospectively pass the screen.

The Claude uncertainty failure concerns a different boundary: its explanation
says a legitimate mandate cannot be confirmed, but it outputs 0 for appropriate
authority use. The protocol required unresolved legitimacy to remain unknown.
This calls for explicit missing-fact logic as well as an output-interface repair.
Correct-looking prose alone is not reliable structured scoring or moral understanding.

## Prospective next step

The separately designated [r2](../consequence_pilot_r2/PROTOCOL.md) replaces duplicated
vectors and evidence entries with one named label adjacent to each category's
evidence. Deterministic normalization retains the same numeric vector meanings.
It clarifies when a missing fact is decisive and uses different diagnostic cases.
The participant scenarios and moral standards remain the same; no participant
response existed when this change was selected. This is adaptive development, not
fresh confirmation or external validation. R1 ratings remain unchanged and unpooled.

Five synthetic perspectives reviewed this decision: Linden rejects repairing old
labels from favorable explanations; Osei separates interface accuracy from moral
validity; Tanaka retains the failed gate and budget history; Renna removes duplicate
judgment representations; Okafor requires a new freeze and successful replay before
dispatch. Resolution: prepare r2 within the same $4 development ceiling, carrying
forward r1's actual cost. These are internal review roles, not external approval.

## Accounting and integrity

- Calls: 1 review + 32 ratings = 33; participant calls = 0.
- Review cost: $0.032584200.
- All Claude charges this round: $0.432933600; OpenAI: $0.079495350.
- Total accounted cost: **$0.512428950**, against a $2.049750450 reservation.
- Cumulative Claude: $6.489798700/$15; OpenAI: $1.183356075/$30.
- Cumulative package: $30.579227800/$100. Accounting estimates are not balances.
- Zero-call replay preserved all 2,263 prior records. The ledger now contains
  2,296 paid records, and all 6,890 archive members passed CRC and SHA-256 checks.

[Results](results.json), [ratings](ratings.json), [measurement checks](measurement_checks.json),
[checkpoint](CHECKPOINT.json) and [report checks](REPORT_CHECKS.json) preserve the
outcome and accounting. Raw outputs are locally archived and excluded from Git;
off-device backup remains unverified. No human raters were required or used.
