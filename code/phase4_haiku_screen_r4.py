"""Per-model dispersion screen on claude-haiku-4-5; frozen evidence is never edited.

Screen ONLY. Collects unprofiled decisions on the conflict tasks whose net
primary can discriminate, and reports their baseline dispersion on the model a
study would actually run on. No profiled arm, no moral score, no participant.

**Why this designation exists.** `capstone_model2_r4` ran the gpt-screened
four-task pool on haiku and found three tasks at a ceiling of 1.000 and one at a
floor of 0.000. Its three null contrasts therefore sat on cells with no room to
move, and measured nothing about the estimand. The one cell with headroom moved
(+0.133, Holm 0.0276; G-U +0.200, p=0.0005).

The requirement carried out of Phase 3 is to screen for dispersion BEFORE
building a study. That requirement was met on gpt-5.4-mini and then not repeated
when the model changed. Where a baseline sits is model-specific in the ordinary
way model bias is; whether profiles move behaviour is a separate question that a
saturated cell cannot ask. This screen re-runs the gate on the new model so the
question can be asked properly, on tasks that vary there.

Seven of the eleven conflict tasks have never been screened on any model but
gpt-5.4-mini, including `referral_fee` and `audit_sampling`, excluded there for
gpt-specific saturation. Those exclusions carry no information about haiku.

Screening is on baseline dispersion only, never on outcomes. The threshold is
fixed here, the screen runs with no profile before any profiled call exists, and
every task's outcome is reported whether it survives or not.

**Revision of r2 and r1, both of which died on the same path in different
halves.** Neither collected a screen probe; both lost their review call and are
preserved at full reservation under the no-retry rule.

  - r1 routed the probes through the provider-agnostic dispatcher but left the
    review on the shared parser, whose `probe` contract caps a reply at 1024
    bytes. Haiku returned a complete, well-formed 1,592-byte fenced verdict.
  - r2 routed the review through the agnostic dispatcher, which at that point
    had only a choice parser and rejected the verdict for not being an action id.

r3 fixes the cause rather than the symptom. `phase4_crossmodel_dispatch` now
offers two contracts a job declares explicitly and exclusively - `valid_actions`
for a task choice, `raw_text` for a complete reply - sharing one usage guard,
stop-reason check and truncation rule. A job declaring both or neither raises.
Every call in this module goes through that one dispatcher, so there is no
routing split left to get half right. The choice path was re-verified after the
change against all 960 stored `capstone_model2_r4` decisions: 960 identical,
zero differences.

Two stages, the second gated on the first:

  1. review  - one independent design review of the task set. Advisory under the
               16 September amendment for already-accepted material; recorded
               either way.
  2. screen  - 25 unprofiled calls per task. Modal share 1.00 disqualifies a task
               as saturated. Surviving tasks become eligible for a separately
               designated profiled study; this run collects none.
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
from phase4_crossmodel_dispatch import dispatch as crossmodel_dispatch
from phase3_representation_diagnostic import profile_parts
from phase3_variant_round import save

import phase4_all_conflict_pool as T

FOLDER = ROOT / "experiments/phase4_coding/haiku_screen_r4"
# The ledger chain advances across phases: the parent is whichever study last
# wrote to the ledger, which is the Phase 4 finite-rule pilot, not the Phase 3
# transfer pilot. Chaining to a stale release fails the reservation audit.
# r1 is the correct parent: its release records the ledger state r2 inherits,
# including r1's own review slot. It stopped at its review gate and never wrote a
# CHECKPOINT, so the parent-checkpoint field below falls back to its release.
# r1's failed slot and full charge are carried forward untouched.
PARENT = ROOT / "experiments/phase4_coding/haiku_screen_r3"
STUDY = "haiku_screen_r4"

# The six screened tasks are byte-identical to material accepted by four prior
# independent reviews. Under the 16 September amendment the review is therefore
# advisory here: recorded and assessed, but not a gate. A NEW or MODIFIED task
# would set this False and restore the hard gate.
REVIEW_ADVISORY = True

N_AGENTS = 60
LEVELS = (0.1, 0.9)   # PD endpoints; all other coordinates hold the drawn value
SCREEN_N = 25
SCREEN_REJECT_AT = 1.0          # modal share that disqualifies a task
# Worst-case reservation, not expected spend: the bound charges the full input
# bound (utf-8 bytes + 1024, which over-counts tokens roughly 4x) plus the full
# max_output at output price, for every call. Prior studies settled near 17% of
# reservation (transfer_pilot_r1: $1.785 reserved, $0.302 actual). Set to cover
# the full three-stage batch: $3.450130 computed, $3.50 ceiling.
CAP = 3_500_000_000             # 3.50 USD hard ceiling for this designation
SEEDS = {"population": 2026091649, "schedule": 2026091650, "analysis": 2026091651}
NEUTRAL = dict.fromkeys(AXES, "NEUTRAL")
# Screening the model the study will actually run on. That is the whole point:
# where a baseline sits is model-specific, so the screen must be too.
PARTICIPANT = RATERS[0]   # claude-haiku-4-5-20251001
# Only tasks whose net primary can differ between options; a constant primary
# cannot show an arm difference on any model.
SCREEN_TASKS = tuple(t for t in T.TASK_IDS if T.primary_discriminates(t))

# r1's review slot failed and is preserved at full reservation under the no-retry
# rule. r2 inherits exactly that one failure and names it explicitly, rather than
# broadly ignoring failures, so any NEW unresolved dispatch still stops the study.
# r1 and r2 each lost their review call and are preserved at full reservation
# under the no-retry rule. r3 inherits exactly those two failures and names them,
# rather than broadly ignoring failures, so any NEW unresolved dispatch still
# stops the study.
#   r1: routed the review through the shared parser, which caps a probe at 1024
#       bytes; haiku returned a complete 1,592-byte fenced verdict.
#   r2: routed the review through the agnostic dispatcher, which then had only a
#       choice parser and rejected a verdict for not being an action id.
INHERITED_FAILURES = ("haiku_screen_r1/review/0", "haiku_screen_r2/review/0")

# r3's review call SUCCEEDED and is not a failure. It returned verdict `reject`
# with six blocking issues, at a charge of $0.003896200, and is preserved in the
# ledger exactly as returned. r4 re-designates only because r3's collector source
# was corrected after its release was frozen - the verdict key `overall_verdict`
# was unreadable, and the 16 September advisory rule was not applied - and the
# write-once rule forbids overwriting a frozen artifact.
#
# THE REVIEW IS NOT RE-RUN. r4 reads r3's recorded response from the ledger. No
# task, threshold, estimand or gate changed. Re-rolling a review to obtain a
# different verdict remains forbidden and has not occurred.
INHERITED_REVIEW = "haiku_screen_r3/review/0"


# Which inherited-failure states are acceptable. Against the parent release the
# r2 failure may still be live; against r3's own release both are historical and
# `failed` is empty. Any other value is a new unresolved dispatch and stops.
_ACCEPTABLE_FAILED = ([],
                      [digest(INHERITED_FAILURES[1])],
                      [digest(f) for f in INHERITED_FAILURES])


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
    """Participant-visible text. `first` fixes which option is listed first."""
    ids = list(T.action_ids(task_id))
    if not first:
        ids.reverse()
    spec = T.task(task_id)
    lines = [f"Option {a.upper()}: {spec['actions'][a]['description']} "
             f"{spec['actions'][a]['effect_text']}" for a in ids]
    options = "# Options" + chr(10) + chr(10).join(lines)
    instruction = 'Return JSON only: {"choice":"<OPTION NAME>"}.'
    sep = chr(10) + chr(10)
    return sep.join((T.COMMON_FRAMING, spec["situation"], options, instruction))



def make_job(slot, stage, system_text, text, maximum=768):
    """kind is always "probe": the shared parse() returns text verbatim only for
    that kind, and forces every other kind through a ratings schema."""
    bound = len((system_text + text).encode("utf-8")) + 1024
    req = request(PARTICIPANT, system_text, text, maximum, temperature=1)
    if MODELS[PARTICIPANT] == "openai":
        req["response_format"] = {"type": "json_object"}
    return {"slot": f"{STUDY}/{slot}", "kind": "probe", "stage": stage, "request": req,
            "input_token_bound": bound,
            "reserved_nano": token_cost_nano(bound, maximum, *PRICES[PARTICIPANT])}


def screen_jobs():
    """Unprofiled dispersion probes: SCREEN_N per task, no profile block."""
    batch = []
    for task_id in SCREEN_TASKS:
        for i in range(SCREEN_N):
            job = make_job(f"screen/{task_id}/{i}", "screen", system(None),
                           body(task_id, first=(i % 2 == 0)))
            job["valid_actions"] = sorted(a.lower() for a in T.action_ids(task_id))
            job["cell"] = {"stage": "screen", "task": task_id, "index": i}
            batch.append(job)
    return batch


def review_packet():
    """Exactly what the reviewer sees. Audited by leakage_gate before dispatch."""
    return {
        "tasks": {t: {"item": T.participant_text(t), "kind": "conflict"}
                  for t in SCREEN_TASKS},
    }


def review_job():
    packet = review_packet()
    job = make_job("review/0", "review", (
        "Review these decision items independently. Stipulated consequences are an "
        "intended and necessary part of every item; their presence is not a defect. "
        "Every item in this packet is a CONFLICT item and is declared as such: it must "
        "present a genuine conflict, with no option that is simply correct. There are "
        "no control items in this packet. Flag an item only if it has a plainly correct "
        "option, if the text states which option the decision-maker ought to choose "
        "beyond the stipulated facts, or if it names a psychological construct or "
        "reveals a study hypothesis. Do not accept merely because the design could show "
        "an effect. Return only JSON with an overall verdict accept/revise/reject, a "
        "blocking_issues list and a limits list. Under 150 words."),
        json.dumps(review_packet(), ensure_ascii=False, sort_keys=True), 1024)
    # Declares the raw-text contract exclusively: a review returns a verdict, not
    # an action id, so `parse_for` reads it verbatim under the same usage guard.
    # r1 and r2 both died here, each having fixed one half of this path.
    job["raw_text"] = True
    assert not job.get("valid_actions"), "Review job must not declare valid_actions"
    return job


def _json_objects(text):
    """Every balanced top-level {...} span in `text`, in order.

    A model that reasons before answering puts prose - and sometimes a fence -
    on both sides of the object. Scanning for balanced braces finds the object
    wherever it sits, without assuming the reply starts or ends with it. String
    literals are tracked so a brace inside a quoted value cannot unbalance it.
    """
    spans, depth, start, in_str, esc = [], 0, None, False, False
    for i, ch in enumerate(text or ""):
        if in_str:
            if esc:
                esc = False
            elif ch == chr(92):
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}" and depth:
            depth -= 1
            if depth == 0:
                spans.append(text[start:i + 1])
    return spans


def read_review(text):
    """Read a verdict from a reply in any shape these models actually produce.

    Three shapes have now been observed or anticipated, and all three are read
    here rather than being rejected on format:

      - a bare JSON object;
      - a fenced object;
      - an object preceded and/or followed by prose, fenced or not, which is how
        `claude-haiku-4-5` answers when it reasons before concluding.

    And two payload shapes: one overall verdict, or a per-task mapping, which is
    what haiku returned to r1.

    Output format is not part of the estimand, and the verdict is advisory for
    already-accepted material under the 16 September amendment, so this reads and
    records rather than gates. It never infers a verdict that is not stated: a
    reply with no parseable verdict object raises.
    """
    if isinstance(text, dict):
        return _shape(text)
    for span in _json_objects(text):
        try:
            value = json.loads(span)
        except ValueError:
            continue
        shaped = _shape(value)
        if shaped is not None:
            return shaped
    raise ValueError("No verdict in review response")


def _shape(value):
    """Normalise one parsed object to {verdict, blocking_issues, limits}, or None."""
    if not isinstance(value, dict) or not value:
        return None
    key = next((k for k in ("verdict", "overall_verdict", "overall") if k in value), None)
    if key:
        return {"verdict": str(value[key]).strip().lower(), "verdict_key": key,
                "blocking_issues": list(value.get("blocking_issues") or []),
                "limits": list(value.get("limits") or [])}
    if all(isinstance(v, dict) and ("verdict" in v or "overall_verdict" in v)
           for v in value.values()):
        verdicts = {k: str(v.get("verdict", v.get("overall_verdict"))).strip().lower()
                    for k, v in value.items()}
        overall = "accept" if all(x == "accept" for x in verdicts.values()) else "revise"
        return {"verdict": overall, "per_task": verdicts,
                "blocking_issues": [f"{k}: {i}" for k, v in value.items()
                                    for i in (v.get("blocking_issues") or [])],
                "limits": []}
    return None


def _inherited_review_text():
    """r3's recorded review response, read from the ledger. No API call.

    The verdict stands exactly as returned, reject included. This function exists
    so r4 cannot accidentally re-roll it.
    """
    record = read_checked(LEDGER / "records" / (digest(INHERITED_REVIEW) + ".json"))
    if record.get("error"):
        raise BudgetStop("Inherited review did not complete")
    return record["parsed"]


def leakage_gate():
    """Refuse to build a batch that leaks, editorialises, or lacks a real conflict."""
    leaks = {t: T.audit_leakage(t) for t in SCREEN_TASKS}
    if any(leaks.values()):
        raise BudgetStop("Task text leaks: " + str({k: v for k, v in leaks.items() if v}))
    comparatives = {t: T.audit_comparatives(t) for t in SCREEN_TASKS}
    if any(comparatives.values()):
        raise BudgetStop("Task text editorialises: "
                         + str({k: v for k, v in comparatives.items() if v}))
    conflict = T.verify_pool()
    allowed = {"tasks"}
    if set(review_packet()) - allowed:
        raise BudgetStop("Review packet carries non-task keys: "
                         + str(sorted(set(review_packet()) - allowed)))
    return {"forbidden_terms_found": 0, "no_comparatives": True,
            "pool_verified": conflict, "review_packet_clean": True,
            "task_content_sha256": T.content_hash()}


def choice(text, valid):
    """Strict parse; the choice must be one of this task's action ids."""
    def unique(pairs):
        if len({k for k, _ in pairs}) != len(pairs):
            raise ValueError("Duplicate JSON key")
        return dict(pairs)
    try:
        value = json.loads(text, object_pairs_hook=unique)
        if not isinstance(value, dict) or set(value) != {"choice"}:
            return None
        picked = str(value["choice"]).lower()
        return picked if picked in valid else None
    except (ValueError, TypeError):
        return None


