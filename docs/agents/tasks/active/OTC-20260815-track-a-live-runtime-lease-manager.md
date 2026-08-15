---
task_id: OTC-20260815-track-a-live-runtime-lease-manager
status: validating
agent: ChatGPT
session_id: null
session_role: postmerge-remediation
session_rotation_count: 3
project_lane: otclient
lane: track-a-runtime-governance
track_id: official-client-re
task_kind: implementation
phase: final-ci
branch: fix/OTC-20260815-track-a-live-runtime-lease-postmerge-p1
base_branch: main
base_main: 3575cc0c0a0b4efbcd9fc860d3226002fe40e70f
worktree: github-only://blakinio/otclient/refs/heads/fix/OTC-20260815-track-a-live-runtime-lease-postmerge-p1
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: 313
created: 2026-08-15T22:04:00+02:00
updated: 2026-08-15T23:16:07+02:00
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
  - PR #311 canonical-live governance decision as pending policy input only
  - repository 45-minute stale-lease convention
depends_on:
  - PR #311 must remain fail-closed until this remediation is merged and governance is revalidated
  - PR #309 noVNC/display evidence is read-only input only
  - coordinator PR #300 disposition ACCEPT_WITH_EDITS and explicit delegation of MODULE_CATALOG.md / CHANGELOG.md
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: low_noise
implementation_authorized: true
last_progress_at: 2026-08-15T23:16:07+02:00
ci_check_generation: postmerge-p1-final
last_verified_code_head: ad30ae9500384aa45bec5307c17c2028cf28c868
semantic_run: 31908930698
semantic_unit_job: 95070957976
semantic_selfhosted_job: 95070958055
semantic_state: success
repository_ci_run: null
repository_ci_required_job: null
repository_ci_state: pending
coordinator_disposition: ACCEPT_WITH_EDITS
coordinator_evidence: docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/canonical-live-lease-manager/20260815-pr312-disposition.md
remediation_evidence: docs/agents/evidence/OTC-20260815-track-a-live-runtime-lease-manager/20260815-postmerge-p1-remediation.md
review_threads: 0
stop_reason: null
next_action: run PR #313 required CI and review on the exact final head; if green with zero material findings, merge under protection, resolve the two post-merge P1 threads on PR #312, then archive this task and release ownership before returning to PR #311
---

# Objective

Keep the authoritative Track A canonical-live controller lease manager safe after two material post-merge concurrency findings, without claiming or mutating a canonical Tibia runtime.

# Promoted implementation — FACT

PR #312 merged to `main` as commit `3575cc0c0a0b4efbcd9fc860d3226002fe40e70f` after coordinator disposition `ACCEPT_WITH_EDITS` and protected CI. Production entrypoint:

`./.github/scripts/tibia-official-client-re-canonical-live-lease`

Authoritative state:

`/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime`

The manager provides serialized `acquire`, `renew`, `validate`, `release`, redacted `status`, and `guard-run`; fixed production state path; task-local token confinement; atomic mode-0600 state; SHA-256 token digest only in shared state; explicit stale takeover reason; generation fencing; and rejection of renew/validate/release by expired holders.

# Post-merge P1 findings — FACT

Two material review findings were posted on merged PR #312 after merge:

1. `guard-run` could release the coordination flock when the guard parent terminated while its child command continued running.
2. time-sensitive operations sampled current time before potentially blocking on the flock, so a lease that expired during the wait could still be accepted.

PR #311 remains fail-closed until the corrected manager is on `main` and governance is revalidated.

# Remediation — FACT

PR #313 is the narrow remediation. The code change:

- makes `LeaseManager.locked()` yield the live flock descriptor;
- passes that descriptor into the guarded child with `pass_fds=(lock_fd,)`, preserving serialization when the guard parent dies before its child;
- samples current time only after lock acquisition in `acquire`, `renew`, `release`, `validate`, `status`, and `guard_run`;
- adds regression tests for post-lock expiry and parent-killed/child-survives lock inheritance.

Final implementation scope is limited to the manager implementation, its tests, this task, and its evidence. Temporary GitHub-only validation workflows were removed from the branch before final CI.

# Validation — FACT

Focused patch/test run:

```text
run=31908781559
job=95070594733 SUCCESS
```

Independent branch validation after the remediation:

```text
run=31908930698 SUCCESS
head=2d548c67c0b0d9e39c5d8a51cd72fd1bba878d9a
unit_job=95070957976 SUCCESS
isolated_selfhosted_job=95070958055 SUCCESS
```

The self-hosted validation used only the task-owned self-test root and preserved the existing `CANONICAL_STATE_UNTOUCHED` contract. It did not create or mutate production canonical-live state.

Durable evidence:

`docs/agents/evidence/OTC-20260815-track-a-live-runtime-lease-manager/20260815-postmerge-p1-remediation.md`

# Safety / non-claims

- No canonical live state directory is created or modified by this remediation.
- No Tibia client process, display `:98`, display `:115`, login/account/session, input, attach, signal, VNC/noVNC, or gameplay state is mutated.
- `:98` is NOT canonicalized.
- PR #303/#309 owned paths and Track B remain untouched.
- No owner-funded Codex/OpenAI API or paid AI quota was invoked by this remediation.

# Acceptance inventory

- [x] coordinator disposition `ACCEPT_WITH_EDITS` recorded;
- [x] PR #312 protected merge to `main` verified as `3575cc0c0a0b4efbcd9fc860d3226002fe40e70f`;
- [x] P1 guard-parent/child-lock finding repaired in PR #313;
- [x] P1 pre-lock-time finding repaired for all affected operations in PR #313;
- [x] focused unit/compile validation SUCCESS (`31908781559` / `95070594733`);
- [x] independent branch unit validation SUCCESS (`31908930698` / `95070957976`);
- [x] isolated Synology validation SUCCESS (`31908930698` / `95070958055`);
- [x] PR #313 currently has zero review threads before readiness transition;
- [ ] PR #313 exact-final-head `CI / Required` SUCCESS;
- [ ] PR #313 final review has zero unresolved material findings;
- [ ] PR #313 protected merge to `main`;
- [ ] two post-merge P1 review threads on PR #312 resolved after fix reaches `main`;
- [ ] task archived/terminally closed and ownership released;
- [ ] PR #311 governance revalidated against corrected manager on `main`.

# Closeout boundary

The task is not complete merely because PR #312 merged. The two post-merge P1 findings reopened implementation. Completion requires PR #313 green/reviewed/merged, the two PR #312 threads resolved, task archival and ownership release. Runtime E2E is `NOT_APPLICABLE_WITH_REASON`: this manager does not mutate a Tibia runtime; its complete applicable path is deterministic CLI/unit behavior plus isolated Synology validation and protected repository CI.
