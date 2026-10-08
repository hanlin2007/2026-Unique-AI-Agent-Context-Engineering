"""Task test-suite: `pytest tests/test_task.py` must pass.

BLACK-BOX contract: these tests treat the whole of src/ as one opaque
pipeline and only check the NUMBERS that come out of build_settlement().
Where inside the pipeline a wrong number is produced is for you to find.

Fixture: data/expenses.csv (an 8-day group trip, 81 expenses, six
travellers, EUR). Report built with fx="USD".

Semantics live in docs/data_dictionary.md: shares of one expense sum
EXACTLY to the expense amount; a transfer (A -> B) means A pays B;
net balances are computed over ALL expenses.

Run from the task root with:  python -m pytest tests/test_task.py -q
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.report import build_settlement

SETTLEMENT = build_settlement("data/expenses.csv", fx="USD")


def test_report_structure():
    assert SETTLEMENT["currency"] == "EUR"
    assert SETTLEMENT["expense_count"] == 81
    assert set(SETTLEMENT) >= {"balances", "transfers", "grand_total_eur", "fx"}


def test_people_roster():
    assert SETTLEMENT["people"] == ["anna", "ben", "carla", "dan", "erin", "finn"]
    assert set(SETTLEMENT["balances"]) == set(SETTLEMENT["people"])


def test_balance_anna():
    assert SETTLEMENT["balances"]["anna"] == 97.72


def test_balance_dan():
    assert SETTLEMENT["balances"]["dan"] == -589.98


def test_balance_erin():
    assert SETTLEMENT["balances"]["erin"] == 250.55


def test_transfer_count():
    # greedy simplification settles this trip in exactly four transfers
    assert len(SETTLEMENT["transfers"]) == 4


def test_transfers_exact():
    assert SETTLEMENT["transfers"] == [
        {"from": "dan", "to": "carla", "amount": 589.98},
        {"from": "ben", "to": "erin", "amount": 250.55},
        {"from": "ben", "to": "anna", "amount": 97.72},
        {"from": "ben", "to": "carla", "amount": 62.0},
    ]


def test_grand_total_eur():
    # sum of all per-person shares across all 81 expenses; conservation
    # means this equals the sum of expense amounts to the cent
    assert SETTLEMENT["grand_total_eur"] == 5962.84


def test_fx_grand_total_usd():
    assert SETTLEMENT["fx"]["ccy"] == "USD"
    assert SETTLEMENT["fx"]["grand_total"] == 6476.84


def test_transfers_well_formed():
    people = set(SETTLEMENT["people"])
    for transfer in SETTLEMENT["transfers"]:
        assert transfer["from"] in people
        assert transfer["to"] in people
        assert transfer["from"] != transfer["to"]
        assert transfer["amount"] > 0
