# Journal data dictionary

The journal CSV (e.g. data/journal_main.csv) has columns
`date,kind,amount,memo`. Amounts are always positive; the DIRECTION of
each kind is fixed by convention and implemented in
`src/normalize.py` (KIND_MAP). These two must always agree.

| kind       | direction | meaning                                   |
|------------|-----------|-------------------------------------------|
| deposit    | IN        | salary, transfers in, one-off income      |
| withdrawal | OUT       | card purchases, cash, ad-hoc spending     |
| payment    | OUT       | scheduled bill payments (subscriptions)   |
| refund     | IN        | money returned TO the account             |
| interest   | IN        | interest credited by the bank             |
| fee        | OUT       | account maintenance fees charged monthly  |

Notes:

- "payment" vs "withdrawal" is about scheduling, not direction; both
  are money out.
- "interest" (a journal kind) is what the bank actually CREDITED. It is
  unrelated to the theoretical accrual computed by src/interest.py,
  which derives interest from daily balances and never reads journal
  rows.
- "fee" rows appear once a month (account maintenance). They are small
  and easy to overlook in totals, but they are real outflows.
