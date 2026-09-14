"""Task definitions for the prospective PD gradient test (pd_gradient_r4).

Revision of r3, which stopped at review with verdict `reject`. The accepted
finding was structural: r2/r3 removed evaluative wording and in doing so removed
the property defining Class P, so `permit_sequence` and `records_release` no
longer established that departing from the procedure produces a materially
better outcome. Class P had collapsed into Class N.

The repair is the Phase 4 finite-rule pattern: **the trade-off is carried by
stipulated quantities, not by adjectives.** Every task states, in a common
stipulated unit, exactly what each option produces. Class membership is then
verifiable by arithmetic from the text alone:

  Class P (divergent): the procedure-departing option has a strictly higher
      stipulated total than the procedure-respecting option.
  Class N (aligned):   the procedure-respecting option has the higher total.

No task uses "better", "stronger", "superior", "sound", "plainly" or any other
comparative judgement. The numbers carry the comparison, and `verify_classes`
recomputes class membership from the stipulated effects rather than trusting the
declared label - so a wording change cannot silently break the design again.

Leakage rules are unchanged from r2 and enforced by `audit_leakage`: no
parameter name, class label, predicted answer or paradigm name in any
participant-visible text. Options are stored by role and labelled through a
counterbalance map, so a fixed label cannot encode the prediction.
"""
from __future__ import annotations

import hashlib
import json

CLASS_P = ("permit_sequence", "tender_award", "records_release")
CLASS_N = ("inspection_backlog", "roster_publication", "grant_arithmetic")
TASK_IDS = CLASS_P + CLASS_N

PROCESS_LABEL = {
    "permit_sequence": "BETA",
    "tender_award": "ALPHA",
    "records_release": "BETA",
    "inspection_backlog": "ALPHA",
    "roster_publication": "BETA",
    "grant_arithmetic": "ALPHA",
}

FORBIDDEN = (
    "procedural dependence", "proceduraldependence", " pd ", "(pd)", "pd=",
    "legitimacy locus", "constraint sensitivity", "response threshold",
    "mode of response", "relational embedding", "tolerance for asymmetry",
    "internalisation dependence", "internalization dependence", "moral scope",
    "affective weighting", "parameter", "coordinate", "profile value",
    "class p", "class n", "hypothesis", "predicted", "prediction",
    "process-respecting", "outcome-maximising", "outcome-maximizing",
    "correct answer", "should choose", "milgram", "asch", "ultimatum",
    "bystander", "reactance", "stanford prison",
)

