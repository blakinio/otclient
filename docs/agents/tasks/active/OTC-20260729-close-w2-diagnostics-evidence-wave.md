---
task_id: OTC-20260729-close-w2-diagnostics-evidence-wave
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
parallel_wave: OTERYN-W2-DIAGNOSTICS-EVIDENCE
parallel_lane: W2-C
parallel_lane_state: active
coordinator_task: OTC-20260729-close-w2-diagnostics-evidence-wave
branch: docs/OTC-20260729-close-w2-diagnostics-evidence-wave
base_branch: main
created: 2026-07-29T00:18:00+02:00
updated: 2026-07-29T00:18:00+02:00
last_verified_commit: "140d83670face0fef1219c43d7d186783d0c57da"
required_base_commit: "140d83670face0fef1219c43d7d186783d0c57da"
risk: low
related_pr: pending
depends_on:
  - merged/archived W2-DIAG
  - merged/archived W2-CP
  - merged/archived W2-AR
  - merged/archived W2-PR
blocks:
  - unambiguous closure of W2 and prevention of duplicate lane relaunch
owned_paths:
  - oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
  - oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md
  - docs/agents/README.md
  - docs/agents/tasks/active/OTC-20260729-close-w2-diagnostics-evidence-wave.md
shared_path_lease: []
contract_role: none
contracts_produced: []
contracts_consumed:
  - merged diagnostics contract from PR #61
  - merged Canary evidence from PR #63
  - merged asset evidence from PR #65
  - merged Windows platform evidence from PR #67
crates_touched: []
features_touched: []
contracts_touched:
  - completed parallel-wave status and future launch routing only
modules_touched: []
reuses:
  - archived W2 task records and exact PR/CI evidence
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

Close `OTERYN-W2-DIAGNOSTICS-EVIDENCE` durably, prevent every completed lane from being relaunched, prove all task/shared-path leases are released and leave exactly one evidence-based next package without implementing it.

# Acceptance criteria

- [ ] W2-DIAG, W2-CP, W2-AR and W2-PR are recorded as merged and archived with exact PR/merge evidence.
- [ ] No W2 lane remains launchable and no shared-path lease remains active.
- [ ] Current coordinator/discovery routing no longer instructs agents to relaunch W2.
- [ ] Open unrelated legacy/operational PRs are distinguished from Rust wave ownership.
- [ ] Exactly one next bounded package is recommended from live merged evidence.
- [ ] The next package is not implemented or pre-claimed by this coordination task.
- [ ] No Rust source, Cargo, lockfile, CI, architecture, protocol, asset, legacy runtime or external repository changes.
- [ ] Exact-head required CI passes; closure PR merges and archives separately.

# Confirmed live state

- Current `main`: `140d83670face0fef1219c43d7d186783d0c57da`.
- W2-DIAG implementation/archive: PR #61 merge `6d0c5ce243e62ff1e5b548a626c3f5e228506717`; PR #62 archive `9b5c86dff694aa65f4b264683f9c5ce3bf000035`.
- W2-CP evidence/archive: PR #63 merge `68567dbb118a3b3f2e420b62f5360979f461a725`; PR #64 archive `a6c8d1cfcac9364612c2ac56a9dc12618581adc9`.
- W2-AR evidence/archive: PR #65 merge `39138bb6673be070878225b4f872121ae5d39a6c`; PR #66 archive `048414f9457f6adaf6c3f94f8a8e6b92d624389d`.
- W2-PR evidence/archive: PR #67 merge `e7d9b5d5feb53debd79c4bdc82da16ca672217c5`; PR #68 archive `140d83670face0fef1219c43d7d186783d0c57da`.
- All four active W2 task records were moved to `docs/agents/tasks/archive/` through separate lifecycle PRs.
- W2-DIAG released its Cargo/lockfile/shared-document lease; evidence lanes held no shared lease.
- Open PRs #23, #37 and #48 remain unrelated legacy/operational work and own no greenfield Rust workspace or W2 evidence path.
- No active Rust-client task or open PR owns deterministic Rust test support/fake-time helpers.

# Next-package decision

Recommend exactly one next bounded Gate 1 package: deterministic Rust test support/fake-time helpers consuming merged `oteryn-foundation::ManualClock` and `oteryn-diagnostics` contracts.

Required envelope:

- one small test-support package only;
- test-owned deterministic builders/fixtures and fake-time orchestration;
- reuse `ManualClock`; do not create a second clock abstraction;
- no async runtime, executor, scheduler, product service, global test registry or runtime integration;
- one unique Cargo/lockfile/shared-document lease after fresh live preflight;
- exact Windows workspace, architecture, supply-chain and repository CI.

Rationale:

- it follows the accepted Gate 1 sequence after diagnostics;
- it strengthens deterministic validation before the Windows shell and synthetic asset implementation packages;
- W2-PR and W2-AR now provide bounded later package evidence;
- W2-CP still requires exact producer coordination and synthetic fixture acquisition before protocol implementation.

# Plan

1. Open an early draft PR.
2. Replace the W2 launch plan with a completed/closed record and exact lane evidence.
3. Change coordinator/discovery routing so no completed W2 lane can be relaunched.
4. Review the full docs-only diff and exact live state.
5. Pass exact-head CI, squash-merge and archive this coordination task separately.

# Validation

| Revision | Check | Result |
|---|---|---|
| `140d83670face0fef1219c43d7d186783d0c57da` | live lane/archive/open-PR/lease preflight | PASS |

# Remaining work

1. Open the draft PR and update closure routing.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Archived at: pending
