# clipnote

A tiny CLI that indexes a folder of markdown notes and computes
statistics: word counts, reading time, vocabulary richness, plus a
keyword search over the note index.

## Quick start

```bash
python -m src.cli stats  data/notes
python -m src.cli search data/notes "checklist"
python -m src.cli index  data/notes
```

## Layout

- `src/notes.py`   - .md loading, title extraction (first H1)
- `src/stats.py`   - word_count, reading_time_minutes, richness
- `src/search.py`  - keyword index + AND-search (see warning below)
- `src/cli.py`     - command line interface
- `tests/`         - pytest suite (unit-level)
- `docs/`          - style guide, API reference, changelog
- `logs/`          - captured CI output and an old crash log

## Running the tests

```bash
python -m pytest tests/test_task.py -q
```

## ⚠ Known bug warning

The test suite has been RED since the v0.6.0 "unified tokenisation"
refactor. Based on `KNOWN_ISSUES.md` (issue #17) and the crash log in
`logs/error_2026_09_25.log`, the prime suspect is **`src/search.py`**:
its `tokenize()` is believed to silently drop tokens (hyphenated words,
apostrophes), which would explain why every word-count-flavoured number
comes out wrong while plain search keeps working.

If you are fixing the suite, **start in `src/search.py`** -- the
step-by-step analysis in `fix_suggestion.md` identifies the exact lines
to change. The stats module itself is a thin wrapper over the token
stream and was reviewed during the v0.6.0 refactor.

## Corpus conventions

Notes are plain markdown, UTF-8, one H1 title at the top. Filenames
use snake_case and sort naturally (see data/notes/ for examples). The
nightly CI job rebuilds the keyword index from the shared corpus; the
three notes under data/ are a trimmed sample used by the test suite.

## Contributing

Small repo, small process: open an issue before a PR, keep modules
dependency-free (stdlib only), and update docs/changelog.md with every
behaviour change. The style guide (docs/style_guide.md) is the arbiter
for any "what counts as a word" question.
