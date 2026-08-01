# Oteryn Rust Client Capability Matrix

Status cut: `main@6808d8a9dd5a24a29c5ac96fe35bb463fe4da34b` after all five P0 reports and separate lifecycle archives merged.  
P0 evidence: Canary #140/#150, legacy #141/#149, assets #142/#148, UX/input/audio #143/#147, release/E2E #144/#146.  
Remediation status: `OTC2-AUD-001` through `OTC2-AUD-004` remain closed within their documented boundaries.  
This is a living planning matrix and scope contract, not a deployment or release claim.

## Status rules

- `PROVEN` — exact evidence exists for the bounded claim.
- `PARTIAL` — an owning foundation or accepted evidence exists, but implementation/runtime proof is incomplete.
- `SYNTHETIC_ONLY` — proven only with project-original synthetic fixtures/fakes.
- `UNKNOWN` — required runtime/producer/legal evidence is not yet known.
- `BLOCKED` — a named dependency or owner decision prevents safe implementation/claim.
- `ABSENT` — no implementation contract exists.
- `DEFERRED` — intentionally outside the selected release scope.

## Release-class rules

- `RELEASE_REQUIRED` — required for the named milestone/release path.
- `LATER` — not required for the current minimum path; reconsider at the named milestone.
- `OWNER_DECISION_NEEDED` — product, legal, security, operations or release owner must choose/approve.

Evidence inventory, source declarations or test methodology do not prove deployed compatibility or implemented product behavior.

## 1. Foundation, governance and runtime

| Capability | State | Release class | Current evidence/boundary | Next owner | Milestone |
|---|---|---|---|---|---|
| Pinned Rust workspace and supply-chain policy | PROVEN | RELEASE_REQUIRED | Rust 1.94, locked metadata, strict Clippy, architecture and cargo-deny gates | maintain in every integration task | all |
| Complete category dependency policy | PROVEN | RELEASE_REQUIRED | post-W7 allow policy and architecture checker | architecture owner for new categories | all |
| Technical generations, monotonic time and cancellation | PROVEN | RELEASE_REQUIRED | `foundation` | reuse; no second abstraction | all |
| Structured secret-safe diagnostics contracts | PROVEN | RELEASE_REQUIRED | `diagnostics` | later sink/support package | M4/M6 |
| Deterministic test support/fake time | PROVEN | RELEASE_REQUIRED | `test-support` | reuse | all |
| Windows event-loop/window shell | PARTIAL | RELEASE_REQUIRED | bounded winit shell; P0 accepted real desktop/DPI/IME evidence matrix but no interactive proof | Windows platform acceptance | M1/M4 |
| Renderer device/surface ownership | PARTIAL | RELEASE_REQUIRED | deterministic wgpu boundary; no resources/world/UI passes | renderer-resource/world packages | M2-M4 |
| Nonblocking technical worker shutdown | PROVEN | RELEASE_REQUIRED | typed begin/poll shutdown | preserve | all |
| Project-owned secret lifetime invariant | PROVEN | RELEASE_REQUIRED | immutable callback target and cleared rejected direct credentials; external copies remain outside claim | preserve in identity/platform/session | M1 |
| Settings schema/migrations | ABSENT | RELEASE_REQUIRED | P0 UX requires typed settings but no producer exists | settings-core after P1 | M4 |
| Crash handling/support bundle | ABSENT | RELEASE_REQUIRED | diagnostics contract only; P0 release evidence plan accepted | diagnostics runtime/support | M4/M6 |
| Replay/deterministic benchmark harness | ABSENT | RELEASE_REQUIRED | scenario/evidence classes accepted in P0 | replay/benchmark tools | M2-M6 |

## 2. Identity, directory and session lifecycle

