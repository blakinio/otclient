# Oteryn Rust Client Capability Matrix

Status cut: `main@67a6c9d726f7e70977803b028270475570210db0` pending independent post-remediation closure audit.  
This is a living planning matrix, not a release claim.

## Status rules

- `PROVEN` — required exact evidence exists for the bounded claim.
- `PARTIAL` — an owning foundation exists but the user workflow is incomplete.
- `SYNTHETIC_ONLY` — proven only with original synthetic fixtures/fakes.
- `UNKNOWN` — runtime/producer/legal evidence is missing.
- `BLOCKED` — a named dependency prevents safe work or claim.
- `ABSENT` — no implementation contract exists.
- `DEFERRED` — intentionally outside the selected release.

The coordinator updates rows only from merged code, exact CI/runtime evidence and accepted product decisions.

## 1. Foundation, governance and runtime

| Capability | State | Current evidence/boundary | Next owning package | Milestone |
|---|---|---|---|---|
| Pinned Rust workspace and supply-chain policy | PROVEN | Rust 1.94 workspace, locked metadata, strict Clippy, architecture and cargo-deny gates | maintain in integration tasks | all |
| Complete category dependency policy | PROVEN | post-W7 remediation replaced partial denylist with complete allow policy | architecture owner for new categories only | all |
| Technical generations, monotonic time and cancellation | PROVEN | `oteryn-foundation` | reuse; no second abstraction | all |
| Structured secret-safe diagnostics contracts | PROVEN | `oteryn-diagnostics` | future sink/support package | M4/M6 |
| Deterministic test support/fake time | PROVEN | `oteryn-test-support` | reuse in all packages | all |
| Windows event-loop/window shell | PARTIAL | bounded `winit` shell exists; interactive matrix incomplete | Windows shell/runtime acceptance | M1/M4 |
| Renderer device/surface ownership | PARTIAL | deterministic `wgpu` surface boundary; no world/UI passes | renderer resource/world packages | M2-M4 |
| Nonblocking technical worker shutdown | PROVEN | typed begin/poll shutdown remediation | extend to future workers | all |
| Safe project-owned secret lifetime contract | PROVEN | remediated bounded overwrite claims | extend to new secret owners | all |
| Settings schema/migrations | ABSENT | no typed settings system | `settings-core` sole producer | M3/M4 |
| Crash handling and support bundle | ABSENT | diagnostics contract only | diagnostics runtime/support package | M4/M6 |
| Replay and deterministic benchmark harness | ABSENT | architecture target only | replay/benchmark tools | M3-M6 |

## 2. Identity, directory and session lifecycle

| Capability | State | Current evidence/boundary | Next owning package | Milestone |
|---|---|---|---|---|
| OAuth Authorization Code + PKCE | SYNTHETIC_ONLY | fake browser/listener/HTTP security E2E | controlled deployment validation | M1 |
| Real browser loopback callback on Windows | UNKNOWN | no named interactive desktop evidence | P0 release/E2E then staging task | M1 |
| Exact deployed Identity/Gateway compatibility | UNKNOWN | repository contracts only | controlled staging E2E | M1 |
| Account generation/lifecycle | PARTIAL | one bounded bootstrap; token family consumed by ticket issuance | account relog/session design | M3/M4 |
| Strict Gateway protocol-v1 directory | SYNTHETIC_ONLY | bounded fake response and relation validation | real staging validation | M1 |
| World/character selection contracts | PROVEN | typed validated directory and explicit selection | native selection UI | M1/M4 |
| Native login and character-selection UX | ABSENT | technical environment-only surface | UI/auth feature packages | M4 |
| One-shot game-entry credential | PROVEN | non-clone/redacted/lifecycle tests | reuse | all |
| Controlled real Canary admission | UNKNOWN | production path fail-closed without exact deployment proof | staging admission task | M1 |
| Relog without full process restart | ABSENT | one bounded bootstrap only | account/game session lifecycle | M3/M4 |
| Reconnect policy | ABSENT | no gameplay session reconnect | session recovery package | M3/M4 |
| Multi-world/issuer routing | BLOCKED | Gateway v1 maps one configured world/issuer | producer contract change required | M5 |
| Gameplay channel selection | BLOCKED | reserved type; no producer directory contract | platform/gateway producer work | M5 |

