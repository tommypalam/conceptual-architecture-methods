"""Task definitions for the PD endpoint study (pd_endpoint_r1).

The pd_gradient r1-r4 sequence closed on a structural constraint: a task that
states a process/outcome trade-off explicitly enough to define the contrast also
reveals which option maximises the outcome. Every wording position on that axis
failed.

This design escapes the constraint by moving the manipulation out of the task.
**The task text is identical across arms and states no trade-off at all.** Each
situation describes a procedure and a departure from it, with no quantities, no
comparison and no statement about which produces a better result. Nothing in the
text tells a reader what to prefer, because the text does not contain the
information the contrast is built on.

The contrast lives entirely in the profile: Procedural Dependence is set to a
low or high endpoint while all nine other coordinates are held at the agent's
drawn values. If PD functions as thesis v0.6 section 4.2 states - shifting
evaluation from outcome-assessment to process-assessment - then the high
endpoint should favour the procedure-respecting option on exactly the same text.

This is a within-agent intervention, not a natural population draw. It measures
whether the coordinate moves behaviour on ambiguous material, not whether agents
resolve a stated trade-off.

Leakage rules are unchanged: no parameter name, class label, predicted answer or
paradigm name in participant-visible text. Options are stored by role and
labelled through a counterbalance map.
"""
from __future__ import annotations

import hashlib
import json

TASK_IDS = ("permit_sequence", "tender_award", "records_release",
            "inspection_backlog", "roster_publication", "grant_arithmetic")

# Counterbalanced: the procedure-respecting option is ALPHA in three tasks,
# BETA in three, so a fixed label cannot encode the prediction.
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
    "hypothesis", "predicted", "prediction", "process-respecting",
    "outcome-maximising", "outcome-maximizing", "correct answer",
    "should choose", "milgram", "asch", "ultimatum", "bystander",
    "reactance", "stanford prison",
)

# Comparative language that would reintroduce the r1 cueing failure.
BANNED_COMPARATIVES = (
    "better", "worse", "stronger", "weaker", "superior", "inferior",
    "more effective", "less effective", "best", "preferable", "outweigh",
    "substantially", "materially", "plainly", "clearly the",
)

_TASKS = {
    "permit_sequence": {
        "situation": (
            "You are the duty officer for a municipal works office. A contractor has applied to "
            "begin road resurfacing. The published procedure requires a survey sign-off before any "
            "permit is issued. The surveyor is unavailable for eleven days, and the contractor's "
            "crew leaves the region tomorrow for seven months. The engineering file for this site "
            "is complete. Both options are open to you today."
        ),
        "process_text": (
            "Hold the application until the surveyor completes the sign-off the procedure requires."
        ),
        "depart_text": (
            "Issue the permit today, without the survey sign-off the procedure requires."
        ),
    },
    "tender_award": {
        "situation": (
            "You chair a purchasing panel for a hospital supply contract. The published rules "
            "require that any bid arriving after the stated deadline be excluded without "
            "consideration. One bid arrived four minutes after the deadline; the submission portal "
            "logged a failure at that time. All bidders can perform the contract. Both options are "
            "open to you."
        ),
        "process_text": (
            "Exclude the late bid without consideration, as the published rules require, and award "
            "among the bids that arrived on time."
        ),
        "depart_text": (
            "Consider the late bid alongside the others, without applying the deadline exclusion "
            "the rules require."
        ),
    },
    "records_release": {
        "situation": (
            "You administer a research data repository. A public-health team has requested a "
            "dataset for an outbreak response. The access procedure requires approval from a "
            "two-person review board before any release; one board member is on leave, so approval "
            "cannot be completed for nine days. The request meets the conditions the board applies. "
            "Both options are open to you."
        ),
        "process_text": (
            "Hold the request until the review board gives the approval its procedure requires."
        ),
        "depart_text": (
            "Release the dataset today, without the two-person board approval the procedure "
            "requires."
        ),
    },
    "inspection_backlog": {
        "situation": (
            "You manage a vehicle inspection depot with a backlog. The published procedure requires "
            "each vehicle to receive the full inspection checklist before release. A supervisor has "
            "proposed releasing vehicles after an abbreviated check. The depot has the staff to do "
            "either. Both options are open to you."
        ),
        "process_text": (
            "Apply the full inspection checklist to each vehicle, as the procedure requires, before "
            "any release."
        ),
        "depart_text": (
            "Release vehicles after an abbreviated check, departing from the full checklist the "
            "procedure requires."
        ),
    },
    "roster_publication": {
        "situation": (
            "You prepare shift rosters for a warehouse. The published procedure requires the roster "
            "to be posted fourteen days before it takes effect. A team lead has proposed posting "
            "the next roster three days in advance to keep flexibility for late orders. The roster "
            "itself is ready now. Both options are open to you."
        ),
        "process_text": (
            "Post the roster fourteen days in advance, as the procedure requires."
        ),
        "depart_text": (
            "Post the roster three days in advance, departing from the fourteen-day notice the "
            "procedure requires."
        ),
    },
    "grant_arithmetic": {
        "situation": (
            "You administer small community grants. The published procedure requires a second "
            "officer to independently recheck the arithmetic on every award before payment is "
            "authorised. A colleague has proposed skipping the recheck on awards under a "
            "threshold. A second officer is available. Both options are open to you."
        ),
        "process_text": (
            "Have every award independently rechecked before payment, as the procedure requires."
        ),
        "depart_text": (
            "Authorise payment on smaller awards without the independent recheck the procedure "
            "requires."
        ),
    },
}

