# Proposed fix for issue #21 (tokenizer splits terms)

Author: a.novak, 2026-09-30
Status: PROPOSED, review pending (branch fix/issue-21-tokenizer-regex)

## Root cause (analysis)

`tokenize()` currently does:

```python
TERM_RE = re.compile(r"[a-z0-9]+")
return [t for t in TERM_RE.findall(text.lower()) if len(t) >= 2]
```

The problem: the character class excludes apostrophes and hyphens, so
"well-known" becomes ["well", "known"] and "don't" becomes ["don"]
(after the length filter eats "t"). The index therefore contains the
FRAGMENTS, not the terms users actually type. A query for a hyphenated
term is split the same way at query time, so it matches every doc that
mentions either fragment - the ranking fills up with noise docs and
the real matches sink. This explains both the wrong ORDER and the
wrong SCORES in the failing tests.

## Proposed patch

In `src/tokenizer.py`, keep intra-word apostrophes and hyphens as
part of the term:

```python
TERM_RE = re.compile(r"[a-z0-9]+(?:['-][a-z0-9]+)*")
```

and drop the length filter to >= 1 so short but legitimate terms
survive.

## Why this should turn the suite green

Once queries and docs tokenise identically on hyphenated terms, the
index stops accumulating fragment noise, the right docs float to the
top, and the score values settle. Both failing assertions (order and
values) share this one root cause, because everything downstream of
the tokenizer is just arithmetic on whatever terms it emitted.

## Confidence

High - the tokenizer is the only stage that has never been reviewed,
it has a crash prior (#6), and the failure signature (everything
wrong at once) matches a corrupted term stream far better than it
matches a scoring bug. The index/rank split was reviewed at v0.3.0.

## Test plan

1. Apply the patch on branch fix/issue-21-tokenizer-regex.
2. Rebuild the fixture index (`python scripts/reindex.py`) so the
   archive docs are indexed under the NEW rule, not the old one.
   Skipping this step is why patch v1 stayed red on build #414 - the
   tests compare against constants that assume a consistent rule end
   to end.
3. `python -m pytest tests/test_task.py -q` - expect all green.
4. Eyeball the probe queries in the reindex output against the docs
   team's expectations (water should top with the cooking notes).

## Out of scope (deliberately)

- Stemming and stopwords. Both were rejected at design time (see
  docs/design.md) and neither is needed to close #21.
- Regenerating the expected constants in the suite. The constants
  are the contract; the code is what drifted.

## Review notes (for s.petrov)

- The regex change touches exactly one line; everything else in the
  module is untouched, so a line-by-line review is a five-minute job.
- s.petrov's trace observations from the kickoff (df printing larger
  than the doc count, ascending result lists) are, I believe,
  artefacts of the SAME root cause: fragment inflation makes every
  computed number look structurally impossible. Happy to walk through
  the trace together before the review call if that helps.
- If this patch v2 also stays red, I will stop arguing and join the
  bisect - but the re-indexing step in the test plan above is new
  since v1, and it is the piece v1 was missing.
