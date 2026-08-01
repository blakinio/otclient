---
task_id: OTC2-20260801-nonblocking-shutdown-remediation
status: active
agent: "GPT-5.6 Thinking"
lane: otclient-v2
track: greenfield-rust
workstream: lifecycle
phase: validation
branch: fix/OTC2-20260801-nonblocking-shutdown-remediation
base_branch: main
created: 2026-08-01T09:52:00+02:00
updated: 2026-08-01T10:34:00+02:00
last_verified_commit: "07121872ddb8243b387b9743b95540142faf3877"
required_base_commit: "43ed867910907cd4ebcf9f14e64977105d08ab7e"
risk: high
related_pr: "127"
depends_on:
  - OTC2-20260801-secret-lifecycle-remediation
  - R1 implementation merge c6d11a6c26f75c2169913e297c14b0ec25419736
  - R1 archive merge 43ed867910907cd4ebcf9f14e64977105d08ab7e
blocks:
  - OTC2-20260801-complete-architecture-policy
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-nonblocking-shutdown-remediation.md
  - oteryn-client/apps/client/src/main.rs
  - oteryn-client/apps/client/src/technical_login.rs
  - oteryn-client/apps/client/src/technical_login_base.rs
  - oteryn-client/apps/client/src/windows_shell.rs
  - oteryn-client/apps/client/src/windows_shell_part1.rs
  - oteryn-client/apps/client/src/windows_shell_part2.rs
  - oteryn-client/apps/client/src/windows_shell_part3.rs
  - oteryn-client/apps/client/src/windows_shell_part4.rs
  - oteryn-client/crates/app-runtime/src/lib.rs
  - oteryn-client/crates/app-runtime/src/model.rs
  - oteryn-client/crates/app-runtime/src/runtime.rs
  - oteryn-client/crates/app-runtime/src/runtime_1.rs
  - oteryn-client/crates/app-runtime/src/runtime_2.rs
  - oteryn-client/crates/app-runtime/src/runtime_3.rs
  - oteryn-client/crates/app-runtime/src/runtime_4.rs
  - oteryn-client/crates/app-runtime/src/runtime_5.rs
  - oteryn-client/crates/app-runtime/src/runtime_6.rs
  - oteryn-client/crates/app-runtime/src/tests.rs
  - oteryn-client/crates/transport/src/lib.rs
  - oteryn-client/crates/transport/src/transport_base.rs
  - oteryn-client/docs/architecture/decisions/2026-08-01-nonblocking-technical-login-shutdown.md
shared_path_lease:
  - "PR #23 recorded a narrow catalogue/changelog transfer; no shared-path edit was required for the final R2 contract."
modules_touched:
  - technical login runtime shutdown
  - Windows event-loop close coordination
  - bounded TCP configuration
crates_touched:
  - oteryn-app-runtime
  - oteryn-transport
  - oteryn-client
features_touched:
  - technical-login shutdown lifecycle
  - bounded synchronous I/O configuration
reuses:
  - existing CancellationSource and owned JoinHandle workers
  - existing event-loop proxy signal and 16 ms active poll cadence
  - existing bounded Ureq and callback limits
contracts_produced:
  - nonblocking begin/poll shutdown state machine
  - typed Pending, Overdue and Complete shutdown progress
  - maximum 30-second TCP connect/read/write configuration
contracts_consumed:
  - merged R1 secret ownership
  - merged W7 entry lifecycle and technical-login runtime
contracts_touched:
  - TechnicalLoginRuntime shutdown API
  - TechnicalLoginController exit integration
  - TransportConfig timeout validation
implementation_authorized: true
policy_version: 2
task_kind: implementation
context_pressure: medium
decomposition_decision: phased
execution_mode: codex
performance_evidence:
  - no latency, throughput or hardware compatibility claim
security_evidence:
  - no credential, private capture, production endpoint or proprietary material used
---

# Goal

Remediate `OTC2-AUD-002` so the Windows event-loop thread never joins an unfinished technical-login worker while preserving deterministic ownership and bounded synchronous I/O.

# Implemented contract

- `TechnicalLoginRuntime::begin_shutdown` records one monotonic start, requests cancellation and returns typed progress.
- `poll_shutdown` joins only workers whose `JoinHandle::is_finished()` is true.
- unfinished workers remain owned as `Pending(WorkerKind)` and become `Overdue(WorkerKind)` after 31 seconds without being detached or abandoned.
- `Complete` is returned only after workers are joined exactly once and session state is logged out.
- close, destroy and failure paths keep the Windows event loop alive through worker-completion user events and a 16 ms `WaitUntil` fallback.
- renderer/window release and `event_loop.exit()` occur only after `Complete`.
- public TCP connect, read and write timeout configuration rejects values above 30 seconds.
- Platform HTTP remains capped at 30 seconds; callback user wait remains capped at 300 seconds with at-most-250-millisecond read slices.
- no dependency, manifest, lockfile, workflow, retry, reconnect, worker-kill or async-runtime change was introduced.

# Evidence

