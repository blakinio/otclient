# OTCLIENT-TIBIA-RE — FULL CLIENT RE coverage matrix

```yaml
report_date: 2026-08-18
repository: blakinio/otclient
track: official-client-re
subject: official native Linux Tibia client only
snapshot_main: ebbb36f50076ff4072c7218e302614c1dfea00b1
source_checklist: docs/agents/reports/OTCLIENT-20260818-full-client-re-100-percent-checklist.md
task: OTC-20260818-track-a-full-client-re-coverage-audit
pr: 536
status_rows_total: 169
done: 10
partial: 64
not_started: 86
blocked: 9
```

## Matrix contract

This file is a compact matrix projection of the canonical 169-row checklist. It does not create new evidence or promote any row. Full subsystem names, evidence keys and exact remaining proof are authoritative in `OTCLIENT-20260818-full-client-re-100-percent-checklist.md`.

Status meanings:

- `DONE` — exact row claim proven at its required evidence boundary;
- `PARTIAL` — dedicated evidence exists, but a semantic/runtime/stability/current-build edge remains;
- `NOT_STARTED` — no dedicated semantic proof package yet; broad `STATIC_PRESENT` evidence is insufficient;
- `BLOCKED` — a concrete current dependency prevents the next required proof.

The counts are row counts, not a weighted percentage of the client.

## 1. Executive status matrix

| Area | DONE | PARTIAL | NOT STARTED | BLOCKED | TOTAL |
|---|---:|---:|---:|---:|---:|
| **A — Lifecycle / version / runtime / login / session** | 1 | 11 | 0 | 4 | 16 |
| **B — Protocol inventory / transport** | 7 | 4 | 2 | 0 | 13 |
| **C — Player state / native gameplay actions** | 0 | 21 | 0 | 1 | 22 |
| **D — Creatures / inventory / equipment / containers / loot** | 0 | 13 | 12 | 0 | 25 |
| **E — Chat / social / party / trade** | 0 | 3 | 11 | 0 | 14 |
| **F — Worldmap / minimap / render / observation** | 2 | 9 | 2 | 2 | 15 |
| **G — Cyclopedia / progression / economy / feature systems** | 0 | 1 | 40 | 0 | 41 |
| **H — Generic UI / action bars / options / health / update resilience** | 0 | 2 | 19 | 2 | 23 |
| **TOTAL** | **10** | **64** | **86** | **9** | **169** |

## 2. Full 169-row ID matrix

Every checklist ID appears exactly once below.

| Area | DONE | PARTIAL | NOT STARTED | BLOCKED |
|---|---|---|---|---|
| **A** | `A04` | `A02`, `A03`, `A05–A13` | — | `A01`, `A14–A16` |
| **B** | `B01`, `B02`, `B05–B09` | `B03`, `B04`, `B12`, `B13` | `B10`, `B11` | — |
| **C** | — | `C01–C09`, `C11–C22` | — | `C10` |
| **D** | — | `D01–D05`, `D08–D11`, `D15–D18` | `D06`, `D07`, `D12–D14`, `D19–D25` | — |
| **E** | — | `E01–E03` | `E04–E14` | — |
| **F** | `F02`, `F09` | `F01`, `F03–F07`, `F13–F15` | `F11`, `F12` | `F08`, `F10` |
| **G** | — | `G02` | `G01`, `G03–G41` | — |
| **H** | — | `H20`, `H23` | `H01–H19` | `H21`, `H22` |

## 3. Scope matrix

