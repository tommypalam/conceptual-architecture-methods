"""Prospectively specified descriptive analysis; no confirmatory significance gate."""
from __future__ import annotations

from collections import Counter
import hashlib
import json
import logging
import math
from pathlib import Path

import numpy as np
import pandas as pd

import utils
from engine.seeding import derive_seed
from phase2_pilot_design import SEED, CONDITIONS, GROUP_CONDITIONS, LABELS, parse
from phase2_pilot_transport import read_record


def wilson(k, n):
    if not n:
        return None
    z = 1.959963984540054
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return [max(0, centre - half), min(1, centre + half)]


def contrast(left, right, *, seed):
    # Both arrays index the SAME complete planned population in identical order.
    x, y = np.asarray(left, dtype=float), np.asarray(right, dtype=float)
    valid = ~np.isnan(x) & ~np.isnan(y)
    n = int(valid.sum())
    delta = x[valid] - y[valid]
    interval = None
    if n:
        rng = np.random.default_rng(seed)
        boots = delta[rng.integers(n, size=(10000, n))].mean(axis=1)
        interval = np.quantile(boots, [.025, .975]).tolist()
    lower = float(np.mean(np.nan_to_num(x, nan=0) - np.nan_to_num(y, nan=1)))
    upper = float(np.mean(np.nan_to_num(x, nan=1) - np.nan_to_num(y, nan=0)))
    return {"paired_n": n, "planned_n": len(x), "excluded_incomplete_pairs": len(x) - n,
            "difference": float(delta.mean()) if n else None, "bootstrap_95": interval,
            "bootstrap_degenerate": bool(n and np.ptp(delta) == 0),
            "missing_outcome_bounds": [lower, upper], "bootstrap_seed": seed}


