---
task_id: OTC-20260730-close-w6-synthetic-assets-wave
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
parallel_wave: OTERYN-W6-SYNTHETIC-ASSETS
parallel_lane: W6-C
parallel_lane_state: active
branch: docs/OTC-20260730-close-w6-synthetic-assets-wave
base_branch: main
created: 2026-07-30T10:52:00+02:00
updated: 2026-07-30T10:52:00+02:00
last_verified_commit: ""
required_base_commit: "4e09e32032e64831c30d6f7aeb31a2ebd4d4520a"
risk: low
related_pr: pending
depends_on:
  - W6 plan PR #90 and archive PR #91
  - W6-ASSET implementation PR #92 and archive PR #94
owned_paths:
  - oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
  - oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md
  - docs/agents/README.md
  - docs/agents/tasks/active/OTC-20260730-close-w6-synthetic-assets-wave.md
shared_path_lease: []
contract_role: none
contracts_produced: []
contracts_consumed:
  - merged and archived W6 plan lifecycle
  - merged and archived W6 synthetic asset schema/compiler lifecycle
crates_touched: []
features_touched: []
contracts_touched:
  - W6 coordination state and future planning authorization only
modules_touched: []
reuses:
  - archived W6 plan and implementation task records
  - exact W6 CI, merge and archive evidence
public_interfaces:
  - coordination documentation only
cross_repo_tasks: []
performance_evidence:
  - no runtime, compiler-throughput or product-performance claim
security_evidence:
  - no secrets, credentials, captures, proprietary assets, dependencies or external-repository writes
---

# Goal

Close `OTERYN-W6-SYNTHETIC-ASSETS` after its plan, implementation and lifecycle archives have merged; release every W6 lease; prohibit W6 relaunch; and leave exactly one bounded recommendation to create a separate W7 technical-login planning task.

This task does not accept W7, create worker lanes, implement Rust packages, add dependencies or claim Identity/Gateway/Canary compatibility.

# Acceptance criteria

- [ ] Reconcile exact current `main`, active tasks, open PRs and W6 merge/archive evidence.
- [ ] Record W6 plan PR #90/archive #91 and implementation PR #92/archive #94 as complete.
- [ ] Replace the launchable W6 record in `CURRENT_PARALLEL_WAVE.md` with a closed-wave record that authorizes no worker.
- [ ] Record that all W6 Cargo, lockfile, dependency-policy and shared-document leases are released.
- [ ] Preserve W6 synthetic-only and non-production boundaries.
- [ ] Update the coordinator prompt so any future wave requires a new planning task, draft PR, accepted plan and separate plan archive before worker launch.
- [ ] Update `docs/agents/README.md` routing without claiming W7 acceptance.
- [ ] Leave exactly one bounded next recommendation: plan `OTERYN-W7-TECHNICAL-LOGIN` after fresh live contract/ownership preflight.
- [ ] Final exact-head required CI and complete changed-file/review inspection pass.
- [ ] Merge through repository gates and archive this task separately.

# Live-state checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-30T10:52:00+02:00
head: pending
branch: docs/OTC-20260730-close-w6-synthetic-assets-wave
pr: pending
status: active
required_main: 4e09e32032e64831c30d6f7aeb31a2ebd4d4520a
proven:
  - PR #90 planned W6 and PR #91 archived that planning task.
  - PR #92 merged the bounded synthetic asset schema/compiler as 3cea444505bfcc5dc4b08b12d1046ef0c34a0f7a.
  - PR #94 archived W6-ASSET and current main is 4e09e32032e64831c30d6f7aeb31a2ebd4d4520a.
  - PR #93 is open legacy Lua/test work and does not own Rust Identity, session, transport, protocol or application-entry paths.
  - PR #48 remains isolated operational non-merge work and PR #23 remains legacy UI-only.
derived:
  - CURRENT_PARALLEL_WAVE.md is stale because it still authorizes W6-ASSET after the lane was merged and archived.
  - W6 must be closed through this separate lifecycle task before a W7 plan can be accepted.
unknown: []
conflicts: []
first_failure:
  marker: stale-current-wave-record
  evidence: CURRENT_PARALLEL_WAVE.md still has status accepted launch plan for OTERYN-W6-SYNTHETIC-ASSETS.
changed_paths:
  - docs/agents/tasks/active/OTC-20260730-close-w6-synthetic-assets-wave.md
validation: []
blockers: []
next_action: Publish the bounded W6 closure documentation, validate it, merge it and archive this task before creating the W7 planning task.
```