## 3. Transport and Canary protocol

| Capability | State | Current evidence/boundary | Next owning package | Milestone |
|---|---|---|---|---|
| Bounded TCP ownership/I/O | PROVEN | connect/read/write/frame terminal-state tests | extend under same transport contract | all |
| Canary challenge/login/admission prefix | SYNTHETIC_ONLY | source-derived synthetic path through enter-world marker | real staging admission | M1 |
| Exact post-admission capability/opcode inventory | UNKNOWN | no normalized exhaustive matrix | P0 Canary discovery | P0 |
| Map description decoder | ABSENT | adapter stops before map description | protocol-map package | M2 |
| Floor/tile update decoding | ABSENT | no post-admission gameplay parser | protocol-map package | M2 |
| Creature add/update/remove decoding | ABSENT | none | protocol-entity package | M2/M3 |
| Item/appearance/effect/projectile decoding | ABSENT | none | protocol-world-visual package | M2/M3 |
| Player stats/skills/conditions decoding | ABSENT | none | protocol-player package | M3 |
| Movement command encoding and acknowledgements | ABSENT | no gameplay commands | protocol-movement package | M2/M3 |
| Look/use/move-item commands | ABSENT | none | protocol-interaction package | M3 |
| Attack/follow/combat commands and events | ABSENT | none | protocol-combat package | M3 |
| Inventory/equipment/container protocol | ABSENT | none | protocol-inventory package | M3 |
| Chat/channel/private/NPC protocol | ABSENT | none | protocol-chat package | M3 |
| Trade/depot/NPC commerce | UNKNOWN | exact server surface not normalized | P0 Canary/legacy inventories | M5 |
| Market and version-specific feature protocol | UNKNOWN | exact supported feature set not normalized | P0 Canary inventory then feature packages | M5 |
| Malformed gameplay packet/fuzz coverage | ABSENT | admission-only negative tests | parser fuzz programme | M2-M6 |
| Exact profile/build negotiation and update action | PARTIAL | initial Current profile fixed | compatibility registry/update UX | M4/M5 |

## 4. Game domain and simulation

| Capability | State | Current evidence/boundary | Next owning package | Milestone |
|---|---|---|---|---|
| Canonical gameplay IDs/entity handles | ABSENT | entry IDs exist; no gameplay entity/item/container IDs | game-domain contract producer | P1 |
| Closed `GameEvent` envelope | ABSENT | no post-admission domain event contract | game-domain contract producer | P1 |
| Closed `GameCommand` envelope | ABSENT | no semantic gameplay command contract | game-domain contract producer | P1 |
| Single-writer simulation runtime | ABSENT | technical app runtime only | simulation-core | P1/P2 |
| World/floor/chunk/tile state | ABSENT | none | world-state | M2 |
| Dynamic creature/entity storage | ABSENT | none | entity-state | M2/M3 |
| Player state/stats/conditions | ABSENT | none | player-state | M3 |
| Inventory/equipment/container state | ABSENT | none | inventory-state | M3 |
| Chat/social state | ABSENT | none | chat-state/social-state | M3/M4 |
| Combat/targeting/cooldown state | ABSENT | none | combat-state | M3 |
| Prediction/reconciliation | ABSENT | none; must remain server-authoritative | movement/simulation package | M3 |
| Immutable render snapshot | ABSENT | renderer has surface only | snapshot contract producer | P1/P2 |
| UI view models | ABSENT | no native UI framework | view-model contract producer | P1/P3 |
| Audio intents | ABSENT | none | audio contract producer | P1/P3 |
| Deterministic replayable domain tests | ABSENT | technical login only | simulation/replay test packages | M2-M6 |

