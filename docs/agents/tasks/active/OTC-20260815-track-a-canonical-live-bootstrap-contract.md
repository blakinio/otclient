---
task_id: OTC-20260815-track-a-canonical-live-bootstrap-contract
status: ready
agent: unassigned
session_id: null
session_role: bootstrap-contract-integrator
session_rotation_count: 0
project_lane: otclient
lane: track-a-runtime-governance
track_id: official-client-re
task_kind: contract
phase: integrate
branch: docs/OTC-20260815-track-a-canonical-live-bootstrap-contract
base_branch: main
base_main: e9df81f50dbb231bc4ac6cc3fc21f260fc358d34
risk: medium
related_pr: 318
updated: 2026-08-16T02:16:00+02:00
lease_expires_at: null
lease_released_at: 2026-08-16T02:16:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-canonical-live-bootstrap-contract.md
  - docs/agents/tasks/archive/OTC-20260815-track-a-canonical-live-bootstrap-contract.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/evidence/OTC-20260815-track-a-canonical-live-bootstrap-contract/**
depends_on:
  - final lease/supervisor manager merged by PR #316 as main@e9df81f50dbb231bc4ac6cc3fc21f260fc358d34
  - fresh manager archive PR #319 must merge before this task is claimed
  - PR #311 must consume the final bootstrap distinction after PR #318 is promoted
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: protected_merge_then_archive
user_communication: terminal_only
implementation_authorized: false
last_progress_at: 2026-08-16T02:16:00+02:00
next_action: after PR #319 merges, claim this task, clean-restack PR #318 on current main, reconcile the contract against the final out-of-band supervisor, require exact-head checks/review, and protected-merge only if clean; do not launch/login a client
---

# Objective

Promote the documentation-only initial canonical-session bootstrap contract against the final lease-manager/supervisor stack without authorizing or performing a live client bootstrap.

# Safety boundary

- Contract only; implementation and live login remain unauthorized.
- Initial creation stays a separate fail-closed transition from ordinary registered-runtime reuse.
- `:98`, `6082`, PID and session remain `UNKNOWN` / `NOT_REGISTERED` without direct evidence.
- Exact client fence remains `15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- PR #303 runtime-owned paths/processes and Track B remain untouched.
