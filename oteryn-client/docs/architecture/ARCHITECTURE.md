# Oteryn Client Architecture

Status: normative target architecture  
Scope: `oteryn-client/`  
Initial platform: Windows desktop  
Initial server compatibility: Canary adapter  
Target ecosystem: Oteryn

## 1. Objective

Build a new high-performance, secure and maintainable game client in Rust. The design is selected for the future Oteryn ecosystem and is not constrained by the implementation structure of the existing OTClient.

The current C++/Lua/OTUI client remains operational during migration and serves only as audited compatibility evidence. It is not a runtime dependency of the new client.

## 2. Architectural principles

1. **Domain before wire format.** Game state, commands and UI models do not contain Canary or Oteryn packet structures.
2. **Data-oriented hot paths.** Frequently processed state is contiguous, compact and specialized rather than represented by deep object hierarchies.
3. **Server authority.** Client prediction improves presentation but never decides inventory, combat, economy or persistent state.
4. **Single ownership.** Every mutable state set has one owning subsystem and explicit lifetime.
5. **Message passing over shared mutation.** Runtime stages exchange bounded commands, events and snapshots.
6. **No blocking frame work.** Network, filesystem, decompression, shader preparation and asset conversion stay outside frame-critical execution.
7. **Measured optimization.** Performance claims require named scenes, hardware, builds and frame-time distributions.
8. **Fail closed at trust boundaries.** Authentication, updater, assets, protocol parsing and extensions reject unsupported or malformed input.
9. **Static core, sandboxed extensibility.** Performance-critical and first-party systems are compiled Rust; optional external extensions use capability-limited WebAssembly.
10. **One normative architecture.** Agents extend these boundaries through ADRs rather than creating parallel designs.

## 3. System context

```text
System browser
    |
    | Authorization Code + PKCE
    v
Oteryn Identity / Platform
    |
    | account session + one-shot game login ticket
    v
Oteryn Client
    |
    | selected character + world + gameplay channel
    v
Game session adapter
    |-- Canary adapter during migration
    `-- Oteryn adapter when native game services are available
```

The client knows logical worlds and gameplay channels. It does not need to know the physical game-node topology.

## 4. Process model

### 4.1 Launcher process

`oteryn-launcher` owns:

- installation and repair;
- update discovery and download;
- signature and manifest verification;
- atomic activation and rollback;
- channel selection for release tracks such as stable or beta;
- launching the client with a minimal, validated argument set;
- collecting non-secret installation diagnostics.

The launcher does not own active game state and does not receive the user's main password.

### 4.2 Client process

`oteryn-client` owns:

- account authentication orchestration;
- world, character and gameplay-channel selection;
- game connection and session lifecycle;
- protocol adaptation;
- game domain and simulation;
- renderer, UI, input and audio;
- runtime assets and local settings;
- optional diagnostics and extension hosting.

Launcher/client IPC is versioned, narrow and authenticated where required. The normal game loop must not depend on the launcher remaining alive.

## 5. Runtime composition

```text
+--------------------------------------------------------------+
| Application shell                                            |
| state machine, lifecycle, user-facing error routing           |
+------------------------------+-------------------------------+
                               |
          +--------------------+--------------------+
          |                                         |
+---------v----------+                    +---------v----------+
| Account services   |                    | Game session       |
| Identity, directory|                    | protocol adapter   |
+---------+----------+                    +---------+----------+
          |                                         |
          |                                GameEvent/GameCommand
          |                                         |
+---------v-----------------------------------------v----------+
| Game domain and deterministic simulation                     |
+---------------------------+----------------------------------+
                            |
                     extracted snapshots
                            |
          +-----------------+------------------+
          |                                    |
+---------v----------+              +----------v---------+
| Renderer           |              | UI application     |
| world/text/effects |              | view models/widgets|
+---------+----------+              +----------+---------+
          |                                    |
          +-----------------+------------------+
                            |
                    platform / input / audio
