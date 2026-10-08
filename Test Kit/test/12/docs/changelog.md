# Changelog

## 0.4.1 (2026-09-20)
- data: August ledger archive moved into data/ (issue #31)
- docs: add reconciliation policy + data dictionary

## 0.4.0 (2026-09-19) - "bank format" release
- bank_io: rewrite statement parsing for the bank's June export
  format (plain CSV, no quoted amounts); the old quoted-amount
  workaround removed (issue #19)
- report: build_recon_report() is now the single entry point; tests
  moved to a black-box contract (numbers and id lists)
- Post-release, the test suite went red - tracked as issue #51
  (statement CSV dialect drift, see KNOWN_ISSUES.md).

## 0.3.2 (2026-08-19)
- scripts: month_end archive carries SHA-256 of both input files
  (issue #26)

## 0.3.1 (2026-08-04)
- match: report the duplicate-consumption count in the report
  (auditor request; always zero in healthy runs)

## 0.3.0 (2026-07-02) - "matching rules" release
- window: value-date window written down (2 days, inclusive end)
  after the May long-weekend settlement confusion
- match: single-use rule formalised - identical-amount entries can
  no longer share one settlement line
- ledger_io: fee accruals (kind F) excluded from reconciliation
- Suite green continuously from this release until v0.4.0.

## 0.2.0 (2026-04-10)
- report: totals added (matched / unmatched both sides)

## 0.1.0 (2026-02-16)
- initial release
