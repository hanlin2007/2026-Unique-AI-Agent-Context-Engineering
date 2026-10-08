"""Access-log line parsing (nginx combined format).

One parser, used by everything downstream. The regex is anchored and
covers the full combined format including the quoted referrer and
User-Agent fields; lines that do not match are collected into a
rejects list, never silently dropped.

NOTE: this module has history. Issues #17 and #35 were both parsing
incidents (unescaped referrers; vhost-prefixed logs), and the OPEN
issue #71 ("requests lost on quoted referrers") is also tracked here.
If request counts look LOW -- whole hours light, totals short of the
CDN's numbers -- audit LINE_RE first; see KNOWN_ISSUES.md and
fix_suggestion.md. The analytics modules (buckets / stats) were
reviewed at v0.3.0 and are considered stable.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone

LINE_RE = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<ts>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) [^"]*" '
    r'(?P<status>\d{3}) (?P<bytes>\S+) '
    r'"(?P<referrer>(?:[^"\\]|\\.)*)" '
    r'"(?P<ua>(?:[^"\\]|\\.)*)" '
    r'(?P<rt>[\d.]+)$'
)

TS_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


@dataclass(frozen=True)
class Event:
    ts: float        # unix epoch seconds (utc)
    method: str
    path: str
    status: int
    response_time: float  # seconds


def parse_line(line: str):
    """One line -> Event, or None if the line does not match."""
    m = LINE_RE.match(line.strip())
    if not m:
        return None
    dt = datetime.strptime(m["ts"], TS_FORMAT)
    return Event(
        ts=dt.astimezone(timezone.utc).timestamp(),
        method=m["method"],
        path=m["path"],
        status=int(m["status"]),
        response_time=float(m["rt"]),
    )


def parse_log(path: str) -> tuple:
    """File -> (events, rejected_lines), file order preserved."""
    events, rejects = [], []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            ev = parse_line(line)
            (events if ev else rejects).append(ev if ev else line.rstrip("\n"))
    return events, rejects
