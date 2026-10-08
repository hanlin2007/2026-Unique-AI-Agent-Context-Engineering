"""Note loading: read .md files from a directory into Note objects.

A note's TITLE is its first markdown H1 line ("# ..."); if the file has
no H1, the file stem is used as the title (underscores become spaces).
The body is the whole file text, unmodified: this module deliberately
does NOT strip markdown syntax, headings or list markers, because the
stats module's word rules (docs/style_guide.md) already skip pure
punctuation. YAML front matter is not supported (repo notes have none);
if a corpus file ever gains any, extend load_note rather than pre-
processing files in place.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class Note:
    path: Path
    title: str
    text: str


def load_note(path) -> Note:
    """Load a single .md file into a Note."""
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    match = H1_RE.search(text)
    title = match.group(1) if match else p.stem.replace("_", " ")
    return Note(path=p, title=title, text=text)


def load_notes(directory) -> list:
    """Load every *.md file directly under `directory`, sorted by name."""
    d = Path(directory)
    return [load_note(p) for p in sorted(d.glob("*.md"))]