def screen_outcome(rows, _tasks=None):
    """Modal share per task, and which tasks survive the saturation gate."""
    out = {}
    for task_id in SCREEN_TASKS:
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


def prepare(persist=False):
    leak = leakage_gate()
    parent = read_checked(PARENT / "release.json")
    # r1 stopped before archiving, so it has no CHECKPOINT; fall back to its
    # release for the provenance digest rather than inventing one.
    checkpoint_path = PARENT / "CHECKPOINT.json"
    check = read_checked(checkpoint_path) if checkpoint_path.exists() else parent
    verify(parent)
    with Ledger(LEDGER, parent) as ledger:
        # Against r3's release the r1 failure is already historical, so `failed`
        # is empty. Either state is acceptable; anything else stops the study.
        if ledger.state["pending"] or ledger.state["failed"] not in _ACCEPTABLE_FAILED:
            raise BudgetStop("Unexpected unresolved dispatch in inherited evidence")
        providers = dict(ledger.state["providers"])

    # Screen only: no profiles are drawn or used.
    population = {"n_agents": 0, "agents": [], "note": "screen-only designation"}
    batch = screen_jobs()   # review is inherited from r3, not re-dispatched
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

    expected = SCREEN_N * len(SCREEN_TASKS)
    if len(slots) != expected or bound > CAP:
        raise BudgetStop(f"Size or cap exceeded: {len(slots)} calls, {bound / 1e9:.6f} USD")
    # The inherited guard hard-coded $11 anthropic, reserving room under the
    # then-$15 ceiling. The researcher raised that ceiling to $32 (constitution
    # amendment, 15 September 2026). Check the actual ceilings.
    caps = {"anthropic": 32_000_000_000, "openai": 30_000_000_000}
    for provider, total in providers.items():
        if total > caps[provider]:
            raise BudgetStop(f"{provider} ceiling would be exceeded: "
                             f"{total / 1e9:.4f} > {caps[provider] / 1e9:.2f}")

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
    if batch != screen_jobs():
        raise BudgetStop("Reconstructed schedule differs")
    if release["leakage_gate"]["task_content_sha256"] != T.content_hash():
        raise BudgetStop("Task content changed after release")

    manifest = {"release_sha256": digest(release), "jobs_sha256": digest(batch)}
    save(folder / "execution_manifest.json", manifest)
    n_screen = SCREEN_N * len(SCREEN_TASKS)

    with Ledger(root, release) as ledger:
        # Against r2's own release the r1 failure is historical, so `failed` is
        # empty here; in prepare() it is still live against the parent release.
        # Either state is acceptable, anything else is not.
        if ledger.state["pending"] or ledger.state["failed"] not in _ACCEPTABLE_FAILED:
            raise BudgetStop("Unexpected unresolved dispatch")
        seen = set()

        def dispatch(job):
            # One dispatcher for every call. The job declares its contract and
            # `parse_for` picks the matching reader; a job declaring both or
            # neither raises rather than being routed by guesswork. Splitting
            # this routing is what cost r1 and r2 their review calls.
            record, _ = crossmodel_dispatch(ledger, job, digest(manifest), responder, replay)
            if charge(record["raw"], job, False) != record["accounted_nano"]:
                raise BudgetStop("Cost replay mismatch")
            seen.add(digest(job["slot"]))
            return record["parsed"]

        # r3's review response, read from the ledger. Not re-dispatched: the
        # verdict stands as recorded, including its reject.
        review = read_review(_inherited_review_text())
        print(json.dumps({"review": review,
                          "accounted_usd": ledger.state["recognition_nano"] / 1e9}), flush=True)

        # Constitution amendment, 16 September 2026: for a designation reusing
        # materials already reviewed and accepted, an independent review is
        # ADVISORY. Its findings are recorded and assessed; a reject does not
        # stop collection. These six tasks are byte-identical to material
        # accepted by moral_capstone_r3 (which then collected 956 decisions),
        # capstone_model2_r1, capstone_model2_r4 and capstone_specificity_r2.
        # Re-running a review to obtain a different verdict remains forbidden:
        # this verdict is recorded in full and stands.
        if review["verdict"] != "accept" and not REVIEW_ADVISORY:
            result = {"study": STUDY, "decision": "review_stop",
                      "screen_calls": 0, "participant_calls": 0, "phase3_pass": None}
        else:
            screen_rows = []
            for job in batch[:n_screen]:
                screen_rows.append({**job["cell"], "choice": dispatch(job)})
            screen = screen_outcome(screen_rows)
            save(folder / "screen_rows.json", screen_rows)
            usable = [t for t, v in screen.items() if v["usable"]]
            result = {"study": STUDY, "decision": "screen_complete", "screen": screen,
                      "usable_tasks": usable, "rejected_tasks":
                          [t for t in SCREEN_TASKS if t not in usable],
                      "screen_calls": len(screen_rows), "participant_calls": 0,
                      "phase4_pass": None, "moral_scores_assigned": False,
                      "note": ("Dispersion measurement only. Usable tasks are eligible for a "
                               "separately designated study; this run collects no profiled "
                               "decision and assigns no moral label.")}
            print(json.dumps({"screen": screen}), flush=True)

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
                          "screen_calls": SCREEN_N * len(SCREEN_TASKS),
                          "participant_calls": 0,
                          "total_calls": len(batch), "root_seed": SEEDS["population"]}))
    else:
        if not args.yes:
            raise BudgetStop("Explicit execution flag required")
        print(json.dumps(collect()))
