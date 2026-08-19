# OTCLIENT-TIBIA-RE — FULL CLIENT RE current refresh

```yaml
refreshed_date: 2026-08-19
repository: blakinio/otclient
track: official-client-re
snapshot_main: 5d1a09dcb5b3abc22d341951b81d557495d755a6
source_checklist: docs/agents/reports/OTCLIENT-20260818-full-client-re-100-percent-checklist.md
source_matrix: docs/agents/reports/OTCLIENT-20260818-full-client-re-matrix.md
source_pr: 536
coordinator_review: 4971484054
status_rows_total: 169
done: 14
partial: 95
not_started: 56
blocked: 4
```

## Purpose

This file is the authoritative current-state overlay for the historical 169-row denominator in `OTCLIENT-20260818-full-client-re-100-percent-checklist.md`.

The base checklist intentionally preserves its 2026-08-18 snapshot and row wording. **Current status must be read from this overlay together with `OTCLIENT-20260818-full-client-re-matrix.md`.** This refresh promotes only independently accepted evidence already present on trusted `main`; it does not infer completion from class names, QMeta presence, GUI diagnostics, or an in-flight Draft.

## Current exact official client fence

Merged #555 plus lifecycle #561 establish the current official native-Linux identity:

```text
version token    15.32
packed size      10214529
packed SHA-256   1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
client size      52109920
client SHA-256   ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
ELF Build ID     d803d9695868713ef6ab0c3cf65f91212c9c6a62
```

The previous `15.32.df7b29 / 51965216 / e6c244bd...` corpus remains historical build-fenced evidence only.

## Current native-login result

Merged clean promotion #577 and lifecycle #578 preserve both halves of the physical result:

```text
RESULT=SUCCESS_AT_PROOF_POINT
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=YES
CAUSAL_PROOF=COMPLETE
STRUCTURAL_IN_GAME_AT_PROOF_POINT=PASS_3_OF_3

CURRENTLY_LOGGED_IN_AT_TERMINAL_GOVERNED_STATE=NO
POST_HANDOFF_SESSION_STABILITY=FAIL_NOT_RETAINED
SECOND_SECRET_ATTEMPT=NOT_PERFORMED
```

This is enough to close the narrow current-build identity/cold-auth/session-reuse/causal-IN_GAME rows whose remaining gate was current-build proof, but it does not make restart/relogin stability successful.

## Status deltas from the historical 2026-08-18 checklist

| Row(s) | Historical | Current | Accepted evidence / boundary |
|---|---|---|---|
| `A01` current official Linux identity/version fence | `BLOCKED` | `DONE` | #555/#561 exact current public-package identity and synchronized Track A fence |
| `A07` native cold-auth entry below form UI | `PARTIAL` | `DONE` | #556 current-build QMeta reproof + #528/#577 causal bounded native-auth success; process handoff is a separate stability issue |
| `A09` retained auth/play-session reuse | `PARTIAL` | `DONE` | #528 exact-current restart without credentials restored the authenticated play session and reached the world; expiry/refresh breadth is outside this narrow row |
| `A14` causal structural `IN_GAME` | `BLOCKED` | `DONE` | #528/#577 visible world proof plus exactly-one `TPlayerProtocolMessageHandler`, `TGameserverGameSession`, and `TWorldmapProtocolMessageHandler` on the same exact process |
| `A16` stable form-less bridge across client update | `BLOCKED` | `PARTIAL` | current-SHA helper/gate set was rebuilt, audited and used on the new exact client; general restart/future-update stability remains open |
| `D06-D07` creature HUD / battle-list model | `NOT_STARTED` | `PARTIAL` | #558 → #566/#567 accepted current-build static G0; no row `DONE` |
| `D12-D14`, `D19-D22` item metadata / stash / depot / managed containers / Quick Loot | `NOT_STARTED` | `PARTIAL` | #559 → #574 current-build D09-D22 package; all fourteen D09-D22 rows accepted `PARTIAL`, existing D09-D11/D15-D18 already were `PARTIAL` |
| `F11-F12` minimap state / markers | `NOT_STARTED` | `PARTIAL` | #545 corrected and promoted through #551/#552; per-method target-address overclaim rejected, static model retained |
| `G01`, `G04-G06` Cyclopedia shell / Bestiary / Charms / Monster Bonus | `NOT_STARTED` | `PARTIAL` | #560 → #564/#565 accepted current-build static G0 |
| `G24-G30` Market / Store / Daily Reward / Reward Wall / Character Info / Blessings-premium / Character auction-trade | `NOT_STARTED` | `PARTIAL` | #546 → #547 accepted exact transport-name + bounded handler/controller evidence, mapped by **canonical semantic row name** rather than source-local G numbering |
| `H07-H14` action bars / hotkeys / options / persistence | `NOT_STARTED` | `PARTIAL` | #544 corrected and promoted through #562/#563; H11/H14 additionally have causal Master Volume persistence/restart/rollback evidence; no row `DONE` |
| `H21-H22` current-version RE / reusable discovery after update | `BLOCKED` | `PARTIAL` | current-build revalidation now exists across #544/#551/#556/#558/#559/#560 and #528 exact-SHA helper gates; breadth and future-update stability remain incomplete |

