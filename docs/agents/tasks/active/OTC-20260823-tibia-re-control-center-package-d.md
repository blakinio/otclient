---
task_id: OTC-20260823-tibia-re-control-center-package-d
status: implementing
agent: ChatGPT
session_id: chatgpt-20260823-package-d
session_role: architect_then_implementer
project_lane: otclient
lane: P4-OFFICIAL-ADAPTER
track_id: official-client-re
task_kind: implementation
phase: control_center_track_a_bridge_repository_only
risk: high
branch: docs/OTC-20260823-package-d-bridge-claim
base_branch: main
base_main: ca7c8eaffd4861e4345cc9eb866a9a4886f93773
created: 2026-08-23T13:26:00+02:00
updated: 2026-08-23T15:31:00+02:00
execution_mode: github_connector_then_track_a_runtime_if_admitted
execution_reason: owner-approved admission-first Package D design; staged repository PRs preserve independent Control Center and Track A audit boundaries before any separately admitted physical runtime operation
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
design_pr: 670
design_merge: 371f5a0451e9bf3e3eac29cc12edfecc310c3ea9
design_spec: docs/superpowers/specs/2026-08-23-control-center-package-d-design.md
implementation_plan: docs/superpowers/plans/2026-08-23-control-center-package-d.md
control_center_core_pr: 672
control_center_core_merge: 14409a502588b09ba0d30fbaed130df56d173aa0
track_a_guarded_transition_pr: 674
track_a_guarded_transition_head: 7f967acd13bb453ca6888e1741932fa657d068c6
track_a_guarded_transition_merge: ca7c8eaffd4861e4345cc9eb866a9a4886f93773
track_a_guarded_transition_validation:
  input_lock_linux: 6_of_6_pass
  canonical_transition_linux: 28_of_28_pass
  canonical_lease_linux: 14_of_14_pass
  canonical_guard_linux: 3_of_3_pass
  python_compile: pass
  git_diff_check: pass
  track_a_canonical_live_governance: pass
  track_a_agent_runtime_governance: pass
  repository_ci: pass
delivery_strategy: staged_prs_preserve_existing_audit_boundaries
planned_stages:
  - control_center_outcome_and_semantic_adapter
  - track_a_input_lock_and_guarded_transition
  - control_center_track_a_bridge
  - governance_and_runtime_admission
owned_paths_current_stage:
  - docs/agents/tasks/active/OTC-20260823-tibia-re-control-center-package-d.md
  - tools/tibia_re_control_center/official_adapter.py
  - tools/tibia_re_control_center/track_a_authority_bridge.py
  - tests/tools/tibia_re_control_center/test_package_d_official_adapter.py
planned_implementation_paths:
  - tools/tibia_re_control_center/execution.py
  - tools/tibia_re_control_center/official_adapter.py
  - tools/tibia_re_control_center/track_a_authority_bridge.py
  - tests/tools/tibia_re_control_center/test_package_d_official_adapter.py
  - .github/scripts/tibia-official-client-re-input-lock.py
  - .github/scripts/test_tibia_official_client_re_input_lock.py
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
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
  - .github/scripts/tibia-official-client-re-input-lock.py
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
  - docs/agents/evidence/OTC-20260823-tibia-re-control-center-package-d-prep/package-d-preparation.md
depends_on:
  - Package D PREP merge 292767ed19856f75be0c6e297bc7567013ee8f54
  - Package D design/plan merge 371f5a0451e9bf3e3eac29cc12edfecc310c3ea9
  - Package D semantic core merge 14409a502588b09ba0d30fbaed130df56d173aa0
  - Package D guarded transition merge ca7c8eaffd4861e4345cc9eb866a9a4886f93773
  - fresh physical runtime admission before any live operation
blocks:
  - no physical action may dispatch until canonical input.lock semantics are made normative in current Track A governance or another current trusted-base rule explicitly admits the reviewed implementation
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
first_action_status: NOT_YET_PHYSICALLY_PROVEN
---

# Control Center Package D — active task

The owner approved design option 3 and explicitly approved the written design spec on 2026-08-23. The design and implementation plan were merged by docs-only PR #670 as `371f5a0451e9bf3e3eac29cc12edfecc310c3ea9`.

The semantic Control Center core is merged in PR #672. The canonical input serialization and two-phase guarded transition are merged in PR #674 as `ca7c8eaffd4861e4345cc9eb866a9a4886f93773`. This checkpoint claims only the next repository-only bridge stage: the semantic `OfficialTibiaAdapter`, new `CanonicalTrackAAuthorityBridge`, and their focused Package D tests.

The task remains `runtime_access:none`. No Official Tibia process/container/window/display/session/network/input operation is authorized by this checkpoint. Historical runtime facts do not authorize access.

The bridge must pass only the token file path to the existing Track A transition supervisor; it must never read or copy token contents. Public transport/result envelopes are exact-key and limited to action hash, fence digest, normalized outcome, reason code and evidence refs. Raw keys, GUI coordinates, opcodes, addresses, pointers, PID/XID/display/window identifiers, bridge handles, lease capabilities and credentials are forbidden across the Control Center boundary.

No physical action is permitted until the current shared input-lock governance rule is normative and the task is freshly re-admitted. The exact runtime order remains semantic validation/effect bound -> budget -> external Track A guard -> input lock -> final current Gate/identity checks -> READY -> Control Center commit -> COMMIT -> fresh final revalidation -> exactly one effect -> authoritative reconciliation. STOP/control-generation/identity/authority changes before commit invalidate waiting work.
