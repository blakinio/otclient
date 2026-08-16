---
task_id: OTC-20260816-track-a-p1-bridge-health-recovery
status: validating
agent: ChatGPT
session_id: chatgpt-p1-fresh-main-20260816-1537
session_role: implementer
project_lane: otclient
lane: P1-BRIDGE
track_id: official-client-re
task_kind: implementation
phase: fresh-main-promotion
branch: feat/OTC-20260816-track-a-p1-bridge-health-recovery-v2
base_branch: main
base_main: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
current_main: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
created: 2026-08-16T15:37:00+02:00
updated: 2026-08-16T15:37:00+02:00
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
  freshness_disposition: DIVERGED_AHEAD_32_BEHIND_6_DO_NOT_MERGE_DIRECTLY
  review_threads_open: 0
  semantic_findings_open: 0
  accepted_component_validation:
    - run: 31947189849
      result: SUCCESS
    - run: 31947285170
      result: SUCCESS
    - run: 31947365151
      result: SUCCESS
  accepted_exact_head_governance: 31947837571
  accepted_exact_head_repository_ci: 31947837633
  later_infrastructure_failure:
    run: 31947967363
    job: 95167045910
    classification: GITHUB_429_BOOST_MIRROR_CLONE
    code_change_required: false
fresh_main_replay:
  accepted_blob_policy: implementation and tests copied by exact blob SHA from source head; no source branch history merged or rebased
  accepted_blobs:
    tests/tools/tibia_runtime_bridge/test_bridge.py: 7543000b822ccd57c6db64b1080e84b3a8437df1
    tests/tools/tibia_runtime_bridge/test_health.py: eed3085871c84fc4b342a3b27d140925fb6bacd2
    tools/tibia_runtime_bridge/CMakeLists.txt: 588293427b6a4f07b91aede0858402da0084ce75
    tools/tibia_runtime_bridge/README.md: d8e8bd4844a8d095e3876ea2baab5558a18a6786
    tools/tibia_runtime_bridge/__init__.py: 3cb0afd1ef3f0ddebeca9d0fd6b410ecc59bfeb5
    tools/tibia_runtime_bridge/bridge.cpp: c47dc3e81162867692e7608f14a9f53dea52bf3b
    tools/tibia_runtime_bridge/health.py: 6181bbd364c8caef5e1e6ee847bf188a721d2cdf
    tools/tibia_runtime_bridge/ipc_client.py: 63bdb9258ce2c67781f43de8f4a482024fc89672
    tools/tibia_runtime_bridge/launcher.py: b92ec9b7752bbe031671ce3f0e521a74f2f1dc1b
    tools/tibia_runtime_bridge/profiles/tibia-15.32.df7b29.json: b3ad235e06170fcc291bb5a6936f75b3f3db65dc
    tools/tibia_runtime_bridge/resolver.py: 8cd1bb3b812c7e93fca641c80202dc69734071db
  shared_index_proof:
    compare_base: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
    source_head: 9ddab031da32c69c55dd2f6940583c2523f00c06
    changelog_delta: +1/-0
    module_catalog_delta: +1/-0
    method: exact source blobs reused only after compare proved they equal current-main content plus one P1 record each
acceptance:
  - preserve exact coordinator-accepted P1 bridge semantics and tests byte-for-byte
  - bind lifecycle IPC to Linux SO_PEERCRED plus boot/PID/start/executable identity and matching PING envelope
  - fail closed for stale registration, stale process identity, same-path endpoint replacement, protocol and transport failures
  - distinguish completed zero-hit discovery from incomplete/error process-memory scans
  - recovery remains bounded/read-only and never launches/logs-in/restarts/signals/attaches to the client
  - launcher LD_PRELOAD activation remains RUNTIME-owned and is not exercised by this P1 task
  - shared indexes preserve all current-main content and add only one P1 record each
  - obtain fresh exact-head Track A governance and repository CI from current main before promotion
  - coordinator performs final promotion review before merge
validation:
  source_semantic_audit: PASS_MATERIAL_FINDINGS_0
  fresh_main_exact_head_governance: PENDING
  fresh_main_repository_ci: PENDING
  physical_e2e: NOT_APPLICABLE_WITH_REASON
  physical_e2e_reason: P1 is a hosted producer; physical attach/restart/relogin evidence belongs to serialized RUNTIME ownership
last_completed_step: replayed accepted P1 code/tests by exact blobs onto main@dbd9520 and integrated shared indexes with compare-proven +1/-0 deltas
next_action: open fresh-main replacement Draft PR, close stale PR #357 superseded, validate exact head, then coordinator-review/promote if current main remains fresh
---

# Track A P1 bridge health/recovery fresh-main promotion

This task replaces the stale/diverged PR #357 promotion surface without changing its accepted semantic implementation. The source branch was 32 commits ahead but 6 commits behind current `main`, so it is not merged or rebased. Accepted implementation/test blobs are replayed directly on current main and the two serialized shared-index changes are reused only after a direct current-main comparison proved each is exactly one added P1 record with zero removals.

The live physical runtime remains outside this task. P1 claims no current display, VNC endpoint, PID, session, login state or physical attach evidence.
