# Provider budget amendment, 2026-09-13

User instruction: "i have 15 bucks on claude so 15 dollar budget for claude and
30 for chatgpt". Interpret these as separate hard ceilings for the current
Phase 3 work, replacing the previous combined $30 nightly ceiling. Carry forward
existing Phase 3 charges rather than treating the amounts as additional credit.
Here ChatGPT means OpenAI API spending used by the study. These are user-reported
budgets, not balances verified through provider billing interfaces.

| Provider | Hard cap | Already accounted | Remaining accounting room |
|---|---:|---:|---:|
| Anthropic / Claude | $15.00 | $0.3274722 | $14.6725278 |
| OpenAI | $30.00 | $0.010098 | $29.989902 |
| Combined | $45.00 | $0.3375702 | $44.6624298 |

The existing $100 package ceiling still applies. Carried-forward Phase 2 cost
is $22.906073025; current package accounting is $23.243643225. Earlier Phase 2
spend is not charged again against these new Phase 3 provider ceilings.
No borrowing between provider allocations. Budgets are ceilings, not targets.

The truncated Claude consultation retains its full $0.248127 reservation.
This amendment neither clears that failure nor authorises a retry. The original
ledger, policy and frozen collectors remain unchanged. Before any later paid
continuation, bind these provider caps into a separately verified collector and
record the failure reconciliation without replacing the old records. Do not use
an independent ledger to restart spending at zero.

`code/phase3_provider_budget.py` audits the existing ledger and provides read-only
provider accounting plus prospective whole-batch cap checks. It makes no API
calls and cannot dispatch. The initial validation allocation ($10 total, with
$1 generation/$2 structural review/$7 recognition) is still a stage limit;
larger provider ceilings do not silently allocate additional money to a stage.
No new model, sample count, recognition schedule or population run is released.

Verification: three offline tests passed, covering separate provider caps,
carried-forward charges, unknown models, inconsistent totals and whole-batch
stage limits. Live read-only ledger accounting agrees with the amounts above;
zero API calls were made. The existing consultation failure remains visible.

Synthetic perspectives: Linden keeps the research claims unchanged; Osei keeps
validation gates intact; Tanaka requires cumulative accounting across providers;
Renna preserves the historical budget/provenance chain; Okafor separates funding
availability from executable release. Resolution: accept the user's provider
ceilings, retain previous charges and test cap enforcement. These are written
perspectives, not independent expert review.
