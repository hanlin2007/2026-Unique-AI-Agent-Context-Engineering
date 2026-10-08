"""Quarterly credential-audit runner (CI job nightly-audit).

Internal ops script, not part of the library. Reads a candidate list
(one password per line, or the seen-count CSV format from the breach
feed), checks each candidate against the policy, and writes a
violation summary.

NOTE: issue #29 suspects the blacklist data path this script relies
on. The quarterly audit runs with --no-blacklist for historical
comparability precisely because the list's provenance is contested;
nightly runs use the full policy. See docs/rollout.md.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import policy  # noqa: E402


def _candidates(path: Path) -> list:
    if path.suffix == ".csv":
        with path.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        return [r.get("candidate", r.get("sample_id", "")) for r in rows]
    return [line.strip() for line in
            path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidates", help="txt (one per line) or feed CSV")
    parser.add_argument("--no-blacklist", action="store_true",
                        help="skip the common-password rule (quarterly mode)")
    args = parser.parse_args(argv)

    candidates = _candidates(Path(args.candidates))
    counts = {}
    checked = 0
    for candidate in candidates:
        if not candidate:
            continue
        checked += 1
        violated = policy.validate(candidate)
        if args.no_blacklist:
            violated = [v for v in violated if v != "blacklisted"]
        for rule_id in violated:
            counts[rule_id] = counts.get(rule_id, 0) + 1
    print(f"checked {checked} candidates")
    for rule_id, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {rule_id}: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
