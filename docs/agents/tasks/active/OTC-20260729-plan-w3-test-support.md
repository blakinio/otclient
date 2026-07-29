---
task_id: OTC-20260729-plan-w3-test-support
status: ready_for_review
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
parallel_wave: OTERYN-W3-TEST-SUPPORT
parallel_lane: W3-C
parallel_lane_state: ready_for_review
branch: docs/OTC-20260729-plan-w3-test-support
base_branch: main
created: 2026-07-29T09:24:00+02:00
updated: 2026-07-29T09:38:00+02:00
last_verified_commit: "07b38e860acdd37faba5ff9847736ae10685b0b4"
required_base_commit: "0b1cd7914c04efd6b41a4a1b975234df715e6104"
risk: low
related_pr: "#71"
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

- [x] Live `main`, active tasks and open PR ownership are recorded.
- [x] W3 has exactly one implementation lane and one unique shared-path lease holder.
- [x] The worker scope consumes `ManualClock` and diagnostics rather than duplicating them.
- [x] No async runtime, executor, scheduler, global registry or product integration is authorized.
- [x] Current coordinator/discovery routing points to W3 and forbids W1/W2 relaunch.
- [x] Exact-head required CI passes; plan merges and archives separately.

# Confirmed live state

- Current required `main`: `0b1cd7914c04efd6b41a4a1b975234df715e6104`.
- W1 and W2 are completed/archived and not launchable.
- Open PRs #23 and #37 own legacy paths; PR #48 is isolated operational work.
- No active Rust task or open PR owns `crates/test-support`, Cargo/lockfile integration or the test-support public surface.

# Delivered plan

- `CURRENT_PARALLEL_WAVE.md` accepts exactly one W3 implementation lane.
- `COORDINATOR_AGENT.md` routes coordination to W3 and preserves historical-wave prohibitions.
- `NEXT_TEST_SUPPORT_AGENT.md` defines the bounded worker package, tests, lease and merge lifecycle.
- `docs/agents/README.md` exposes current launch routing.

# Validation

| Evidence | Result |
|---|---|
| live preflight on `0b1cd7914c04efd6b41a4a1b975234df715e6104` | PASS |
| complete five-file path/content/full-diff review on `07b38e860acdd37faba5ff9847736ae10685b0b4` | PASS |
| Rust Client run `30431875004` | PASS: Windows workspace and Supply Chain |
| repository CI run `30431875234` | PASS: all required jobs and `CI / Required` |
| final task-record head | exact-head rerun required before merge |

# Boundaries preserved

- no Rust source, Cargo, lockfile, architecture, CI, protocol, asset, legacy runtime or external-repository change;
- no package implementation or pre-created worker branch/lease;
- no runtime, platform, server or performance compatibility claim.

# Completion

- Final status: ready after final exact-head rerun
- PR: #71
- Merge commit: pending
- Archived at: pending
