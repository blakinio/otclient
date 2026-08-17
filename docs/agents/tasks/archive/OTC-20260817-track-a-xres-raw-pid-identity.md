---
task_id: OTC-20260817-track-a-xres-raw-pid-identity
status: completed
agent: ChatGPT
session_id: chatgpt-xres-raw-pid-identity-archive-20260817
session_role: runtime_discriminator_closeout
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: archived
base_branch: main
risk: high
updated: 2026-08-17T11:42:00+02:00
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
mutation_authorized: false
client_byte_mutation_authorized: false
owner_funded_ai_api_authorized: false
ownership_released: true
owned_paths: []
implementation_pr: 457
implementation_merge_commit: 16c6fb695a85a6ba3a809fcf5b031ce4ac7e11fc
helper_repair_pr: 455
helper_repair_merge: 60ab740872d52f3f7c4802d49fd5275a9968d085
physical_v1:
  run: 32013868595
  exact_client_launches: 1
  cleanup: COMPLETE
  disposition: PARSER_LENGTH_DEFECT_FOUND_AND_REPAIRED
physical_v2:
  run: 32015479835
  hosted_preflight_job: 95343925201
  physical_job: 95344000918
  exact_client_launches: 1
  exact_client_pid: 13648
  xres_server_version: '1.2'
  viewable_candidate_xid: '0x00c00011'
  viewable_candidate_geometry: '1920x1080'
  reply_client_base: '0x00c00000'
  reply_mask: LocalClientPid
  reply_value_length_bytes: 4
  reply_pid: 13648
  cleanup: COMPLETE
classification:
  primary: XRES_PROVES_VIEWABLE_WINDOW_OWNED_BY_EXACT_CLIENT
  physical_identity: PROVEN
  wrapper_red_job_semantics: EXPECTED_ASSERTION_FALSE_NEGATIVE_AFTER_VALID_RAW_EVIDENCE
validation:
  material_findings_open: 0
  review_threads_open: 0
  terminal_governance_run: 32016345778
  terminal_governance_result: SUCCESS
  ready_ci_run: 32016422937
  ready_required_job: 95347019361
  ready_required_result: SUCCESS
helper_followup:
  finding: XRES-V2-AUD-001
  severity: LOW
  blocking_task_closeout: false
  physical_retry_required: false
  owner: persistent raw-XRes helper / canonical runtime task
safety:
  canonical_state_access: NONE
  credentials_used: false
  login_used: false
  gameplay_used: false
  process_memory_accessed: false
  client_bytes_mutated: false
  additional_identity_launch_authorized: false
evidence:
  - docs/agents/evidence/OTC-20260817-track-a-xres-raw-pid-identity/20260817-v1-physical-parser-discriminator.md
  - docs/agents/evidence/OTC-20260817-track-a-xres-raw-pid-identity/20260817-helper-fix-audit.md
  - docs/agents/evidence/OTC-20260817-track-a-xres-raw-pid-identity/20260817-v2-physical-pid-identity.md
  - docs/agents/evidence/OTC-20260817-track-a-xres-raw-pid-identity/20260817-v2-final-audit.md
last_completed_step: PR #457 merged the conclusive physical XRes resource-to-exact-client PID evidence and this archive closeout releases all task ownership
next_action: none for this task; downstream runtime or worldmap physical validation must create its own fresh admission and may consume the proven identity evidence
---

# Track A raw XRes PID identity — archived

The task is terminal. The bounded physical identity gate was proven and merged. No runtime surface remains owned by this task and no further identity launch is authorized.
