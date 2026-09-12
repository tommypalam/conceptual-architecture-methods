"""Prospectively specified behavioural estimators; no moral scoring."""
from __future__ import annotations

import json
import logging
from collections import Counter
from pathlib import Path

import pandas as pd
from scipy.stats import beta, binomtest

import utils
from phase2_confirmation_design import CONDITIONS, GROUP_CONDITIONS, LABELS, N_PROFILES, N_GROUPS, SEED, parse
from phase2_confirmation_transport import read_record, PRIOR_PHASE2_NANO


def cp(k, n, alpha=.05):
    if not n:
        return [0., 1.]
    return [float(beta.ppf(alpha / 2, k, n-k+1)) if k else 0.,
            float(beta.ppf(1-alpha / 2, k+1, n-k)) if k < n else 1.]


def paired(x, y, planned, family_size=6):
    valid = [(a, b) for a, b in zip(x, y) if a is not None and b is not None]
    n = len(valid)
    n10 = sum(a == 1 and b == 0 for a, b in valid)
    n01 = sum(a == 0 and b == 1 for a, b in valid)
    missing = planned - n
    def interval(alpha):
        l10, u10 = cp(n10, n, alpha/2)
        l01, u01 = cp(n01, n, alpha/2)
        return [max(-1., l10-u01), min(1., u10-l01)]
    p = float(binomtest(n10, n10+n01, .5).pvalue) if n10+n01 else 1.
    return {"planned_pairs": planned, "complete_pairs": n, "missing_pairs": missing,
            "n10": n10, "n01": n01, "difference": (n10-n01)/n if n else None,
            "ci95": interval(.05), "family_ci95": interval(.05/family_size),
            "missing_assignment_bounds": [(n10-n01-missing)/planned, (n10-n01+missing)/planned],
            "complete_pair_exact_p": p, "primary_p": p if not missing else 1.}


def holm(rows):
    ordered = sorted(range(len(rows)), key=lambda i: rows[i]["primary_p"])
    previous = 0.
    for rank, i in enumerate(ordered):
        previous = min(1., max(previous, (len(rows)-rank)*rows[i]["primary_p"]))
        rows[i]["holm_p"] = previous
        rows[i]["reject_05"] = previous <= .05


