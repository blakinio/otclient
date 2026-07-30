---
task_id: OTC-20260730-close-w6-current-main
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
parallel_wave: OTERYN-W6-SYNTHETIC-ASSETS
parallel_lane: W6-C
parallel_lane_state: validating
branch: docs/OTC-20260730-close-w6-current-main
base_branch: main
created: 2026-07-30T11:30:00+02:00
updated: 2026-07-30T11:36:00+02:00
last_verified_commit: "3f7213bcff0b67aaddc6d8d662480669f3a8e345"
required_base_commit: "a8e95bbce06eda7eb7954843cb7833fbf87160cc"
risk: low
related_pr: "#99"
depends_on:
  - W6 plan PR #90 and archive PR #91
  - W6-ASSET implementation PR #92 and archive PR #94
  - merged legacy PR #93 and task archive PR #95
owned_paths:
  - docs/agents/README.md
  - docs/agents/tasks/active/OTC-20260730-close-w6-current-main.md
  - oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
  - oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md
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

Close `OTERYN-W6-SYNTHETIC-ASSETS` from current `main`, release every W6 lease, prohibit W6 relaunch and leave exactly one bounded recommendation to plan `OTERYN-W7-TECHNICAL-LOGIN` in a separate planning task.

This task does not accept W7, create worker lanes, implement Rust packages, add dependencies or claim Identity/Gateway/Canary compatibility.

# Acceptance criteria

- [x] Reconcile exact current `main`, active tasks, open PRs and W6 merge/archive evidence.
- [x] Record W6 plan PR #90/archive #91 and implementation PR #92/archive #94 as complete.
- [x] Replace the stale launchable W6 record with a closed record that authorizes no worker.
- [x] Record that all W6 Cargo, lockfile, dependency-policy and shared-document leases are released.
- [x] Update coordinator routing without claiming W7 acceptance.
- [x] Leave exactly one next recommendation: plan `OTERYN-W7-TECHNICAL-LOGIN` after fresh contract and ownership preflight.
- [x] Review the exact changed-file list and complete diff; exactly four authorized coordination paths changed.
- [ ] Pass exact-head Rust Client and repository CI.
- [ ] Merge through repository gates and archive this task separately before W7 planning begins.

# Evidence

| Work | Delivery | Merge | Archive | Archive merge |
|---|---:|---|---:|---|
| W6 plan | PR #90 | `e27a4f15fa30f03abfcd6f265f900922eb1312f0` | PR #91 | `8094d9075fecd7b7c3de0d1b0eb400207a839776` |
| W6-ASSET | PR #92 | `3cea444505bfcc5dc4b08b12d1046ef0c34a0f7a` | PR #94 | `4e09e32032e64831c30d6f7aeb31a2ebd4d4520a` |
| legacy options hardening | PR #93 | `bdb73eea3c862f31e87fca81317ab3511c3a85a0` | PR #95 | `a8e95bbce06eda7eb7954843cb7833fbf87160cc` |

# Live-state checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-30T11:36:00+02:00
head: pending-current-commit
branch: docs/OTC-20260730-close-w6-current-main
pr: 99
status: validating
required_main: a8e95bbce06eda7eb7954843cb7833fbf87160cc
proven:
  - W6 plan, worker and both lifecycle archives are merged.
  - PR #23 remains legacy presentation only.
  - PR #48 remains isolated operational non-merge work.
  - PR #97 owns legacy asset rehearsal only.
  - No active Rust task or open PR owns Identity, account-session, directory, game-entry, transport, protocol-canary, technical-login composition or login E2E paths.
  - All prior Rust shared-path leases are released.
  - PR #99 changes exactly four authorized coordination paths and the complete diff was reviewed.
derived:
  - CURRENT_PARALLEL_WAVE.md on main was stale because it still authorized the completed W6 worker.
unknown: []
conflicts: []
first_failure: null
changed_paths:
  - docs/agents/README.md
  - docs/agents/tasks/active/OTC-20260730-close-w6-current-main.md
  - oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
  - oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md
validation:
  - command: complete PR #99 changed-file and diff review
    result: PASS
    evidence: exactly four authorized coordination paths; no product/dependency/workflow/external-repository change
blockers: []
next_action: Mark PR #99 ready, wait for exact-head required checks and merge only through the repository gate; archive this task separately before W7 planning.
```
