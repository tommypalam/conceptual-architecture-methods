"""Lossless task-content projection for recognition; never includes profiles or keys.

New adapter over immutable canonical r2 and reviewed alternative r3 wording.
The compact escalation recipe reconstructs every one of 600 possible user turns
per form. Recognition sees branches, not simulated participant choices.
"""
import base64
import hashlib
import json
from pathlib import Path

import phase3_canonical_stimuli as c
from phase3_budget import read_checked
from phase3_protocol_kernel import Escalation, asch_schedule, peer_answers

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/phase3_benchmarks"
SEED = 2026091306
MODS = ("base", "peer_rebellion", "experimenter_absent", "diffused_responsibility")
ARMS = ("social_removal", "nonsocial_removal", "unrestricted")


def pack_lines(turns):
    lines, indices = [], {}
    rows = []
    for turn in turns:
        row = []
        for line in turn.split("\n"):
            if line not in indices:
                indices[line] = len(lines)
                lines.append(line)
            row.append(indices[line])
        rows.append(row)
    return {"lines": lines, "turns": rows}


def unpack_lines(packed):
    return ["\n".join(packed["lines"][i] for i in row) for row in packed["turns"]]


def pack_cells(cells):
    by_row = {}
    for row, col in cells:
        by_row.setdefault(row, []).append(col)
    groups = {}
    for row, cols in by_row.items():
        groups.setdefault(tuple(cols), []).append(row)
    return [[rows, list(cols)] for cols, rows in groups.items()]


def unpack_cells(groups):
    return [[row, col] for rows, cols in groups for row in rows for col in cols]


def alternatives():
    return {r["benchmark"]: r["stimulus"] for r in
            read_checked(BASE / "variants_r3/candidates.json")["candidates"]}


def alternative_escalation(state, modulator="base"):
    if not isinstance(state, Escalation) or state.terminal or modulator not in MODS:
        raise ValueError("Active state and known condition required")
    s = alternatives()["milgram"]
    d, p = state.delivered, state.prods
    setting = s[{"base": "mod_base", "experimenter_absent": "mod_remote",
                 "diffused_responsibility": "mod_shared"}.get(modulator, "mod_base")]
    if modulator == "peer_rebellion":
        # Before level 20, observers' existence must already be explicit. These
        # exact clauses come from the accepted before/after texts, without a new
        # generated actor or inferred behaviour.
        setting = s["mod_base"] + " " + (s["mod_peer_before"] if d == 19 and p == 0 else
                  s["mod_peer_after"] if d >= 19 else s["mod_peer_before"].split(" Just before level 20,")[0])
    feedback = s["feedback_early" if d < 20 else "feedback_20" if d == 20 else
                 "feedback_21" if d == 21 else "feedback_late"]
    transition = " " + s["correct_event"] if 0 < d < 20 and d % 3 == 0 and p == 0 else ""
    instruction = s[f"prod_{p}"] if p else s["error_event"]
    return (f"{setting}\nAlready delivered: {d} levels. Next proposed reprimand: level {d+1} of 30.\n"
            f"{feedback}{transition}\nSupervisor's instruction: {instruction}\n"
            'Return exactly {"action":"continue"}, {"action":"hesitate"}, or {"action":"quit"}.')


def escalation_text(form, state, modulator="base"):
    if form == "canonical":
        return c.escalation_turn(state, modulator=modulator)
    if form == "alternative":
        return alternative_escalation(state, modulator)
    raise ValueError("Unknown form")


