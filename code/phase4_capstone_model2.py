"""Second-model replication of the Phase 4 moral capstone.

Frozen evidence is never edited.

Every profiled decision in Phase 4 so far ran on one model, gpt-5.4-mini. An
external review identified single-model design as the ceiling on every thread in
this project. This designation repeats `moral_capstone_r3` on
claude-haiku-4-5-20251001 - a different provider - and changes nothing else.

Same four tasks from the eligible pool, same four arms (E numeric, V matched
prose, U none, G guidance only), same deterministic rule map
(`conflict-rules-r1`), same paired within-agent estimand, same permutation
inference with Holm across tasks. Fresh agents and fresh seeds.

The question is whether the capstone effect is a property of the encoding or of
one model. A null here would not erase the gpt-5.4-mini result; it would bound
it to that model, which is itself worth knowing and is reported as the finding.

The sign of the result is not a success gate.
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
from phase3_representation_diagnostic import profile_parts, numeric_rows, prose_rows, words
from phase3_variant_round import save

import phase4_eligible_pool as T

FOLDER = ROOT / "experiments/phase4_coding/capstone_model2_r1"
# Chain to the study that last wrote to the ledger.
PARENT = ROOT / "experiments/phase4_coding/capstone_specificity_r2"
STUDY = "capstone_model2_r1"

N_AGENTS = 60
TASKS = T.TASK_IDS   # four tasks, both gates passed across sets A and B
ARMS = ("E", "V", "U", "G")
# Worst-case reservation, not expected spend; prior studies settled near 17%.
# Haiku is roughly 1.5x gpt-5.4-mini per call, so the r3 ceiling is raised.
CAP = 6_000_000_000             # 6.00 USD ceiling for this designation
SEEDS = {"population": 2026091610, "schedule": 2026091611, "analysis": 2026091612}
NEUTRAL = dict.fromkeys(AXES, "NEUTRAL")
# The whole point of this designation: every Phase 4 profiled decision so far
# ran on gpt-5.4-mini (RATERS[1]). This repeats the capstone on a different
# provider's model, changing nothing else.
PARTICIPANT = RATERS[0]   # claude-haiku-4-5-20251001

# Historical failed slots are carried forward untouched under the no-retry rule.
INHERITED_FAILURE = "pd_gradient_r1/review/0"


PARAMETERS = ("LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW")
_PLACEHOLDER = dict.fromkeys(PARAMETERS, 0.5)
NL_SEP = chr(10) + chr(10)


GUIDANCE = (
    "# Ethical guidance" + NL_SEP +
    "Weigh the interests of everyone affected. Avoid causing harm, avoid "
    "deceiving anyone, avoid coercing anyone, and treat people with equivalent "
    "claims equally. Where these cannot all be satisfied, decide which matters "
    "most in this situation and act on it." + NL_SEP
)


def system(profile=None, arm="U"):
    """System prompt for one arm.

    E  full numeric profile
    V  the same values as information-matched prose
    U  no profile
    G  no profile, plus explicit ethical guidance
    """
    if arm not in ARMS:
        raise ValueError(f"Unknown arm: {arm}")
    original = context_prompt(dict(profile) if profile else _PLACEHOLDER, NEUTRAL)
    prefix, block, suffix = profile_parts(original)
    suffix = suffix[:suffix.index("# Your task")] + (
        "# Your task" + chr(10)
        + "Use the supplied information to make the requested decision. "
        + "Do not infer a demographic identity or additional facts. "
        + "Return only the requested JSON object." + chr(10))
    if arm == "E":
        selected = block
    elif arm == "V":
        rows = numeric_rows(block)
        body_text = NL_SEP.join(
            f'For {name}, your position is {words(value)} percent of the way '
            f'from "{low}" toward "{high}".'
            for name, value, low, high in rows)
        selected = "# Your decision-making profile" + NL_SEP + body_text + NL_SEP
        if prose_rows(selected) != rows:
            raise BudgetStop("Prose translation lost information")
    elif arm == "G":
        selected = GUIDANCE
    else:
        selected = ""
    return prefix + selected + suffix


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



def make_job(slot, stage, system_text, text, maximum=64):
    """kind is always "probe": the shared parse() returns text verbatim only for
    that kind, and forces every other kind through a ratings schema."""
    bound = len((system_text + text).encode("utf-8")) + 1024
    req = request(PARTICIPANT, system_text, text, maximum, temperature=1)
    # response_format is OpenAI-only; sending it to an Anthropic model is invalid.
    # The strict choice parser enforces the JSON contract for both providers.
    if MODELS[PARTICIPANT] == "openai":
        req["response_format"] = {"type": "json_object"}
    return {"slot": f"{STUDY}/{slot}", "kind": "probe", "stage": stage, "request": req,
            "input_token_bound": bound,
            "reserved_nano": token_cost_nano(bound, maximum, *PRICES[PARTICIPANT])}


def participant_jobs(population):
    """Each agent answers each eligible task in each arm."""
    batch = []
    for agent in population["agents"]:
        block = []
        for task_id in TASKS:
            for arm in ARMS:
                first = (agent["agent_id"] + TASKS.index(task_id)) % 2 == 0
                job = make_job(f"participant/{agent['agent_id']}/{task_id}/{arm}",
                               "participant", system(agent["parameters"], arm),
                               body(task_id, first))
                job["cell"] = {"stage": "participant", "task": task_id, "arm": arm,
                               "agent_id": agent["agent_id"],
                               "first": "first" if first else "second"}
                block.append(job)
        random.Random(SEEDS["schedule"] + agent["agent_id"]).shuffle(block)
        batch.extend(block)
    return batch


def review_packet():
    """Exactly what the reviewer sees. Audited by leakage_gate before dispatch."""
    return {
        "tasks": {t: {"item": T.participant_text(t)} for t in TASKS},
        # No classification labels are sent. r2's packet included per-action
        # good/not_good headlines, which its reviewer correctly identified as an
        # answer key. The reviewer now sees only the stipulated structure.
        "stipulated_structure": {f"{t}/{a}": {
            "standards_upheld": T.standards_upheld(t, a),
            "net_total": T.total_delta(t, a),
        } for t in TASKS for a in T.action_ids(t)},
        "dispersion_evidence": {**T.DISPERSION,
                                "source": "moral_conflict_screen_r2 and _b2, 25 unprofiled decisions each"},
    }


def review_job():
    packet = review_packet()
    return make_job("review/0", "review", (
        "Review these decision items independently. Stipulated consequences are an "
        "intended and necessary part of every item; their presence is not a defect, and "
        "an item is not flawed merely because its consequences point somewhere. Each "
        "item must be a conflict in which no option upholds every one of harm "
        "avoidance, deception avoidance, coercion avoidance and unfairness avoidance; "
        "the supplied structure states exactly which each option upholds and its net "
        "total. Note that the supplied dispersion figures are measured behaviour: these "
        "items were already answered 25 times each with no profile, and every one drew "
        "both options, so an item is not to be flagged as having no either-way choice "
        "when the measurement shows otherwise. Flag an item only if some option upholds "
        "every standard, if the text states which option ought to be chosen beyond the "
        "stipulated facts, or if it names a psychological construct or reveals a study "
        "hypothesis. Do not accept merely because the design could show an effect. "
        "Return only JSON with verdict accept/revise/reject, blocking_issues list, "
        "limits list. Under 150 words."),
        json.dumps(review_packet(), ensure_ascii=False, sort_keys=True), 1024)


def leakage_gate():
    """Refuse to build a batch that leaks, editorialises, or lacks a real conflict."""
    leaks = {t: T.audit_leakage(t) for t in T.TASK_IDS}
    if any(leaks.values()):
        raise BudgetStop("Task text leaks: " + str({k: v for k, v in leaks.items() if v}))
    comparatives = {t: T.audit_comparatives(t) for t in T.TASK_IDS}
    if any(comparatives.values()):
        raise BudgetStop("Task text editorialises: "
                         + str({k: v for k, v in comparatives.items() if v}))
    conflict = T.verify_pool()
    # verify_pool() already enforces conflict structure, a discriminating net
    # primary, and non-saturation for every pooled task.
    clean = conflict
    # The capstone reviewer must see the rule map and the dispersion evidence to
    # judge the classification and the task selection; those are task content,
    # not meta-description of the experiment.
    allowed = {"tasks", "stipulated_structure", "dispersion_evidence"}
    if set(review_packet()) - allowed:
        raise BudgetStop("Review packet carries non-task keys: "
                         + str(sorted(set(review_packet()) - allowed)))
    return {"forbidden_terms_found": 0, "no_comparatives": True,
            "pool_verified": conflict, "no_clean_option": clean,
            "primary_discriminates_on_eligible_tasks": True,
            "review_packet_clean": True,
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


def analyze(rows, n_agents):
    """Score every decision through the frozen rule map and contrast the arms.

    Primary: proportion of decisions whose net-score headline is `good`, per arm
    per task, with the E-U difference. Labels come from the stipulated
    transition, never from agent text.
    """
    from phase4_eligible_pool import primary_outcome

    rng = random.Random(SEEDS["analysis"])
    scored = []
    for row in rows:
        if row["choice"] is None:
            scored.append({**row, "net": None, "strict": None,
                           "weighted": None, "fixed": None})
            continue
        out = primary_outcome(row["task"], row["choice"])
        scored.append({**row, "net": out["primary_net"],
                       "strict": out["secondary_strict_relative"],
                       "weighted": out["secondary_weighted"],
                       "fixed": out["fixed_standard_headline"]})

    def rate(task_id, arm, key):
        vals = [r[key] for r in scored
                if r["task"] == task_id and r["arm"] == arm and r[key] is not None]
        return (round(sum(v == "good" for v in vals) / len(vals), 4), len(vals)) if vals else (None, 0)

    cells = {}
    for task_id in TASKS:
        for arm in ARMS:
            good, n = rate(task_id, arm, "net")
            cells[f"{task_id}/{arm}"] = {
                "n_valid": n, "net_good_rate": good,
                "strict_good_rate": rate(task_id, arm, "strict")[0],
                "weighted_good_rate": rate(task_id, arm, "weighted")[0],
                "choice_distribution": {
                    a: sum(1 for r in scored
                           if r["task"] == task_id and r["arm"] == arm and r["choice"] == a)
                    for a in T.action_ids(task_id)},
            }

    def paired(task_id, arm_a, arm_b, key="net"):
        """Within-agent paired difference, permutation test on sign flips."""
        by_agent = {}
        for r in scored:
            if r["task"] == task_id and r[key] is not None:
                by_agent.setdefault(r["agent_id"], {})[r["arm"]] = r[key]
        diffs = [int(v[arm_a] == "good") - int(v[arm_b] == "good")
                 for v in by_agent.values() if arm_a in v and arm_b in v]
        if not diffs:
            return {"n_pairs": 0, "difference": None, "perm_p": None}
        mean = sum(diffs) / len(diffs)
        hits = 0
        for _ in range(10_000):
            flipped = sum(x if rng.random() < 0.5 else -x for x in diffs)
            if abs(flipped / len(diffs)) >= abs(mean):
                hits += 1
        return {"n_pairs": len(diffs), "difference": round(mean, 4),
                "perm_p": (hits + 1) / 10_001,
                "discordant": sum(1 for x in diffs if x != 0)}

    contrasts = {}
    for task_id in TASKS:
        for arm in ("E", "V", "G"):
            contrasts[f"{task_id}/{arm}-U"] = paired(task_id, arm, "U")

    # Holm across the primary E-U contrasts only.
    primaries = {k: v for k, v in contrasts.items() if k.endswith("/E-U")}
    ordered = sorted((v["perm_p"], k) for k, v in primaries.items() if v["perm_p"] is not None)
    m = len(ordered)
    for i, (p_value, key) in enumerate(ordered):
        contrasts[key]["holm_adjusted_p"] = min(1.0, p_value * (m - i))

    # Which standard each arm privileges, from the stipulated action properties.
    standards = {}
    for arm in ARMS:
        counts = {s: 0 for s in T.STANDARDS}
        total = 0
        for r in scored:
            if r["choice"] is None or r["arm"] != arm:
                continue
            total += 1
            for s, upheld in T.standards_upheld(r["task"], r["choice"]).items():
                counts[s] += int(not upheld)
        standards[arm] = {"n": total,
                          "violation_rates": {s: (round(c / total, 4) if total else None)
                                              for s, c in counts.items()}}

    return {"study": STUDY, "n_agents": n_agents, "cells": cells,
            "contrasts": contrasts, "standard_violations_by_arm": standards,
            "primary_outcome": "net-score headline good-rate; prespecified in PROTOCOL section 2",
            "rule_version": "conflict-rules-r1",
            "analysis_status": "prospective; sign of the result is not a success gate",
            "phase4_pass": None,
            "moral_labels": "deterministic classification under stipulated standards, not moral truth"}


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
        if ledger.state["pending"] or ledger.state["failed"] not in ([], [digest(INHERITED_FAILURE)]):
            raise BudgetStop("Unexpected unresolved dispatch in inherited evidence")
        providers = dict(ledger.state["providers"])

    population = Population.draw(N_AGENTS, seed=SEEDS["population"]).to_dict()
    batch = [review_job()] + participant_jobs(population)
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

    expected = 1 + N_AGENTS * len(TASKS) * len(ARMS)
    if len(slots) != expected or bound > CAP:
        raise BudgetStop(f"Size or cap exceeded: {len(slots)} calls, {bound / 1e9:.6f} USD")
    # The inherited guard hard-coded $11 anthropic / $20 openai, reserving room
    # under the then-$15 ceiling for the moral capstone. That capstone has since
    # run, and the researcher raised the Anthropic ceiling to $32 (constitution
    # amendment, 15 September 2026). Check the actual ceilings instead of a
    # stale sub-limit.
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
    if batch != [review_job()] + participant_jobs(pop):
        raise BudgetStop("Reconstructed schedule differs")
    if release["leakage_gate"]["task_content_sha256"] != T.content_hash():
        raise BudgetStop("Task content changed after release")

    manifest = {"release_sha256": digest(release), "jobs_sha256": digest(batch)}
    save(folder / "execution_manifest.json", manifest)


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
            rows = []
            for i, job in enumerate(batch[1:], 1):
                valid = {a.lower() for a in T.action_ids(job["cell"]["task"])}
                rows.append({**job["cell"], "choice": choice(dispatch(job), valid)})
                if i % 80 == 0:
                    print(json.dumps({"completed": i, "assigned": len(batch) - 1,
                                      "accounted_usd": ledger.state["recognition_nano"] / 1e9}),
                          flush=True)
            save(folder / "scored_rows.json", rows)
            result = analyze(rows, N_AGENTS)
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
                          "tasks": list(TASKS), "arms": list(ARMS),
                          "participant_calls": N_AGENTS * len(TASKS) * len(ARMS),
                          "total_calls": len(batch), "root_seed": SEEDS["population"]}))
    else:
        if not args.yes:
            raise BudgetStop("Explicit execution flag required")
        print(json.dumps(collect()))
