# textidx design notes

Last updated: 2026-09-15 (v0.3.0 era). Maintainer: Mei Lin.
Audience: anyone touching src/. Read the invariants BEFORE the code;
the code assumes you have. Corrections via merge request, please.

## Goals

textidx answers "which of my notes talks about X" over a folder of
small plain-text docs. It is deliberately simple: one folder, one
index in memory, one ranking formula. The design favours
*predictability*: the same folder must always produce the same
ranking, down to the tie-breaks.

## The pipeline

```
tokenizer.py  raw text -> terms (lowercase alphanumeric, len >= 2)
index.py      postings (term -> {doc: tf}) + df per term
rank.py       tf-idf scoring, idf = ln(1 + N/df), sorted output
api.py        folder IO + rounding edge (3dp); the public surface
```

The library does no stemming and no stopword removal. With seven to
a few hundred small docs, both cost more relevance than they buy.

## Invariants

1. doc_id is the filename minus ".txt"; files are processed in sorted
   filename order, so index construction is deterministic.
2. Document frequency is defined in docs/data_dictionary.md and the
   ranking depends on it - read that definition before touching
   index.py. The df cleanup at v0.3.0 was specifically about getting
   this definition written down and REVIEWED.
3. Ranking order (best first, ties by doc_id ascending) is part of
   the public contract; the test suite pins it.
4. Scores are rounded to 3dp at the api edge, never inside rank.py.
5. The tokenizer's treatment of apostrophes/hyphens as separators is
   historical and intentional (v0.1); changing it re-indexes the
   world, so it needs a migration plan, not a drive-by regex edit.
   (Yes, issue #21 disagrees with this paragraph. The paragraph was
   here first.)

## Ranking alternatives considered (and rejected)

BM25 was prototyped in a spike (2026-07) and abandoned: with seven
to a few hundred short docs, the length-normalisation term buys
nothing measurable and the two extra magic constants (k1, b) made
every ranking review an argument about someone else's defaults.
Cosine-normalised tf-idf was rejected for the same reason - the doc
lengths here are uniform enough that the normaliser is noise. Plain
tf-idf with a smoothed idf won on the only criterion that matters
for a notes archive: nobody has ever complained that the top result
was the wrong doc, only that it was missing.

## What would make us revisit this design

- The archive growing past ~5k docs (memory is fine, startup time is
  not - the index would need persistence).
- Multi-folder search (doc_id collisions need namespacing).
- Phrase queries (postings would need positions, a real schema
  change).
None of these are scheduled.

## Operational notes

The nightly-reindex job (scripts/reindex.py) exists because the notes
archive is edited by humans on laptops, not by a pipeline: files
appear, disappear, and occasionally arrive as .txt~ editor backups
(see issue #14). The job rebuilds from scratch every night - at this
scale, incremental indexing would be complexity for its own sake.
Probe queries in the job output are the team's early-warning system:
the docs team knows roughly what "water" or "night sky" should top
with, and a probe that looks wrong gets an issue filed before users
notice. That is exactly how #21 was reported.
