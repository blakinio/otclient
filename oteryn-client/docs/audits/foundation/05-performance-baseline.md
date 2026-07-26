# Performance Baseline Audit

## Evidence status

- `PROVEN` the maintained client is native C++ with LuaJIT, OpenGL, multiple execution threads and release LTO/IPO support.
- `PROVEN` the maintained client has a `Stats` facility and Lua-visible pause/resume controls.
- `PROVEN` existing architecture documentation mentions known UI/render degradation cases and texture-atlas work, but these are not a reproducible benchmark suite.
- `BLOCKED` this audit environment does not provide a built Windows client, supported game assets, GPU capture tools or a controlled live/replay scene.
- `BLOCKED` no trustworthy current FPS, frame-time, RAM, CPU, GPU, startup or relog measurements are recorded by this audit.
- `REJECTED` using illustrative FPS estimates from design discussion as baseline evidence.

The output of this audit is therefore a mandatory measurement protocol and fixture plan, not claimed results.

## Baseline principles

Every measurement must record:

```text
client commit
Canary commit or replay revision
asset manifest/version
build profile and compiler/toolchain
Windows version
CPU / GPU / RAM
GPU driver
resolution / refresh / scaling / vsync / frame cap
warm-up duration
measurement duration
scene/seed and input script
median, p95, p99 and worst relevant frame time
CPU/GPU memory
CPU/GPU utilization
queue/backlog/draw/instance counters when available
```

Average FPS alone is not accepted.

## Required reference scenes

### P0 — Startup and entry

Procedure:

1. clean user cache and shader/pipeline cache as defined by each client;
2. start launcher/client;
3. measure process start to first interactive login frame;
4. authenticate against fake service or controlled local environment;
5. select one character/channel;
6. measure ticket request, game connect, first map packet and first stable rendered world frame.

Metrics:

- startup wall time;
- main-thread blocking spans;
- peak/settled RAM;
- files/bytes decoded or uploaded;
- time to interactive;
- first-frame pipeline/shader stalls.

Status: `BLOCKED` until runnable Windows environment and legal assets exist.

### P1 — Light map

Synthetic/replay scene:

- one visible floor;
- mostly static ground/items;
- local player plus <= 5 creatures;
- minimal effects/text;
- health/status/chat/inventory UI visible.

Purpose: renderer/frame-loop overhead and high-refresh ceiling.

### P2 — Dense town

- dense multi-layer tiles/items;
- 50–100 visible dynamic entities with outfits, health bars, names and icons;
- mixed walking/idling animation;
- chat, battle list and multiple panels active;
- representative text density.

Purpose: extraction, sorting, draw/instance count, text and UI pressure.

### P3 — Heavy combat

- 100+ creatures where protocol/gameplay constraints permit;
- repeated movement, health changes, projectiles, effects and floating text;
- target/follow state;
- cooldown/action feedback;
- network/domain event burst fixture.

Purpose: simulation, protocol application, transient rendering and frame-time spikes.

### P4 — UI virtualization

Separate deterministic cases:

- thousands of chat rows with ongoing insertions;
- 500 battle-list entries with sorting/filter changes;
- large market/offer table;
- many inventory/container rows;
- resize, scroll and search.

Purpose: retained-tree growth, layout invalidation, text shaping and allocations.

### P5 — Fast map movement/streaming

- continuous camera/player motion through changing chunks;
- asynchronous decode/upload of synthetic assets;
- bounded cache near its configured budget;
- direction reversals and revisiting evicted chunks.

Purpose: asset-worker backpressure, chunk cache and hitching.

### P6 — Session lifecycle

Script:

1. login Channel 1;
2. play fixed replay interval;
3. logout normally;
4. select Channel 2;
5. login with fresh transaction;
6. repeat Channel 1/2 cycle 100 times;
7. include 20 simulated connection failures.

Metrics:

- retained tasks/threads/subscriptions;
- RAM/GPU resource trend;
- stale callback/session attempts;
- time to selection and re-entry;
- queue cleanup.

Purpose: prove relog does not accumulate state.

### P7 — Long soak

- 4 hours minimum initially, later 12–24 hours for release acceptance;
- mixed deterministic gameplay/UI workload;
- periodic relog/reconnect/device resize;
- diagnostics enabled at production sampling level.

