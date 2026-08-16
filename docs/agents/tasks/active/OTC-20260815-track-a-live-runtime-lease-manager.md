---
task_id: OTC-20260815-track-a-live-runtime-lease-manager
status: validating
agent: ChatGPT
session_id: automation-20260816-0716-manager-cancellation
session_role: implementer
session_rotation_count: 7
project_lane: otclient
lane: track-a-runtime-governance
track_id: official-client-re
task_kind: implementation
phase: validate
branch: fix/OTC-20260815-track-a-live-runtime-lease-manager-cancellation
base_branch: main
base_main: 150460e3a13cca1b6f08d1c788f39d9c5319117d
risk: high
related_pr: 321
created: 2026-08-15T22:04:00+02:00
updated: 2026-08-16T07:25:00+02:00
lease_expires_at: 2026-08-16T08:10:00+02:00
lease_released_at: null
stale_takeover_count: 2
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-guard.py
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
last_progress_at: 2026-08-16T07:25:00+02:00
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
decomposition_decision: phased
validation_level: full
heavy_validation_runs: 1
human_interruptions: 0
ci_checks_for_current_head: 0
ci_check_generation: ready
terminal_ci_wait_started_at: 2026-08-16T07:25:00+02:00
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
stall_warnings: 0
reopen_reason: PR #311 fresh P1 PRRT_kwDOTVmdjs6ZkaMN proved the merged supervisor can die on process-group SIGTERM while a signal-ignoring guarded descendant survives, prematurely releasing coordination.lock
previous_closeout: PR #319 archived the pre-finding manager at main e9df81f50dbb231bc4ac6cc3fc21f260fc358d34; that closeout is superseded for final Track A governance by this reopening
previous_session_state: terminally released; no active manager session or lease existed on main, so no stale takeover or concurrent branch ownership was performed
pre_final_validation_head: bad931b659956de75d0ba06cb1efeb82d7261559
pre_final_unit_job: 95120547075
pre_final_unit_result: success
pre_final_audit_job: 95120547040
pre_final_audit_result: success
last_completed_step: cancellation-safe supervisor implementation, deterministic signal-ignoring process-group regression, fresh-audit assertions and changelog update are complete; pre-final GitHub-hosted unit and fresh independent audit passed
next_action: require deterministic unit, isolated Synology, fresh independent audit, zero material review findings and repository CI / Required PASS on the frozen exact PR #321 head, then protected-merge and perform a fresh manager closeout/archive
---

# Objective

Repair the post-closeout cancellation P1 without weakening the final out-of-band supervisor model: cancellation of a foreground guard process group must not release the coordination flock while any guarded descendant remains alive.

# Repair

The caller blocks `SIGHUP`, `SIGINT`, `SIGQUIT` and `SIGTERM` immediately across the supervisor fork. The lock-owning child installs non-terminating handlers before restoring the inherited mask, preventing cancellation from killing the sole flock owner during post-fork setup. A cancellation already pending before the child existed is relayed while the child remains masked. Once dispatched, a guarded command still receives no flock descriptor; if it deliberately ignores process-group cancellation, the child-subreaper remains alive and retains `coordination.lock` until the primary plus all adopted/orphaned descendants have exited.

The deterministic regression starts the guard in a fresh process group, waits until a guarded child has installed `SIGTERM` ignore behavior, sends `SIGTERM` to the whole process group, proves the foreground guard dies, proves nonblocking acquisition of `coordination.lock` still fails while the child survives, and then proves the supervisor releases the lock only after guarded lifetime ends.

# Safety boundary

- No Tibia launch, login, attach, input or runtime mutation.
- No credentials.
- Do not touch PR #303 runtime-owned paths/processes or Track B.
- Preserve exact client fence `15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- `:98`, `6082`, PID and session remain `UNKNOWN` / `NOT_REGISTERED`.
- No owner-funded Codex/OpenAI API or paid AI quota.
