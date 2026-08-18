# OTCLIENT-TIBIA-RE — FULL CLIENT RE 100% checklist

```yaml
report_date: 2026-08-18
repository: blakinio/otclient
track: official-client-re
subject: official native Linux Tibia client only
snapshot_main: ebbb36f50076ff4072c7218e302614c1dfea00b1
task: OTC-20260818-track-a-full-client-re-coverage-audit
pr: 536
execution_class: github_hosted
runtime_access: none
researched_exact_client_version: 15.32.df7b29
researched_exact_client_size: 51965216
researched_exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
status_rows_total: 169
done: 10
partial: 64
not_started: 86
blocked: 9
```

## Purpose

This is the canonical subsystem-by-subsystem completion checklist for reverse engineering the **whole official native Linux Tibia client**, not only login, protocol or worldmap. It intentionally includes gameplay state/actions, inventory/equipment, containers, creatures, chat/social/trade, minimap/worldmap, feature systems, analyzers, generic UI, client options/settings, runtime health and updater/version resilience.

The row counts are **not a weighted completion percentage**. One `DONE` row can represent a narrow exact-binary fact while one `NOT_STARTED` row can represent an entire product subsystem.

## Status contract

- **DONE** — the exact row claim is fully proven at its required evidence boundary. A static symbol/QMeta/protobuf name alone can never make a row `DONE`. A build-fenced `DONE` still requires current-build revalidation before reuse on a newer official client.
- **PARTIAL** — dedicated evidence exists beyond broad lexical presence, but a causal semantic/runtime/current-build/restart-stability edge remains.
- **NOT_STARTED** — only broad capability-census/static-presence evidence exists, or no dedicated semantic proof package exists. This does **not** mean the official client lacks the feature.
- **BLOCKED** — a concrete current dependency prevents the next required proof; the exact unblock route is identified below.

## Current-version hard stop

The exact researched `15.32.df7b29` client is now rejected by the live client/server path as too old. PR #528 records the live version-gate diagnosis and requires a legitimate official-client update before another secret-bearing authentication attempt. Therefore old VAs/RVAs, QMeta addresses, vptrs, instruction fences and native-auth helper assumptions are discovery evidence only until the new current binary is fenced and revalidated.

## Evidence key

| Key | Primary durable evidence |
|---|---|
| `CAP` | `docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md` |
| `COV` | `docs/agents/reports/OTCLIENT-20260816-track-a-coverage-audit-refresh.md` plus canonical denominator registries |
| `S1` | `docs/agents/reports/OTCLIENT-20260818-track-a-s1-unfiltered-static-census.md` |
| `S2` | `docs/agents/reports/OTCLIENT-20260818-track-a-s2-player-inbound-static.md` |
| `S5` | `docs/agents/reports/OTCLIENT-20260818-track-a-s5-container-inbound-static.md` |
| `S6` | `docs/agents/reports/OTCLIENT-20260818-track-a-s6-chat-inbound-static.md` |
| `S7` | `docs/agents/reports/OTCLIENT-20260818-track-a-s7-inventory-equipment-static.md` |
| `S8` | `docs/agents/reports/OTCLIENT-20260818-track-a-s8-creature-inbound-static.md` |
| `S9` | `docs/agents/reports/OTCLIENT-20260818-track-a-s9-action-control-static-census.md`, promoted by #537 on this snapshot |
| `AUTH` | PR #498 / `docs/research/native-client/NATIVE_AUTH_SESSION_FLOW.md` |
| `GAMELOGIN` | PR #499 / `docs/research/native-client/NATIVE_GAME_LOGIN_CREDENTIAL_PROOF.md` |
| `LOGIN-E2E` | PR #528 and `docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/**` |
| `XRES` | promoted PRs #457/#461/#465 plus PR #528 gen16 runtime evidence |
| `NET` | promoted outbound transport chain through PR #500 |
| `XYZ` | PR #302 direct-player-position consumer |
| `WM` | PR #367 and `docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md` |
| `WM-CANARY` | PR #462 one-byte `[19,14]` startup canary |
| `WM-EXT` | PR #473 static server-delivery extent plus active physical PR #475 |
| `WORLD-OBS` | PR #439 world-observation/Atlas producer boundary |
| `P0-CYCLOPEDIA` | PR #435 exact-client Cyclopedia structural evidence |
| `NONE` | no dedicated Track A semantic proof located on this trusted snapshot |

