# Current Parallel Agent Wave

Status: accepted launch plan  
Wave ID: `OTERYN-W4-WINDOWS-SHELL`  
Evidence cut: `main` `e7b251c2b898ad76655ed71c72e72c1e26f9364f`

Live Git, active tasks and open PRs remain authoritative. W1, W2 and W3 are completed, archived and not launchable. This plan authorizes exactly one implementation lane only after the W4 plan and its lifecycle archive merge.

## 1. Confirmed transition state

- W1 foundation primitives are merged/archived and must not be relaunched.
- W2 diagnostics/evidence lanes are merged/archived and must not be relaunched.
- W3 deterministic test support is merged/archived through PR #76 and must not be relaunched.
- All prior Cargo/lockfile/shared-document leases are released.
- Open PRs #23 and #37 own legacy paths only; PR #48 is isolated operational non-merge work.
- No active Rust task or open PR owns `oteryn-client/apps/client/`, the application-shell contract or its Cargo/lockfile integration.

## 2. Objective

Implement one bounded Windows blank-window application shell that proves main-thread event ownership, deterministic shell state transitions, safe diagnostics and orderly shutdown without beginning renderer, protocol or product-feature work.

The wave uses:

```text
1 coordinator
1 implementation worker
```

No secondary implementation or research lane is authorized.

## 3. Dependency graph

```text
merged foundation (#54)
merged diagnostics (#61)
merged test support (#73)
merged Windows evidence (#67)
          |
          v
W4-SHELL blank-window application package
```

## 4. Lane W4-C — Coordinator

Prompt: `prompts/COORDINATOR_AGENT.md`

Responsibilities:

- verify live ownership and exact required base before worker launch;
- prevent W1-W3 relaunch;
- grant one Cargo/lockfile/shared-document lease only to W4-SHELL;
- require exact dependency, Windows workspace, architecture, supply-chain and repository CI evidence;
- merge/archive the worker independently;
- close W4 and record exactly one next bounded recommendation.

The coordinator does not implement the worker package while preparing or closing the wave.

## 5. Lane W4-SHELL — Windows blank-window application shell

Prompt: `prompts/NEXT_WINDOWS_SHELL_AGENT.md`

Workstream: WS-R02 platform/application foundation  
Contract role: producer

Required merged producers:

```text
oteryn-foundation: PR #54
oteryn-diagnostics: PR #61
oteryn-test-support: PR #73
Windows platform evidence: PR #67
W4 plan/archive: current main at worker preflight
```

Purpose:

- add exactly one application package under `oteryn-client/apps/client/` with package name `oteryn-client` and architecture category `app`;
- exact-pin `winit = "=0.30.13"` as the sole new direct external dependency unless fresh primary evidence changes before the worker task starts;
- create one resizable blank Windows window after `resumed`;
- keep event-loop, window, DPI/IME policy and shutdown coordination on the main thread;
- provide a deterministic, testable shell state machine independent of an interactive desktop;
- record bounded structured lifecycle diagnostics with existing diagnostics contracts;
- accept one bounded synthetic `EventLoopProxy` user event from a one-shot thread and join it after the event loop exits;
- terminate through one idempotent close path with no surviving worker.

Required design boundaries:

- no separate platform crate unless implementation proves a concrete reusable boundary; prefer one package;
- no renderer, GPU surface, `wgpu`, `raw-window-handle` direct dependency or graphics work;
- no direct `windows-sys`, Win32 FFI, unsafe code or message hook;
- no async runtime, executor, scheduler, polling loop or background service;
- no protocol, identity, networking, assets, audio, feature UI, persistence, settings or updater;
- no arbitrary runtime text in errors or diagnostics;
- no global mutable application state or global logger/subscriber;
- no minimum Windows release, hardware, DPI, IME or performance compatibility claim.

Expected exclusive path:

```text
oteryn-client/apps/client/**
```

Expected shared-path lease:

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/deny.toml
oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
oteryn-client/docs/operations/RUST_WORKSPACE.md
docs/agents/MODULE_CATALOG.md
docs/agents/BUILD_TEST_MATRIX.md
docs/agents/CHANGELOG.md
```

`deny.toml` is leased only for a narrowly evidenced license/source adjustment if exact cargo-deny proves the current allowlist insufficient. Rust toolchain, architecture checker/rules/fixtures and CI workflow remain read-only unless a separate blocker is recorded.

Acceptance envelope:

- exactly one new application package;
- exact direct dependency selection with source/license/MSRV/advisory evidence;
- deterministic tests for startup/running/closing/exited transitions, duplicate close, stale generation, bounded command handling and bounded diagnostics;
- no interactive desktop required for unit tests;
- binary compiles on exact Windows CI and contains one main-thread `ApplicationHandler`;
- full diff contains no renderer, protocol, assets, direct Win32 or unrelated cleanup;
- locked metadata, formatting, Clippy, all-target tests, architecture validation, cargo-deny and repository CI pass on exact final head.

## 6. Runtime evidence policy

GitHub-hosted Windows compilation does not prove interactive desktop behavior. The worker must publish an evidence matrix distinguishing:

- `PASS` automated state-machine/build/supply-chain evidence;
- `OBSERVED` behavior genuinely exercised on a named interactive Windows environment;
- `BLOCKED` launch/close, DPI, multi-monitor, IME or physical-input scenarios unavailable in the current runner.

Unavailable cases are explicit blockers for compatibility claims, not blockers to merging the bounded spike when all code/automated acceptance and documentation requirements pass.

## 7. Shared-path lease

| Path group | Lease holder | Other work |
|---|---|---|
| Cargo workspace/lockfile and dependency policy | W4-SHELL | read-only |
| application package/public shell contract | W4-SHELL | no duplicate producer |
| shared catalogue/matrix/changelog/layout/workspace docs | W4-SHELL | read-only |
| architecture checker/rules/fixtures | none | read-only |
| Rust CI/toolchain | none | read-only |

The worker claims the lease only through its active task and live draft PR after a fresh overlap check.

## 8. Merge and completion rules

- W4-SHELL starts only after this plan and its archive merge.
- Any material producer/dependency evidence change requires restack and exact-head revalidation.
- The worker merges only through the root autonomous gate and receives a separate archive PR.
- W4 closes only after the worker is merged/archived, no lease remains and one evidence-based next package is recorded.

Candidate next package after successful closure: a small renderer-surface ownership evidence/spike only if W4 establishes a stable window/shutdown boundary. It is not authorized by this plan.
