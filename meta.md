# PARIA decision log

Current decisions are recorded here; [NEXT_STEPS.md](NEXT_STEPS.md) owns execution
status. The [earlier log](docs/archive/meta_through_2026-09-06.md) is preserved
byte-for-byte, including its original encoding defects and historical templates.

## 2026-09-09 — Completed independent audit and interpretation

The effective r3 audit has 200 valid records and 2,000 estimates (two legitimate
abstentions retained as incorrect for accuracy). All 173 reused r2 records were
byte-preserved; r3 collected 27 new responses with the identical frozen design.
The malformed r2 response is preserved separately inside the final local backup.
Together with the older strict-format attempt there were 202 unique paid audit
attempts, approximately $0.435918 at Haiku's $1/$5 token rates.

Model: claude-haiku-4-5-20251001; neutral context; sampling seed 20260604. Literal
thresholds are met: seven parameters exceed .35 with binomial p<.05 against .25;
six reach .50. However, all aggregate accuracies fall below their 92–94% empirical
majority baselines. None of the ten active-parameter permutation tests reaches
p<.05 (1,999 resamples, unadjusted). Active strata contain only 20 observations
per trait. No claim of established recoverability or overall phase pass follows.
The complete table reports Wilson confidence intervals and both accuracy views.

Synthetic review: Linden separates literal thresholds from the conceptual claim;
Osei notes the missing evidence of manipulated-trait recovery; Tanaka emphasises
class imbalance and low active-stratum precision; Renna rejects treating audit
completion as phase closure; Okafor confirms traceable records and backups.
Resolution: audit collection/scoring complete, scientific result mixed and not
sufficient to establish validity; remaining battery decisions stay open.

The prompt requested at most 15 commentary words; observed median 21, maximum
66, with 186/200 above the requested limit. This limitation is disclosed and did
not cause response selection. The report and all 200 records have a checksum
inventory and verified local ZIP backup. Two new offline audit-format/resume
tests passed; frozen source sweep and original audit modules remain unchanged.

## 2026-09-09 — Brief-audit malformed-response continuation

Brief audit r2 stopped at item 174: the response supplied null for both ID quartile
and confidence, although the frozen schema requires numeric confidence even for
abstention. The preceding 173 records parsed successfully. No scoring results
were inspected to select reuse. A linked r3 designation copies all 173 valid
records byte-for-byte and retains r2's malformed attempt in place, with its hash
and reason recorded in a continuation ledger. The remaining schedule contains
27 calls: a new attempt for that malformed item and 26 undispatched items.
The prompt, model, blind pack, confidence schema, token cap and scoring remain
identical. This is operational recovery within the authorised 200-item audit,
not a theoretical departure or a relaxed parser. Both failed attempt and final
effective observation counts must be disclosed in the completed report.

## 2026-09-09 — User-approved concise audit format

The user explicitly authorised completing the Claude audit with extra commentary
allowed, while instructing Claude to use as few words as possible without losing
explanatory ability. A separate CLI now requests compact estimates JSON followed
by at most one 15-word explanatory sentence. It accepts trailing prose and stores
it unchanged, recording word count separately; verbosity never selects outcomes.
Invalid quartiles/confidence, duplicate JSON keys and multiple structured answers
are still rejected. The original frozen audit/scoring modules remain unchanged.

New designation: `claude_audit_20260909_brief_r2`. The same 200-item blind pack,
Claude snapshot, temperature, token cap and analysis are retained. All 200 items
receive the revised prompt; the one earlier failed-format response remains in
its original designation and is not pooled. No private answer key is sent.
Two offline tests passed, covering commentary handling, ambiguity/schema rejection,
blinding, checkpoint resumption and exactly-once item collection.

Synthetic review: Linden retains evidence-based interpretation and abstention;
Osei requires identical item selection across the revision; Tanaka separates
format compliance from statistical inclusion; Renna discloses the prompt revision;
Okafor preserves original failures and tests resume behaviour. Resolution: apply
the user's approved operational format change in a new designation and score the
complete new audit without changing the scientific thresholds.

## 2026-09-09 — Background collection completed; audit format stop

On the user's return, verified committed-format checksum inventories and local
backup manifests: source 15,000 records, all valid; rotations 4,500 records,
4,498 valid parses and two parse failures; no API failures in either run.
Both same-computer ZIP archives exist. Recorded token usage gives $13.380867 for
the source and $4.5390015 for rotations at standard rates, $17.9198685 combined.
The supervisor exited at 13:50:09 UTC after rotations finished because the
independent audit's first response failed strict parsing. Haiku returned its
ten estimates in a fenced JSON object followed by prose, triggering Extra data.
This was a format failure, not a credential or quota error. The one audit record
is preserved and 199 items remain undispatched. No parser/prompt/model change or
new audit designation has been made; consultation is required under the user's
new-departure rule. Phase 1.5 remains open, with paraphrases also pending.

