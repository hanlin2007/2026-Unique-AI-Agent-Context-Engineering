# Proposed fix for issue #51 (statement CSV dialect)

Author: n.achterberg, 2026-10-01
Status: PROPOSED, review pending (branch fix/issue-51-csv-dialect)

## Root cause (analysis)

`load_statement()` currently assumes the June-era format: comma
delimiter, no quoting, plain decimal amounts. The bank has changed
its export twice this year, and if the September file has drifted
back toward the OLD convention (quoted amounts, possibly semicolon
delimiters on the EU locale export), then DictReader silently
mis-splits rows: an amount like "1,245.00" becomes TWO fields, every
subsequent column shifts left, and the amount parse either fails or
- worse - succeeds on the WRONG substring. A handful of lines
affected this way explains the sub-percent drift in the matched
total and the wrong-looking unmatched lists.

## Proposed patch

In `src/bank_io.py`, detect the dialect instead of assuming it, and
route amounts through a parser that tolerates quoted thousand
separators:

```python
def load_statement(path: str) -> list:
    with open(path, newline="", encoding="utf-8") as fh:
        sample = fh.read(2048)
        dialect = csv.Sniffer().sniff(sample, delimiters=",;")
        reader = csv.DictReader(fh, dialect=dialect)
        lines = []
        for row in reader:
            lines.append(StatementLine(
                day=_parse_day(row["date"]),
                ref=row["ref"].strip(),
                amount=_parse_amount(row["amount"]),
                description=row.get("description", "").strip(),
            ))
    return lines


def _parse_amount(s: str) -> float:
    s = s.strip().strip('"').replace(",", "")
    return round(float(s), 2)
```

## Why this should turn the suite green

Once the parser stops mis-splitting drifted rows, every statement
line lands in the right columns, the right lines become available
to the matcher, and both the unmatched lists and the totals follow.
The matching core itself is v0.3 code with months of clean
reconciliations - the corruption has to be entering at the IO edge.

## Confidence

High - the bank's export history (#19, plus the June change), the
unreviewed v0.4.0 rewrite, and a symptom signature (small total
drift + wrong lists) that is exactly what dropped/shifted lines
produce.

## Test plan

1. Apply the patch on branch fix/issue-51-csv-dialect.
2. `python -m pytest tests/test_task.py -q` - expect all green.
3. `python scripts/month_end.py` - the policy line must report
   duplicates=0 before finance ops will look at anything else.
4. Hex-dump the first 2 KB of the September statement and attach it
   to the issue so the NEXT format drift is detectable by diff
   rather than by a red suite.

## Out of scope (deliberately)

- The matching core (window / match / report). v0.3 code, months of
  clean reconciliations, and - per the meeting on 2026-10-03 - the
  last place we look. p.delgado's trace observations are noted and
  will be revisited ONLY if the hex dump comes back clean.
- Widening WINDOW_DAYS or touching AMOUNT_TOLERANCE. Both are
  policy, owned by the quarterly review, not by this fix.
