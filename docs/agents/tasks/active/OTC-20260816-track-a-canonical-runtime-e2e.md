---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: implementing
agent: ChatGPT
session_id: chatgpt-raw-xres-helper-hosted-20260817
session_role: hosted_protocol_helper_researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: raw-xres-helper-hosted-validation
branch: diag/OTC-20260817-track-a-raw-xres-helper-hosted
base_branch: main
base_main: 55803133a5abe8b1e75e4660da1d2b84b154ab9a
risk: high
updated: 2026-08-17T08:40:00+02:00
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
execution_reason: trusted main now contains coordinator-promoted evidence proving a raw full-display viewable X11 resource exists but exact client PID ownership remains UNKNOWN; libxcb-res/libXRes convenience libraries are absent while contained XResproto protocol definitions expose the QueryClientIds/LocalClientPid wire basis. This phase implements only a pure hosted/static byte encoder/parser for XRes QueryVersion and QueryClientIds. It performs no socket connection, QueryExtension discovery, X server/client launch, Synology access, canonical state access, credentials/login/gameplay or Track B work. Physical identity retry remains forbidden until this helper is validated and separately admitted.
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
implementation_scope:
  - encode QueryVersion request for caller-provided extension major opcode
  - parse exact bounded QueryVersion reply and optionally fence sequence
  - require server XRes version at least 1.2
  - encode one-resource QueryClientIds request with LocalClientPid mask
  - parse bounded QueryClientIds replies into client/mask/value records
  - extract exactly one positive LocalClientPid only from exact requested resource/mask/value shape
  - reject truncation, declared-length mismatch, oversized payloads, excessive counts, malformed value lengths, duplicate target records, wrong mask, wrong resource and sequence mismatch
forbidden:
  - any network/socket/X11 connection in the helper or tests
  - any physical Synology/Xvfb/official-client execution during this phase
  - canonical lease/registration/session observation or mutation
  - credentials, login or gameplay
  - accepting a viewable XID as official-client-owned without direct resource/PID identity proof
  - canonical bootstrap retry
  - canonical window identity relaxation
  - Track B and historical PR #303 runtime surfaces
acceptance:
  - helper has no network/socket/process/runtime imports or side effects
  - QueryVersion little-endian and big-endian exact request fixtures pass
  - QueryVersion valid reply/sequence/version checks pass
  - QueryVersion malformed/truncated/non-reply/length-mismatch/wrong-version cases reject
  - QueryClientIds little-endian and big-endian exact request fixtures pass
  - QueryClientIds valid single-PID and zero-ID replies parse deterministically
  - QueryClientIds malformed/truncated/declared-length/count/value-length/oversize cases reject
  - exact resource/mask/duplicate/PID validity checks reject ambiguous identity
  - dedicated GitHub-hosted workflow passes
  - Track A governance and repository CI pass on exact head
  - no physical runtime access occurs
last_completed_step: coordinator promotion #444 and lifecycle #445 are merged on trusted main; XRes child tasks are archived and ownership-released; the canonical task is freshly rebound to a pure hosted raw-wire validation branch
next_action: implement the pure XRes wire helper, deterministic unit fixtures and hosted-only validation workflow; run exact-head governance/CI and hand the validated helper to coordinator for code promotion before any physical identity retry.
---

# Track A canonical runtime E2E — hosted raw-XRes helper validation

This phase is deliberately non-runtime. It produces a strict reusable wire codec only; socket/X server/client use remains a later separately admitted RUNTIME step.
