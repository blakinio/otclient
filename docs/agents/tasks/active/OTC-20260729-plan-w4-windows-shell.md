---
task_id: OTC-20260729-plan-w4-windows-shell
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
parallel_wave: OTERYN-W4-WINDOWS-SHELL
parallel_lane: W4-C
parallel_lane_state: active
branch: docs/OTC-20260729-plan-w4-windows-shell
base_branch: main
created: 2026-07-29T11:35:00+02:00
updated: 2026-07-29T11:35:00+02:00
last_verified_commit: "e7b251c2b898ad76655ed71c72e72c1e26f9364f"
required_base_commit: "e7b251c2b898ad76655ed71c72e72c1e26f9364f"
risk: medium
related_pr: pending
depends_on:
  - completed/archived W3 through PR #76
  - merged Windows platform evidence PR #67
  - merged foundation, diagnostics and test-support contracts
owned_paths:
  - oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
  - oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md
  - oteryn-client/docs/agents/prompts/NEXT_WINDOWS_SHELL_AGENT.md
  - docs/agents/README.md
  - docs/agents/tasks/active/OTC-20260729-plan-w4-windows-shell.md
shared_path_lease: []
contract_role: none
contracts_produced: []
contracts_consumed:
  - W2 Windows platform evidence
  - merged foundation/diagnostics/test-support contracts
crates_touched: []
features_touched: []
contracts_touched:
  - W4 launch routing only
modules_touched: []
reuses:
  - winit 0.30.13 primary-source evidence
  - architecture category app
  - existing Windows Rust CI and cargo-deny policy
public_interfaces:
  - coordination documentation only
cross_repo_tasks: []
performance_evidence:
  - no runtime or performance claim
security_evidence:
  - no secrets, native FFI, proprietary assets or external-repository writes
---

# Goal

Create one accepted W4 plan for a bounded Windows blank-window application-shell spike without implementing it in this coordination task.

# Acceptance criteria

- [ ] Live main, active tasks, open PR ownership and expired W1-W3 lanes are recorded.
- [ ] Exactly one implementation lane and one unique Cargo/lockfile/shared-document lease are authorized.
- [ ] The worker adds one application package and exact-pinned `winit 0.30.13` only.
- [ ] The worker reuses foundation, diagnostics and test-support contracts.
- [ ] Renderer/GPU, protocol, identity, assets, audio, feature UI, persistence, async runtime and direct Win32 remain excluded.
- [ ] Automated acceptance and unavailable interactive-hardware evidence are distinguished.
- [ ] Current routing points to W4 and forbids W1-W3 relaunch.
- [ ] Exact-head required CI passes; plan merges and archives separately.

# Confirmed live state

- Current main: `e7b251c2b898ad76655ed71c72e72c1e26f9364f`.
- W1, W2 and W3 are completed, archived and not launchable.
- No active Rust task or open PR owns `apps/client`, the application-shell contract or Cargo/lockfile integration.
- Open PR #23 and #37 are legacy-only; PR #48 is isolated operational non-merge work.
- Primary-source revalidation on 2026-07-29 still identifies `winit 0.30.13`, Apache-2.0, MSRV 1.70, with Windows IME fixes in the current patch release.

# Planned worker

One lane `W4-SHELL` will add one `oteryn-client` application package under `oteryn-client/apps/client/`, exact-pin `winit = "=0.30.13"`, implement a deterministic shell state machine and one blank Windows window, and record exact automated plus named-runtime evidence boundaries.

# Runtime evidence policy

GitHub-hosted Windows compilation and unit tests do not prove interactive DPI/IME/multi-monitor behavior. The worker must:

- automate all state-machine and dependency checks;
- run only runtime checks that the exact runner can genuinely support;
- record unavailable desktop, multi-monitor, IME and physical-input cases as explicit blockers rather than inferred passes;
- make no minimum-Windows or hardware compatibility claim.

# Validation

| Revision | Check | Result |
|---|---|---|
| `e7b251c2b898ad76655ed71c72e72c1e26f9364f` | live preflight, ownership and dependency evidence | PASS |

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Archived at: pending
