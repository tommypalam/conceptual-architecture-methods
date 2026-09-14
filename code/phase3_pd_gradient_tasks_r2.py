"""Task definitions for the prospective PD gradient test (pd_gradient_r2).

Revision of r1, which stopped at review with verdict `revise`. Changes:
  - Situations state the trade-off as fact with no evaluative comparison. No
    text asserts that one option is superior, stronger, or plainly correct.
  - Class N situations give base rates rather than stating that following the
    procedure is also the better outcome.
  - Option texts name the departure without editorial framing.
See ../experiments/phase3_benchmarks/pd_gradient_r1/ASSESSMENT.md.

Six fresh binary dilemmas in two prespecified classes:

  Class P (divergent) - the process-respecting action and the outcome-maximising
      action select DIFFERENT options. Prediction: higher Procedural Dependence
      predicts the process-respecting option.
  Class N (aligned) - both considerations select the SAME option. Prediction:
      no PD gradient, because the process/outcome axis has nothing to separate.

Class N is the discriminating control. A PD gradient on P together with its
absence on N distinguishes a process/outcome mechanism from a general dissent
dial; a P-only study cannot make that distinction.

Each task stores its two options as `process_text` and `outcome_text` - by role,
never by label. Labels are assigned by `labelled_options`, which counterbalances
across tasks so the process-respecting option is ALPHA in three tasks and BETA
in three. This prevents a fixed label, or a general pro-rule bias, from
reproducing the predicted pattern without any PD gradient. Storing options by
role also makes a label/role mismatch structurally impossible.

Leakage rules enforced by `audit_leakage` and the offline tests:
  - No parameter name, code, or the phrase "procedural dependence" appears in
    any participant-visible text.
  - No task states or hints at a predicted, preferred or correct answer.
  - No task names a classic paradigm or references this study's hypothesis.
  - Option labels are neutral tokens with no evaluative valence.

None of these tasks is S1-S3 or a decanonised classic benchmark. No parameter,
marginal, correlation entry, locked question or societal axis definition is
changed by this module.
"""
from __future__ import annotations

import hashlib
import json

CLASS_P = ("permit_sequence", "tender_award", "records_release")
CLASS_N = ("inspection_backlog", "roster_publication", "grant_arithmetic")
TASK_IDS = CLASS_P + CLASS_N

# Counterbalance: which label the process-respecting option carries.
# Three ALPHA and three BETA, and within each class the split is 2/1 vs 1/2,
# so neither a fixed label nor a class-label pairing can encode the prediction.
PROCESS_LABEL = {
    "permit_sequence": "BETA",
    "tender_award": "ALPHA",
    "records_release": "BETA",
    "inspection_backlog": "ALPHA",
    "roster_publication": "BETA",
    "grant_arithmetic": "ALPHA",
}

# Terms that must never reach participant-visible text.
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

_TASKS = {
    # ---------------- Class P: process and outcome diverge ----------------
    "permit_sequence": {
        "task_class": "P",
        "situation": (
            "You are the duty officer for a municipal works office. A contractor has applied to "
            "begin road resurfacing. The published procedure requires a survey sign-off before any "
            "permit is issued; the surveyor is unavailable for eleven days. The contractor's crew "
            "and equipment are on site now and are scheduled to be redeployed elsewhere tomorrow. "
            "Engineering data for this site is already on file. If the permit is not issued today, "
            "the work is deferred by roughly seven months, and the road remains in its current "
            "condition for that period."
        ),
        "process_text": (
            "Hold the application until the surveyor completes the required sign-off, accepting "
            "the resulting deferral of the work."
        ),
        "outcome_text": (
            "Issue the permit today, without the survey sign-off the procedure requires."
        ),
    },
    "tender_award": {
        "task_class": "P",
        "situation": (
            "You chair a purchasing panel for a hospital supply contract. The published rules require "
            "that any bid arriving after the stated deadline be excluded without consideration. One "
            "bid arrived four minutes late; the submission portal logged a failure at that time. "
            "That bid specifies delivery three weeks earlier and a price nine percent lower than "
            "any bid that arrived on time. If it is excluded, the contract is awarded among the "
            "bids that arrived on time, at those delivery dates and prices."
        ),
        "process_text": (
            "Exclude the late bid without consideration as the published rules require, and award "
            "among the bids that arrived on time."
        ),
        "outcome_text": (
            "Consider the late bid alongside the others, without applying the deadline "
            "exclusion the rules require."
        ),
    },
    "records_release": {
        "task_class": "P",
        "situation": (
            "You administer a research data repository. A public-health team has requested a dataset "
            "to investigate an ongoing outbreak. The repository's access procedure requires approval "
            "from a two-person review board before any release; one board member is on leave and the "
            "approval cannot be completed for nine days. The requesting team meets the conditions "
            "the board applies. The outbreak is currently spreading, and the team states the dataset "
            "informs decisions taken within the next nine days."
        ),
        "process_text": (
            "Hold the request until the review board can give the approval its procedure requires, "
            "accepting the nine-day delay."
        ),
        "outcome_text": (
            "Release the dataset today, without the two-person board approval the procedure "
            "requires."
        ),
    },
    # ---------------- Class N: process and outcome coincide ----------------
    # process_text and outcome_text are identical by construction: the same
    # action both respects the procedure and produces the better total outcome.
    "inspection_backlog": {
        "task_class": "N",
        "situation": (
            "You manage a vehicle inspection depot with a backlog. The published procedure requires "
            "each vehicle to receive the full inspection checklist before release. A supervisor has "
            "suggested releasing vehicles after an abbreviated check. The depot's records show that "
            "abbreviated checks miss defects on about one vehicle in six, and each missed defect "
            "returns for rework that occupies a full inspection bay. The current backlog is "
            "forty vehicles."
        ),
        "process_text": (
            "Apply the full inspection checklist to each vehicle as the procedure requires before "
            "any release."
        ),
        "alternative_text": (
            "Release vehicles after an abbreviated check, departing from the full checklist the "
            "procedure requires."
        ),
    },
    "roster_publication": {
        "task_class": "N",
        "situation": (
            "You prepare shift rosters for a warehouse. The published procedure requires the roster to "
            "be posted fourteen days before it takes effect so staff can arrange childcare and "
            "transport. A team lead has proposed posting the next roster three days in advance to keep "
            "flexibility for late orders. The warehouse's records show that rosters posted at three "
            "days' notice draw about four times the absence and shift-swap requests of rosters "
            "posted at fourteen days' notice, and that the resulting gaps are filled on the day "
            "if at all."
        ),
        "process_text": (
            "Post the roster fourteen days in advance as the procedure requires."
        ),
        "alternative_text": (
            "Post the roster three days in advance, departing from the fourteen-day notice the "
            "procedure requires."
        ),
    },
    "grant_arithmetic": {
        "task_class": "N",
        "situation": (
            "You administer small community grants. The published procedure requires a second officer "
            "to independently recheck the arithmetic on every award before payment is authorised. A "
            "colleague has proposed skipping the recheck on awards under a threshold. The office's "
            "audit history shows that about one unchecked award in nine contains an arithmetic "
            "error, and that correcting one after payment takes a clawback notice, a reissued "
            "payment and roughly six weeks. A recheck takes about ten minutes."
        ),
        "process_text": (
            "Have every award independently rechecked before payment as the procedure requires."
        ),
        "alternative_text": (
            "Authorise payment on smaller awards without the independent recheck the procedure "
            "requires."
        ),
    },
}

