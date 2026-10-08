# Proposed fix for issue #71 (requests lost on quoted referrers)

Author: k.vasquez, 2026-10-03
Status: PROPOSED, review pending (branch fix/issue-71-referrer-regex)

## Root cause (analysis)

The referrer and UA groups in LINE_RE are:

```python
r'"(?P<referrer>(?:[^"\\]|\\.)*)" '
r'"(?P<ua>(?:[^"\\]|\\.)*)" '
```

The `(?:[^"\\]|\\.)*` construction handles escaped quotes but is
overly strict about backslashes: a referrer ending in a backslash, or
containing an escape the pattern doesn't expect, fails the WHOLE line
match (the pattern is anchored at both ends). Those lines fall out of
parse_line() as None and the request vanishes from the sample. The
CDN comparison shows exactly this shape: whole hours light by a
roughly constant share, worst where search referrers (query strings,
commas, encoded characters) are common.

## Proposed patch

In `src/parser.py`, relax both quoted groups and drop the brittle
end anchor so trailing junk can't sink a line:

```python
LINE_RE = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<ts>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) [^"]*" '
    r'(?P<status>\d{3}) (?P<bytes>\S+) '
    r'"(?P<referrer>[^"]*)" '
    r'"(?P<ua>[^"]*)" '
    r'(?P<rt>[\d.]+)'
)
```

`[^"]*` accepts everything up to the closing quote, escapes or not,
and the unanchored tail tolerates any trailing whitespace the shipper
adds.

## Why this should turn the suite green

The failing tests assert hourly counts and percentiles; both are
computed on the parsed sample. Once the rejects stop, the sample
matches the CDN's numbers and the hours and percentiles should snap
back to the expected values.

## Confidence

High - same class of bug as #17 and #35. The crash trace in
logs/error_2026_09_30.log shows a parse failure on a referrer line,
and the rejects list in a local run is where the missing requests go.

## Rollback plan

If the patch makes anything worse, revert the branch and re-apply
only the unanchored tail (the smallest hunk). The group relaxation is
independent and can land separately. Either way, rerun the suite and
paste the CDN cross-check line into issue #71 for the record.
