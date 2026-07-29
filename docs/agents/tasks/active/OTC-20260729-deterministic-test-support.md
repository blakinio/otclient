---
task_id: OTC-20260729-deterministic-test-support
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R01
parallel_wave: OTERYN-W3-TEST-SUPPORT
parallel_lane: W3-TEST
parallel_lane_state: active
coordinator_task: OTC-20260729-plan-w3-test-support
branch: test/OTC-20260729-deterministic-test-support
base_branch: main
created: 2026-07-29T10:08:00+02:00
updated: 2026-07-29T10:08:00+02:00
last_verified_commit: "9bb2f60d780d2ea6723015876cf95c7fa5e3cbfe"
required_base_commit: "9bb2f60d780d2ea6723015876cf95c7fa5e3cbfe"
risk: low
related_pr: pending
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

- [ ] Exactly one new library crate, category `tool`, with only workspace-local foundation and diagnostics dependencies.
- [ ] `ManualClock` is reused directly; no second clock trait or implementation.
- [ ] Deterministic timeline exposes current/advance/try-set and exact technical-context construction.
- [ ] Diagnostic fixture builder accepts reviewed static text and already-classified values only.
- [ ] Duplicate and field-bound failures propagate from diagnostics without partial event construction.
- [ ] Focused deterministic, redaction, thread-observation and compile-fail doctests pass.
- [ ] No async runtime, executor, scheduler, sleep, hidden thread, global registry, runtime integration or external data.
- [ ] Workspace/catalogue/matrix/changelog/layout/operations are current.
- [ ] Exact-head Rust Windows, supply-chain and repository required CI pass.
- [ ] PR merges and task archives independently; lease is released.

# Plan

1. Open an early draft PR and verify the unique lease.
2. Add the crate and workspace integration.
3. Add deterministic tests and compile-fail boundary evidence.
4. Update shared documentation.
5. Review full diff, validate exact head, merge and archive.

# Validation

| Revision | Check | Result |
|---|---|---|
| `9bb2f60d780d2ea6723015876cf95c7fa5e3cbfe` | live ownership/base/producer preflight | PASS |

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Shared-path lease: held by W3-TEST
- Archived at: pending
