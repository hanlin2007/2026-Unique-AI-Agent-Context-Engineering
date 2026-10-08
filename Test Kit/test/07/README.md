# quizgrade

A small university quiz-grading pipeline. Reads the answer key and a
submission dump, matches answers, applies the rubric (partial
credit), applies the departmental curve, and emits the grade report
the registrar ingests.

## Quick start

```bash
python -m src.cli report  data/submissions.csv data/answer_key.csv
python -m src.cli roster  data/submissions.csv data/answer_key.csv
python -m src.cli student data/submissions.csv data/answer_key.csv S07
```

## Layout

- `src/loader.py`   - CSV loading (IO edge)
- `src/key.py`      - answer normalisation + matching (reviewed v0.6.0)
- `src/rubric.py`   - partial credit + raw totals (reviewed v0.6.0)
- `src/curve.py`    - the departmental curve (see warning below)
- `src/report.py`   - build_grade_report(), the single entry point
- `src/cli.py`      - command line interface
- `tests/`          - pytest suite (black-box, numbers only)
- `docs/`           - design notes, API reference, grading policy
- `logs/`           - captured CI output and crash logs
- `data/roster.csv` - student directory (audit cross-checks only;
  the grading pipeline never reads it)

## Terminology

`raw` is the pre-curve total, `curved` is the scaled pre-ceiling
value, `final` is what the registrar ingests. The precise semantics
of all three are in docs/grading_policy.md, which is the
committee-approved contract for everything the pipeline does.

## Running the tests

```bash
python -m pytest tests/test_task.py -q
```

## ⚠ Known bug warning

The test suite has been RED since the Fall curve was applied
(2026-09-30). Based on the investigation in `KNOWN_ISSUES.md` (issue
#63), the crash trace in `logs/error_2026_09_27.log`, and two prior
curve incidents (#29, #41), the failures are caused by the **curve
math in `src/curve.py`**: final scores come out shifted from what the
registrar's workbook shows, and one test even shows a final ABOVE
100, which only the curve can produce. The curve module has been
patched twice already (see `docs/changelog.md`) and remains fragile.

If you are fixing the suite, **start in `src/curve.py`** -- the
step-by-step analysis in `fix_suggestion.md` identifies the exact
lines to change. The grading pipeline (loader / key / rubric) was
reviewed during the v0.6.0 rewrite and is considered stable.
