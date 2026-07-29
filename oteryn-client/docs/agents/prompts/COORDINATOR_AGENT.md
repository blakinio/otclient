# Parallel Wave Coordinator Agent Prompt

W1, W2, W3 and W4 are completed and closed. W5 is the current accepted plan only after its planning lifecycle merges. Copy the block below into a fresh coordinator session; do not implement the worker package while coordinating.

```text
Work autonomously in repository:

blakinio/otclient

Role: coordinate `OTERYN-W5-RENDER-SURFACE`. Do not implement the renderer worker while coordinating.

Current Git/main, root and nested AGENTS.md, live open PRs, active tasks, accepted architecture, merged contracts/evidence and exact CI are authoritative. Do not rely on chat history.

Repository safety:

- routine writes only to blakinio/otclient;
- never mutate Canary, Oteryn Platform, upstream or another repository;
- never push directly to main;
- one task/branch/worktree per change;
- no branch-protection, review or CI bypass;
- no success or compatibility claim without exact evidence.

Mandatory reads:

1. AGENTS.md
2. docs/agents/README.md
3. oteryn-client/AGENTS.md
4. oteryn-client/docs/architecture/ARCHITECTURE.md
5. oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
6. oteryn-client/docs/agents/PROGRAM.md
7. oteryn-client/docs/agents/WORKSTREAMS.md
8. oteryn-client/docs/agents/MULTI_AGENT_EXECUTION.md
9. oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
10. oteryn-client/docs/operations/RUST_WORKSPACE.md
11. every active Rust task, open PR, review thread and required check
12. merged foundation/diagnostics/test-support/application-shell source and W4 runtime evidence
13. current primary wgpu/pollster registry source, licenses, MSRV and advisories

Revalidate before launch:

- W1-W4 are completed/archived and not launchable;
- W5 plan PR and its separate archive PR are merged;
- no active task or PR owns `crates/renderer`, the renderer-surface contract, Cargo/lockfile or shell composition paths;
- open legacy/operational PRs do not overlap W5 paths;
- exact primary evidence still supports `wgpu 30.0.0` and `pollster 1.0.1`, or the plan is amended before launch;
- the existing architecture checker still recognizes category `renderer` and no rule/fixture change is required.

Current wave:

- one coordinator;
- one implementation lane `W5-RENDER` using `NEXT_RENDERER_SURFACE_AGENT.md`;
- no secondary implementation or research lane.

W5-RENDER boundaries:

- exactly one package under `oteryn-client/crates/renderer/`, package name `oteryn-renderer`, category `renderer`;
- exact `wgpu = "=30.0.0"`, default features disabled, Windows `std` and `dx12` only unless fresh primary evidence changes;
- exact `pollster = "=1.0.1"`, default features disabled, used only for one synchronous main-thread bootstrap;
- preserve main-thread shell window ownership and deterministic close;
- own instance/surface/adapter/device/queue plus clear/present only;
- deterministic CPU-side unconfigured/configured/suspended/lost/closing lifecycle and stale-generation rejection;
- no game/map/entity rendering, assets, textures, shader module/framework, pipeline, render graph, UI, protocol, identity, network, audio, settings, persistence or extensions;
- no direct Win32/windows-sys/raw-window-handle dependency, unsafe, global renderer singleton, hidden service, reusable async runtime, scheduler, worker thread or continuous redraw loop;
- architecture checker/rules/fixtures, Rust CI/toolchain remain read-only unless a separate blocker is recorded.

Unique shared-path lease for W5-RENDER:

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

For the worker verify:

- unique task, branch/worktree and early draft PR;
- exact owned paths and unique lease in task front matter;
- exact dependency source/version/license/MSRV/advisory evidence;
- one renderer package and narrow shell integration only;
- CPU-side tests run without a GPU or interactive desktop;
- surface config occurs only for non-zero size;
- timeout/occluded/outdated/lost/validation and close policies are explicit;
- fatal renderer failure routes through the existing shell close path;
- renderer resources are released before the window;
- interactive Windows/GPU evidence is never inferred from compilation.

Merge readiness:

- full changed-file list and diff reviewed;
- automated acceptance and explicit runtime-evidence blockers documented;
- exact-head locked metadata, fmt, Clippy, all-target tests, architecture check, cargo-deny and repository CI pass;
- no unresolved comments/reviews/threads, overlap or migration/cross-repository blocker;
- base is current main and PR is mergeable;
- squash merge followed by a separate lifecycle archive PR.

After the worker archive merges, close W5 durably, release every lease and recommend exactly one next bounded package from live evidence. Do not implement that next package in the closure task.
```
