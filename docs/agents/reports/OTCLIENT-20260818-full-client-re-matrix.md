# OTCLIENT-TIBIA-RE — FULL CLIENT RE coverage matrix

```yaml
report_date: 2026-08-19
repository: blakinio/otclient
track: official-client-re
subject: official native Linux Tibia client only
snapshot_main: 5d1a09dcb5b3abc22d341951b81d557495d755a6
source_checklist: docs/agents/reports/OTCLIENT-20260818-full-client-re-100-percent-checklist.md
current_refresh_overlay: docs/agents/reports/OTCLIENT-20260818-full-client-re-current-refresh.md
source_pr: 536
coordinator_review: 4971484054
status_rows_total: 169
done: 14
partial: 95
not_started: 56
blocked: 4
```

## Matrix contract

This is the compact **current** projection of the canonical 169-row denominator. The detailed checklist preserves the historical 2026-08-18 row definitions/evidence snapshot; `OTCLIENT-20260818-full-client-re-current-refresh.md` records every accepted post-snapshot status delta and is authoritative together with this matrix for current status.

Status meanings remain fail-closed:

- `DONE` — the exact row claim is proven at its required evidence boundary;
- `PARTIAL` — dedicated evidence exists, but a semantic/runtime/stability/breadth edge remains;
- `NOT_STARTED` — no dedicated semantic package sufficient for `PARTIAL` has been accepted;
- `BLOCKED` — a concrete current dependency prevents the next required proof.

Static class/QMeta/protobuf presence alone never makes a row `DONE`. Diagnostic-only GUI evidence never advances canonical status.

## 1. Executive status matrix

| Area | DONE | PARTIAL | NOT STARTED | BLOCKED | TOTAL |
|---|---:|---:|---:|---:|---:|
| **A — Lifecycle / version / runtime / login / session** | 5 | 10 | 0 | 1 | 16 |
| **B — Protocol inventory / transport** | 7 | 4 | 2 | 0 | 13 |
| **C — Player state / native gameplay actions** | 0 | 21 | 0 | 1 | 22 |
| **D — Creatures / inventory / equipment / containers / loot** | 0 | 22 | 3 | 0 | 25 |
| **E — Chat / social / party / trade** | 0 | 3 | 11 | 0 | 14 |
| **F — Worldmap / minimap / render / observation** | 2 | 11 | 0 | 2 | 15 |
| **G — Cyclopedia / progression / economy / feature systems** | 0 | 12 | 29 | 0 | 41 |
| **H — Generic UI / action bars / options / health / update resilience** | 0 | 12 | 11 | 0 | 23 |
| **TOTAL** | **14** | **95** | **56** | **4** | **169** |

## 2. Full 169-row ID matrix

Every checklist ID appears exactly once.

| Area | DONE | PARTIAL | NOT STARTED | BLOCKED |
|---|---|---|---|---|
| **A** | `A01`, `A04`, `A07`, `A09`, `A14` | `A02`, `A03`, `A05`, `A06`, `A08`, `A10–A13`, `A16` | — | `A15` |
| **B** | `B01`, `B02`, `B05–B09` | `B03`, `B04`, `B12`, `B13` | `B10`, `B11` | — |
| **C** | — | `C01–C09`, `C11–C22` | — | `C10` |
| **D** | — | `D01–D22` | `D23–D25` | — |
| **E** | — | `E01–E03` | `E04–E14` | — |
| **F** | `F02`, `F09` | `F01`, `F03–F07`, `F11–F15` | — | `F08`, `F10` |
| **G** | — | `G01`, `G02`, `G04–G06`, `G24–G30` | `G03`, `G07–G23`, `G31–G41` | — |
| **H** | — | `H07–H14`, `H20–H23` | `H01–H06`, `H15–H19` | — |

## 3. Current exact-client and login matrix

| Evidence boundary | Current result | Coverage consequence |
|---|---|---|
| Current official native-Linux fence | `15.32`, size `52109920`, SHA-256 `ed5469b9...`, ELF Build ID `d803d969...` | `A01=DONE`; old `e6c244bd...` addresses remain historical-only |
| Current-build cold-auth QMeta/gates | independently re-proven on exact current SHA | supports `A07=DONE`, `H21=PARTIAL`; not a blanket ABI guarantee |
| Native login → world proof | `SUCCESS_AT_PROOF_POINT`, `CHARACTER_ACTUALLY_LOGGED_INTO_GAME=YES`, structural `PASS_3_OF_3` | `A14=DONE`; causal world entry is no longer blocked |
| Retained authenticated-session reuse | restart without credentials restored authenticated play session and reached world | `A09=DONE` at the narrow row boundary |
| Later process handoff | governed session not retained; terminal state login screen | `A15=BLOCKED`; prevents a stability success claim |
| Current-SHA helper rediscovery | helper/gate set rebuilt/revalidated on new client | `A16=PARTIAL`, `H22=PARTIAL`; future-update/restart breadth remains open |

## 4. Accepted current-build subsystem deltas