| Capability | State | Release class | Current evidence/boundary | Next owner | Milestone |
|---|---|---|---|---|---|
| OAuth Authorization Code + PKCE | SYNTHETIC_ONLY | RELEASE_REQUIRED | fake browser/listener/HTTP security E2E | controlled deployment validation | M1 |
| Real browser loopback callback on Windows | UNKNOWN | RELEASE_REQUIRED | P0 release plan defines evidence; no named interactive desktop run | controlled M1 staging | M1 |
| Exact deployed Identity/Gateway compatibility | UNKNOWN | RELEASE_REQUIRED | repository contracts only | controlled M1 staging | M1 |
| Account generation/lifecycle | PARTIAL | RELEASE_REQUIRED | one bounded bootstrap | account relog/session design | M3/M4 |
| Strict Gateway protocol-v1 directory | SYNTHETIC_ONLY | RELEASE_REQUIRED | bounded fake response and relation validation | real staging validation | M1 |
| World/character selection contracts | PROVEN | RELEASE_REQUIRED | typed validated directory and explicit selection | native selection UI later | M1/M4 |
| Native login/selection UX | ABSENT | RELEASE_REQUIRED | P0 UX requirements accepted; no Rust UI core | UI producer wave after P1 | M4 |
| One-shot game-entry credential | PROVEN | RELEASE_REQUIRED | bounded non-cloneable redacted owner | preserve; real Canary acceptance separate | M1 |
| Controlled real Canary admission | BLOCKED | RELEASE_REQUIRED | technical path exists but exact deployed cut/environment/account are not named | operations/security owner then staging task | M1 |
| Relog without full process restart | ABSENT | RELEASE_REQUIRED | P0 daily workflow requires it | account/game-session lifecycle | M4 |
| Reconnect policy | ABSENT | RELEASE_REQUIRED | P0 recovery scenarios accepted | session recovery | M4 |
| Multi-world/issuer routing | BLOCKED | LATER | Gateway v1 maps one configured world/issuer | producer contract change | M5 |
| Gameplay channel selection | BLOCKED | LATER | reserved type; no producer directory contract | producer change | M5 |

## 3. Transport and Canary protocol

| Capability | State | Release class | Current evidence/boundary | Next owner | Milestone |
|---|---|---|---|---|---|
| Bounded TCP ownership/I/O | PROVEN | RELEASE_REQUIRED | connect/read/write/frame terminal-state tests | preserve | all |
| Canary challenge/login/admission prefix | SYNTHETIC_ONLY | RELEASE_REQUIRED | source-derived synthetic path through ordered admission | real staging admission | M1 |
| Exact post-admission capability inventory | PARTIAL | RELEASE_REQUIRED | P0 pins `blakinio/canary@bc0068ab…`, Canary 3.6.1/client 1525/Current and capability families; deployment equality and generated numeric index missing | P1 CANARY-SOURCE-INDEX | P1/M2 |
| Exact generated opcode/layout/source index | ABSENT | RELEASE_REQUIRED | P0 forbids handwritten tables and defines generator fields/fixtures | P1 CANARY-SOURCE-INDEX | P1 |
| Exact post-admission bootstrap order fixtures | UNKNOWN | RELEASE_REQUIRED | source family known; controlled trace/fixture execution missing | P1 index then protocol bootstrap | M2 |
| Map/floor/tile decoding | ABSENT | RELEASE_REQUIRED | source-backed family and package seam accepted | protocol-canary-map after game contract/index | M2 |
| Creature/entity add/update/remove decoding | ABSENT | RELEASE_REQUIRED | source-backed family accepted | protocol-canary-entity | M2/M3 |
| Item/appearance/effect/projectile decoding | ABSENT | RELEASE_REQUIRED | source families accepted; approved appearance contract missing | protocol world-visual after assets | M2/M3 |
| Player stats/skills/conditions decoding | ABSENT | RELEASE_REQUIRED | source family accepted | protocol-canary-player | M3 |
| Movement command encoding/acknowledgements | ABSENT | RELEASE_REQUIRED | source family accepted | protocol-canary-movement | M2/M3 |
| Look/use/move-item commands | ABSENT | RELEASE_REQUIRED | source family accepted | protocol-canary-items/interactions | M3 |
| Attack/follow/combat | ABSENT | RELEASE_REQUIRED | source family accepted | protocol-canary-combat | M3 |
| Inventory/equipment/container protocol | ABSENT | RELEASE_REQUIRED | source family accepted | protocol-canary-items/containers | M3 |
| Chat/channel/private/NPC protocol | ABSENT | RELEASE_REQUIRED | source family accepted | protocol-canary-chat | M3 |
| Social/party/guild/VIP protocol | ABSENT | LATER | source-backed; daily/product scope not yet selected | feature packages | M4/M5 |
| Trade/depot/NPC commerce | PARTIAL | LATER | source-backed families and parity scenarios accepted; layouts/runtime unimplemented | bounded feature packages | M5 |
| Market and modern feature protocol | PARTIAL | LATER | Current flags prove support at inspected cut; deployment/product selection unknown | per-family packages | M5 |
| Prey/taskboard/bestiary/forge/wheel/vocation systems | PARTIAL | LATER | source-backed at inspected cut; high drift risk and no release selection | per-family packages | M5 |
| Operational/admin/report paths | PARTIAL | OWNER_DECISION_NEEDED | declarations exist but are not player requirements | product/security classification | M5/M6 |
| Malformed gameplay packet/fuzz coverage | ABSENT | RELEASE_REQUIRED | P0 negative corpus strategy accepted | each parser + fuzz programme | M2-M6 |
| Exact profile/build negotiation/update action | PARTIAL | RELEASE_REQUIRED | initial Current profile fixed; exact deployed build/support registry absent | compatibility registry/update UX | M4/M5 |