# Each task stipulates a common unit and the exact total each option produces.
# `process_total` and `depart_total` are the stipulated arithmetic, not a
# judgement; verify_classes() derives class membership from them.
_TASKS = {
    # ------- Class P: departing from the procedure yields the higher total -------
    "permit_sequence": {
        "task_class": "P",
        "unit": "service-days of usable road",
        "situation": (
            "You are the duty officer for a municipal works office. A contractor has applied to "
            "begin road resurfacing. The published procedure requires a survey sign-off before any "
            "permit is issued. The surveyor is unavailable for eleven days, and the contractor's "
            "crew leaves the region tomorrow for seven months.\n\n"
            "The effects are fixed and known. Issuing the permit today produces 2,400 service-days "
            "of usable road this year. Waiting for the sign-off produces 900 service-days. The "
            "survey, when it is eventually carried out, will record the same condition either way, "
            "and no other effect follows from either option."
        ),
        "process_text": (
            "Hold the application until the surveyor completes the sign-off the procedure requires. "
            "This produces 900 service-days."
        ),
        "depart_text": (
            "Issue the permit today, without the survey sign-off the procedure requires. "
            "This produces 2,400 service-days."
        ),
        "process_total": 900,
        "depart_total": 2400,
    },
    "tender_award": {
        "task_class": "P",
        "unit": "thousand units of supply delivered",
        "situation": (
            "You chair a purchasing panel for a hospital supply contract. The published rules "
            "require that any bid arriving after the stated deadline be excluded without "
            "consideration. One bid arrived four minutes after the deadline; the submission portal "
            "logged a failure at that time.\n\n"
            "The effects are fixed and known. Awarding among the bids that arrived on time delivers "
            "50 thousand units of supply over the contract term. Awarding to the late bid delivers "
            "78 thousand units over the same term at the same cost. Both bidders can perform, and "
            "no other effect follows from either option."
        ),
        "process_text": (
            "Exclude the late bid without consideration, as the published rules require, and award "
            "among the bids that arrived on time. This delivers 50 thousand units."
        ),
        "depart_text": (
            "Consider the late bid alongside the others, without applying the deadline exclusion "
            "the rules require. This delivers 78 thousand units."
        ),
        "process_total": 50,
        "depart_total": 78,
    },
    "records_release": {
        "task_class": "P",
        "unit": "people covered by the resulting public-health measure",
        "situation": (
            "You administer a research data repository. A public-health team has requested a "
            "dataset for an outbreak response. The access procedure requires approval from a "
            "two-person review board before any release; one board member is on leave, so approval "
            "cannot be completed for nine days.\n\n"
            "The effects are fixed and known. Releasing the dataset today results in a measure "
            "covering 40,000 people. Releasing it after the nine-day approval results in a measure "
            "covering 15,000 people. The board would approve the request in either case, and no "
            "other effect follows from either option."
        ),
        "process_text": (
            "Hold the request until the review board gives the approval its procedure requires. "
            "This covers 15,000 people."
        ),
        "depart_text": (
            "Release the dataset today, without the two-person board approval the procedure "
            "requires. This covers 40,000 people."
        ),
        "process_total": 15000,
        "depart_total": 40000,
    },
    # ------- Class N: following the procedure yields the higher total -------
    "inspection_backlog": {
        "task_class": "N",
        "unit": "vehicles cleared this month",
        "situation": (
            "You manage a vehicle inspection depot with a backlog. The published procedure requires "
            "each vehicle to receive the full inspection checklist before release. A supervisor has "
            "proposed releasing vehicles after an abbreviated check.\n\n"
            "The effects are fixed and known. Applying the full checklist clears 610 vehicles this "
            "month. Releasing after an abbreviated check clears 450 vehicles this month, because "
            "missed defects return for rework that occupies the inspection bays. No other effect "
            "follows from either option."
        ),
        "process_text": (
            "Apply the full inspection checklist to each vehicle, as the procedure requires, before "
            "any release. This clears 610 vehicles."
        ),
        "depart_text": (
            "Release vehicles after an abbreviated check, departing from the full checklist the "
            "procedure requires. This clears 450 vehicles."
        ),
        "process_total": 610,
        "depart_total": 450,
    },
    "roster_publication": {
        "task_class": "N",
        "unit": "shifts covered next month",
        "situation": (
            "You prepare shift rosters for a warehouse. The published procedure requires the roster "
            "to be posted fourteen days before it takes effect. A team lead has proposed posting "
            "the next roster three days in advance to keep flexibility for late orders.\n\n"
            "The effects are fixed and known. Posting at fourteen days covers 880 shifts next "
            "month. Posting at three days covers 700 shifts, because short-notice rosters draw "
            "absence and swap requests that are filled on the day if at all. No other effect "
            "follows from either option."
        ),
        "process_text": (
            "Post the roster fourteen days in advance, as the procedure requires. This covers "
            "880 shifts."
        ),
        "depart_text": (
            "Post the roster three days in advance, departing from the fourteen-day notice the "
            "procedure requires. This covers 700 shifts."
        ),
        "process_total": 880,
        "depart_total": 700,
    },
    "grant_arithmetic": {
        "task_class": "N",
        "unit": "awards correctly paid this quarter",
        "situation": (
            "You administer small community grants. The published procedure requires a second "
            "officer to independently recheck the arithmetic on every award before payment is "
            "authorised. A colleague has proposed skipping the recheck on awards under a "
            "threshold.\n\n"
            "The effects are fixed and known. Rechecking every award results in 340 awards "
            "correctly paid this quarter. Skipping the recheck on smaller awards results in 295, "
            "because errors found after payment require a clawback notice and a reissued payment. "
            "No other effect follows from either option."
        ),
        "process_text": (
            "Have every award independently rechecked before payment, as the procedure requires. "
            "This results in 340 awards correctly paid."
        ),
        "depart_text": (
            "Authorise payment on smaller awards without the independent recheck the procedure "
            "requires. This results in 295 awards correctly paid."
        ),
        "process_total": 340,
        "depart_total": 295,
    },
}

