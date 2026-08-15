---
task_id: OTC-20260815-track-a-promotion-coordination
status: ready
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
updated: 2026-08-15T13:41:30+02:00
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
last_progress_at: 2026-08-15T13:41:30+02:00
ci_checks_for_current_head: 2
ci_check_generation: terminal
tterminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 1
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 2
stall_warnings: 0
stop_reason: coverage promotion is integrated and validated; no independent worker-spawn capability exists, so the prompt permits serial execution of the highest-information READY researcher lane only after coordinator ownership is released
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

Coordinator session rotation 2 is now released (`status: ready`) before claiming any researcher branch.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Promotion ledger

## ACCEPT

- #283: bounded read-only runtime bridge implementation; exact accepted tool/test blobs rebuilt on #300. `session-status` remains DERIVED until live structural correlation.
- exact-build reversible structural world transition from run `31806312967` / job `94785974126`; standalone player XYZ and A3/A4 remain unproven.

## ACCEPT_WITH_EDITS

- #279: fail-closed worldmap reconstruction tooling; exact accepted blobs rebuilt on #300. Real capture/mappings/complete OTBM remain UNKNOWN.
- #290: bounded historical login/recovery procedure retained as `REVALIDATION_REQUIRED`.
- #304: bounded exact-build quantitative coverage baseline reviewed at source head `43a60bd96cc644b656b200c9edbfb75578b330b6`; source CI `31882010038` SUCCESS; exact accepted evidence copied under coordinator ownership in `7b2f824e1038ea3d90200186fdb257ba25c95bc1`; coordinator integration head `0f5f835426ae9cd633c41e0cd0898d0a7dab87a4` passed CI `31882563937`; source Draft #304 closed unmerged after promotion.

## RETURN_FOR_EVIDENCE

- #295: material review findings plus Track B ownership collision.
- #301 P2-NETWORK: contract-only head `29ca506501efc716330a80ab2b96eaf9bbe3d4d5`; no experiment delivered; highest-information READY lane.
- #302 P0-STATE: typed read-only probe exists, but self-hosted run `31880617510` / job `95002559098` remains queued; no semantic direct-position result.
- #303 RUNTIME: semantic run remains blocked behind #302. Cleanup hardening at `4bd5cbc47fbfd816a6ab5dd66b57c88b3ff981f4`; durable waiting checkpoint `2b6350abeb4de37180247c585b90bd1e4c0a9d0f`; safety only, not semantic evidence.

## REJECT/SUPERSEDE

- #289 broad stale continuation and superseded P2 model;
- #296 stale lifecycle Draft after accepted correction integration;
- #277 stale Oteryn-dependent handover with unique negative history preserved;
- #280 superseded only as an active Track A dependency; broader infrastructure remains separately owned/open.

# Quantitative baseline now accepted

```yaml
protocol_identifier_inventory: 349/349
protocol_direct_qmeta_links: 27/349
generated_message_semantic_support: UNKNOWN/349
protocol_handler_qmeta_records: 47/47
direct_qt_connection_raw_census: 2184/2184
direct_qt_connection_semantic_classification: UNKNOWN/2184
legacy_qobject_connect_edges: 40/41
high_information_gameaction_sender_metaobjects: 29/31
p0_top_level_requirement_registry: 16/16
p0_live_read_coverage: UNKNOWN/UNKNOWN
bridge_v1_profile_target_inventory: 7/7
p1_overall_field_evidence_coverage: UNKNOWN/UNKNOWN
p2_chain_closure: UNKNOWN/5
restart_relogin_stability: UNKNOWN/1
```

# Canonical non-completion boundary

```yaml
P2: OPEN_writer_ownership_transform_order_final_egress_harness
P1: PARTIAL_read_only_bridge_integrated_live_authority_unknown
P0: PARTIAL_structural_world_transition_fact_direct_player_state_unknown
RUNTIME: PARTIAL_one_generation_world_evidence_restart_relogin_unknown
ACTION: A3_A4_NOT_PROVEN
COMPLETE: false
```

# Validation checkpoint

- source #304 exact-head CI: `31882010038` = SUCCESS;
- exact source blobs promoted by SHA under coordinator evidence;
- coordinator integration head `0f5f835426ae9cd633c41e0cd0898d0a7dab87a4` = CI `31882563937` SUCCESS;
- source #304 closed Draft/unmerged after promotion;
- no programme-completion claim is made.

# Next action

Claim #301 as an isolated Draft-only P2 researcher session. Revalidate its exact head/task/owned paths, use current canonical #299 facts plus bounded historical exact-build evidence, and execute the `TGameserverDualConnection -> TProtocolWriter/TIODeviceWriter` ownership/provenance discriminator. Do not write #300 while #301 is active. After #301 reaches a reviewable Draft handoff, release it and rotate back to #300 for independent promotion review.
