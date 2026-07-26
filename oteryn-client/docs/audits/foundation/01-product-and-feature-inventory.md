# Product and Feature Inventory

Evidence cut: 2026-07-27

## Method

The inventory describes observable behavior required from the new product. Legacy module boundaries are not copied. Evidence comes from maintained client source/modules/tests, Canary protocol/game source and the accepted Rust architecture.

Priority labels:

- **MPS** — minimum playable slice;
- **Beta** — required before a broad beta;
- **Later** — intentionally after beta or dependent on a separate contract;
- **Unknown** — product/contract decision still required.

## Account, entry and lifecycle

| Capability | Priority | Evidence | Audit result |
|---|---|---|---|
| System-browser Oteryn login with Authorization Code + PKCE | MPS | `modules/client_entergame/oteryn_identity*.lua`; Platform game-session contract | `PROVEN` current maintained flow exists; Rust implementation is independent |
| Account session separate from game session | MPS | Platform/Gateway contract and accepted `CLIENT_LIFECYCLE.md` | `PROVEN` separate ticket/session credentials exist; exact Rust API remains implementation work |
| Character selection | MPS | current enter-game/character-list behavior and Canary login layouts | `PROVEN` behavior exists |
| World selection | MPS | Canary modern world list and Gateway authoritative `world_id` | `PROVEN` current concepts exist; Platform/Gateway semantics are narrower than desired channels |
| Gameplay-channel selection | MPS | Canary multi-channel world-list implementation | `PROVEN` Canary can expose the same character per channel; `BLOCKED` Oteryn-native channel-ticket routing contract |
| One-shot game ticket/session handoff | MPS | `GAME_SESSION_CANARY_CONTRACT.md` | `PROVEN` for one configured world/issuer process |
| Logout | MPS | current `Game`/`ProtocolGame` lifecycle and E2E baseline | `PROVEN` behavior exists |
| Relog to a different channel | MPS | product decision ADR-0005; Canary channel list | `SUPPORTED` UI/lifecycle model is defined; native ticket routing remains blocked |
| Reconnect same game session | Beta | current legacy reconnect behavior and architecture | `UNKNOWN` exact Canary resume semantics for Rust; initial ticket replay is forbidden |
| Account logout / token expiry recovery | MPS | Identity security boundary | `PROVEN` required behavior; exact Platform response taxonomy needs fixtures |
| Typed user recovery actions | MPS | accepted lifecycle architecture | `PROVEN` architecture requirement; implementation absent |

## World and core gameplay

| Capability | Priority | Evidence | Audit result |
|---|---|---|---|
| Game transport, handshake, framing and session state | MPS | Canary `ProtocolProfile`, transport profiles, `ProtocolGame` | `PROVEN` server behavior exists; exact fixture set incomplete |
| Map region/tile decoding | MPS | maintained client map/things and Canary `ProtocolGame` | `PROVEN` behavior exists |
| Floors, camera and visibility | MPS | maintained map renderer and protocol | `SUPPORTED`; exact normalized rules need source-level audit during adapter work |
| Creature/player/NPC appearance | MPS | Canary appearance includes and client thing/outfit state | `PROVEN` behavior surface exists |
| Creature spawn, move, update and removal | MPS | `ProtocolGame` and legacy game/map callbacks | `PROVEN` behavior exists |
| Local player movement and stop | MPS | current input/game commands and Canary movement handling | `PROVEN` behavior exists |
| Movement interpolation/prediction | MPS | product performance requirement | `UNKNOWN` exact reconciliation policy; must remain presentation-only |
| Basic player stats/resources | MPS | Canary current profile feature flags and client parsers | `PROVEN` multiple payloads exist; exact MPS subset requires fixtures |
| Effects, projectiles and floating text | MPS | Canary protocol and renderer behavior | `SUPPORTED`; exact packet families/ordering need adapter audit |
| Lighting | Beta | maintained renderer/protocol | `SUPPORTED`; visual acceptance fixture missing |
| Death/session end | MPS | protocol/session-end enums and current lifecycle | `PROVEN` behavior exists; normalized domain cases need tests |

## Items and containers

| Capability | Priority | Evidence | Audit result |
|---|---|---|---|
| Item type/appearance resolution | MPS | current things runtime and Canary item IDs | `PROVEN` required; asset mapping/legal inputs blocked |
| Equipment/inventory | MPS | client inventory module and Canary player/item state | `PROVEN` behavior exists |
| Open/update/close containers | MPS | Canary `Container` protocol surfaces and client module | `PROVEN` behavior exists |
| Move/use/use-with items | MPS | current output protocol and interaction behavior | `PROVEN` behavior exists; exact command fixtures required |
| Stack/subtype/count semantics | MPS | protocol item serialization | `SUPPORTED`; exact version-specific rules need dedicated mapping |
| Depot, inbox, stash | Beta | Canary global data model and current client features | `PROVEN` server domains exist; client UX scope needs separate feature packages |
| NPC trade | Beta | Canary `Npc`, market/trade logic and legacy UI | `PROVEN` behavior exists |
| Direct player trade | Beta | Canary per-channel in-memory model | `PROVEN` same-channel behavior; cross-channel trade is not claimed |

