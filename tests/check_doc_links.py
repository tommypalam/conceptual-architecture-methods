"""Check that every relative link in the live Markdown documents resolves.

Run from anywhere:
    python tests/check_doc_links.py            # report only, exit 1 if any broken
    python tests/check_doc_links.py --fix-moves # also repair links broken by MOVES

**Why this exists.** The 19 September reorganisation moved the thesis, paper,
publication records and handoffs into sub-folders of docs/. A file that changes
depth silently breaks every relative link inside it, and every link pointing at
it, and nothing in the project would have noticed. This checker is what noticed.

**Scope.** Live documents only. `archive/`, `experiments/` and
`docs/thesis/history/` are frozen: they are never edited, and links inside them
are deliberately not checked, because a frozen document's dead link is part of
the historical record rather than a defect to repair. Links FROM live documents
INTO frozen areas are checked, since those must keep working.

`--fix-moves` only rewrites a link when the target demonstrably moved (it is in
MOVES below). It never guesses at a target it cannot account for.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FROZEN = ("archive/", "experiments/", "docs/thesis/history/")
SKIP_DIRS = {".git", "node_modules", "output", "data", ".claude"}

# old repository-relative path -> new one. Directories end with "/".
MOVES = {
    "docs/LF3262767.pdf": "docs/thesis/LF3262767.pdf",
    "docs/thesis.md": "docs/thesis/thesis.md",
    "docs/thesis_abstract.txt": "docs/thesis/abstract.txt",
    "docs/figures/": "docs/thesis/figures/",
    "docs/thesis_build/": "docs/thesis/build/",
    "docs/paper_draft.md": "docs/paper/paper_draft.md",
    "docs/citation_verification.md": "docs/paper/citation_verification.md",
    "docs/publication_20260913.md": "docs/publications/publication_20260913.md",
    "docs/publication_20260914.md": "docs/publications/publication_20260914.md",
    "docs/publication_20260915.md": "docs/publications/publication_20260915.md",
    "docs/publication_20260916.md": "docs/publications/publication_20260916.md",
    "docs/publication_20260917.md": "docs/publications/publication_20260917.md",
    "docs/NEXT_CHAT_HANDOFF.md": "docs/handoffs/NEXT_CHAT_HANDOFF.md",
    "docs/desktop_handoff.md": "docs/handoffs/desktop_handoff.md",
    "docs/desktop_transfer.json": "docs/handoffs/desktop_transfer.json",
}
_NEW_TO_OLD = {v: k for k, v in MOVES.items()}

LINK = re.compile(r"(?<!\!)\[([^\]]*)\]\(([^)\s]+)(\s+\"[^\"]*\")?\)|\!\[([^\]]*)\]\(([^)\s]+)\)")


def posix(p):
    return str(p).replace("\\", "/")


def map_forward(path):
    """Where an OLD repository-relative path lives now."""
    if path in MOVES:
        return MOVES[path]
    for old, new in MOVES.items():
        if old.endswith("/") and path.startswith(old):
            return new + path[len(old):]
    return path


def old_location(path):
    """Where a CURRENT repository-relative path used to live."""
    if path in _NEW_TO_OLD:
        return _NEW_TO_OLD[path]
    for new, old in _NEW_TO_OLD.items():
        if new.endswith("/") and path.startswith(new):
            return old + path[len(new):]
    return path


def live_markdown():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if not name.endswith(".md"):
                continue
            rel = posix(Path(dirpath, name).relative_to(ROOT))
            if rel.startswith(FROZEN):
                continue
            yield rel


def is_relative(target):
    return not re.match(r"^(?:[a-zA-Z][a-zA-Z0-9+.-]*:|#|/)", target)


def check(fix=False):
    broken, fixed, checked = [], [], 0
    for rel in sorted(live_markdown()):
        path = ROOT / rel
        raw = path.read_bytes()
        crlf = raw.count(b"\r\n") > 0
        text = raw.decode("utf-8", errors="replace").replace("\r\n", "\n")
        here_new = posix(Path(rel).parent)
        here_old = posix(Path(old_location(rel)).parent)
        changed = False

        def visit(match):
            nonlocal changed, checked
            target = match.group(2) or match.group(5)
            if not target or not is_relative(target):
                return match.group(0)
            body, _, anchor = target.partition("#")
            if not body:
                return match.group(0)
            checked += 1
            now = posix(os.path.normpath(os.path.join(here_new, body)))
            if (ROOT / now).exists():
                return match.group(0)
            # Broken as written. Was it valid in the OLD layout, via a move?
            was = posix(os.path.normpath(os.path.join(here_old, body)))
            moved_to = map_forward(was)
            if (ROOT / moved_to).exists() and (moved_to != now):
                better = posix(os.path.relpath(ROOT / moved_to, ROOT / here_new))
                if fix:
                    changed = True
                    fixed.append((rel, target, better))
                    new_target = better + (("#" + anchor) if anchor else "")
                    return match.group(0).replace("(" + target, "(" + new_target, 1)
                broken.append((rel, target, f"moved -> {better}"))
                return match.group(0)
            broken.append((rel, target, "target does not exist"))
            return match.group(0)

        new_text = LINK.sub(visit, text)
        if fix and changed:
            out = new_text.encode("utf-8")
            if crlf:
                out = out.replace(b"\n", b"\r\n")
            path.write_bytes(out)
    return checked, broken, fixed


def main():
    fix = "--fix-moves" in sys.argv
    checked, broken, fixed = check(fix=fix)
    print(f"relative links checked: {checked}")
    if fixed:
        print(f"\nrepaired {len(fixed)} link(s) broken by the reorganisation:")
        for rel, old, new in fixed:
            print(f"  {rel}: {old}  ->  {new}")
    if broken:
        print(f"\nBROKEN: {len(broken)}")
        for rel, target, why in broken:
            print(f"  {rel}: ({target})  [{why}]")
        return 1
    print("\nno broken relative links in live documents")
    return 0


if __name__ == "__main__":
    sys.exit(main())
