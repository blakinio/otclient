---
task_id: OTC2-20260801-nonblocking-shutdown-remediation
status: active
agent: "GPT-5.6 Thinking"
lane: otclient-v2
track: greenfield-rust
workstream: lifecycle
phase: implementation
branch: fix/OTC2-20260801-nonblocking-shutdown-remediation
base_branch: main
created: 2026-08-01T09:52:00+02:00
updated: 2026-08-01T09:52:00+02:00
last_verified_commit: "43ed867910907cd4ebcf9f14e64977105d08ab7e"
required_base_commit: "43ed867910907cd4ebcf9f14e64977105d08ab7e"
risk: high
related_pr: "pending"
depends_on:
  - OTC2-20260801-secret-lifecycle-remediation
  - R1 implementation merge c6d11a6c26f75c2169913e297c14b0ec25419736
  - R1 archive merge 43ed867910907cd4ebcf9f14e64977105d08ab7e
blocks:
  - OTC2-20260801-complete-architecture-policy
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-nonblocking-shutdown-remediation.md
  - oteryn-client/crates/app-runtime/src/model.rs
  - oteryn-client/crates/app-runtime/src/runtime.rs
  - oteryn-client/crates/app-runtime/src/worker.rs
  - oteryn-client/crates/app-runtime/src/lib.rs
  - oteryn-client/crates/app-runtime/src/tests.rs
  - oteryn-client/apps/client/src/main.rs
  - oteryn-client/apps/client/src/technical_login.rs
  - oteryn-client/crates/transport/src/lib.rs
  - oteryn-client/crates/identity/src/lib.rs only if the callback observation constant/test needs naming
  - oteryn-client/docs/architecture/TECHNICAL_LOGIN.md
  - oteryn-client/docs/research/technical-login/W7_LOGIN_E2E_EVIDENCE.md
shared_path_lease:
  - pending narrow transfer from PR #23 for the W7 app-runtime catalogue row and one bounded R2 changelog entry
modules_touched: []
crates_touched:
  - oteryn-app-runtime
  - oteryn-transport
  - oteryn-identity only for an existing callback cancellation-bound constant or test
features_touched:
  - technical-login shutdown lifecycle
  - bounded synchronous I/O configuration
reuses:
  - existing CancellationSource and owned JoinHandle workers
  - existing event-loop proxy signal and 16 ms active poll cadence
  - existing bounded Ureq global timeout
contracts_produced:
  - nonblocking begin/poll shutdown state machine
  - typed pending, overdue and complete shutdown progress
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

Remediate `OTC2-AUD-002` so Windows event-loop shutdown never joins an unfinished technical-login worker, while retaining deterministic ownership and bounded synchronous I/O.

# Fresh preflight

- exact launch `main`: `43ed867910907cd4ebcf9f14e64977105d08ab7e`;
- R1 implementation PR #124 and archive PR #126 are merged;
- open PRs #23, #48 and #97 were inspected;
- none owns `oteryn-app-runtime`, `apps/client` Rust shell composition, `oteryn-transport`, `oteryn-identity` or the owned technical-login evidence paths;
- PR #23 still owns `docs/agents/MODULE_CATALOG.md` and `docs/agents/CHANGELOG.md`; no edit is allowed until a narrow durable transfer is recorded;
- no active task or open PR for `OTC2-AUD-002` exists;
- required gates remain Rust Client Windows, Supply Chain and repository `CI / Required`.

# Confirmed blocking paths

- `TechnicalLoginRuntime::cancel_active`, `disconnect_to_logged_out`, `shutdown` and `Drop` currently reach synchronous worker joins;
- `ShellApplication::request_exit` calls technical-login shutdown before `event_loop.exit()`;
- `ShellApplication::exiting` repeats technical-login shutdown;
- `poll` already joins only workers whose `JoinHandle::is_finished()` is true;
- worker completion already sends a user-event signal, and `about_to_wait` already provides a 16 ms fallback while a worker is active;
- Ureq already enforces a non-zero global timeout no greater than 30 seconds;
- Identity callback read slices already use at most 250 milliseconds within a callback deadline no greater than 300 seconds;
- `TransportConfig` rejects zero timeouts but currently accepts values above 30 seconds.

# Accepted state machine

