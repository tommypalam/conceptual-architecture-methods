"""Prospective PD gradient collector (pd_gradient_r4); frozen evidence is never edited.

Revision of r3, which stopped at review with verdict `reject`. The accepted
finding was that r2/r3 wording no longer established Class P membership. r4
carries the trade-off in stipulated quantities and derives class membership from
those totals, so the defect cannot recur silently. See
../experiments/phase3_benchmarks/pd_gradient_r3/ASSESSMENT.md.

Identical design to r2. r2 was re-designated only because its collector source
was corrected after its release was frozen, and the write-once rule forbids
overwriting a frozen artifact. No task, seed, estimand or gate changed; see
../experiments/phase3_benchmarks/pd_gradient_r2/STATUS.md.

Revision of r1, which stopped at review with verdict `revise`. Three repairs:
  - Every job is tagged kind "probe". The shared parse() returns response text
    verbatim only for that kind; any other kind is forced through a ratings
    schema, which is what rejected r1's well-formed review response.
  - The review packet no longer contains a rendered profile block, which had
    carried all ten coordinate names to the reviewer.
  - The leakage gate now audits the review packet as well as participant text.

Three stages, each gated on the one before:

  1. review      - one independent design review of the task set. A non-accept
                   verdict stops the study with zero participant calls.
  2. screen      - 25 unprofiled calls per task. Any task whose modal share is
                   1.00 is rejected as saturated; if that leaves fewer than six
                   usable tasks the study stops rather than substituting.
  3. participants - 120 profiled decisions per surviving task.

The screen decides only whether a task can discriminate, never which result is
wanted: it runs with no profile, before any profiled call exists, and its
threshold is fixed here. Screen outcomes for every task are reported.
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from engine.population import Population
from phase3_budget import BudgetStop, POLICY, canonical, digest, read_checked, token_cost_nano
from phase3_design_pilot import request, RATERS, JUDGE, PRICES
from phase3_design_pilot_r2 import review_value
from phase3_protocol_kernel import context_prompt, AXES
from phase3_recognition_recovery import verify, sha
from phase3_recognition_run import ROOT, LEDGER, Ledger, network, charge, MODELS
from phase3_representation_diagnostic import profile_parts
from phase3_variant_round import save

import phase3_pd_gradient_tasks_r4 as T

FOLDER = ROOT / "experiments/phase3_benchmarks/pd_gradient_r4"
# The ledger chain advances across phases: the parent is whichever study last
# wrote to the ledger, which is the Phase 4 finite-rule pilot, not the Phase 3
# transfer pilot. Chaining to a stale release fails the reservation audit.
# r1 is the correct parent: its release records the ledger state r2 inherits,
# including r1's own review slot. It stopped at its review gate and never wrote a
# CHECKPOINT, so the parent-checkpoint field below falls back to its release.
# r1's failed slot and full charge are carried forward untouched.
PARENT = ROOT / "experiments/phase3_benchmarks/pd_gradient_r3"
STUDY = "pd_gradient_r4"

N_PER_TASK = 120
SCREEN_N = 25
SCREEN_REJECT_AT = 1.0          # modal share that disqualifies a task
# Worst-case reservation, not expected spend: the bound charges the full input
# bound (utf-8 bytes + 1024, which over-counts tokens roughly 4x) plus the full
# max_output at output price, for every call. Prior studies settled near 17% of
# reservation (transfer_pilot_r1: $1.785 reserved, $0.302 actual). Set to cover
# the full three-stage batch: $3.450130 computed, $3.50 ceiling.
CAP = 3_500_000_000             # 3.50 USD hard ceiling for this designation
SEEDS = {"population": 2026091507, "schedule": 2026091508, "analysis": 2026091509}
NEUTRAL = dict.fromkeys(AXES, "NEUTRAL")
PARTICIPANT = RATERS[1]

# r1's review slot failed and is preserved at full reservation under the no-retry
# rule. r2 inherits exactly that one failure and names it explicitly, rather than
# broadly ignoring failures, so any NEW unresolved dispatch still stops the study.
INHERITED_FAILURE = "pd_gradient_r1/review/0"


PARAMETERS = ("LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW")
_PLACEHOLDER = dict.fromkeys(PARAMETERS, 0.5)


def system(profile=None):
    """System prompt. profile=None is the unprofiled screen arm.

    `context_prompt` requires all ten coordinates, so the unprofiled arm is
    built from a placeholder and then has its profile block removed entirely -
    the same strip-the-block construction the transfer pilot used for its U arm.
    The placeholder values never reach the prompt.
    """
    original = context_prompt(dict(profile) if profile else _PLACEHOLDER, NEUTRAL)
    prefix, block, suffix = profile_parts(original)
    suffix = suffix[:suffix.index("# Your task")] + (
        "# Your task\nUse the supplied information to make the requested decision. "
        "Do not infer a demographic identity or additional facts. "
        "Return only the requested JSON object.\n")
    return prefix + (block if profile else "") + suffix


def body(task_id, first):
    """Participant-visible task text. `first` fixes which label is shown first."""
    options = T.labelled_options(task_id)
    order = ("ALPHA", "BETA") if first else ("BETA", "ALPHA")
    listed = "\n".join(f'Option {label}: {options[label]}' for label in order)
    return "\n\n".join((
        T.participant_text(task_id),
        "# Options\n" + listed,
        'Return JSON only: {"choice":"ALPHA"} or {"choice":"BETA"}.',
    ))


def make_job(slot, stage, system_text, text, maximum=64):
    """kind is always "probe": the shared parse() returns text verbatim only for
    that kind, and forces every other kind through a ratings schema."""
    bound = len((system_text + text).encode("utf-8")) + 1024
    req = request(PARTICIPANT, system_text, text, maximum, temperature=1)
    req["response_format"] = {"type": "json_object"}
    return {"slot": f"{STUDY}/{slot}", "kind": "probe", "stage": stage, "request": req,
            "input_token_bound": bound,
            "reserved_nano": token_cost_nano(bound, maximum, *PRICES[PARTICIPANT])}


def screen_jobs():
    """Unprofiled dispersion probes: SCREEN_N per task, no profile block."""
    batch = []
    for task_id in T.TASK_IDS:
        for i in range(SCREEN_N):
            job = make_job(f"screen/{task_id}/{i}", "screen", system(None),
                           body(task_id, first=(i % 2 == 0)))
            job["cell"] = {"stage": "screen", "task": task_id, "index": i}
            batch.append(job)
    return batch


def participant_jobs(population, tasks):
    batch = []
    for agent in population["agents"]:
        block = []
        for task_id in tasks:
            # Label order alternates deterministically so presentation cannot
            # align with the counterbalanced process label.
            first = (agent["agent_id"] + T.TASK_IDS.index(task_id)) % 2 == 0
            job = make_job(f"participant/{agent['agent_id']}/{task_id}", "participant",
                           system(agent["parameters"]), body(task_id, first))
            job["cell"] = {"stage": "participant", "task": task_id,
                           "agent_id": agent["agent_id"], "first": "ALPHA" if first else "BETA",
                           "pd": agent["parameters"]["PD"],
                           "task_class": T.predictions()[task_id]["task_class"],
                           "process_label": T.predictions()[task_id]["process_label"]}
            block.append(job)
        random.Random(SEEDS["schedule"] + agent["agent_id"]).shuffle(block)
        batch.extend(block)
    return batch


def review_packet():
    """Exactly what the reviewer sees. Audited by leakage_gate before dispatch."""
    return {
        "tasks": {t: {"situation": T.participant_text(t),
                      "options": T.labelled_options(t)} for t in T.TASK_IDS},
        "claimed_classes": {t: T.predictions()[t]["task_class"] for t in T.TASK_IDS},
        "stipulated_totals": {t: {"unit": T.predictions()[t]["unit"],
                                  "following_procedure": T.predictions()[t]["process_total"],
                                  "departing_from_procedure": T.predictions()[t]["depart_total"]}
                              for t in T.TASK_IDS},
    }


def review_job():
    packet = review_packet()
    return make_job("review/0", "review", (
        "Review this prospective design independently. For each task decide whether it truly "
        "belongs to its claimed class, checking the stipulated totals: class P is where departing "
        "from the procedure yields the strictly higher stipulated total, class N is where "
        "following it does. The totals are stipulated facts of the scenario, not claims to "
        "verify externally. Also check that no task reveals a preferred answer, "
        "names a psychological parameter, or is recognisable as a classic paradigm. Flag any "
        "blocking issue. Do not accept merely because the design could show an effect. Return "
        "only JSON with verdict accept/revise/reject, blocking_issues list, limits list. "
        "Keep the entire JSON under 150 words."),
        json.dumps(packet, ensure_ascii=False, sort_keys=True), 1024)


def leakage_gate():
    """Refuse to build a batch whose participant text leaks the hypothesis."""
    found = {t: T.audit_leakage(t) for t in T.TASK_IDS}
    leaking = {t: v for t, v in found.items() if v}
    if leaking:
        raise BudgetStop(f"Task text leaks hypothesis terms: {leaking}")
    labels = [T.PROCESS_LABEL[t] for t in T.TASK_IDS]
    if labels.count("ALPHA") != 3 or labels.count("BETA") != 3:
        raise BudgetStop("Process label is not counterbalanced 3/3")
    for ids in (T.CLASS_P, T.CLASS_N):
        if len({T.PROCESS_LABEL[t] for t in ids}) != 2:
            raise BudgetStop("A task class is label-constant")
    # r1's gate audited participant text only, so a rendered profile block in the
    # review packet carried all ten coordinate names to the reviewer unnoticed.
    packet = json.dumps(review_packet(), ensure_ascii=False).lower()
    in_packet = sorted({term.strip() for term in T.FORBIDDEN if term.strip() in packet})
    if in_packet:
        raise BudgetStop(f"Review packet leaks hypothesis terms: {in_packet}")
    # r3's accepted defect: wording stopped establishing Class P membership.
    # Class is now derived from the stipulated totals, not trusted from the label.
    classes = T.verify_classes()
    return {"forbidden_terms_found": 0, "counterbalanced": True,
            "review_packet_clean": True, "classes_verified_from_totals": classes,
            "task_content_sha256": T.content_hash()}


def choice(text):
    def unique(pairs):
        if len({k for k, _ in pairs}) != len(pairs):
            raise ValueError("Duplicate JSON key")
        return dict(pairs)
    try:
        value = json.loads(text, object_pairs_hook=unique)
        if not isinstance(value, dict) or set(value) != {"choice"}:
            return None
        return value["choice"] if value["choice"] in ("ALPHA", "BETA") else None
    except (ValueError, TypeError):
        return None


def screen_outcome(rows):
    """Modal share per task, and which tasks survive the saturation gate."""
    out = {}
    for task_id in T.TASK_IDS:
        votes = [r["choice"] for r in rows if r["task"] == task_id and r["choice"]]
        if not votes:
            out[task_id] = {"n_valid": 0, "modal_share": None, "usable": False,
                            "reason": "no valid screen responses"}
            continue
        modal = max(votes.count(v) for v in set(votes)) / len(votes)
        usable = modal < SCREEN_REJECT_AT
        out[task_id] = {"n_valid": len(votes), "modal_share": round(modal, 4),
                        "usable": usable,
                        "reason": "usable" if usable else "deterministic baseline; cannot discriminate",
                        "near_ceiling": bool(usable and modal >= 0.85)}
    return out


def analyze(rows, screen, n):
    """Per-task PD correlation on the process-respecting option, plus the P-N contrast."""
    from phase3_pd_gradient_power import point_biserial

    preds = T.predictions()
    usable = [t for t in T.TASK_IDS if screen[t]["usable"]]
    tasks_out, rng = {}, random.Random(SEEDS["analysis"])
    for task_id in usable:
        subset = [r for r in rows if r["task"] == task_id]
        if len(subset) != n:
            raise BudgetStop(f"Missing or duplicate decisions for {task_id}")
        process_label = preds[task_id]["process_label"]
        pd_values = [r["pd"] for r in subset if r["choice"]]
        picked = [1 if r["choice"] == process_label else 0 for r in subset if r["choice"]]
        r_obs = point_biserial(pd_values, picked)
        entry = {"task_class": preds[task_id]["task_class"],
                 "gradient_predicted": preds[task_id]["gradient_predicted"],
                 "n_assigned": len(subset), "n_valid": len(picked),
                 "process_rate": round(sum(picked) / len(picked), 4) if picked else None,
                 "r_pd_process": None if r_obs is None else round(r_obs, 4),
                 "perm_p": None}
        if r_obs is not None:
            shuffled, hits = list(picked), 0
            for _ in range(10_000):
                rng.shuffle(shuffled)
                alt = point_biserial(pd_values, shuffled)
                if alt is not None and abs(alt) >= abs(r_obs):
                    hits += 1
            entry["perm_p"] = (hits + 1) / 10_001
        tasks_out[task_id] = entry

    def mean_r(class_name):
        values = [v["r_pd_process"] for v in tasks_out.values()
                  if v["task_class"] == class_name and v["r_pd_process"] is not None]
        return round(sum(values) / len(values), 4) if values else None

    p_mean, n_mean = mean_r("P"), mean_r("N")
    return {"study": STUDY, "screen": screen, "tasks": tasks_out,
            "mean_r_class_P": p_mean, "mean_r_class_N": n_mean,
            "primary_contrast_P_minus_N": (None if p_mean is None or n_mean is None
                                           else round(p_mean - n_mean, 4)),
            "analysis_status": "prospective; sign of the result is not a success gate",
            "phase3_pass": None, "moral_scores_assigned": False}


def prepare(persist=False):
    leak = leakage_gate()
    parent = read_checked(PARENT / "release.json")
    # r1 stopped before archiving, so it has no CHECKPOINT; fall back to its
    # release for the provenance digest rather than inventing one.
    checkpoint_path = PARENT / "CHECKPOINT.json"
    check = read_checked(checkpoint_path) if checkpoint_path.exists() else parent
    verify(parent)
    with Ledger(LEDGER, parent) as ledger:
        if ledger.state["pending"] or ledger.state["failed"] != [digest(INHERITED_FAILURE)]:
            raise BudgetStop("Unexpected unresolved dispatch in inherited evidence")
        providers = dict(ledger.state["providers"])

    population = Population.draw(N_PER_TASK, seed=SEEDS["population"]).to_dict()
    batch = [review_job()] + screen_jobs() + participant_jobs(population, T.TASK_IDS)
    # dispatch() checks job["kind"] against cap["kind"], so the slot record must
    # carry "kind"; the descriptive stage name rides alongside it.
    slots = {j["slot"]: {"kind": j["kind"], "stage": j["stage"], "model": j["request"]["model"],
                         "input_token_bound": j["input_token_bound"],
                         "reserved_nano": j["reserved_nano"],
                         "max_output": j["request"].get("max_tokens",
                                                        j["request"].get("max_completion_tokens")),
                         "request_sha256": digest(j["request"])} for j in batch}
    bound = sum(j["reserved_nano"] for j in batch)
    for j in batch:
        providers[MODELS[j["request"]["model"]]] += j["reserved_nano"]

    expected = 1 + SCREEN_N * len(T.TASK_IDS) + N_PER_TASK * len(T.TASK_IDS)
    if len(slots) != expected or bound > CAP:
        raise BudgetStop(f"Size or cap exceeded: {len(slots)} calls, {bound / 1e9:.6f} USD")
    if providers["anthropic"] > 11_000_000_000 or providers["openai"] > 20_000_000_000:
        raise BudgetStop("Moral capstone reserve would be consumed")

    paths = [Path(__file__), ROOT / "code/phase3_pd_gradient_tasks.py",
             ROOT / "code/phase3_pd_gradient_power.py", FOLDER / "PROTOCOL.md",
             ROOT / "code/engine/population.py", ROOT / "code/utils.py",
             ROOT / "code/phase3_protocol_kernel.py",
             ROOT / "prompts/system_prompt_template.md"]
    release = {"id": STUDY, "population_sha256": digest(population), "jobs_sha256": digest(batch),
               "slots": slots, "recognition_cap_nano": bound, "prior_screening_nano": 0,
               "original_screening_cap_nano": CAP,
               "provider_caps_nano": parent["provider_caps_nano"],
               "parent_checkpoint_sha256": digest(check), "leakage_gate": leak,
               "historical_keys": sorted(p.stem for p in (LEDGER / "records").glob("*.json")),
               "preserved_files": {p.relative_to(LEDGER).as_posix(): sha(p)
                                   for p in LEDGER.rglob("*.json")},
               "failure_log_prefix_bytes": (LEDGER / "failures.jsonl").stat().st_size,
               "failure_log_prefix_sha256": sha(LEDGER / "failures.jsonl"),
               "source_sha256": {**parent["source_sha256"],
                                 **{p.relative_to(ROOT).as_posix(): sha(p) for p in paths}}}
    with Ledger(LEDGER, release):
        pass
    if persist:
        save(FOLDER / "population.json", population)
        save(FOLDER / "requests.json", batch)
        save(FOLDER / "release.json", release)
    return release, population, batch


def collect(replay=False, root=LEDGER, folder=FOLDER, responder=network, test_data=None):
    root, folder = Path(root), Path(folder)
    if root == LEDGER and test_data is not None:
        raise BudgetStop("Test data on real ledger")
    leakage_gate()
    release, pop, batch = test_data or tuple(
        read_checked(folder / f) for f in ("release.json", "population.json", "requests.json"))
    verify(release, root)
    if digest(pop) != release["population_sha256"] or digest(batch) != release["jobs_sha256"]:
        raise BudgetStop("Changed population or requests")
    if batch != [review_job()] + screen_jobs() + participant_jobs(pop, T.TASK_IDS):
        raise BudgetStop("Reconstructed schedule differs")
    if release["leakage_gate"]["task_content_sha256"] != T.content_hash():
        raise BudgetStop("Task content changed after release")

    manifest = {"release_sha256": digest(release), "jobs_sha256": digest(batch)}
    save(folder / "execution_manifest.json", manifest)
    n_screen = SCREEN_N * len(T.TASK_IDS)

    with Ledger(root, release) as ledger:
        # Against r2's own release the r1 failure is historical, so `failed` is
        # empty here; in prepare() it is still live against the parent release.
        # Either state is acceptable, anything else is not.
        if ledger.state["pending"] or ledger.state["failed"] not in ([], [digest(INHERITED_FAILURE)]):
            raise BudgetStop("Unexpected unresolved dispatch")
        seen = set()

        def dispatch(job):
            record, _ = ledger.dispatch(job, digest(manifest), responder, replay)
            if charge(record["raw"], job, False) != record["accounted_nano"]:
                raise BudgetStop("Cost replay mismatch")
            seen.add(digest(job["slot"]))
            return record["parsed"]

        review = review_value(dispatch(batch[0]))
        print(json.dumps({"review": review,
                          "accounted_usd": ledger.state["recognition_nano"] / 1e9}), flush=True)

        if review["verdict"] != "accept":
            result = {"study": STUDY, "decision": "review_stop",
                      "screen_calls": 0, "participant_calls": 0, "phase3_pass": None}
        else:
            screen_rows = [{**j["cell"], "choice": choice(dispatch(j))}
                           for j in batch[1:1 + n_screen]]
            screen = screen_outcome(screen_rows)
            save(folder / "screen_rows.json", screen_rows)
            print(json.dumps({"screen": screen}), flush=True)

            rejected = [t for t, v in screen.items() if not v["usable"]]
            if rejected:
                result = {"study": STUDY, "decision": "screen_stop", "screen": screen,
                          "rejected_tasks": rejected, "screen_calls": len(screen_rows),
                          "participant_calls": 0, "phase3_pass": None,
                          "note": ("Saturated tasks cannot discriminate any arm contrast. "
                                   "Replacement requires a new linked designation.")}
            else:
                rows = []
                for i, job in enumerate(batch[1 + n_screen:], 1):
                    rows.append({**job["cell"], "choice": choice(dispatch(job))})
                    if i % 120 == 0:
                        print(json.dumps({"completed": i,
                                          "assigned": len(batch) - 1 - n_screen,
                                          "accounted_usd": ledger.state["recognition_nano"] / 1e9}),
                              flush=True)
                save(folder / "scored_rows.json", rows)
                result = analyze(rows, screen, N_PER_TASK)
                result["screen_calls"] = len(screen_rows)
                result["participant_calls"] = len(rows)

        if set(ledger.state["reservations"]) - set(release["historical_keys"]) != seen:
            raise BudgetStop("Unmanifested dispatch")
        result.update(review=review, calls=len(seen),
                      accounted_nano=ledger.state["recognition_nano"],
                      provider_totals_nano=ledger.state["providers"],
                      release_sha256=digest(release))
        save(folder / "results.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("prepare", "run"))
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args()
    if args.command == "prepare":
        release, _, batch = prepare(True)
        print(json.dumps({"maximum_usd": release["recognition_cap_nano"] / 1e9,
                          "screen_calls": SCREEN_N * len(T.TASK_IDS),
                          "participant_calls": N_PER_TASK * len(T.TASK_IDS),
                          "total_calls": len(batch), "root_seed": SEEDS["population"]}))
    else:
        if not args.yes:
            raise BudgetStop("Explicit execution flag required")
        print(json.dumps(collect()))
