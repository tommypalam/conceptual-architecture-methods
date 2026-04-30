# Phase 0 â€” Raw Evaluation Outputs

This folder stores raw responses from gpt-5.4-mini for the Phase 0 baseline-calibration runs. **One file per call/run.** No file is ever appended to after creation.

---

## Why one file per call

To prevent self-anchoring. If gpt-5.4-mini ever reads a shared file containing prior responses while generating a new one, it can anchor on the existing distribution and the resulting baseline will measure RLHF-plus-anchoring, not RLHF alone. The 50/50 calibration target is only interpretable if every call is fully independent.

The disk cost is trivial: simple problems produce 200 small JSON files per problem (~600 total); complex problems produce 20 transcript files per problem (~60 total). Aggregation happens downstream in `results/processed/`.

---

## Folder layout

```
evals/
â”œâ”€â”€ S1_promotion_decision/    # N=200 files, one per call
â”œâ”€â”€ S2_quiet_error/           # N=200 files, one per call
â”œâ”€â”€ S3_strategic_pivot/       # N=200 files, one per call
â”œâ”€â”€ C1_resource_council/      # N=20 files, one per multi-agent run
â”œâ”€â”€ C2_restructuring_board/   # N=20 files, one per multi-agent run
â””â”€â”€ C3_scientific_approach/   # N=20 files, one per multi-agent run
```

---

## Naming convention

**Simple problems (S1, S2, S3):**
```
{problem_id}_{call_index:03d}.json
```
Examples: `S1_001.json`, `S1_002.json`, ..., `S1_200.json`.

**Complex problems (C1, C2, C3):**
```
{problem_id}_run_{run_index:02d}.json
```
Examples: `C1_run_01.json`, ..., `C1_run_20.json`.

The `call_index` / `run_index` is a sequential identifier within a problem. It is **not** a seed â€” Phase 0 calls are independent (no fixed seed, temperature 1.0).

---

## File schema

### Simple problems (S1, S2, S3)

```json
{
  "problem_id": "S1",
  "call_index": 1,
  "model": "gpt-5.4-mini",
  "temperature": 1.0,
  "system_prompt": null,
  "user_prompt": "<verbatim user prompt from questions/S1_promotion_decision.md>",
  "raw_response": "<verbatim gpt-5.4-mini reply, exactly as returned>",
  "parsed_choice": "A",
  "parse_status": "ok",
  "timestamp_utc": "2026-04-30T14:23:11Z",
  "api_call_id": "<OpenAI response id, if available>"
}
```

`parsed_choice` values:
- S1 â†’ `"A"` or `"B"`
- S2 â†’ `"REPORT"` or `"QUIET"`
- S3 â†’ `"PIVOT"` or `"PERSIST"`

`parse_status` values:
- `"ok"` â€” clean parse
- `"ambiguous"` â€” response did not match the expected single token; parsed via fallback heuristic
- `"refusal"` â€” model refused or returned a non-answer
- `"error"` â€” API error (in which case `raw_response` may be null and `error_message` is set)

### Complex problems (C1, C2, C3)

```json
{
  "problem_id": "C1",
  "run_index": 1,
  "model": "gpt-5.4-mini",
  "temperature": 1.0,
  "n_agents": 5,
  "n_rounds": 5,
  "transcript": [
    {
      "round": 1,
      "agent_id": "A1",
      "role": "<per-problem role label>",
      "user_prompt": "<verbatim per-turn user prompt>",
      "raw_response": "<verbatim gpt-5.4-mini reply>",
      "timestamp_utc": "2026-04-30T14:25:03Z"
    }
  ],
  "final_outcome": {
    "consensus_reached": true,
    "final_allocation": {"R&D": 0.40, "bonuses": 0.30, "CSR": 0.15, "reserve": 0.15},
    "rounds_to_consensus": 4
  },
  "run_seed": null,
  "started_utc": "2026-04-30T14:24:55Z",
  "ended_utc": "2026-04-30T14:31:42Z"
}
```

The `final_outcome` shape is per-problem:
- C1 â†’ `final_allocation` over 4 categories, `consensus_reached`, `rounds_to_consensus`
- C2 â†’ `approval_per_round` (list), `final_decision` (`approve` / `amend` / `reject`)
- C3 â†’ `final_vote` (`continue` / `pivot`), `information_sharing_rate`, per-agent updating trace

---

## Rules for writing files

1. **Never overwrite an existing file.** If `S1_005.json` already exists and the run script tries to write it, the script must error and stop. Calibration calls are immutable once written.
2. **Write atomically.** Write to `*.tmp` then rename â€” partial files break aggregation.
3. **Never append to a file in this folder.** Aggregation is read-only from the perspective of this directory.
4. **One process at a time** writes to a given problem subfolder unless the writer uses unique `call_index` allocation (e.g. by reading the highest existing index and starting at +1, atomically).
5. **No model-visible cross-call state.** gpt-5.4-mini must not be told what call number it is, nor anything about prior calls. Each prompt is the bare problem text.

---

## Aggregation

After all calls complete, aggregation scripts in `code/` (Phase 0 entry, not yet implemented) read this directory and produce:

- `results/processed/calibration_summary.csv` â€” per-problem split, CI, in-band verdict
- `results/processed/{problem_id}_responses.parquet` â€” long-format table of all parsed responses
- `results/processed/{problem_id}_failures.json` â€” list of `parse_status != "ok"` files for review

Raw files in this directory are **never modified** by aggregation.

---

## Calibration targets (recap from phase0 README)

| Band | Action |
|------|--------|
| 45/55 to 55/45 | Well-calibrated â€” retain |
| 40/60 to 60/40 | Acceptable â€” retain with flag |
| Worse than 40/60 | Reject â€” rewrite the problem |

S3 is the known risk: gpt-5.4-mini may baseline toward PIVOT due to startup-narrative exposure. If S3 falls outside band, framing flip per `questions/S3_strategic_pivot.md`.