- gate-controlled runtime test proves `Pending -> Overdue -> Complete`, worker retention while overdue, rejection of new work and eventual joined/logged-out completion.
- transport test rejects each 31-second connect/read/write value and accepts the exact 30-second boundary.
- accepted ADR: `oteryn-client/docs/architecture/decisions/2026-08-01-nonblocking-technical-login-shutdown.md`.
- source head `07121872ddb8243b387b9743b95540142faf3877` passed Rust Client run `30693860685` and CI run `30693860840`.
- Windows job `91353213087` passed locked metadata, rustfmt, strict Clippy, complete workspace tests and architecture policy.
- Supply Chain job `91353213100` passed.
- repository `CI / Required` job `91353329580` passed.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T10:34:00+02:00
head: 5506e83a9a28acf66a3445817c45f9022a4addf2
branch: fix/OTC2-20260801-nonblocking-shutdown-remediation
pr: 127
status: active
context_routes:
  - docs/agents/AGENTS.md
  - docs/agents/EXECUTION_PROTOCOL.md
  - oteryn-client/docs/audits/post-w7/REMEDIATION_PLAN.md
  - oteryn-client/crates/app-runtime/src/runtime.rs
  - oteryn-client/apps/client/src/windows_shell.rs
  - oteryn-client/crates/transport/src/lib.rs
  - oteryn-client/docs/architecture/decisions/2026-08-01-nonblocking-technical-login-shutdown.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-nonblocking-shutdown-remediation.md
  - oteryn-client/apps/client/src/main.rs
  - oteryn-client/apps/client/src/technical_login.rs
  - oteryn-client/apps/client/src/technical_login_base.rs
  - oteryn-client/apps/client/src/windows_shell.rs
  - oteryn-client/apps/client/src/windows_shell_part1.rs
  - oteryn-client/apps/client/src/windows_shell_part2.rs
  - oteryn-client/apps/client/src/windows_shell_part3.rs
  - oteryn-client/apps/client/src/windows_shell_part4.rs
  - oteryn-client/crates/app-runtime/src/lib.rs
  - oteryn-client/crates/app-runtime/src/model.rs
  - oteryn-client/crates/app-runtime/src/runtime.rs
  - oteryn-client/crates/app-runtime/src/runtime_1.rs
  - oteryn-client/crates/app-runtime/src/runtime_2.rs
  - oteryn-client/crates/app-runtime/src/runtime_3.rs
  - oteryn-client/crates/app-runtime/src/runtime_4.rs
  - oteryn-client/crates/app-runtime/src/runtime_5.rs
  - oteryn-client/crates/app-runtime/src/runtime_6.rs
  - oteryn-client/crates/app-runtime/src/tests.rs
  - oteryn-client/crates/transport/src/lib.rs
  - oteryn-client/crates/transport/src/transport_base.rs
  - oteryn-client/docs/architecture/decisions/2026-08-01-nonblocking-technical-login-shutdown.md
proven:
  - Windows event-loop close handling no longer joins an unfinished technical-login worker.
  - Every worker remains owned until JoinHandle::is_finished and is then joined exactly once.
  - Overdue is typed diagnostic state and does not authorize renderer/window release or event-loop exit.
  - TCP connect, read and write timeout configuration is capped at 30 seconds.
  - Source head 07121872ddb8243b387b9743b95540142faf3877 passed the full Rust and repository CI ladder.
derived:
  - No new dependency, manifest, lockfile or workflow change is required.
  - The existing worker-completion proxy and 16 ms fallback are sufficient for deterministic progress.
unknown: []
conflicts: []
first_failure:
  marker: resolved-rustfmt-and-clippy
  evidence: Initial rustfmt and two dead-code/collapsible-if diagnostics were corrected without weakening checks.
rejected_hypotheses:
  - Event-loop shutdown may synchronously join because I/O is bounded.
  - An overdue worker may be detached, forgotten or force-terminated.
  - Callback user-wait deadline must be shortened below 300 seconds.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-nonblocking-shutdown-remediation.md
  - oteryn-client/apps/client/src/main.rs
  - oteryn-client/apps/client/src/technical_login.rs
  - oteryn-client/apps/client/src/technical_login_base.rs
  - oteryn-client/apps/client/src/windows_shell.rs
  - oteryn-client/apps/client/src/windows_shell_part1.rs
  - oteryn-client/apps/client/src/windows_shell_part2.rs
  - oteryn-client/apps/client/src/windows_shell_part3.rs
  - oteryn-client/apps/client/src/windows_shell_part4.rs
  - oteryn-client/crates/app-runtime/src/lib.rs
  - oteryn-client/crates/app-runtime/src/model.rs
  - oteryn-client/crates/app-runtime/src/runtime.rs
  - oteryn-client/crates/app-runtime/src/runtime_1.rs
  - oteryn-client/crates/app-runtime/src/runtime_2.rs
  - oteryn-client/crates/app-runtime/src/runtime_3.rs
  - oteryn-client/crates/app-runtime/src/runtime_4.rs
  - oteryn-client/crates/app-runtime/src/runtime_5.rs
  - oteryn-client/crates/app-runtime/src/runtime_6.rs
  - oteryn-client/crates/app-runtime/src/tests.rs
  - oteryn-client/crates/transport/src/lib.rs
  - oteryn-client/crates/transport/src/transport_base.rs
  - oteryn-client/docs/architecture/decisions/2026-08-01-nonblocking-technical-login-shutdown.md
validation:
  - command: cargo metadata --locked --format-version 1
    result: PASS
    evidence: Rust Client Windows job 91353213087 on 07121872ddb8243b387b9743b95540142faf3877.
  - command: cargo fmt --all --check
    result: PASS
    evidence: Rust Client Windows job 91353213087.
  - command: cargo clippy --workspace --all-targets --locked -- -D warnings
    result: PASS
    evidence: Rust Client Windows job 91353213087.
  - command: cargo test --workspace --all-targets --locked
    result: PASS
    evidence: Rust Client Windows job 91353213087, including shutdown and timeout regression tests.
  - command: cargo run --locked -p oteryn-architecture-check -- workspace .
    result: PASS
    evidence: Rust Client Windows job 91353213087.
  - command: cargo deny check --all-features
    result: PASS
    evidence: Rust Client Supply Chain job 91353213100.
  - command: repository CI / Required
    result: PASS
    evidence: CI job 91353329580.
blockers:
  - Final documentation-head CI and review gate remain pending.
next_action: Complete exact-head CI, changed-file review and merge PR #127.
```
