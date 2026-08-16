---
task_id: OTC-20260816-track-a-p1-bridge-health-recovery
status: ready
agent: ChatGPT
session_id: chatgpt-p1-fresh-main-20260816-1537
session_role: implementer
project_lane: otclient
lane: P1-BRIDGE
track_id: official-client-re
task_kind: implementation
phase: coordinator-promotion-ready
branch: feat/OTC-20260816-track-a-p1-bridge-health-recovery-v2
base_branch: main
base_main: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
current_main: 259e418b2c526f93bd697f07c42b73b1fd40a914
created: 2026-08-16T15:37:00+02:00
updated: 2026-08-16T16:07:00+02:00
risk: medium
researcher_delivery: draft_only
implementation_authorized: true
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-p1-bridge-health-recovery.md
  - tools/tibia_runtime_bridge/**
  - tests/tools/tibia_runtime_bridge/**
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
modules_touched:
  - Track A official-client runtime bridge tooling
reuses:
  - PR #357 accepted P1 semantic implementation and hosted evidence
  - merged coordinator serialization PR #370
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_P1_BRIDGE_ALIAS.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
supersedes_pr: 357
depends_on:
  - RUNTIME for later physical attach/restart/relogin evidence; not mutated by this task
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: fresh-main replay and deterministic validation require no physical runtime or owner-funded AI
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
decomposition_decision: single
decomposition_reason: exact accepted P1 content replayed onto current main to remove stale/diverged branch history before promotion
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
validation_level: component
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
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
owner_funded_ai_api_authorized: false
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
source_pr:
  number: 357
  accepted_head: 9ddab031da32c69c55dd2f6940583c2523f00c06
  disposition: CLOSED_SUPERSEDED_BY_372
  semantic_findings_open: 0
  accepted_component_validation:
    - {run: 31947189849, result: SUCCESS}
    - {run: 31947285170, result: SUCCESS}
    - {run: 31947365151, result: SUCCESS}
fresh_main_replay:
  accepted_blob_policy: implementation and tests copied by exact blob SHA from source head; no source branch history merged or rebased
  shared_index_proof:
    compare_base: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
    source_head: 9ddab031da32c69c55dd2f6940583c2523f00c06
    changelog_delta: +1/-0
    module_catalog_delta: +1/-0
    method: exact source blobs reused only after compare proved they equal current-main content plus one P1 record each
  later_main_advance:
    from: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
    to: 259e418b2c526f93bd697f07c42b73b1fd40a914
    compare_status: NON_OVERLAPPING
    files:
      - .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
      - .github/scripts/tibia-official-client-re-canonical-live-session.sh
      - .github/scripts/tibia-official-client-re-canonical-live-transition.py
      - docs/agents/tasks/archive/OTC-20260816-track-a-canonical-bootstrap-implementation.md
acceptance:
  - preserve exact coordinator-accepted P1 bridge semantics and tests byte-for-byte
  - bind lifecycle IPC to Linux SO_PEERCRED plus boot/PID/start/executable identity and matching PING envelope
  - fail closed for stale registration, stale process identity, same-path endpoint replacement, protocol and transport failures
  - distinguish completed zero-hit discovery from incomplete/error process-memory scans
  - recovery remains bounded/read-only and never launches/logs-in/restarts/signals/attaches to the client
  - launcher LD_PRELOAD activation remains RUNTIME-owned and is not exercised by this P1 task
  - shared indexes preserve all current-main content and add only one P1 record each
  - coordinator performs final promotion review before merge
validation:
  source_semantic_audit: PASS_MATERIAL_FINDINGS_0
  accepted_replay_head: 7865507fd583a32d5065e1926e51bc80c5af09f6
  accepted_replay_track_a_governance_run: 31950483860
  accepted_replay_track_a_governance_result: SUCCESS
  accepted_replay_canonical_live_governance_run: 31950483871
  accepted_replay_canonical_live_governance_result: SUCCESS
  accepted_replay_repository_ci_run: 31950483984
  accepted_replay_repository_ci_result: SUCCESS
  final_checkpoint_head: PENDING_AFTER_THIS_TASK_ONLY_UPDATE
  final_checkpoint_track_a_governance: PENDING
  final_checkpoint_repository_ci: PENDING
  review_threads_open: 0
  physical_e2e: NOT_APPLICABLE_WITH_REASON
  physical_e2e_reason: P1 is a hosted producer; physical attach/restart/relogin evidence belongs to serialized RUNTIME ownership
audit:
  result: PASS
  material_findings_open: 0
last_completed_step: verified accepted replay exact-head governance/canonical-live governance/repository CI, closed source PR #357 superseded, and proved trusted-main advance through #371/#375 changes only non-overlapping RUNTIME-INFRA/archive paths
next_action: obtain final exact-head governance and repository CI after this task-only checkpoint update, then coordinator mark ready and squash-merge PR #372; archive and release ownership after merge
---

# Track A P1 bridge health/recovery fresh-main promotion

This task promotes the accepted P1 bridge without importing the stale history of PR #357. The fresh replay preserves the accepted implementation/tests and the two coordinator-serialized shared-index additions. The live physical runtime remains outside P1 ownership; `session-status` remains derived until separately correlated by RUNTIME.
