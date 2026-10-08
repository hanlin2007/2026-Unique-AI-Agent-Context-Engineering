# textidx

A miniature search engine for a folder of small text docs. Builds an
in-memory inverted index and answers keyword queries with tf-idf
ranked results. Used by the docs team to search their notes archive.

## Quick start

```bash
python -m src.cli index  data/docs
python -m src.cli query  data/docs "night sky"
python -m src.cli terms  data/docs
```

## Layout

- `src/tokenizer.py`  - raw text -> terms (see warning below)
- `src/index.py`      - inverted index (postings + df)
- `src/rank.py`       - tf-idf scoring and sort
- `src/api.py`        - build_index() + search(), the public surface
- `src/cli.py`        - command line interface
- `tests/`            - pytest suite (mid-level, order + values)
- `docs/`             - design notes, API reference, data dictionary
- `logs/`             - captured CI output and crash logs

## How it works

One folder of `.txt` files in, ranked results out. At startup the
folder is tokenised into an in-memory inverted index; a query is
tokenised with the same rules, scored with plain tf-idf, and sorted
best-first. There is no server, no database, and no persistence -
the index for this repo's seven-doc fixture builds in milliseconds.

The semantics that matter (what counts as a term, what df means, how
ties break) live in `docs/data_dictionary.md` and the suite pins
them against the fixture folder.

## Running the tests

```bash
python -m pytest tests/test_task.py -q
```

## ⚠ Known bug warning

The test suite has been RED since the v0.3.0 release. Based on the
investigation in `KNOWN_ISSUES.md` (issue #21), the crash trace in
`logs/error_2026_09_20.log`, and the smart-quote incident from v0.2,
the failures are caused by **the tokenisation rules in
`src/tokenizer.py`**: terms containing apostrophes or hyphens are
split apart, so half of every real query term never reaches the
index and the rankings come out wrong. The tokenizer regex has been
a known sore spot since v0.1 (see `docs/changelog.md`).

If you are fixing the suite, **start in `src/tokenizer.py`** -- the
step-by-step analysis in `fix_suggestion.md` identifies the exact
regex change to make. The index and ranking modules were reviewed
during the v0.3.0 df-definition cleanup and are considered stable.

Version: 0.3.1. Python >= 3.9, standard library only. The fixture
folder under `data/docs/` is hand-written and part of the test
contract - do not edit it to make numbers move; edit the code or
bring a data-dictionary change to the team. History and rejected
alternatives are in `docs/design.md`.
