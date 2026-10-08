# Onboarding - logwatch team

Welcome! This doc should get you productive in an afternoon.

## Your first hour

1. Read README.md top to bottom, then docs/log_format.md (it is the
   analytics contract; docs/design.md explains how the code maps onto
   it).
2. Run the CLI against data/access.log - `summary`, `hours` and
   `tail` show you everything the pipeline does.
3. Run the test suite. It is currently RED and that is EXPECTED - see
   KNOWN_ISSUES.md #71. Your first week will probably touch this.

## Where things live (and where the bugs live)

- src/buckets.py, src/stats.py - the analytics. Split out of the old
  analyze.py at v0.3.0 and reviewed then. Treat as read-only unless a
  staff engineer signs off.
- src/parser.py - where the action is. Three parsing incidents in a
  year (#17, #35, and the open #71). If a count looks low anywhere,
  the odds are good the trail ends here.
- src/api.py - thin orchestration; no logic lives here by design.
- scripts/nightly_capacity.py - ops job; its CDN cross-check line is
  the early-warning for sample-shortage issues.
- logs/ - captured CI output. Grep it before you debug; someone has
  probably seen your failure already.

## Team rituals

- Postmortem doc for every red-suite episode > 24h (see notes/).
- The APM percentile method is reviewed quarterly against
  docs/log_format.md (s.lindgren owns the calendar invite).
- Changelog entries are mandatory for src/ changes, optional elsewhere.

## Glossary

- "event" - one parsed request.
- "reject" - a line that didn't parse; surfaced, never dropped.
- "bucket" - one hour of requests, labelled by its start.
- "the sample" - the parsed events all stats are computed on.
- "the parser" - src/parser.py. Historically cursed.
