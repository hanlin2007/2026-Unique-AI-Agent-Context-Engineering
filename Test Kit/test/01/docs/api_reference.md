# API reference

v0.5.1. Human-maintained; minor drift possible.

## src.journal
### load_journal(path) -> list[Transaction]
CSV -> date-sorted transactions (stable sort, ISO dates).

## src.normalize
### KIND_MAP: dict
raw journal kind -> canonical kind ("deposit" | "withdrawal").
### normalize(transactions) -> list[JournalEntry]
Signs amounts by canonical kind; checks the input is date-sorted.
JournalEntry = (date, kind, signed_amount).

## src.daily
### apply_entry(balance, signed_amount) -> float
New balance, rounded to 2dp. Raises InsufficientFundsError on overdraft.
### compute_daily_rollups(entries) -> list[(date, float)]
ONE (date, closing) tuple per active day; closing is the balance after
that day's LAST entry. Sorted by date.

## src.aggregate
### month_summary(entries, daily, year, month) -> dict
Keys: opening, closing, total_in, total_out, active_days.
total_out is a positive number. Pure function, no caching.

## src.interest
### accrue_interest(daily, annual_rate=0.0365) -> float
Daily accrual on each day's CLOSING balance, every day including the
last; sum rounded to 2dp at the end.
### effective_annual_rate(annual_rate) -> float
APY display helper.

## src.currency
### convert(amount, src, dst) -> float
USD-pivot conversion, Decimal internally, half-even to dst minor unit.
### round_to_minor(amount: Decimal, currency) -> Decimal
### format_amount(amount, currency) -> str
### convert_many(amounts, src, dst) -> list

## src.rates
RATES_USD (Decimal rates vs USD), SNAPSHOT_DATE.

## src.report
### build_report(journal_path, fx="USD", annual_rate=0.0365) -> dict
Keys: journal, native_currency, months, grand, interest, fx.
