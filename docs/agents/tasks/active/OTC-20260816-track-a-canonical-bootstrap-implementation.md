---
task_id: OTC-20260816-track-a-canonical-bootstrap-implementation
status: implementing
agent: ChatGPT
session_id: chatgpt-runtime-bootstrap-20260816-1328
session_role: implementation_worker
project_lane: otclient
lane: RUNTIME-INFRA
track_id: official-client-re
task_kind: implementation
phase: implement-bootstrap-rebind
branch: ci/OTC-20260816-track-a-canonical-bootstrap-implementation
base_branch: main
base_main: 0d7b2607912552599ae501891491aab439cfde7b
risk: high
updated: 2026-08-16T13:28:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-bootstrap-implementation.md
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - .github/scripts/test_track_a_agent_runtime_governance.py
modules_touched: []
reuses:
  - .github/scripts/tibia-official-client-re-canonical-live-lease.py
  - .github/scripts/tibia-official-client-re-canonical-live-guard.py
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
depends_on: []
blocks:
  - OTC-20260816-track-a-canonical-runtime-e2e
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: deterministic supervisor/transition implementation and tests only; physical Synology mutation is forbidden until reviewed code is promoted to main
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: implement and prove authority transaction primitives before any physical runtime consumer uses them
validation_level: heavy
session_rotation_count: 0
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 0
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
persistent_session_role: none
physical_e2e_required: false
owner_funded_ai_api_authorized: false
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
acceptance:
  - deterministic tests prove canonical flock is held continuously across bootstrap absence proof through atomic registration commit
  - bootstrap refuses missing/invalid/current-lease mismatch, existing registration and non-unique exact-client candidates
  - bootstrap validates a worker result against exact PID/start/exe/hash/display/window/state evidence before registration
  - registration is atomic mode 0600, generation-bound, and revalidated before success
  - worker cannot inherit lease capability or canonical flock fd
  - precommit failure cleans only explicitly proven bootstrap descendant process group
  - rebind is non-client-mutating, requires unchanged exact registered identity and current uniqueness, then atomically advances only registration metadata
  - cancellation/partial-failure tests remain fail-closed
  - existing lease/guard/governance tests remain green
last_completed_step: fresh-main no-runtime implementation task claimed after physical reconciliation proved canonical bootstrap required
next_action: implement transition supervisor and deterministic tests without Synology access
---

# Canonical live bootstrap/rebind implementation

This task exists only to make the already-accepted Track A bootstrap/rebind contract executable and testable. It owns no physical runtime. No branch code from this task may run on Synology until merged to trusted `main` and the RUNTIME owner refreshes from that promoted commit.
