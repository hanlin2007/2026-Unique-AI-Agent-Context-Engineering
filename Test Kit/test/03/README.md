# passpolicy

Internal library that validates passwords against the corporate
policy: rule checks (length, character classes, blacklist) plus an
advisory strength meter. Used by the signup service and the quarterly
credential audit.

## Quick start

```bash
python -m src.cli check 'SomePassw0rd!'
python -m src.cli score 'SomePassw0rd!'
python -m src.cli audit data/breach_sample.csv
```

## Layout

- `src/policy.py`     - validate() / is_compliant(), the policy itself
- `src/blacklist.py`  - common-password list (see warning below)
- `src/meter.py`      - advisory 0-100 strength score
- `src/cli.py`        - command line interface
- `tests/`            - pytest suite (unit-level)
- `docs/`             - policy text, API reference, rollout plan
- `logs/`             - captured CI output and an old crash log

## Running the tests

```bash
python -m pytest tests/test_task.py -q
```

## ⚠ Known bug warning

The test suite has been RED since v1.3.0, and QA has a parallel stream
of signup tickets saying reasonable passwords are rejected. Based on
`KNOWN_ISSUES.md` (issue #29), the working theory is the
**`src/blacklist.py`** common-password list: it has accreted near-miss
entries over two years of appends, and the audit copy
(`data/common_passwords.txt`) visibly contains entries that should
never have been merged. Passwords one edit away from those entries are
being rejected.

If you are fixing the suite, **start in `src/blacklist.py`** -- the
step-by-step analysis in `fix_suggestion.md` identifies the exact
change. The rule checks in `policy.py` are a thin, reviewed wrapper
and the meter is advisory only.