## 2026-09-09 — Constraints and consultation clarified

The user clarified that earlier departures from the original theory were made
for necessary binding constraints and remain accepted. The theory should still
guide review, read together with documented operational amendments. A new
departure requires a concrete physical or technical limitation and consultation
with the user before implementation; theoretical fidelity is not relaxed for
convenience. Record the evidence, minimal proposed workaround and consequences.
This rule is now in both project constitutions. It does not reverse historical
phase closures or authorise changing the running frozen sweep. The first Claude
candidates' semantic drift has no demonstrated physical necessity. No new
departure is approved by this clarification, and disclosure approval for the
prepared theory-containing Anthropic request remains pending.

## 2026-09-09 — User-authorised fresh Phase 1.5 restart

After reviewing recovery dependencies and API cost estimates, the user explicitly
requested a complete restart and delegated selection of a Claude model similar
to GPT-5.4 mini. The new source designation is `option_c_20260909_restart`;
all 15,000 slots will be newly collected, with no reuse or pooling of the earlier
sample. Historical evidence and the unused shard preparation remain provenance.
This supersedes the continuation plan as the active execution path.

Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) is selected for independent
paraphrase generation and blind audit. Official provider documentation positions
it as the lightweight high-throughput model, with $1/$5 per million input/output
tokens, close to GPT-5.4 mini's $0.75/$4.50 tier. This is an approximate capability
tier match, not demonstrated equal research-task performance. No behavioural
model substitution is made. Sources: https://platform.claude.com/docs/en/models/overview
and https://developers.openai.com/api/docs/models/gpt-5.4-mini.

Synthetic review: Linden rejects claiming model equivalence from pricing; Osei
requires a fresh designation with unchanged prompts and allocation; Tanaka keeps
all new outcomes and discloses the restart, without pooling historical data;
Renna retains the independent-coder limitation and human semantic-review gate;
Okafor requires an operational checkpoint before sustained dispatch. Resolution:
fresh fixed-N sweep, pinned Claude snapshot, then the 200-item audit and 9,000
robustness calls; no optional 15,000-call gradient extension automatically added.
Both model IDs were accessible. The ten-call OpenAI checkpoint passed all parsing
and model checks (8,959 input and 499 output tokens); the fresh sweep then started.
Claude returned three candidates but violated literal labels. Mechanical label
restoration produced structurally valid candidates; the user's requested theory
comparison then found semantic drift and rejected all three for behavioural use.
See [semantic review](docs/phase1_5_paraphrase_review_20260909.md). A new generation
will vary endpoint descriptions only, holding all other template text literal,
before any paraphrase behavioural calls. Human sign-off remains pending.

The background follow-up supervisor (PID 5336 at launch) queues rotations and
blind coding after complete source verification, then checks recorded human
paraphrase approvals before further dispatch. It creates checksum inventories
and same-computer ZIP backups. Three restart-tool tests passed in addition to
the 19 baseline and four continuation tests. At a subsequent checkpoint all
1,795 newly collected responses were valid, with approximately $1.60 token cost.

Automatic approval review rejected the new theory-grounded generation request
because sending private thesis text and derived feedback to Anthropic required
explicit disclosure approval. The request is frozen locally and was not sent;
the user has been asked for that specific permission. Other authorised work
continues. See [restart operations](docs/phase1_5_restart_20260909.md).

## 2026-09-09 — Cross-computer continuation preparation

The user requested completion of Phase 1.5, confirmed original responses remain
on another computer, and authorised collecting remaining slots here for a later
merge. Neither provider key is configured yet. A separate tested wrapper now
supports full-source recovery and inventory-only sharding, without modifying the
frozen scientific runner. The prepared September 9 shard schedules 6,360 new
slots; the unidentified original failed slot awaits payload recovery.

Synthetic review: Linden requires honest separation of absent and observed data;
Osei supports the fixed allocation without outcome selection; Tanaka requires
disjoint keys and verified pooling; Renna flags the collection gap and dependent
audit prerequisites; Okafor requires fail-stop execution and local backup.
Resolution: preserve the full target and snapshot, reserve every inventoried key,
collect only never-dispatched slots, and withhold pooled claims until recovery.
All 19 existing tests and four new continuation tests passed. No paid calls or
merge occurred. See [continuation instructions](docs/phase1_5_continuation.md).

## 2026-09-07 — Sample recovery handoff

