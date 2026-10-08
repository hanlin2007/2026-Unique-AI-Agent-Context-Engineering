"""Tokenizer.

Splits raw text into lowercase alphanumeric terms. Apostrophes and
hyphens act as separators ("well-known" -> ["well", "known"],
"don't" -> ["don", "t"]); single-character fragments are dropped so
contraction debris does not pollute the index.

This behaviour was REVIEWED at v0.3.0 (issue #6: the smart-quote
crash turned out to be an encoding problem at the IO edge, not a
tokenizer problem) and is considered stable. The regex below has not
changed since v0.1.
"""
from __future__ import annotations

import re

TERM_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list:
    """Raw text -> list of terms (lowercased, length >= 2)."""
    return [t for t in TERM_RE.findall(text.lower()) if len(t) >= 2]
