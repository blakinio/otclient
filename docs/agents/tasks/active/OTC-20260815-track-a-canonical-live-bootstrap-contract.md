---
task_id: OTC-20260815-track-a-canonical-live-bootstrap-contract
status: validating
agent: ChatGPT
session_id: chatgpt-20260816-0416-bootstrap
session_role: bootstrap-contract-integrator
session_rotation_count: 1
project_lane: otclient
lane: track-a-runtime-governance
track_id: official-client-re
task_kind: contract
phase: validate
branch: docs/OTC-20260815-track-a-canonical-live-bootstrap-contract
base_branch: main
base_main: 25700f08c3f5729e4ee38bf8c0a3ca04020379be
risk: medium
related_pr: 318
updated: 2026-08-16T04:24:00+02:00
lease_expires_at: 2026-08-16T05:09:00+02:00
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
execution_reason: narrow documentation reconciliation, PR state inspection and exact-head GitHub validation require no owner-funded AI or local runtime mutation
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: protected_merge_then_archive
user_communication: terminal_only
implementation_authorized: false
last_progress_at: 2026-08-16T04:24:00+02:00
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: high
decomposition_decision: single
validation_level: full
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 0
last_completed_step: reconciled the bootstrap contract against final main guard-run source and reviewed the complete PR #318 diff; scope is exactly the contract plus this task record, with no PR #303 runtime-owned paths, Track B, live runtime or credential mutation
next_action: require zero unresolved review findings and exact-head repository CI PASS on this frozen combined head, then protected-merge PR #318 and perform fresh post-merge task archival/release before claiming PR #311
---

# Objective

Promote the documentation-only initial canonical-session bootstrap contract against the final lease-manager/supervisor stack without authorizing or performing a live client bootstrap.

# Safety boundary

- Contract only; implementation and live login remain unauthorized.
- Initial creation stays a separate fail-closed transition from ordinary registered-runtime reuse.
- `:98`, `6082`, PID and session remain `UNKNOWN` / `NOT_REGISTERED` without direct evidence.
- Exact client fence remains `15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- PR #303 runtime-owned paths/processes and Track B remain untouched.