| Package | Accepted current impact |
|---|---|
| UI/settings #544 → #562/#563 | `H07–H14 = PARTIAL`; H11/H14 strengthened by causal Master Volume `100→43→restart 43→rollback 100→restart 100`; fullscreen persistence remains inconclusive |
| World/minimap #545 → #551/#552 | `F11`, `F12 = PARTIAL`; `F13` remains PARTIAL; `F08/F10` remain blocked; false per-method direct-address claims rejected |
| Auth/session #556 → #569/#570 | exact-current cold-auth/game-server/character-selection QMeta structure revalidated; signal targets kept distinct from call-safe methods |
| Creature/combat #558 → #566/#567 | `D06`, `D07 = PARTIAL`; C15-C17 and D01-D05/D08 remain PARTIAL corroboration |
| Inventory/containers #559 → #574 | all `D09–D22 = PARTIAL`; current-build queue→handler→storage/controller routing materially strengthened; no row DONE |
| Features #560 → #564/#565 | `G01`, `G04–G06 = PARTIAL`; no row DONE |
| Economy static #546 → #547/#549 | canonical semantic rows `G24–G30 = PARTIAL`; `G31` remains NOT_STARTED |
| Economy runtime #550 → #579/#580 | `canonical_live_G24_G31_status_delta = NONE`; GUI observations remain diagnostic/not promotable |
| Action→protocol S10 #539 → #571/#572 | B04/C21 remain PARTIAL; terminal blocker `BLOCKED_MISSING_RETAINED_CODE_WINDOW`; absent action-specific edge is not inferred |
| G01-G06 historical package #557 → #581 | superseded; no canonical coverage delta |

## 5. Critical dependency matrix

| Dependency / proof gate | Current state | Main affected rows | Required transition |
|---|---|---|---|
| Restart/relogin semantic stability | `BLOCKED` by observed post-handoff session loss | `A15`, breadth of `A16/H22` | identify/repair lifecycle semantics and prove equivalent session rediscovery across handoff/restart |
| Authoritative player XYZ | `BLOCKED` | `C10` | separately legitimate current registered `IN_GAME` lifecycle, then bounded causal movement correlation |
| Worldmap server delivery / patch causality | `BLOCKED` | `F08`, `F10` | complete #475 under fresh legal Track A admission; separate server delivery, negotiation, storage, renderer and picker effects |
| Action-specific router→protocol link | static retained-window gap known | `B04`, `C21` and broader live actions | obtain new admissible exact code/dataflow evidence or use a separately legal causal runtime discriminator; do not infer missing H2 edge |
| Core live-state semantics | open | many `C/D/E/F` PARTIAL rows | queue/handler/storage/controller → authoritative current values with causal correlation |
| Feature/economy semantics | mixed PARTIAL/NOT_STARTED | majority of `G` | dedicated exact-current semantic packages; transactions remain fail-closed |
| Settings breadth/stability | PARTIAL | `H07–H14` | per-setting storage/persistence/profile semantics and safe reversible proof where appropriate |
| Current/future update rediscovery | PARTIAL, no longer globally blocked | `A16`, `H21`, `H22` | broaden exact-current revalidation and prove repeatable future-update/restart discovery |

## 6. Remaining BLOCKED rows

Only four rows are currently `BLOCKED`:

```text
A15  Restart/relogin semantic stability
C10  Authoritative local-player XYZ
F08  Server-delivered map extent/control model
F10  Worldmap patch causal propagation
```

A blocked row is not disproven. It records a concrete missing dependency.

## 7. Completion matrix

| Programme condition | Required for 100% |
|---|---|
| All 169 IDs classified `DONE` | **YES** |
| Static/QMeta/protobuf name alone sufficient | **NO** |
| Current official-client fence | established now, but future updates require revalidation |
| Causal live state/action proof where required | **YES** |
| Restart/relogin rediscovery | **YES** for stable lifecycle/bridge rows |
| Client-update rediscovery | **YES** for update-resilience rows |
| Diagnostic-only GUI observation accepted as canonical semantic proof | **NO** |
| OCR/image matching/coordinate automation accepted as semantic proof | **NO** |
| Reusable structured interface rather than ad-hoc UI automation | **YES** |

## Interpretation

The programme has moved materially since the 2026-08-18 snapshot: current-client identity and causal native login-to-world are proven, multiple current-build subsystem G0 packages have landed, inventory/container coverage is substantially broader, and the settings/economy/minimap gaps are no longer uniformly untouched. Semantic completion remains far from 100%: 95 rows are still only `PARTIAL`, 56 remain `NOT_STARTED`, and four have concrete blockers.

The next work should target causal semantics and stability rather than accumulating more lexical presence. In particular, #475 and C10/A15 are high-leverage blockers; other feature work should move `NOT_STARTED→PARTIAL` only through dedicated evidence and `PARTIAL→DONE` only at the exact row acceptance boundary.

## Audit / runtime boundary

This matrix refresh is repository-only documentation synthesis with `runtime_access: none`. No official client execution, credentials, login, GUI input, gameplay, transaction, process-memory access or runtime mutation was performed for this refresh.
