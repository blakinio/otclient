---
task_id: OTC-20260823-tibia-re-control-center-package-d
status: designing
agent: ChatGPT
session_id: chatgpt-20260823-package-d
session_role: architect_then_implementer
project_lane: otclient
lane: P4-OFFICIAL-ADAPTER
track_id: official-client-re
task_kind: implementation
phase: design
risk: high
branch: feat/OTC-20260823-tibia-re-control-center-package-d
base_branch: main
base_main: 6e8ce50a734097363484c6173570eb934d759b83
created: 2026-08-23T13:26:00+02:00
updated: 2026-08-23T13:26:00+02:00
execution_mode: github_connector_then_track_a_runtime_if_admitted
execution_reason: approved admission-first Package D design; repository work precedes any separately admitted physical runtime operation
policy_version: 2
prompting_standard_version: 2.1
validation_level: high
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
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
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
network_listener_allowed: false
official_client_access: false
physical_e2e_required: conditional_after_fresh_admission
owner_funded_ai_api_authorized: false
direct_codex_authorized: false
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
owned_paths:
  - docs/agents/tasks/active/OTC-20260823-tibia-re-control-center-package-d.md
  - docs/superpowers/specs/2026-08-23-control-center-package-d-design.md
planned_implementation_paths:
  - tools/tibia_re_control_center/official_adapter.py
  - tests/tools/tibia_re_control_center/test_package_d_official_adapter.py
  - .github/scripts/tibia-official-client-re-input-lock.py
  - .github/scripts/test_tibia_official_client_re_input_lock.py
shared_paths_pending_revalidation:
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
modules_touched:
  - tibia_re_control_center Official Tibia runtime adapter architecture
  - Track A canonical authority/transition reuse boundary
  - shared GUI/input serialization boundary
reuses:
  - tools/tibia_re_control_center/official_adapter_contract.py
  - tools/tibia_re_control_center/model.py
  - tools/tibia_re_control_center/scenario.py
  - tools/tibia_re_control_center/execution.py
  - .github/scripts/tibia-official-client-re-canonical-live-lease.py
  - .github/scripts/tibia-official-client-re-canonical-live-guard.py
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
  - docs/agents/evidence/OTC-20260823-tibia-re-control-center-package-d-prep/package-d-preparation.md
depends_on:
  - Package D PREP merge 292767ed19856f75be0c6e297bc7567013ee8f54
  - current Track A authority/transition scripts on trusted main
  - fresh physical runtime admission before any live operation
blocks:
  - no physical action may dispatch until current GUI/shared input serialization is implemented or an existing reviewed primitive is located and proven
  - no action capability promotion without fresh current semantic action and authoritative confirmation evidence
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
approved_design: admission_first_conditional_single_action_promotion
preferred_first_candidate: turn
fallback_candidate: move
first_action_rule: exactly_one_action_may_be_promoted_only_after_full_fresh_proof
---

# Control Center Package D — active task

The owner approved design option 3 on 2026-08-23: admission-first, then conditional promotion of exactly one bounded Official Tibia action. `turn` is the preferred first candidate and `move` is only a separately proven fallback.

This task starts in repository-only design mode with `runtime_access:none`. It MUST be re-admitted and this checkpoint updated before any Official Tibia process/container/window/display/session/network/input operation. Historical runtime facts do not authorize access.

The adapter must reuse the current Track A lease, canonical transition/rebind/Gate B and whole-lifetime guard. The Control Center local `dispatch_gate` remains local safety serialization only and MUST NOT be held while waiting for external Track A authority or the shared GUI/input lock.

No physical action is permitted unless the exact current chain succeeds: semantic validation and finite EffectBound -> budget reservation -> fresh external Track A authority/whole-lifetime guard -> shared GUI/input lock -> final registration/lease/generation/Gate/capability/identity/target checks -> one-shot Control Center `commit_dispatch()` -> exactly one bounded physical effect under the same guard/lock -> authoritative reconciliation. Any STOP/control-generation/identity/authority change invalidates waiting work before commit.

Current first-slice status remains fail-closed until new evidence exists. Package D PREP's `UNKNOWN` R/A grades are not promoted by task creation or design approval.