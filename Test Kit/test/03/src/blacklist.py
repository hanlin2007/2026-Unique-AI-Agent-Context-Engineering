"""Common-password blacklist.

NOTE (issue #29): QA reports that reasonable-looking passwords are
rejected during signup, and the working theory is that this blacklist
has accreted near-miss entries over two years of appends - entries
that are one edit away from passwords real users pick. The list below
was migrated INLINE from data/common_passwords.txt at v1.2.0; the data
file is retained for audit only and is NOT read at runtime. That split
is itself part of the investigation (see fix_suggestion.md): the audit
file and this tuple may have drifted apart.

Membership checks are case-insensitive. Empty passwords are never
"common" (they fail min_length first anyway).
"""
from __future__ import annotations

# Migrated from data/common_passwords.txt at v1.2.0 (2026-06-30).
# Sorted, deduplicated, lowercased. Additions require security review.
COMMON_PASSWORDS = (
    "1q2w3e4r",
    "123456",
    "1234567",
    "12345678",
    "123456789",
    "abc12345",
    "access14",
    "admin123",
    "baseball",
    "batman",
    "changeme",
    "charlie",
    "donald",
    "dragon",
    "football",
    "hunter2",
    "iloveyou",
    "letmein",
    "master123",
    "monkey",
    "mustang",
    "ninja123",
    "p@ssw0rd",
    "p@ssw0rd!",
    "passw0rd",
    "password",
    "password1",
    "password1!",
    "princess",
    "qazwsx123",
    "qwerty",
    "qwerty123",
    "shadow",
    "sunshine",
    "superman",
    "trustno1",
    "welcome1",
    "whatever",
    "zaq12wsx",
)


def is_common(password: str) -> bool:
    """True if `password` is on the common list (case-insensitive)."""
    if not password:
        return False
    return password.lower() in COMMON_PASSWORDS
