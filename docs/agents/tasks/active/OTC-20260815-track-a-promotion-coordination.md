---
task_id: OTC-20260815-track-a-promotion-coordination
status: active
agent: ChatGPT
session_id: chatgpt-coordinator-20260815-1330
session_role: coordinator
session_rotation_count: 2
project_lane: otclient
lane: track-a-coordination
track_id: official-client-re
task_kind: integration
phase: promotion-review-integration
branch: docs/OTC-20260815-track-a-promotion-coordination
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/docs/OTC-20260815-track-a-promotion-coordination
worktree_mode: isolated_branch_checkout_equivalent
created: 2026-08-15T12:23:00+02:00
updated: 2026-08-15T13:30:00+02:00
risk: medium
related_pr: 300
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-promotion-coordination.md
  - docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/**
  - docs/agents/reports/OTCLIENT-20260815-track-a-promotion-coordination.md
  - docs/agents/tasks/archive/OTC-20260814-official-client-capability-experiment-sweep.md
  - tools/tibia_worldmap_reconstruction/**
  - tests/tools/tibia_worldmap_reconstruction/**
  - docs/agents/reports/OTC-20260812-worldmap-reconstruction.md
  - tools/tibia_runtime_bridge/**
  - tests/tools/tibia_runtime_bridge/**
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
modules_touched:
  - agent-coordination
  - tibia-worldmap-reconstruction
  - tibia-runtime-bridge
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: high
context_growth: controlled
decomposition_decision: phased
invocation_started_at: 2026-08-15T12:48:00+02:00
last_progress_at: 2026-08-15T13:30:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: other
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 2
stall_warnings: 0
---

# Objective

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete. Researchers remain Draft-only; this task alone performs campaign-level promotion/integration subject to repository gates. Track B remains outside mutation authority.

# Live-state contract

```yaml
TASK_ID: OTC-20260815-track-a-promotion-coordination
TASK_RECORD: docs/agents/tasks/active/OTC-20260815-track-a-promotion-coordination.md
PROJECT_LANE: otclient
BASE_MAIN: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
BRANCH: docs/OTC-20260815-track-a-promotion-coordination
WORKTREE: github-only://blakinio/otclient/refs/heads/docs/OTC-20260815-track-a-promotion-coordination
```

The previous coordinator session checkpointed `READY`; this session is a rotation on the same task/branch after refetching the exact live branch head `fd52b138658056727978dbfeed6857f0e4cb7dc7`. No researcher branch/worktree is shared.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Promotion ledger

## ACCEPT

- PR #283: bounded read-only runtime bridge implementation only. Source closed unmerged at `d93ccb34f66af7d3198a50a46e706b4f902ae637`; exact accepted blobs rebuilt on #300. `session-status` remains DERIVED pending live structural correlation.
- Exact-build reversible structural world transition from run `31806312967` / job `94785974126`; standalone player XYZ and A3/A4 remain unproven.

## ACCEPT_WITH_EDITS

- PR #279: fail-closed worldmap reconstruction tooling; exact accepted blobs rebuilt on current-main integration branch. Real capture/mappings/complete OTBM remain UNKNOWN.
- PR #290: bounded historical login/recovery procedure retained as `REVALIDATION_REQUIRED`.

## RETURN_FOR_EVIDENCE

- #295: material review findings plus Track B ownership collision.
- #301 P2-NETWORK: contract-only head `29ca506501efc716330a80ab2b96eaf9bbe3d4d5`; no experiment delivered.
- #302 P0-STATE: typed read-only probe exists, but self-hosted run `31880617510` remains queued; no semantic direct-position result.
- #303 RUNTIME: runtime semantic run remains blocked behind #302. During this rotation the RUNTIME workflow was additionally hardened fail-closed for observer cleanup on code head `4bd5cbc47fbfd816a6ab5dd66b57c88b3ff981f4`; this is safety repair only, not semantic evidence.

## REVIEW_REQUIRED_THIS_SESSION

- #304 COVERAGE-AUDIT: new reviewable worker handoff at exact Draft head `43a60bd96cc644b656b200c9edbfb75578b330b6` with deterministic validator and exact-head CI `31882010038` reported SUCCESS. Must be independently reviewed against canonical evidence before disposition.

## REJECT/SUPERSEDE

- #289 broad stale continuation and superseded P2 model;
- #296 stale lifecycle Draft after accepted correction integration;
- #277 stale Oteryn-dependent handover with unique negative history preserved;
- #280 superseded only as an active Track A dependency; broader infrastructure remains separately owned/open.

# Canonical non-completion boundary

```yaml
P2: OPEN_writer_ownership_transform_order_final_egress_harness
P1: PARTIAL_read_only_bridge_integrated_live_authority_unknown
P0: PARTIAL_structural_world_transition_fact_direct_player_state_unknown
RUNTIME: PARTIAL_one_generation_world_evidence_restart_relogin_unknown
ACTION: A3_A4_NOT_PROVEN
PROTOCOL_COVERAGE: 349/349 scoped identifier inventory; semantic classification UNKNOWN/349
QMETA_COVERAGE: 47/47 scoped handler inventory; semantic direct-Qt classification UNKNOWN/2184
P0_COVERAGE: UNKNOWN/UNKNOWN
COMPLETE: false
```

# Integration validation carried forward

Coordinator integration checkpoint `941921ae6c481d2ad6d94c0b182fba8c1bd40f68` was previously audited for changed paths and exact source-blob identity. Worldmap and runtime-bridge integrated product/test blobs match the accepted source blobs. Exact-head CI run `31882005845` was in progress when the previous session exhausted its two ordinary checks; this rotation will not treat that as semantic proof and will use fresh final-head validation only after any new accepted integration change.

# Acceptance inventory

- [x] current main and governance refetched;
- [x] coordinator task/branch ownership rotated safely after prior `READY` checkpoint;
- [x] #279/#283/#290 accepted bounded slices integrated/preserved;
- [x] #301/#302 current dispositions evidence-backed;
- [ ] #304 new evidence head reviewed and assigned one exact disposition;
- [ ] accepted coverage evidence, if any, integrated only as a bounded canonical slice;
- [ ] P2/P0/RUNTIME live gates satisfied or left explicitly incomplete with durable blockers;
- [ ] quantitative coverage state reconciled item-by-item without overstating inventory percentages;
- [ ] final audit/E2E/exact-head CI/PR hygiene/task archive/ownership release complete.

# Execution budget

```yaml
session_rotation_count: 2
last_progress_at: 2026-08-15T13:30:00+02:00
ordinary_ci_checks_for_current_head: 0
terminal_ci_checks: 0
repair_cycles: 0
context_reconstruction_attempts: 2
stall_warnings: 0
```

# Next action

Review exact #304 head `43a60bd96cc644b656b200c9edbfb75578b330b6`: verify owned paths, validator/provenance, exact-head CI and whether every percentage/UNKNOWN boundary is supportable. Assign one coordinator disposition, then integrate only the accepted bounded coverage slice if warranted.
