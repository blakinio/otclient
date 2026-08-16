---
task_id: OTC-20260814-map-observation-track-a-correction
status: validating
agent: ChatGPT
session_id: chatgpt-coord-replay-20260816-1408
session_role: coordinator_replay_validator
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: documentation
phase: validate
branch: docs/OTC-20260814-map-observation-track-a-correction-v2
base_branch: main
base_main: 19556a5bca362dede3f9c2608902eda6e358b2bc
risk: low
updated: 2026-08-16T14:12:00+02:00
owned_paths:
  - docs/agents/contracts/MAP_OBSERVATION_V1.md
  - docs/agents/tasks/active/OTC-20260814-map-observation-track-a-correction.md
modules_touched: []
reuses:
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - coordinator-promoted Track A worldmap/runtime-bridge evidence only
depends_on: []
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: bounded contract ownership correction and exact-head validation require no checkout, physical runtime or owner-funded AI
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
user_communication: low_noise
context_pressure: low
context_growth: stable
context_score: 4
estimate_confidence: high
decomposition_decision: single
decomposition_reason: same stale task replayed from current main with one frozen contract and one task record
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
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
supersedes_pr: 295
supersession_reason: old branch predates current routing/admission governance and over-compresses frozen MAP_OBSERVATION_V1 semantics
acceptance:
  - preserve schema_version 1 record types and all existing field/completeness/order/delta/transition/forbidden-data semantics
  - correct current authoritative live producer to Track A official-client-re / official native Linux Tibia client
  - explicitly exclude Track B from current producer ownership
  - require coordinator-promoted Track A worldmap/runtime-bridge reuse without treating Draft or historical PR state as authority
  - replace stale OTClient ProtocolGame P1 wording with exact-client structural read-only P1 boundary
  - keep runtime_access none and make no current display/VNC/PID/session claim
  - exact-head required CI and Track A governance pass before promotion
  - zero unresolved review threads and old PR 295 remains intentionally closed superseded
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
last_completed_step: replayed the stale ownership correction from current main while preserving the full frozen v1 record contract
next_action: open the fresh replacement PR, verify full two-file diff, then run exact-head required CI/governance and independently audit wording before merge
---

# Correct MAP_OBSERVATION_V1 producer ownership to Track A

## Factual basis

The current `main` contract still describes the producer as OTClient decoded `Map`/`Tile` state. That conflicts with the current programme ownership: official-client observation/reconstruction belongs to Track A `official-client-re`; Track B remains isolated.

PR #295 identified the ownership defect but is intentionally closed superseded because its 2026-08-14 diff also removed/compressed frozen v1 record details and predates the mandatory current Track A routing/admission fields.

## Replay boundary

This replay changes only ownership/source and P1 integration wording. The existing JSONL schema, common fields, completeness rules, ordered thing identity, delta invariants, transition/action evidence and forbidden-data rules are preserved.

No live runtime operation, client instrumentation, login, VNC/X11 observation, client mutation, Track B mutation, proprietary material or owner-funded AI/API use is part of this task.
