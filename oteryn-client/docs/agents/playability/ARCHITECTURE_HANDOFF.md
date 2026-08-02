# Full-Playability Architecture Handoff

Purpose: compact required architecture context for every future Oteryn Rust client worker.
Authority: `oteryn-client/docs/architecture/ARCHITECTURE.md`, accepted ADRs, live task ownership and exact Git state override this summary.

## 1. Product boundary

The greenfield client lives under:

```text
oteryn-client/
```

The executable lives under:

```text
oteryn-client/apps/client/
```

Initial production target is Windows desktop. Initial game-server compatibility is the project-owned Canary adapter. The target ecosystem is Oteryn.

The legacy C++/Lua/OTUI client is never a Rust runtime dependency. It is read-only behavioural and migration evidence.

## 2. Existing workspace and current responsibility

| Package/path | Category | Current responsibility | Current boundary |
|---|---|---|---|
| `crates/foundation` | foundation | generations, monotonic time, cancellation and primitive errors | no product/domain policy |
| `crates/diagnostics` | diagnostics | bounded structured diagnostics and redaction | no global sink/subscriber |
| `crates/test-support` | test-support | deterministic builders/fake time using foundation | test-only |
| `crates/account-session` | account-session | account generation/lifecycle marker | no bearer persistence |
| `crates/world-directory` | world-directory | validated worlds/characters and explicit selection | no gameplay-channel inference |
| `crates/game-session` | game-session | one-shot entry credential/request/result lifecycle | no wire layout |
| `crates/game-domain` | game-domain | canonical session-scoped gameplay IDs/handles and closed v1 `GameEvent`/`GameCommand` envelopes | no Canary, simulation, renderer, UI or app policy |
| `crates/platform` | platform | strict Platform ticket/Gateway HTTP boundary | no browser state or game wire |
| `crates/identity` | identity | OAuth Authorization Code + PKCE transaction | no passwords, UI or game wire |
| `crates/protocol-core` | protocol-core | bounded wire primitives and parser errors | protocol-neutral only |
| `crates/transport` | transport | bounded TCP ownership and I/O lifecycle | no domain/UI policy |
| `crates/protocol-canary` | protocol-canary | exact bounded Current-profile admission mapping | stops before gameplay decode; runtime source descriptors must be aligned with the P1 generated `bc0068ab…` index before P2 parser work |
| `tools/canary-protocol-index` | tool/evidence | deterministic exact-source opcode/dispatch/feature index for inspected Canary Current cut | no wire-layout or deployment-equality claim |
| `crates/app-runtime` | app-runtime | technical-login orchestration, generations and worker shutdown | no duplicate backend contracts |
| `crates/renderer` | renderer | window-surface/device ownership boundary | no world rendering yet |
| `crates/asset-types` | asset-types | synthetic typed asset/pack schema | no runtime mounting |
| `crates/asset-runtime` | asset-runtime | immutable verified synthetic-v1 pack open/index/lookup and generation-fenced handles | no media decode, GPU upload, loose files or production compatibility |
| `crates/input-actions` | input-actions | framework-neutral physical events and semantic action/context/binding lifecycle | no platform adapter, default keymap, gameplay mapping, UI or settings |
| `tools/asset-compiler` | tool | deterministic safe synthetic pack compiler | no production importer/runtime |
| `apps/client` | app | Windows shell, renderer and technical-login composition | no gameplay/domain/UI framework |
| `tests/integration/technical-login` | integration-test | fake technical-login E2E | no real deployment proof |
| `tests/security/auth` | security-test | authentication negative/security evidence | no production credential use |
| `tools/architecture-check` | tool | complete category edge allow policy | architecture gate only |

Do not assume the table is current without checking live manifests and task records.

## 3. Normative runtime composition

```text
Application shell
  |-- account/identity services
  |-- game session/protocol adapter
  |-- asset runtime
  |-- input and audio platform services
  v
Game command/event boundary
  v
Single-writer deterministic game domain/simulation
  |-- immutable render snapshots -> renderer
  |-- bounded view models -> UI
  `-- audio intents -> audio system
```

The missing shared spine for gameplay must be produced deliberately. No protocol, renderer or UI worker may invent private replacements for public game IDs, `GameEvent`, `GameCommand`, render snapshots, view-model/action contracts or asset-runtime handles.

## 4. Required ownership rules

### Application/event thread

Owns:

- Windows event loop and window lifetime;
- raw OS event ingestion;
- frame orchestration and presentation;
- application state transitions that require OS coordination.

Must not:

- block on network, filesystem, decoding or worker joins;
- own authoritative game state;
- parse gameplay packets.

### Simulation owner

Owns:

- the only mutable session game state;
- deterministic ordered application of validated game events;
- local semantic commands and explicitly bounded prediction;
- publication of generation-stable render/UI snapshots.

Must not:

- own sockets, GPU resources or widget trees;
- contain Canary packet fields.

### Protocol and transport

Transport owns bytes, connection lifetime, bounded I/O, framing state and cancellation. Protocol adapters own exact supported wire mapping and translate only to/from merged domain contracts.

They must not mutate the game world, create UI strings from raw server text or call renderer/input code.

### Renderer

Owns device/surface/resource caches, extraction, culling, batching and GPU submission from immutable snapshots.

It must not own authoritative entities, protocol semantics or feature business logic.

### UI

Owns retained presentation state, focus, layout, accessibility, docking and view-model rendering. Features emit semantic actions through a merged action boundary.

`ui-core` may provide primitives only and must not depend on concrete inventory/chat/market features.

### Assets

Offline tools validate provenance, normalize input and build immutable packs. Runtime opens verified packs, exposes logical handles and schedules bounded decode/upload away from frame-critical work.

Runtime must not read arbitrary loose source files or silently accept unsigned/unsupported production content.

## 5. Dependency direction

Expected direction for gameplay work:

```text
foundation
  <- diagnostics / test-support
  <- game-domain contracts
  <- asset-types / asset-runtime contracts

