# Next Renderer Surface Agent Prompt

Use this prompt only after the W5 plan PR and its lifecycle archive merge. It authorizes exactly one `W5-RENDER` worker and no other lane.

```text
Work autonomously in repository:

blakinio/otclient

Task: implement the single bounded `OTERYN-W5-RENDER-SURFACE` worker package.

Current Git/main, root and nested AGENTS.md, live open PRs, active task records, accepted architecture, merged source/contracts and exact CI are authoritative. Do not rely on chat history.

Repository safety:

- routine writes only to blakinio/otclient;
- never mutate upstream, Canary, Oteryn Platform or another repository;
- never push directly to main;
- create one unique task, branch/worktree and early draft PR;
- no branch-protection, review or CI bypass;
- no secrets, proprietary assets or unsupported compatibility claims.

Mandatory preflight:

1. Read AGENTS.md and docs/agents/README.md.
2. Read oteryn-client/AGENTS.md, ARCHITECTURE.md, REPOSITORY_LAYOUT.md, PROGRAM.md, WORKSTREAMS.md, MULTI_AGENT_EXECUTION.md, CURRENT_PARALLEL_WAVE.md and RUST_WORKSPACE.md.
3. Inspect all active Rust tasks, open PRs, comments, reviews, threads and required checks.
4. Verify W1-W4 are historical and W5 plan plus plan archive are merged.
5. Verify no task/PR owns `crates/renderer`, renderer surface ownership, Cargo/lockfile or shell composition.
6. Read merged application-shell source/tests and W4 runtime evidence.
7. Revalidate exact current primary-source evidence for wgpu/pollster version, feature set, license, MSRV, advisories and source.
8. Confirm category `renderer` already exists and the current architecture rules allow the intended local dependency edges.

Create task:

`docs/agents/tasks/active/OTC-20260729-renderer-surface-ownership.md`

Use branch:

`feat/OTC-20260729-renderer-surface-ownership`

Declare exclusive owned paths:

- oteryn-client/crates/renderer/**
- oteryn-client/docs/research/renderer/W5_RUNTIME_EVIDENCE.md
- the active task record

Declare unique shared-path lease:

- oteryn-client/Cargo.toml
- oteryn-client/Cargo.lock
- oteryn-client/deny.toml
- oteryn-client/apps/client/Cargo.toml
- oteryn-client/apps/client/src/main.rs
- oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
- oteryn-client/docs/operations/RUST_WORKSPACE.md
- docs/agents/MODULE_CATALOG.md
- docs/agents/BUILD_TEST_MATRIX.md
- docs/agents/CHANGELOG.md

`deny.toml` may change only when exact cargo-deny evidence requires a narrow license/source adjustment. Architecture checker/rules/fixtures, Rust toolchain and CI workflows are read-only unless a separate blocker is recorded.

Implement exactly one package:

- path: `oteryn-client/crates/renderer/`
- package: `oteryn-renderer`
- architecture category: `renderer`

Candidate exact Windows dependencies, subject to fresh evidence:

```toml
wgpu = { version = "=30.0.0", default-features = false, features = ["std", "dx12"] }
pollster = { version = "=1.0.1", default-features = false }
```

Use `pollster::block_on` only once for synchronous main-thread adapter/device bootstrap. Do not create a reusable executor, reactor, scheduler, service or background thread.

Required deterministic contract:

- typed process-generation ownership;
- closed states for unconfigured, configured, suspended, lost and closing;
- configure only for non-zero physical size;
- deterministic resize/minimize/restore/suspend/loss/reconfigure/close transitions;
- stale-generation rejection without mutation;
- timeout and occluded outcomes skip presentation without becoming fatal;
- outdated and lost outcomes require bounded reconfiguration;
- validation/backend-fatal failures use closed non-secret error kinds;
- idempotent close and no presentation after close;
- bounded frame/reconfigure counters with explicit overflow behavior.

Required Windows adapter:

- preserve the shell's main-thread event loop and window ownership;
- create one wgpu instance and one surface from a shell-owned lifetime-safe window;
- request one compatible adapter/device/queue during startup;
- use DX12 only under the planned feature set;
- configure the surface only for non-zero size;
- clear one original fixed color and present; no shader or pipeline;
- redraw only from event-driven requests, not a continuous animation loop;
- integrate resize, suspend and close with the deterministic state contract;
- release renderer resources before the window;
- route fatal renderer failure through the existing shell close path.

Forbidden scope:

- game/map/entity rendering or render snapshot schema;
- textures, assets, asset formats, uploads or proprietary material;
- WGSL/shader modules, shader framework, pipelines, bind groups or render graph;
- UI, text, protocol, identity, networking, audio, settings, persistence, updater or extension runtime;
- direct windows-sys/Win32/raw-window-handle dependency or unsafe code;
- global renderer singleton, global mutable registry or global logger;
- async runtime, reusable executor, scheduler, polling loop, hidden service or worker thread;
- minimum Windows, GPU/driver/hardware/device-loss-recovery or performance compatibility claim.

Testing and evidence:

- CPU-side state tests must require no window/GPU/interactive desktop;
- cover every required transition, stale generation, idempotence and bounds;
- compile/test the concrete Windows adapter on exact Windows CI;
- create `W5_RUNTIME_EVIDENCE.md` with `PASS`, `OBSERVED` and `BLOCKED` matrix;
- mark visible clear/present, real resize/minimize, suspend/resume, surface/device loss, adapter/driver/hardware compatibility and performance `BLOCKED` unless genuinely exercised on a named environment;
- record exact runner OS/image/version and exact final head.

Validation gate:

- `cargo metadata --locked --format-version 1`;
- `cargo fmt --all --check`;
- `cargo clippy --workspace --all-targets --locked -- -D warnings`;
- `cargo test --workspace --all-targets --locked`;
- architecture workspace validation;
- cargo-deny advisories/licenses/bans/sources;
- repository required CI;
- full changed-file and full-diff review;
- no comments, requested changes or unresolved threads;
- current main/base and mergeability verified.

Use squash merge, then a separate docs-only lifecycle archive PR that releases every lease. Do not start the next package while archiving this worker.
```
