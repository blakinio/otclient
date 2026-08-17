---
task_id: OTC-20260817-track-a-xres-raw-pid-identity
status: validating
agent: ChatGPT
session_id: chatgpt-xres-raw-pid-identity-v2-20260817
session_role: runtime_discriminator
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: terminal-validation
branch: diag/OTC-20260817-track-a-xres-raw-pid-identity-physical-authorized-v2
base_branch: main
base_main: 60ab740872d52f3f7c4802d49fd5275a9968d085
pr: 457
risk: high
updated: 2026-08-17T11:35:00+02:00
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_class: github_hosted
runner: github-hosted
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
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
owner_authorization_basis: current owner invocation 2026-08-17 requesting completion of the full follow-on task after the mutation-design closeout
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
helper_fix_promoted:
  pr: 455
  merge: 60ab740872d52f3f7c4802d49fd5275a9968d085
  helper_blob: ac3c292087918d01e10006d153f84170210d81d5
  tests: 35/35 PASS
  transport_free: PASS
physical_v1:
  run: 32013868595
  exact_client_launches: 1
  xres_query_version: PROVEN_1_2
  xres_query_client_ids_pid_identity: NOT_PROVEN
  cleanup: COMPLETE
physical_v2:
  run: 32015479835
  hosted_preflight_job: 95343925201
  hosted_preflight_result: SUCCESS
  physical_job: 95344000918
  runtime_governance: PASS
  exact_client_launches: 1
  namespace: /home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260817-track-a-xres-raw-pid-identity/ephemeral-32015479835-1
  source_fence: PASS
  support_fence: PASS
  display: ':231'
  client_pid: 13648
  xres_server_version: '1.2'
  viewable_candidate_xid: '0x00c00011'
  viewable_candidate_geometry: '1920x1080'
  reply_client_base: '0x00c00000'
  reply_mask: LocalClientPid
  reply_value_length_bytes: 4
  reply_pid: 13648
  raw_reply_hex: 01000300040000000100000000000000000000000000000000000000000000000000c000020000000400000050350000
  wrapper_result: FALSE_NEGATIVE_OVERSTRICT_EXACT_RESOURCE_ECHO_REQUIREMENT
  physical_identity: PROVEN
  cleanup: COMPLETE
  canonical_state_access: NONE
  login: false
  gameplay: false
  process_memory_access: false
  client_bytes_mutated: false
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-xres-raw-pid-identity.md
  - docs/agents/evidence/OTC-20260817-track-a-xres-raw-pid-identity/**
modules_touched:
  - track-a-xres-runtime-discriminator
safety:
  canonical_state_access: forbidden
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  process_memory_access: false
  client_byte_mutation: false
  v1_exact_client_launches_consumed: 1
  v2_exact_client_launches_consumed: 1
  further_identity_launch_authorized: false
  track_b_access: false
  broad_process_cleanup: forbidden
classification:
  primary: XRES_PROVES_VIEWABLE_WINDOW_OWNED_BY_EXACT_CLIENT
  wrapper_red_job_semantics: EXPECTED_ASSERTION_FALSE_NEGATIVE_AFTER_VALID_RAW_EVIDENCE
  confidence: DIRECT_PHYSICAL_RAW_REPLY_PLUS_PRIMARY_XSERVER_SEMANTICS
helper_followup:
  finding: XRES-V2-AUD-001
  severity: LOW
  blocking_this_task: false
  additional_physical_run_required: false
  issue: persistent helper incorrectly requires returned CLIENTIDVALUE.spec.client to echo exact queried resource XID, while X server returns owning client resource-base
  owner: persistent raw-XRes helper owner / canonical runtime task
acceptance:
  - fresh physical v2 admission passed
  - exactly one v2 isolated exact-client launch occurred
  - final t35 contained exactly one VIEWABLE 1920x1080 candidate
  - XRes QueryVersion proved 1.2
  - raw QueryClientIds reply was retained before helper interpretation
  - LocalClientPid decoded from the reply equals the exact launched client PID 13648
  - returned client-base behavior is consistent with primary X server ConstructClientIds/ConstructClientIdValue semantics
  - physical resource-to-exact-client PID identity is therefore proven
  - cleanup completed
  - no canonical state, credentials, login, gameplay, process memory or client-byte mutation occurred
  - one-shot v2 workflow/patcher removed before merge
  - final audit has zero material findings for this task
  - exact-head Track A governance and repository CI pass before merge
  - task is archived and ownership released after merge
evidence:
  - docs/agents/evidence/OTC-20260817-track-a-xres-raw-pid-identity/20260817-v1-physical-parser-discriminator.md
  - docs/agents/evidence/OTC-20260817-track-a-xres-raw-pid-identity/20260817-helper-fix-audit.md
  - docs/agents/evidence/OTC-20260817-track-a-xres-raw-pid-identity/20260817-v2-physical-pid-identity.md
  - docs/agents/evidence/OTC-20260817-track-a-xres-raw-pid-identity/20260817-v2-final-audit.md
last_completed_step: physical v2 raw XRes evidence directly bound the unique VIEWABLE 1920x1080 resource 0x00c00011 to exact launched client PID 13648; cleanup completed and no further identity launch is required
next_action: remove consumed one-shot v2 runtime surfaces, validate terminal #457 exact head, merge, then archive this task and release ownership; downstream RUNTIME work may consume the proven identity only under its own fresh admission.
---

# Raw XRes PID identity discriminator — terminal validation

The physical identity question is resolved. The red physical job is an assertion false negative caused by the helper expecting the reply to echo the queried resource ID. The retained raw reply and X server semantics independently prove the unique VIEWABLE 1920x1080 resource is owned by the exact fenced client process. No further physical retry is authorized for this task.
