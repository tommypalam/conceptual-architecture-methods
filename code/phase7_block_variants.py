"""Meaning-changing and form-changing edits of ONE entry in the rendered profile block.

The understanding programme asks whether behaviour tracks the MEANING of a profile
field or merely its form. That needs two kinds of edit to a single entry, with
everything else in the prompt held byte-identical:

    flip_gloss   keep the name, the line and the number; swap what the two ends
                 of the scale are said to MEAN. Form almost untouched, meaning
                 inverted.
    rename       keep the gloss, the line and the number; change the NAME.
                 Meaning (as explained) untouched, form changed.

Composed, they give the four Stage 1 variants for a field F:

    CANON    the block exactly as every prior designation rendered it
    FLIP     same name, endpoint explanations swapped
    INVERT   a new name consistent with the swapped explanations
    NONCE    a name with no content, canonical explanations

**An entry, as measured against the real renderer** (not assumed):

     6. Procedural Dependence: 0.90
        (0 = outcome-dominant; results matter, methods are secondary;
         1 = process-dominant; fair procedure matters independently)

The endpoint texts contain INTERNAL semicolons, so the gloss is parsed by line
prefix and suffix - "    (0 = " ... ";" and "     1 = " ... ")" - never by
splitting on ";". A looser parse would cut PD's low endpoint in half.

**Edits are made in place on three known lines.** The block is never re-assembled
from parts, so every other byte of it is untouched by construction rather than by
careful re-joining. That is the lesson of `phase5_position_render`, where
re-assembly silently dropped a leading space and only an identity test caught it.

**The invariants `verify_variants` enforces**, all against the real renderer:

  - CANON is the input, byte for byte.
  - flip_gloss is an INVOLUTION: applied twice it returns the input byte for byte.
    This is the strongest check available - any corruption of either endpoint
    text, of the punctuation frame, or of whitespace breaks it.
  - flip_gloss preserves total length and the exact multiset of characters: it is
    a pure rearrangement.
  - rename to the entry's own name is the identity.
  - Every variant differs from CANON on the three lines of the target entry and
    NOWHERE else; line count and the multiset of numerals never change.
"""
from __future__ import annotations

import re
from collections import Counter

import phase5_position_render as PR

PARAMETERS = PR.PARAMETERS
_NAME_OF = {code: name for name, code in PR.PRINTED.items()}

_LOW_PREFIX, _LOW_SUFFIX = "    (0 = ", ";"
_HIGH_PREFIX, _HIGH_SUFFIX = "     1 = ", ")"

VARIANTS = ("CANON", "FLIP", "INVERT", "NONCE")


def locate(block, code):
    """(lines, index of the entry's numbered line) for parameter `code`.

    The block must be in the renderer's canonical form; `split_block` enforces it.
    """
    if code not in PARAMETERS:
        raise ValueError(f"Unknown parameter code: {code}")
    PR.split_block(block)                     # raises unless canonical and complete
    lines = block.split("\n")
    hits = [i for i, l in enumerate(lines)
            if (m := PR._ENTRY.match(l)) and PR.PRINTED[m.group(3)] == code]
    if len(hits) != 1:
        raise ValueError(f"Expected exactly one entry for {code}, found {len(hits)}")
    i = hits[0]
    low, high = lines[i + 1], lines[i + 2]
    if not (low.startswith(_LOW_PREFIX) and low.endswith(_LOW_SUFFIX)):
        raise ValueError(f"{code}: low-endpoint line is not in the measured form: {low!r}")
    if not (high.startswith(_HIGH_PREFIX) and high.endswith(_HIGH_SUFFIX)):
        raise ValueError(f"{code}: high-endpoint line is not in the measured form: {high!r}")
    return lines, i


def endpoints(block, code):
    """(low text, high text) of the entry's gloss, exactly as rendered."""
    lines, i = locate(block, code)
    low = lines[i + 1][len(_LOW_PREFIX):-len(_LOW_SUFFIX)]
    high = lines[i + 2][len(_HIGH_PREFIX):-len(_HIGH_SUFFIX)]
    return low, high


def flip_gloss(block, code):
    """Swap what the two ends of `code`'s scale are said to mean. An involution."""
    lines, i = locate(block, code)
    low, high = endpoints(block, code)
    lines[i + 1] = _LOW_PREFIX + high + _LOW_SUFFIX
    lines[i + 2] = _HIGH_PREFIX + low + _HIGH_SUFFIX
    return "\n".join(lines)


def rename(block, code, new_name):
    """Replace the printed name of `code`'s entry. Number, gloss and line stay put."""
    if not new_name or ":" in new_name or "\n" in new_name:
        raise ValueError(f"Unusable field name: {new_name!r}")
    lines, i = locate(block, code)
    m = PR._ENTRY.match(lines[i])
    lines[i] = f"{m.group(1)}{m.group(2)}. {new_name}: {m.group(4)}"
    return "\n".join(lines)


