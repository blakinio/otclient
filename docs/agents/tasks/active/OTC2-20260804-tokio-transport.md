---
task_id: OTC2-20260804-tokio-transport
coordination_id: OTS-20260804-native-protocol-selection
status: implementing
phase: validate
agent: "Tokio transport implementation owner"
project_lane: otclient-v2
track: greenfield-rust
branch: feat/OTC2-20260804-tokio-transport
base_branch: main
created: 2026-08-04
updated: 2026-08-04
risk: high
related_prs:
  - 266
depends_on:
  - completed OTC2-20260804-dual-protocol-architecture
  - completed OTC2-20260804-platform-gateway-protocol-plan
  - completed OTC2-20260804-native-protocol-contract
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
last_progress_at: 2026-08-04T16:05:00Z
ci_checks_for_current_head: 0
ci_check_generation: validation-2
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Goal

Replace the production Rust-client blocking game transport with an application-owned Tokio runtime and bounded protocol-neutral full-duplex session supervision while preserving the current Oteryn Identity/Gateway/Game Session chain and exact protocol-canary behavior.

# Acceptance criteria

- [x] The application owns Tokio runtime creation and shutdown; there is no hidden global runtime.
- [x] The production connection/admission owner executes on the application-owned Tokio runtime rather than an OS connection worker thread.
- [x] Read, write and control paths are independently owned, bounded and cannot starve cancellation.
- [x] Connect, read, write and idle deadlines are explicit and bounded.
- [x] Queue-full, timeout, cancellation, stale-session and terminal protocol/connection failures are typed.
- [x] Session generation fencing prevents queued work from reaching a replacement session.
- [x] Errors that can desynchronize framing close the session terminally.
- [x] TCP_NODELAY, current frame limits, Gateway/Game Session behavior and protocol-canary public behavior remain compatible.
- [x] Deterministic tests cover full-duplex I/O, partial I/O, cancellation, timeout/EOF, saturation, ordering, priority, replacement isolation and joined shutdown.
- [ ] Comparative bounded evidence records queue latency, throughput, CPU/allocation or high-water proxies, slow-consumer behavior and shutdown latency without claiming lower physical RTT.
- [ ] Focused validation, workspace validation, exact-head CI, independent audit and required E2E pass.
- [ ] The implementation PR merges, the task archives and every lease releases.

# Boundaries

This task must not change Platform, Game Gateway, Otheryn, OAuth, ticket behavior, Game Session schema, Canary opcodes/fields/framing, protocol selection policy or create protocol-oteryn.

# Concurrency

The native protocol contract and correspondence work merged through PRs #265 and #267 without runtime overlap. Legacy PR #23 is stale and waiting for visual approval; its old shared-index lease is expired. This package will make only narrow current-main catalogue/changelog additions and will not mutate PR #23 or its feature paths.

# Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 2
  session_id: 20260804T150400Z-tokio-transport
  session_started_at: 2026-08-04T15:04:00Z
  checkpointed_at: 2026-08-04T16:05:00Z
  last_progress_at: 2026-08-04T16:05:00Z
  phase: validate
  exact_head: a0298943c2af71ddad1be9dfaf8801b8a0f611d9
  pull_request: 266
  active_operation: exact-head compile lint and deterministic transport test validation
  external_run_ids: []
  operation_started_at: 2026-08-04T16:05:00Z
  wait_deadline_at: null
  check_generation: validation-2
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: PR #266 remains open and its branch retains the registered ownership
  next_action: inspect exact-head CI, repair any compile or test failure, then produce comparative bounded evidence and closeout documentation
```

# Evidence log

- Trusted base at claim: `914e8d560e09f8bb319f2af5d09a495167f010d6`.
- PR #266 owns the implementation package; merged contract PRs #265 and #267 did not change Tokio or runtime code.
- Tokio is exact-pinned at `1.51.4` with only IO, macros, networking, multi-thread runtime, synchronization and time features.
- `oteryn-transport` now owns bounded gameplay/background/inbound queues, header-first frame allocation, typed terminal failure classes, generation fencing, TCP_NODELAY, external and internal cancellation, full-duplex reader/writer tasks and joined supervisor shutdown.
- `oteryn-app-runtime` now lazily owns and shuts down a named two-thread Tokio network runtime. Identity remains on its existing worker thread; connection/admission work no longer owns an OS thread.
- Blocking transport remains available only as a test/evidence baseline behind `blocking-baseline`; the exported production `TcpTransport` names the Tokio session.
- Deterministic tests cover partial IO, connect/read/write timeouts, EOF, malformed and oversized framing, protocol-terminal errors, inbound and outbound saturation, control priority, gameplay FIFO/priority, stale generations, external cancellation and repeated joined shutdown cycles.
- A runtime test records that connection admission executes on `oteryn-network`, not the caller/application thread.
- Earlier run `30925782744` reached formatting, Clippy and supply-chain success; its three terminal-wait test failures were traced to calling close-oriented `join` when a peer/deadline outcome was intended. The API now separates `wait` from caller-initiated `join`.
