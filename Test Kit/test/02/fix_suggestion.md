# Proposed fix for issue #17 (index tokenizer drops words)

Author: Tom, 2026-09-26
Status: PROPOSED, review pending (branch fix/issue-17-tokenizer)

## Root cause (analysis)

`src/search.py` defines the token stream everything else consumes:

```python
TOKEN_RE = re.compile(r"[A-Za-z0-9]+")

def tokenize(text: str) -> list:
    return [t.lower() for t in TOKEN_RE.findall(text)]
```

The character class `[A-Za-z0-9]` excludes `-` and `'`, so a word like
"well-known" is split and -- worse for counting -- the tokenizer is the
single source of truth for what counts as a token since the v0.6.0
"unified tokenisation" refactor. Any consumer that counts tokens now
under/over-counts depending on how many compounds the text contains.
That is exactly the failure signature in the suite: hyphen-heavy notes
are off, plain notes are fine.

## Proposed patch

In `src/search.py`:

```python
TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)?")
```

i.e. allow ONE internal hyphen per token. Rationale: keeps "state of
the art" style multi-hyphen compounds from exploding the index while
capturing the common single-hyphen case ("well-known", "follow-up").

Also update `build_index` to keep tokens in first-seen order instead of
sorting, so the index reflects reading order -- the stats consumers
were written against pre-v0.6.0 behaviour where order was preserved.

## Why this should turn the suite green

Once the tokenizer stops dropping the hyphenated tail of compounds,
token counts line up with the fixture expectations again, and reading
time (derived from the counts) follows.

## Confidence

High. The timeline fits (failures began with the v0.6.0 tokenisation
refactor), the old crash log points into this file, and the failing
tests are precisely the ones whose fixtures contain hyphens.

## Alternatives considered

1. Revert v0.6.0 wholesale. Rejected: the refactor also fixed the
   duplicate-token index bloat, and a revert would reopen issue #13.
2. Add a second, stats-specific regex in search.py and export both.
   Rejected as over-engineering: one tokenizer, one source of truth was
   the whole point of v0.6.0.
3. Treat hyphens as token separators but count the pieces with a
   weight. Rejected: non-integer word counts would leak into the CLI
   and confuse everyone.

## Rollout plan

Apply the TOKEN_RE patch on the branch, run the suite, then run
scripts/build_index.py against the full corpus and diff the token
counts against the 2026-09-21 baseline. Expect a small UPWARD drift in
unique tokens (compounds now indexed whole). If the drift exceeds 2%,
revisit alternative 2 before merging.

## Note from Anika (2026-09-27)

I still think "one optional hyphen" is arbitrary and `tokenize` was
never meant to define what a WORD is for stats purposes -- the style
guide (docs/style_guide.md) defines words, and stats should follow
that, not the search index. Outvoted in review; recording the dissent
here. If this patch does not turn the suite green, please re-read the
style guide before iterating on TOKEN_RE again.