## Remaining-step codes

| Code | Exact next proof required |
|---|---|
| `CURRENT-FENCE` | Acquire the legitimate current official Linux client through the official update path; record exact version, size and SHA-256 before applying old-build RE. |
| `CURRENT-RE` | On the newly fenced client, re-prove required QMeta/vptr/offset/instruction/object contracts and rebuild/revalidate any exact-build helper. |
| `IN-GAME` | Complete native auth → character selection → game-server login and prove causal structural `IN_GAME`, without OCR/coordinate login. |
| `LIVE-STATE` | Bind the static/queue/handler/storage/controller surface to authoritative current live values with causal correlation. |
| `LIVE-ACTION` | Starting from promoted S9 and exact code/dataflow evidence, prove semantic action → routing/protocol serialization → server/client effect, then expose it through the stable bridge. |
| `STABILITY` | Prove rediscovery and equivalent semantics across restart/relogin; for address-sensitive rows also revalidate after client update. |
| `DEDICATED-G0` | Create the first dedicated exact-build subsystem package and prove read-only G0/G1 semantics; add reversible action proof only where safe. |
| `SAFE-READ` | Build a dedicated read-only semantic model for the account/economy surface; do not spend, purchase, transfer or irreversibly mutate resources for proof. |
| `SETTINGS` | Recover the official-client settings persistence/controller/storage model and prove safe read plus reversible write/reload semantics. |
| `WM-475` | Execute/complete the authorized #475 causal baseline `[18,14]` vs `[19,14]` discriminator and separate server delivery, storage, render and picker effects. |
| `OS-EGRESS` | Trace the proven QTcpSocket path to a specific Linux syscall/kernel write only if programme acceptance actually requires that lower boundary. |
| `NO-GAP` | No missing step for the exact build-fenced claim; newer-client reuse is gated by `CURRENT-RE`. |

## A. Lifecycle, version, runtime, login and session

| ID | Subsystem / acceptance surface | Status | Evidence | Remaining step |
|---|---|---|---|---|
| A01 | Current official Linux client identity/version fence | **BLOCKED** | LOGIN-E2E | CURRENT-FENCE |
| A02 | Launcher/update path and client refresh | **PARTIAL** | LOGIN-E2E | CURRENT-FENCE |
| A03 | Native Linux startup / Qt graphics initialization | **PARTIAL** | XRES, LOGIN-E2E | CURRENT-RE |
| A04 | X11/XRes exact-client window ownership | **DONE** | XRES | NO-GAP |
| A05 | noVNC / remote-view observability chain | **PARTIAL** | LOGIN-E2E | STABILITY |
| A06 | Canonical lease / registration / Gate A / rebind / Gate B control plane | **PARTIAL** | ADR/runtime governance | STABILITY |
| A07 | Native cold-auth entry below form UI | **PARTIAL** | AUTH, LOGIN-E2E | CURRENT-RE |
| A08 | 2FA/device/login-confirmation preservation | **PARTIAL** | AUTH | IN-GAME |
| A09 | Retained auth/play-session reuse | **PARTIAL** | AUTH | CURRENT-RE |
| A10 | Character list + world list model | **PARTIAL** | AUTH, LOGIN-E2E | IN-GAME |
| A11 | Native character-selection request | **PARTIAL** | AUTH | IN-GAME |
| A12 | Game-server login message/credential path | **PARTIAL** | AUTH, GAMELOGIN | IN-GAME |
| A13 | Disconnect/reconnect/character-switch reaction paths | **PARTIAL** | AUTH, CAP | IN-GAME then STABILITY |
| A14 | Causal structural `IN_GAME` | **BLOCKED** | LOGIN-E2E | CURRENT-FENCE → CURRENT-RE → IN-GAME |
| A15 | Restart/relogin semantic stability | **BLOCKED** | LOGIN-E2E | IN-GAME → STABILITY |
| A16 | Stable form-less bridge across client update | **BLOCKED** | LOGIN-E2E | CURRENT-RE → STABILITY |

