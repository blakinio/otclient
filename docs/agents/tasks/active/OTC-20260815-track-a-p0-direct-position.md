---
task_id: OTC-20260815-track-a-p0-direct-position
status: implementing
agent: ChatGPT
session_id: chatgpt-p0-player-state-continuation-20260817
session_role: researcher
session_rotation_count: 7
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: runtime-research
phase: runtime_snapshot_producer_tooling
branch: research/OTC-20260815-track-a-p0-direct-position
base_branch: main
current_main: 26c89a7d3b044acf88299f8d68eee4ac16b5d13c
risk: medium
updated: 2026-08-17T15:29:00+02:00
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
independent_runtime_provider_candidate:
  pr: 475
  task: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
  ownership: OTHER_ACTIVE_RUNTIME_TASK
  runtime_access: ephemeral_isolated
  target_uniqueness_checkpoint: PROVEN
  current_head: 062cf9396480a6012278cd5e0068aee403bdcc47
  current_run: 32035179935
  current_job: 95404298697
  current_mode: no_client_persistent_home_metadata_only
  current_client_executed: false
  current_in_game: false
  p0_direct_observation_legal_now: false
  note: P0 must not touch the task-owned runtime directly; only the RUNTIME owner may produce a bounded handoff if its independently authorized lifecycle later reaches IN_GAME and its own admission permits the extra read-only evidence capture.
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
producer_tooling_goal:
  purpose: prepare a deterministic read-only direct snapshot helper that a legally admitted RUNTIME owner can execute inside an independently authorized existing lifecycle without an extra login or movement stimulus
  required_snapshot_labels: [before, stepped, restored]
  direct_fields: [0x78, 0x7c, 0x80]
  exact_typed_vptr: 0x308ca70
  must_record: [pid, process_start_ticks, boot_id_sha256, main_base, typed_object, private_data_pointer, signed_i32_xyz, wall_time_ns, monotonic_ns]
  must_not_claim: semantic authority without causal correlation and negative controls
last_completed_step: fresh generation-8 canonical admission evidence was promoted and archived through #482/#486; current main is 26c89a7d3b044acf88299f8d68eee4ac16b5d13c; active independent RUNTIME #475 was inspected without touching its runtime and its current head is explicitly no-client, so no legal P0 live read exists yet
next_action: implement and hosted-validate the read-only direct snapshot helper, then publish a bounded producer handoff request to the active RUNTIME owner; execute no live P0 observation unless that owner independently reaches a legal IN_GAME lifecycle and accepts the handoff under its own current admission
---

# Objective

Recover and causally validate a direct standalone authoritative player-position read for the exact official native Linux client, distinct from camera, viewport, map-origin and stale/copy coordinates.

# Current classification

```text
DIRECT_PLAYER_XYZ=INCONCLUSIVE
```

Static exact-client evidence supports `TPlayerData +0x78/+0x7c/+0x80` as the strongest direct XYZ-shaped candidate, represented as three signed 32-bit fields. This is not semantic proof of authoritative current player position.

The former XID→PID dependency is complete through #457/#461/#465 and must not be repeated. Fresh canonical admission #482 proved lease generation 8 released and authoritative registration absent; #486 archived and released that RUNTIME task.

P0 remains a GitHub-hosted evidence consumer. It does not bootstrap/login, create a second logged-in session, mutate client bytes, write process memory, or take over another task's runtime. A current legal IN_GAME lifecycle must be supplied by RUNTIME. Until then the only legal continuation is deterministic producer tooling and coordination, not another generic static-analysis substitute.
