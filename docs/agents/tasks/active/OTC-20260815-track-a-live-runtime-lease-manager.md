---
task_id: OTC-20260815-track-a-live-runtime-lease-manager
status: implementing
agent: ChatGPT
session_id: automation-20260816-0716-manager-cancellation
session_role: implementer
session_rotation_count: 7
project_lane: otclient
lane: track-a-runtime-governance
track_id: official-client-re
task_kind: implementation
phase: implement
branch: fix/OTC-20260815-track-a-live-runtime-lease-manager-cancellation
base_branch: main
base_main: 150460e3a13cca1b6f08d1c788f39d9c5319117d
risk: high
related_pr: null
created: 2026-08-15T22:04:00+02:00
updated: 2026-08-16T07:16:00+02:00
lease_expires_at: 2026-08-16T08:01:00+02:00
lease_released_at: null
stale_takeover_count: 2
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-guard.py
  - .github/scripts/test_tibia_official_client_re-canonical-live-guard.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_guard.py
  - .github/workflows/tibia-official-client-re-canonical-live-lease.yml
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260815-track-a-live-runtime-lease-manager.md
  - docs/agents/tasks/archive/OTC-20260815-track-a-live-runtime-lease-manager.md
  - docs/agents/evidence/OTC-20260815-track-a-live-runtime-lease-manager/**
modules_touched:
  - track-a-runtime-governance
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: bounded manager code/test/workflow repair and GitHub validation can be completed without owner-funded AI or live runtime mutation
run_scope: single_task
continuation_policy: protected_merge_then_fresh_closeout
task_completion_policy: protected_merge_then_archive
user_communication: terminal_only
implementation_authorized: true
last_progress_at: 2026-08-16T07:16:00+02:00
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
decomposition_decision: phased
validation_level: focused
heavy_validation_runs: 0
human_interruptions: 0
ci_checks_for_current_head: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
stall_warnings: 0
reopen_reason: PR #311 fresh P1 PRRT_kwDOTVmdjs6ZkaMN proved the merged supervisor can die on process-group SIGTERM while a signal-ignoring guarded descendant survives, prematurely releasing coordination.lock
previous_closeout: PR #319 archived the pre-finding manager at main e9df81f50dbb231bc4ac6cc3fc21f260fc358d34; that closeout is superseded for final Track A governance by this reopening
previous_session_state: terminally released; no active manager session or lease existed on main, so no stale takeover or concurrent branch ownership was performed
last_completed_step: live main, archived manager task, released prior lease, PR #311 review state and current supervisor implementation reverified; dedicated repair branch claimed from main@150460e3a13cca1b6f08d1c788f39d9c5319117d
next_action: make the lock-owning subreaper cancellation-safe and add a deterministic signal-ignoring-descendant regression before exact-head validation
---

# Objective

Repair the post-closeout cancellation P1 without weakening the final out-of-band supervisor model: cancellation of a foreground guard process group must not release the coordination flock while any guarded descendant remains alive.

# Safety boundary

- No Tibia launch, login, attach, input or runtime mutation.
- No credentials.
- Do not touch PR #303 runtime-owned paths/processes or Track B.
- Preserve exact client fence `15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- `:98`, `6082`, PID and session remain `UNKNOWN` / `NOT_REGISTERED`.
- No owner-funded Codex/OpenAI API or paid AI quota.
