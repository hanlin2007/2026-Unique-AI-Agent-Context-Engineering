# Rollout plan - passpolicy v1.3.x

Owner: platform-security. Last updated 2026-09-21.

## Consumers

| consumer            | integration          | rollout gate        |
|---------------------|----------------------|---------------------|
| signup-service      | REST shim (py-sdk)   | suite green         |
| admin-console       | direct import        | suite green + sec rev|
| credential-audit    | CLI (audit subcmd)   | quarterly           |

## Current status (2026-09-21)

- v1.3.0 shipped 2026-09-20: blacklist data-path refresh (part of the
  #29 investigation), meter labels unchanged.
- Test suite went RED immediately after v1.3.0 - 3 of 9 failing. The
  failures are tracked as issue #29 and are believed to be the same
  underlying blacklist drift the release was supposed to fix (i.e. the
  release fixed the wrong half of the data path).
- signup-service remains on v1.2.3-pinned SDK until the suite is green
  again. admin-console follows the same pin. credential-audit is
  unaffected (it runs with --no-blacklist for historical comparisons).

## Blockers

1. issue #29 (see KNOWN_ISSUES.md). fix_suggestion.md has the proposed
   patch; r.alvarez owns, t.oka reviews.
2. Growth-team escalation on signup abandonment. Not a code blocker,
   but it decides whether we hotfix or roll forward.

## Rollback plan

If the #29 patch misbehaves in staging, revert to the v1.2.3 tag and
re-pin consumers. The v1.2.3 tag uses the pre-migration data-file
loader, which is why logs/error_2026_08_30.log (the v1.1.0-era crash)
was re-reviewed during planning: any return to file-loading must keep
the explicit encoding= parameter.
