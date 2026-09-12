"""Post-collection, unblinded implementation diagnostics; never moral scores."""
import json
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from run_phase2_confirmation import ROOT, RAW, PACKAGE, verify
from phase2_confirmation_design import parse, LABELS
from phase2_pilot_design import parse as strict_pilot_parse
from phase2_confirmation_transport import read_record, digest, now


def diagnose():
    manifest = verify()
    if (RAW / "execution.lock").exists():
        raise RuntimeError("Run diagnostics after collection and replay audit")
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(read_record, sorted((RAW / "records").glob("*.json"))))
        groups = list(pool.map(read_record, sorted((RAW / "groups").glob("*.json"))))
    statuses, schema, strict_comparison = Counter(), Counter(), Counter()
    failures, c2_candidates, unregistered_proposals = [], [], []
    for r in results:
        m = r["meta"]
        p = parse(r, LABELS[m["problem"]], simple=m["stage"] == "simple")
        statuses[m["problem"] + ":" + p["status"]] += 1
        if p["status"] != "ok":
            failures.append({"slot": r["slot"], "status": p["status"], "text": p["text"], "record_hash": digest(r)})
        if m["stage"] != "complex":
            continue
        if (m["problem"] == "C2" and m["round"] < 5
                and p["fields"].get("AMENDMENT", "NONE").strip() not in ("", "NONE")
                and p["fields"].get("ACTION") != "amend"):
            unregistered_proposals.append({"slot": r["slot"], "fields": p["fields"], "record_hash": digest(r)})
        old = strict_pilot_parse(r, LABELS[m["problem"]])
        strict_comparison["confirmation_vote_ok"] += p["vote"] is not None
        strict_comparison["strict_pilot_vote_ok"] += old["vote"] is not None
        strict_comparison["recovered_by_prospective_parser"] += p["vote"] is not None and old["vote"] is None
        strict_comparison["previously_valid_label_changed"] += old["vote"] is not None and old["vote"] != p["vote"]
        required = ["REASONING", "VOTE"]
        if m["problem"] == "C2":
            required += ["ACTION", "AMENDMENT", "ADOPT"]
        elif m["problem"] == "C3":
            required += ["ACTION", "SHARE"]
        for name in required:
            # A canonical inline vote is a valid independent vote even if not a headed field.
            if name != "VOTE" and not p["fields"].get(name):
                schema[m["problem"] + ":missing_" + name] += 1
        if m["problem"] == "C2" and re.search(r"\b(adopted|amended|revised)\b", p["text"], re.I):
            intent = read_record(RAW / "dispatches" / (digest(r["slot"]) + ".json"))
            user = intent["request"]["messages"][-1]["content"]
            if "Currently adopted amendment IDs: NONE\n" in user:
                c2_candidates.append({"slot": r["slot"], "text": p["text"], "record_hash": digest(r)})
    events = Counter()
    for g in groups:
        proposal_texts = list(g["state"]["proposals"].values())
        events[g["problem"] + ":duplicate_proposal_text_ids"] += len(proposal_texts)-len(set(proposal_texts))
        for event in g["state"]["audit"]:
            for key in ("invalid_adoptions", "malformed_adoption_field", "reference_only_proposal", "field_errors",
                        "unavailable_citations", "transcript_only_citations"):
                events[g["problem"] + ":" + key] += bool(event.get(key))
            if g["problem"] == "C3" and event.get("vote_status") != "ok" and event.get("authenticated_disclosures"):
                events["C3:disclosure_retained_despite_bad_vote"] += 1
    review = {"parser_failures": failures, "c2_no_adoptions_word_screen": c2_candidates,
              "c2_unregistered_proposal_text": unregistered_proposals,
              "screen_warning": "Unblinded lexical candidates, including negations and proposals; not established hallucinations or moral labels."}
    review_path = RAW / "review" / "diagnostic_candidates.json"
    with review_path.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(review, f, indent=2)
        f.write("\n")
    report = {"at": now(), "manifest_hash": digest(manifest), "statuses_by_task": dict(statuses),
              "missing_field_diagnostics": dict(schema), "parser_comparison_on_fresh_responses": dict(strict_comparison),
              "group_audit_event_counts": dict(events), "parser_failure_count": len(failures),
              "c2_word_screen_candidates": len(c2_candidates), "candidates_hash": digest(review),
              "c2_proposal_text_without_amend_action": len(unregistered_proposals),
              "moral_scores_assigned": False, "human_gold_review": False}
    with (PACKAGE / "analysis" / "diagnostics.json").open("x", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    diagnose()