```

## 6. Execution model

The exact thread count is benchmark-driven, but ownership boundaries are fixed.

### Main/event thread

- window and OS event loop;
- input ingestion;
- frame orchestration;
- presentation/swapchain lifecycle;
- application-state transitions that require OS coordination.

### Simulation owner

- consumes validated domain events and local commands;
- owns mutable game state;
- advances deterministic client-side timing;
- produces immutable or generation-stable render/UI snapshots;
- applies prediction and reconciliation where explicitly supported.

The simulation may run on a dedicated thread or a scheduled high-priority task. It must have one logical writer.

### Render preparation and GPU execution

- extracts visible data from the latest published snapshot;
- performs culling, batching and buffer preparation;
- builds render graph passes;
- submits modern GPU commands through `wgpu`;
- never calls protocol or feature business logic.

### Async I/O runtime

- Identity and directory HTTP;
- game transport;
- reconnect timers and heartbeats;
- downloads and remote manifests;
- bounded delivery into application/domain queues.

### Worker pool

- texture and audio decoding;
- asset decompression;
- atlas preparation;
- shader preprocessing/warm-up;
- minimap and cache tasks;
- replay compression and non-critical diagnostics.

### Audio callback/thread

- real-time-safe mixing and device output;
- no blocking, unbounded allocation or filesystem access.

## 7. Synchronization rules

- No broad `Arc<Mutex<GameState>>` shared by renderer, UI and network.
- Network produces validated events into a bounded queue.
- Simulation is the only writer of session game state.
- Renderer reads a double/triple-buffered render snapshot or generation-published extraction.
- UI reads view models/signals derived from domain state and owns its presentation state.
- Queue saturation has explicit policy: coalesce, drop non-critical diagnostics, disconnect on unsafe protocol backlog, or apply backpressure.
- Every asynchronous result carries an owner/session generation so stale callbacks cannot mutate a replacement session.

## 8. Game domain

The domain is independent of transport and presentation.

Representative model:

```text
SessionState
PlayerState
WorldState
  |- chunked tile storage
  |- creature storage
  |- item references
  |- projectiles/effects
InventoryState
ContainerState
CombatState
ChatState
FeatureState
```

Identifiers are strongly typed:

```text
AccountId
CharacterId
WorldId
WorldChannelId
GameSessionId
EntityId
ItemTypeId
ItemInstanceId
ContainerId
```

Local render/entity handles use generational indices. Persistent/server identifiers remain separate from transient session handles.

## 9. Data model

### Dynamic entities

Use specialized sparse-set or arena storage with struct-of-arrays layouts for frequently scanned components such as position, appearance, health and render flags.

Avoid a universal reflection-heavy ECS scheduler in the hot path. Systems are explicit and ordered. An ECS-like storage abstraction is acceptable only when benchmarks show no loss of control or locality.

### World map

The map is divided by floor and spatial chunk. Initial candidate chunk sizes are benchmark inputs, not fixed facts.

Each chunk tracks:

- revision/generation;
- dirty regions;
- compact tile occupancy;
- static and dynamic render extraction;
- lighting/visibility inputs;
- GPU cache references;
- memory residency state.

Changing one tile must not rebuild an entire visible floor.

## 10. Renderer

Primary API abstraction: `wgpu`.

Expected native backends include Direct3D 12 and Vulkan on Windows, with Metal/Vulkan portability retained by architecture but not claimed until tested.

Renderer layers:

```text
Render snapshot
  -> visibility extraction
  -> stable ordering/depth classification
  -> instance/batch construction
  -> render graph
  -> world passes
  -> effects and lighting
  -> text
  -> UI
  -> post-processing/presentation
```

Required design properties:

- instanced sprites;
- texture arrays and/or atlases selected by measured asset constraints;
- persistent/reused GPU buffers;
- chunk-level caching;
- glyph atlas and batched text;
- pipeline and bind-group caching;
- asynchronous resource upload;
- bounded transient allocation;
- explicit GPU memory budgets and eviction;
- device-loss recovery path;
- no per-sprite script callback.

The renderer never owns authoritative game state.

## 11. UI

The production UI is implemented in Rust and does not require OTUI/OTML or Lua.

Model:

- retained tree for hierarchy, focus, accessibility and incremental layout;
- reactive/view-model updates for state propagation;
- immediate render-command extraction for efficient GPU batching;
- virtualized collections for chat, battle list, market and large inventories;
- dirty layout/style propagation rather than full-tree work every frame.

UI core provides primitives only. Features register panels, actions, settings and view models through narrow interfaces. `ui-core` must not depend on inventory, market, chat or any other concrete feature.

Required capabilities:

- flex and grid layout;
- anchors/constraints where needed;
- high-DPI scaling;
- clipping and nested scrolling;
- keyboard navigation and focus;
- drag and drop;
- text shaping and localization;
- accessibility tree;
- docking/layout persistence;
- inspectable developer diagnostics.

## 12. Input

Input is normalized into actions rather than read directly by features.

```text
OS events -> physical input state -> bindings/contexts -> semantic actions
```

The input system owns:

- keyboard/mouse/gamepad devices;
- focus and capture;
- binding conflicts;
- action contexts such as gameplay, chat and modal UI;
- deterministic event ordering;
- accessibility-related alternatives.

Game commands are emitted through the application/domain command boundary, never directly to a socket.

## 13. Audio

Audio uses an explicit graph or voice manager over a cross-platform backend such as `cpal`.

It supports:

- decoded/streamed assets;
- categories and user mixing;
- positional and UI sound separation;
- bounded voice count and prioritization;
- device replacement/recovery;
- no allocation or locking in the real-time callback where avoidable.

## 14. Networking and protocol adapters

The transport layer handles bytes, encryption, framing, connection health and optional stream semantics. It does not create game widgets or mutate domain storage.

Protocol adapters translate:

```text
wire messages <-> validated adapter structures <-> GameEvent/GameCommand
```

Two separate adapters are planned:

- `protocol-canary`: exact supported Canary compatibility;
- `protocol-oteryn`: future native Oteryn game protocol.

Both target the same stable domain contracts. The game domain must compile and test without either adapter.

The Oteryn transport may later use QUIC or another multiplexed transport, but that decision is not encoded into the domain model. Network streams must not be confused with gameplay world channels.

## 15. Authentication and sessions

Account authentication:

```text
client -> system browser -> Oteryn Identity
       <- authorization code through validated loopback callback
