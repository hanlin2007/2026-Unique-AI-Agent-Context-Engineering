# textidx data dictionary

This document is the source of truth for index and ranking
semantics. When a doc and the code disagree, THE DOC WINS - file an
issue. (Process note: this document was WRITTEN as part of the
v0.3.0 cleanup precisely because the team kept rediscovering that
"everyone knows what df means" was not, in fact, true. Quote it in
review; do not paraphrase it.)

## Terms

A term is a maximal run of lowercase letters and digits, length >= 2
after lowercasing. Apostrophes and hyphens are separators: the token
"well-known" indexes as "well" and "known". (Behaviour since v0.1;
changing it is a re-indexing migration, not a tweak.)

## Document frequency (df)

df(term) is the number of DISTINCT documents that contain the term
at least once. A document containing the term five times contributes
1 to df, not 5. df can never exceed the number of indexed documents
- if you ever see a df larger than n_docs in a debug trace, the
index build is broken, full stop.

## Term frequency (tf)

tf(term, doc) is the raw occurrence count of the term in the
document. No length normalisation, no log damping - the doc set is
small and roughly uniform in length, and simplicity wins.

## Ranking

score(doc, query) = sum over query terms of tf(term, doc) *
idf(term), with idf(term) = ln(1 + N / df(term)) and N = number of
documents.

Results are ordered BEST FIRST: highest score first. Ties are broken
by doc_id ascending (alphabetical). A query whose terms are all
unknown returns an empty list. Scores are presented rounded to 3dp
at the api edge.

Worked example ("water", N = 7, df = 3, tf = 4): idf = ln(1 + 7/3)
= 1.204; score = 4 * 1.204 = 4.816. If a trace ever shows this query
returning a sub-1.0 top score, or returning the doc with tf = 2
ahead of the doc with tf = 4, something upstream is miscomputing.

## The fixture folder

data/docs/ holds seven hand-written docs (astronomy, chess, cooking,
gardening, hiking, jazz, python) with deliberately overlapping
vocabulary. "water" is shared by cooking/gardening/hiking, "night"
by astronomy/hiking/jazz, "club" by chess/hiking/jazz - the overlaps
exist so that df and tf can be told apart by the suite: a term
appearing several times in ONE doc must score that doc high without
inflating the term's df. Treat fixture edits as contract changes:
any edit re-verified against this dictionary and the suite in the
same commit.
