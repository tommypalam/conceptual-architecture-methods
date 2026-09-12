"""Post-hoc formatting/state diagnostics. Never changes the frozen pilot analysis."""
from collections import Counter
import json
from pathlib import Path
import re

from phase2_pilot_transport import read_record, digest
from phase2_pilot_design import parse, LABELS, held_items, PACKAGE, ROOT
from phase2_group_fields_v2 import parse_group_fields


def diagnose():
    root = ROOT / "data" / "raw" / "phase2_exploratory_20260912"
    records = [read_record(p) for p in sorted((root / "records").glob("*.json"))]
    groups = [read_record(p) for p in sorted((root / "groups").glob("*.json"))]
    gmap = {(g["problem"], g["group"], g["config"], g["arm"]): g for g in groups}
    failures, evidence, examples = [], [], []
    candidate_cases, changed_valid = [], []
    n_group = 0
    for r in records:
        m = r["meta"]
        p = parse(r, LABELS[m["problem"]], simple=m["stage"] == "simple")
        if m["stage"] == "complex":
            n_group += 1
            candidate = parse_group_fields(p["text"], LABELS[m["problem"]])
            if p["status"] == "ok" and candidate["vote"] != p["vote"]:
                changed_valid.append(r["slot"])
            elif p["status"] != "ok":
                candidate_cases.append({"slot": r["slot"], "old_status": p["status"], "candidate_vote": candidate["vote"]})
        if p["status"] != "ok":
            inline = re.findall(r"(?<!\n)VOTE:\s*(" + "|".join(LABELS[m["problem"]]) + r")\s*$", p["text"])
            failures.append({"slot": r["slot"], "status": p["status"],
                             "unique_inline_vote": inline[0] if len(inline) == 1 else None})
            if m["problem"] == "C3":
                state = gmap["C3", m["group"], m["config"], m["arm"]]["state"]
                before = {x for a in state["audit"] if a["round"] < m["round"] for x in a["authenticated_disclosures"]}
                after = {x for a in state["audit"] if a["round"] <= m["round"] for x in a["authenticated_disclosures"]}
                own = held_items(state["group"], m["agent"], m["round"])
                cited = set(re.findall(r"\bE\d{2}\b", p["text"]))
                ignored = (cited & own) - before
                if ignored:
                    evidence.append({"slot": r["slot"], "direct_but_not_processed_due_invalid_vote": sorted(ignored),
                                     "still_not_authenticated_after_round": sorted(ignored - after)})
        selected_c2 = (m["stage"] == "complex" and m["problem"] == "C2" and m["group"] == 1
                       and m["config"] == "00100" and m["arm"] == "U" and m["round"] in [4, 5] and m["agent"] == 44)
        selected_c3 = (m["stage"] == "complex" and m["problem"] == "C3" and m["group"] == 1
                       and m["config"] == "00100" and m["arm"] == "E" and m["round"] == 5 and m["agent"] == 14)
        if selected_c2 or selected_c3:
            intent = read_record(root / "dispatches" / (digest(r["slot"]) + ".json"))
            excerpt = ("four independent positive trials with p<0.05" if selected_c3 else
                       "The adopted safeguard already preserves the restructuring" if m["round"] == 4 else
                       "The amended plan already requires a review of non-layoff savings")
            assert excerpt in p["text"]
            examples.append({"slot": r["slot"], "short_response_excerpt": excerpt,
                             "explicit_state_line": [line for line in intent["request"]["messages"][1]["content"].splitlines()
                                                     if line.startswith("Currently adopted amendment IDs:")],
                             "response_hash": digest(r), "request_hash": digest(intent)})
    report = {"label": "Post-hoc diagnostics; frozen outputs unchanged", "failures": failures,
              "failure_problem_counts": dict(Counter(x["slot"][1] for x in failures)),
              "omitted_private_evidence_from_invalid_replies": evidence, "qualitative_examples": examples}
    (PACKAGE / "analysis" / "posthoc_diagnostics.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    import hashlib
    candidate_report = {"status": "Offline candidate only; no frozen outcome changed",
                        "group_responses_checked": n_group, "prior_valid_votes_changed": changed_valid,
                        "recovered_votes": sum(x["candidate_vote"] is not None for x in candidate_cases),
                        "prior_invalid": len(candidate_cases), "invalid_cases": candidate_cases,
                        "candidate_sha256": hashlib.sha256((ROOT / "code" / "phase2_group_fields_v2.py").read_bytes()).hexdigest()}
    (PACKAGE / "analysis" / "parser_candidate_check.json").write_text(json.dumps(candidate_report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"failures": len(failures), "by_problem": report["failure_problem_counts"],
                      "potential_ignored_disclosures": evidence, "examples": examples}))


if __name__ == "__main__":
    diagnose()