def analyze(raw, out):
    raw, out = Path(raw), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    results = [read_record(p) for p in sorted((raw / "records").glob("*.json"))]
    groups = [read_record(p) for p in sorted((raw / "groups").glob("*.json"))]
    simple = {}
    status = Counter()
    tokens = Counter()
    rows = []
    for r in results:
        m = r["meta"]
        parsed = parse(r, LABELS[m["problem"]], simple=m["stage"] == "simple")
        status[m["stage"] + ":" + parsed["status"]] += 1
        usage = (r.get("response") or {}).get("usage") or {}
        tokens.update({k: usage.get(k, 0) for k in ("prompt_tokens", "completion_tokens")})
        rows.append({**m, "vote": parsed["vote"], "status": parsed["status"]})
        if m["stage"] == "simple":
            key = (m["problem"], m["config"], m["arm"], m["agent"])
            if key in simple:
                raise ValueError("Duplicate simple identity")
            simple[key] = int(parsed["vote"] == LABELS[m["problem"]][0]) if parsed["vote"] else None
    utils.log_dataframe_summary(pd.DataFrame(rows), "Confirmation response table; every response retained", logging.getLogger("confirmation"))
    pd.DataFrame(rows).to_csv(out / "responses.csv", index=False, lineterminator="\n")
    cells, contrasts, secondary_context = [], [], []
    for problem in ("S1", "S2", "S3"):
        for config, arm in CONDITIONS:
            values = [simple.get((problem, config, arm, aid)) for aid in range(1, N_PROFILES+1)]
            valid = [v for v in values if v is not None]
            cells.append({"problem": problem, "config": config, "arm": arm, "first_label": LABELS[problem][0],
                          "first_count": sum(valid), "valid": len(valid), "missing": N_PROFILES-len(valid),
                          "rate": sum(valid)/len(valid) if valid else None, "ci95": cp(sum(valid), len(valid))})
        for config in ("00100", "11011"):
            x = [simple.get((problem, config, "E", aid)) for aid in range(1, N_PROFILES+1)]
            y = [simple.get((problem, config, "U", aid)) for aid in range(1, N_PROFILES+1)]
            contrasts.append({"problem": problem, "config": config, "contrast": "E-U", **paired(x, y, N_PROFILES)})
        for arm in ("E", "U"):
            x = [simple.get((problem, "11011", arm, aid)) for aid in range(1, N_PROFILES+1)]
            y = [simple.get((problem, "00100", arm, aid)) for aid in range(1, N_PROFILES+1)]
            secondary_context.append({"problem": problem, "arm": arm, "contrast": "11011-00100",
                                      **paired(x, y, N_PROFILES)})
    holm(contrasts)
    # Context contrasts are descriptive, with no new significance declaration.
    indexed = {}
    for g in groups:
        key = (g["problem"], g["config"], g["arm"], g["group"])
        if key in indexed:
            raise ValueError("Duplicate group identity")
        indexed[key] = g
    group_cells, group_tests = [], []
    def group_value(problem, config, arm, gid, metric="choice"):
        g = indexed.get((problem, config, arm, gid))
        if not g or g["result"]["status"] != "ok":
            return None
        r = g["result"]
        return int(r["outcome"] == LABELS[problem][0]) if metric == "choice" else int(r["consensus"])
    for problem in ("C1", "C2", "C3"):
        for config, arm in GROUP_CONDITIONS:
            gs = [indexed.get((problem, config, arm, gid)) for gid in range(1, N_GROUPS+1)]
            present = [g for g in gs if g]
            values = [group_value(problem, config, arm, gid) for gid in range(1, N_GROUPS+1)]
            valid = [v for v in values if v is not None]
            group_cells.append({"problem": problem, "config": config, "arm": arm,
                                "first_label": LABELS[problem][0], "first_count": sum(valid), "valid": len(valid),
                                "missing": N_GROUPS-len(valid), "ci95": cp(sum(valid), len(valid)),
                                "consensus": sum(g["result"]["consensus"] for g in present),
                                "mean_rounds": sum(g["result"]["rounds"] for g in present)/len(present) if present else None,
                                "mean_public_evidence": sum(g["result"]["public_evidence"] for g in present)/len(present) if present else None,
                                "adoptions": sum(g["result"]["adoptions"] for g in present)})
        for config in ("00100", "11011"):
            x = [group_value(problem, config, "E", gid) for gid in range(1, N_GROUPS+1)]
            y = [group_value(problem, config, "U", gid) for gid in range(1, N_GROUPS+1)]
            group_tests.append({"problem": problem, "config": config, "metric": "first_label", **paired(x, y, N_GROUPS, 7)})
    x = [group_value("C1", "00100", "E", gid, "consensus") for gid in range(1, N_GROUPS+1)]
    y = [group_value("C1", "00100", "U", gid, "consensus") for gid in range(1, N_GROUPS+1)]
    group_tests.append({"problem": "C1", "config": "00100", "metric": "consensus_by_round5", **paired(x, y, N_GROUPS, 7)})
    holm(group_tests)
    charged = sum(r["charged_nano"] for r in results)
    complete = len(simple) == 4800 and len(indexed) == 300
    summary = {"seed": SEED, "complete_allocation": complete, "response_count": len(results),
               "simple_slots": len(simple), "group_runs": len(groups), "status": dict(status),
               "token_usage": dict(tokens), "accounted_nano": charged, "accounted_usd": charged/1e9,
               "aggregate_phase2_accounted_usd": (charged+PRIOR_PHASE2_NANO)/1e9,
               "api_errors": sum(bool(r["error"]) for r in results),
               "integrity_errors": sum(bool(r.get("integrity_error")) for r in results),
               "unknown_usage": sum(not r["usage_known"] for r in results),
               "simple_cells": cells, "primary_individual_contrasts": contrasts,
               "descriptive_context_contrasts": secondary_context,
               "group_cells": group_cells, "secondary_group_contrasts": group_tests}
    (out / "summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8", newline="\n")
    lines = ["# Fresh-sample Phase 2 behavioural results", "", f"Seed {SEED}; {len(results)} responses; {len(groups)}/300 group runs.",
             f"Complete allocation: {complete}. Conservative run accounting ${charged/1e9:.8f}; pilot plus follow-up ${(charged+PRIOR_PHASE2_NANO)/1e9:.8f}.", "",
             "## Individual primary comparisons", "", "Difference is encoded minus context-only probability of the first label. Six exact paired tests use Holm adjustment.",
             "Intervals are conservative finite-sample paired intervals; family intervals use Bonferroni over six contrasts.", "",
             "| Task | Context | E-U | Pointwise 95% CI | Family 95% CI | Holm p | Missing pairs |",
             "|---|---|---:|---|---|---:|---:|"]
    for r in contrasts:
        lines.append(f"| {r['problem']} | {r['config']} | {r['difference']} | {r['ci95']} | {r['family_ci95']} | {r['holm_p']:.5g} | {r['missing_pairs']} |")
    lines += ["", "## Group outcomes", "", "Twenty matched groups per condition. These are secondary endpoints with limited power; neutral bridges are descriptive.", "",
              "| Task | Context | Arm | First label | Count / valid | Missing | Consensus | Mean rounds | Mean public evidence |",
              "|---|---|---|---|---|---:|---:|---:|---:|"]
    for r in group_cells:
        lines.append(f"| {r['problem']} | {r['config']} | {r['arm']} | {r['first_label']} | {r['first_count']} / {r['valid']} | {r['missing']} | {r['consensus']} | {r['mean_rounds']} | {r['mean_public_evidence']} |")
    lines += ["", "Seven prespecified secondary group contrasts use their own Holm family; see summary.json for paired counts, exact tests and intervals.",
              "No ethical understanding, human resemblance, moral quality, individual-axis identification, or superiority to a postfilter is established by these behavioural comparisons.",
              "The two anchor environments change all five context bits together. Model snapshot, prompts and profiles delimit generalisation.", ""]
    (out / "RESULTS.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in summary.items() if not isinstance(v, list)}), flush=True)
    return summary