def analyze(raw_root, output):
    raw_root, output = Path(raw_root), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    records = [read_record(p) for p in sorted((raw_root / "records").glob("*.json"))]
    intents = [read_record(p) for p in sorted((raw_root / "dispatches").glob("*.json"))]
    outcomes = [read_record(p) for p in sorted((raw_root / "groups").glob("*.json"))]
    if records and len({r["mock"] for r in records}) != 1:
        raise ValueError("Mixed mock/live data")
    rows, status = [], Counter()
    completion_reasons, call_ids = Counter(), []
    usage = Counter()
    for r in records:
        meta = r["meta"]
        parsed = parse(r, LABELS[meta["problem"]], simple=meta["stage"] == "simple")
        status[parsed["status"]] += 1
        response = r.get("response") or {}
        if response.get("id"):
            call_ids.append(response["id"])
        for key in ("prompt_tokens", "completion_tokens"):
            usage[key] += (response.get("usage") or {}).get(key, 0)
        completion_reasons.update([str((response.get("choices") or [{}])[0].get("finish_reason"))])
        if meta["stage"] == "simple":
            rows.append({**{k: meta[k] for k in ("problem", "agent", "config", "arm")},
                         "status": parsed["status"], "outcome": parsed["vote"],
                         "value": float(parsed["vote"] == LABELS[meta["problem"]][0]) if parsed["vote"] else None})
    if rows:
        utils.log_dataframe_summary(pd.DataFrame(rows), "Phase 2 pilot simple responses (no rows dropped)", logging.getLogger("pilot"))
    lookup = {(r["problem"], r["agent"], r["config"], r["arm"]): r["value"] for r in rows}
    cells, contrasts = [], []
    for problem in ("S1", "S2", "S3"):
        arrays = {}
        for config, arm in CONDITIONS:
            values = [lookup.get((problem, a, config, arm)) for a in range(1, 51)]
            arrays[config, arm] = values
            valid = [v for v in values if v is not None]
            k = int(sum(valid))
            cells.append({"problem": problem, "config": config, "arm": arm, "metric": LABELS[problem][0],
                          "successes": k, "valid": len(valid), "planned": 50, "missing_invalid": 50 - len(valid),
                          "rate": k / len(valid) if valid else None, "wilson_95": wilson(k, len(valid)),
                          "saturated": bool(valid and k in (0, len(valid))), "root_seed": SEED})
        for config in ("00100", "11011"):
            contrasts.append({"problem": problem, "contrast": "E-U", "config": config,
                              **contrast(arrays[config, "E"], arrays[config, "U"], seed=derive_seed(SEED, "analysis", problem, config))})
        for arm in ("E", "U"):
            contrasts.append({"problem": problem, "contrast": "11011-00100", "arm": arm,
                              **contrast(arrays["11011", arm], arrays["00100", arm], seed=derive_seed(SEED, "analysis", problem, arm))})
    group_cells = []
    for problem in ("C1", "C2", "C3"):
        for config, arm in GROUP_CONDITIONS:
            selected = [g for g in outcomes if (g["problem"], g["config"], g["arm"]) == (problem, config, arm)]
            valid = [g for g in selected if g["result"]["status"] == "ok"]
            k = sum(g["result"]["outcome"] == LABELS[problem][0] for g in valid)
            group_cells.append({"problem": problem, "config": config, "arm": arm, "metric": LABELS[problem][0],
                                "successes": k, "valid": len(valid), "planned": 5, "missing_invalid": 5 - len(valid),
                                "rate": k / len(valid) if valid else None, "wilson_95": wilson(k, len(valid)),
                                "rounds": [g["result"]["rounds"] for g in selected],
                                "consensus_groups": sum(g["result"]["consensus"] for g in selected),
                                "proposal_counts": [g["result"]["proposals"] for g in selected],
                                "adoption_counts": [g["result"]["adoptions"] for g in selected],
                                "public_evidence_counts": [g["result"]["public_evidence"] for g in selected],
                                "ties": sum(g["result"]["tie_break"] for g in selected),
                                "pre_tie_tallies": [g["result"]["final_tally"] for g in selected],
                                "unavailable_citations": sum(len(a.get("unavailable_citations", [])) for g in selected for a in g["state"]["audit"]),
                                "transcript_only_citations": sum(len(a.get("transcript_only_citations", [])) for g in selected for a in g["state"]["audit"]),
                                "root_seed": SEED})
    group_contrasts = []
    group_lookup = {(g["problem"], g["group"], g["config"], g["arm"]): g["result"] for g in outcomes}
    for problem in ("C1", "C2", "C3"):
        for config in ("00100", "11011"):
            pairs = []
            for gid in range(1, 6):
                e, u = [group_lookup.get((problem, gid, config, arm)) for arm in ("E", "U")]
                if e and u and e["status"] == u["status"] == "ok":
                    pairs.append(int(e["outcome"] == LABELS[problem][0]) - int(u["outcome"] == LABELS[problem][0]))
            group_contrasts.append({"problem": problem, "config": config, "contrast": "E-U", "paired_n": len(pairs),
                                    "differences": pairs, "mean": float(np.mean(pairs)) if pairs else None,
                                    "ci": None, "note": "Five matched groups; descriptive only. Cell Wilson intervals reported separately."})
    resolved_hashes = {r["intent_hash"] for r in records}
    from phase2_pilot_transport import digest
    pending = [i for i in intents if digest(i) not in resolved_hashes]
    accounted = sum(r["charged_nano"] for r in records) + sum(i["reserved_nano"] for i in pending)
    result = {"root_seed": SEED, "mock": records[0]["mock"] if records else None,
              "responses": len(records), "dispatches": len(intents), "unresolved_dispatches": len(pending),
              "accounted_usd_including_allowance": accounted / 1e9,
              "unknown_usage_records": sum(not r["usage_known"] for r in records),
              "status_counts": dict(status), "finish_reasons": dict(completion_reasons),
              "duplicate_provider_ids": len(call_ids) - len(set(call_ids)), "usage": dict(usage),
              "simple_cells": cells, "simple_contrasts": contrasts, "group_cells": group_cells,
              "group_contrasts": group_contrasts, "completed_group_runs": len(outcomes),
              "complete_allocation": len(rows) == 600 and len(outcomes) == 75}
    result["simple_rows"] = len(rows)
    (output / "summary.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    if rows:
        pd.DataFrame(rows).to_csv(output / "simple_responses.csv", index=False)
    # Plain-language tables never equate the first label with ethical success.
    lines = ["# Exploratory pilot descriptive results", "", f"Root seed: {SEED}. Mock data: {result['mock']}.", "",
             f"Saved responses: {len(records)}; completed group runs: {len(outcomes)}/75; unresolved dispatches: {len(pending)}.",
             f"Conservative usage accounting including 10% allowance: ${accounted / 1e9:.6f} / $10.", "",
             "First-label rates below describe choices, not moral quality. Wilson 95% intervals use profiles for simple tasks and groups for group tasks.", "",
             "| Task | Context | Arm | First label | Count | Rate (95% CI) | Missing/invalid |",
             "|---|---|---|---|---|---|---|"]
    for cell in cells + group_cells:
        ci = cell["wilson_95"]
        estimate = f"{cell['rate']:.0%} ({ci[0]:.0%}–{ci[1]:.0%})" if ci else "unavailable"
        lines.append(f"| {cell['problem']} | {cell['config']} | {cell['arm']} | {cell['metric']} | {cell['successes']}/{cell['valid']} | {estimate} | {cell['missing_invalid']} |")
    lines += ["", "Paired contrasts and process diagnostics are in summary.json. Intervals are exploratory and unadjusted for multiple comparisons.",
              "No pilot effect is a confirmatory finding; five matched groups per cell cannot establish reliable group-level effect sizes.", ""]
    (output / "RESULTS.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    # The hash index covers every existing immutable raw artifact, including intents.
    index = {str(p.relative_to(raw_root)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(raw_root.rglob("*.json"))}
    (output / "raw_checksums.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: result[k] for k in ("responses", "simple_rows", "completed_group_runs", "complete_allocation", "accounted_usd_including_allowance", "status_counts")}), flush=True)
    return result
