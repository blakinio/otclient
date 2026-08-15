---
task_id: OTC-20260815-track-a-promotion-coordination
status: ready
agent: ChatGPT
session_id: chatgpt-coordinator-20260815-125938
session_role: coordinator
session_rotation_count: 1
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
updated: 2026-08-15T13:27:26+02:00
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
last_progress_at: 2026-08-15T13:27:26+02:00
ci_checks_for_current_head: 0
ci_check_generation: other
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Objective

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete while researchers remain Draft-only and the coordinator alone promotes accepted evidence. Track B is outside mutation authority.

# Live-state contract

```yaml
TASK_ID: OTC-20260815-track-a-promotion-coordination
TASK_RECORD: docs/agents/tasks/active/OTC-20260815-track-a-promotion-coordination.md
PROJECT_LANE: otclient
BASE_MAIN: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
BRANCH: docs/OTC-20260815-track-a-promotion-coordination
WORKTREE: github-only://blakinio/otclient/refs/heads/docs/OTC-20260815-track-a-promotion-coordination
```

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Durable campaign checkpoint

## Integrated accepted evidence

- PR #279 `ACCEPT_WITH_EDITS`: source closed unmerged at `04356aa9c042ce19d9d8431b91f18567e410a5e5`; exact accepted worldmap tool/test blobs rebuilt on #300; source exact-head CI `31681889560` SUCCESS; 23/23 focused tests, syntax and synthetic reconstruct/compare/plan evidence retained. Real capture/mappings/complete OTBM remain UNKNOWN.
- PR #283 `ACCEPT`: source closed unmerged at `d93ccb34f66af7d3198a50a46e706b4f902ae637`; exact accepted read-only bridge/test blobs rebuilt on #300; source exact-head CI `31680615776` SUCCESS; exact runtime validation `31654823776` / `94306874981` retained. `session-status` remains DERIVED until live structural correlation; authoritative position/restart/write API remain UNKNOWN.
- PR #290 `ACCEPT_WITH_EDITS`: bounded historical login/recovery procedure preserved as `REVALIDATION_REQUIRED`; source closed.
- bounded exact-build reversible structural world transition from run `31806312967` / job `94785974126` retained as FACT world-state evidence only; A3/A4 remain unproven.

## Rejected/superseded

- #289 stale broad continuation / superseded P2 model;
- #296 stale lifecycle draft after accepted correction integration;
- #277 stale Oteryn-dependent handover; unique negative history preserved;
- #280 superseded only as an active Track A dependency; broader infrastructure PR remains separately owned/open.

## Return for evidence

- #295: material review findings plus Track B ownership collision.
- #301 P2-NETWORK: current head `29ca506501efc716330a80ab2b96eaf9bbe3d4d5`; dispatch contract only; READY/unassigned, no experiment result.
- #302 P0-STATE: current head `e45b126923495b209c08a77e9a3db96b44ad71a4`; typed read-only probe exists but run `31880617510` job `95002559098` remains queued; no semantic result.
- #303 RUNTIME: current head `0270b1f3b6e75c995649b405758f058bae026c88`; no self-hosted reacquire semantic job executed; serialized behind #302.
- #304 COVERAGE-AUDIT: current head `7eec15079e54bc163785013025cdea47d30e57c7`; dispatch contract only; READY/unassigned, no registries/validator.

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

# Validation checkpoint

Coordinator integration checkpoint `941921ae6c481d2ad6d94c0b182fba8c1bd40f68` was audited for changed paths and exact source-blob identity:

- all 23 changed files are within declared Track A coordinator/integration scope;
- current worldmap tool/test blob SHAs exactly equal the accepted #279 source blobs;
- current runtime-bridge tool/test/profile blob SHAs exactly equal the accepted #283 source blobs;
- `main` was still `8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45` immediately before exact-head validation;
- exact-head CI run `31882005845` progressed from `pending` to `in_progress` across the two ordinary checks allowed for that SHA; no third poll is permitted by the anti-stall contract.

This task is not marked completed and #300 remains Draft because independent researcher evidence and programme gates are outstanding. The current checkpoint commit is documentation-only after the audited integration head; no product/tool/test blob changed after `941921ae...`.

# Execution budget state

```yaml
invocation_started_at: 2026-08-15T12:48:00+02:00
checkpoint_at: 2026-08-15T13:27:26+02:00
elapsed_minutes_approx: 39
ordinary_ci_checks_for_941921ae: 2
repair_cycles: 0
context_reconstruction_attempts: 1
stall_warnings: 0
stop_reason: current coordinator-safe work exhausted; runtime lanes are waiting and READY P2/coverage tasks require separate Draft-only researcher sessions, but the available toolset cannot spawn an independent worker and coordinator role must not impersonate them
```

# Next action

A separate Draft-only researcher session must claim `OTC-20260815-track-a-p2-writer-ownership` / PR #301 first (highest information gain) and execute its exact-client writer-ownership hypothesis without reviving the superseded models. In parallel, #302/#303 may resume only when the serialized self-hosted runtime lane assigns their jobs, and another independent static researcher may claim #304. The next coordinator session must refetch main/PR heads, review only newly produced evidence, and continue promotion from this checkpoint.
