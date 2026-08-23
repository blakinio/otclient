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
phase: track_a_guarded_transition_repository_only
risk: high
branch: feat/OTC-20260823-package-d-track-a-guarded-dispatch
base_branch: main
base_main: 5d6b4007dbf3b16911ad59204fb7f8beb635cf6c
created: 2026-08-23T13:26:00+02:00
updated: 2026-08-23T15:27:46+02:00
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
delivery_strategy: staged_prs_preserve_existing_audit_boundaries
planned_stages:
  - control_center_outcome_and_semantic_adapter
  - track_a_input_lock_and_guarded_transition
  - control_center_track_a_bridge
  - governance_and_runtime_admission
owned_paths_current_stage:
  - docs/agents/tasks/active/OTC-20260823-tibia-re-control-center-package-d.md
  - .github/scripts/tibia-official-client-re-input-lock.py
  - .github/scripts/test_tibia_official_client_re_input_lock.py
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
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
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
  - docs/agents/evidence/OTC-20260823-tibia-re-control-center-package-d-prep/package-d-preparation.md
depends_on:
  - Package D PREP merge 292767ed19856f75be0c6e297bc7567013ee8f54
  - Package D design/plan merge 371f5a0451e9bf3e3eac29cc12edfecc310c3ea9
  - current Track A authority/transition scripts on trusted main
  - fresh physical runtime admission before any live operation
blocks:
  - no physical action may dispatch until current GUI/shared input serialization is implemented and normative or an existing reviewed primitive is located and proven
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
track_a_guarded_transition_pr: 674
track_a_guarded_transition_head: 00cbc3f639560b82e0faa70a6a027ece046af1f7
track_a_guarded_transition_validation:
  input_lock_linux: 4_of_4_pass
  canonical_transition_linux: 26_of_26_pass
  canonical_lease_linux: 14_of_14_pass
  canonical_guard_linux: 3_of_3_pass
  python_compile: pass
  git_diff_check: pass
  track_a_canonical_live_governance: pass
  track_a_agent_runtime_governance: pending_checkpoint_refresh
---

# Control Center Package D — active task

The owner approved design option 3 and then explicitly approved the written design spec on 2026-08-23. The design and implementation plan were merged by docs-only PR #670 as `371f5a0451e9bf3e3eac29cc12edfecc310c3ea9`.

Implementation is deliberately staged because the existing Package A fresh falsification audit allows only Control Center implementation/test paths and would correctly reject unrelated Track A `.github/scripts/**` changes. Package D will therefore not weaken that audit merely to fit a mixed PR. Control Center code/tests and Track A authority/input infrastructure are separate implementation stages under this same active task, with task checkpoints serialized through docs-only updates when needed.

The task remains `runtime_access:none` during repository implementation. It MUST be freshly re-admitted and this checkpoint updated before any Official Tibia process/container/window/display/session/network/input operation. Historical runtime facts do not authorize access.

The adapter must reuse the current Track A lease, canonical transition/rebind/Gate B and whole-lifetime guard. The Control Center local `dispatch_gate` remains local safety serialization only and MUST NOT be held while waiting for external Track A authority or the shared GUI/input lock.

No physical action is permitted unless the exact current chain succeeds: semantic validation and finite EffectBound -> budget reservation -> fresh external Track A authority/whole-lifetime guard -> shared GUI/input lock -> final registration/lease/generation/Gate/capability/identity/target checks -> one-shot Control Center `commit_dispatch()` -> exactly one bounded physical effect under the same guard/lock -> authoritative reconciliation. Any STOP/control-generation/identity/authority change invalidates waiting work before commit.

Current first-slice status remains fail-closed. Package D PREP's `UNKNOWN` R/A grades are not promoted by task creation, design approval, repository implementation or fake E2E.