def escalation_recipe(form):
    # Deduplicate exact turn lines. A 30-row baseline plus four prod replacements
    # and condition-specific prefixes reconstructs ALL 600 turns without showing
    # hypothetical agent choices or 600 repeated full paragraphs to the judge.
    turns = [escalation_text(form, Escalation(d)).split("\n") for d in range(30)]
    replacements = []
    for p in range(1, 5):
        # Some feedback lines include a correct/no-action event only at p=0.
        changes = {}
        for d in range(30):
            following = escalation_text(form, Escalation(d, p)).split("\n")
            for i, (before, after) in enumerate(zip(turns[d], following)):
                if before != after:
                    changes.setdefault(after, []).append([d, i])
        replacements.append([{"text": text, "at": pack_cells(cells)} for text, cells in changes.items()])
    settings = []
    for mod in MODS[1:]:
        groups = {}
        for d in range(30):
            for p in range(5):
                first = escalation_text(form, Escalation(d, p), mod).split("\n")[0]
                # Canonical first line includes a changing level counter.
                suffix = turns[d][0].split(" Already administered:", 1)
                if len(suffix) == 2:
                    first = first.split(" Already administered:", 1)[0]
                groups.setdefault(first, []).append([d, p])
        settings.append([{"text": text, "at": pack_cells(cells)} for text, cells in groups.items()])
    return {"baseline": pack_lines(["\n".join(lines) for lines in turns]), "hesitation_replacements": replacements,
            "condition_first_lines": settings,
            "first_line_suffix": " Already administered:" if " Already administered:" in turns[0][0] else ""}


def expand_recipe(recipe, d, p, m):
    lines = unpack_lines(recipe["baseline"])[d].split("\n")
    if p:
        for group in recipe["hesitation_replacements"][p-1]:
            for row, col in unpack_cells(group["at"]):
                if row == d:
                    lines[col] = group["text"]
    if m:
        group = next(g for g in recipe["condition_first_lines"][m-1] if [d, p] in unpack_cells(g["at"]))
        suffix = recipe["first_line_suffix"]
        lines[0] = group["text"] + (suffix + lines[0].split(suffix, 1)[1] if suffix else "")
    return "\n".join(lines)


def image_schedule(form):
    manifest = read_checked(BASE / "perception_20260913/manifest.json")
    kind = "line" if form == "canonical" else "colour"
    jobs = [j for j in manifest["jobs"] if j["stimulus"]["kind"] == kind]
    rows = asch_schedule([j["stimulus"] for j in jobs], SEED)
    paths = {j["stimulus"]["id"]: j for j in jobs}
    for row in rows:
        job = paths[row["id"]]
        png = (ROOT / job["image"]).read_bytes()
        if hashlib.sha256(png).hexdigest() != job["image_sha256"]:
            raise ValueError("Frozen image changed")
        row["png"] = png
    return rows


def alternative_asch(trial, group_size=5, dissent=False, private=False):
    s = alternatives()["asch"]
    answers = peer_answers(trial, group_size=group_size, dissent=dissent)
    return (f"Trial {trial['trial']}. {s['private_response' if private else 'public_response']}\n" +
            "\n".join(f"Panel member {i}: {a}" for i, a in enumerate(answers, 1)) +
            f"\n{s['question']} " +
            'Return exactly {"choice":"A"}, {"choice":"B"}, or {"choice":"C"}.')


def alternative_ultimatum(role, offer=None):
    s = alternatives()["ultimatum"]
    if role == "proposer" and offer is None:
        return s["setup"] + "\n" + s["proposer"] + '\nReturn exactly {"offer_to_other":N}, with integer N from 0 through 100.'
    if role != "responder" or type(offer) is not int or offer not in (10, 20, 30, 40, 50):
        raise ValueError("Unknown role/offer")
    return s["setup"] + "\n" + s["responder"].format(offer=offer, remainder=100-offer) + '\nReturn exactly {"action":"accept"} or {"action":"reject"}.'


def alternative_bystander(others, danger):
    if type(others) is not int or others not in (0, 3) or danger not in ("standard", "elevated"):
        raise ValueError("Unknown condition")
    s = alternatives()["bystander"]
    return {"setup": s["setup_alone" if others == 0 else "setup_group"],
            "turns": [f"Decision opportunity {i} of 3. {s[f'{danger}_{i}']} " +
                      'Return exactly {"action":"help"} or {"action":"wait"}.' for i in (1, 2, 3)]}


def alternative_reactance(ranking, arm):
    # Canonical validates labels, removed rank and available set.
    c.reactance_turn(ranking, arm=arm)
    s = alternatives()["reactance"]
    removed = ranking[1]
    available = [o for o in c.OPTIONS if o != removed] if arm != "unrestricted" else list(c.OPTIONS)
    return (s[arm].format(removed=removed) + "\nAvailable choices: " + ", ".join(available) +
            ". " + s["response_instruction"] +
            '\nReturn exactly {"choice":"A","ranking":["A","B","C","D","E"]}, using your chosen label and ranking.')


