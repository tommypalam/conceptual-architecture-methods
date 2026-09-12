# C1 - The Resource Council

**Archive source:** Seventh binary-package C1 calibration after tiny B nudge/rollback. User-reported result: run-level PACKAGE_A 20/20; agent-level final votes 61 PACKAGE_A / 39 PACKAGE_B at N=20 single-call runs. Verdict: REWRITE / RETUNE.

**Diagnosis:** The run-level package-majority metric amplifies small agent-level leans into 20/20 outcomes. Like C3, C1 should be calibrated on agent-level final votes during Phase 0. v8 keeps the binary package design but explicitly defines agent-level final votes as the calibration metric, and removes the forced "package with majority is adopted" framing that makes the model converge toward a single committee outcome.
