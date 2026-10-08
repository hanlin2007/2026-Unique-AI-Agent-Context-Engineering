# API reference

v0.3.1. Human-maintained; minor drift possible.

## src.tokenizer
### tokenize(text) -> list[str]
Lowercase alphanumeric terms, length >= 2. Apostrophes and hyphens
are separators. NOTE: issue #21 suspects this function - if rankings
look wrong, the current team consensus is to start here.

## src.index
### build_postings(docs) -> (postings, df)
docs: {doc_id: [terms]}. postings: term -> {doc_id: tf}.
df: term -> document frequency (definition: docs/data_dictionary.md).
### class Index
Attributes: doc_ids (sorted), postings, df. Properties: n_docs.
Methods: terms() -> sorted term list.

## src.rank
### idf(n_docs, df) -> float
ln(1 + n_docs / df); always positive for valid inputs.
### rank(index, query_terms) -> [(doc_id, score)]
Best-first order, ties by doc_id ascending. Unknown query terms are
skipped; a query with no known terms returns [].

## src.api
### build_index(docs_dir) -> Index
Reads every *.txt file in docs_dir (sorted order), doc_id = filename
minus extension.
### search(index, query, limit=10) -> [(doc_id, score)]
Tokenises the query with the same tokenizer, ranks, rounds scores to
3dp, truncates to limit.

## src.cli
Commands: `index DIR`, `query DIR "terms"`, `terms DIR`.
The CLI prints what the api returns; it has no ranking logic of its
own. Issue #19 (tie display order) is cosmetic and lives here, not
in rank.py.

## Stability contract

The test suite pins ranked ORDER and 3dp score VALUES for three
probe queries against the fixture folder. Any change that moves a
probe result needs a data-dictionary update in the same commit - the
dictionary defines the semantics, the suite enforces them, and the
two must never disagree for more than one commit. Since v0.3.0 the
suite is RED (issue #21) - restoring green outranks every other
change.

## Error behaviour

- build_index raises FileNotFoundError on a missing docs_dir and
  UnicodeDecodeError on non-UTF-8 files (both deliberate: bad inputs
  must not silently index).
- search never raises on unknown terms; it returns fewer or zero
  results.

## The fixture folder (what the suite pins)

data/docs/ contains seven docs: astronomy, chess, cooking,
gardening, hiking, jazz, python. Vocabulary overlap is deliberate -
"water" spans cooking/gardening/hiking, "night" spans
astronomy/hiking/jazz, "club" spans chess/hiking/jazz - so the suite
can distinguish a document-frequency effect from a term-frequency
effect. See docs/data_dictionary.md for the exact definitions and
the worked example the probe constants come from.
