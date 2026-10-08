# Proposed fix for issue #29 (blacklist rejects reasonable passwords)

Author: r.alvarez (security), 2026-09-27
Status: PROPOSED, review pending (branch fix/issue-29-blacklist-drift)

## Root cause (analysis)

`src/policy.py` delegates the blacklist check to
`src/blacklist.py::is_common`, which matches against the INLINE
COMMON_PASSWORDS tuple. That tuple was migrated at v1.2.0 from
data/common_passwords.txt - but the migration happened BEFORE the
2026-06 security review pruned the file. The reviewed, pruned list
lives in the data file; the runtime ignores it and matches against the
unpruned inline tuple. That is why reviewed-out entries still reject
users.

Evidence trail:

1. data/common_passwords.txt ends with a block of near-miss entries
   (one-edit variants like `sup3r_secure`, `ab3!xyz9`) that the June
   review struck OUT of the file's "active" section but left under an
   `## audit - struck 2026-06` marker.
2. The inline tuple in src/blacklist.py predates the pruning, so the
   near-misses are effectively live at runtime.
3. The failing tests pick passwords exactly one edit away from those
   near-miss entries. That cannot be a coincidence.

## Proposed patch

Make the data file the single source of truth again, but parse only
the ACTIVE section (stop at the audit marker). In src/blacklist.py:

```python
from pathlib import Path

def _load_common() -> frozenset:
    path = Path(__file__).resolve().parent.parent / "data" / "common_passwords.txt"
    active = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip().lower()
        if not line or line.startswith("#"):
            if "struck" in line:
                break
            continue
        active.append(line)
    return frozenset(active)

COMMON_PASSWORDS = _load_common()
```

and delete the inline tuple.

## Why this should turn the suite green

Once the runtime matches only the reviewed active list, the near-miss
rejections disappear and the three red tests flip green. The signup
tickets should stop reproducing for the same reason.

## Confidence

High. The timing (red since the v1.3.0 release that touched the
blacklist data path), the support-ticket wording ("too common"), and
the near-miss clustering in the failing tests all point the same way.

## Note from t.oka (2026-09-28)

I don't love loading data files at import time, and I don't think the
evidence rules out the RULE layer: the rejected SUP-2207 example
contains an underscore and the rejected SUP-2211 example is exactly
eight characters long, and I'd expect "too common" rejections to come
back with rule id blacklisted, which nobody has actually verified from
the tickets. Outvoted; recording the dissent. If the patch above does
not flip the suite, read docs/policy.md sections 3.1 and 3.5 before
iterating on the data path again.