## 5. Assets and resource runtime

| Capability | State | Current evidence/boundary | Next owning package | Milestone |
|---|---|---|---|---|
| Synthetic asset schema and deterministic compiler | PROVEN | typed IDs, pack v1, safe opened-object reads | preserve | all |
| Immutable pack open/verify/index/lookup | ABSENT | no runtime crate | asset-runtime contract/implementation | P1/M2 |
| Bounded async decode scheduling | ABSENT | none | asset-runtime decode layer | M2 |
| RGBA texture upload/resource handles | ABSENT | no renderer resource integration | renderer-resource | M2 |
| Sprite/appearance metadata representation | UNKNOWN | synthetic blob/RGBA slice only | P0 asset discovery and schema extension | M2 |
| Real Canary-compatible importer | ABSENT | no real formats/import | offline importer packages | M2-M5 |
| Production asset provenance/rights | UNKNOWN | no approved source/redistribution contract | P0 asset/legal output and owner decision | M2/M6 |
| Local user-owned import policy | UNKNOWN | not accepted | asset product/legal decision | M2/M4 |
| Pack signing/authenticated manifest | ABSENT | synthetic pack hashing only | launcher/update asset-security package | M4/M6 |
| Runtime cache/streaming/eviction | ABSENT | none | asset-runtime streaming | M3/M4 |
| Font/glyph resources | ABSENT | none | text/ui resource pipeline | M3/M4 |
| Audio resources/streaming | ABSENT | none | audio asset pipeline | M3/M4 |

## 6. Renderer and presentation

| Capability | State | Current evidence/boundary | Next owning package | Milestone |
|---|---|---|---|---|
| DX12 device/surface lifecycle | PARTIAL | compile/tests; limited interactive evidence | renderer acceptance/device recovery | M2/M4 |
| Render resource cache and handles | ABSENT | surface only | renderer-resource | P1/M2 |
| Camera/floor visibility extraction | ABSENT | none | world-renderer | M2 |
| Tile/item/creature sprite batching | ABSENT | none | world-renderer | M2 |
| Projectiles/effects/animations | ABSENT | none | effects-renderer | M2/M3 |
| Lighting/ambient/transparency | ABSENT | none | lighting-renderer | M3/M4 |
| Text shaping/glyph atlas | ABSENT | none | text-renderer | M3/M4 |
| UI render pass/clipping/scissor | ABSENT | none | ui-renderer | M3 |
| Minimap rendering | ABSENT | none | minimap feature | M4 |
| GPU memory budgets/eviction | ABSENT | none | renderer-resource/performance | M4/M6 |
| Device-loss recovery | ABSENT | none | renderer platform package | M4/M6 |
| Named scene/frame-time benchmarks | ABSENT | no performance evidence | benchmark programme | M2-M6 |

## 7. Native UI and user workflows

| Capability | State | Current evidence/boundary | Next owning package | Milestone |
|---|---|---|---|---|
| UI primitive/layout/focus/accessibility core | ABSENT | no Rust UI core | `ui-core` sole producer | P1/M3 |
| Reactive view-model binding/action routing | ABSENT | none | UI application contracts | P1/M3 |
| Login and error presentation | ABSENT | technical config only | auth UI feature | M4 |
| World/character selection | ABSENT | contract only | selection UI feature | M4 |
| Game viewport/HUD/status bars | ABSENT | none | gameplay HUD feature | M2/M3 |
| Inventory/equipment panels | ABSENT | none | inventory UI feature | M3 |
| Container windows/drag-drop | ABSENT | none | container UI + input feature | M3 |
| Chat console/channels | ABSENT | none | chat UI feature | M3 |
| Battle list/targeting | ABSENT | none | combat UI feature | M3 |
| Action bars/hotkeys/cooldowns | ABSENT | none | action-bar feature | M3/M4 |
| Minimap/map controls | ABSENT | none | minimap feature | M4 |
| NPC/trade/market/feature panels | UNKNOWN | exact required feature set pending | feature-specific packages | M5 |
| Docking/layout persistence | ABSENT | none | UI shell/settings | M4 |
| High-DPI and IME acceptance | PARTIAL | platform research/shell only | UI platform acceptance | M4 |
| Localization | ABSENT | none | localization core and feature strings | M4/M5 |
| Accessibility tree/navigation | ABSENT | architecture target only | UI core/accessibility | M4/M6 |
| Developer UI inspector | ABSENT | none | UI diagnostics | M4/M6 |