## Combat and social

| Capability | Priority | Evidence | Audit result |
|---|---|---|---|
| Attack/follow target | MPS | current game commands and Canary `ProtocolGame` | `PROVEN` behavior exists |
| Combat state/icons/cooldowns | MPS basic; Beta full | Canary/player protocol and legacy action-bar lifecycle | `PROVEN` domains exist; exact current payload fixtures required |
| Battle list | Beta | maintained `game_battle`/interface behavior | `PROVEN` user surface exists |
| Local chat/say | MPS | Canary `Chat` and `TextMessage` | `PROVEN` per-channel behavior exists |
| Private/channel chat | Beta | current console and Canary chat channels | `PROVEN` behavior exists; cross-channel semantics require product/server contract |
| Party/shared XP | Beta | Canary party and multi-channel architecture | `PROVEN` party gameplay is per channel; global party presence is not established |
| Guild/VIP/friends presence | Beta | Canary global data model and client modules | `SUPPORTED`; exact cross-channel presence contract needs audit |
| Reporting/moderation surfaces | Later | current protocol features | `SUPPORTED`; product policy required |

## Navigation and action UI

| Capability | Priority | Evidence | Audit result |
|---|---|---|---|
| Main game viewport and panels | MPS | current game interface and target UI architecture | `PROVEN` required behavior; new UI is native Rust |
| Minimal health/mana/status UI | MPS | current interface/player stats | `PROVEN` |
| Chat input/output | MPS | current console | `PROVEN` |
| Inventory/container UI | MPS | current modules | `PROVEN` |
| Minimap | Beta | `game_minimap` | `PROVEN` user feature; source/provenance of map data needs design |
| Hotkeys and semantic input actions | MPS basic; Beta editor | current hotkey/action modules and target input architecture | `PROVEN` behavior required |
| Action bars and cooldown overlays | Beta | current action-bar module/tests | `PROVEN` behavior exists |
| Docking/layout persistence | Beta | accepted UI architecture | `SUPPORTED`; no Rust implementation/fixtures |
| DPI, ultrawide and accessibility | Beta | target architecture and legacy UI risks | `PROVEN` product requirement; acceptance matrix unresolved |
| Localization | Beta | current locale model and target UI | `SUPPORTED`; language/product set unresolved |

## Services and advanced features

| Capability | Priority | Evidence | Audit result |
|---|---|---|---|
| Market | Beta | Canary market packets and current client | `PROVEN` |
| Store/coins | Later | current protocol/module surfaces | `SUPPORTED`; commercial/product contract required |
| Prey/task hunt/bestiary/bosstiary | Later | Canary player domains and protocol | `PROVEN` server domains; exact client contract outside MPS |
| Wheel of Destiny / Monk / proficiency | Later | current profile features and maintained modules | `PROVEN` version-specific payloads exist |
| Forge/imbuements | Later | Canary includes and maintained features | `PROVEN` |
| Taskboard/Soul Seals | Later | current protocol feature flags | `PROVEN` packet families exist; exact contract/fixtures required |
| Houses | Later | Canary multi-channel data model | `PROVEN` per-channel physical state; client UX not MPS |
| Extensions | Later | ADR-0004 | `PROVEN` architecture decision; implementation intentionally deferred |

## Runtime product capabilities

| Capability | Priority | Audit result |
|---|---|---|
| Verified asset pack loading | MPS | `PROVEN` required; actual pack/importer inputs blocked by rights audit |
| Renderer diagnostics and frame-time metrics | MPS | `PROVEN` architecture requirement |
| Audio device and basic effects | Beta | `SUPPORTED`; exact asset/source inputs unresolved |
| Settings schema and local persistence | MPS basic; Beta full | `PROVEN` requirement |
| Crash-safe redacted diagnostics | Beta | `PROVEN` security requirement |
| Signed launcher/updater and rollback | Production | `PROVEN` production requirement; not MPS vertical slice |
| Sanitized replay/benchmark tooling | MPS engineering | `PROVEN` required to make progress without live server |

## Minimum playable slice recommendation

The first real gameplay milestone should include only:

1. Identity/account session through fake services first, then exact Platform contract;
2. character/world/gameplay-channel selection;
3. one game session through `protocol-canary` Current profile;
4. map/tiles, local player and basic creatures;
5. movement and basic use/attack commands;
6. essential player stats;
7. equipment/inventory and one container;
8. local/system chat;
9. minimal native Rust UI/input;
10. normal logout and relog to another advertised channel;
11. verified synthetic asset pack;
12. metrics and deterministic replay.

Market, action bars, minimap, social systems and modern feature families are intentionally outside the first vertical slice.

## Rejected product assumptions

- `REJECTED` new Rust modules should mirror legacy Lua modules one-to-one.
- `REJECTED` every existing modern Canary feature is required for first login/playability.
- `REJECTED` seamless live channel migration is required.
- `REJECTED` client prediction may decide authoritative combat, inventory or economy state.
