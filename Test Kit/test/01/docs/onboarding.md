# Onboarding - ledgetool team

Welcome! This doc should get you productive in an afternoon.

## Your first hour

1. Read README.md top to bottom, then docs/design.md (the invariants
   section is the part everyone quotes in review).
2. Run the CLI against data/journal_main.csv - `report`, `months` and
   `daily` show you everything the pipeline does.
3. Run the test suite. It is currently RED and that is EXPECTED - see
   KNOWN_ISSUES.md #42. Your first week will probably touch this.

## Where things live (and where the bugs live)

- src/journal.py, src/normalize.py, src/daily.py, src/aggregate.py,
  src/interest.py - the pipeline. Split out of the old ledger.py at
  v0.5.0 and reviewed then. Treat as read-only unless a staff engineer
  signs off.
- src/currency.py - where the action is. Three rounding incidents in
  two quarters. If a number looks wrong anywhere in a report, the odds
  are good the trail ends here.
- src/rates.py - rate table, quarterly snapshots, never hand-edit.
- src/report.py - orchestration only; no logic lives here by design.
- scripts/generate_report.py - ops script, runs nightly. Its fx
  appendix is the canary for currency issues.
- logs/ - captured CI output. Grep it before you debug; someone has
  probably seen your failure already.

## Team rituals

- Postmortem doc for every red-suite episode > 24h (see notes/).
- Rate table refreshes quarterly; calendar invite owned by Priya.
- Changelog entries are mandatory for src/ changes, optional elsewhere.

## Glossary

- "journal" - one CSV of transactions, single currency, date-sorted.
- "rollup" - the output of compute_daily_rollups.
- "fx appendix" - the currency-converted totals at the end of the
  report. Historically cursed.
- "canonical kind" - deposit/withdrawal; see docs/data_dictionary.md.
