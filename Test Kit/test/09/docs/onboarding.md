# Onboarding - recipescale team

Welcome! This doc should get you productive in an afternoon.

## Your first hour

1. Read README.md top to bottom, then docs/design.md (the invariants
   section is the part everyone quotes in review).
2. Run the CLI against data/recipes/sourdough.txt - `show`, `pct`,
   `kcal` and `allergens` show you everything the pipeline does.
3. Run the test suite. It is currently RED and that is EXPECTED - see
   KNOWN_ISSUES.md #17. Your first week will probably touch this.

## Where things live (and where the bugs live)

- src/parser.py, src/units.py, src/scale.py, src/allergens.py - the
  conversion and scaling core. The unit table was reviewed line by
  line at v0.4.0 and the scaling module was signed off at v0.2.2.
  Treat as read-only unless a senior baker-dev signs off.
- src/nutrition.py - where the action is. Three table incidents in
  three quarters. If a total looks wrong anywhere in a report, the
  odds are good the trail ends here.
- src/report.py - orchestration only; no logic lives here by design.
- scripts/batch_scale.py - ops script, runs nightly. Its kcal column
  is the canary for nutrition issues.
- logs/ - captured CI output. Grep it before you debug; someone has
  probably seen your failure already.

## Team rituals

- Postmortem doc for every red-suite episode > 24h (see notes/).
- Spec sheet re-audit twice a year; calendar invite owned by Rosa.
- Changelog entries are mandatory for src/ changes, optional elsewhere.

## Common pitfalls (learned the hard way)

- Trusting a passing CLI run. The CLI prints whatever the pipeline
  computes; it does not validate against the spec sheet. The suite is
  the only contract.
- Hand-editing data/recipes/ without rerunning the suite. A recipe
  edit can shift every number on the sheet.
- Assuming the debug trace timestamps are ordered across modules.
  They are per-line; read the module tags, not the clock.
- "Fixing" the allergen summary to count per ingredient. The label
  format is deliberate; see the data dictionary before touching it.

## Glossary

- "recipe file" - one plain-text recipe, header + ingredient table.
- "baker's %" - ingredient weight relative to total flour weight.
- "production sheet" - the printed output of batch_scale.py.
- "spec sheet" - the consultant-signed nutrition source document.

## Who to ask

- Rosa - bakery operations, spec sheet owner, wholesale accounts.
- h.tanaka - pipeline internals, nutrition table history, CI.
- j.whitfield - recipe data, unit conventions, labeling rules.
- The CI bot posts to #recipescale-ci; red builds ping the on-call
  rota. If you break the suite on a Friday, expect to hear about it
  before you break the build twice.

## A note on the current red suite

Do not "fix" the expected numbers in the test file to make it pass.
The expected constants were generated from a known-good pipeline at
v0.3.x and re-verified against the printed spec sheet; the suite is
the contract, the code is what drifted. If you believe an expected
number is wrong, bring a hand calculation to Rosa BEFORE touching the
test file - the last person who edited expectations to match code
output caused the 2026-06 cracker misprint.