## B. Protocol inventory and transport

| ID | Subsystem / acceptance surface | Status | Evidence | Remaining step |
|---|---|---|---|---|
| B01 | Complete generated protocol identifier inventory 349/349 | **DONE** | S1/COV | NO-GAP |
| B02 | Protocol direction inventory 160 C2S / 189 S2C | **DONE** | S1/COV | NO-GAP |
| B03 | Common inbound dispatcher topology | **PARTIAL** | S1-S8 | LIVE-STATE |
| B04 | Common outbound action router → protocol edge | **PARTIAL** | S9 | LIVE-ACTION |
| B05 | Outbound framing | **DONE** | NET | NO-GAP |
| B06 | Outbound sequence field semantics | **DONE** | NET | NO-GAP |
| B07 | Outbound encryption transform / TXteaHelper role | **DONE** | NET | NO-GAP |
| B08 | Compression absence on the proven outbound path | **DONE** | NET | NO-GAP |
| B09 | Final binary egress at Qt/QTcpSocket boundary | **DONE** | NET | NO-GAP |
| B10 | Specific Linux OS socket syscall | **NOT_STARTED** | NET | OS-EGRESS |
| B11 | Complete inbound transform/framing/decryption order | **NOT_STARTED** | COV | DEDICATED-G0 |
| B12 | Per-message semantic support across all 349 identifiers | **PARTIAL** | S1-S9/COV | LIVE-STATE |
| B13 | Unknown incoming-event preservation/classification | **PARTIAL** | S1/CAP | LIVE-STATE |

## C. Player state and native gameplay actions

| ID | Subsystem / acceptance surface | Status | Evidence | Remaining step |
|---|---|---|---|---|
| C01 | Player inbound queue signal boundaries | **PARTIAL** | S2 | LIVE-STATE |
| C02 | Player identity/vocation/level model | **PARTIAL** | S2, CAP | LIVE-STATE |
| C03 | HP / max HP | **PARTIAL** | S2, CAP | LIVE-STATE |
| C04 | Mana / max mana | **PARTIAL** | S2, CAP | LIVE-STATE |
| C05 | Skills/base-effective skill values | **PARTIAL** | S2, CAP | LIVE-STATE |
| C06 | Capacity / soul / vocation-specific values | **PARTIAL** | S2, CAP | LIVE-STATE |
| C07 | Conditions/status flags/mana shield/resting state | **PARTIAL** | CAP | LIVE-STATE |
| C08 | Cooldown/exhaustion groups and lifetimes | **PARTIAL** | CAP | LIVE-STATE |
| C09 | PvP/combat-mode state | **PARTIAL** | CAP | LIVE-STATE |
| C10 | Authoritative local-player XYZ | **BLOCKED** | XYZ | IN-GAME → causal movement correlation |
| C11 | Eight-direction movement | **PARTIAL** | S9, CAP | LIVE-ACTION |
| C12 | Four-direction rotation | **PARTIAL** | S9, CAP | LIVE-ACTION |
| C13 | Stop / cancel movement | **PARTIAL** | S9, CAP | LIVE-ACTION |
| C14 | GoPath / autowalk/path state | **PARTIAL** | S9, CAP | LIVE-ACTION |
| C15 | Attack | **PARTIAL** | S8/S9 | LIVE-ACTION |
| C16 | Follow | **PARTIAL** | S8/S9 | LIVE-ACTION |
| C17 | Cancel attack/follow target | **PARTIAL** | S9, CAP | LIVE-ACTION |
| C18 | Use object | **PARTIAL** | S9, CAP | LIVE-ACTION |
| C19 | Use-with / use two objects | **PARTIAL** | S9, CAP | LIVE-ACTION |
| C20 | Use-on-creature | **PARTIAL** | S9, CAP | LIVE-ACTION |
| C21 | Move item/object | **PARTIAL** | S9, CAP | LIVE-ACTION |
| C22 | Mount/outfit/tactics player actions | **PARTIAL** | S9, CAP | LIVE-ACTION |

