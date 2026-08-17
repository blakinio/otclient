---
task_id: OTC-20260817-track-a-xres-raw-pid-identity
status: validating
agent: ChatGPT
session_id: chatgpt-xres-raw-pid-identity-20260817
session_role: runtime_discriminator
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: validate-helper-fix
branch: diag/OTC-20260817-track-a-xres-raw-pid-identity-physical-authorized-v1
base_branch: main
base_main: d9529da35ada6ab2a7bf4d2e70205cc0dd7b14ab
pr: 455
risk: high
updated: 2026-08-17T11:14:00+02:00
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
prerequisites:
  raw_xres_helper_pr: 448
  raw_xres_helper_merge: d9529da35ada6ab2a7bf4d2e70205cc0dd7b14ab
  raw_xres_helper_path: .github/scripts/tibia-official-client-re-xres-wire.py
  prior_physical_discriminator: 31973388722
  prior_result: XRES_IDENTITY_UNRESOLVED_HELPER_UNAVAILABLE
owned_paths:
  - .github/scripts/tibia-official-client-re-xres-wire.py
  - .github/scripts/test_tibia_official_client_re_xres_wire.py
  - docs/agents/tasks/active/OTC-20260817-track-a-xres-raw-pid-identity.md
  - docs/agents/evidence/OTC-20260817-track-a-xres-raw-pid-identity/**
modules_touched:
  - track-a-xres-wire-helper
  - track-a-xres-runtime-discriminator
safety:
  current_phase_runtime_access: none
  canonical_state_access: forbidden
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  process_memory_access: false
  client_byte_mutation: false
  v1_exact_client_launch_limit: 1
  v1_exact_client_launches_consumed: 1
  track_b_access: false
  broad_process_cleanup: forbidden
physical_v1:
  run: 32013868595
  hosted_preflight_job: 95339063640
  hosted_preflight_result: SUCCESS
  physical_job: 95339104951
  runtime_governance: PASS
  exact_client_launches: 1
  namespace: /home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260817-track-a-xres-raw-pid-identity/ephemeral-32013868595-1
  source_fence: PASS
  support_fence: PASS
  warp: PASS
  display: ':231'
  xres_query_version: PROVEN
  xres_server_version: '1.2'
  xres_extension_major_opcode: 148
  xres_query_client_ids_pid_identity: NOT_PROVEN
  failure: QueryClientIds CLIENTIDVALUE.length was interpreted by promoted helper as CARD32-count rather than byte-count
  cleanup: COMPLETE
  canonical_state_access: NONE
  login: false
  gameplay: false
helper_fix:
  root_cause: XRes CLIENTIDVALUE.length is a byte count; LocalClientPid uses length=4 followed by one CARD32 PID, while promoted parser multiplied length by four again
  parser_fix_commit: c466f1fcf350518f8b5d250439efc955dca7cf0d
  regression_test_commit: 1a8de024e9d4274e5ea811f8aa9bafe743814239
  one_shot_v1_workflow_retained: false
  one_shot_v1_patchers_retained: false
  physical_retry_on_v1_branch_authorized: false
acceptance:
  - corrected helper treats CLIENTIDVALUE.length as bytes and rejects non-CARD32-aligned lengths
  - LocalClientPid fixture encodes length=4 and one CARD32 PID for both byte orders
  - deterministic malformed/truncated/oversized/ambiguous fixtures continue to fail closed
  - helper remains pure and transport-free
  - full #455 diff contains no reusable physical one-shot workflow/patcher
  - fresh audit has zero material findings
  - exact-head Track A governance, raw XRes helper workflow and repository CI pass
  - #455 merges without claiming XID-to-PID identity proof
  - same task then continues from merged main on a fresh physical-authorized-v2 branch with a new one-launch admission
classification:
  desired: XRES_PROVES_VIEWABLE_WINDOW_OWNED_BY_EXACT_CLIENT
  current: V1_PHYSICAL_DISCRIMINATOR_EXPOSED_PROMOTED_HELPER_PARSER_DEFECT
  failure_is_evidence: true
validation:
  first_generation:
    head: 87e1bda874c5fdc48833c367054b5be9fcf96ad1
    run: 32013415890
    hosted_job: 95337663549
    result: FAILED_BEFORE_PHYSICAL_EXECUTION
    first_error: XRES_RAW_PATCH_REFUSED=SNAPSHOT_RAW_XRES_INSERT_COUNT:0
    physical_job: 95337705295
    physical_job_result: SKIPPED
    exact_client_launches: 0
  ownership_generation:
    run: 32013718874
    hosted_job: 95338687963
    hosted_result: SUCCESS
    physical_job: 95338745980
    physical_result: FAILED_ADMISSION_BEFORE_EXECUTION
    exact_client_launches: 0
  valid_physical_v1:
    run: 32013868595
    hosted_job: 95339063640
    physical_job: 95339104951
    result: PARSER_DEFECT_AFTER_ONE_LAUNCH
    cleanup: COMPLETE
    exact_client_launches: 1
last_completed_step: one authorized v1 physical launch proved XRes 1.2 and exposed a deterministic CLIENTIDVALUE.length parser defect; cleanup completed, one-shot physical surfaces were removed, and the parser plus deterministic fixtures were corrected on #455
next_action: validate the helper fix and terminal #455 diff on hosted exact head, perform a fresh audit, merge #455 when all gates pass, then continue this same task on a fresh physical-authorized-v2 branch from merged main.
---

# Raw XRes PID identity discriminator

The v1 physical discriminator is intentionally exhausted after exactly one isolated exact-client launch. It did not prove XID-to-PID ownership because it exposed a protocol-parser defect in the promoted #448 helper. Current work is static/hosted repair only; another physical launch requires a fresh v2 branch/admission after this helper fix reaches trusted `main`.
