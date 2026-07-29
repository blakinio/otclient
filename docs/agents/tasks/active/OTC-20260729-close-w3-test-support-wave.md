---
task_id: OTC-20260729-close-w3-test-support-wave
status: awaiting_ci
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
parallel_wave: OTERYN-W3-TEST-SUPPORT
parallel_lane: W3-C
parallel_lane_state: validating
branch: docs/OTC-20260729-close-w3-test-support-wave
base_branch: main
created: 2026-07-29T11:02:00+02:00
updated: 2026-07-29T11:10:00+02:00
last_verified_commit: "0991bfdc2be0a56168996d86155684f56cbe2baa"
required_base_commit: "3431ecbecdd104df35cd569fa353a94fbe8ee67e"
risk: low
related_pr: "#75"
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

- [x] W3 plan and implementation are recorded as merged and archived with exact evidence.
- [x] No W3 lane remains launchable and no W3 shared-path lease remains active.
- [x] Current routing no longer instructs agents to launch W3.
- [x] Open unrelated legacy/operational PRs remain distinguished from Rust ownership.
- [x] Exactly one next bounded package is recommended from merged evidence.
- [x] The next package is not implemented, tasked, branched or leased here.
- [x] No Rust source, Cargo, lockfile, CI, architecture, protocol, asset, legacy runtime or external-repository change.
- [ ] Exact-head required CI passes; closure merges and archives separately.

# Delivered closure

- `CURRENT_PARALLEL_WAVE.md` is a completed/closed W3 record containing exact delivery/archive evidence and released lease state.
- `COORDINATOR_AGENT.md` is a post-W3 planning prompt and authorizes no worker launch.
- `docs/agents/README.md` treats W1/W2/W3 prompts as historical and requires a separate accepted plan.
- Exactly one non-authorizing next recommendation is recorded: a blank-window Windows application-shell spike.

# Confirmed live state

- Current required `main`: `3431ecbecdd104df35cd569fa353a94fbe8ee67e`.
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
- no renderer/GPU surface, protocol, identity, assets, audio, feature UI, persistence or async runtime;
- named Windows runtime evidence for launch/close, DPI, resize/minimize/restore, focus and IME;
- one unique Cargo/lockfile/shared-document lease after a separate accepted plan.

# Validation

| Revision | Check | Result |
|---|---|---|
| `3431ecbecdd104df35cd569fa353a94fbe8ee67e` | live W3/archive/open-PR/lease preflight | PASS |
| `0991bfdc2be0a56168996d86155684f56cbe2baa` | complete four-file path/content review | PASS |
| final task-record head | exact-head required CI pending |

# Boundaries preserved

- no Rust source, Cargo, lockfile, CI, toolchain, deny policy or architecture change;
- no protocol constant, asset byte, legacy runtime or external-repository change;
- no new accepted wave, implementation task, worker branch or active lease;
- no product/runtime/server/performance compatibility claim.

# Completion

- Final status: awaiting exact-head CI
- PR: #75
- Merge commit: pending
- Archived at: pending
