# clipnote style guide

How we count things. This document is the CONTRACT for src/stats.py;
when code and prose disagree, the prose wins and the code is wrong.

## Words

A WORD is a maximal run of letters and digits that may contain
INTERNAL hyphens or apostrophes. Examples:

| text                  | words | tokens                                  |
|-----------------------|-------|-----------------------------------------|
| well-known            | 1     | well-known                              |
| state-of-the-art      | 1     | state-of-the-art                        |
| it's                  | 1     | it's                                    |
| don't-miss            | 1     | don't-miss                              |
| red-eye, re-filled    | 2     | red-eye / re-filled                     |
| 2026-09-14            | 1     | 2026-09-14                              |

A hyphen or apostrophe only glues when it sits BETWEEN two
letters/digits: "-hello" counts as "hello", and "hello-" counts as
"hello".

## Reading time

Reading time is reported in whole minutes at 200 words per minute and
ALWAYS rounded UP. 250 words -> 2 minutes. 400 words -> 2 minutes.
401 words -> 3 minutes. Zero words -> zero minutes.

Rationale: the CLI shows reading time to users deciding whether to
open a note; "1 minute" for 250 words systematically under-promises.

## Vocabulary richness

unique words / total words, case-insensitive, rounded to 3 decimals.
Empty text is defined as 0.0 (no division by zero).

## Search tokenisation is NOT word tokenisation

src/search.py uses a coarser, alphanumeric-only tokenisation for
indexing. That is deliberate: searching "known" should find a note
that only contains "well-known". The search token stream must never be
used to COUNT words. (This distinction was muddied once, in the v0.6.0
refactor discussion; the modules remain separate by design.)

## FAQ

**Why does the search index disagree with the word count for the same
note?** They answer different questions. The index optimises recall
("find the note"), the counter optimises fidelity ("how long is this
note"). See the section above.

**Does a markdown heading marker ("#") count as a word?** No. Only
the alphanumeric runs count; the hash is punctuation and is skipped.

**Does a bullet marker ("-") start a hyphenated word?** No. A leading
hyphen at the start of a line is a list marker; the word after it is
counted on its own.

**Are numbers words?** Yes. "2026" and "50" each count as one word,
and "2026-09-14" counts as one word under the internal-hyphen rule.
