---
task_id: OTC-20260729-plan-w3-test-support
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
parallel_wave: OTERYN-W3-TEST-SUPPORT
parallel_lane: W3-C
parallel_lane_state: active
branch: docs/OTC-20260729-plan-w3-test-support
base_branch: main
created: 2026-07-29T09:24:00+02:00
updated: 2026-07-29T09:24:00+02:00
last_verified_commit: "0b1cd7914c04efd6b41a4a1b975234df715e6104"
required_base_commit: "0b1cd7914c04efd6b41a4a1b975234df715e6104"
risk: low
related_pr: pending
depends_on:
  - completed/archived W2 at PR #70
owned_paths:
  - oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
  - oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md
  - oteryn-client/docs/agents/prompts/NEXT_TEST_SUPPORT_AGENT.md
  - docs/agents/README.md
  - docs/agents/tasks/active/OTC-20260729-plan-w3-test-support.md
shared_path_lease: []
contract_role: none
contracts_produced: []
contracts_consumed:
  - merged foundation contract from PR #54
  - merged diagnostics contract from PR #61
crates_touched: []
features_touched: []
contracts_touched:
  - W3 launch routing only
modules_touched: []
reuses:
  - closed W2 evidence and recommendation
  - Gate 1 package order
  - multi-agent execution protocol
public_interfaces:
  - coordination documentation only
cross_repo_tasks: []
performance_evidence:
  - no runtime or performance claim
security_evidence:
  - no secrets, assets, captures or external-repository writes
---

# Goal

Create one accepted, bounded W3 launch plan for deterministic Rust test support and fake-time helpers without implementing the package in this coordination task.

# Acceptance criteria

- [ ] Live `main`, active tasks and open PR ownership are recorded.
- [ ] W3 has exactly one implementation lane and one unique shared-path lease holder.
- [ ] The worker scope consumes `ManualClock` and diagnostics rather than duplicating them.
- [ ] No async runtime, executor, scheduler, global registry or product integration is authorized.
- [ ] Current coordinator/discovery routing points to W3 and forbids W1/W2 relaunch.
- [ ] Exact-head required CI passes; plan merges and archives separately.

# Confirmed live state

- Current `main`: `0b1cd7914c04efd6b41a4a1b975234df715e6104`.
- W1 and W2 are completed/archived and not launchable.
- Open PRs #23 and #37 own legacy paths; PR #48 is isolated operational work.
- No active Rust task or open PR owns `crates/test-support`, Cargo/lockfile integration or the test-support public surface.

# Planned worker

One lane `W3-TEST` will add one small `oteryn-test-support` crate with deterministic test-owned builders around merged foundation and diagnostics contracts.

# Validation

| Revision | Check | Result |
|---|---|---|
| `0b1cd7914c04efd6b41a4a1b975234df715e6104` | live preflight and overlap review | PASS |

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Archived at: pending
