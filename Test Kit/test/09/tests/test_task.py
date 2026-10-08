"""Task test-suite: `pytest tests/test_task.py` must pass.

BLACK-BOX contract: these tests treat the whole pipeline as opaque
and only check the NUMBERS that come out of build_scaling_report().
Where inside the pipeline a wrong number is produced is for you to
find.

Fixture: data/recipes/sourdough.txt (6 ingredients, one loaf base),
scaled to target_loaves=4.

Run from the task root with:  python -m pytest tests/test_task.py -q
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.report import build_scaling_report

REP = build_scaling_report("data/recipes/sourdough.txt", target_loaves=4)


def test_report_structure():
    assert REP["recipe"] == "Classic Sourdough"
    assert REP["base_loaves"] == 1
    assert REP["target_loaves"] == 4
    assert set(REP) >= {"scaled_grams", "bakers_pct", "allergens",
                        "nutrition"}


def test_scaled_flour_grams():
    assert REP["scaled_grams"]["strong bread flour"] == 2000.0
    assert REP["scaled_grams"]["whole wheat flour"] == 400.0


def test_scaled_water_and_salt_grams():
    assert REP["scaled_grams"]["water"] == 1600.0
    assert REP["scaled_grams"]["sea salt"] == 44.0


def test_scaled_honey_grams():
    # 1 tbsp per loaf, 4 loaves
    assert REP["scaled_grams"]["honey"] == 60.0


def test_bakers_pct_water():
    assert REP["bakers_pct"]["water"] == 66.7


def test_bakers_pct_starter_and_salt():
    assert REP["bakers_pct"]["sourdough starter"] == 20.0
    assert REP["bakers_pct"]["sea salt"] == 1.8


def test_bakers_pct_flour_entries():
    assert REP["bakers_pct"]["strong bread flour"] == 83.3
    assert REP["bakers_pct"]["whole wheat flour"] == 16.7


def test_allergen_summary():
    assert REP["allergens"] == {"gluten": 1, "wheat": 1}


def test_nutrition_totals():
    assert REP["nutrition"]["total_kcal"] == 10162.4
    assert REP["nutrition"]["kcal_per_loaf"] == 2540.6


def test_total_dough_weight():
    assert REP["nutrition"]["total_dough_g"] == 4584.0
