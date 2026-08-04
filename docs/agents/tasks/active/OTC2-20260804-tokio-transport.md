---
task_id: OTC2-20260804-tokio-transport
coordination_id: OTS-20260804-native-protocol-selection
status: implementing
phase: investigate
agent: "Tokio transport implementation owner"
project_lane: otclient-v2
track: greenfield-rust
branch: feat/OTC2-20260804-tokio-transport
base_branch: main
created: 2026-08-04
updated: 2026-08-04
risk: high
related_prs: []
depends_on:
  - completed OTC2-20260804-dual-protocol-architecture
  - completed OTC2-20260804-platform-gateway-protocol-plan
blocks:
  - later protocol-oteryn and automatic-selection packages require the shared async transport boundary
reuses:
  - oteryn-foundation cancellation and generation primitives
  - oteryn-transport bounded limits and stable errors
  - oteryn-app-runtime application lifecycle ownership
  - existing Gateway, Game Session and protocol-canary consumers
owned_paths:
  - docs/agents/tasks/active/OTC2-20260804-tokio-transport.md
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/crates/transport/**
  - oteryn-client/crates/app-runtime/**
  - oteryn-client/apps/client/**
  - oteryn-client/tests/integration/technical-login/**
  - oteryn-client/docs/research/transport/**
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
modules_touched:
  - oteryn-transport
  - oteryn-app-runtime
  - Windows client runtime composition
public_interfaces:
  - protocol-neutral bounded async transport/session supervision
shared_path_lease:
  - path: oteryn-client/Cargo.toml
    owner: OTC2-20260804-tokio-transport
  - path: oteryn-client/Cargo.lock
    owner: OTC2-20260804-tokio-transport
  - path: oteryn-client/crates/app-runtime/**
    owner: OTC2-20260804-tokio-transport
  - path: docs/agents/MODULE_CATALOG.md
    owner: OTC2-20260804-tokio-transport
    note: narrow current-main row update; the legacy PR #23 checkpoint is stale since 2026-07-24 and its lease has expired
  - path: docs/agents/CHANGELOG.md
    owner: OTC2-20260804-tokio-transport
    note: narrow current-main entry; the legacy PR #23 checkpoint is stale since 2026-07-24 and its lease has expired
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: true
  integration_required: true
  e2e_required: true
execution_mode: github-only
execution_reason: repository mutation and GitHub Actions provide the available exact-head build and test environment
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: terminal_only
implementation_authorized: true
decomposition_decision: phased
decomposition_reason: one cohesive transport/runtime migration with sequential implementation, validation, audit and closeout phases
context_pressure: high
context_growth: stable
context_score: 10
estimate_confidence: medium
invocation_started_at: 2026-08-04T15:04:00Z
last_progress_at: 2026-08-04T15:04:00Z
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Goal

Replace the production Rust-client blocking game transport with an application-owned Tokio runtime and bounded protocol-neutral full-duplex session supervision while preserving the current Oteryn Identity/Gateway/Game Session chain and exact protocol-canary behavior.

# Acceptance criteria

- [ ] The application owns Tokio runtime creation and shutdown; there is no hidden global runtime.
- [ ] The production game connection path uses Tokio TCP rather than blocking worker-owned socket I/O.
- [ ] Read, write and control paths are independently owned, bounded and cannot starve cancellation.
- [ ] Connect, read, write and idle deadlines are explicit and bounded.
- [ ] Queue-full, timeout, cancellation, stale-session and terminal protocol/connection failures are typed.
- [ ] Session generation fencing prevents queued work from reaching a replacement session.
- [ ] Errors that can desynchronize framing close the session terminally.
- [ ] TCP_NODELAY, current frame limits, Gateway/Game Session behavior and protocol-canary public behavior remain compatible.
- [ ] Deterministic loopback tests cover full-duplex I/O, partial I/O, cancellation, timeout/reset/EOF, saturation, ordering, priority, replacement isolation and joined shutdown.
- [ ] Comparative bounded evidence records queue latency, throughput, CPU/allocation or high-water proxies, slow-consumer behavior and shutdown latency without claiming lower physical RTT.
- [ ] Focused validation, workspace validation, exact-head CI, independent audit and required E2E pass.
- [ ] The implementation PR merges, the task archives and every lease releases.

# Boundaries

This task must not change Platform, Game Gateway, Otheryn, OAuth, ticket behavior, Game Session schema, Canary opcodes/fields/framing, protocol selection policy or create protocol-oteryn.

# Concurrency

PR #265 is a contract-only task owning its own task record, one future correspondence document and `docs/agents/CROSS_REPO_CONTRACTS.md`. This package does not touch those paths. Legacy PR #23 is stale and waiting for visual approval; its old shared-index lease is expired. This package will make only narrow current-main catalogue/changelog additions and will not mutate PR #23 or its feature paths.

# Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 1
  session_id: 20260804T150400Z-tokio-transport
  session_started_at: 2026-08-04T15:04:00Z
  checkpointed_at: 2026-08-04T15:04:00Z
  last_progress_at: 2026-08-04T15:04:00Z
  phase: investigate
  exact_head: pending task-record commit
  pull_request: none
  active_operation: repository discovery and interface design
  external_run_ids: []
  operation_started_at: null
  wait_deadline_at: null
  check_generation: draft
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: task branch exists and ownership remains non-conflicting
  next_action: inspect the remaining runtime, protocol-core, application composition, tests, workflows and lockfile, then commit the smallest complete Tokio transport design
```

# Evidence log

- Trusted base at claim: `914e8d560e09f8bb319f2af5d09a495167f010d6`.
- Open PR #265 is non-overlapping and explicitly forbids runtime/Tokio changes.
- Existing transport is synchronous `std::net::TcpStream` with bounded frame lengths and stable terminal errors.
- Existing application runtime owns cancellable/joined Identity and connection worker threads.
- Production Canary admission remains fail-closed before real network and credential handoff; its public contract must remain unchanged.
