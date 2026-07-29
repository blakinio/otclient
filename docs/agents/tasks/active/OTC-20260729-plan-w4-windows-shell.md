---
task_id: OTC-20260729-plan-w4-windows-shell
status: awaiting_ci
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
parallel_wave: OTERYN-W4-WINDOWS-SHELL
parallel_lane: W4-C
parallel_lane_state: validating
branch: docs/OTC-20260729-plan-w4-windows-shell
base_branch: main
created: 2026-07-29T11:35:00+02:00
updated: 2026-07-29T11:43:00+02:00
last_verified_commit: "78c82fd73914773d18f55b9fbe26241407549b9d"
required_base_commit: "e7b251c2b898ad76655ed71c72e72c1e26f9364f"
risk: medium
related_pr: "#77"
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

- [x] Live main, active tasks, open PR ownership and expired W1-W3 lanes are recorded.
- [x] Exactly one implementation lane and one unique Cargo/lockfile/shared-document lease are authorized.
- [x] The worker adds one application package and exact-pinned `winit 0.30.13` only.
- [x] The worker reuses foundation, diagnostics and test-support contracts.
- [x] Renderer/GPU, protocol, identity, assets, audio, feature UI, persistence, async runtime and direct Win32 remain excluded.
- [x] Automated acceptance and unavailable interactive-hardware evidence are distinguished.
- [x] Current routing points to W4 and forbids W1-W3 relaunch.
- [ ] Exact-head required CI passes; plan merges and archives separately.

# Confirmed live state

- Current required main: `e7b251c2b898ad76655ed71c72e72c1e26f9364f`.
- W1, W2 and W3 are completed, archived and not launchable.
- No active Rust task or open PR owns `apps/client`, the application-shell contract or Cargo/lockfile integration.
- Open PR #23 and #37 are legacy-only; PR #48 is isolated operational non-merge work.
- Primary-source revalidation on 2026-07-29 still identifies `winit 0.30.13`, Apache-2.0, MSRV 1.70, with Windows IME fixes in the current patch release.

# Delivered plan

- `CURRENT_PARALLEL_WAVE.md` accepts exactly one W4-SHELL implementation lane.
- `COORDINATOR_AGENT.md` routes coordination to W4 and preserves W1-W3 relaunch prohibitions.
- `NEXT_WINDOWS_SHELL_AGENT.md` defines package, dependency, runtime-evidence, tests, lease and merge lifecycle.
- `docs/agents/README.md` exposes current W4 routing.

# Runtime evidence policy

GitHub-hosted Windows compilation and unit tests do not prove interactive DPI/IME/multi-monitor behavior. The worker must automate all possible acceptance and mark unavailable desktop/hardware cases explicitly blocked for compatibility claims.

# Validation

| Revision | Check | Result |
|---|---|---|
| `e7b251c2b898ad76655ed71c72e72c1e26f9364f` | live preflight, ownership and dependency evidence | PASS |
| `78c82fd73914773d18f55b9fbe26241407549b9d` | complete five-file path/content review | PASS |
| final task-record head | exact-head required CI pending |

# Boundaries preserved

- no Rust source, Cargo, lockfile, dependency policy, CI, architecture rule, protocol, asset, legacy runtime or external-repository change;
- no implementation task, branch or active shared-path lease pre-created;
- no runtime, minimum-Windows, device, DPI, IME or performance compatibility claim.

# Completion

- Final status: awaiting exact-head CI
- PR: #77
- Merge commit: pending
- Archived at: pending
