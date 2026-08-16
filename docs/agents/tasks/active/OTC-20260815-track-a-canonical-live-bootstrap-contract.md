---
task_id: OTC-20260815-track-a-canonical-live-bootstrap-contract
status: running
agent: ChatGPT
session_id: automation-20260816-0511-bootstrap-replacement
session_role: implementer
session_rotation_count: 2
project_lane: otclient
lane: track-a-runtime-governance
track_id: official-client-re
task_kind: contract
phase: implement
branch: docs/OTC-20260815-track-a-canonical-live-bootstrap-contract
base_branch: main
base_main: 25700f08c3f5729e4ee38bf8c0a3ca04020379be
risk: medium
related_pr: 318
updated: 2026-08-16T05:12:00+02:00
lease_expires_at: 2026-08-16T05:57:00+02:00
lease_released_at: null
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-canonical-live-bootstrap-contract.md
  - docs/agents/tasks/archive/OTC-20260815-track-a-canonical-live-bootstrap-contract.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/evidence/OTC-20260815-track-a-canonical-live-bootstrap-contract/**
depends_on:
  - final lease/supervisor manager merged by PR #316 as main@e9df81f50dbb231bc4ac6cc3fc21f260fc358d34
  - fresh manager archive merged by PR #319 as main@25700f08c3f5729e4ee38bf8c0a3ca04020379be
  - PR #311 must consume the final bootstrap distinction after PR #318 is promoted
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: narrow documentation reconciliation, review repair and exact-head GitHub validation require no owner-funded AI or local runtime mutation
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: protected_merge_then_archive
user_communication: terminal_only
implementation_authorized: false
invocation_started_at: 2026-08-16T05:11:13+02:00
last_progress_at: 2026-08-16T05:12:00+02:00
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: high
decomposition_decision: single
validation_level: focused
heavy_validation_runs: 0
stale_takeover_count: 1
stale_takeover_reason: predecessor lease expired at 2026-08-16T05:06:00+02:00 and PR head/task branch showed no writes after 2026-08-16T04:23:15+02:00; live review state exposed unresolved material P1 findings requiring replacement-session repair
human_interruptions: 0
ci_checks_for_current_head: 0
ci_check_generation: repair_required
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
audit_result: SUPERSEDED_BY_REVIEW_FINDINGS
audit_evidence: docs/agents/evidence/OTC-20260815-track-a-canonical-live-bootstrap-contract/20260816-independent-contract-audit.md
audit_material_findings_open: 3
e2e_result: NOT_APPLICABLE
e2e_reason: documentation-only bootstrap contract; live bootstrap implementation and real-client execution are explicitly outside this PR and require a future separately authorized task
last_completed_step: replacement-session takeover persisted after stale predecessor lease; exact prior head CI / Required was green but three unresolved P1 review findings invalidate promotion until repaired
next_action: repair all three P1 bootstrap contract findings on this branch, rerun fresh independent contract audit and exact-head CI, resolve review threads, then protected-merge only if clean
---

# Objective

Promote the documentation-only initial canonical-session bootstrap contract against the final lease-manager/supervisor stack without authorizing or performing a live client bootstrap.

# Safety boundary

- Contract only; implementation and live login remain unauthorized.
- Initial creation stays a separate fail-closed transition from ordinary registered-runtime reuse.
- `:98`, `6082`, PID and session remain `UNKNOWN` / `NOT_REGISTERED` without direct evidence.
- Exact client fence remains `15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- PR #303 runtime-owned paths/processes and Track B remain untouched.