client -> token/ticket exchange -> account session
```

Game entry:

```text
account session
 -> select character
 -> select world
 -> select gameplay channel
 -> request one-shot ticket scoped to that selection
 -> connect through selected protocol adapter
 -> create game session
```

The main Oteryn password is never collected by the game client login UI or sent to Canary/Oteryn game nodes.

Account session and game session are separate lifetimes. Relog ends only the game session and returns to character/channel selection while the valid account session remains.

## 16. Gameplay world channels

A world can expose multiple parallel gameplay channels.

The client represents each channel with a server-provided descriptor such as:

- stable `WorldChannelId`;
- display label;
- status;
- population/queue information;
- compatibility requirements;
- optional recommendation and latency estimate.

The client does not infer physical node addresses. Routing is authoritative from the platform/gateway contract.

Changing from Channel 1 to Channel 2 uses relog:

1. request normal game-session closure;
2. wait for success or follow explicit timeout/error policy;
3. destroy session-scoped state;
4. return to selection;
5. request a new one-shot ticket for Channel 2;
6. create a new game session.

No seamless in-game channel handoff is part of the initial architecture.

## 17. Features and modularity

Three extension levels exist:

1. engine/application crates compiled into the product;
2. first-party feature crates compiled into the product and activated by negotiated capabilities;
3. optional WebAssembly extensions with explicit capabilities and resource limits.

Feature examples include inventory, containers, chat, battle list, minimap, action bars, market and settings UI.

Features communicate through typed application/domain APIs and published view models. They do not access transport bytes, renderer internals or another feature's private state.

## 18. Assets

Source assets are imported and compiled outside the frame runtime into signed Oteryn asset packs.

Pipeline:

```text
source -> provenance/license validation -> normalization -> conversion
       -> atlas/array preparation -> compression -> manifest/hash/signature
       -> immutable versioned pack
```

Runtime access uses logical asset identifiers and memory-mapped/indexed pack data where appropriate. It does not depend on loose development source files.

Canary-compatible source formats may have dedicated importers. Their runtime representation remains Oteryn-owned and optimized.

## 19. Settings

Settings are schema-versioned and typed. Scopes include device, account, character and local profile.

Secrets are never stored in normal settings files. Platform credential stores are used for eligible long-lived credentials.

Settings migrations are explicit, testable and reversible where practical. UI layout data has size and structure limits.

## 20. Extensions

Third-party extensions, when enabled, run in WebAssembly with:

- declared capabilities;
- private bounded storage;
- memory and execution budgets;
- no native library loading;
- no arbitrary filesystem access;
- no arbitrary outbound network access;
- no direct protocol or raw memory access;
- revocable host handles.

Extension support is not required for the minimum playable milestone and may remain disabled until its security model is implemented and reviewed.

## 21. Diagnostics and replay

Built-in diagnostics expose:

- frame-time distributions;
- simulation and UI timing;
- draw/instance counts;
- queue occupancy;
- CPU and GPU memory budgets;
- network RTT/jitter and reconnect state;
- asset streaming activity;
- version and capability information.

Replays store sanitized normalized domain events/commands or legally captured synthetic wire fixtures. Authentication material, private chat and personal data are excluded or explicitly redacted.

Replay and benchmark tools must be usable without a live server.

## 22. Error model

Errors are typed and routed to user actions:

```text
Retry
ChooseAnotherChannel
ReturnToSelection
UpdateClient
RepairAssets
AuthenticateAgain
Exit
```

Protocol, identity, updater and asset errors retain internal diagnostic context while exposing safe user-facing messages. No component should terminate the process through uncontrolled panic for malformed external input.

## 23. Platform policy

Windows is the first required production target. Architecture remains portable, but no Linux, macOS or other compatibility claim is made until that target has its own CI and runtime acceptance.

Platform-specific code stays behind narrow abstractions for:

- window/event integration;
- URL launch and loopback callback;
- credential storage;
- filesystem locations;
- process/launcher integration;
- crash handling;
- raw/high-precision input.

## 24. Definition of done for an implementation slice

A slice is complete only when:

- it lives in the owning layer and obeys dependency direction;
- external input is validated and bounded;
- state ownership and teardown are deterministic;
- focused tests exist;
- required performance evidence exists for hot-path work;
- unsupported combinations fail clearly;
- security and cross-repository contracts are current;
- the full diff contains no unrelated or unlicensed material;
- exact-head CI and runtime evidence required by the workstream pass.