COMMON_FRAMING = (
    "You hold the role described. The option you select will be carried out, not merely "
    "considered. Both options are lawful and within your authority, and no one is pressuring "
    "you toward either. The stated quantities are certain and known to you; there are no "
    "hidden costs, benefits or later effects beyond those described. Decide on the situation "
    "as given."
)


def _other(label):
    return "BETA" if label == "ALPHA" else "ALPHA"


def task(task_id):
    if task_id not in TASK_IDS:
        raise ValueError(f"Unknown task: {task_id}")
    return json.loads(json.dumps(_TASKS[task_id]))


def labelled_options(task_id):
    spec = _TASKS[task_id]
    process_label = PROCESS_LABEL[task_id]
    return {process_label: spec["process_text"], _other(process_label): spec["depart_text"]}


def participant_text(task_id):
    return "\n\n".join((COMMON_FRAMING, _TASKS[task_id]["situation"]))


def audit_leakage(task_id):
    blob = (participant_text(task_id) + " " + " ".join(labelled_options(task_id).values())).lower()
    return [term for term in FORBIDDEN if term.strip() in blob]


def verify_classes():
    """Recompute class membership from the stipulated totals.

    This is the r3 repair: class membership is derived from arithmetic in the
    task text rather than trusted from the declared label, so a future wording
    change cannot silently collapse Class P into Class N again.
    """
    problems = []
    for task_id in TASK_IDS:
        spec = _TASKS[task_id]
        departing_is_higher = spec["depart_total"] > spec["process_total"]
        declared = spec["task_class"]
        derived = "P" if departing_is_higher else "N"
        if derived != declared:
            problems.append(f"{task_id}: declared {declared}, totals imply {derived}")
        if spec["depart_total"] == spec["process_total"]:
            problems.append(f"{task_id}: totals are equal, no trade-off")
        for role in ("process_text", "depart_text"):
            if str(spec[role.replace("_text", "_total")]) not in spec[role].replace(",", ""):
                problems.append(f"{task_id}: {role} does not state its stipulated total")
    if problems:
        raise ValueError("Class verification failed: " + "; ".join(problems))
    return {"verified_from_totals": True, "tasks": len(TASK_IDS)}


def predictions():
    out = {}
    for task_id in TASK_IDS:
        spec = _TASKS[task_id]
        divergent = spec["depart_total"] > spec["process_total"]
        process_label = PROCESS_LABEL[task_id]
        out[task_id] = {
            "task_class": spec["task_class"],
            "divergent": divergent,
            "process_label": process_label,
            "depart_label": _other(process_label),
            "process_total": spec["process_total"],
            "depart_total": spec["depart_total"],
            "unit": spec["unit"],
            "pd_predicts": process_label if divergent else None,
            "gradient_predicted": divergent,
        }
    return out


def content_hash():
    payload = json.dumps(
        {"tasks": _TASKS, "framing": COMMON_FRAMING, "process_label": PROCESS_LABEL,
         "predictions": predictions()},
        sort_keys=True, separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main():
    verify_classes()
    preds = predictions()
    print(f"tasks: {len(TASK_IDS)}  (Class P: {len(CLASS_P)}, Class N: {len(CLASS_N)})")
    print(f"content hash: {content_hash()}\n")
    print(f"{'task':20s} {'class':5s} {'process':>9s} {'depart':>9s} {'gap':>9s} "
          f"{'label':5s} {'predicts':8s} leaks")
    for task_id in TASK_IDS:
        p = preds[task_id]
        gap = p["depart_total"] - p["process_total"]
        print(f"  {task_id:18s} {p['task_class']:5s} {p['process_total']:>9,} "
              f"{p['depart_total']:>9,} {gap:>+9,} {p['process_label']:5s} "
              f"{str(p['pd_predicts'] or 'none'):8s} {audit_leakage(task_id) or 'none'}")

    labels = [preds[t]["process_label"] for t in TASK_IDS]
    print(f"\ncounterbalance: process label ALPHA x{labels.count('ALPHA')}, "
          f"BETA x{labels.count('BETA')}")
    print(f"class verification: {verify_classes()}")
    total_leaks = sum(len(audit_leakage(t)) for t in TASK_IDS)
    print(f"leakage audit: {total_leaks} forbidden terms")
    words = [len(participant_text(t).split()) for t in TASK_IDS]
    print(f"participant text length: {min(words)}-{max(words)} words")


if __name__ == "__main__":
    main()
