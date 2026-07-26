# Platform, Hardware and Dependency Audit

## Platform scope

- `PROVEN` Windows desktop is the first required product and CI target.
- `PROVEN` the architecture keeps platform boundaries narrow for window/event integration, URL launch, loopback callback, credential storage, filesystem paths, launcher IPC, crash handling and high-precision input.
- `REJECTED` claiming Linux, macOS, Android, browser or Steam Deck support from portable Rust source or `wgpu` alone.
- `INFERRED` retaining portable interfaces is useful, but every additional platform requires an explicit product decision, CI, packaging and runtime acceptance.

## Windows baseline capabilities

The first client must support:

- modern 64-bit Windows process model;
- per-monitor DPI awareness and monitor changes;
- modern GPU API through `wgpu`;
- system-browser URL launch and loopback callback;
- operating-system credential storage;
- UTF-8/Unicode paths and input;
- raw/high-precision mouse and deterministic keyboard handling where needed;
- audio device enumeration/replacement;
- crash/minidump or equivalent redacted diagnostics;
- signed installer/updater integration;
- safe user-data/cache paths and atomic file replacement.

Exact minimum Windows release is `UNKNOWN`. It must be selected from product/user population, dependency support and CI runner availability, not assumed by this audit.

## Hardware tier framework

Concrete models are intentionally not frozen because no reproducible client benchmark exists yet.

### Minimum tier

Purpose: supported play at 60 Hz with conservative graphics/settings.

Required evidence before selection:

- integrated or entry discrete GPU that supports the selected `wgpu` backend/features;
- RAM/VRAM sufficient for measured MPS asset residency and OS overhead;
- CPU capable of P2/P3 scenes below 16.67 ms p95;
- supported Windows/driver combination available for test;
- clean install/update and long-session evidence.

Status: `BLOCKED` pending asset statistics and P1–P8 benchmark results.

### Recommended tier

Purpose: full normal feature set at 1440p/144 Hz target conditions.

Required evidence:

- P2/P3/P5 under provisional architecture budgets;
- stable p95/p99 without recurring shader/asset stalls;
- sufficient VRAM for normal high-quality cache budget;
- UI/chat/battle-list virtualization acceptance;
- relog/soak stability.

Status: `BLOCKED` pending renderer and MPS vertical slice.

### High-refresh tier

Purpose: 144–240 Hz presentation in light/normal scenes, with dense-scene stability prioritized over peak FPS.

Required evidence:

- P1 high-refresh ceiling and CPU submission cost;
- P2/P3 1% low/frame-time distribution;
- high-DPI/ultrawide validation;
- input latency measurement where practical.

Status: `BLOCKED` pending product benchmark harness.

## Hardware selection rules

- choose at least one real test machine per tier, not only synthetic cloud runners;
- record exact CPU/GPU/RAM/driver/monitor mode;
- include one integrated-GPU or low-end case if the minimum market requires it;
- avoid selecting tiers solely by release year or marketing class;
- revalidate after asset format/compression and UI/text stack are stable;
- do not make a GPU vendor mandatory unless a proven backend defect requires it;
- keep feature-level fallbacks explicit and measurable.

## Graphics API and windowing

### `wgpu`

- `PROVEN` selected by ADR-0002 as the renderer abstraction.
- Exact crate version, feature flags and Windows backend policy are `UNKNOWN` until WS-R01/WS-R08 performs current primary-documentation review and a Windows bootstrap spike.
- Required audit in the implementation task: supported Rust version, D3D12/Vulkan behavior, surface/device-loss lifecycle, shader format/tooling, pipeline cache support, texture/format limits, unsafe/native dependencies, license and maintenance.
- An evidence-backed ADR amendment is allowed if the selected boundary proves unsuitable.

### Window/event library

A library such as `winit` is a candidate, not an accepted dependency.

Required proof:

- Windows DPI and monitor transitions;
- resize/minimize/restore and surface lifecycle;
- IME/text input;
- raw mouse and keyboard behavior;
- event-loop integration with async/network and renderer ownership;
- licensing, maintenance and unsafe/FFI surface.

Status: `UNKNOWN` exact library/version.

## Async and networking

An async runtime is expected for Identity, directory, transport, updater and workers, but the runtime must not own domain correctness or force the renderer onto its scheduler.

Candidate categories:

- async runtime;
- HTTP/TLS client;
- TCP/UDP/QUIC transport depending on exact protocol;
- bounded channel/queue primitives;
- cancellation and timeouts.

