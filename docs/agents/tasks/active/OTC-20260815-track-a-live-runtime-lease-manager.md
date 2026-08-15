---
task_id: OTC-20260815-track-a-live-runtime-lease-manager
status: validating
agent: ChatGPT
session_id: chatgpt-lease-normal-exit-20260815-2350
session_role: postmerge-remediation
session_rotation_count: 4
project_lane: otclient
lane: track-a-runtime-governance
track_id: official-client-re
task_kind: implementation
phase: normal-launcher-exit-flock-remediation
branch: fix/OTC-20260815-track-a-live-runtime-lease-normal-exit
base_branch: main
base_main: f6fa2264904c6ffb3734d4a63e1edbb29260fcc1
worktree: github-only://blakinio/otclient/refs/heads/fix/OTC-20260815-track-a-live-runtime-lease-normal-exit
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: null
created: 2026-08-15T22:04:00+02:00
updated: 2026-08-15T23:50:00+02:00
lease_released_at: null
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-live-runtime-lease-manager.md
  - docs/agents/tasks/archive/OTC-20260815-track-a-live-runtime-lease-manager.md
  - docs/agents/evidence/OTC-20260815-track-a-live-runtime-lease-manager/**
  - .github/scripts/tibia-official-client-re-canonical-live-lease
  - .github/scripts/tibia-official-client-re-canonical-live-lease.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_lease.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_lease_selfhosted.sh
  - .github/workflows/tibia-official-client-re-canonical-live-lease.yml
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
modules_touched:
  - track-a-runtime-governance
reuses:
  - PR #312 initial manager promotion
  - PR #313 post-lock-time and killed-parent child-lock remediation
depends_on:
  - PR #311 must remain fail-closed until this remediation is merged and governance is revalidated
  - PR #309 noVNC/display evidence is read-only input only
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: low_noise
implementation_authorized: true
last_progress_at: 2026-08-15T23:50:00+02:00
ci_check_generation: normal-launcher-exit-lock-retention
last_verified_code_head: d3e71de0d3b58e13cd14e823762ea8c236a5948c
semantic_run: null
semantic_unit_job: null
semantic_selfhosted_job: null
semantic_state: pending
repository_ci_run: null
repository_ci_required_job: null
repository_ci_state: pending
review_threads: 0
stop_reason: null
next_action: run deterministic unit and isolated Synology validation for the normal-launcher-exit lock-retention regression, then protected-review/merge the narrow remediation before allowing PR #311 to proceed
---

# Objective

Close the remaining canonical-live lease serialization defect: a `guard-run` launcher that exits normally after forking/backgrounding a mutation child must not release the coordination flock while that child remains alive.

# Promoted baseline — FACT

PR #312 merged the canonical-live lease manager. PR #313 merged two concurrency corrections: time-sensitive operations sample time after acquiring the flock, and a guarded child inherits the flock descriptor when the guard parent is killed.

# New post-merge P1 finding — FACT

Final review on PR #311 reproduced a distinct normal-return path:

```text
guard-run -- bash -c 'sleep 8 &'
```

The immediate launcher exits normally. Although the descendant inherited the same open file description, `LeaseManager.locked()` explicitly called `LOCK_UN` in its `finally` block. On Linux `flock` is associated with the open file description, so that explicit unlock released the shared flock even while the background descendant remained alive. A second nonblocking flock could then succeed, allowing a stale takeover to overlap the surviving mutation after expiry.

This is separate from the PR #313 killed-parent regression and keeps PR #311 fail-closed.

# Remediation

The narrow fix removes explicit `LOCK_UN` from the generic `locked()` context manager and closes only the manager's descriptor copy. Ordinary operations still release the lock when their final descriptor closes. For `guard-run`, descendants inherit the open file description; therefore the lock remains held until the last surviving mutation descendant closes its inherited descriptor.

A deterministic regression test forks a background child, lets the immediate launcher exit normally, proves a second nonblocking flock is denied while the child remains alive, and proves the flock becomes acquirable after the child exits.

# Safety / non-claims

- No production canonical-live state is used by tests.
- No Tibia process, login/session, display, VNC/noVNC, input or instrumentation is mutated.
- `:98` remains NOT_PROVEN/NOT_REGISTERED as canonical.
- PR #303 runtime paths/processes and Track B remain untouched.
- No owner-funded Codex/OpenAI API or paid AI quota is authorized or used.

# Acceptance inventory

- [x] normal-launcher-return unlock root cause identified;
- [x] explicit `LOCK_UN` removed from production lock context;
- [x] normal-return surviving-child regression added;
- [ ] deterministic unit suite SUCCESS on exact remediation head;
- [ ] isolated Synology validation SUCCESS without production canonical-state use;
- [ ] repository `CI / Required` SUCCESS on exact final head;
- [ ] zero unresolved material review findings;
- [ ] protected merge to `main`;
- [ ] PR #311 review finding resolved only after this fix reaches `main`;
- [ ] manager task archived/terminally closed after all post-merge findings are resolved.