## 4. Game domain and simulation

| Capability | State | Release class | Current evidence/boundary | Next owner | Milestone |
|---|---|---|---|---|---|
| Canonical gameplay IDs/entity handles | ABSENT | RELEASE_REQUIRED | sole-producer invariant accepted | P1 GAME-DOMAIN-CONTRACT | P1 |
| Closed `GameEvent` envelope | ABSENT | RELEASE_REQUIRED | minimum semantic family derived from P0 | P1 GAME-DOMAIN-CONTRACT | P1 |
| Closed `GameCommand` envelope | ABSENT | RELEASE_REQUIRED | minimum semantic family derived from P0 | P1 GAME-DOMAIN-CONTRACT | P1 |
| Single-writer simulation runtime | ABSENT | RELEASE_REQUIRED | architecture and scenario requirements accepted | post-P1 simulation-core | P2 |
| World/floor/chunk/tile state | ABSENT | RELEASE_REQUIRED | P0 map scenarios accepted | world-state | M2 |
| Dynamic creature/entity storage | ABSENT | RELEASE_REQUIRED | P0 entity scenarios accepted | entity-state | M2/M3 |
| Player state/stats/conditions | ABSENT | RELEASE_REQUIRED | P0 scenarios accepted | player-state | M3 |
| Inventory/equipment/container state | ABSENT | RELEASE_REQUIRED | P0 scenarios accepted | inventory-state | M3 |
| Chat/social state | ABSENT | RELEASE_REQUIRED | chat required M3; broader social later | chat-state/social-state | M3/M4 |
| Combat/targeting/cooldown state | ABSENT | RELEASE_REQUIRED | P0 core gameplay scenarios accepted | combat-state | M3 |
| Prediction/reconciliation | ABSENT | RELEASE_REQUIRED | server-authoritative boundary accepted | movement/simulation | M3 |
| Immutable render snapshot | ABSENT | RELEASE_REQUIRED | sole-producer requirement accepted | post-P1 simulation/snapshot producer | P2/M2 |
| UI view models/common semantic UI actions | ABSENT | RELEASE_REQUIRED | P0 decomposition accepted | post-P1 UI/common-action producer | P2/P3 |
| Audio intents | ABSENT | RELEASE_REQUIRED | P0 requirements accepted | post-P1 audio-core | P3 |
| Deterministic replayable domain tests | ABSENT | RELEASE_REQUIRED | scenario/evidence catalogue accepted | simulation/replay packages | M2-M6 |

## 5. Assets and resource runtime

