# Next Windows Application Shell Agent Prompt

Copy the block below into one fresh worker session only after the W4 plan and its lifecycle archive have merged.

```text
Work autonomously in repository:

blakinio/otclient

Task: implement lane `W4-SHELL` from `OTERYN-W4-WINDOWS-SHELL` as one bounded Windows blank-window application package.

Do not rely on chat history. Current Git/main, root and nested AGENTS.md, live open PRs, active tasks, accepted architecture, merged foundation/diagnostics/test-support source, merged Windows evidence and exact CI are authoritative.

Repository safety:

- routine writes only to blakinio/otclient;
- never mutate upstream, Canary, Oteryn Platform or another repository;
- never push directly to main;
- create one task, one branch/worktree and an early draft PR;
- stop for unresolved ownership overlap, secrets/proprietary data, required external writes or a stable-boundary conflict needing an ADR.

Fresh preflight:

1. Read AGENTS.md, docs/agents/README.md and oteryn-client/AGENTS.md.
2. Read ARCHITECTURE.md, REPOSITORY_LAYOUT.md, PROGRAM.md, WORKSTREAMS.md, MULTI_AGENT_EXECUTION.md, CURRENT_PARALLEL_WAVE.md and RUST_WORKSPACE.md.
3. Inspect all active Rust tasks, open PRs, review threads and current main.
4. Read merged foundation, diagnostics and test-support public APIs/tests.
5. Read all merged Windows platform evidence under docs/research/windows-platform/.
6. Revalidate exact winit version, release notes, Cargo metadata, license, MSRV, advisories and Windows dependency graph from primary sources.
7. Confirm no owner holds `apps/client`, Cargo/lockfile or W4 shared docs.
8. Record exact producer/base/dependency evidence in the task.

Required package:

- add exactly one package at `oteryn-client/apps/client/`;
- package name `oteryn-client`;
- architecture category `app`;
- exact direct external dependency `winit = "=0.30.13"` unless the fresh evidence gate proves a different exact version and the plan is updated first;
- workspace-local dependencies only on `oteryn-foundation`, `oteryn-diagnostics` and `oteryn-test-support` when each is concretely used;
- no other direct dependency.

Required public behavior:

- one deterministic shell state machine with explicit startup, running, closing and exited phases;
- typed process generation and stale-generation rejection;
- idempotent close request and bounded application command handling;
- bounded structured lifecycle diagnostics using reviewed static text/keys and classified values;
- one main-thread `ApplicationHandler` that creates one resizable blank window after `resumed`;
- handle close, destroyed, focus, resize including zero-size/minimize/restore, scale factor, keyboard, modifiers, mouse, wheel, cursor, IME and redraw events without renderer work;
- enable IME explicitly on the active window;
- accept one bounded synthetic user event through `EventLoopProxy` from one named one-shot thread;
- join the one-shot thread after `run_app` returns;
- exit through one deterministic close state and no surviving worker.

Hard boundaries:

- do not create a separate platform crate unless a concrete reusable boundary is proven and the W4 plan is amended before implementation;
- no renderer, GPU surface, wgpu, shader or frame loop;
- no direct raw-window-handle, windows-sys, Win32 FFI, unsafe code or window message hook;
- no async runtime, executor, scheduler, polling loop or background service;
- no protocol, authentication, networking, endpoint, assets, audio, feature UI, persistence, settings or updater;
- no global mutable application state, logger/subscriber or sink installation;
- no arbitrary external/runtime text in errors or diagnostics;
- no minimum Windows release, device, DPI, IME, hardware or performance claim.

Owned path:

- `oteryn-client/apps/client/**`
- the worker task record

Unique shared lease:

- `oteryn-client/Cargo.toml`
- `oteryn-client/Cargo.lock`
- `oteryn-client/deny.toml`
- `oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md`
- `oteryn-client/docs/operations/RUST_WORKSPACE.md`
- `docs/agents/MODULE_CATALOG.md`
- `docs/agents/BUILD_TEST_MATRIX.md`
- `docs/agents/CHANGELOG.md`

`deny.toml` may change only if exact cargo-deny evidence requires a narrow license/source allowance. Do not weaken advisories, source, wildcard or duplicate-version policy merely to pass CI.

Required automated tests:

- startup -> running -> closing -> exited transitions;
- duplicate close remains idempotent;
- stale process generation is rejected without state mutation;
- command queue/batch bound is enforced;
- zero-size/minimize and restore state are deterministic;
- focus/modifier/IME state is cleared on close/focus loss as designed;
- diagnostic buffer is bounded and insertion order deterministic;
- error and diagnostic Display/Debug contain no arbitrary external text;
- repeated state-machine construction/close cycles have no global state;
- compile barriers or API shape prevent arbitrary strings from entering reviewed diagnostic text.

Runtime evidence matrix:

- record exact Windows CI runner/OS information available from workflow logs;
- mark automated compile/test/architecture/supply-chain evidence `PASS`;
- mark interactive behavior only `OBSERVED` when genuinely exercised on a named interactive Windows environment;
- mark unavailable desktop launch/close, multi-monitor DPI, IME and physical-input cases `BLOCKED`, never inferred pass;
- absence of interactive hardware is a compatibility blocker but does not invalidate the bounded code spike when all automated acceptance and documentation are complete.

Validation from `oteryn-client/` on exact final head:

- `cargo metadata --locked --format-version 1`
- `cargo fmt --all --check`
- `cargo clippy --workspace --all-targets --locked -- -D warnings`
- `cargo test --workspace --all-targets --locked`
- `cargo run --locked -p oteryn-architecture-check -- workspace .`
- `cargo deny check`
- required Rust Client Windows/Supply Chain and repository `CI / Required`

Before merge:

- review the complete changed-file list and full diff;
- update task, module catalogue, build/test matrix, changelog, repository layout and workspace operations;
- add one focused runtime-evidence report under `oteryn-client/docs/research/windows-platform/` without rewriting historical evidence;
- keep the PR body current with exact validation SHA and explicit compatibility blockers;
- verify comments/reviews/threads and unchanged current base;
- mark ready, pass any ready-for-review exact-head run and squash-merge with expected head SHA;
- archive the task in a separate lifecycle PR and release the lease.
```