| Area | Scope represented by IDs |
|---|---|
| **A** | current-client fence, updater/launch, Qt/X11/noVNC, canonical runtime control, native auth, 2FA preservation, retained sessions, character/world list, character selection, game-server login, reconnect, causal `IN_GAME`, restart/relogin and update-stable bridge |
| **B** | all 349 generated protocol identifiers, direction split, inbound/outbound dispatch, framing, sequence, encryption, compression result, QTcpSocket egress, OS egress, inbound transform ordering, per-message semantics and unknown incoming events |
| **C** | player identity, HP/mana, skills, capacity/soul, conditions, cooldowns, PvP modes, authoritative XYZ, movement, rotation, stop/cancel, pathing, attack/follow, use/use-with/use-on-creature, move object and player actions |
| **D** | creatures, creature HUD/battle list, inventory, equipment, item metadata, containers, stash, depot search, managed containers, Quick Loot, loot tracking, gain/waste and analyzer suite |
| **E** | chat/channels, NPC conversation/trade, player trade, Friends/VIP/Social, party/shared experience, white/blacklists and Exiva configuration |
| **F** | world/map protocol, worldmap storage, viewport/render/picker/camera, server-delivered extent, map mutation causality, minimap, coordinate transforms, world observation and OTBM reconstruction |
| **G** | Cyclopedia, Bestiary/charms, monster bonus effects, Bosstiary, Prey, Taskboard/Bounty/Weekly/Soul Seals, Skill Wheel, Forge, Imbuements, Weapon Proficiency, Quest Log/Tracker, Houses, Market, Store, rewards, character/account panels, Calendar/News, Highscores, Hirelings, podium, offline training, vocation/tutorial, inspect/item info and Outfit Memorial |
| **H** | modal/death/logout UI, context menus, generic dialogs, drag/drop, action bars, hotkeys, multi-action buttons, graphics/audio/interface/gameplay options, settings persistence, sound events, network/FPS/latency state, passive anti-cheat/session signals, sessiondump lead, updater/current-client revalidation and full-client coverage registry |

## 4. Critical dependency matrix

| Dependency / proof gate | Current state | Main affected rows | Required transition |
|---|---|---|---|
| **Current official client fence** | `BLOCKED` | `A01`, `A14–A16`, `H20–H22` plus every old-address-sensitive runtime row | acquire legitimate current Linux client → record exact version/size/SHA-256 |
| **Current-build RE refresh** | `BLOCKED_BY_CURRENT_FENCE` | auth helper, QMeta/vptr/offset/instruction-sensitive rows | re-prove exact-build contracts before reuse |
| **Causal structural IN_GAME** | `BLOCKED` | `A14`, `A15`, `C10` and most `LIVE-STATE`/`LIVE-ACTION` work | native auth → character selection → game-server login → structural world-state proof |
| **Authoritative player XYZ** | `BLOCKED` | `C10` | causal movement correlation against current `IN_GAME` runtime |
| **Worldmap server-delivery causality** | `BLOCKED` | `F08`, `F10` | complete authorized PR #475 baseline `[18,14]` vs `[19,14]` discriminator |
| **Core live-state semantics** | `OPEN` | player/creature/inventory/container/chat/world rows | queue/handler/storage/controller → authoritative live-value correlation |
| **Core live-action semantics** | `OPEN` | movement/combat/use/container/chat actions | promoted S9 → exact dataflow/serialization → causal server/client effect |
| **Options/settings semantic model** | `NOT_STARTED` | `H10–H14` | recover persistence/controller/storage model → safe read → reversible write/reload proof |
| **Feature/economy waves** | `MOSTLY_NOT_STARTED` | majority of `G` plus parts of `D/E/H` | dedicated read-only G0/G1 packages; no spending/transfers for proof |
| **Restart/update-stable bridge** | `BLOCKED` | `A15`, `A16`, `H21`, `H22` | current-build rediscovery + restart/relogin equivalence |

## 5. Completion matrix

| Programme condition | Required for 100% |
|---|---|
| All 169 IDs classified `DONE` | **YES** |
| Static/QMeta/protobuf name alone sufficient | **NO** |
| Current official-client version fenced | **YES** for runtime-sensitive claims |
| Causal live state/action proof where required | **YES** |
| Restart/relogin rediscovery | **YES** for stable bridge rows |
| Client-update rediscovery | **YES** for update-resilience rows |
| OCR/image matching/coordinate automation accepted as semantic proof | **NO** |
| Reusable structured interface rather than ad-hoc UI automation | **YES** |

## Interpretation

The matrix shows that the programme is strongest in protocol inventory/transport (`B`) and has substantial partial structural work in the core gameplay path (`A`, `C`, `D`, `F`). The largest untouched semantic surface is the feature/economy family (`G`), followed by generic UI/options/settings (`H`). The dominant cross-cutting blocker is the obsolete researched client build `15.32.df7b29`: current runtime-sensitive work must wait for a legitimate current-client fence and exact-build RE refresh rather than reusing historical addresses as if they were current.