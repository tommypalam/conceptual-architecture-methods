# Step D — Current-Model Naked Baseline (original dilemmas)

Date: 2026-07-28 · Model: gpt-5.4-mini-2026-03-17 · N=100 · naked protocol
(no system message; "Reply with only: X or Y"; max_tokens=20)

| prob | split | CI | verdict | action |
|------|-------|-----|---------|--------|
| S1 | A 57 / B 43 | [0.47,0.66] | ACCEPTABLE | KEEP (no rewrite) |
| S2 | FR 0 / LOCAL 100 | [0.00,0.04] | FAIL | REWRITE (severe, 50pp) |
| S3 | ADOPT 30 / WAIT 70 | [0.22,0.40] | FAIL | REWRITE (moderate, 20pp) |
| C1 | A 30 / B 70 | [0.22,0.40] | FAIL | REWRITE (moderate, 20pp) |
| C2 | APPROVE 25 / REJECT 75 | [0.18,0.34] | FAIL | REWRITE (moderate-hard, 25pp) |
| C3 | CONTINUE 59 / PIVOT 41 | [0.49,0.68] | ACCEPTABLE | KEEP (no rewrite) |

Reference baseline for all Step D rewrites. Rewrites are measured against 45-55
(PASS) / 40-60 (ACCEPTABLE) under this same naked protocol. Only S2, S3, C1, C2
need rewriting; S1 and C3 are kept as Phase-0a-validated.