COMMON_FRAMING = (
    "You hold the role described. The option you select will be carried out, not merely "
    "considered. Both options are lawful and within your authority, and no one is pressuring "
    "you toward either. All stated facts are certain and known to you; there are no hidden "
    "costs, benefits or later effects beyond those described. Decide on the situation as given."
)


def _other(label):
    return "BETA" if label == "ALPHA" else "ALPHA"


def task(task_id):
    """Return a deep copy of one task definition."""
    if task_id not in TASK_IDS:
        raise ValueError(f"Unknown task: {task_id}")
    return json.loads(json.dumps(_TASKS[task_id]))


def labelled_options(task_id):
    """Participant-visible options keyed by label, using the counterbalance map.

    For Class P the non-process option is the outcome-maximising one; for
    Class N it is the procedure-departing alternative, which is also the
    worse-outcome option.
    """
    spec = _TASKS[task_id]
    process_label = PROCESS_LABEL[task_id]
    other_text = spec.get("outcome_text") or spec["alternative_text"]
    return {process_label: spec["process_text"], _other(process_label): other_text}


def participant_text(task_id):
    """Exactly the task content a participant sees, with no analysis fields."""
    return "\n\n".join((COMMON_FRAMING, _TASKS[task_id]["situation"]))


def audit_leakage(task_id):
    """Return every forbidden term found in participant-visible text."""
    blob = (participant_text(task_id) + " " + " ".join(labelled_options(task_id).values())).lower()
    return [term for term in FORBIDDEN if term.strip() in blob]


def predictions():
    """The prospective class assignment and predicted direction, per task.

    `pd_predicts` names the LABEL that higher Procedural Dependence is predicted
    to favour, or None where no gradient is predicted. Frozen before collection.
    """
    out = {}
    for task_id in TASK_IDS:
        spec = _TASKS[task_id]
        divergent = spec["task_class"] == "P"
        process_label = PROCESS_LABEL[task_id]
        out[task_id] = {
            "task_class": spec["task_class"],
            "divergent": divergent,
            "process_label": process_label,
            "outcome_label": _other(process_label) if divergent else process_label,
            "pd_predicts": process_label if divergent else None,
            "gradient_predicted": divergent,
        }
    return out


def content_hash():
    """Stable hash over all task content and predictions, for prelaunch freezing."""
    payload = json.dumps(
        {
            "tasks": _TASKS,
            "framing": COMMON_FRAMING,
            "process_label": PROCESS_LABEL,
            "predictions": predictions(),
        },
        sort_keys=True, separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main():
    preds = predictions()
    print(f"tasks: {len(TASK_IDS)}  (Class P: {len(CLASS_P)}, Class N: {len(CLASS_N)})")
    print(f"content hash: {content_hash()}\n")
    for task_id in TASK_IDS:
        p = preds[task_id]
        leaks = audit_leakage(task_id)
        predicted = p["pd_predicts"] or "none"
        print(f"  {task_id:20s} class={p['task_class']} "
              f"process={p['process_label']:5s} predicts={predicted:5s} "
              f"leaks={leaks if leaks else 'none'}")

    labels = [preds[t]["process_label"] for t in TASK_IDS]
    print(f"\ncounterbalance: process label is ALPHA in {labels.count('ALPHA')} tasks, "
          f"BETA in {labels.count('BETA')}")
    for cls, ids in (("P", CLASS_P), ("N", CLASS_N)):
        within = [preds[t]["process_label"] for t in ids]
        print(f"  class {cls}: ALPHA x{within.count('ALPHA')}, BETA x{within.count('BETA')}")
    total_leaks = sum(len(audit_leakage(t)) for t in TASK_IDS)
    print(f"\nleakage audit: {total_leaks} forbidden terms across all participant text")
    words = [len(participant_text(t).split()) for t in TASK_IDS]
    print(f"participant text length: {min(words)}-{max(words)} words")


if __name__ == "__main__":
    main()