### Explicit non-deltas

- `A15` remains **BLOCKED** because the post-proof process handoff lost the governed in-game session. Negative stability evidence is not success.
- `A11-A13` remain **PARTIAL**: current-build login routing is materially stronger, but complete character-list/game-login/disconnect semantics are not promoted to `DONE` here.
- `B04` and `C21` remain **PARTIAL**. #539/S10 terminated with `BLOCKED_MISSING_RETAINED_CODE_WINDOW`; H1 sender wrapper and H3 queue/builder facts were accepted, but the action-specific connect/member edge was not proven.
- `C10` remains **BLOCKED** pending a separately legal causal current-player XYZ discriminator.
- `F08` and `F10` remain **BLOCKED** pending #475 server-delivery / worldmap patch causality.
- `G31` World transfer/main-character change remains **NOT_STARTED**. #547 found no dedicated transport mapping and #550's later GUI observation is explicitly diagnostic/not promotable.
- #550 contributes **no canonical G24-G31 live status delta**; its bounded runtime task closed `BLOCKED_RUNTIME_ADMISSION_UNAVAILABLE`.
- #557 contributes **no coverage delta**; it was closed unmerged as superseded after later current-build #560 evidence.
- `H01-H06` and `H15-H19` are not promoted from compiled-name/controller presence alone. The current-build UI/settings refresh intentionally keeps their semantic edges unresolved.

## Updated totals

```text
DONE         14
PARTIAL      95
NOT_STARTED  56
BLOCKED       4
TOTAL       169
```

These are row counts, not a weighted client-completion percentage.

## Remaining blocked rows

```text
A15  Restart/relogin semantic stability
C10  Authoritative local-player XYZ
F08  Server-delivered map extent/control model
F10  Worldmap patch causal propagation
```

Everything else is either `DONE`, `PARTIAL`, or `NOT_STARTED`; `PARTIAL` must not be read as semantic completion.

## Current programme frontier

1. Resolve #475 under fresh legal Track A admission to separate server delivery, protocol negotiation, storage and render/picker effects for F08/F10.
2. Revisit C10 only when a separately legitimate current registered `IN_GAME` lifecycle exists; do not bootstrap/login solely to manufacture XYZ evidence.
3. Repair/research A15 session-retention semantics across process handoff/restart without reusing the already-completed #528 one-shot proof merely for duplication.
4. Continue dedicated semantic packages for the 56 `NOT_STARTED` rows and convert `PARTIAL` rows to `DONE` only with their exact causal/live/stability boundary.
5. Treat #539/S10's missing retained action-specific connect window as a known static limitation rather than inferring the absent edge.

## Safety / audit boundary

This refresh is repository-only documentation synthesis with `runtime_access: none`. It performs no client execution, login, credential use, GUI input, gameplay, transaction, process-memory access or runtime mutation.
