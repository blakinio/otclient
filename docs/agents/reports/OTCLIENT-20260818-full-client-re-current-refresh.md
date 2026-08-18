# OTCLIENT-TIBIA-RE — FULL CLIENT RE current refresh

```yaml
refreshed_at: 2026-08-18T16:08:00+02:00
repository: blakinio/otclient
track: official-client-re
snapshot_main: ebbb36f50076ff4072c7218e302614c1dfea00b1
source_checklist: docs/agents/reports/OTCLIENT-20260818-full-client-re-100-percent-checklist.md
source_matrix: docs/agents/reports/OTCLIENT-20260818-full-client-re-matrix.md
pr: 536
status_rows_total: 169
done: 10
partial: 65
not_started: 86
blocked: 8
```

## Purpose

This is the current-state overlay for the canonical 169-row checklist and matrix. It records only material evidence that appeared after the original matrix snapshot. It does not rewrite historical evidence and does not promote an in-flight producer result as canonical.

## Material refresh facts

### Current official Linux package fingerprint — PR #528

The obsolete researched build remains:

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
live disposition: rejected as too old
```

PR #528 now also retains a read-only current-official package probe:

```text
run/job: 32140385842 / 95721374178
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
unpacked_size: 52109920
```

This is meaningful current-package identity evidence, so checklist row `A01` is no longer a pure `BLOCKED` absence. It is now `PARTIAL`: the current upstream package fingerprint is known, while the canonical on-disk source-package `bin/client` identity is still explicitly `UNKNOWN` and must be re-inventoried before updater mutation or current-build RE.

No credential/login claim follows from this probe. `CHARACTER_ACTUALLY_LOGGED_INTO_GAME=NO` remains unchanged.

### S10 action-to-protocol retained code-window harvest — PR #539

A new bounded static lane is active:

```text
PR: #539
Task: OTC-20260818-track-a-s10-action-protocol-code-window-harvest
State: IN_PROGRESS / ready
Primary target:
  TContainerGameActionHandler / TGenericGameActionHandler
   -> sendMoveObject
   -> exact protocol owner
   -> exact message producer
```

S10 uses retained exact-SHA repository evidence only and does not acquire or run a client. It may improve `B04` and `C21` if it recovers direct code/dataflow/connect evidence, but no such edge is promoted yet. Therefore those rows remain `PARTIAL`.

### Current main and coverage PR

```text
main: ebbb36f50076ff4072c7218e302614c1dfea00b1
main change since matrix snapshot: none
PR #536 state: open / Draft / mergeable
independent submitted reviews: 0
```

The required fresh independent documentation audit is still unavailable in this worker session, so PR #536 remains Draft.

## Status delta

| Row | Previous | Current | Reason |
|---|---|---|---|
| `A01` Current official Linux client identity/version fence | `BLOCKED` | `PARTIAL` | current upstream packed/unpacked fingerprint and unpacked size are now retained by #528; canonical on-disk source-package identity and full current-build revalidation remain open |

No other row changes status in this refresh.

Updated totals:

```text
DONE         10
PARTIAL      65
NOT_STARTED  86
BLOCKED       8
TOTAL       169
```

## Immediate programme frontier

```text
1. #528: read-only inventory canonical source-package bin/client and reconcile it with the current official manifest/fingerprint.
2. #528: after exact current package identity is proven, re-prove native auth/character-login contracts for that exact SHA before another login attempt.
3. #539: harvest direct retained sendMoveObject action -> protocol -> producer code/dataflow evidence; fail closed if the retained window is absent.
4. #475/#302 remain blocked from their semantic goals until their own legal runtime/evidence gates are satisfied.
5. #536 remains Draft until a fresh independent documentation audit returns zero material findings.
```
