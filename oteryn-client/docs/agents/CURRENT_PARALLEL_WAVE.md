# Current Parallel Agent Wave

Status: accepted launch plan  
Wave ID: `OTERYN-W3-TEST-SUPPORT`  
Evidence cut: `main` `0b1cd7914c04efd6b41a4a1b975234df715e6104`

Live Git, active task records and open PRs remain authoritative. W1 and W2 are completed, archived and not launchable. This plan authorizes exactly one implementation lane after its coordination-plan lifecycle merges.

## 1. Confirmed transition state

- W1-F foundation primitives are merged/archived and must not be relaunched.
- W2-DIAG, W2-CP, W2-AR and W2-PR are merged/archived through PR #70.
- All W2 task, contract and shared-path leases are released.
- Open PRs #23 and #37 own legacy paths only; PR #48 is isolated non-merge operational work.
- No active Rust-client task or open PR owns deterministic test support, `crates/test-support`, Cargo/lockfile integration or the proposed public surface.

## 2. Objective

Complete Gate 1 package 5 with one small deterministic Rust test-support crate that reuses merged clock and diagnostics contracts without introducing runtime infrastructure.

The wave uses:

```text
1 coordinator
1 implementation worker
```

No evidence or secondary implementation lane is authorized.

## 3. Dependency graph

```text
merged oteryn-foundation (#54)
          +
merged oteryn-diagnostics (#61)
          |
          v
W3-TEST deterministic test support
```

## 4. Lane W3-C — Coordinator

Prompt: `prompts/COORDINATOR_AGENT.md`

Responsibilities:

- verify live ownership and the exact required base before worker launch;
- prevent W1/W2 relaunch;
- grant one Cargo/lockfile/shared-document lease only to W3-TEST;
- require exact-head Windows workspace, architecture, supply-chain and repository CI;
- merge/archive the worker independently;
- close W3 and recommend exactly one next bounded package.

The coordinator does not implement the worker package while preparing or closing the wave.

## 5. Lane W3-TEST — Deterministic test support and fake time

Prompt: `prompts/NEXT_TEST_SUPPORT_AGENT.md`

Workstream: WS-R01 test infrastructure, consuming WS-R14 diagnostics contracts  
Contract role: producer

Required merged producers:

```text
oteryn-foundation: PR #54 merge 7a68f6e7d92eb6b05078bb001e4881d78544a82b
oteryn-diagnostics: PR #61 merge 6d0c5ce243e62ff1e5b548a626c3f5e228506717
W3 plan/archive: current main at worker preflight
```

Purpose:

- add exactly one `oteryn-test-support` library crate under `oteryn-client/crates/test-support/`;
- provide deterministic test-owned timeline/context and diagnostic-event fixture builders;
- consume `oteryn_foundation::ManualClock` directly rather than defining another clock trait or implementation;
- consume classified `oteryn-diagnostics` values rather than adding arbitrary runtime strings;
- keep every failure type closed and secret-free;
- remain usable without window, network, filesystem, async runtime or product service startup.

Required design boundaries:

- standard-library-first; only merged workspace-local `oteryn-foundation` and `oteryn-diagnostics` dependencies;
- architecture category `tool`; no new architecture category or checker-policy change;
- no second clock abstraction and no `MonotonicClock` implementation;
- no sleep, wall-clock time, hidden thread, executor, scheduler, timer wheel or polling loop;
- no global mutable fixture registry, singleton or environment mutation;
- no logger/subscriber/sink installation, telemetry, crash report, support bundle or replay implementation;
- no protocol, authentication, endpoint, user data, proprietary asset or private path fixture;
- no product/runtime integration and no compatibility or performance claim.

Expected exclusive path:

```text
oteryn-client/crates/test-support/**
```

Expected shared-path lease:

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
oteryn-client/docs/operations/RUST_WORKSPACE.md
docs/agents/MODULE_CATALOG.md
docs/agents/BUILD_TEST_MATRIX.md
docs/agents/CHANGELOG.md
```

The architecture checker, its fixtures, Rust toolchain, deny policy and CI workflow remain read-only because the accepted `tool -> foundation/diagnostics` graph needs no new category or rule.

Acceptance envelope:

- exactly one new library crate and no external dependency;
- deterministic timeline/context construction using the shared `ManualClock` state;
- deterministic diagnostic event/field insertion order and explicit classified values;
- focused tests for time progression, backwards/overflow propagation, generations/context, duplicate/bounded fields, redaction and clone/thread observation;
- compile/doctest barrier showing arbitrary runtime strings are not accepted as safe fixture values;
- locked metadata, formatting, Clippy, workspace tests, architecture validation and supply-chain checks pass on exact final head;
- full diff contains no runtime integration or unrelated cleanup.

## 6. Shared-path lease

| Path group | Lease holder | Other work |
|---|---|---|
| Cargo workspace/lockfile | W3-TEST | read-only |
| test-support crate/public surface | W3-TEST | no duplicate producer |
| shared catalogue/matrix/changelog/layout/workspace docs | W3-TEST | read-only |
| architecture checker/fixtures | none | read-only |
| Rust CI/toolchain/deny policy | none | read-only |

The worker claims the lease only through its active task and live draft PR after a fresh overlap check.

## 7. Merge and completion rules

- W3-TEST starts only after this plan and its archive are merged.
- Any material producer change requires restack and exact-head revalidation.
- The worker merges only through the root autonomous gate and receives a separate archive PR.
- W3 closes only after the worker is merged/archived, no lease remains and one evidence-based next package is recorded.

Candidate next package after successful closure: the bounded Windows application-shell spike from merged W2-PR evidence. It is not authorized by this plan.
