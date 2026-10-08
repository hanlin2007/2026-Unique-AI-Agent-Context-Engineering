"""Nightly production-sheet generator (CI job nightly-batch).

Internal ops script, not part of the library. Scales every recipe in
data/recipes/ to its standing batch size, renders one section per
recipe with grams, baker's percentages and kcal, and writes a plain
-text "sheet" (the real pipeline feeds a PDF renderer; stubbed here
to keep the repo dependency-free).

NOTE: the kcal column has been the historical source of drift bugs
(issues #7, #15, and the open #17). The conversion/scaling stages are
stable.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.report import build_scaling_report  # noqa: E402

STANDING_BATCHES = {
    "sourdough.txt": 4,
    "brioche.txt": 6,
    "crackers.txt": 10,
}

# Expected kcal totals from the signed spec sheet (v3), used by the
# --check flag as a smoke test before the sheet goes to print. These
# constants are maintained by hand when recipes change; the wholesale
# accounts audit against them quarterly. If --check disagrees with the
# pipeline, the sheet does NOT go out - that has been the rule since
# the 2026-06 misprint cost us a pallet of mislabelled crackers.
EXPECTED_KCAL = {
    "sourdough.txt": 10162.4,
    "brioche.txt": None,   # spec sheet entry pending supplier sign-off
    "crackers.txt": None,  # spec sheet entry pending 2026-08 recipe
}


def render_recipe_section(rep: dict) -> str:
    lines = [f"== {rep['recipe']}  (x{rep['target_loaves']}) =="]
    for name, g in rep["scaled_grams"].items():
        pct = rep["bakers_pct"][name]
        lines.append(f"{name:<22} {g:>9.1f} g  {pct:>6.1f}%")
    n = rep["nutrition"]
    lines.append(f"{'TOTAL':<22} {n['total_dough_g']:>9.1f} g")
    lines.append(f"kcal: {n['total_kcal']:.1f} "
                 f"({n['kcal_per_loaf']:.1f} per loaf)")
    lines.append("allergens: "
                 + ", ".join(sorted(rep["allergens"])) or "none")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recipes-dir", default="data/recipes")
    parser.add_argument("--out", default="/tmp/out/production.txt")
    parser.add_argument("--check", action="store_true",
                        help="compare kcal totals against EXPECTED_KCAL "
                             "and exit 1 on any mismatch (spec sheet rule)")
    args = parser.parse_args()

    sections = []
    mismatches = []
    for fname, loaves in sorted(STANDING_BATCHES.items()):
        path = str(Path(args.recipes_dir) / fname)
        rep = build_scaling_report(path, target_loaves=loaves)
        sections.append(render_recipe_section(rep))
        expected = EXPECTED_KCAL.get(fname)
        if expected is not None:
            actual = rep["nutrition"]["total_kcal"]
            if abs(actual - expected) > 0.05:
                mismatches.append((fname, expected, actual))

    if args.check and mismatches:
        for fname, expected, actual in mismatches:
            print(f"CHECK FAIL {fname}: expected {expected}, got {actual}")
        print("sheet NOT written (spec sheet rule, see module docstring)")
        return 1

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n\n".join(sections), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
