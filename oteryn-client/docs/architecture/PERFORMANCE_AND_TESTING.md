# Performance Budgets and Test Strategy

Performance figures in this document are initial engineering targets. They are not product claims until measured on named hardware, build, scene and server/replay revision.

## 1. Measurement policy

Every performance result records:

- commit SHA and build profile;
- Rust/toolchain and relevant dependency versions;
- operating system and graphics driver;
- CPU, GPU, RAM and display mode;
- scene/replay fixture revision;
- warm-up policy and duration;
- median, p95, p99 and worst relevant frame time;
- CPU/GPU memory and queue occupancy;
- whether diagnostics affected the result.

Average FPS alone is insufficient.

## 2. Initial target tiers

The foundation audit defines exact hardware. Until then, use three named classes:

- `minimum`: lowest supported Windows hardware;
- `recommended`: mainstream target;
- `high-refresh`: hardware expected to drive 144–240 Hz presentation.

Do not select concrete models without audit evidence and product ownership approval.

## 3. Frame budgets

Initial recommended-tier targets:

| Area | 144 Hz budget target |
|---|---:|
| simulation/domain update | <= 1.5 ms p95 |
| world extraction/culling/batching CPU | <= 2.0 ms p95 |
| UI update/layout/extraction | <= 1.0 ms p95 |
| protocol event application | <= 0.75 ms p95 under normal load |
| main-thread orchestration excluding wait | <= 0.5 ms p95 |
| total CPU frame work | <= 5.5 ms p95 |
| GPU frame | <= 6.0 ms p95 |

At 60 Hz on minimum hardware, normal gameplay should stay below 16.67 ms p95 with no recurring asset-streaming stalls. Exact acceptance thresholds are finalized after baseline scenes exist.

## 4. Stability targets

- no blocking network/filesystem/decompression work in frame-critical paths;
- no routine unbounded allocation growth during a session;
- no regular frame spikes caused by shader/pipeline creation after warm-up;
- bounded protocol and worker queues with observable saturation;
- deterministic teardown without accumulating tasks, timers, GPU resources or subscriptions over repeated relogs;
- device/asset recovery does not corrupt session state.

## 5. Benchmark scenes

The audit must define legally reproducible scenes covering:

1. empty/light map;
2. dense town with players, outfits, labels and UI panels;
3. heavy combat with creatures, effects, projectiles and text;
4. large inventory/container and battle-list activity;
5. high-volume chat and UI virtualization;
6. fast map movement with asset streaming;
7. repeated login/relog between gameplay channels;
8. reconnect and full snapshot application;
9. minimized/background and device resize behavior;
10. long soak session.

Scenes should use normalized replay or synthetic fixtures so CI/dev comparisons do not require a live production server.

## 6. Memory budgets

The audit provides asset-size evidence. The architecture requires explicit configurable budgets for:

- mutable game/domain state;
- CPU decoded asset cache;
- GPU textures/buffers;
- transient frame arenas;
- UI tree and glyph cache;
- replay/diagnostics buffers;
- extension memory.

Each cache has eviction, pressure metrics and a bounded failure mode. “Use all available memory” is not a policy.

## 7. Test layers

### Unit and property tests

- typed identifiers and conversions;
- data structures/arenas/chunks;
- deterministic domain rules;
- settings migrations;
- UI layout primitives;
- asset index parsing;
- redaction rules.

### Protocol tests

- golden encode/decode fixtures;
- version/capability gates;
- malformed, truncated and oversized input;
- state-machine ordering;
- differential tests against verified Canary behavior where legally and technically possible;
- fuzzing and minimized regressions.

### Integration tests

- account and game-session state machines with fake endpoints;
- world/character/gameplay-channel selection;
- relog Channel 1 -> Channel 2;
- reconnect without ticket replay;
- app/domain/adapter composition;
- asset mount/update/rollback;
- extension sandbox limits.

### UI tests

- interaction and focus;
- keyboard-only flows;
- DPI and representative resolutions;
- localization expansion;
- virtualization behavior;
- accessible names/roles;
- screenshot/reference tests using original fixtures.

### Renderer tests

- render extraction correctness;
- ordering, clipping and batching;
- device-loss/resize paths;
- visual scene snapshots with tolerances;
- CPU/GPU benchmark gates;
- no runtime pipeline compilation in warmed scenes when avoidable.

### Security tests

Follow `SECURITY_MODEL.md` negative cases. Security failures cannot be waived as flaky performance tests.

### Soak and fault tests

- repeated login/relog/logout cycles;
- packet delay/loss/reordering within protocol semantics;
- disk-full/cache corruption;
- asset/update interruption;
- audio/GPU device replacement;
- extension exhaustion;
- multi-hour memory/resource stability.

## 8. Determinism and replay

Simulation tests use a controlled time source and ordered inputs. Given the same initial snapshot, capabilities and command/event stream, deterministic subsystems produce the same final state.

Presentation-only interpolation and GPU rendering may be nondeterministic but must not change authoritative domain outcomes.

Replay metadata includes schema revision and capability set. Old replays either migrate explicitly or fail with a clear incompatibility message.

## 9. CI stages after bootstrap

Proposed stages:

1. format and workspace metadata;
2. architecture/dependency checks;
3. clippy with workspace lints;
4. unit/property tests;
5. protocol golden/fuzz smoke corpus;
6. security and dependency/license checks;
7. Windows build and headless integration tests;
8. renderer/UI tests on supported GPU runner when available;
9. benchmark trend jobs, initially non-blocking until stable noise thresholds are established;
10. packaging/update clean-install tests.

Windows is the first required compiled platform. Other targets require explicit policy and evidence.

## 10. Regression policy

A hot-path PR must include before/after evidence using the same fixture and environment. A correctness fix may accept a measured cost only with explicit budget analysis and approval.

Performance work may not weaken validation, security checks, deterministic lifecycle or server authority.

## 11. Acceptance milestones

### Foundation

Workspace builds, architecture edges are enforced, deterministic clocks/IDs/test support exist.

### Render vertical slice

Synthetic chunked map renders with measured instancing/batching and stable frame time.

### Protocol vertical slice

Verified Canary fixtures produce domain events without UI/network coupling.

### Playable slice

Login, selection, gameplay channel, map, movement, entities, basic UI, relog and diagnostics work against the exact selected Canary pair.

### Production candidate

Complete security/update/asset gates, feature acceptance, soak tests, crash diagnostics and exact hardware performance matrix pass.
