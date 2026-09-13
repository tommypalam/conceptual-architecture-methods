# Pilot stopped at structural review; recognition not tested

The approved pilot made two calls: GPT-5.4 mini generated a scenario and Sonnet4.6
reviewed it. The review requested revision. No recognition or coding calls ran.
This candidate therefore has no recognition-rate estimate and was not evaluated
against either the exploratory N5 rule or the formal N50 gate.

The candidate used anonymous strangers dividing100 equal-value research tokens.
Its final sentence mixed the experimental schedule into participant-facing text:
it stated six isolated conversations, then described proposer/responder shares
of10,20,30,40 and50 without clearly separating one unrestricted proposer task
from five fixed-offer responder tasks. Claude flagged that ambiguity as a blocking
count mismatch. The intended engine schedule is indeed one proposer task plus
five responder tasks, not six share pairs or five restricted proposer offers.

This is a wording/role-schedule defect, not evidence against the intended allocation
mechanism. Our local assessment also finds that the neutral research-token setting
offers little distance from a textbook allocation task. Fixing the schedule alone
would not establish low recognition. No paid iteration follows automatically.

## Execution and evidence

The review contained a complete JSON object inside a Markdown code fence. The
frozen runner accepted its raw text/model/usage but its downstream JSON reader
stopped before interpreting the verdict. The raw response was not overwritten.
An independent offline audit removed only that complete fence in derived data,
validated the unchanged JSON against the original schema, and recovered `revise`.
That disposition requires stopping under the frozen protocol regardless of the
formatting issue. No model call was repeated and no acceptance was substituted.

This is an audited stopped run, not a claim that the original runner completed
successfully. The frozen runtime and original manifests remain unchanged. The
derived disposition, exact review, candidate and record hashes are in
[STOP_CHECKPOINT.json](STOP_CHECKPOINT.json). Use
`py -3.11 -B code/verify_phase3_design_pilot_stop.py` for its zero-call audit;
the original full-pipeline verifier still encounters the preserved JSON fence.

| Accounting item | USD |
|---|---:|
| Generation | 0.000954525 |
| Structural review | 0.003405600 |
| **This pilot** | **0.004360125** |
| Maximum authorised pilot reservation | 0.425814400 |
| Claude cumulative total / remaining under $15 cap | 5.952994300 / 9.047005700 |
| OpenAI cumulative total / remaining under $30 cap | 0.154957275 / 29.845042725 |
| All Phase3 accounting | 6.107951575 |
| Package including Phase2 / $100 cap | 29.014024600 / 100 |

These are conservative estimates, not provider balances. The pilot cost less
than half a US cent. The earlier full recognition screen remains $5.687192500;
its five alternative rejections are unchanged and not pooled with this pilot.

The local audit checked exact request/manifest links, model/parser/cost replay,
all650 inherited records and the prior archive. The new ledger contains652 paid
records. All1,958 JSON/JSONL archive members passed byte/hash and CRC checks.
No additional API calls were made during verification. The fence-extraction
tests cover surrounding prose, incomplete JSON and semantic-schema rejection.

Archive: `output/phase3_design_pilot_r1_stopped_20260913.zip`.
SHA256: `8c5ecd80447e25b7b355d05406d24e87d2b8f5959f0645a25e0da2dbbfd55e24`.
Raw records and archives remain local and excluded from Git. Off-device backup
is unverified. The earlier approval block was resolved; none is pending here.

## Next design work

The [offline repair proposal](REPAIR_PROPOSAL.md) separates participant wording
from the engine's six-conversation schedule. It is not an independently reviewed
replacement and cannot be used as an accepted candidate. Before another paid
candidate round, strengthen the drafting contract so it clearly distinguishes
participant instructions, role-specific prompts and engine-only scheduling.
Also require a genuinely specified new setting rather than substituting tokens
for money. Preserve the allocation mechanism and disclose changed stakes.

Do not rerun the generated candidate merely to resume. Under this approved pilot,
a structural revision ends the round. A future revision needs a new designation
and independent review before recognition. Population remains gated; neither
ethical understanding, human resemblance nor moral quality was tested here.

## Five-perspective review

Linden distinguishes a wording defect from the thesis's substantive claims.
Osei requires separate role instructions and a clearly defined participant setting.
Tanaka records zero recognition observations rather than imputing a failure rate.
Renna retains all five benchmarks and all ten LPM coordinates unchanged. Okafor
preserves the fenced response, audits it without repeat spending, and fixes the
next drafting contract prospectively. The tension is whether to treat the count
issue as easily inferable; resolution is to require explicit role scheduling and
respect the independent revise verdict. These are synthetic perspectives, not
external experts or additional model reviews.
