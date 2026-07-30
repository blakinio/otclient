---
task_id: OTC-20260730-close-w6-wave-current-main
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
parallel_wave: OTERYN-W6-SYNTHETIC-ASSETS
parallel_lane: W6-C
parallel_lane_state: ready
branch: docs/OTC-20260730-close-w6-wave-current-main
base_branch: main
created: 2026-07-30T11:29:00+02:00
updated: 2026-07-30T11:35:00+02:00
last_verified_commit: ""
required_base_commit: "a8e95bbce06eda7eb7954843cb7833fbf87160cc"
risk: low
related_pr: "#98"
depends_on:
  - W6 plan PR #90 and archive PR #91
  - W6-ASSET implementation PR #92 and archive PR #94
  - merged legacy PR #93 and task archive PR #95
supersedes:
  - closed unmerged PR #96 and task OTC-20260730-close-w6-synthetic-assets-wave because its branch predated PR #95
owned_paths:
  - oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
  - oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md
  - docs/agents/README.md
  - docs/agents/tasks/active/OTC-20260730-close-w6-wave-current-main.md
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
  - reviewed four-path documentation from closed unmerged PR #96
  - archived W6 plan and implementation records
public_interfaces:
  - coordination documentation only
cross_repo_tasks: []
performance_evidence:
  - no runtime or product-performance claim
security_evidence:
  - no secrets, credentials, captures, proprietary assets, dependencies or external-repository writes
---

# Goal

Close `OTERYN-W6-SYNTHETIC-ASSETS` from exact current `main`, release every W6 lease, prohibit relaunch and leave exactly one bounded recommendation to create a separate `OTERYN-W7-TECHNICAL-LOGIN` planning task.

This task supersedes closed unmerged PR #96 only because that branch was created before PR #95 advanced `main`. PR #96 passed visible exact-head workflows, but branch protection continued to report the required check as expected. No rule was bypassed and no force-push or manual shared-file conflict resolution was used.

# Acceptance criteria

- [x] Start from exact current `main` `a8e95bbce06eda7eb7954843cb7833fbf87160cc`.
- [x] Preserve one task, one fresh branch and one early draft PR lifecycle.
- [x] Publish exactly the reviewed W6 closure changes in four coordination paths.
- [x] Record W6 plan #90/#91 and implementation #92/#94 as complete and archived.
- [x] Record PR #93 merged and archived by #95.
- [x] Release every W6 Cargo, lockfile, dependency-policy and shared-document lease.
- [x] Authorize no worker from the closed-wave record.
- [x] Leave exactly one bounded W7 planning recommendation without accepting or launching W7.
- [ ] Pass exact-head Rust Client, repository CI, complete changed-file/diff review and no-thread gate.
- [ ] Merge through repository protection and archive this task separately.

# Completed evidence

| Work | Delivery | Merge | Archive | Archive merge |
|---|---:|---|---:|---|
| W6 plan | PR #90 | `e27a4f15fa30f03abfcd6f265f900922eb1312f0` | PR #91 | `8094d9075fecd7b7c3de0d1b0eb400207a839776` |
| W6-ASSET | PR #92 | `3cea444505bfcc5dc4b08b12d1046ef0c34a0f7a` | PR #94 | `4e09e32032e64831c30d6f7aeb31a2ebd4d4520a` |
| legacy options task | PR #93 | `bdb73eea3c862f31e87fca81317ab3511c3a85a0` | PR #95 | `a8e95bbce06eda7eb7954843cb7833fbf87160cc` |

PR #92 final feature head `c51b24c489b181bc8a950a94d1fdf272bc60be7a` passed Rust Client run `30494659925` and repository CI run `30494660024`. PR #94 separately archived the implementation and released its lease.

Closed unmerged PR #96 exact head `1c7d9f5c6be335ab09e52792e352e4c5455ec2c6` passed Rust Client run `30530338692` and repository CI run `30530338882`; it was superseded rather than force-updated because its base predated PR #95.

# Live-state checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-30T11:35:00+02:00
head: pending-current-commit
branch: docs/OTC-20260730-close-w6-wave-current-main
pr: 98
status: ready
required_main: a8e95bbce06eda7eb7954843cb7833fbf87160cc
proven:
  - W6 plan PR #90/archive #91 and worker PR #92/archive #94 are merged.
  - PR #93 merged and PR #95 separately archived its task.
  - Closed PR #96 was not merged and introduced no main change.
  - PR #23 remains legacy UI-only and PR #48 remains isolated operational non-merge work.
  - No active Rust task or open PR owns W7 Identity, account-session, world-directory, game-entry, transport, protocol-canary or login-composition paths.
  - The current PR publishes exactly four coordination paths and no product/dependency/workflow change.
derived:
  - W6 is complete, archived and no longer launchable.
  - Every previous Rust shared-path lease is released.
  - The only next recommendation is a separate W7 planning task and draft PR.
unknown: []
conflicts: []
first_failure:
  marker: exact-head-validation-pending
  evidence: the published current-main closure head must pass required checks before merge.
changed_paths:
  - docs/agents/README.md
  - docs/agents/tasks/active/OTC-20260730-close-w6-wave-current-main.md
  - oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
  - oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md
validation: []
blockers: []
next_action: Complete exact-head CI, full diff and review-thread inspection, merge PR #98, then archive this task separately before creating the W7 plan.
```
