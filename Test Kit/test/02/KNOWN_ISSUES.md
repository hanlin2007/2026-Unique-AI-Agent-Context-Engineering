# Known issues

## #17 - Index tokenizer drops words (OPEN, high priority)

Reported 2026-09-22 by Anika, reproduced on every CI build since
v0.6.0 (the "unified tokenisation" refactor).

Symptom: word counts come out wrong for any note containing hyphenated
compounds, reading times drift with them, and the fixture-level stats
test fails. Plain keyword search still works, which is consistent with
a tokenizer that *silently drops* tokens rather than mis-splitting the
whole stream.

History: before v0.6.0 each module had its own regex and the numbers
were stable for months. The refactor centralised tokenisation in
`src/search.py` (TOKEN_RE / tokenize), and the failures started the
same week. The crash log from the v0.3.x era
(`logs/error_2026_09_25.log`) shows this module has bitten us before.

Current theory (see fix_suggestion.md): TOKEN_RE's character class
excludes hyphens and apostrophes, so tokens containing them never make
it into the stream at all. Two reviewers have read the file and
disagreed on whether this matters for *search*; for *stats* the impact
is now clear.

Suspected location: `src/search.py`, TOKEN_RE + tokenize().

What we have RULED OUT so far: notes.py (loading is a straight
read_text, verified byte-for-byte against the fixtures), cli.py (pure
presentation; the numbers are wrong before formatting), and the
fixtures themselves (regenerated from the corpus on 2026-09-23, counts
still off). That leaves the token stream, and the token stream lives
in search.py since v0.6.0.

Impact: test suite red (3 of 8 tests failing).

## #14 - CLI table wraps on long titles (OPEN, low priority)

Titles over 28 chars are truncated with no ellipsis. Cosmetic.

## #12 - index JSON not stable across runs (OPEN, low priority)

scripts/build_index.py emits dict-ordered JSON; nightly diffs are
noisy. A sort_keys=True would do. Not blocking anything.

## #11 - load_notes crashes on empty directory (CLOSED)

Fixed in v0.5.4 by returning an empty list early.

## #9 - richness divides by zero on empty note (CLOSED)

Fixed in v0.5.1 (guard clause in vocabulary_richness).

## #7 - search token KeyError on cold index (CLOSED)

v0.2.0 era; missing setdefault in build_index. Crash log preserved in
logs/error_2026_09_25.log (second block). This was the FIRST of the
three search.py incidents - the file has history.