## D. Creatures, inventory/equipment, containers and loot telemetry

| ID | Subsystem / acceptance surface | Status | Evidence | Remaining step |
|---|---|---|---|---|
| D01 | Creature-family inbound queue boundaries | **PARTIAL** | S8 | LIVE-STATE |
| D02 | Queue → non-QMeta creature handler dispatch | **PARTIAL** | S8 | exact code window → LIVE-STATE |
| D03 | Creature handler → model/storage mutation | **PARTIAL** | S8 | exact code window → LIVE-STATE |
| D04 | Central creature registry/lifecycle | **PARTIAL** | S8, CAP | LIVE-STATE |
| D05 | Creature health/outfit/speed/skull/party/marks/light/type/unpass fields | **PARTIAL** | S8, CAP | LIVE-STATE |
| D06 | Creature HUD names/icons/status effects | **NOT_STARTED** | CAP | DEDICATED-G0 |
| D07 | Battle-list filters/sorting/secondary lists | **NOT_STARTED** | CAP | DEDICATED-G0 |
| D08 | Battle target/first-next target selection | **PARTIAL** | S8/S9 | LIVE-ACTION |
| D09 | Inventory Set/Delete/PlayerInventory inbound boundaries | **PARTIAL** | S7 | LIVE-STATE |
| D10 | Equipment slot semantic model | **PARTIAL** | S7, CAP | LIVE-STATE |
| D11 | Inventory storage → status-controller propagation | **PARTIAL** | S7 | LIVE-STATE |
| D12 | Appearance ID ↔ item name/description lookup | **NOT_STARTED** | CAP | DEDICATED-G0 |
| D13 | Item count/subtype/tier/charges/duration metadata | **NOT_STARTED** | CAP | DEDICATED-G0 |
| D14 | Object/weapon proficiency XP metadata | **NOT_STARTED** | CAP | DEDICATED-G0 |
| D15 | Open-container registry/storage | **PARTIAL** | S5/S7 | LIVE-STATE |
| D16 | Create/change/delete-in-container propagation | **PARTIAL** | S5 | LIVE-STATE |
| D17 | Container close/up/parent/pagination navigation | **PARTIAL** | S5/S9 | LIVE-ACTION |
| D18 | Container sort/object-info requests | **PARTIAL** | S5/S9 | LIVE-ACTION |
| D19 | Stash semantic model | **NOT_STARTED** | CAP | DEDICATED-G0 |
| D20 | Depot search | **NOT_STARTED** | CAP | DEDICATED-G0 |
| D21 | Managed/special containers | **NOT_STARTED** | CAP | DEDICATED-G0 |
| D22 | Quick Loot / obtain-container assignment | **NOT_STARTED** | CAP | DEDICATED-G0 |
| D23 | Loot tracking / dropped-item model | **NOT_STARTED** | CAP | DEDICATED-G0 |
| D24 | Gain/Waste storage and metrics | **NOT_STARTED** | CAP | DEDICATED-G0 |
| D25 | Loot/Waste/Impact/Damage/Hunting/Progress/Party Hunt analyzer suite | **NOT_STARTED** | CAP | DEDICATED-G0 |

## E. Chat, social, party and trade

