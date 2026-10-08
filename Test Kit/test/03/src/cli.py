"""Command line interface for passpolicy.

Usage:
    python -m src.cli check  <password>
    python -m src.cli score  <password>
    python -m src.cli audit  <file-with-one-password-per-line>
"""
from __future__ import annotations

import sys

from . import meter, policy


def _cmd_check(password: str) -> int:
    violated = policy.validate(password)
    if not violated:
        print("compliant")
        return 0
    print("non-compliant:")
    for rule_id in violated:
        print(f"  {rule_id}: {policy.describe(rule_id)}")
    return 1


def _cmd_score(password: str) -> None:
    print(f"{meter.score(password)}/100 ({meter.label(password)})")


def _cmd_audit(path: str) -> int:
    with open(path, encoding="utf-8") as fh:
        candidates = [line.rstrip("\n") for line in fh if line.strip()]
    bad = 0
    for candidate in candidates:
        if not policy.is_compliant(candidate):
            bad += 1
            print(f"FAIL {candidate!r}: {', '.join(policy.validate(candidate))}")
    print(f"audited {len(candidates)} passwords, {bad} non-compliant")
    return 1 if bad else 0


def main(argv) -> int:
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    command, operand = argv[1], argv[2]
    if command == "check":
        return _cmd_check(operand)
    if command == "score":
        _cmd_score(operand)
        return 0
    if command == "audit":
        return _cmd_audit(operand)
    print(f"unknown command: {command}")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
