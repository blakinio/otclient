---
task_id: OTC-20260824-canonical-rebind-repair
status: validating
agent: ChatGPT
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: implementation
phase: validate
policy_version: 2
branch: fix/OTC-20260824-canonical-rebind-repair
base_branch: main
base_sha: c8e9209c618a269b8c363051549419d784a6e7a7
risk: high
decomposition_decision: single
decomposition_reason: narrow existing canonical transition repair with one implementation surface and focused regression suite
context_pressure: medium
context_growth: stable
context_score: 6
estimate_confidence: high
execution_mode: local_terminal_and_github
execution_reason: isolated worktree for TDD; GitHub-hosted exact-head validation; no physical runtime is required or permitted
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
  - docs/agents/tasks/active/OTC-20260824-canonical-rebind-repair.md
  - docs/agents/CHANGELOG.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/tasks/archive/OTC-20260824-canonical-rebind-repair.md
modules_touched:
  - canonical-live-transition
reuses:
  - PR #688 terminal fail-closed evidence
  - current main canonical-live transition implementation
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
invocation_started_at: 2026-08-24T19:32:00+02:00
last_progress_at: 2026-08-24T20:10:40+02:00
ci_checks_for_current_head: 5
ci_check_generation: f441f7444c55a9480bbb59b24450b786c33ceb9d
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 1
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
acceptance:
  - canonical adoption rebind accepts the fail-closed evidence refresh BRIDGE_3_OF_3_SEMANTICS_UNPROVEN -> NO_STRUCTURAL_BRIDGE only when stable adoption identity is unchanged
  - stable adoption identity drift remains rejected before commit
  - the committed registration carries the fresh fail-closed state_evidence and ordinary Gate B remains strict
  - deterministic tests, independent audit, exact-head required CI, merge and terminal closeout complete without runtime/gameplay/client input
pr: 689
tdd_red: registered_identity_state_evidence_mismatch
focused_transition_tests: 30_OF_30_PASS
focused_py_compile: PASS
focused_track_a_governance: PASS
focused_git_diff_check: PASS
required_ci_f441: PASS
independent_audit_f441: PASS
review_threads_f441: 0
requested_changes_f441: 0
optional_package_a_f441: NON_BLOCKING_PATH_BOUNDARY_FALSE_POSITIVE
optional_package_a_core_f441: PASS
optional_package_a_failure_reason: shared CHANGELOG/MODULE_CATALOG trigger caused an unrelated canonical task diff to be evaluated against Package A-only changed-path allowlist; repository CI / Required and all task-specific Track A gates passed
current_blocker: NONE
implementation_head: 6976799c239d091ffc8370c7a785220848eb222d
next_action: freeze a ready-state checkpoint so exact-head required CI reruns with PR non-draft; merge only if required CI and task-specific Track A gates pass and no material review finding appears
---

# Canonical adoption rebind repair

Current `main` at task claim is `c8e9209c618a269b8c363051549419d784a6e7a7`, the merge commit of terminal PR #688. PR #688 proved that no physical action was dispatched and identified the repository blocker: a fresh adoption probe may legitimately tighten fail-closed evidence from `BRIDGE_3_OF_3_SEMANTICS_UNPROVEN` to `NO_STRUCTURAL_BRIDGE` while the stable adoption identity remains unchanged, but canonical rebind currently rejects the evidence difference before it can atomically refresh the registration.

This task is repository-only. It does not inspect, connect to, rebind, mutate, login to, or move the physical official-client runtime.