def task_content(name, form):
    if name not in c.BENCHMARKS or form not in ("canonical", "alternative"):
        raise ValueError("Unknown task/form")
    s = alternatives()[name]
    if name == "milgram":
        recipe = escalation_recipe(form)
        return [{"type": "text", "text": json.dumps({
            "setup": c.ESCALATION_SETUP if form == "canonical" else s["setup"],
            "delivery": "Exact turn recipe: d is the number of delivered levels (0..29), p the number of consecutive hesitations at that level (0..4). Baseline has a dictionary of literal lines; each turn row lists line indices to join with newlines. Baseline turn d is p=0 in the first condition. For p>0 apply the hesitation replacements. Each at entry [rows,columns] means every combination: rows are d, columns are line indices. The other three conditions replace the first line using at entries whose rows are d and columns are p; retain the indicated suffix and counter if present. All indices are zero-based. Read each reconstructed turn as one decision. Continue delivers one level and resets p to zero; delivering level30 ends the task. Hesitate increments p; hesitation at p=4 ends the task. Quit ends it immediately. Conditions are separate conversations. No previous participant choices are supplied here.",
            "recipe": recipe}, separators=(",", ":"))}]
    if name == "asch":
        rows = image_schedule(form)
        content = [{"type": "text", "text": c.ASCH_SETUP if form == "canonical" else s["setup"]}]
        for row in rows:
            content += [{"type": "text", "text": f"Trial {row['trial']} image:"},
                        {"type": "image", "source": {"type": "base64", "media_type": "image/png",
                         "data": base64.b64encode(row["png"]).decode()}}]
        cells = []
        for size, dissent, private in ((5, False, False), (5, True, False), (5, False, True),
                                     (1, False, False), (2, False, False), (3, False, False)):
            # Size5 is the base cell, not duplicated as an extra condition.
            turns = [c.asch_turn(row, group_size=size, dissent=dissent, private=private)
                     if form == "canonical" else alternative_asch(row, size, dissent, private) for row in rows]
            cells.extend(turns)
        content.append({"type": "text", "text": "The dictionary below contains literal turn lines. Join the indexed lines in each turn row with newlines. Every consecutive group of 18 turns is a separate conversation using the 18 corresponding images in order. Previous answers stay within that conversation; no answers are supplied here.\n" + json.dumps(pack_lines(cells), separators=(",", ":"))})
        return content
    if name == "ultimatum":
        fn = c.ultimatum_turn if form == "canonical" else alternative_ultimatum
        text = {"delivery": "Every listed task is an isolated conversation; no answer to any other role or offer is visible.",
                "tasks": [fn("proposer")] + [fn("responder", offer) for offer in (10, 20, 30, 40, 50)]}
    elif name == "bystander":
        text = {"delivery": "Each case is a separate conversation. Present the setup and one event at a time. Help ends it immediately; wait advances to the next event. Stop after the third decision. Earlier answers stay within that case; none are supplied here.", "cases": []}
        for others in (0, 3):
            for danger in ("standard", "elevated"):
                text["cases"].append({"setup": c.bystander_setup(others=others, danger=danger),
                    "turns": [c.bystander_turn(i, danger=danger) for i in (1, 2, 3)]} if form == "canonical" else alternative_bystander(others, danger))
    else:
        fn = c.reactance_turn if form == "canonical" else alternative_reactance
        # Enumerate every possible removed label without inventing initial answers.
        cases = {}
        for removed in c.OPTIONS:
            ranking = [x for x in c.OPTIONS if x != removed]
            ranking.insert(1, removed)
            cases[removed] = [fn(ranking, arm=arm) for arm in ARMS]
        text = {"setup": c.REACTANCE_SETUP if form == "canonical" else s["setup"] + '\nReturn exactly {"ranking":["A","B","C","D","E"]}, rearranging the labels into your preferred order.',
                "delivery": "Obtain the initial ranking first. The second-ranked label selects a case below. Copy that initial conversation into three isolated continuations, one per listed notice. No initial answer or preferred label is supplied here. Each continuation requests a choice and all-five desirability ranking.", "cases": cases}
    return [{"type": "text", "text": json.dumps(text, separators=(",", ":"))}]