## 8. Input and audio

| Capability | State | Current evidence/boundary | Next owning package | Milestone |
|---|---|---|---|---|
| Normalized physical input state | ABSENT | window events only | input-core | P1/M2 |
| Semantic action contexts/bindings | ABSENT | none | input-actions | P1/M2 |
| Movement/camera actions | ABSENT | none | gameplay input feature | M2 |
| Mouse picking/context actions | ABSENT | none | viewport interaction | M3 |
| Drag/drop and capture | ABSENT | none | UI/input integration | M3 |
| Configurable hotkeys/conflict handling | ABSENT | none | input settings | M3/M4 |
| Gamepad/accessibility alternatives | ABSENT | none | input accessibility | M4/M6 |
| Audio backend/device lifecycle | ABSENT | none | audio-core | P1/M3 |
| UI/game/positional sound mixing | ABSENT | none | audio features | M3/M4 |
| Voice budget/prioritization | ABSENT | none | audio runtime | M4 |
| Device replacement/recovery | ABSENT | none | audio platform acceptance | M4/M6 |

## 9. Product, operations and release

| Capability | State | Current evidence/boundary | Next owning package | Milestone |
|---|---|---|---|---|
| Controlled staging technical-login runbook | ABSENT | no named deployment evidence | P0 release/E2E then M1 task | M1 |
| Minimum-visible-world E2E | ABSENT | no gameplay | P2 integration E2E | M2 |
| Core gameplay scenario suite | ABSENT | no gameplay | P3 E2E | M3 |
| Multi-hour soak and network-loss scenarios | ABSENT | none | reliability programme | M4/M6 |
| Launcher/install/repair | ABSENT | architecture target only | launcher programme | M4/M6 |
| Signed update manifest/download/rollback | ABSENT | none | updater/security package | M4/M6 |
| Packaging/signing/release channels | ABSENT | none | release engineering | M4/M6 |
| Windows version/GPU/driver support matrix | UNKNOWN | CI compile only | P0 release inventory then acceptance | M4/M6 |
| Fuzzing of external parsers | ABSENT | negative tests only | security/fuzz programme | M2-M6 |
| Performance budgets and regression gates | ABSENT | none | benchmark/performance programme | M2-M6 |
| Memory/resource leak evidence | ABSENT | none | soak/profiling programme | M3-M6 |
| Privacy/telemetry decision | UNKNOWN | diagnostics contracts only | product/security decision | M4/M6 |
| Support/rollback/incident procedures | ABSENT | none | operations | M6 |
| Approved release candidate scenarios | ABSENT | none | final validation | M6 |

## 10. Required P0 outputs before implementation authorization

P0 must replace the major `UNKNOWN` areas with exact evidence:

1. Canary post-admission protocol and feature inventory with source/revision paths and fixture feasibility.
2. Legacy/original user workflow parity inventory without copying implementation or assets.
3. Asset source/import/runtime/provenance decision matrix.
4. Windows UI/input/audio/accessibility acceptance inventory.
5. Staging, E2E, performance, packaging and release evidence plan.
6. Coordinator aggregation that marks release-required versus deferred capabilities and proposes the smallest P1 contract producers.

No P0 worker changes Rust source or claims implementation readiness.
