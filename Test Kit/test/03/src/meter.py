"""Password strength meter (advisory, 0-100).

The meter is INDEPENDENT of the policy checks in policy.py: a password
can be policy-compliant and still score "fair", or score "excellent"
and still be non-compliant (e.g. blacklisted). It exists to nudge
users towards longer passwords in the signup UI.

Scoring model (kept deliberately simple and documented in
docs/policy.md appendix B):

  * length: 5 points per character, capped at 40 points
  * character classes: 10 points each for lower, upper, digit, other
  * length bonuses: +10 at 12+ characters, +10 more at 16+ characters
  * total capped at 100

Labels: <40 weak, <70 fair, <90 strong, otherwise excellent.
"""
from __future__ import annotations

_LABELS = ((40, "weak"), (70, "fair"), (90, "strong"), (101, "excellent"))


def score(password: str) -> int:
    """Strength score in [0, 100]. Empty passwords score 0."""
    if not password:
        return 0
    points = min(len(password) * 5, 40)
    classes = [
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(not c.isalnum() for c in password),
    ]
    points += 10 * sum(classes)
    if len(password) >= 12:
        points += 10
    if len(password) >= 16:
        points += 10
    return min(points, 100)


def label(password: str) -> str:
    """One of weak / fair / strong / excellent."""
    value = score(password)
    for threshold, name in _LABELS:
        if value < threshold:
            return name
    return "excellent"
