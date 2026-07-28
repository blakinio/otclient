---
task_id: OTC-20260728-windows-platform-evidence
status: awaiting_ci
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R02
parallel_wave: OTERYN-W2-DIAGNOSTICS-EVIDENCE
parallel_lane: W2-PR
parallel_lane_state: validating
branch: docs/OTC-20260728-windows-platform-evidence
base_branch: main
created: 2026-07-28T23:58:00+02:00
updated: 2026-07-29T00:02:00+02:00
last_verified_commit: "a8f830d2193b919f1e7b3a79bfd30da4daa02a9d"
required_base_commit: "048414f9457f6adaf6c3f94f8a8e6b92d624389d"
risk: low
related_pr: "#67"
depends_on:
  - merged foundation audit PR #47
  - merged diagnostics PR #61
owned_paths:
  - oteryn-client/docs/research/windows-platform/**
  - docs/agents/tasks/active/OTC-20260728-windows-platform-evidence.md
shared_path_lease: []
contract_role: none
contracts_produced: []
contracts_consumed:
  - accepted Windows-first architecture
  - merged foundation and diagnostics contracts
crates_touched: []
features_touched: []
contracts_touched:
  - evidence only; no accepted platform API
modules_touched: []
reuses:
  - foundation platform/hardware audit
  - official winit/raw-window-handle documentation
  - Microsoft Win32 DPI/input/IME/lifecycle documentation
public_interfaces:
  - documentation evidence only
cross_repo_tasks: []
performance_evidence:
  - no runtime or performance claim
security_evidence:
  - no native code, unsafe, FFI, secrets or private captures
---

# Goal

Evaluate current primary Windows window/event/DPI/IME/raw-input/shutdown evidence and Rust dependency candidates, then recommend one bounded Windows application-shell spike without adding code, dependencies, workflows or architecture changes.

# Acceptance criteria

- [x] Window/event, DPI, IME, input, focus, resize/minimize and shutdown requirements are explicit.
- [x] Current candidate versions, licenses, MSRV and dependency roles are recorded from primary sources.
- [x] Main-thread ownership and deterministic shutdown ordering are defined without selecting an async runtime.
- [x] Minimum Windows support remains unknown because exact runtime evidence is absent.
- [x] One bounded implementation spike is recommended with exact acceptance and non-goals.
- [x] No Cargo, lockfile, platform/app crate, workflow, architecture or external-repository change.
- [ ] Exact-head required CI passes; task merges and archives independently.

# Delivered evidence

- `README.md`: exact evidence boundary, findings and primary references.
- `WINDOW_AND_EVENT_REQUIREMENTS.md`: window lifecycle, DPI, IME, input and event observations.
- `DEPENDENCY_EVALUATION.md`: winit/raw-window-handle/direct-Win32 roles, versions, licenses, MSRV and selection gates.
- `THREAD_AND_SHUTDOWN_MODEL.md`: main-thread ownership, closed command boundary and idempotent shutdown state machine.
- `SPIKE_RECOMMENDATION.md`: one blank-window winit-only application-shell package with named Windows runtime acceptance.

# Material findings

1. Main thread must own the event loop, window creation, DPI/IME policy and lifecycle coordination.
2. `winit 0.30.13` is the recommended spike candidate, not an accepted production dependency.
3. `raw-window-handle 0.6.2` is interop only and should not be direct unless a later renderer boundary needs it.
4. Direct Win32 bindings are deferred until a measured winit gap proves the need.
5. Raw Input registration must be application-owned because Windows allows one target window per device class per process.
6. Exact minimum Windows version and DPI/IME/device compatibility remain blocked on named runtime evidence.

# Validation

| Revision | Check | Result |
|---|---|---|
| `048414f9457f6adaf6c3f94f8a8e6b92d624389d` | live ownership/preflight | PASS |
| `a8f830d2193b919f1e7b3a79bfd30da4daa02a9d` | complete six-file content/scope review | PASS |
| final task-record head | exact-head required CI | pending |

# Boundaries preserved

- no product/window code or dependency selection;
- no direct Win32, unsafe or FFI implementation;
- no GPU/surface/renderer, protocol, assets, UI or async runtime;
- no Windows release, hardware, DPI, IME, input or performance compatibility claim.

# Remaining work

1. Pass exact-head required CI.
2. Mark PR #67 ready, inspect files/diff/comments/reviews/threads/base and squash-merge.
3. Archive this task separately.

# Completion

- Final status: awaiting exact-head CI
- PR: #67
- Merge commit: pending
- Archived at: pending
