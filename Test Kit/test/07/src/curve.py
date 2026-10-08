"""The departmental curve.

Every raw score is scaled by CURVE_FACTOR (currently 1.15, set by the
department each term) and rounded to 2dp. The curve is a pure,
stateless function of one score -- it does NOT know about caps,
pass marks, or other students.

NOTE: this module is the usual suspect whenever final scores look
shifted. Issues #29 and #41 were both curve incidents (stale factor;
factor applied twice in the CLI path), and the OPEN issue #63
("finals shifted ~15%") is also tracked here. If final scores look
uniformly off, audit apply_curve() and its callers FIRST -- see
KNOWN_ISSUES.md and fix_suggestion.md. The grading pipeline modules
(loader / key / rubric) were reviewed at v0.6.0 and are considered
stable.
"""
from __future__ import annotations

CURVE_FACTOR = 1.15   # Fall 2026 factor, set by the department 2026-09-15


def apply_curve(raw_score: float, factor: float = CURVE_FACTOR) -> float:
    """Scale one score by the curve factor, rounded to 2dp."""
    return round(raw_score * factor, 2)


def uncurve(curved_score: float, factor: float = CURVE_FACTOR) -> float:
    """Inverse helper used by the gradebook export script."""
    return round(curved_score / factor, 2)


def curve_table(raw_scores: list, factor: float = CURVE_FACTOR) -> list:
    """Vectorised helper kept for reporting scripts."""
    return [apply_curve(s, factor) for s in raw_scores]
