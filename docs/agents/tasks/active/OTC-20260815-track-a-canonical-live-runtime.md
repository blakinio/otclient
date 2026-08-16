---
task_id: OTC-20260815-track-a-canonical-live-runtime
status: waiting
agent: unassigned
session_id: null
session_role: governance-integrator
session_rotation_count: 4
project_lane: otclient
lane: track-a-governance
track_id: official-client-re
task_kind: implementation
phase: integrate
branch: docs/OTC-20260815-track-a-canonical-live-runtime
base_branch: main
base_main: e9df81f50dbb231bc4ac6cc3fc21f260fc358d34
risk: medium
related_pr: 311
updated: 2026-08-16T02:17:00+02:00
lease_expires_at: null
lease_released_at: 2026-08-16T02:17:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-canonical-live-runtime.md
  - docs/agents/tasks/archive/OTC-20260815-track-a-canonical-live-runtime.md
  - docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md
  - docs/agents/evidence/OTC-20260815-track-a-canonical-live-runtime/**
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/CHANGELOG.md
depends_on:
  - final lease/supervisor manager merged by PR #316 as main@e9df81f50dbb231bc4ac6cc3fc21f260fc358d34
  - fresh manager archive PR #319 must merge
  - bootstrap contract PR #318 must be reconciled and promoted first
  - PR #303 runtime evidence remains factual input only and its runtime-owned surface must not be touched
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: protected_merge_then_archive
user_communication: terminal_only
implementation_authorized: true
last_progress_at: 2026-08-16T02:17:00+02:00
next_action: after PR #318 merges, claim this task, clean-restack PR #311 on final current main so Gate A requires final supervised whole-lifetime mutation semantics, Gate B requires current exact-runtime registration/preflight, and bootstrap remains a separate fail-closed transition; require exact-head CI/review and archive after protected merge
---

# Objective

Finish Track A canonical-live runtime governance on the final manager and bootstrap contracts while preserving strict separation between controller authority, current runtime identity and initial creation.

# Required final boundary

- Gate A: current authoritative lease plus final out-of-band supervisor for the entire mutation/process-tree lifetime.
- Gate B: current exact-runtime registration/preflight proving PID/process-start identity, exact version/size/SHA, display/window and mutation-relevant state.
- Initial creation/bootstrap: separate fail-closed transition; it is not ordinary Gate B reuse.
- Exact client fence: `15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- `:98`, `6082`, PID and session remain `UNKNOWN` / `NOT_REGISTERED` until direct evidence.
- PR #303 runtime-owned paths/processes and Track B remain untouched.
