# FULL CLIENT RE 100% — coordinator current-main audit

Date: 2026-08-19  
Source PR: #536  
Source head: `24bdc5b959ff02733ada3967cae8ad1df1465f7d`  
Coordinator review: `4971484054`  
Decision: **ACCEPT_WITH_EDITS**

## Audit scope

The audit independently re-read the source 169-row denominator, matrix/current-refresh contract and the promoted evidence that landed after the source snapshot. No runtime work was performed.

Source ancestry at audit time was stale:

```text
current main: 5d1a09dcb5b3abc22d341951b81d557495d755a6
source merge base: ebbb36f50076ff4072c7218e302614c1dfea00b1
source ahead_by: 14
source behind_by: 28
```

Direct source merge is therefore inappropriate. The historical checklist is retained as a byte-identical denominator snapshot while current status is repaired in a clean promotion from current `main`.

## Accepted source design

The following source properties are accepted without correction:

- exactly 169 stable row IDs across A-H;
- fail-closed `DONE / PARTIAL / NOT_STARTED / BLOCKED` status meanings;
- row counts are not a weighted completion percentage;
- static/QMeta/protobuf/class presence alone is insufficient for `DONE`;
- runtime-sensitive claims require current-build and causal/stability proof at their row boundary;
- the historical detailed checklist is a useful fixed denominator and should not be rewritten merely because newer evidence landed.

## Material findings repaired in clean promotion

### COV-AUD-001 — current-client/login state stale

#555/#561 establish the exact current official Linux fence. #528/#577/#578 prove a causal native login-to-world event on that exact build while separately proving later session-retention failure.

Accepted deltas:

```text
A01 -> DONE
A07 -> DONE
A09 -> DONE
A14 -> DONE
A16 -> PARTIAL
A15 remains BLOCKED
```

The proof-point success and later stability failure are both preserved; neither is allowed to erase the other.

### COV-AUD-002 — current-build RE no longer globally blocked

Current-build packages promoted through #551/#562/#569/#566/#574/#564 and current-SHA native-login helpers establish real exact-current revalidation breadth.

Accepted deltas:

```text
H21 BLOCKED -> PARTIAL
H22 BLOCKED -> PARTIAL
```

Neither row is `DONE`; breadth, restart stability and future-update rediscovery remain incomplete.

### COV-AUD-003 — missing accepted G0 status deltas

Accepted promotions missing from the source current matrix:

```text
F11,F12                     NOT_STARTED -> PARTIAL
D06,D07                     NOT_STARTED -> PARTIAL
D12-D14,D19-D22             NOT_STARTED -> PARTIAL
G01,G04-G06                 NOT_STARTED -> PARTIAL
H07-H14                     NOT_STARTED -> PARTIAL
```

Existing `PARTIAL` rows corroborated by these packages remain `PARTIAL`; no row becomes `DONE` merely because a current-build structural package exists.

### COV-AUD-004 — economy row-ID reconciliation

The economy source used task-local numbering that does not match the canonical 169-row semantic IDs. Mapping must be by canonical row name.

Accepted canonical deltas from promoted static census #547:

```text
G24 Market                              -> PARTIAL
G25 Store / Tibia Coins                 -> PARTIAL
G26 Daily Reward                        -> PARTIAL
G27 Reward Wall / resting               -> PARTIAL
G28 Character Info                      -> PARTIAL
G29 Blessings / premium                 -> PARTIAL
G30 Character auction / trade           -> PARTIAL
G31 World transfer / main-character     remains NOT_STARTED
```

#550 does not change those statuses: its GUI sequence is diagnostic-only and its terminal archive explicitly records `canonical_live_G24_G31_status_delta: NONE`.

### COV-AUD-005 — stale frontier prose

#539/S10 is terminal, not `IN_PROGRESS`. Its accepted result leaves `B04` and `C21` `PARTIAL` and records `BLOCKED_MISSING_RETAINED_CODE_WINDOW` for the unproven action-specific connect/member edge.

#557 is terminal superseded and adds no canonical status delta.

### COV-AUD-006 — compiled-name presence is not semantic G0

The current-build UI/settings scan found dedicated controllers/types for portions of H01-H06/H15-H19, but the producer itself preserved the semantic model/lifecycle edges as unresolved. The coordinator therefore does not advance those rows merely from compiled presence.

## Current projection

After applying only accepted, evidence-backed deltas:

```text
DONE         14
PARTIAL      95
NOT_STARTED  56
BLOCKED       4
TOTAL       169
```

Area totals:

```text
A  5 / 10 /  0 / 1 = 16
B  7 /  4 /  2 / 0 = 13
C  0 / 21 /  0 / 1 = 22
D  0 / 22 /  3 / 0 = 25
E  0 /  3 / 11 / 0 = 14
F  2 / 11 /  0 / 2 = 15
G  0 / 12 / 29 / 0 = 41
H  0 / 12 / 11 / 0 = 23
```

The four current blocked rows are exactly:

```text
A15 restart/relogin semantic stability
C10 authoritative local-player XYZ
F08 server-delivered map extent/control model
F10 worldmap patch causal propagation
```

## Safety and provenance

This audit uses repository evidence only:

```yaml
runtime_access: none
client_executed: false
credential_use: false
login: false
gui_input: false
gameplay: false
transaction: false
process_memory_access: false
runtime_mutation: false
```

No diagnostic observation is upgraded beyond its admitted evidence grade.
