# API reference

v1.3.1. Human-maintained; minor drift possible.

## src.policy
### MIN_LEN: int = 8
Minimum password length. Boundary is INCLUSIVE (docs/policy.md 3.1).
### SPECIAL: frozenset
The ten-symbol special class from docs/policy.md 3.5.
### RULE_ORDER: tuple
Fixed reporting order for validate().
### validate(password) -> list[str]
Ids of violated rules, in RULE_ORDER. Empty list == compliant.
Raises TypeError on non-str input.
### is_compliant(password) -> bool
Boolean form of validate().
### describe(rule_id) -> str
Human-readable rule text, for CLI/UX copy.

## src.blacklist
### COMMON_PASSWORDS: tuple[str]
Reviewed common-password list, lowercased, sorted. Migrated inline
from data/common_passwords.txt at v1.2.0. The data file is audit-only
and is NOT read at runtime.
### is_common(password) -> bool
Case-insensitive exact membership. Empty string -> False.

## src.meter
### score(password) -> int
Advisory strength, 0-100 (docs/policy.md appendix B). Independent of
policy compliance.
### label(password) -> str
weak / fair / strong / excellent.

## src.cli
### main(argv) -> int
Commands: check / score / audit. Exit codes: 0 ok, 1 violations found,
2 usage error.

## Data files
### data/common_passwords.txt
AUDIT COPY of the blacklist, including the struck-out section from the
2026-06 review. Not read at runtime. Format: one lowercased entry per
line; `#` lines are comments; the struck section begins at the
`## audit - struck 2026-06 ##` marker.
### data/breach_sample.csv
Anonymised sample from the 2026-Q2 credential-stuffing incident feed.
Columns: sample_id, source, seen_count, first_seen, notes. Used by
scripts/audit_passwords.py demos only; contains no real credentials.

## Exit codes (cli + audit script)

| code | meaning                                  |
|------|------------------------------------------|
| 0    | compliant / audit clean                  |
| 1    | violations found                         |
| 2    | usage error (bad args, missing file)     |

## Versioning notes

The library follows semver loosely: patch releases may extend the
blacklist (data-only change), minor releases may add rules, and rule
SEMANTICS changes (like the 2024-11 length amendment) always ship with
a docs/policy.md update in the same commit.
