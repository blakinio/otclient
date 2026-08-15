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
phase: postmerge-review-remediation
branch: fix/OTC-20260815-track-a-live-runtime-lease-postmerge-p1
base_branch: main
base_main: 3575cc0c0a0b4efbcd9fc860d3226002fe40e70f
worktree: github-only://blakinio/otclient/refs/heads/fix/OTC-20260815-track-a-live-runtime-lease-postmerge-p1
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: 313
created: 2026-08-15T22:04:00+02:00
updated: 2026-08-15T23:14:00+02:00
lease_released_at: null
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-live-runtime-lease-manager.md
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
last_progress_at: 2026-08-15T23:14:00+02:00
ci_check_generation: postmerge-p1-remediation
last_verified_code_head: ad30ae9500384aa45bec5307c17c2028cf28c868
semantic_run: 31908781559
semantic_unit_job: 95070594733
semantic_state: success
repository_ci_run: null
repository_ci_required_job: null
repository_ci_state: pending
coordinator_disposition: ACCEPT_WITH_EDITS
coordinator_evidence: docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/canonical-live-lease-manager/20260815-pr312-disposition.md
review_threads: 2
stop_reason: null
next_action: validate PR #313 on its exact final head, remediate any material findings, merge under protection, resolve the two post-merge P1 threads on PR #312, archive this task and release ownership, then revalidate PR #311 against the corrected manager on main
---

# Objective

Keep the authoritative Track A canonical-live controller lease manager safe and promotable after two material post-merge concurrency findings, without claiming or mutating a canonical Tibia runtime.

# Promoted implementation — FACT

PR #312 merged to `main` as commit `3575cc0c0a0b4efbcd9fc860d3226002fe40e70f` after coordinator disposition `ACCEPT_WITH_EDITS` and protected CI. Production entrypoint:

`./.github/scripts/tibia-official-client-re-canonical-live-lease`

Authoritative state:

`/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime`

The merged manager provides serialized `acquire`, `renew`, `validate`, `release`, redacted `status`, and `guard-run`; fixed production state path; task-local token confinement; atomic mode-0600 state; SHA-256 token digest only in shared state; explicit stale takeover reason; generation fencing; and rejection of renew/validate/release by expired holders.

# Post-merge review findings — FACT

Two P1 review findings were posted on merged PR #312 after merge:

1. `guard-run` could release the coordination flock when the guard parent was terminated while its child command continued running.
2. `acquire`, `renew`, `release`, `validate`, `status`, and `guard-run` sampled current time before potentially blocking on the flock, so an already-expired lease could still be accepted after a long wait.

These findings are material. PR #311 therefore remains fail-closed until the corrected manager is on `main` and governance is revalidated.

# Remediation — FACT

PR #313 is the narrow post-merge remediation. It changes only:

- `.github/scripts/tibia-official-client-re-canonical-live-lease.py`;
- `.github/scripts/test_tibia_official_client_re_canonical_live_lease.py`;
- this active task record.

The remediation:

- makes `locked()` yield the live flock descriptor;
- passes that descriptor into the guarded child with `pass_fds`, so killing the guard parent does not release serialization while the child still runs;
- samples current time only after the flock is acquired for every time-sensitive operation;
- adds regression coverage for post-lock expiry across all affected operations and for a killed guard parent with a surviving child.

Focused GitHub-only validation run `31908781559`, job `95070594733`, completed SUCCESS. It ran the full lease unit suite and `py_compile` before committing the remediation. The temporary transformation workflow was removed before PR #313 was opened.

# Historical accepted validation — FACT

Corrected pre-merge semantic code head:

```text
head=e368173086ba8bb1235218b3ec11e046e2c909cb
custom_run=31907695244
unit_job=95067968895 SUCCESS
selfhosted_job=95067968820 SUCCESS
repository_ci=31907697738 SUCCESS
ci_required_job=95068323632 SUCCESS
```

Promotion metadata head:

```text
head=46651d89db2d1a79bf4f66df005b8bcd7267959c
repository_ci=31908198411 SUCCESS
ci_required_job=95069317568 SUCCESS
```

# Safety / non-claims

- No canonical live state directory is created or modified by this remediation.
- No Tibia client process, display `:98`, display `:115`, login/account/session, input, attach, signal, VNC/noVNC, or gameplay state is mutated.
- `:98` is NOT canonicalized.
- This is a cooperative same-UID programme-governance fence, not a hostile-user security boundary.
- PR #303/#309 owned paths and Track B remain untouched.
- No owner-funded Codex/OpenAI API or paid AI quota is used.

# Acceptance inventory

- [x] coordinator disposition `ACCEPT_WITH_EDITS` recorded;
- [x] original stale-release regression repaired and validated before PR #312 merge;
- [x] PR #312 protected merge to `main` verified as `3575cc0c0a0b4efbcd9fc860d3226002fe40e70f`;
- [x] post-merge P1 guard-parent/child-lock finding reproduced by code inspection and repaired in PR #313;
- [x] post-merge P1 pre-lock-time finding repaired for all affected operations in PR #313;
- [x] focused remediation unit/compile validation SUCCESS (`31908781559` / `95070594733`);
- [ ] PR #313 exact-final-head required repository CI SUCCESS;
- [ ] PR #313 independent review has zero unresolved material findings;
- [ ] PR #313 protected merge to `main`;
- [ ] two post-merge P1 review threads on PR #312 resolved after the fix is on `main`;
- [ ] source task archived/terminally closed and ownership released;
- [ ] PR #311 governance revalidated against the corrected manager on `main`.

# Closeout boundary

This task is not complete merely because PR #312 merged. The two post-merge P1 findings reopened implementation. Completion requires PR #313 green/reviewed/merged, the two PR #312 threads resolved, task archival and ownership release. Runtime E2E is NOT_APPLICABLE for this manager implementation because it does not mutate a Tibia runtime; the complete applicable path is deterministic lease CLI/unit/self-hosted behavior plus protected repository CI.
