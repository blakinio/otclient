---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: ready
agent: ChatGPT
session_id: chatgpt-xres-client-base-followup-20260817
session_role: canonical_runtime_integration
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: xres-client-base-helper-fix-ready
branch: fix/OTC-20260816-track-a-canonical-runtime-xres-client-base
base_branch: main
base_main: c55e3523e6e9d50df511e65dce9145a8f951a5f5
risk: high
updated: 2026-08-17T11:48:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
  - .github/scripts/tibia-official-client-re-xres-wire.py
  - .github/scripts/test_tibia_official_client_re-xres-wire.py
  - .github/workflows/tibia-official-client-re-xres-wire.yml
modules_touched:
  - track-a-xres-wire-helper
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: physical XRes identity is promoted and archived, and the retained v2 reply has now been used to correct the persistent helper's exact-resource-echo assumption under hosted-only validation. No further identity launch is required or authorized.
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
client_byte_mutation_authorized: false
persistent_session_role: none
physical_e2e_required: true
owner_funded_ai_api_authorized: false
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
identity_chain:
  raw_xres_helper_promotion_pr: 448
  raw_xres_helper_promotion_merge: d9529da35ada6ab2a7bf4d2e70205cc0dd7b14ab
  client_id_length_fix_pr: 455
  client_id_length_fix_merge: 60ab740872d52f3f7c4802d49fd5275a9968d085
  physical_identity_pr: 457
  physical_identity_merge: 16c6fb695a85a6ba3a809fcf5b031ce4ac7e11fc
  physical_identity_run: 32015479835
  physical_identity_job: 95344000918
  physical_identity: PROVEN
  physical_identity_classification: XRES_PROVES_VIEWABLE_WINDOW_OWNED_BY_EXACT_CLIENT
  physical_identity_cleanup: COMPLETE
  identity_archive_pr: 459
  identity_archive_merge: c55e3523e6e9d50df511e65dce9145a8f951a5f5
  identity_ownership_released: true
retained_v2_fixture:
  queried_resource_xid: '0x00c00011'
  returned_client_base: '0x00c00000'
  returned_mask: LocalClientPid
  returned_pid: 13648
  exact_launched_pid: 13648
  raw_reply_hex: 01000300040000000100000000000000000000000000000000000000000000000000c000020000000400000050350000
helper_followup:
  finding: XRES-V2-AUD-001
  severity: LOW
  prior_helper_blob: ac3c292087918d01e10006d153f84170210d81d5
  corrected_helper_blob: 2552a275e3d8068e4f874d91438b3cfb696a441e
  corrected_test_blob: 03e696b8d2f0f5dfa8ce9b7844cf4402b131d5b9
  issue: extract_local_client_pid incorrectly required CLIENTIDVALUE.spec.client to echo the exact queried resource XID; the X server selects the owner from the requested resource and may return the owning client resource-base instead.
  correction: retain one-spec exactly-one-record fail-closed behavior, require nonzero returned client identifier, exact LocalClientPid mask, exactly one positive CARD32 PID, and do not require exact resource-XID echo.
  retained_physical_fixture_regression: PASS
  additional_physical_run_required: false
  additional_physical_run_authorized: false
validation:
  helper_fix_head_before_checkpoint: bd78a6fad5c6c3526037a44a9f70cc6d8d7c20f7
  dedicated_run: 32016911653
  dedicated_job: 95348227276
  dedicated_result: SUCCESS
  deterministic_tests: 37
  deterministic_tests_passed: 37
  purity_contract: XRES_WIRE_PURE_TRANSPORT_FREE_PASS
  governance_run: 32016911587
  governance_result: SUCCESS
  repository_ci_run: 32016911767
  repository_required_job: 95348545046
  repository_required_result: SUCCESS
  physical_runtime_used_for_helper_fix: false
classification:
  primary: PROVEN_HOSTED_RAW_XRES_CLIENT_BASE_SEMANTICS_WITH_RETAINED_PHYSICAL_FIXTURE
safety:
  canonical_state_access: forbidden_during_hosted_fix
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  process_memory_access: false
  client_byte_mutation: false
  physical_identity_retry_authorized: false
  track_b_access: false
acceptance:
  - persistent helper accepts the retained v2 resource-to-client-base reply and extracts PID 13648
  - zero returned client identifiers remain rejected
  - wrong mask, wrong value shape, zero PID and multi-record replies remain rejected
  - 37 deterministic helper tests pass
  - helper remains transport-free and performs no I/O
  - exact-head Track A runtime governance passes for the implementation head
  - exact-head repository CI passes for the implementation head
  - no Synology, X11, official-client or canonical-state access occurs in this hosted fix
  - after promotion, any P0 physical work starts with its own fresh RUNTIME admission and may proceed only if a legal current IN_GAME lifecycle exists; do not bootstrap a session solely for P0
last_completed_step: hosted-only XRes client-base helper correction passed 37/37 deterministic fixtures including the retained v2 physical reply, purity validation, Track A governance and repository CI with no physical runtime access
next_action: validate this single final checkpoint head, mark PR #461 ready, protected-merge the correction, then perform fresh P0 RUNTIME admission and stop fail-closed if no legal current IN_GAME lifecycle is available
---

# Track A canonical runtime E2E — XRes client-base helper follow-up

Physical X11 resource ownership is proven and durable. The persistent helper now accepts the server's owning-client resource-base semantics while preserving one-spec fail-closed cardinality and PID-shape checks. No physical identity retry is authorized.
