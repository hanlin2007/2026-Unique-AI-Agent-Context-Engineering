"""Corporate password policy checks.

The policy text lives in docs/policy.md and is the CONTRACT; this
module implements it literally. Rule ids returned by validate(), in
the fixed order they are reported:

    min_length     at least MIN_LEN characters (boundary INCLUSIVE:
                   exactly MIN_LEN characters is acceptable)
    needs_upper    at least one uppercase letter A-Z
    needs_lower    at least one lowercase letter a-z
    needs_digit    at least one digit 0-9
    needs_special  at least one special character from SPECIAL
    blacklisted    not on the common-password list (case-insensitive)

validate() returns the ids of VIOLATED rules only, so an empty list
means the password is compliant. is_compliant() is the boolean form.
"""
from __future__ import annotations

from .blacklist import is_common

MIN_LEN = 8

# Special characters recognised by the policy. The authoritative list
# is docs/policy.md section 3.5 ("symbols"): ! @ # $ % ^ & * - _
SPECIAL = frozenset("!@#$%^&*")

RULE_ORDER = (
    "min_length",
    "needs_upper",
    "needs_lower",
    "needs_digit",
    "needs_special",
    "blacklisted",
)


def validate(password: str) -> list:
    """Ids of the rules `password` violates (empty list == compliant)."""
    if not isinstance(password, str):
        raise TypeError("password must be a str")
    violated = []
    if len(password) <= MIN_LEN:
        violated.append("min_length")
    if not any(c.isupper() for c in password):
        violated.append("needs_upper")
    if not any(c.islower() for c in password):
        violated.append("needs_lower")
    if not any(c.isdigit() for c in password):
        violated.append("needs_digit")
    if not any(c in SPECIAL for c in password):
        violated.append("needs_special")
    if is_common(password):
        violated.append("blacklisted")
    return violated


def is_compliant(password: str) -> bool:
    """True when `password` violates no policy rule."""
    return not validate(password)


def describe(rule_id: str) -> str:
    """Human-readable explanation of a rule id, for CLI output."""
    return {
        "min_length": f"at least {MIN_LEN} characters",
        "needs_upper": "at least one uppercase letter",
        "needs_lower": "at least one lowercase letter",
        "needs_digit": "at least one digit",
        "needs_special": f"at least one of {''.join(sorted(SPECIAL))}",
        "blacklisted": "too common (on the blacklist)",
    }[rule_id]