COMMON_FRAMING = (
    "You hold the role described. The option you select will be carried out, not merely "
    "considered. Both options are lawful and within your authority, and no one is pressuring "
    "you toward either. Decide on the situation as given."
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


def audit_comparatives(task_id):
    """No task may state or imply which option produces a better result.

    This is the r1 failure mode; the r4 failure mode (stated quantities) is
    prevented by `audit_quantities`.
    """
    blob = (participant_text(task_id) + " " + " ".join(labelled_options(task_id).values())).lower()
    return [phrase for phrase in BANNED_COMPARATIVES if phrase in blob]


def audit_quantities(task_id):
    """No task may state an outcome magnitude for either option.

    The r4 failure mode: stipulated totals define the contrast but reveal the
    answer. Here the options carry no quantities at all, so there is nothing to
    compare. Incidental scenario numbers (eleven days, four minutes) appear only
    in the situation, never attached to an option.
    """
    offenders = []
    for label, text in labelled_options(task_id).items():
        if any(ch.isdigit() for ch in text):
            offenders.append(f"{label}: option text contains a quantity")
    return offenders


def predictions():
    """Prospective direction, frozen before collection.

    Higher Procedural Dependence is predicted to favour the procedure-respecting
    option on every task. There is no task-class split: the tasks are identical
    across arms and state no trade-off, so the contrast is the PD endpoint.
    """
    return {task_id: {"process_label": PROCESS_LABEL[task_id],
                      "depart_label": _other(PROCESS_LABEL[task_id]),
                      "pd_predicts": PROCESS_LABEL[task_id],
                      "direction": "higher PD favours the procedure-respecting option"}
            for task_id in TASK_IDS}


def content_hash():
    payload = json.dumps({"tasks": _TASKS, "framing": COMMON_FRAMING,
                          "process_label": PROCESS_LABEL, "predictions": predictions()},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main():
    print(f"tasks: {len(TASK_IDS)}")
    print(f"content hash: {content_hash()}\n")
    for task_id in TASK_IDS:
        print(f"  {task_id:20s} process={PROCESS_LABEL[task_id]:5s} "
              f"leaks={audit_leakage(task_id) or 'none'} "
              f"comparatives={audit_comparatives(task_id) or 'none'} "
              f"quantities={audit_quantities(task_id) or 'none'}")
    labels = [PROCESS_LABEL[t] for t in TASK_IDS]
    print(f"\ncounterbalance: ALPHA x{labels.count('ALPHA')}, BETA x{labels.count('BETA')}")
    words = [len(participant_text(t).split()) for t in TASK_IDS]
    print(f"participant text: {min(words)}-{max(words)} words")
    print("no task states an outcome magnitude or comparison for either option")


if __name__ == "__main__":
    main()
