"""Render the profile block with two lines exchanged, for the position control.

`phase5_position_counterbalance` specifies a 2x2 crossing the label binding with
the line order. Realising the EXCHANGED order means taking the block that
`context_prompt` produces and moving two whole entries - each a numbered line plus
its indented gloss - then renumbering.

**Why this is delicate enough to deserve its own module with its own tests.** The
block is a formatted string, and every prior designation in this project depends
on it being byte-stable. String surgery on it can silently corrupt a gloss,
renumber wrongly, drop a trailing blank line, or change length - and any of those
would break the numeral-identical property the whole control rests on. The
functions here are therefore verified against the real renderer, not against an
assumed format, and `verify_render()` checks the output rather than trusting it.

**The format, as measured** (not assumed):

    header (6 lines)
     1. Legitimacy Locus: 0.41
        (0 = ...;
         1 = ...)
    <blank>
     2. Constraint Sensitivity: 0.83
    ...

Each entry is four lines - the numbered line, two gloss lines, one blank - except
the last, which carries an extra trailing line. Entries are identified by a strict
pattern matching only the numbered lines, because the gloss lines also begin with
whitespace and a digit and a looser pattern splits them apart.
"""
from __future__ import annotations

import re

PARAMETERS = ("LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW")

# The names as the renderer prints them. Note "Internalization" with a z: the
# template uses the American spelling while the project documents use the
# British one. Matching the template is what matters here.
PRINTED = {
    "Legitimacy Locus": "LL",
    "Constraint Sensitivity": "CS",
    "Response Threshold": "RT",
    "Mode of Response": "MoR",
    "Relational Embedding": "RE",
    "Procedural Dependence": "PD",
    "Tolerance for Asymmetry": "TfA",
    "Internalization Dependence": "ID",
    "Moral Scope": "MS",
    "Affective Weighting": "AW",
}

_ENTRY = re.compile(
    r"^(\s*)(\d+)\. (" + "|".join(re.escape(n) for n in PRINTED) + r"): ([0-9.]+)$")


def split_block(block, expect_canonical=True):
    """(header, [(code, [lines...]), ...]) from a rendered profile block.

    `expect_canonical` guards the INPUT case, where the block must be the
    renderer's own canonical order. A reordered block is parsed with it False.
    """
    lines = block.split("\n")
    starts = [i for i, l in enumerate(lines) if _ENTRY.match(l)]
    if len(starts) != 10:
        raise ValueError(f"Expected ten numbered entries, found {len(starts)}")
    header = lines[:starts[0]]
    entries = []
    for k, i in enumerate(starts):
        j = starts[k + 1] if k + 1 < len(starts) else len(lines)
        code = PRINTED[_ENTRY.match(lines[i]).group(3)]
        entries.append((code, lines[i:j]))
    if expect_canonical and tuple(c for c, _ in entries) != PARAMETERS:
        raise ValueError("Rendered block is not in the canonical parameter order")
    return header, entries


def reorder(block, order):
    """Re-emit `block` with entries in `order`, renumbered 1..10.

    The trailing blank-line structure is preserved by moving each entry's own
    trailing lines with it, then normalising: every entry but the last ends in
    exactly one blank line, and the last keeps whatever the original last entry
    had after its gloss.
    """
    if sorted(order) != sorted(PARAMETERS):
        raise ValueError("order must be a permutation of the ten parameters")
    header, entries = split_block(block)
    by_code = dict(entries)

    # Separate each entry's content from its trailing blanks so that moving an
    # entry does not move a blank that belongs to the block's structure.
    content, trailing = {}, {}
    for code, lines in entries:
        end = len(lines)
        while end > 0 and lines[end - 1].strip() == "":
            end -= 1
        content[code] = lines[:end]
        trailing[code] = lines[end:]

    # The last entry in the ORIGINAL block carries the block's trailing lines.
    original_last = entries[-1][0]
    block_tail = trailing[original_last]

    out = list(header)
    for n, code in enumerate(order, start=1):
        body = list(content[code])
        m = _ENTRY.match(body[0])
        # Renumber, preserving the renderer's leading-space padding. The template
        # pads EVERY entry with a single space, including 10, so the periods line
        # up. Stripping it for 10 was caught by the identity test below.
        body[0] = f" {n}. {m.group(3)}: {m.group(4)}"
        out.extend(body)
        if n < 10:
            out.append("")
    out.extend(block_tail)
    return "\n".join(out)


