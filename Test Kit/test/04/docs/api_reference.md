# API reference

v0.9.2. Human-maintained; minor drift possible.

## src.ledger
### PEOPLE: tuple
The six travellers, roster order.
### load_expenses(path) -> list[Expense]
CSV -> date-sorted Expenses (stable sort). Expense = (date, payer,
amount, category, split_among, memo). split_among is always a tuple of
people ("all" expands to the full roster).
### parse_row(row) -> Expense
Raises ValueError on unknown payer, bad split_among, non-positive
amount, or payer not in split_among.

## src.split
### split_expense(amount, people) -> dict
Per-person shares summing EXACTLY to amount (largest remainder at cent
granularity; leftover cents to the first members in order).
### split_all(expenses) -> list[dict]
One shares-dict per expense, order preserved.

## src.settle
### simplify(balances) -> list[dict]
Greedy pairing of largest creditor with largest debtor; settles
min(credit, debt) per step; EPSILON=0.005. Transfers are dicts
{"from", "to", "amount"}; the "from" side is the DEBTOR.

## src.fx
### convert(amount, src, dst) -> float
EUR-pivot conversion, Decimal internally, half-even to dst minor unit.
### round_to_minor(amount: Decimal, currency) -> Decimal
### format_amount(amount, currency) -> str
### EXPONENTS: dict
Minor-unit exponents (JPY is 0, the rest 2).

## src.rates
### RATES_PER_EUR: dict[str, Decimal]
Monthly snapshot (SNAPSHOT_DATE). Audit copy: data/fx_snapshot.csv.

## src.report
### build_settlement(path, fx="EUR") -> dict
The single entry point. Keys: path, currency, people, expense_count,
balances, transfers, grand_total_eur, fx.

## src.cli
### main(argv) -> int
Commands: report / balances / transfers.
