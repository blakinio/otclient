---
task_id: OTC-20260729-close-w3-test-support-wave
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
parallel_wave: OTERYN-W3-TEST-SUPPORT
parallel_lane: W3-C
parallel_lane_state: active
branch: docs/OTC-20260729-close-w3-test-support-wave
base_branch: main
created: 2026-07-29T11:02:00+02:00
updated: 2026-07-29T11:02:00+02:00
last_verified_commit: "3431ecbecdd104df35cd569fa353a94fbe8ee67e"
required_base_commit: "3431ecbecdd104df35cd569fa353a94fbe8ee67e"
risk: low
related_pr: pending
depends_on:
  - W3 plan PR #71 and archive PR #72
  - W3 implementation PR #73 and archive PR #74
owned_paths:
  - oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
  - oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md
  - docs/agents/README.md
  - docs/agents/tasks/active/OTC-20260729-close-w3-test-support-wave.md
shared_path_lease: []
contract_role: none
contracts_produced: []
contracts_consumed:
  - merged deterministic test-support contract from PR #73
  - merged Windows platform evidence from PR #67
crates_touched: []
features_touched: []
contracts_touched:
  - completed W3 status and future launch routing only
modules_touched: []
reuses:
  - archived W3 task records and exact CI evidence
  - Gate 1 package order
  - W2 Windows platform evidence
public_interfaces:
  - coordination documentation only
cross_repo_tasks: []
performance_evidence:
  - no runtime or performance claim
security_evidence:
  - no secrets, assets, captures or external-repository writes
---

# Goal

Close `OTERYN-W3-TEST-SUPPORT` durably, prevent its relaunch, prove all leases are released and leave exactly one next bounded package without implementing or pre-claiming it.

# Acceptance criteria

- [ ] W3 plan and implementation are recorded as merged and archived with exact evidence.
- [ ] No W3 lane remains launchable and no W3 shared-path lease remains active.
- [ ] Current routing no longer instructs agents to launch W3.
- [ ] Open unrelated legacy/operational PRs remain distinguished from Rust ownership.
- [ ] Exactly one next bounded package is recommended from merged evidence.
- [ ] The next package is not implemented, tasked, branched or leased here.
- [ ] No Rust source, Cargo, lockfile, CI, architecture, protocol, asset, legacy runtime or external-repository change.
- [ ] Exact-head required CI passes; closure merges and archives separately.

# Confirmed live state

- Current `main`: `3431ecbecdd104df35cd569fa353a94fbe8ee67e`.
- W3 plan/archive: PR #71 merge `15ed1dbecdd05d4eabe6d6d1e667febbcbd122dd`; PR #72 archive `9bb2f60d780d2ea6723015876cf95c7fa5e3cbfe`.
- W3 implementation/archive: PR #73 merge `5d768bd08ec1040c1f283467e8cd2753f20bc3ac`; PR #74 archive `3431ecbecdd104df35cd569fa353a94fbe8ee67e`.
- W3-TEST Cargo/lockfile/shared-document lease is released.
- Open PRs #23 and #37 remain legacy-only; PR #48 remains isolated operational non-merge work.

# Next recommendation

Recommend exactly one next bounded package: the blank-window Windows application-shell spike described by merged W2-PR evidence.

Required envelope:

- one small application/platform vertical slice only;
- main-thread event loop and deterministic shutdown ordering;
- current primary dependency/version/license/MSRV revalidation before Cargo changes;
- no renderer/GPU surface, protocol, identity, assets, audio, feature UI or async runtime;
- named Windows runtime evidence for DPI, resize/minimize, focus, IME and close behavior;
- one unique Cargo/lockfile/shared-document lease after a separate accepted plan.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Archived at: pending