A library such as `tokio` is a candidate, not frozen.

Required proof:

- Windows support and shutdown semantics;
- cancellation safety;
- TLS backend/certificate policy;
- bounded buffering/backpressure;
- runtime thread ownership and diagnostics;
- dependency/unsafe/license footprint.

Status: `UNKNOWN` exact packages/versions.

## Text and fonts

Candidate categories:

- Unicode segmentation/bidi;
- shaping;
- font parsing/rasterization;
- glyph atlas integration.

Possible libraries must be evaluated against required scripts, DPI quality, caching, license and unsafe/native surface. No font family or text stack is selected by this audit.

Status: `UNKNOWN`; blocked in part by localization/font product decisions.

## Audio

A backend such as `cpal` is a candidate.

Required proof:

- Windows device enumeration and replacement;
- output latency and format negotiation;
- callback real-time behavior;
- no blocking/allocation on callback path;
- license/maintenance/unsafe surface;
- compatibility with selected decoding stack.

Status: `UNKNOWN`; audio is not part of the first workspace bootstrap.

## WebAssembly extensions

The accepted architecture requires WebAssembly for optional third-party extensions, but no runtime is selected.

A future evaluation must compare:

- deterministic fuel/time limits;
- memory limits and pooling;
- component/interface model maturity required by product;
- Windows packaging/binary size/startup cost;
- capability host-call control;
- supply-chain/license/unsafe surface;
- crash containment and diagnostics.

Status: `UNKNOWN`; explicitly post-playable and not a bootstrap dependency.

## Serialization, schemas and binary formats

- `PROVEN` normalized domain commands/events and asset schemas need stable versioning.
- `REJECTED` selecting Protobuf, FlatBuffers, Cap'n Proto, MessagePack or another schema technology before the native Oteryn protocol/asset requirements are measured.
- `INFERRED` Rust-native manually controlled structures may be sufficient for internal domain/replay initially, with a documented versioned file envelope.

## Dependency policy requirements

WS-R01 must establish:

- pinned Rust toolchain and minimum supported Rust version policy;
- committed application `Cargo.lock`;
- workspace-level lint policy;
- `unsafe` denied by default, explicit reviewed exceptions only;
- advisory/vulnerability scanning;
- license allow/deny policy;
- duplicate/version-tree visibility;
- reproducible source policy and no unreviewed git/path dependencies;
- dependency update process and rollback;
- Windows build cache policy without treating cache as source of truth.

## Candidate dependency decision table

| Area | Architecture position | Exact dependency status | Gate |
|---|---|---|---|
| Rust toolchain | Rust stable | version `UNKNOWN` | WS-R01 current primary docs + Windows CI |
| GPU | `wgpu` selected | version/features/backend `UNKNOWN` | WS-R01 metadata + WS-R08 spike |
| window/events | narrow abstraction required | candidate `UNKNOWN` | WS-R02 Windows behavior spike |
| async/network | async I/O required | candidate `UNKNOWN` | WS-R02/WS-R05 |
| HTTP/TLS | secure Identity/updater required | candidate `UNKNOWN` | WS-R03/WS-R15 threat model |
| text/font | native shaped text required | candidate `UNKNOWN` | WS-R10 localization/DPI spike |
| audio | real-time-safe backend required | candidate `UNKNOWN` | WS-R12 |
| WASM | sandbox required later | runtime `UNKNOWN` | WS-R16 post-playable |
| logging/tracing | structured redacted diagnostics required | candidate `UNKNOWN` | WS-R01/WS-R14 |
| serialization | versioned internal files/contracts | technology `UNKNOWN` | owning format/protocol task |

## CI hardware implications

Initial required CI:

- Windows compile/test for workspace/toolchain and non-GPU crates;
- headless domain/protocol/security tests;
- documentation/architecture checks;
- dependency/license/advisory checks.

GPU tests:

- `BLOCKED` reliable supported GPU runner policy is not established;
- renderer logic should have CPU-side unit tests and offscreen smoke where supported;
- product performance acceptance must run on named physical Windows hardware even if CI offers a GPU runner.

## Audit conclusion

- `PROVEN` Windows-first, Rust stable and `wgpu` architecture direction.
- `BLOCKED` concrete hardware tiers, minimum Windows release and product performance claims.
- `UNKNOWN` exact versions/packages for all dependencies, including `wgpu` version.
- `PROVEN` the first bootstrap package can establish workspace/toolchain/lint/license/architecture policy without prematurely selecting the application, protocol, audio, text or extension stacks.