| ID | Subsystem / acceptance surface | Status | Evidence | Remaining step |
|---|---|---|---|---|
| E01 | Chat inbound queue/handler/channel-storage boundaries | **PARTIAL** | S6 | LIVE-STATE |
| E02 | Chat outbound action boundary | **PARTIAL** | S9 | LIVE-ACTION |
| E03 | Channel/private/NPC channel model and events | **PARTIAL** | S6/S9 | LIVE-STATE |
| E04 | Channel moderation invite/exclude | **NOT_STARTED** | CAP | DEDICATED-G0 |
| E05 | NPC semantic conversation/options | **NOT_STARTED** | CAP | DEDICATED-G0 |
| E06 | NPC trade offers/prices/buy-sell state | **NOT_STARTED** | CAP | DEDICATED-G0 |
| E07 | Player-to-player trade own/counteroffer state | **NOT_STARTED** | CAP | DEDICATED-G0 |
| E08 | Friends account search | **NOT_STARTED** | CAP | DEDICATED-G0 |
| E09 | VIP/contact storage/groups/icons/online state | **NOT_STARTED** | CAP | DEDICATED-G0 |
| E10 | Social dialog/controller model | **NOT_STARTED** | CAP | DEDICATED-G0 |
| E11 | Party invite/join/leave/leadership lifecycle | **NOT_STARTED** | CAP | DEDICATED-G0 |
| E12 | Shared-experience state/action | **NOT_STARTED** | CAP | DEDICATED-G0 |
| E13 | White/blacklist configuration | **NOT_STARTED** | CAP | DEDICATED-G0 |
| E14 | Exiva options/configuration | **NOT_STARTED** | CAP | DEDICATED-G0 |

## F. Worldmap, minimap, storage, rendering and observation

| ID | Subsystem / acceptance surface | Status | Evidence | Remaining step |
|---|---|---|---|---|
| F01 | World/map inbound protocol families | **PARTIAL** | CAP/S1/WM | LIVE-STATE |
| F02 | Worldmap handler → storage static dependency graph | **DONE** | WM | NO-GAP |
| F03 | TWorldMapStorage bounds/eviction semantics | **PARTIAL** | WM | LIVE-STATE |
| F04 | Viewport geometry/default/recompute | **PARTIAL** | WM | LIVE-STATE |
| F05 | RenderProvider fixed-32 clipping/index/iteration | **PARTIAL** | WM | LIVE-STATE |
| F06 | Picker screen/world transforms | **PARTIAL** | WM | LIVE-STATE |
| F07 | Camera layout/ViewPort co-ownership | **PARTIAL** | WM | LIVE-STATE |
| F08 | Server-delivered map extent/control model | **BLOCKED** | WM-EXT/#475 | WM-475 |
| F09 | `[19,14]` one-byte patched-client startup canary | **DONE** | WM-CANARY | NO-GAP |
| F10 | Worldmap patch causal propagation | **BLOCKED** | WM-CANARY/#475 | WM-475 |
| F11 | Minimap controller / visible area / floor state | **NOT_STARTED** | CAP/WM | DEDICATED-G0 |
| F12 | Minimap markers | **NOT_STARTED** | CAP/WM | DEDICATED-G0 |
| F13 | World↔screen coordinate transforms | **PARTIAL** | CAP/WM | LIVE-STATE |
| F14 | World Observation Index / deterministic export boundary | **PARTIAL** | WORLD-OBS | LIVE-STATE |
| F15 | OTBM-compatible reconstruction/static-dynamic classification | **PARTIAL** | WM/WORLD-OBS | LIVE-STATE |

## G. Cyclopedia, progression, economy and feature systems

