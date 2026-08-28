---
task_id: OTC-20260828-current-login-field6-scalar-owner-promotion
status: validating
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: validate
branch: docs/OTC-20260828-current-login-field6-scalar-owner-promotion
base_branch: main
base_main: 7a7a7cc4d09dee08ea07f8c91144d8ac869111b7
created: 2026-08-28T15:25:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
canonical_boot_epoch_recovery: NOT_APPLICABLE
canonical_recovery: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
physical_action_budget: 0
physical_action_count: 0
physical_e2e_required: false
implementation_authorized: false
owned_paths:
  - docs/agents/evidence/OTC-20260828-current-login-field6-scalar-owner-promotion/**
  - docs/agents/tasks/active/OTC-20260828-current-login-field6-scalar-owner-promotion.md
modules_touched: []
reuses:
  - trusted-main promotion #747 current login field6 producer boundary
  - source-only PR #751 exact current scalar-owner discrimination
blocks:
  - Track B PR #284 CURRENT_GAME_LOGIN_FIELD6_VALUE_STILL_UNKNOWN
---

# Objective

Promote only independently revalidated exact-current facts from source Draft PR #751 that eliminate the remaining statically scalar `slot+0x60` candidates without inventing a `GameclientMessageLogin.field6` value.

# Acceptance

1. Docs/evidence only; source analyzers/workflows are not promoted.
2. Preserve exact client fence `15.32.75d4a0 / d1a16819... / 52105824`.
3. Preserve the independent three-candidate scalar census and focused exact re-assertion.
4. Promote `0xceddcb / edx=1` only as a rejected worldmap-path candidate, not as a login value.
5. Keep `GameclientMessageLogin.field6` runtime value UNKNOWN and prohibit Track B mutation/game E2E from this evidence.
6. Set the next blocker to governed read-only runtime observation of producer input `edx` at exact current `0xe25620`.
7. Require exact-head CI, Track A governance, fresh artifact audit and zero review blockers before merge.
8. After merge, close source #751 unmerged as consumed and archive promotion lifecycle before opening the runtime successor.

next_action: open the clean promotion PR, bind its number, require exact-head CI/governance and independent artifact audit, merge, close #751 unmerged as consumed, archive this promotion, then start the governed read-only runtime scalar-observation successor.