def verify_render(render_block, coordinates, order):
    """Check a reordered block against the properties the control depends on."""
    import collections
    normal = render_block(coordinates)
    moved = reorder(normal, order)
    nums = lambda s: sorted(re.findall(r"\d+\.\d+", s))
    _, ne = split_block(normal)
    _, me = split_block(moved, expect_canonical=False)

    problems = []
    # The strongest available invariant: reordering by the identity permutation
    # must return the input byte-for-byte. This catches padding, numbering and
    # blank-line errors that the property checks below would miss. It caught a
    # dropped leading space on entry 10.
    if reorder(normal, PARAMETERS) != normal:
        problems.append("identity reorder is not byte-identical to the input")
    if nums(normal) != nums(moved):
        problems.append("numeral multiset changed")
    if len(normal.split("\n")) != len(moved.split("\n")):
        problems.append("line count changed")
    if tuple(c for c, _ in me) != tuple(order):
        problems.append("reordered block is not in the requested order")
    # every parameter's VALUE must be unchanged, only its position moves
    nv = {c: _ENTRY.match(l[0]).group(4) for c, l in ne}
    mv = {c: _ENTRY.match(l[0]).group(4) for c, l in me}
    if nv != mv:
        problems.append(f"a value changed: {nv} -> {mv}")
    # numbering must run 1..10 in the new order
    seq = [int(_ENTRY.match(l[0]).group(2)) for _, l in me]
    if seq != list(range(1, 11)):
        problems.append(f"numbering is not 1..10: {seq}")
    # the gloss travelling with each entry must be the same text
    ng = {c: [x.strip() for x in l[1:] if x.strip()] for c, l in ne}
    mg = {c: [x.strip() for x in l[1:] if x.strip()] for c, l in me}
    for c in PARAMETERS:
        if ng[c] != mg[c]:
            problems.append(f"{c}: gloss text changed when moved")
    if problems:
        raise ValueError("Render verification failed: " + "; ".join(problems))
    return {"verified": True, "order": list(order),
            "same_numerals": True, "same_line_count": True,
            "values_preserved": True, "glosses_preserved": True,
            "note": ("Only the order of entries and their numbering differ. Every "
                     "value stays with its own label, every gloss travels with "
                     "its own entry, and the block's length and numeral multiset "
                     "are unchanged.")}


def main():
    import sys
    sys.path.insert(0, ".")
    from phase3_protocol_kernel import context_prompt, AXES
    from phase3_representation_diagnostic import profile_parts
    import phase5_position_counterbalance as PC

    ex = {"LL": 0.41, "CS": 0.83, "RT": 0.19, "MoR": 0.57, "RE": 0.28,
          "PD": 0.22, "TfA": 0.66, "ID": 0.74, "MS": 0.35, "AW": 0.50}
    NEUTRAL = dict.fromkeys(AXES, "NEUTRAL")
    render = lambda c: profile_parts(context_prompt(c, NEUTRAL))[1]

    v = verify_render(render, ex, PC.EXCHANGED_ORDER)
    print("verified:", v["verified"])
    moved = reorder(render(ex), PC.EXCHANGED_ORDER)
    print("\nexchanged block, entry lines only:")
    for l in moved.split("\n"):
        if _ENTRY.match(l):
            print("  ", l)


if __name__ == "__main__":
    main()
