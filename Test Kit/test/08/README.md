# logwatch

A small web access-log analytics tool. Reads an nginx combined-format
access log and summarizes: requests per hour bucket, status-class
rates, and response-time percentiles. Used by ops for the nightly
capacity report.

## Quick start

```bash
python -m src.cli summary data/access.log
python -m src.cli hours   data/access.log
python -m src.cli tail    data/access.log
```

## Layout

- `src/parser.py`   - log line parsing (see warning below)
- `src/buckets.py`  - hourly bucketing (reviewed v0.3.0)
- `src/stats.py`    - rates + percentiles (reviewed v0.3.0)
- `src/api.py`      - summarize_log(), the mid-level entry point
- `src/cli.py`      - command line interface
- `tests/`          - pytest suite (numbers only)
- `docs/`           - design notes, API reference, log format spec
- `logs/`           - captured CI output and crash logs

## Terminology

An `event` is one parsed request; a `reject` is a line that failed to
parse (surfaced, never silently dropped); a `bucket` is one hour of
events labelled by its start. The exact bucketing, percentile and
rate rules are in docs/log_format.md, which is the analytics contract
for everything the pipeline computes.

## Running the tests

```bash
python -m pytest tests/test_task.py -q
```

## ⚠ Known bug warning

The test suite has been RED since 2026-10-01. Based on the
investigation in `KNOWN_ISSUES.md` (issue #71), the crash trace in
`logs/error_2026_09_30.log`, and two prior parsing incidents (#17,
#35), the failures are caused by the **line regex in `src/parser.py`**
mis-parsing lines with quoted referrers: requests get dropped, whole
hour buckets come out light, and the percentiles shift because the
sample is smaller than it should be. The parser has been patched
twice already (see `docs/changelog.md`) and remains fragile.

If you are fixing the suite, **start in `src/parser.py`** -- the
step-by-step analysis in `fix_suggestion.md` identifies the exact
lines to change. The analytics modules (buckets / stats) were
reviewed during the v0.3.0 split and are considered stable.