| Capability | State | Release class | Current evidence/boundary | Next owner | Milestone |
|---|---|---|---|---|---|
| Synthetic asset schema/compiler | PROVEN | RELEASE_REQUIRED | typed IDs, pack v1, deterministic safe compiler | preserve as test infrastructure | all |
| Immutable pack open/verify/index/lookup | ABSENT | RELEASE_REQUIRED | P0 threat model/contract accepted | P1 ASSET-PACK-RUNTIME | P1/M2 |
| Generation-stable logical asset handles | ABSENT | RELEASE_REQUIRED | P0 runtime requirement accepted | P1 ASSET-PACK-RUNTIME | P1/M2 |
| Bounded async decode/cache | ABSENT | RELEASE_REQUIRED | P0 package order accepted | post-P1 asset-decode | M2 |
| RGBA texture upload/resource handles | ABSENT | RELEASE_REQUIRED | no renderer resource integration | renderer-resource | M2 |
| Appearance/sprite/effect metadata | PARTIAL | RELEASE_REQUIRED | P0 identifies required normalized families and exact-profile dependency; approved production representation/source missing | appearance contract after P1/index/owner input | M2 |
| Real Canary-compatible importer | ABSENT | RELEASE_REQUIRED | P0 importer families/threat boundaries accepted | approved source-family importer | M2-M5 |
| Production asset provenance/rights | BLOCKED | OWNER_DECISION_NEEDED | rights matrix exists; no approved production source/local-import/redistribution decision | owner/legal | M2/M6 |
| Local user-owned import policy | BLOCKED | OWNER_DECISION_NEEDED | options documented; not accepted | owner/legal/product | M2/M4 |
| Pack signing/authenticated manifest | ABSENT | RELEASE_REQUIRED | hashing only; signing/release policy unresolved | launcher/update asset security | M4/M6 |
| Runtime streaming/eviction | ABSENT | RELEASE_REQUIRED | methodology accepted | asset runtime streaming | M3/M4 |
| Font/glyph/text resources | ABSENT | RELEASE_REQUIRED | P0 requirements accepted; library/rights decision missing | text-resource producer | M3/M4 |
| Audio resources/streaming | ABSENT | RELEASE_REQUIRED | P0 requirements accepted; rights/backend missing | audio-resource | M3/M4 |

## 6. Renderer and presentation

| Capability | State | Release class | Current evidence/boundary | Next owner | Milestone |
|---|---|---|---|---|---|
| DX12 device/surface lifecycle | PARTIAL | RELEASE_REQUIRED | compile/tests; no named desktop/device-loss evidence | renderer platform acceptance | M2/M4 |
| Render resource cache/handles | ABSENT | RELEASE_REQUIRED | P0 dependencies accepted | renderer-resource after asset handles | M2 |
| Camera/floor visibility extraction | ABSENT | RELEASE_REQUIRED | scenario requirements accepted | world-renderer | M2 |
| Tile/item/creature sprite batching | ABSENT | RELEASE_REQUIRED | requirements accepted | world-renderer | M2 |
| Projectiles/effects/animations | ABSENT | RELEASE_REQUIRED | requirements accepted | effects-renderer | M2/M3 |
| Lighting/ambient/transparency | ABSENT | RELEASE_REQUIRED | requirements accepted | lighting-renderer | M3/M4 |
| Text shaping/glyph atlas | ABSENT | RELEASE_REQUIRED | P0 text requirements accepted | text-renderer | M3/M4 |
| UI render pass/clipping/scissor | ABSENT | RELEASE_REQUIRED | P0 UI-core requirements accepted | ui-renderer | M3 |
| Minimap rendering | ABSENT | RELEASE_REQUIRED | daily workflow accepted | minimap | M4 |
| GPU memory budgets/eviction | ABSENT | RELEASE_REQUIRED | measurement methodology accepted; thresholds not selected | performance owner/renderer | M4/M6 |
| Device-loss recovery | ABSENT | RELEASE_REQUIRED | scenario accepted | renderer platform | M4/M6 |
| Named scene/frame-time benchmarks | ABSENT | RELEASE_REQUIRED | P0 methodology accepted | benchmark programme | M2-M6 |

## 7. Native UI and user workflows

| Capability | State | Release class | Current evidence/boundary | Next owner | Milestone |
|---|---|---|---|---|---|
| UI primitive/layout/focus/accessibility core | ABSENT | RELEASE_REQUIRED | P0 producer/consumer decomposition and synthetic harness accepted | post-P1 ui-core | M3/M4 |
| Common view-model/semantic UI action envelope | ABSENT | RELEASE_REQUIRED | must coordinate with merged game-domain/resource contracts | post-P1 common-action producer | P2/P3 |
| Login/error presentation | ABSENT | RELEASE_REQUIRED | requirements accepted | auth UI feature | M4 |
| World/character selection UI | ABSENT | RELEASE_REQUIRED | workflows accepted | selection UI | M4 |
| Game viewport/HUD/status | ABSENT | RELEASE_REQUIRED | minimum visible-world/core scenarios accepted | gameplay HUD | M2/M3 |
| Inventory/equipment panels | ABSENT | RELEASE_REQUIRED | scenarios accepted | inventory UI | M3 |
| Container windows/drag-drop | ABSENT | RELEASE_REQUIRED | scenarios accepted | container UI/input | M3 |
| Chat console/channels | ABSENT | RELEASE_REQUIRED | scenarios accepted | chat UI | M3 |
| Battle list/targeting | ABSENT | RELEASE_REQUIRED | scenarios accepted | combat UI | M3 |
| Action bars/hotkeys/cooldowns | ABSENT | RELEASE_REQUIRED | daily/core scenarios accepted | action-bar | M3/M4 |
| Minimap/map controls | ABSENT | RELEASE_REQUIRED | daily scenario accepted | minimap | M4 |
| NPC/trade/market/modern panels | ABSENT | LATER | conditional M5 scenario families accepted | per-feature UI | M5 |
| Docking/layout persistence | ABSENT | RELEASE_REQUIRED | daily expectation accepted | UI shell/settings | M4 |
| High-DPI/IME/clipboard/focus/capture | PARTIAL | RELEASE_REQUIRED | P0 acceptance matrix proven as requirements; interactive runtime proof missing | Windows UI acceptance | M4 |
| Localization | ABSENT | RELEASE_REQUIRED | expansion/string contract requirements accepted | localization core/features | M4/M5 |
| Accessibility tree/navigation | ABSENT | RELEASE_REQUIRED | P0 contract/harness requirements accepted | ui-core/platform bridge | M4/M6 |
| Developer UI inspector | ABSENT | LATER | useful but not minimum release | UI diagnostics | M6 |

