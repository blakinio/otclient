---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: ready
agent: ChatGPT
session_id: chatgpt-raw-xres-helper-hosted-20260817
session_role: hosted_protocol_helper_researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: coordinator-promotion-ready-raw-xres-wire
branch: diag/OTC-20260817-track-a-raw-xres-helper-hosted
base_branch: main
base_main: 55803133a5abe8b1e75e4660da1d2b84b154ab9a
risk: high
updated: 2026-08-17T08:48:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
  - .github/scripts/tibia-official-client-re-xres-wire.py
  - .github/scripts/test_tibia_official_client_re_xres_wire.py
  - .github/workflows/tibia-official-client-re-xres-wire.yml
modules_touched:
  - track-a-xres-wire-helper
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-bootstrap-implementation.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-xres-window-identity.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-xres-support-inventory.md
  - docs/agents/evidence/OTC-20260816-track-a-xres-support-inventory/20260816-fixed-path-result.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: the pure hosted/static raw-XRes wire codec is implemented and validated after one coordinator code-review hardening cycle. It performs no socket/network/process/runtime I/O, encodes/parses QueryVersion and one-spec QueryClientIds(LocalClientPid), rejects malformed/ambiguous replies fail-closed, and has deterministic little/big-endian fixtures. Physical identity retry remains forbidden until coordinator promotes this code to trusted main and a fresh separately admitted RUNTIME discriminator is created.
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
validation_level: heavy
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
runner: github-hosted
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
mutation_authorized: false
persistent_session_role: none
physical_e2e_required: true
owner_funded_ai_api_authorized: false
promotion_chain:
  post_rhi_xres_promotion_pr: 444
  post_rhi_xres_promotion_merge: 7540a679420689c388d9d11125c9fd8846956a10
  xres_child_archive_pr: 445
  xres_child_archive_merge: 55803133a5abe8b1e75e4660da1d2b84b154ab9a
promoted_window_identity_frontier:
  glx_present: true
  raw_viewable_full_display_xid_present: true
  raw_viewable_xid: 0x00c00011
  raw_viewable_geometry: 1920x1080
  xdotool_named_visible_count: 0
  exact_client_pid_ownership_of_viewable_xid: UNKNOWN
  convenience_libxcb_res_present: false
  convenience_libXRes_present: false
  contained_XResproto_present: true
  observed_query_client_ids_minor_opcode: 4
  observed_local_client_pid_mask: 0x02
  observed_query_client_ids_request_fixed_size: 8
  observed_query_client_ids_reply_fixed_size: 32
wire_contract:
  xres_protocol_major: 1
  xres_protocol_minor: 2
  query_version_minor_opcode: 0
  query_client_ids_minor_opcode: 4
  local_client_pid_mask: 0x02
  extension_major_opcode_source: caller_provided_from_core_QueryExtension
  supported_byte_orders:
    - little
    - big
  helper_network_access: false
  helper_socket_access: false
  helper_query_extension_access: false
implementation:
  helper_path: .github/scripts/tibia-official-client-re-xres-wire.py
  helper_blob: ce5992bc1171eef9f24a71dfc97da728f18627a9
  test_path: .github/scripts/test_tibia_official_client_re_xres_wire.py
  dedicated_workflow: .github/workflows/tibia-official-client-re-xres-wire.yml
  query_version_encoder: PASS
  query_version_reply_parser: PASS
  minimum_version_fence: PASS
  query_client_ids_one_spec_encoder: PASS
  bounded_reply_parser: PASS
  local_client_pid_extractor: PASS
  exactly_one_record_for_one_spec_required: true
  zero_id_reply_returns_unresolved_none: true
  transport_free: true
coordinator_review:
  material_findings_open: 0
  hardening_finding: one-spec extraction originally ignored unrelated extra records
  hardening_resolution: require exactly one record total for any nonempty one-spec result
  hardening_test: test_rejects_extra_non_target_record_even_with_target
validation:
  semantic_head_before_terminal_checkpoint: 06c6f18fc4a8920428ca353173b0596758a0190a
  dedicated_workflow_run: 32001448940
  dedicated_workflow_job: 95302425720
  dedicated_result: SUCCESS
  deterministic_tests: 33
  deterministic_tests_passed: 33
  purity_contract: XRES_WIRE_PURE_TRANSPORT_FREE_PASS
  track_a_governance_run: 32001448948
  track_a_governance_result: SUCCESS
  physical_runtime_access: NONE
evidence:
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/20260817-raw-xres-wire-hosted.md
classification:
  primary: PROVEN_HOSTED_RAW_XRES_WIRE_CODEC_FAIL_CLOSED_AND_TRANSPORT_FREE_WITH_33_DETERMINISTIC_FIXTURES
safety:
  canonical_bootstrap_retry_authorized: false
  canonical_window_identity_relaxation_authorized: false
  physical_identity_retry_authorized_before_promotion: false
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  track_b_access: false
forbidden:
  - any physical Synology/Xvfb/official-client execution from this source Draft
  - any network/socket/X11 connection in helper/tests
  - canonical lease/registration/session observation or mutation
  - credentials, login or gameplay
  - accepting a viewable XID as official-client-owned without direct resource/PID identity proof
  - canonical bootstrap retry
  - canonical window identity relaxation
  - Track B and historical PR #303 runtime surfaces
acceptance:
  - QueryVersion exact little/big fixtures: PASS
  - QueryVersion valid/malformed/version/sequence cases: PASS
  - QueryClientIds exact little/big fixtures: PASS
  - valid single PID and zero-ID unresolved cases: PASS
  - malformed/truncated/declared-length/count/value/oversize cases: PASS
  - exact resource/mask/PID/duplicate/extra-record ambiguity cases: PASS
  - dedicated GitHub-hosted validation: PASS
  - AST transport-free contract: PASS
  - Track A governance: PASS
  - evidence persisted: PASS
  - physical runtime access: NONE
last_completed_step: pure raw-XRes helper passed 33/33 deterministic fixtures and AST transport-free validation on run 32001448940/job 95302425720 after coordinator hardening required exact one-record semantics for the one-spec LocalClientPid query; evidence is persisted and no physical action occurred
next_action: coordinator independently review and promote the persistent helper/test/workflow plus this bounded evidence to current trusted main. Only after promotion may a fresh separately admitted task-owned physical identity discriminator be created; do not launch the official client or alter canonical window identity before that promotion.
---

# Track A canonical runtime E2E — raw-XRes helper terminal source

The reusable wire codec is ready for coordinator promotion. It proves only encoding/parsing behavior, not physical XID ownership.
