---
task_id: OTC-20260816-track-a-canonical-client-window-wait-fix
status: implementing
agent: ChatGPT
session_id: chatgpt-coord-window-wait-fix-20260816-1746
session_role: runtime_infrastructure_maintainer
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: runtime_worker_repair
phase: implement
branch: fix/OTC-20260816-track-a-canonical-client-window-wait-fix
base_branch: main
base_main: ffe954be315ee29825c726b996a30fea8475a0f3
risk: medium
updated: 2026-08-16T17:46:00+02:00
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/test_tibia_official_client_re_canonical_live_session.py
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-client-window-wait-fix.md
modules_touched: []
reuses:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/20260816-v5-worker-timeout.md
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: deterministic worker wait-budget defect is fully testable without physical runtime; no Synology execution is required or authorized for this repair
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
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
owner_funded_ai_api_authorized: false
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
acceptance:
  - production client-window discovery uses one bounded wait budget comfortably below the transition worker timeout of 300 seconds
  - no nested outer loop multiplies the window helper wait budget
  - client liveness is checked during the window wait and preserves distinct client_exited versus client_window_missing classification
  - deterministic hosted tests exercise found-window and exited-client behavior and assert the production wait budget/invocation shape
  - no physical runtime, login, credentials, VNC, Synology or client execution is used by validation
  - exact-head Track A governance and repository CI pass before promotion
last_completed_step: claimed fresh current-main hosted-only worker repair after v5 checkpoint proved the nested window wait can exceed the supervisor budget
next_action: implement the single-budget window helper and deterministic tests, then run exact-head governance/CI and coordinator promotion
---

# Track A canonical client window wait fix

This task repairs only the deterministic wait-budget defect identified by canonical runtime v5. It must not trigger or emulate a physical canonical bootstrap.