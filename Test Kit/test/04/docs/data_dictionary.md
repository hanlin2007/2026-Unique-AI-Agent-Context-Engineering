# Expense data dictionary

The expense CSV (e.g. data/expenses.csv) has columns
`date,payer,amount,category,split_among,memo`. This document is the
CONTRACT for what the derived numbers mean; src/split.py, src/settle.py
and src/report.py must agree with it. When code and prose disagree,
the prose wins.

## Columns

| column      | meaning                                                     |
|-------------|-------------------------------------------------------------|
| date        | ISO calendar date of the expense                            |
| payer       | who fronted the money (one of the six travellers)           |
| amount      | EUR, positive, cents precision                              |
| category    | free-form bucket (hotel, dinner, train, ...)                |
| split_among | "all", or pipe-separated subset, e.g. "anna|ben|carla"      |
| memo        | free text                                                   |

The payer must be a member of split_among (you cannot front money for
a group you are not part of, in this ledger's world).

## Shares

Each expense is divided among its split_among members. The shares MUST
sum to the expense amount EXACTLY, cent for cent - conservation is the
whole point of a settlement tool. Because most amounts do not divide
evenly, leftover cents are distributed ONE each to the first members
in split_among order (largest-remainder at cent granularity).

Example: 23.30 among anna|ben|carla -> anna 7.77, ben 7.77,
carla 7.76. Sum: 23.30. Never 23.29, never 23.31.

## Balances

A person's NET balance is (everything they PAID) minus (everything
they OWE as shares), computed over ALL expenses in the ledger. Positive
means the group owes them; negative means they owe the group. Over any
complete ledger the balances sum to zero.

## Transfers

The settlement is a list of transfers that zeroes every balance. A
transfer {"from": A, "to": B, "amount": x} means **A PAYS B** x EUR.
The "from" side is always a DEBTOR (negative balance); the "to" side
is always a CREDITOR (positive balance). If a report ever shows a
transfer whose "from" side has a positive balance, the transfer list
is backwards, not "an alternative convention".

## Grand total and fx appendix

grand_total_eur is the sum of ALL per-person shares across ALL
expenses; by conservation it equals the sum of expense amounts to the
cent. The fx appendix converts that single figure for display; it is
never an input to any balance.