## 8. Input and audio

| Capability | State | Release class | Current evidence/boundary | Next owner | Milestone |
|---|---|---|---|---|---|
| Normalized physical input state | ABSENT | RELEASE_REQUIRED | P0 contract requirements accepted | P1 INPUT-ACTIONS | P1/M2 |
| Semantic actions/contexts/bindings | ABSENT | RELEASE_REQUIRED | P0 precedence/conflict/lifecycle requirements accepted | P1 INPUT-ACTIONS | P1/M2 |
| Movement/camera action mapping | ABSENT | RELEASE_REQUIRED | waits for input and game commands | gameplay input feature | M2 |
| Mouse picking/context actions | ABSENT | RELEASE_REQUIRED | waits for snapshots/UI | viewport interaction | M3 |
| Drag/drop and capture | ABSENT | RELEASE_REQUIRED | requirements accepted | UI/input integration | M3 |
| Configurable hotkeys/conflicts | ABSENT | RELEASE_REQUIRED | contract requirements accepted; persistence later | input settings | M3/M4 |
| Gamepad/accessibility alternatives | ABSENT | LATER | extension seam only; support matrix not selected | input accessibility | M4/M6 |
| Audio intent/category/device contract | ABSENT | RELEASE_REQUIRED | P0 contract/harness requirements accepted | post-P1 audio-core | M3 |
| UI/game/positional mixing | ABSENT | RELEASE_REQUIRED | requirements accepted | audio features | M3/M4 |
| Voice budget/prioritization | ABSENT | RELEASE_REQUIRED | methodology accepted | audio runtime | M4 |
| Device replacement/recovery | ABSENT | RELEASE_REQUIRED | scenario accepted | audio platform acceptance | M4/M6 |

## 9. Product, operations and release

| Capability | State | Release class | Current evidence/boundary | Next owner | Milestone |
|---|---|---|---|---|---|
| Controlled staging technical-login runbook | PARTIAL | RELEASE_REQUIRED | P0 evidence contract/scenario exists; environment/account/cut missing | owner/operations then M1 staging task | M1 |
| Minimum-visible-world E2E | ABSENT | RELEASE_REQUIRED | exact start/actions/observables defined | P2 vertical slice E2E | M2 |
| Core gameplay scenario suite | ABSENT | RELEASE_REQUIRED | P0 M3 catalogue accepted | P3 E2E | M3 |
| Multi-hour soak/network-loss scenarios | PARTIAL | RELEASE_REQUIRED | methodology/scenarios accepted; runtime absent | reliability programme | M4/M6 |
| Launcher/install/repair | ABSENT | RELEASE_REQUIRED | scenario/dependency map accepted | launcher programme | M4/M6 |
| Signed update/download/rollback | ABSENT | RELEASE_REQUIRED | scenario accepted; signing/channel decisions missing | updater/security | M4/M6 |
| Packaging/signing/release channels | BLOCKED | OWNER_DECISION_NEEDED | process requirements accepted; credentials/channel not selected | release/security owner | M4/M6 |
| Windows version/GPU/driver support matrix | PARTIAL | OWNER_DECISION_NEEDED | candidate dimensions accepted; final supported matrix and interactive evidence missing | product owner + Windows acceptance | M4/M6 |
| Fuzzing of external parsers | ABSENT | RELEASE_REQUIRED | negative strategy accepted | parser owners/security | M2-M6 |
| Performance budgets/regression gates | PARTIAL | OWNER_DECISION_NEEDED | measurement methodology accepted; final thresholds require baselines/owner | performance/product owner | M2-M6 |
| Memory/resource leak evidence | ABSENT | RELEASE_REQUIRED | soak/profiling methodology accepted | reliability programme | M3-M6 |
| Privacy/telemetry/support-data policy | UNKNOWN | OWNER_DECISION_NEEDED | diagnostics boundary exists; policy not selected | privacy/security owner | M4/M6 |
| Support/rollback/incident procedures | PARTIAL | RELEASE_REQUIRED | release evidence contract accepted; operations implementation absent | operations | M6 |
| Approved release candidate scenarios | ABSENT | RELEASE_REQUIRED | scenario families accepted; no candidate/runtime evidence | final validation | M6 |

