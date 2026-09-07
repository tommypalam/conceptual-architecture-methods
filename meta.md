# PARIA decision log

Current decisions are recorded here; [NEXT_STEPS.md](NEXT_STEPS.md) owns execution
status. The [earlier log](docs/archive/meta_through_2026-09-06.md) is preserved
byte-for-byte, including its original encoding defects and historical templates.

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