| ID | Subsystem / acceptance surface | Status | Evidence | Remaining step |
|---|---|---|---|---|
| G01 | Cyclopedia shell/request-cache model | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G02 | Cyclopedia map | **PARTIAL** | CAP/P0-CYCLOPEDIA | LIVE-STATE |
| G03 | Cyclopedia houses data/actions | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G04 | Bestiary kills/unlocks/loot/progress | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G05 | Charms selection/assignment | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G06 | Monster Bonus Effects | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G07 | Bosstiary/Boss Tracker | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G08 | Boss difficulty selection | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G09 | Prey | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G10 | Taskboard | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G11 | Bounty Tasks | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G12 | Weekly Tasks | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G13 | Soul Seals | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G14 | Skill Wheel nodes/points/configuration | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G15 | Skill Wheel gems | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G16 | Skill Wheel presets | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G17 | Exaltation Forge fusion | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G18 | Exaltation Forge transfer/convergence | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G19 | Imbuements/durations/tracker | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G20 | Weapon Proficiency | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G21 | Quest Log | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G22 | Quest Tracker | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G23 | Houses catalogue/ownership/actions/errors | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G24 | Market catalogue/offers/history/statistics | **NOT_STARTED** | CAP | SAFE-READ |
| G25 | Store catalogue/Tibia Coins/transaction history | **NOT_STARTED** | CAP | SAFE-READ |
| G26 | Daily Reward | **NOT_STARTED** | CAP | SAFE-READ |
| G27 | Reward Wall/resting bonuses/returner state | **NOT_STARTED** | CAP | SAFE-READ |
| G28 | Character Info panels | **NOT_STARTED** | CAP | SAFE-READ |
| G29 | Blessings/premium panels | **NOT_STARTED** | CAP | SAFE-READ |
| G30 | Character auction/trade UI | **NOT_STARTED** | CAP | SAFE-READ |
| G31 | World transfer/main-character change | **NOT_STARTED** | CAP | SAFE-READ |
| G32 | Calendar | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G33 | News/returner information | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G34 | Highscores | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G35 | Hirelings | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G36 | Creature podium | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G37 | Offline training | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G38 | Vocation selection | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G39 | Tutorial hints/overlay | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G40 | Inspect player/object and Item Info | **NOT_STARTED** | CAP | DEDICATED-G0 |
| G41 | Outfit Memorial | **NOT_STARTED** | CAP | DEDICATED-G0 |

## H. Generic UI, action bars, options/settings, health and update resilience

| ID | Subsystem / acceptance surface | Status | Evidence | Remaining step |
|---|---|---|---|---|
| H01 | Server modal dialogs | **NOT_STARTED** | CAP | DEDICATED-G0 |
| H02 | Death dialog/fair-fight data | **NOT_STARTED** | CAP | DEDICATED-G0 |
| H03 | Logout confirmation/close request | **NOT_STARTED** | CAP | DEDICATED-G0 |
| H04 | Generic context-menu semantic actions | **NOT_STARTED** | CAP | DEDICATED-G0 |
| H05 | Generic dialog/modal/window/tab/selection state | **NOT_STARTED** | CAP | DEDICATED-G0 |
| H06 | Drag-and-drop semantic state | **NOT_STARTED** | CAP | DEDICATED-G0 |
| H07 | Action-bar assignment model | **NOT_STARTED** | CAP | DEDICATED-G0 |
| H08 | Hotkey configuration/use mode | **NOT_STARTED** | CAP | DEDICATED-G0 |
| H09 | Multi-action buttons/cooldown overlays | **NOT_STARTED** | CAP | DEDICATED-G0 |
| H10 | Graphics options/settings model | **NOT_STARTED** | NONE | SETTINGS |
| H11 | Audio/music/ambient options/settings model | **NOT_STARTED** | NONE | SETTINGS |
| H12 | Interface/sidebar/UI options/settings model | **NOT_STARTED** | NONE | SETTINGS |
| H13 | Gameplay/control options/settings model | **NOT_STARTED** | NONE | SETTINGS |
| H14 | Options persistence/profile/migration model | **NOT_STARTED** | NONE | SETTINGS |
| H15 | Structured sound-event/world-cue model | **NOT_STARTED** | CAP | DEDICATED-G0 |
| H16 | Network lane/dual-connection live state | **NOT_STARTED** | CAP | DEDICATED-G0 |
| H17 | Latency/FPS/frame-timing state | **NOT_STARTED** | CAP | DEDICATED-G0 |
| H18 | Anti-cheat passive safety/session signals only | **NOT_STARTED** | CAP | DEDICATED-G0 |
| H19 | `TSessiondumpPlayer` research lead | **NOT_STARTED** | CAP | DEDICATED-G0 |
| H20 | Updater/package manifest/current-client acquisition | **PARTIAL** | LOGIN-E2E | CURRENT-FENCE |
| H21 | Current-version QMeta/vptr/offset/instruction revalidation | **BLOCKED** | LOGIN-E2E | CURRENT-FENCE → CURRENT-RE |
| H22 | Reusable discovery after client update | **BLOCKED** | LOGIN-E2E | CURRENT-RE → STABILITY |
| H23 | Full-client semantic coverage registry tied to evidence gates | **PARTIAL** | COV/this report | progressively promote rows only after their evidence gate passes |

