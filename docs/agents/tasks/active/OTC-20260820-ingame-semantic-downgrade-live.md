---
task_id: OTC-20260820-ingame-semantic-downgrade-live
status: ready
agent: ChatGPT
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: validation
phase: validate
branch: runtime/OTC-20260820-ingame-semantic-downgrade-live
base_branch: main
base_sha: 7e6b0a83253e871bdf6b7506e5026d73ee0a9a90
risk: high
runtime_access: canonical_reuse_or_mutation
runtime_owner_task: OTC-20260820-ingame-semantic-downgrade-live
runtime_namespace: canonical-live-runtime
canonical_registration: PRESENT
canonical_lease_generation: UNKNOWN
registration_lease_generation: UNKNOWN
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: UNKNOWN
mutation_authorized: false
metadata_transition_authorized: true
metadata_transition: semantic_downgrade
gui_input_authorized: false
process_control_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
owner_funded_ai_api_authorized: false
execution_mode: trusted_main_synology
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_stop
policy_version: 2
context_pressure: low
context_growth: stable
context_score: 4
decomposition_decision: single
current_blocker: none
next_action: on trusted main, freshly prove exact runtime identity and lease authority, perform only the metadata semantic-downgrade transition, then rerun the read-only Surveyor negative E2E on the still-logged-out target and archive
---

# Track A live semantic downgrade

This task owns only correction of the already-identified stale canonical registration semantics after PR #629. It must not log in, type credentials, select a character, send GUI input, restart/kill/signal/attach/inject into the client, or perform gameplay.

The only write permitted on the physical runtime is the reviewed `semantic-downgrade` canonical metadata transition from legacy `state=IN_GAME / state_evidence=BRIDGE_3_OF_3` to fail-closed `state=UNKNOWN / state_evidence=BRIDGE_3_OF_3_SEMANTICS_UNPROVEN`, after fresh stable exact-runtime identity and current lease authority are proven. `mutation_authorized=false` refers to client/runtime process mutation; the metadata authority transition is separately and explicitly bounded above.