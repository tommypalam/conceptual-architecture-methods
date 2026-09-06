# NEXT STEPS — working state for future sessions (updated 2026-09-06)

## Current execution update (2026-09-06)

**Latest execution update:** The corrected Windows User OPENAI_API_KEY passed
a model-metadata request (HTTP 200) for `gpt-5.4-mini-2026-03-17`. The user
authorised execution. Fresh run `option_c_20260906_r2` passed its first 10 calls:
10/10 parsed, exact model in all responses, 5 observations per delivery, and
reasoning present in all 5 full-harness responses. Its design hash is identical
to the original manifest. The remaining 14,990 calls have been launched at
concurrency 5. Check current process/record status before starting another runner.

Preserve `option_c_20260906`: the earlier invalid-credential attempt contains
five API failures and no model outputs. The `_r2` designation changes credentials
and storage only, not the frozen scientific design, model, or seed. Raw records
remain local artefacts; do not commit them or the secret key.

User authorised continuing validity work before the supervisor's implementation
review. Branch: `phase1-5-validity`. The new Option-C runner is
`code/run_validity_sweep.py`; see `docs/phase1_5_execution.md` for the frozen design,
commands, statistical criteria, and remaining battery work. The original
`run_phase1_5_sweep.py` and its July pilot records are preserved.

The delivery comparison is implemented and running with real API calls after
offline verification (10 new tests plus 29 existing engine checks). Load the key
from the Windows User environment into the process; never ask for it in chat or
store it in source. No full sweep or battery verdict exists yet.

The alternative arm retains scaffold text. Its headroom is an experimental
outcome, not an assumption. The next step is to monitor the fixed-N run, then
analyse its full saved output without changing the protocol. The remaining coherence,
paraphrase, and numeric/verbal tools are now implemented and offline-tested
(nine new tests), but have no empirical pass. See `docs/phase1_5_followup.md` for
the two CLI entry points, fixed analysis decisions, and supervisor code handoff.
The user chose Claude for independent generation/coding; ANTHROPIC_API_KEY was
absent from Windows User scope at the latest check. Configure/verify it without
displaying it, verify an explicit available Claude model ID, and install the
optional Anthropic SDK before real Claude calls. Generated paraphrases still
require actual human semantic review of their exact hashes.

## Previous working state and approved decision (2026-07-29)

Read this first in a new chat. It says exactly where the project is and what the
next concrete action is. Authoritative background: `CLAUDE.md`, `meta.md`, and
`experiments/PHASE0_CLOSURE_2026-07-29.md`.

## Where we are

- **Phase 0 CLOSED.** 0a locked (May 2026, frozen). 4 drifted dilemmas
  recalibrated to bistable naked and re-locked in
  `experiments/phase0b_calibration/questions/`. 0b established the agent-framing
  harness is NOT behaviourally neutral on gpt-5.4-mini-2026-03-17 (any scaffold
  text collapses S2/C2/C3; localised to the "decision-making simulation"
  preamble; not fixable by template revision). 0c hash-locked holdout N=1000
  gave the working baselines. Verdict: keep all 6 on 0c-measured baselines,
  tiered PRIMARY (S1/S3) / SECONDARY (C1/C2/C3) / LOW-POWER (S2).
- **Phase 1 pilot PASSED** (S3 clean + config-responsive reasoning; S2 expected
  harness skew). `experiments/phase1_pilot/PHASE1_PILOT_RESULT_2026-07-29.md`.
- **Phase 1.5 pilot sweep done:** encoding mechanism PARTIALLY ALIVE — S3 shows
  real gradients (RT correct direction, RE wrong direction, both Cohen's h>0.2);
  S1 pinned 125/125 under the full harness (headroom, not mechanism).
  `experiments/phase1_5_encoding_validity/SWEEP_PILOT_FINDING_2026-07-29.md`.

## THE DECIDED NEXT STEP — full Phase 1.5 sweep, "Option C" (dual delivery)

**Decision (user-approved 2026-07-29): run the full §4.1 single-parameter sweep
under BOTH deliveries and treat the contrast as the result.**

Why: the full Phase-2 harness PINS low-headroom problems (S1 pinned in the
pilot), so a spec-literal sweep would false-negative the framework's primary
gate for harness reasons, not encoding reasons. Option C measures encoding where
it is observable AND quantifies how much the harness suppresses it — which also
answers whether Phase 2 can use the full harness at all (a live question from 0b).

Concretely:
1. **Full harness delivery** (spec-faithful §4.1: system message + DECISION/
   REASONING, neutral config) — shows pinning / suppression.
2. **Headroom-preserving delivery** (the Phase-0b naked/near-neutral envelope:
   `--delivery user_prefix --bare-label`) — shows the parameters' true gradients.

Run all 10 parameters × {0.1,0.3,0.5,0.7,0.9} × S1/S2/S3 × N=50 under EACH
delivery (spec's 7,500-call sweep tier, ×2 for the contrast). Consider staging:
start with the PRIMARY problems (S1, S3) and the parameters with directional
hypotheses (§6.1.1), expand if the contrast is clean. Analysis per §4.1.2/3
(logistic slope, Cohen's h, monotonicity), reported per delivery.

Rig already built: `code/run_phase1_5_sweep.py` (pilot scale) + `SweepProfile`
in `engine/phase0b.py`. It currently runs the FULL-harness delivery; add the
headroom delivery path (it reuses the same `delivery`/`bare_label` seams already
in `phase0b_runner.run_phase0b`).

## Open item to fold in

- **RE-on-S3 wrong-direction** result (§6.1.1 predicted higher RE → WAIT; pilot
  showed ADOPT rising with RE). Investigate per §4.1.3 during the full sweep:
  read RE=0.1 vs 0.9 reasoning traces — inverted encoding? hypothesis wrong?
  noise at N=25? The full N=50 sweep + traces should resolve it.

## Standing rules (unchanged)

- Phase 0a prompts FROZEN; recalibrated set is the working locked set.
- Diagnostic runs → `experiments/phase0b_archive/` (dated); pass `--runs-root`
  or `--sample-tag` so nothing lands in the real results tree.
- SOLID throughout (protocols + DI; composition roots are the only wiring point).
- Supervisor only after Phase 0 + 1 fully complete.
- Concurrency ≤ 5 on real runs (200k TPM cap → 429s above that).
- Mock is the default provider; real runs need `--provider openai` + key in env.

## Documented spec deviations (flag to supervisor after Phase 0/1)

Recalibrated set used for 0b/0c; 0c delivery naked (not null_b); measured-baseline
interpretation extended to substantial-shift problems; Phase 1 pilot on S3+S2 (not
S2 alone); Option-C dual-delivery sweep. All recorded in the phase result docs +
spec §2.1.6 amendment.