- `begin_shutdown` records one monotonic start moment, marks closing and cancels the active worker without joining it;
- `poll_shutdown` joins only after `is_finished()` and then returns `Complete`;
- while unfinished, it returns typed `Pending(worker_kind)`;
- after 31 seconds, it returns typed `Overdue(worker_kind)` but retains, owns and continues polling the worker;
- no worker is detached, force-terminated, forgotten or replaced by an unowned reaper;
- application exit releases renderer/window and calls `event_loop.exit()` only after technical-login shutdown reports `Complete`;
- worker completion signals wake the event loop; a 16 ms `WaitUntil` remains the bounded fallback;
- the runtime `Drop` fallback may synchronously join only as an ownership invariant outside the event-loop exit path; the event-loop path must prove completion before controller drop.

# I/O bounds

- Ureq global timeout remains configurable from 1 second through 30 seconds;
- TCP connect, read and write timeout configuration becomes configurable from greater than zero through 30 seconds;
- callback deadline remains configurable through 300 seconds;
- callback accept/read cancellation remains observable in at most 250 milliseconds;
- no automatic retry or reconnect is introduced.

# Acceptance

- no event-loop callback calls a function that joins an unfinished technical-login worker;
- close/failure paths begin shutdown once and continue polling until complete;
- an overdue worker produces a stable typed error/status while remaining owned;
- event-loop wake signal and 16 ms fallback both drive shutdown progress;
- renderer/window release occurs after technical worker completion and before final event-loop exit;
- TCP timeout values over 30 seconds fail configuration before network I/O;
- focused tests prove nonblocking begin/poll, overdue retention and eventual join;
- full locked workspace, strict Clippy, tests, architecture, Supply Chain and repository CI pass;
- no R3 asset-open or R4 architecture-policy implementation enters the diff.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T09:52:00+02:00
head: 43ed867910907cd4ebcf9f14e64977105d08ab7e
branch: fix/OTC2-20260801-nonblocking-shutdown-remediation
pr: null
status: active
context_routes:
  - docs/agents/AGENTS.md
  - docs/agents/EXECUTION_PROTOCOL.md
  - oteryn-client/docs/audits/post-w7/REMEDIATION_PLAN.md
  - oteryn-client/crates/app-runtime/src/runtime.rs
  - oteryn-client/apps/client/src/main.rs
  - oteryn-client/crates/transport/src/lib.rs
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-nonblocking-shutdown-remediation.md
  - oteryn-client/crates/app-runtime/src/model.rs
  - oteryn-client/crates/app-runtime/src/runtime.rs
  - oteryn-client/crates/app-runtime/src/worker.rs
  - oteryn-client/crates/app-runtime/src/lib.rs
  - oteryn-client/crates/app-runtime/src/tests.rs
  - oteryn-client/apps/client/src/main.rs
  - oteryn-client/apps/client/src/technical_login.rs
  - oteryn-client/crates/transport/src/lib.rs
  - oteryn-client/docs/architecture/TECHNICAL_LOGIN.md
  - oteryn-client/docs/research/technical-login/W7_LOGIN_E2E_EVIDENCE.md
proven:
  - Current main contains merged and archived R1 state.
  - Open PRs 23, 48 and 97 do not own affected Rust or evidence paths.
  - Current event-loop exit reaches synchronous technical-worker joins.
  - Existing completion signals and 16 ms polling can drive a nonblocking shutdown state machine.
  - Ureq and callback bounds already meet the accepted 30-second and 250-millisecond limits.
derived:
  - R2 needs no new dependency, manifest or lockfile change.
  - TransportConfig is the smallest shared enforcement point for the missing TCP hard cap.
unknown:
  - Final Windows borrow/lifecycle details until exact-head compilation validates the event-loop rewrite.
conflicts:
  - PR #23 retains catalogue/changelog ownership until a narrow transfer is recorded.
first_failure:
  marker: implementation-not-started
  evidence: Only the active task record exists on the R2 branch.
rejected_hypotheses:
  - Event-loop shutdown may synchronously join because configured I/O is usually short.
  - An overdue worker may be detached or force-terminated.
  - Callback deadline must be reduced below the accepted 300-second user-flow bound.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-nonblocking-shutdown-remediation.md
validation:
  - command: fresh main, open PR and path ownership preflight
    result: PASS
    evidence: main 43ed867910907cd4ebcf9f14e64977105d08ab7e; open PRs 23/48/97 inspected; no affected Rust overlap.
  - command: shutdown and I/O source inventory
    result: PASS
    evidence: synchronous joins, event-loop callers, Ureq bound, callback slices and missing TransportConfig cap identified.
blockers:
  - Shared catalogue/changelog edits require a narrow durable lease transfer from PR #23.
next_action: Open the draft PR and implement the nonblocking shutdown state machine on the declared paths.
```
