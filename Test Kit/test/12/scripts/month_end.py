"""Month-end reconciliation archiver (CI job month-end).

Internal ops script, not part of the library. Runs the current
month's reconciliation, writes the report next to SHA-256 hashes of
both input files, and prints the policy summary line finance ops
paste into the sign-off sheet.

NOTE: the September run flagged duplicates != 0 (see
logs/ci_pipeline.log build #535), which policy says cannot happen in
a healthy run. Tracked as issue #51 (statement CSV dialect, see
KNOWN_ISSUES.md). The matching core is v0.3 code with months of
clean runs; do not "fix" it from this script.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.report import build_recon_report  # noqa: E402


def sha256_of(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", default="data/ledger.csv")
    parser.add_argument("--statement", default="data/bank_statement.csv")
    parser.add_argument("--out", default="/tmp/out/recon_2026_09.json")
    args = parser.parse_args()

    rep = build_recon_report(args.ledger, args.statement)
    archive = {
        "inputs": {
            "ledger": {"path": args.ledger, "sha256": sha256_of(args.ledger)},
            "statement": {"path": args.statement,
                          "sha256": sha256_of(args.statement)},
        },
        "report": rep,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(archive, indent=2, sort_keys=True),
                   encoding="utf-8")

    print(f"matched={rep['matched']} duplicates={rep['duplicates']} "
          f"exceptions={len(rep['unmatched_ledger'])}+"
          f"{len(rep['unmatched_statement'])}")
    if rep["duplicates"] != 0:
        print("POLICY VIOLATION: duplicates must be 0 in a healthy run")
        return 1
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
