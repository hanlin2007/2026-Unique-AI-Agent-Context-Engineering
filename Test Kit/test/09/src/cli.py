"""Command line interface for recipescale.

Usage:
    python -m src.cli show       data/recipes/sourdough.txt [LOAVES]
    python -m src.cli pct        data/recipes/sourdough.txt
    python -m src.cli kcal       data/recipes/sourdough.txt [LOAVES]
    python -m src.cli allergens  data/recipes/sourdough.txt
"""
from __future__ import annotations

import sys

from .parser import parse_recipe
from .report import build_scaling_report


def _render_table(headers, rows) -> str:
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    line = "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    sep = "  ".join("-" * w for w in widths)
    body = ["  ".join(str(c).ljust(widths[i]) for i, c in enumerate(row))
            for row in rows]
    return "\n".join([line, sep, *body])


def _cmd_show(path: str, loaves: int) -> None:
    rep = build_scaling_report(path, target_loaves=loaves)
    print(f"recipe: {rep['recipe']}  "
          f"(base {rep['base_loaves']} -> target {rep['target_loaves']})")
    rows = [(name, f"{g:.1f}") for name, g in rep["scaled_grams"].items()]
    print(_render_table(["ingredient", "grams"], rows))
    n = rep["nutrition"]
    print(f"dough: {n['total_dough_g']:.1f} g   "
          f"kcal: {n['total_kcal']:.1f} total / {n['kcal_per_loaf']:.1f} per loaf")


def _cmd_pct(path: str) -> None:
    rep = build_scaling_report(path)
    rows = [(name, f"{p:.1f}%") for name, p in rep["bakers_pct"].items()]
    print(_render_table(["ingredient", "baker's %"], rows))


def _cmd_kcal(path: str, loaves: int) -> None:
    rep = build_scaling_report(path, target_loaves=loaves)
    n = rep["nutrition"]
    print(f"total_kcal={n['total_kcal']:.1f} "
          f"kcal_per_loaf={n['kcal_per_loaf']:.1f}")


def _cmd_allergens(path: str) -> None:
    rep = build_scaling_report(path)
    for allergen, count in rep["allergens"].items():
        print(f"{allergen}: {count}")


def main(argv) -> int:
    if len(argv) < 3:
        print(__doc__)
        return 2
    cmd, path = argv[1], argv[2]
    loaves = int(argv[3]) if len(argv) > 3 else 1
    if cmd == "show":
        _cmd_show(path, loaves)
    elif cmd == "pct":
        _cmd_pct(path)
    elif cmd == "kcal":
        _cmd_kcal(path, loaves)
    elif cmd == "allergens":
        _cmd_allergens(path)
    else:
        print(f"unknown command: {cmd}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
