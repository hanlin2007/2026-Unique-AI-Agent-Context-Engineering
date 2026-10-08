# Changelog

## 0.6.2 (2026-09-21)
- docs: add style guide defining word tokenisation and reading time
- notes: title falls back to file stem when no H1 is present

## 0.6.0 (2026-09-15) - "unified tokenisation" release
- search: tokenize() centralised as THE token stream for the project;
  per-module regexes removed as part of the cleanup
- search: build_index now deduplicates tokens per note
- After this release the stats tests went red - tracked as issue #17
  (index tokenizer drops words, see KNOWN_ISSUES.md). The search
  module is the prime suspect and is under active investigation.

## 0.5.4 (2026-08-30)
- notes: load_notes returns [] on empty directory instead of crashing

## 0.5.1 (2026-08-02)
- stats: vocabulary_richness returns 0.0 on empty text (issue #9)

## 0.5.0 (2026-07-20)
- stats: add unique_words / vocabulary_richness
- cli: add `index` command

## 0.4.0 (2026-05-11)
- search: AND semantics for multi-token queries (was OR)

## 0.3.2 (2026-03-18)
- cli: align stats table columns; truncate titles at 28 chars
  (introduced the cosmetic truncation tracked as issue #14)

## 0.3.1 (2026-03-02)
- search: fix IndexError in build_index on notes with no tokens
  (crash log preserved at logs/error_2026_09_25.log for reference)

## 0.3.0 (2026-02-14)
- search: rewrite build_index around token sets per note
- scripts: build_index.py gains a corpus-size summary line

## 0.2.0 (2026-01-19)
- initial public release: stats + search over a folder of .md notes

## 0.1.3 (2025-12-08)
- notes: tolerate CRLF line endings in titles

## 0.1.2 (2025-11-21)
- stats: reading_time_minutes documented as rounding UP (was implicit)
- stats: reject negative word counts with ValueError

## 0.1.1 (2025-11-02)
- search: OR semantics for multi-token queries (later changed to AND
  in 0.4.0; see that entry for rationale)

## 0.1.0 (2025-10-12)
- internal prototype: word_count + a 20-line search over stdin
