---
task_id: OTC-20260824-canonical-stale-registration-recovery
status: implementing
phase: implement
agent: ChatGPT
session_id: chatgpt-canonical-stale-registration-recovery-20260824
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: implementation
policy_version: 2
branch: fix/OTC-20260824-canonical-stale-registration-recovery
base_branch: main
base_sha: 6f8efdaa0b9c9fb7bbaa5c36605a23e21155883f
risk: high
decomposition_decision: single
decomposition_reason: one bounded canonical-registration metadata lifecycle extending the existing transition authority boundary
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
execution_mode: local_terminal_and_github
execution_reason: isolated worktree for TDD and deterministic repository validation; no physical runtime is required or authorized
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
  - .github/scripts/test_track_a_agent_runtime_governance.py
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_RUNTIME_ALIAS.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_COORDINATOR_ALIAS.md
  - docs/agents/README.md
  - docs/agents/AGENTS.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260824-canonical-stale-registration-recovery.md
  - docs/agents/tasks/archive/OTC-20260824-canonical-stale-registration-recovery.md
modules_touched:
  - canonical-live-transition
  - track-a-runtime-admission-governance
reuses:
  - PR #692 terminal stale-registration evidence
  - PR #689 narrow rebind evidence-refresh repair
  - merged canonical transition and Kasm adoption proof from PR #596
  - canonical lease/supervisor authority root and flock
  - authoritative runtime-registration.json namespace
depends_on: []
blocks: []
track_a_runtime_admission_version: 1
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
ROUTING_CONTRACT: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
invocation_started_at: 2026-08-24T22:57:00+02:00
last_progress_at: 2026-08-24T22:57:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
acceptance:
  - add distinct canonical_recovery admission class and stale-registration-recovery transition; neither is ordinary generation rebind
  - recovery requires current Gate A/coordination flock and the one authoritative canonical registration path only
  - old registration must be existing-runtime adoption, fail-closed UNKNOWN, exact current fence, and stale in both PID and process-start identity
  - fresh adoption proof must be complete and singleton across all running Docker containers on the exact accepted fence
  - recovery requires continuity of boot identity, canonical container name, display and remote-view endpoint while allowing only runtime-instance identity replacement
  - recovery repeats identical fresh proof before commit and after commit, increments registration_generation, binds lease_generation to current controller, and rolls back exact old registration on post-commit failure
  - recovered registration persists fresh UNKNOWN state/evidence and cannot promote IN_GAME or grant client mutation authority
  - no new state root, registration path, lock, lease, token or authority system is introduced
  - deterministic tests prove success plus stale/fence/uniqueness/continuity/drift/rollback/lease-change refusal cases
  - Track A governance, independent audit, exact-head required CI, merge and terminal closeout complete with runtime_access:none
source_terminal_pr: 692
source_terminal_main: 6f8efdaa0b9c9fb7bbaa5c36605a23e21155883f
tdd_red: PASS_EXPECTED_FAILURE_MISSING_RECOVERY_OPERATION
tdd_red_head: 80125b53be5a3fce4b0664bd7e990bfdbe45f7c3
tdd_red_run: 32778517429
tdd_red_job: 97595046076
tdd_red_result: 36 tests executed; existing cases PASS; 10 expected recovery errors from missing parser operation/function
focused_transition_tests: PENDING
focused_governance_tests: PENDING
independent_audit: PENDING
required_ci: PENDING
current_blocker: NONE
next_action: implement the smallest stale-registration-recovery transition that makes the Linux RED cases pass without weakening rebind or Gate B
---

# Canonical stale-registration recovery

This repository-only task introduces a separately named, fail-closed metadata recovery lifecycle for the exact terminal condition proven by PR #692. It does not execute the lifecycle against the live client and cannot use its own unmerged governance edits as runtime authority.

The lifecycle remains inside the existing canonical state root, coordination flock, lease capability and authoritative `runtime-registration.json`. It may replace stale adoption runtime identity only after complete singleton exact-target proof and narrow continuity checks; all client/gameplay/login/process mutation remains forbidden.
