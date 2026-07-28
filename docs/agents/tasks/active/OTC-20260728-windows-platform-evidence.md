---
task_id: OTC-20260728-windows-platform-evidence
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R02
parallel_wave: OTERYN-W2-DIAGNOSTICS-EVIDENCE
parallel_lane: W2-PR
parallel_lane_state: active
branch: docs/OTC-20260728-windows-platform-evidence
base_branch: main
created: 2026-07-28T23:58:00+02:00
updated: 2026-07-28T23:58:00+02:00
last_verified_commit: "048414f9457f6adaf6c3f94f8a8e6b92d624389d"
required_base_commit: "048414f9457f6adaf6c3f94f8a8e6b92d624389d"
risk: low
related_pr: pending
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

- [ ] Window/event, DPI, IME, input, focus, resize/minimize and shutdown requirements are explicit.
- [ ] Current candidate versions, licenses, MSRV and dependency roles are recorded from primary sources.
- [ ] Main-thread ownership and deterministic shutdown ordering are defined without selecting an async runtime.
- [ ] Minimum Windows support remains unknown unless exact evidence proves it.
- [ ] One bounded implementation spike is recommended with exact acceptance and non-goals.
- [ ] No Cargo, lockfile, platform/app crate, workflow, architecture or external-repository change.
- [ ] Exact-head required CI passes; task merges and archives independently.

# Confirmed context

- Current `main` is `048414f9457f6adaf6c3f94f8a8e6b92d624389d`.
- Foundation audit records Windows-first requirements but no exact minimum Windows version or accepted window/event dependency.
- Current primary documentation identifies `winit 0.30.13` (Apache-2.0, Rust 1.70) and `raw-window-handle 0.6.2` (MIT OR Apache-2.0 OR Zlib, Rust 1.64) as candidates; neither is accepted by this evidence task.
- The current workspace uses Rust 1.94.0.
- No active task/PR owns `oteryn-client/docs/research/windows-platform/**`.

# Boundaries

- no product/window code or Cargo dependency selection;
- no direct Win32/unsafe/FFI implementation;
- no GPU/surface/renderer work;
- no compatibility claim for a Windows release or hardware tier;
- no async runtime or scheduler decision.

# Plan

1. Open an early draft PR.
2. Record normative event/window requirements and primary-source references.
3. Evaluate winit/raw-window-handle/direct Win32 roles and supply-chain boundaries.
4. Define main-thread/shutdown ownership and one bounded spike.
5. Validate, merge and archive separately.

# Validation

| Revision | Check | Result |
|---|---|---|
| `048414f9457f6adaf6c3f94f8a8e6b92d624389d` | live ownership/preflight | PASS |

# Remaining work

1. Open draft PR and write the evidence package.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Archived at: pending
