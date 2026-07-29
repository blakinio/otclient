---
task_id: OTC-20260729-deterministic-test-support
status: awaiting_ci
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R01
parallel_wave: OTERYN-W3-TEST-SUPPORT
parallel_lane: W3-TEST
parallel_lane_state: validating
coordinator_task: OTC-20260729-plan-w3-test-support
branch: test/OTC-20260729-deterministic-test-support
base_branch: main
created: 2026-07-29T10:08:00+02:00
updated: 2026-07-29T10:42:00+02:00
last_verified_commit: "53b4c6ac6af74ff0409c12e6daeafed86c547fae"
required_base_commit: "9bb2f60d780d2ea6723015876cf95c7fa5e3cbfe"
risk: low
related_pr: "#73"
depends_on:
  - W3 plan PR #71 and archive PR #72
  - oteryn-foundation PR #54
  - oteryn-diagnostics PR #61
owned_paths:
  - oteryn-client/crates/test-support/**
  - docs/agents/tasks/active/OTC-20260729-deterministic-test-support.md
shared_path_lease:
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
  - oteryn-client/docs/operations/RUST_WORKSPACE.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/CHANGELOG.md
contract_role: producer
contracts_produced:
  - deterministic test timeline and diagnostic fixture builders
contracts_consumed:
  - oteryn-foundation ManualClock/Moment/generation contract
  - oteryn-diagnostics classified value/event/context contract
crates_touched:
  - oteryn-test-support
features_touched:
  - deterministic test time
  - classified diagnostic fixtures
contracts_touched:
  - new test-only helper API
modules_touched: []
reuses:
  - oteryn_foundation::ManualClock
  - oteryn_diagnostics structured contracts
public_interfaces:
  - TestTimeline
  - DiagnosticEventFixture
  - TestSupportError
cross_repo_tasks: []
performance_evidence:
  - no runtime or performance claim
security_evidence:
  - classified diagnostic values only; no secret-bearing fixtures
---

# Goal

Add exactly one small `oteryn-test-support` crate providing deterministic test-owned time/context and structured diagnostic-event fixtures while reusing merged foundation and diagnostics contracts.

# Acceptance criteria

- [x] Exactly one new library crate, category `tool`, with only workspace-local foundation and diagnostics dependencies.
- [x] `ManualClock` is reused directly; no second clock trait or implementation.
- [x] Deterministic timeline exposes current/advance/try-set and exact technical-context construction.
- [x] Diagnostic fixture builder accepts reviewed static text and already-classified values only.
- [x] Duplicate and field-bound failures propagate from diagnostics without partial event construction.
- [x] Focused deterministic, redaction, thread-observation and compile-fail doctests pass.
- [x] No async runtime, executor, scheduler, sleep, hidden thread, global registry, runtime integration or external data.
- [x] Workspace/catalogue/matrix/changelog/layout/operations are current.
- [x] Exact-head Rust Windows, supply-chain and repository required CI pass on the reviewed implementation head.
- [ ] Final task-record head passes required CI; PR merges and task archives independently.

# Delivered contract

- `TestTimeline` owns or clones the existing `ManualClock`, exposes it directly and provides explicit `now`, `advance`, `try_set` and technical-context construction.
- `DiagnosticEventFixture` accepts only `&'static str` message/keys and already-classified `DiagnosticValue` values, then delegates duplicate and field-bound enforcement to diagnostics.
- `TestSupportError` contains only closed `StaticTextError` and `DiagnosticBuildError` values.
- Two compile-fail doctests reject runtime-owned message/key strings.
- Unit tests cover deterministic time, clone/thread observation with barriers and no sleeps, backwards/overflow non-mutation, exact generations/correlation, insertion order, duplicate/limit propagation and redaction across Display/Debug/clones.

# Review findings and fixes

1. Initial locked metadata failed because one copied registry checksum differed from the existing generated lockfile; the exact main checksum was restored and only the local package entry retained.
2. `cargo fmt --check` reported three mechanical layout changes in the new source; the exact rustfmt output was applied.
3. Full ten-file review restored existing trailing-slash path notation in the build/test matrix.
4. No runtime integration, external dependency, architecture-policy edit or unrelated cleanup remains.

# Validation

| Evidence | Result |
|---|---|
| live ownership/base/producer preflight on `9bb2f60d780d2ea6723015876cf95c7fa5e3cbfe` | PASS |
| complete ten-file/full-diff review on `53b4c6ac6af74ff0409c12e6daeafed86c547fae` | PASS |
| Rust Client run `30435982581` | PASS: locked metadata, fmt, Clippy, unit/doctests, architecture and Supply Chain |
| repository CI run `30435982834` | PASS: all required jobs and `CI / Required` |
| final task-record head | exact-head rerun pending |

# Boundaries preserved

- no second clock, wall-clock source, sleep, polling loop, timer wheel, async runtime, executor or scheduler;
- no global registry, singleton, environment mutation, logger/subscriber, sink, upload, replay or product service;
- no protocol/authentication/endpoint/user/private/proprietary fixtures;
- no architecture-check, fixture, Rust CI/toolchain or deny-policy change;
- no runtime, server, platform or performance compatibility claim.

# Completion

- Final status: awaiting final exact-head CI
- PR: #73
- Merge commit: pending
- Shared-path lease: held by W3-TEST until archive merge
- Archived at: pending
