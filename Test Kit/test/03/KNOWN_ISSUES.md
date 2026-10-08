# Known issues

## #29 - Blacklist rejects reasonable passwords (OPEN, high priority)

Reported 2026-09-18 by support (ticket cluster SUP-2201..SUP-2217),
test suite red since v1.3.0 (2026-09-20).

Symptom: signup rejects passwords that look nothing like dictionary
words. Example from SUP-2207: `Sup3r_secure` is refused; example from
SUP-2211: an 8-character mixed password refused. Support quotes users
saying "the site says my password is too common".

History: the blacklist began life as data/common_passwords.txt with
37 classic entries. Over two years it absorbed appends from three
sources: the 2024 rockyou refresh, a pen-test dump, and ad-hoc support
requests ("please block variations of our company name"). Review
discipline slipped; the file visibly contains near-miss junk (see the
last dozen lines of data/common_passwords.txt).

Complication: at v1.2.0 the list was migrated INLINE into
src/blacklist.py (COMMON_PASSWORDS) and the data file was kept "for
audit". The two may have drifted. The current theory (see
fix_suggestion.md) is that the runtime is matching against the stale
audit file rather than the reviewed inline list, OR that the inline
migration carried the junk across. Either way, the fix is in
blacklist.py's data path.

Suspected location: `src/blacklist.py`, COMMON_PASSWORDS + is_common().

Impact: test suite red (3 of 9 tests failing); signup abandonment
uptick flagged by growth team on 2026-09-25.

## #26 - meter label boundary confusing (OPEN, low priority)

A 69-point password says "fair", a 70-point one says "strong"; support
wants hysteresis. Parked until #29 lands.

## #21 - audit subcommand exits 0 on failures (CLOSED)

Fixed in v1.2.3: audit now exits 1 when any candidate fails.

## #15 - UnicodeDecodeError reading legacy lists (CLOSED)

v1.1.0 era, crash log preserved at logs/error_2026_08_30.log. The
loader assumed ASCII on a latin-1 dump. Moot since the inline
migration, kept for reference.