game-domain contracts
  <- protocol adapters
  <- simulation/domain state
  <- feature state crates

asset runtime contracts
  <- renderer resource layer
  <- UI/text/audio resource consumers

simulation snapshots/view models/actions
  <- renderer / UI / input mapping / audio intents

merged services and feature composition
  <- app-runtime
  <- apps/client
```

Forbidden examples:

- domain -> Canary packet types;
- transport -> renderer/UI;
- renderer -> protocol or feature state mutation;
- UI core -> inventory/chat/market implementation;
- feature crate -> another feature's private storage;
- any greenfield crate -> legacy client source/module runtime.

The architecture checker is authoritative for declared category edges, but workers still verify semantic ownership.

## 6. Trust boundaries

External input includes OAuth callbacks, HTTP/JSON, TCP frames, asset manifests/files, settings, updates, extension data and user-provided paths.

Every boundary requires:

- explicit size/count/depth/time bounds;
- checked arithmetic and allocation;
- stable typed errors without raw secrets/backend/OS text;
- stale-generation rejection;
- deterministic cleanup and cancellation;
- negative tests for malformed, truncated, trailing, duplicated and unsupported input;
- no panic/unwrap on untrusted input.

Passwords never enter the Oteryn native-auth client path. Secret ownership claims remain limited to visible project-owned buffers; no universal erasure claim is permitted.

## 7. Current technical-login baseline

Merged W7 provides:

- native OAuth/PKCE and strict Gateway boundary;
- world/character directory and one-shot game-entry contracts;
- bounded TCP/protocol admission adapter;
- fake E2E through ordered Canary enter-world admission;
- Windows shell/runtime composition;
- fail-closed production Canary path without named deployment proof.

It does not provide:

- map/world packet decoding;
- authoritative simulation and immutable render snapshots;
- app-composed asset decode/resource upload or production import;
- world rendering;
- native UI framework or login presentation;
- Windows input adapter, product binding map or gameplay action consumers;
- inventory, containers, chat, combat, minimap or audio;
- reconnect/relog account lifecycle;
- launcher/updater/production deployment.

Workers must not relaunch W1-W7 prompts. Extend merged contracts through new bounded tasks.

## 8. Contract production order

P1 completed and separately archived the sole producers for:

1. canonical server/domain identifiers and session-scoped handles;
2. closed v1 `GameEvent` and `GameCommand` envelopes;
3. immutable verified synthetic-v1 asset runtime handles;
4. normalized physical input and semantic action/context contracts;
5. deterministic exact-source Canary Current opcode/dispatch evidence.

P2 is staged in `WAVE_P2_MINIMUM_VISIBLE_WORLD.md` and preserves these next sole producers:

1. `simulation-core` — the only mutable gameplay writer and immutable `RenderSnapshot` producer;
2. `protocol-canary` — the only Canary gameplay decoder/encoder, after mandatory `bc0068ab…` development-baseline alignment;
3. `asset-decode` — the only bounded CPU decoded-image producer;
4. `renderer-resource` — the only generation-fenced GPU resource handle/upload/cache producer;
5. `input-platform` — the only Windows/winit adapter into `input-actions`;
6. one serialized visible-world integration owner for `world-renderer` and `apps/client`;
7. one separate controlled M2 runtime acceptance owner.

Consumers start only from merged producer contracts or explicitly private synthetic fixtures. Synthetic composition remains a partial consumer; M2 is complete only after controlled login -> visible world -> movement/reconciliation -> logout acceptance on an exact named environment.

## 9. Shared integration paths

These paths normally require a recorded single-holder lease:

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/deny.toml
oteryn-client/tools/architecture-check/**
oteryn-client/tests/architecture-fixtures/**
oteryn-client/apps/client/**
docs/agents/MODULE_CATALOG.md
docs/agents/BUILD_TEST_MATRIX.md
docs/agents/CHANGELOG.md
oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
oteryn-client/docs/operations/RUST_WORKSPACE.md
.github/workflows/rust-client.yml
```

A worker may not manually merge lockfile fragments. Exclusive crate work may wait in `integration_ready` until the coordinator grants the lease and the branch is restacked on exact `main`.

## 10. Minimum reads for future workers

Every playability worker reads only:

1. its active task/checkpoint and live PR/CI;
2. `docs/agents/EXECUTION_PROTOCOL.md`;
3. `docs/agents/CONTEXT_HANDOFF.md`;
4. `docs/agents/PROMPTING_STANDARD.md` when writing downstream prompts;
5. this handoff;
6. the smallest relevant normative architecture/ADR and producer contract;
7. the current capability matrix row(s) it owns.

Do not load all historical wave prompts, full chat history or unrelated audit reports.

## 11. Slice definition of done

A slice is done only when:

- one owner and dependency direction are clear;
- public contracts are merged before consumers claim compatibility;
- external inputs are bounded/fail-closed;
- lifecycle and teardown are deterministic;
- focused and component tests pass;
- exact heavy final gates pass on final head;
- runtime/performance/compatibility evidence required by the claim exists;
- capability matrix and task checkpoint are current;
- task lifecycle is archived separately after merge.