Purpose: memory/resource stability and rare stalls.

### P8 — Failure and device recovery

- window resize/minimize/restore;
- GPU device loss simulation where backend supports it;
- audio device removal;
- corrupt cache/asset mount rejection;
- network backlog/disconnect;
- worker cancellation during shutdown.

Purpose: bounded recovery without corrupting session state.

## Legacy baseline harness

The maintained client baseline should use:

- exact Windows release preset and commit;
- isolated `--user-dir` to avoid personal configuration;
- existing `g_stats` samples or an explicitly reviewed extension;
- PresentMon/ETW or equivalent external frame-time capture where approved;
- GPU vendor-neutral capture where possible;
- fixed synthetic/local Canary environment;
- same legally available assets and resolution used for the Rust comparison;
- scripted keyboard/mouse/network/replay sequence.

`BLOCKED` the maintained client currently has no normalized replay harness capable of guaranteeing identical live input to a future Rust client. The audit recommends creating normalized domain/replay fixtures before comparative optimization claims.

## Rust benchmark harness requirements

The future tools must provide:

- headless deterministic domain replay;
- offscreen renderer scene runner where supported;
- interactive Windows GPU benchmark runner;
- machine-readable JSON result with schema version;
- trace/metrics correlation by frame and session generation;
- warm-up and sample-window controls;
- automatic asset/scene hash recording;
- trend comparison without making noisy microbenchmarks required prematurely.

Benchmark tooling is engineering infrastructure, not telemetry permission.

## Initial target budgets

The accepted architecture contains provisional recommended-tier 144 Hz budgets:

| Area | Provisional p95 target |
|---|---:|
| simulation/domain | <= 1.5 ms |
| world extraction/culling/batching CPU | <= 2.0 ms |
| UI update/layout/extraction | <= 1.0 ms |
| protocol event application | <= 0.75 ms under normal load |
| main orchestration excluding wait | <= 0.5 ms |
| total CPU frame work | <= 5.5 ms |
| GPU frame | <= 6.0 ms |

Audit classification:

- `PROVEN` these are accepted engineering targets.
- `UNKNOWN` whether they are achievable on the eventual recommended hardware and real production assets.
- `REJECTED` treating them as current product guarantees.

The first renderer/domain vertical slices must report measured values and may propose evidence-backed budget adjustments through architecture review.

## Memory budgets

Exact values remain `UNKNOWN` until asset inventory and scenes exist. Every cache must nonetheless have a configured budget and observable pressure behavior for:

- mutable domain state;
- CPU compressed/decoded assets;
- GPU textures/buffers;
- transient frame arenas;
- glyph/text cache;
- UI tree/view models;
- replay/diagnostic buffers;
- extension memory.

Required evidence before freezing values:

1. type/sprite/audio counts and sizes;
2. minimum/recommended hardware VRAM/RAM;
3. dense-scene peak residency;
4. eviction/reload cost;
5. 100-cycle relog and soak trends.

## Performance acceptance by milestone

| Milestone | Required measurement |
|---|---|
| workspace bootstrap | CI/tool duration only; no product FPS claim |
| synthetic asset pack | deterministic build size/time and bounded parser memory |
| renderer vertical slice | P1/P2 synthetic frame-time, draw/instance count and memory |
| domain/replay slice | event throughput and deterministic final-state checks |
| Canary MPS | P0–P6 on selected exact client/server/assets |
| beta | P1–P8 on minimum/recommended hardware |
| production | complete hardware matrix, long soak, update/install and crash diagnostics |

## Optimization rules

- measure before changing;
- correctness, validation and security are not disabled for speed;
- hot-path allocation reduction must include before/after evidence;
- GPU and CPU work are measured separately;
- no benchmark-only code path that differs materially from product behavior;
- performance regressions may be accepted only with explicit correctness/security rationale and remaining budget;
- one exceptional maximum frame does not override a good distribution, but recurring p99 stalls cannot be hidden by average FPS.

## Audit conclusion

- `BLOCKED` numeric baseline and concrete hardware acceptance.
- `PROVEN` the exact scenes, metadata and measurement policy needed to create trustworthy baseline evidence.
- `INFERRED` normalized replay and synthetic asset/renderer scenes should be established before broad protocol/UI feature implementation, because they allow performance work without a production server or proprietary committed assets.
