"""
seeding.py — deterministic seed derivation.

Single Responsibility: turn a set of string/int parts into a stable 32-bit seed
via SHA-256. Every place that needs a reproducible per-call / per-run seed uses
`derive_seed(*parts)` so the derivation is identical and defined once. Given the
same parts, the same seed always results — the basis for resume-after-failure
and reproducible runs (spec §1.4, §5.2).
"""

from __future__ import annotations

import hashlib

_MASK32 = 2 ** 32


def derive_seed(*parts) -> int:
    """Stable 32-bit seed from an ordered set of parts (joined by ':')."""
    key = ":".join(str(p) for p in parts).encode()
    return int(hashlib.sha256(key).hexdigest(), 16) % _MASK32
