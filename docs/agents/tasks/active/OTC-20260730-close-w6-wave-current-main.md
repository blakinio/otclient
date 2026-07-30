---
task_id: OTC-20260730-close-w6-wave-current-main
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
parallel_wave: OTERYN-W6-SYNTHETIC-ASSETS
parallel_lane: W6-C
parallel_lane_state: active
branch: docs/OTC-20260730-close-w6-wave-current-main
base_branch: main
created: 2026-07-30T11:29:00+02:00
updated: 2026-07-30T11:29:00+02:00
last_verified_commit: ""
required_base_commit: "a8e95bbce06eda7eb7954843cb7833fbf87160cc"
risk: low
related_pr: pending
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

This task supersedes closed unmerged PR #96 only because that branch was created before PR #95 advanced `main`. PR #96 passed its visible exact-head workflows, but branch protection continued to report the required check as expected. No rule was bypassed and no force-push or manual shared-file conflict resolution is used.

# Acceptance criteria

- [x] Start from exact current `main` `a8e95bbce06eda7eb7954843cb7833fbf87160cc`.
- [x] Preserve one task, one fresh branch and one early draft PR lifecycle.
- [ ] Publish exactly the reviewed W6 closure changes in four coordination paths.
- [ ] Record W6 plan #90/#91 and implementation #92/#94 as complete and archived.
- [ ] Record PR #93 merged and archived by #95.
- [ ] Release every W6 Cargo, lockfile, dependency-policy and shared-document lease.
- [ ] Authorize no worker from the closed-wave record.
- [ ] Leave exactly one bounded W7 planning recommendation without accepting or launching W7.
- [ ] Pass exact-head Rust Client, repository CI, complete changed-file/diff review and no-thread gate.
- [ ] Merge through repository protection and archive this task separately.

# Live-state checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-07-30T11:29:00+02:00
head: pending
branch: docs/OTC-20260730-close-w6-wave-current-main
pr: pending
status: active
required_main: a8e95bbce06eda7eb7954843cb7833fbf87160cc
proven:
  - W6 plan PR #90/archive #91 and worker PR #92/archive #94 are merged.
  - PR #93 merged as bdb73eea3c862f31e87fca81317ab3511c3a85a0 and PR #95 archived its task as a8e95bbce06eda7eb7954843cb7833fbf87160cc.
  - Closed PR #96 was not merged and introduced no main change.
  - PR #23 remains legacy UI-only and PR #48 remains isolated operational non-merge work.
  - No active Rust task or open PR owns W7 Identity, session, directory, transport, protocol or login-composition paths.
derived:
  - A current-main closure branch avoids the stale-base required-check ambiguity without bypassing protection.
unknown: []
conflicts: []
first_failure:
  marker: closure-content-pending
  evidence: the fresh task and branch exist but the reviewed closure documentation is not yet republished.
changed_paths:
  - docs/agents/tasks/active/OTC-20260730-close-w6-wave-current-main.md
validation: []
blockers: []
next_action: Open the early draft PR, publish the reviewed four-path closure, validate and merge it, then archive this task separately.
```
