# Onboarding - stocktake team

Welcome! This doc should get you productive in an afternoon.

## Your first hour

1. Read README.md top to bottom, then docs/design.md (the invariants
   section is the part everyone quotes in review).
2. Run the CLI against data/lots.csv + data/movements.csv - `report`,
   `reorder` and `valuation` show you everything the pipeline does.
3. Run the test suite. It is currently RED and that is EXPECTED - see
   KNOWN_ISSUES.md #57. Your first week will probably touch this.

## Where things live (and where the bugs live)

- src/lots.py, src/transfers.py - the lot pipeline. Rewritten at v0.4.0
  and reviewed then. Treat as read-only unless a staff engineer signs
  off.
- src/valuation.py - where the action is. Three rounding incidents in
  three quarters (#31, #44, and the open #57). If a money number looks
  wrong anywhere in a report, the odds are good the trail ends here.
- src/reorder.py, src/catalog.py - small, stable, boring.
- src/report.py - orchestration only; no logic lives here by design.
- scripts/nightly_snapshot.py - ops script, runs nightly. Its valuation
  canary line is the early-warning for valuation issues.
- logs/ - captured CI output. Grep it before you debug; someone has
  probably seen your failure already.

## Team rituals

- Postmortem doc for every red-suite episode > 24h (see notes/).
- Cycle count every second Friday; discrepancies go to inventory
  control, not into the repo.
- Changelog entries are mandatory for src/ changes, optional elsewhere.

## Glossary

- "lot" - one receipt row: quantity at a unit cost, in one warehouse.
- "movement" - one row of the movements CSV: an order (stock out) or
  a transfer (stock between warehouses).
- "closing" - remaining units after all movements are applied.
- "valuation" - money value of remaining stock. Historically cursed.
- "reorder point" - catalogue-level stock threshold, total across
  warehouses.
