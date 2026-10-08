# Onboarding - budgetsplit team

Welcome! This doc should get you productive in an afternoon.

## Your first hour

1. Read README.md top to bottom, then docs/data_dictionary.md - the
   dictionary is the contract everyone quotes in review, especially
   the sections on shares and transfers.
2. Run the CLI against data/expenses.csv: `report`, `balances` and
   `transfers` show you everything the engine does.
3. Run the test suite. It is currently RED and that is EXPECTED - see
   KNOWN_ISSUES.md #51. Your first week will probably touch this.

## Where things live (and where the bugs live)

- src/ledger.py, src/split.py, src/settle.py, src/report.py - the
  engine. Split out of the old monolith at v0.9.0 and reviewed then.
  Treat as read-only unless a staff engineer signs off.
- src/fx.py - where the action is. Two rounding incidents last year
  and an open one now. If a number looks wrong anywhere in a report,
  the odds are good the trail ends here.
- src/rates.py - monthly snapshot, never hand-edit (v0.3.1 incident).
- scripts/monthly_close.py - ops script, runs the monthly close for
  the finance channel. Its fx appendix is the canary for fx issues.
- logs/ - captured CI output. Grep it before you debug; someone has
  probably seen your failure already.

## Team rituals

- Settlement reports are NEVER sent from a red build. The trip group
  is waiting on the current one, which is why #51 is high priority.
- The data dictionary changes only by group consensus, and the code
  changes to match - never the other way around.
- If you propose touching the engine modules, pair with someone who
  was here for the v0.9.0 split. If you propose touching fx.py, pair
  with anyone - it is everyone's shared nemesis.