def _rename_flipped(block, code, new_name):
    # rename() insists on a canonical block, so flip AFTER renaming would fail its
    # parse. Rename first on the canonical block, then swap the gloss lines by index.
    lines, i = locate(block, code)
    low, high = endpoints(block, code)
    m = PR._ENTRY.match(lines[i])
    lines[i] = f"{m.group(1)}{m.group(2)}. {new_name}: {m.group(4)}"
    lines[i + 1] = _LOW_PREFIX + high + _LOW_SUFFIX
    lines[i + 2] = _HIGH_PREFIX + low + _HIGH_SUFFIX
    return "\n".join(lines)


def variant(block, code, kind, *, invert_name, nonce_name):
    """One of the four Stage 1 variants of `code`'s entry."""
    if kind == "CANON":
        return block
    if kind == "FLIP":
        return flip_gloss(block, code)
    if kind == "INVERT":
        return _rename_flipped(block, code, invert_name)
    if kind == "NONCE":
        return rename(block, code, nonce_name)
    raise ValueError(f"Unknown variant: {kind}")


def verify_variants(render_block, coordinates, code, *, invert_name, nonce_name):
    """Check every variant of a real rendered block against the invariants above."""
    canon = render_block(coordinates)
    lines, i = locate(canon, code)
    target = {i, i + 1, i + 2}
    numerals = lambda s: sorted(re.findall(r"\d+\.\d+", s))
    problems = []

    if variant(canon, code, "CANON", invert_name=invert_name, nonce_name=nonce_name) != canon:
        problems.append("CANON is not the input byte for byte")
    flipped = flip_gloss(canon, code)
    if flip_gloss(flipped, code) != canon:
        problems.append("flip_gloss is not an involution: two flips did not restore the input")
    if flipped == canon:
        problems.append("flip_gloss changed nothing: the two endpoint texts are identical")
    if len(flipped) != len(canon) or Counter(flipped) != Counter(canon):
        problems.append("flip_gloss is not a pure rearrangement of the block's characters")
    if rename(canon, code, _NAME_OF[code]) != canon:
        problems.append("rename to the entry's own name is not the identity")

    low, high = endpoints(canon, code)
    f_low, f_high = endpoints(flipped, code)
    if (f_low, f_high) != (high, low):
        problems.append("flipped endpoints are not the canonical endpoints exchanged")

    built = {}
    for kind in VARIANTS:
        v = variant(canon, code, kind, invert_name=invert_name, nonce_name=nonce_name)
        built[kind] = v
        v_lines = v.split("\n")
        if len(v_lines) != len(lines):
            problems.append(f"{kind}: line count changed")
            continue
        changed = {k for k, (a, b) in enumerate(zip(lines, v_lines)) if a != b}
        if not changed <= target:
            problems.append(f"{kind}: lines outside the target entry changed: {sorted(changed - target)}")
        if numerals(v) != numerals(canon):
            problems.append(f"{kind}: multiset of numerals changed")
        expected = {"CANON": set(), "FLIP": {i + 1, i + 2},
                    "INVERT": {i, i + 1, i + 2}, "NONCE": {i}}[kind]
        if changed != expected:
            problems.append(f"{kind}: changed lines {sorted(changed)} != expected {sorted(expected)}")
    if len(set(built.values())) != len(VARIANTS):
        problems.append("the four variants are not four distinct blocks")
    if problems:
        raise ValueError("Variant verification failed: " + "; ".join(problems))
    return {"verified": True, "code": code, "entry_line": i + 1,
            "low_endpoint": low, "high_endpoint": high,
            "flip_is_involution": True, "flip_is_pure_rearrangement": True,
            "lengths": {k: len(v) for k, v in built.items()},
            "note": ("Each variant differs from the canonical block on the target "
                     "entry's lines only. FLIP has the identical length and "
                     "character multiset as CANON; INVERT and NONCE differ in "
                     "length only through the name, and every within-variant "
                     "contrast compares two blocks that differ in one numeral.")}


def main():
    import sys
    sys.path.insert(0, ".")
    from phase3_protocol_kernel import context_prompt, AXES
    from phase3_representation_diagnostic import profile_parts

    ex = {"LL": 0.41, "CS": 0.83, "RT": 0.19, "MoR": 0.57, "RE": 0.28,
          "PD": 0.90, "TfA": 0.66, "ID": 0.74, "MS": 0.35, "AW": 0.50}
    neutral = dict.fromkeys(AXES, "NEUTRAL")
    render = lambda c: profile_parts(context_prompt(c, neutral))[1]
    v = verify_variants(render, ex, "PD", invert_name="Outcome Dominance",
                        nonce_name="Factor K")
    print("verified:", v["verified"], "| entry line:", v["entry_line"])
    print("lengths:", v["lengths"])
    canon = render(ex)
    for kind in VARIANTS:
        b = variant(canon, "PD", kind, invert_name="Outcome Dominance", nonce_name="Factor K")
        lines, i = b.split("\n"), v["entry_line"] - 1
        print(f"\n[{kind}]")
        for l in lines[i:i + 3]:
            print("   |" + l)
    # every one of the ten entries must survive a double flip, not just PD
    for code in PARAMETERS:
        assert flip_gloss(flip_gloss(canon, code), code) == canon, code
    print("\ndouble flip restores the input byte for byte on all ten entries")


if __name__ == "__main__":
    main()
