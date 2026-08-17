---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: validating
agent: ChatGPT
session_id: chatgpt-xres-client-base-followup-20260817
session_role: canonical_runtime_integration
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: xres-client-base-helper-followup
branch: fix/OTC-20260816-track-a-canonical-runtime-xres-client-base
base_branch: main
base_main: c55e3523e6e9d50df511e65dce9145a8f951a5f5
risk: high
updated: 2026-08-17T11:44:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
  - .github/scripts/tibia-official-client-re-xres-wire.py
  - .github/scripts/test_tibia_official_client_re_xres_wire.py
  - .github/workflows/tibia-official-client-re-xres-wire.yml
modules_touched:
  - track-a-xres-wire-helper
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: physical XRes identity is now promoted and archived; the retained v2 raw reply disproved the helper's exact-resource-echo assumption, so the next bounded step is a hosted-only semantic correction using the retained reply as a deterministic regression fixture before any later RUNTIME consumer reuses the helper.
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
  current_helper_blob: ac3c292087918d01e10006d153f84170210d81d5
  issue: extract_local_client_pid incorrectly requires CLIENTIDVALUE.spec.client to echo the exact queried resource XID; the X server selects the owner from the requested resource and may return the owning client resource-base instead.
  correction: retain one-spec exactly-one-record fail-closed behavior, require nonzero returned client identifier, exact LocalClientPid mask, exactly one positive CARD32 PID, and do not require exact resource-XID echo.
  additional_physical_run_required: false
  additional_physical_run_authorized: false
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
  - deterministic helper tests pass
  - helper remains transport-free and performs no I/O
  - exact-head Track A runtime governance passes
  - exact-head repository CI passes
  - no Synology, X11, official-client or canonical-state access occurs in this hosted fix
  - after promotion, any P0 physical work starts with its own fresh RUNTIME admission and may proceed only if a legal current IN_GAME lifecycle exists; do not bootstrap a session solely for P0
last_completed_step: PR #457 promoted direct physical resource-to-exact-client PID identity and PR #459 archived that discriminator with ownership released; the only immediate canonical follow-up is the retained-reply helper semantic correction
next_action: implement and validate the hosted-only XRes client-base helper correction, promote it, then perform fresh P0 RUNTIME admission and stop fail-closed if no legal current IN_GAME lifecycle is available
---

# Track A canonical runtime E2E — XRes client-base helper follow-up

Physical X11 resource ownership is proven and durable. This branch does not repeat that physical experiment. It corrects the persistent pure wire helper using the retained real v2 reply, then returns control to a separately admitted downstream RUNTIME phase.
