---
task_id: OTC-20260815-track-a-live-runtime-lease-manager
status: active
agent: ChatGPT
session_id: chatgpt-live-runtime-lease-manager-20260815-2204
session_role: implementation-worker
session_rotation_count: 0
project_lane: otclient
lane: track-a-runtime-governance
track_id: official-client-re
task_kind: implementation
phase: implement-validate
branch: feat/OTC-20260815-track-a-live-runtime-lease-manager
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/feat/OTC-20260815-track-a-live-runtime-lease-manager
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: null
created: 2026-08-15T22:04:00+02:00
updated: 2026-08-15T22:04:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-live-runtime-lease-manager.md
  - docs/agents/evidence/OTC-20260815-track-a-live-runtime-lease-manager/**
  - .github/scripts/tibia-official-client-re-canonical-live-lease.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_lease.py
  - .github/workflows/tibia-official-client-re-canonical-live-lease.yml
modules_touched: []
reuses:
  - docs/agents/TIBIA_RESEARCH_TRACKS.md from PR #311 as pending governance input only
  - repository 45-minute stale-lease convention
depends_on:
  - PR #311 governance decision as pending/unmerged policy input only
  - PR #309 noVNC/display evidence as read-only input only
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: implement an independent task-scoped atomic lease primitive on disjoint paths without mutating active PR #311/#303/#309 owned files
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: low_noise
implementation_authorized: true
invocation_started_at: 2026-08-15T22:04:00+02:00
last_progress_at: 2026-08-15T22:04:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: initial
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Implement a fail-closed authoritative Track A canonical-live controller lease primitive that closes PR #311 review finding `discussion_r3790149828` without touching #311's actively owned governance paths.

The manager must serialize acquire/renew/release/status transitions on the persistent Track A runner state and make stale takeover explicit. It must not launch, stop, signal, log in, attach to or otherwise mutate the official Tibia client.

# Required safety properties

- authoritative state root defaults to `/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime`;
- all lease mutations are serialized by a stable POSIX `flock` coordination file;
- lease state is written atomically and mode `0600`;
- exactly one non-expired controller identity exists at a time;
- renew/release require the current lease token from a mode-`0600` task-local token file;
- stale takeover is allowed only after expiry while holding the coordination lock and increments a generation counter;
- a stale holder's old token cannot renew/release a replacement lease;
- public/status output never reveals the lease token;
- invasive runtime operations remain forbidden unless the caller first validates a current lease; this PR does not implement runtime mutation itself;
- Track B and PR #303/#309 runtime paths/processes remain untouched.

# Validation

- deterministic local unit tests for concurrent acquire, renew, release, stale takeover, stale-token rejection, atomic state and token redaction;
- one task-owned self-hosted workflow execution on `[otclient, synology]` using an isolated temporary state root only; it must not touch the future canonical live state directory or any client process;
- exact-head repository CI terminal before handoff.

# Promotion boundary

This is a Draft implementation slice. It does not make the existing `:98` session canonical and does not authorize canonical live-runtime reuse by itself. PR #311 must still resolve its policy review finding and explicitly keep reuse disabled until a reviewed manager is promoted.

# Next action

Open the Draft PR early, then implement the atomic lease script, tests and isolated self-hosted semantic workflow on the owned paths above.