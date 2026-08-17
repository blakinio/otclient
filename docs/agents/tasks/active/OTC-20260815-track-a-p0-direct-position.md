---
task_id: OTC-20260815-track-a-p0-direct-position
status: waiting
agent: ChatGPT
session_id: chatgpt-p0-player-state-continuation-20260817
session_role: researcher
session_rotation_count: 7
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: runtime-research
phase: runtime_handoff_ready
branch: research/OTC-20260815-track-a-p0-direct-position
base_branch: main
current_main: 26c89a7d3b044acf88299f8d68eee4ac16b5d13c
risk: medium
updated: 2026-08-17T15:37:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p0-direct-position.md
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/**
  - .github/workflows/tibia-official-client-re-p0-direct-position.yml
  - .github/scripts/tibia-official-client-re-p0-direct-position.py
  - .github/scripts/tibia-official-client-re-p0-runtime-snapshot.py
  - .github/scripts/test_tibia_official_client_re_p0_runtime_snapshot.py
  - .github/workflows/tibia-official-client-re-p0-runtime-snapshot-hosted.yml
reuses:
  - merged producer PR #435 / merge 8c9486e2c6109a7a39b564804c8acd707659b5e0
  - physical XRes identity PR #457 / merge 16c6fb695a85a6ba3a809fcf5b031ce4ac7e11fc
  - XRes client-base correction PR #461 / merge 1eb4a8edecba3966aa1e6155e241b404eb4d30cb
  - canonical XRes integration PR #465 / merge f8e628a255a18ec92839bbb45ef0e3b40bef8605
  - fresh P0 current-admission PR #482 / merge a94e931cdc454e0e28c2ef628be23b926c4e3657
  - P0 admission archive/release PR #486 / merge 26c89a7d3b044acf88299f8d68eee4ac16b5d13c
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
execution_class: github_hosted
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
mutation_authorized: false
owner_funded_ai_api_authorized: false
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: low_noise
static_input_blocker: CLOSED_BY_MERGED_PR_435
xid_pid_research: COMPLETE_DO_NOT_REPEAT
semantic_player_xyz_proven: false
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
strongest_candidate:
  type_route: TPlayerData
  primary_vptr_offset: 0x308ca70
  object_live_identity: UNKNOWN
  x_offset: 0x78
  y_offset: 0x7c
  z_offset: 0x80
  representation: signed_i32_x3
  static_property_site: 0x8367c1
  classification: XYZ_SHAPED_CANDIDATE_NOT_SEMANTICALLY_PROVEN
fresh_canonical_admission:
  producer_pr: 482
  physical_run: 32033237388
  physical_job: 95397745114
  runner: synology-otclient-01
  lease_status: released
  lease_generation: 8
  authoritative_registration: ABSENT
  legal_registered_in_game_lifecycle: false
  result: BLOCKED_NO_LEGAL_EXISTING_IN_GAME_LIFECYCLE
runtime_snapshot_helper:
  path: .github/scripts/tibia-official-client-re-p0-runtime-snapshot.py
  blob_sha: afd8cd7023ad667421eddce71dbc1575770e0f32
  fields: [0x78, 0x7c, 0x80]
  representation: signed_i32_x3
  memory_access: read_only
  memory_writes: 0
  records: [pid, process_start_ticks, boot_id_sha256, main_base, typed_object, private_data_pointer, xyz, wall_time_ns, monotonic_ns]
  semantic_claim_emitted: false
  validation_head: 74ee39fc0136142f2dd0b425a34e6e75fa38430e
  validation_run: 32035752607
  validation_job: 95405675923
  validation_result: SUCCESS
  handoff_doc_head: 01c4c169a119a2d4ad50762ee72c10941f5cc1de
  handoff_doc_validation_run: 32035842654
  handoff_doc_validation_result: SUCCESS
runtime_producer_handoff:
  evidence_contract: docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260817-runtime-producer-handoff-v2.md
  active_provider_pr: 475
  provider_task: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
  provider_ownership: OTHER_ACTIVE_RUNTIME_TASK
  provider_runtime_access: ephemeral_isolated
  producer_request_comment: 5316768394
  no_extra_login_requested: true
  no_extra_movement_requested: true
  requested_existing_stimulus: Right_then_Left_restore
  requested_snapshots: [before, stepped, restored]
  direct_runtime_takeover_by_p0: forbidden
provider_current_state:
  checked_head: 1b68f7508ea2e8618799af58f1a59863dcd56cdd
  checked_commit_purpose: one_no_secret_prelogin_focus_scan
  current_in_game: false
  current_p0_live_read_available: false
  note: provider remains pre-login/no-secret at this checkpoint; P0 must not infer future IN_GAME or consume the provider runtime until the RUNTIME owner reaches it under its own admission and accepts the handoff
acceptance:
  exact_fence: PASS
  typed_candidate_discovery: PASS
  direct_offsets_static_support: PASS
  current_exact_pid_start_identity: MISSING
  current_xres_ownership: MISSING_FOR_CURRENT_LIFECYCLE
  structurally_verified_in_game: MISSING
  direct_xyz_observations: 0
  independent_structural_world_coordinate_observations: 0
  known_delta_correlation: NOT_RUN
  inverse_control: NOT_RUN
  camera_viewport_map_origin_stale_copy_negatives: NOT_RUN
  repeatability: NOT_VERIFIED
  restart_relogin_stability: NOT_VERIFIED
  direct_player_xyz: INCONCLUSIVE
hard_stop_policy:
  p0_only_bootstrap_authorized: false
  p0_only_login_authorized: false
  second_logged_in_session_authorized: false
  process_memory_write_authorized: false
  worldmap_research_authorized_for_p0: false
last_completed_step: implemented and hosted-validated a bounded O_RDONLY runtime snapshot helper for exact TPlayerData +0x78/+0x7c/+0x80; persisted the same-session RUNTIME producer contract and sent it to active provider #475 without touching that task-owned runtime; #475 remains pre-login/no-secret, so no legal P0 live observation exists yet
next_action: no P0 worker should touch a live runtime now; resume only when a RUNTIME owner independently reaches a legal exact-client IN_GAME lifecycle and explicitly accepts the same-session handoff, then consume before/stepped/restored read-only snapshots plus current identity, independent coordinate/control and negative-control evidence
---

# Objective

Recover and causally validate a direct standalone authoritative player-position read for the exact official native Linux client, distinct from camera, viewport, map-origin and stale/copy coordinates.

# Current classification

```text
DIRECT_PLAYER_XYZ=INCONCLUSIVE
```

Static exact-client evidence supports `TPlayerData +0x78/+0x7c/+0x80` as the strongest direct XYZ-shaped candidate, represented as three signed 32-bit fields. This is not semantic proof of authoritative current player position.

The former XID→PID dependency is complete through #457/#461/#465 and must not be repeated. Fresh canonical admission #482 proved lease generation 8 released and authoritative registration absent; #486 archived and released that RUNTIME task.

P0 now has a deterministic, hosted-validated read-only snapshot helper and a precise same-session producer contract. The active RUNTIME provider candidate #475 is currently pre-login/no-secret and remains owned by another task. P0 therefore waits without taking over that runtime, creating another session, or treating world-map research as its target.