The user asked whether topping up credits permits retaining the interrupted
sample, requested a Markdown handoff, and authorised pushing all changes including
the abstract. The handoff distinguishes 8,639 reusable valid responses from the
one failed attempt: completing the fixed design needs 6,361 further successful
responses, not a fresh 15,000-call experiment. This is a proposed continuation,
not an implemented or executed resume command.

Synthetic review: Linden and Osei favour preserving the fixed design and avoiding
outcome-selected reuse; Tanaka requires one effective response per planned slot
with all failed attempts disclosed; Renna flags collection-time comparability;
Okafor requires a separately tested continuation ledger and unchanged originals.
Resolution: document a new linked designation, reuse every valid original record,
fill only unfilled slots, and retain the failure in the source archive. No paid
calls or frozen-code edits were made. See
[HANDOFF_2026-09-07.md](docs/HANDOFF_2026-09-07.md).

## 2026-09-06 — Documentation consolidation and provisional abstract

**User request:** clean up Markdown, update/remove redundant documents, create
AGENTS.md using the CLAUDE.md formula, push the project, and write a rigorous
provisional abstract including unfinished work.

**Decision:** README is the project introduction; NEXT_STEPS is the current
operational ledger; docs/README is the document map. AGENTS.md and CLAUDE.md share
the same constitution body, updated from the existing formula. Scientific
commitments and approval rules remain explicit. The five review roles are
labelled synthetic perspectives, not external reviewers or automatic delegation.
The user's communication preferences are included.

**Concise synthetic review:** Linden: distinguish proposed normative architecture
from demonstrated understanding. Osei: separate pilot functionality from validity.
Tanaka: keep incomplete samples incomplete and do not claim future statistical
results. Renna: distinguish PARIA from the wider Hexagon programme. Okafor:
consolidate navigation while preserving frozen evidence. Resolution: a separate
provisional abstract, current status reconciliation, and unchanged source papers,
prompts, experiment records, and frozen runner code.

Moved the wider-programme OVERVIEW to docs/research_programme.md, retaining its
scope while correcting PARIA overclaims. Archived the old meta log and June
novelty assessment. Removed redundant active copies and stale task lists; Git
history retains the previous README/CLAUDE/NEXT_STEPS versions. The main-study
plan remains a draft; its proposed Python mixed-model cross-check is explicitly
unresolved rather than presented as an implemented binomial estimator.

The user explicitly authorised pushing all project changes to the existing
GitHub remote. This supersedes the earlier lack of publication authorisation.
Raw per-call artifacts and credentials remain excluded from the push.

**Verification:** active Markdown links resolve; AGENTS.md and CLAUDE.md match
apart from their titles; archived documents match their pre-cleanup bytes.
No code, test, source paper, locked prompt, or historical phase evidence changed.
All 8,640 interrupted-run records passed their integrity checks: 8,639 valid,
one API failure, and exact returned model identity on successful calls. Both
September designations now have checksum inventories for publication; raw
payloads remain local.

## 2026-09-06 — Source sweep interrupted by API credit exhaustion

Observed process exit after 8,640/15,000 records in option_c_20260906_r2.
One terminal HTTP 429 reported insufficient_quota / credit_balance_exhausted;
the runner stopped after its current batch and emitted the partial report.
There was no outcome-based stopping decision. The failed record remains stored;
the 6,360 undispatched observations remain missing. No resumption or new paid
run was initiated during documentation cleanup. Funding and an explicit
continuation/restart protocol are required before further source collection.

## Retained methodological decisions

- [Phase 0 closure](experiments/PHASE0_CLOSURE_2026-07-29.md): locked recalibrated
  dilemmas, naked holdout, measured baselines, and headroom tiers.
- [Phase 1 result](experiments/phase1_pilot/PHASE1_PILOT_RESULT_2026-07-29.md):
  S3 plus S2 operational pilot; validity still requires Phase 1.5.
- [Option-C protocol](docs/phase1_5_execution.md): exact snapshot, fixed N,
  joint role/format contrast, immutable records, fail-stop execution.
- [Follow-up protocol](docs/phase1_5_followup.md): independent Claude route;
  200-item blind audit with prevalence-aware diagnostics; six verbal bins;
  human-reviewed paraphrases and all-pair equivalence; optional gradient extension.
- [Historical log](docs/archive/meta_through_2026-09-06.md): original discussions,
  implementation verification, credential-only restart, and earlier decisions.

## Recording future decisions

Add dated entries with the user's objective, concrete decision, evidence,
limitations/deviations, and affected artifacts. Record synthetic review only
where substantive judgment warrants it. Never rewrite historical evidence to
make an experiment appear complete or a planned validation appear passed.
