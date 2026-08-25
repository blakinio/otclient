---
task_id: OTC-20260825-canonical-boot-epoch-registration-recovery
status: completed
phase: archived
agent: ChatGPT
session_id: chatgpt-canonical-boot-epoch-registration-recovery-20260825
session_role: released
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: implementation
policy_version: 2
branch: docs/OTC-20260825-canonical-boot-epoch-registration-recovery-closeout
base_branch: main
base_sha: b0ebce78eff3c580ef70fc805480fd15449000b1
risk: high
decomposition_decision: single
decomposition_reason: one bounded canonical-registration metadata lifecycle extending the existing transition authority boundary
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
execution_mode: local_terminal_and_github
execution_reason: isolated worktree for TDD and deterministic repository validation; no physical runtime access is required or authorized
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
  - .github/workflows/track-a-canonical-live-governance.yml
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
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
  - docs/agents/tasks/active/OTC-20260825-canonical-boot-epoch-registration-recovery.md
modules_touched:
  - canonical-live-transition
  - track-a-runtime-admission-governance
reuses:
  - PR #693 canonical stale-registration recovery implementation and tests
  - PR #694 terminal boot-identity-discontinuity evidence
  - canonical lease/supervisor authority root and coordination flock
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
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
input_allowed: false
movement_allowed: false
ROUTING_CONTRACT: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
invocation_started_at: 2026-08-25T16:00:00+02:00
last_progress_at: 2026-08-25T18:52:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: ready
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
acceptance:
  - add a distinct canonical_boot_epoch_recovery admission class and boot-epoch-registration-recovery transition; neither may weaken canonical_recovery from PR #693 or masquerade as rebind
  - old registration must be authoritative existing-runtime adoption, exact-fenced, UNKNOWN/fail-closed, from a different boot identity and older lease generation
  - a repeated fresh adoption proof must establish the current boot identity, complete all-running-Docker inventory, exactly one current exact-fenced target and a self-consistent fresh fingerprint
  - boot discontinuity must positively prove the prior registered process instance cannot survive in the current boot epoch
  - canonical Docker namespace, display, remote-view endpoint/mapping and current X11 window-to-PID identity must be unambiguous; both PID and start ticks are fresh
  - recovery runs only under the current valid canonical lease and continuously held canonical coordination flock
  - registration replacement is atomic, registration-generation-incremented, current-lease-generation-bound and CAS-protected against concurrent registration drift
  - identical fresh proof is required before commit and after commit; post-commit failure rolls back only the transaction's exact committed record
  - recovered registration remains state UNKNOWN and grants no login, credentials, relog, restart, character selection, gameplay, input, movement or semantic promotion authority
  - deterministic TDD covers success plus same-boot refusal, non-adoption/state/fence/uniqueness/namespace/display/window/process/fingerprint/lease/probe-drift/registration-race/rollback boundaries
  - Track A governance, independent audit, exact-head required CI, merge and terminal closeout complete with runtime_access:none
source_terminal_prs: [693, 694]
source_terminal_main: b0ebce78eff3c580ef70fc805480fd15449000b1
baseline_transition_tests: PASS_37
tdd_red: PASS_EXPECTED_FAILURE_BOOT_EPOCH_OPERATION_ABSENT
focused_transition_tests: PASS_42
focused_track_a_governance: PASS
git_diff_check: PASS
baseline_kasm_probe_tests: PASS_10
baseline_track_a_governance: PASS
runtime_recovery_executed: false
semantic_promotion_performed: false
physical_action_performed: false
runtime_mutation_performed: false
e2e: NOT_APPLICABLE
e2e_reason: repository-only metadata transition implementation; owner explicitly prohibited physical runtime actions
current_blocker: NONE
implementation_pr: 696
implementation_head: 8263dc1fe10911e343b2a61aa7fafb8d4c8ed48b
implementation_merge: bc54657d35b9b8d898f6da57aac830e51d74bea2
independent_audit: PASS
independent_audit_review: 5021555242
independent_audit_material_findings_open: 0
exact_head_ci_run: 32873930391
exact_head_ci: PASS
exact_head_track_a_governance_run: 32873930019
exact_head_track_a_governance: PASS
exact_head_canonical_live_governance_run: 32873930001
exact_head_canonical_live_governance: PASS
package_a_cross_trigger_run: 32873929966
package_a_cross_trigger_disposition: NON_REQUIRED_PATH_BOUNDARY_FALSE_POSITIVE_CORE_PASS
ownership_released: true
task_archived: true
next_action: NONE
---

# Canonical boot-epoch registration recovery

Repository-only implementation task created from current main after terminal PRs #693 and #694. The task introduces a separately reviewed fail-closed registration lifecycle for a proven boot-epoch discontinuity. It does not execute that lifecycle against the live Tibia client and grants no runtime, login, credential, gameplay, input or semantic-promotion authority.

## Terminal closeout

Implementation PR #696 merged as `bc54657d35b9b8d898f6da57aac830e51d74bea2` after exact-head 42/42 transition tests, Track A governance, canonical-live governance, CI, and fresh detached-checkout audit all passed. The Package A cross-trigger failed only its unrelated changed-path allowlist while its deterministic core passed. No canonical recovery execution, semantic promotion, login, credentials, relog, restart, character selection, gameplay, input, movement, or physical runtime action occurred. Ownership is released.
