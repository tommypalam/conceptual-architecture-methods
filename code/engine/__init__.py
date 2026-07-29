"""
engine — the Concepts-as-Architecture simulation engine.

Operational core of the Implementation Specification v0.1, decomposed on SOLID
lines: each module has one responsibility and depends on interfaces, not
concretes. The composition roots (code/run_engine.py, code/run_phase0b.py) are
the only places concrete blocks are wired together.

Shared blocks
  llm_client       provider-agnostic async call layer (SupportsComplete)   §1.1, §5.4.2
  record_sink      RecordSink protocol + JSON/memory sinks (write-once)     §1.3
  seeding          one deterministic seed-derivation rule                  §1.4, §5.2
  questions        read dilemma bodies from the locked Phase 0 files
  prompt_assembly  system-prompt population, config descriptions           §5.3
  parsing          DECISION / REASONING / vote / action extraction         §5.4.1
  population       paired-agent draw + exposure ordering                   §5.1–5.2
  scoring          rate + Wilson-CI aggregation                            §7.5.3

Phase machinery
  simple_runner    LPM simple-problem engine                               Part 5
  problems         C1/C2/C3 protocol defs + evidence + bridge              §6.4–6.5
  orchestrator     Agents-of-Chaos multi-agent runner                      §6.1–6.3
  complex_runner   drive orchestrator across runs/configs + bridge         §6.4–6.5
  phase0b          null-condition + sweep assemblers (empty/neutral/sham/  §2.1,
                   ladder/sweep), all one NullConditionAssembler Protocol   §4.1
  phase0b_runner   harness-neutral / sweep grid runner                     §2.1.4
  phase0b_scorer   18-cell pass/fail evaluation                            §2.1.4

Harness-investigation + calibration blocks (Phase-0b closure, 2026-07-28/29)
  delivery         Delivery Protocol: system-role vs user-prefix message shape
  framing          swappable TaskFraming (preamble/rule/reasoning/bare-label)
  ablation         framing-ablation runner (empty harness)
  ablation_scorer  ablation variant x problem scoring
  recalibrate      naked-prompt recalibration rig (Phase-0b/0c calibration)

The engine never touches the immutable Phase 0 archive.
"""

__all__ = [
    # shared blocks
    "llm_client", "record_sink", "seeding", "questions",
    "prompt_assembly", "parsing", "population", "scoring",
    # phase machinery
    "simple_runner", "problems", "orchestrator", "complex_runner",
    "phase0b", "phase0b_runner", "phase0b_scorer",
    # harness-investigation + calibration
    "delivery", "framing", "ablation", "ablation_scorer", "recalibrate",
]