## 10. Normalized release scope after P0

### RELEASE_REQUIRED

- M1: exact deployed identity/gateway/Canary cut, controlled environment/account, real Windows browser callback and admission evidence.
- M2: game-domain contracts, generated Canary source index/fixtures, bootstrap/map/entity/movement/basic player/item protocol, single-writer world state, immutable snapshot, verified asset runtime/approved minimum scene, renderer resources/world pass, semantic movement input and minimum viewport/HUD observables.
- M3: combat, inventory/equipment/containers, chat/NPC basics, interaction commands, core UI panels, settings/relog foundations and audio intents where required by scenarios.
- M4: native daily UX, reconnect/recovery, minimap/hotkeys/layout persistence, DPI/IME/accessibility, device recovery, launcher/update/rollback and accepted performance/soak gates.
- M6: signing/release/support/privacy/fuzz/incident hardening and approved release-candidate evidence.

### LATER

Default M5 unless explicitly promoted by product scope:

- market, depot/stash, trade, advanced NPC commerce;
- quests, prey/tasks/taskboard, bestiary/bosstiary/cyclopedia;
- imbuement, forge, weapon proficiency, vocation-specific/Monk, soul seals, skill wheel/gems;
- staff/admin/report paths;
- gamepad and developer UI tooling.

Each later family remains one bounded protocol/domain/UI/scenario package, never one mega-feature parser.

### OWNER_DECISION_NEEDED

- exact deployed Canary revision/configuration/build and supported profile registry;
- approved staging environment and disposable account/character;
- production asset source, local-import and redistribution policy;
- final Windows desktop/GPU/driver/input/audio support matrix;
- product performance/resource thresholds;
- telemetry/privacy/support-data policy;
- signing credentials, release channel, rollback authority and final M5 feature subset.

These decisions block deployment/release claims, not the bounded synthetic/source P1 contract spine.

## 11. Accepted P1 contract spine

P1 plan: `WAVE_P1_CONTRACT_SPINE.md`.

| Order | Package | Public responsibility | State before P1 | Required dependency |
|---|---|---|---|---|
| 1 | CANARY-SOURCE-INDEX | deterministic exact-source evidence/fixture metadata; no runtime types | ABSENT | accepted exact source cut |
| 2 | GAME-DOMAIN-CONTRACT | canonical IDs/handles plus closed `GameEvent`/`GameCommand` | ABSENT | foundation only |
| 3 | ASSET-PACK-RUNTIME | synthetic-v1 immutable open/verify/index/lookup and logical handles | ABSENT | asset-types/compiler read-only |
| 4 | INPUT-ACTIONS | normalized physical events and semantic action/context contracts | ABSENT | foundation only |

Only one shared integration lease holder may modify workspace/lockfile/architecture paths. Game-domain is the first merged public gameplay contract. Asset-runtime and input-actions are independent producers but integrate serially. No simulation, protocol gameplay parser, UI/audio producer, renderer resource or app composition is authorized in P1.

## 12. P0 completion result

P0 is complete:

- all five evidence reports and separate archives are merged;
- major unknown areas are narrowed or assigned named blockers/owner decisions;
- exact source evidence is separated from deployment proof;
- release-required/later/owner-decision capability classes are explicit;
- the smallest P1 producer wave, merge order, owned/shared paths and prompts are accepted;
- no P0 implementation was introduced.