## Programme conclusions

1. **Structural discovery is broad, semantic completion is not.** The programme has a complete 349-message protocol denominator and a 642-record Tibia-owned QMeta denominator, but denominator completeness is not semantic completeness.
2. **The independent repo-only S1–S9 wave is now closed.** Promoted S9 adds the 28-class `*GameActionHandler` denominator and principal movement/attack/follow/use/container/chat/player/router QMeta boundaries. It still does not prove per-action receiver/protocol dataflow, serialization or server effect.
3. **The core path is materially ahead of feature UI.** Login/session, outbound transport, player/containers/chat/inventory/creatures, worldmap and action-control surfaces have dedicated bounded work; most feature systems are still broad `STATIC_PRESENT` leads only.
4. **Inventory/equipment is not `DONE`.** S7 proves exact queue/handler/storage/controller surfaces and corrects handler ownership, but queue→handler→inventory mutation→controller→authoritative live slot/value causality remains open.
5. **Creatures are not `DONE`.** S8 exhausts the retained QMeta frontier and proves exact queue/model/storage/action-handler surfaces, but non-QMeta inbound dispatch and live mutation causality remain open.
6. **Options/settings are a first-class gap.** Graphics, audio, interface/sidebar, gameplay/control and persistence/profile settings are explicit `NOT_STARTED` rows because no dedicated Track A semantic settings model was located on this trusted snapshot.
7. **The current official-client version update is the dominant cross-cutting blocker.** Runtime-sensitive proof must not reuse the `15.32.df7b29` address/fence set until the new client is acquired, hashed and re-reversed where needed.
8. **Programme `100%` means every row `DONE`.** That requires current-build proof, causal live semantics where required, restart/relogin/update-stable rediscovery and a reusable structured interface rather than OCR, image matching or coordinate automation.

## Recommended execution order

```text
1. Legitimately update/fence the current official Linux client.
2. Re-prove current-build QMeta/vptr/offset/instruction contracts and rebuild/revalidate native bridge helpers.
3. Complete native login -> character selection -> game-server login -> causal IN_GAME.
4. Use the single legal canonical runtime to close player XYZ, restart/relogin and worldmap server-delivery blockers.
5. Starting from promoted S9, recover exact action connection/dataflow windows and convert core action boundaries into router -> protocol -> causal runtime proofs.
6. Close queue/handler/storage semantics for player, creature, inventory, container and chat families.
7. Run dedicated read-only packages for item metadata, loot/analyzers, social/trade and minimap.
8. Run dedicated feature waves for Cyclopedia/Bestiary/Bosstiary/Prey/Taskboard/Skill Wheel/Forge/Imbuements/Weapon Proficiency/Quest/Houses/Market.
9. Recover and validate the missing official-client settings/options model: graphics, audio, interface, gameplay/control and persistence.
10. Finish P3 account/economy read-only surfaces and prove restart/update-resilient full bridge/API coverage.
```

## Audit and E2E boundary

This report performs no official-client execution, no Synology/X11/VNC/process-memory observation, no credential or secret access, no login/gameplay, no proprietary-byte staging and no client mutation. It is a repository evidence synthesis only.

`E2E: NOT_APPLICABLE` — this documentation/audit change does not modify product/runtime behaviour.
