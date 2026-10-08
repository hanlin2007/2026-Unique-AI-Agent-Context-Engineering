# API reference

v0.6.2. Human-maintained; minor drift possible.

## src.notes
### load_note(path) -> Note
Load one .md file. Note = (path, title, text); title is the first H1,
else the file stem with underscores replaced by spaces.
### load_notes(directory) -> list[Note]
All *.md files directly under `directory`, sorted by filename.

## src.stats
### WPM: int = 200
Words-per-minute assumption for reading time. Chosen from the average
adult silent-reading rate for non-technical prose; do not tune per note.
### word_count(text) -> int
Word count under the style-guide token rules (hyphenated compounds and
apostrophes count as one word). Numbers count as words.
### reading_time_minutes(words) -> int
Whole minutes at WPM, rounded UP. Raises ValueError on negative input.
reading_time_minutes(0) == 0 by definition (no ceiling of zero).
### unique_words(text) -> int
Distinct words, case-insensitive. Same token rules as word_count.
### vocabulary_richness(text) -> float
unique / total, 3dp; 0.0 on empty text. Intentionally naive: no
lemmatisation, so "run" and "runs" are two words.

## src.search
### tokenize(text) -> list[str]
Lowercased ALPHANUMERIC tokens for indexing (search-only semantics;
see docs/style_guide.md for why this differs from word tokenisation).
### build_index(notes) -> dict
token -> sorted list of note titles. Tokens are deduplicated per note,
so a title appears at most once per token.
### search(index, query) -> list[str]
Titles containing EVERY query token (AND semantics), sorted. An empty
query (or one with no alphanumeric characters) returns [].

## src.cli
### main(argv) -> int
Commands: stats / search / index. Exit code 2 on usage errors. The
stats table truncates titles at 28 chars (known cosmetic issue #14).
