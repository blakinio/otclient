---
task_id: OTC2-20260804-tokio-transport
coordination_id: OTS-20260804-native-protocol-selection
status: validating
phase: terminal-ci
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
  - oteryn-client/docs/architecture/decisions/ADR-001-dual-protocol-selection-and-async-transport.md
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
  - path: oteryn-client/docs/architecture/decisions/ADR-001-dual-protocol-selection-and-async-transport.md
    owner: OTC2-20260804-tokio-transport
    note: implementation-status update only
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
estimate_confidence: high
invocation_started_at: 2026-08-04T15:04:00Z
last_progress_at: 2026-08-04T18:20:00Z
ci_checks_for_current_head: 2
ci_check_generation: terminal-current-main-4
terminal_ci_wait_started_at: 2026-08-04T18:20:00Z
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 4
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Goal

Replace the production Rust-client blocking game transport with an application-owned Tokio runtime and bounded protocol-neutral full-duplex session supervision while preserving the current Oteryn Identity/Gateway/Game Session chain and exact protocol-canary behavior.

# Acceptance criteria

- [x] The application owns Tokio runtime creation and shutdown; there is no hidden global runtime.
- [x] The production connection/admission owner executes on the application-owned Tokio runtime rather than an OS connection worker thread.
- [x] Read, write and control paths are independently owned, bounded and cannot starve cancellation.
- [x] Connect, read, write and idle deadlines are explicit, total-operation bounded and cancellation-aware.
- [x] Queue-full, timeout, cancellation, stale-session and terminal protocol/connection failures are typed.
- [x] Session generation fencing prevents queued work from reaching a replacement session.
- [x] Errors that can desynchronize framing close the session terminally.
- [x] TCP_NODELAY, current frame limits, Gateway/Game Session behavior and protocol-canary public behavior remain compatible.
- [x] Deterministic tests cover full-duplex I/O, partial I/O, connect/read/write deadlines, cancellation during connect/read/backpressured write, reset/EOF classification, saturation, ordering, priority, replacement isolation and joined shutdown.
- [x] Comparative bounded evidence records queue latency, throughput, process CPU time, allocation/backpressure proxies, slow-consumer behavior and shutdown latency without claiming lower physical RTT.
- [ ] Exact-head workspace CI and the deterministic technical-login E2E suite pass on the final current-main checkpoint head.
- [x] Independent diff audit has no open critical, high or material-medium finding and no unresolved review thread.
- [ ] The implementation PR merges, the task archives and every lease releases.

# Boundaries

This task does not change Platform, Game Gateway, Otheryn, OAuth, ticket behavior, Game Session schema, Canary opcodes/fields/framing, protocol selection policy or create protocol-oteryn.

# Concurrency

The native protocol contract and correspondence work merged through PRs #265 and #267 without runtime overlap. Current-main Canary work touches producer-specific gameplay/task paths and does not overlap the Tokio implementation. Legacy PR #23 is stale and waiting for visual approval; its old shared-index lease is expired. This package makes only narrow current catalogue/changelog and accepted-ADR status additions and does not mutate PR #23 or its feature paths.

# Independent audit

```yaml
audited_pr: 266
audited_code_evidence_head: 6543e9dd69ac537e4d8bdbed6431fd51504c3dc7
critical_open: 0
high_open: 0
material_medium_open: 0
unresolved_review_threads: 0
scope_boundary_violations: 0
temporary_workflows_remaining: 0
generated_target_files_remaining: 0
result: PASS
repairs:
  - total read/write operation deadlines now cannot be extended indefinitely by partial progress
  - connected backpressured-write cancellation is covered and bounded
  - connection-reset classification is covered in addition to abrupt EOF
  - blocking and Tokio evidence now run in separate Windows processes and record process CPU time
  - accidental target metadata and every temporary workflow were removed before terminal CI
```

# Comparative evidence

```yaml
run: 30929681775
job: windows-cpu-evidence
source_sha: d9e536d75b3ed4aeb78e301549651d91f6868881
runner: Windows_X64
rustc: 1.94.0
tokio: 1.51.4
blocking:
  latency_us_p50_p95_p99: [40, 74, 91]
  burst_frames_per_second: 23003.74
  cpu_time_ms: 62.500
  shutdown_us: 52
tokio:
  latency_us_p50_p95_p99: [42, 70, 99]
  burst_frames_per_second: 87961.58
  cpu_time_ms: 46.875
  shutdown_us: 121
  queue_high_water: 968
  queue_full: 0
  slow_consumer_cancel_us: 15788
throughput_ratio: 3.82
cpu_ratio: 0.75
physical_rtt_claim: false
```

# Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 4
  session_id: 20260804T150400Z-tokio-transport
  session_started_at: 2026-08-04T15:04:00Z
  checkpointed_at: 2026-08-04T18:20:00Z
  last_progress_at: 2026-08-04T18:20:00Z
  phase: terminal-ci
  observed_current_main: 8002e2b51d9f0ba825f788815d814aed5101c925
  synchronized_parent_head: 92e7d2d77b48733946caaa86511e8be950a8536c
  prior_exact_green_head: fbd442348dee034abbc2326f96013a16edaa582b
  code_evidence_head: 6543e9dd69ac537e4d8bdbed6431fd51504c3dc7
  pull_request: 266
  active_operation: final exact-head CI after current-main synchronization and checkpoint refresh
  external_run_ids:
    - 30929681775
    - 30930746953
    - 30930747500
  operation_started_at: 2026-08-04T18:20:00Z
  wait_deadline_at: null
  check_generation: terminal-current-main-4
  checks_used: 0
  status: active
  safe_to_resume: true
  auto_merge_enabled: true
  resume_condition: PR #266 remains open and current-main compatible
  next_action: require the new exact-head Rust Client and CI workflows; auto-merge when green; then archive this task from current main and release every lease
```

# Evidence log

- Trusted base at claim: `914e8d560e09f8bb319f2af5d09a495167f010d6`.
- Tokio is exact-pinned at `1.51.4` with only IO, macros, networking, multi-thread runtime, synchronization and time features.
- `oteryn-transport` owns bounded gameplay/background/inbound queues, header-first frame allocation, typed terminal failure classes, generation fencing, TCP_NODELAY, external/internal cancellation, full-duplex reader/writer tasks and joined supervisor shutdown.
- `oteryn-app-runtime` lazily owns and shuts down a named two-thread Tokio network runtime. Identity remains on its existing worker thread; connection/admission work no longer owns an OS thread.
- Blocking transport remains only as a feature-gated test/evidence baseline; the exported production `TcpTransport` names the Tokio session.
- Deterministic tests cover partial I/O, total connect/read/write deadlines, EOF and reset classification, malformed and oversized framing, protocol-terminal errors, inbound/outbound saturation, cancellation during a backpressured write, control priority, gameplay FIFO/priority, stale generations, external cancellation and repeated joined shutdown cycles.
- A runtime test records that connection admission executes on `oteryn-network`, not the caller/application thread.
- Windows evidence run `30929681775` passed focused format, strict all-target Clippy, transport tests and release-mode separate-process measurement before committing the raw and interpreted evidence.
- Exact synchronized head `fbd442348dee034abbc2326f96013a16edaa582b` passed Rust Client run `30930746953` and repository CI run `30930747500` before `main` advanced again.
- Earlier terminal-wait failures were repaired by separating peer/deadline `wait` from caller-initiated close-and-`join`; later audit found and repaired partial-progress deadline resetting before terminal CI.
- No Platform, Gateway, Otheryn, protocol-canary wire, Game Session schema, OAuth, ticket or native-protocol product path is modified by PR #266.
