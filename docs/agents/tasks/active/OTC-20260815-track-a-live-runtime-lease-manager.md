---
task_id: OTC-20260815-track-a-live-runtime-lease-manager
status: implementing
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
worktree: github-only://blakinio/otclient/refs/heads/feat/OTC-20260815-track-a-live-runtime-lease-manager
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: 312
created: 2026-08-15T22:04:00+02:00
updated: 2026-08-15T23:03:00+02:00
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
  - PR #311 must remain fail-closed until this implementation is independently promoted
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
last_progress_at: 2026-08-15T23:03:00+02:00
ci_check_generation: final-release-head
last_verified_code_head: e368173086ba8bb1235218b3ec11e046e2c909cb
semantic_run: 31907695244
semantic_unit_job: 95067968895
semantic_selfhosted_job: 95067968820
semantic_state: success
repository_ci_run: 31907697738
repository_ci_required_job: 95068323632
repository_ci_state: success
promotion_metadata_head: 46651d89db2d1a79bf4f66df005b8bcd7267959c
promotion_metadata_ci_run: 31908198411
promotion_metadata_ci_required_job: 95069317568
promotion_metadata_ci_state: success
coordinator_disposition: ACCEPT_WITH_EDITS
coordinator_evidence: docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/canonical-live-lease-manager/20260815-pr312-disposition.md
delegated_paths:
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
review_threads: 0
stop_reason: null
---

# Objective

Promote the coordinator-accepted canonical-live controller lease manager with required reusable-tool discovery metadata, without claiming or mutating a canonical Tibia runtime.

# Coordinator disposition — FACT

Coordinator PR #300 independently re-reviewed the corrected implementation and assigned `ACCEPT_WITH_EDITS`. The prior material stale-release bypass was repaired on code head `e368173086ba8bb1235218b3ec11e046e2c909cb` and validated by custom run `31907695244` plus repository CI `31907697738`, both SUCCESS.

Coordinator delegated only `docs/agents/MODULE_CATALOG.md` and `docs/agents/CHANGELOG.md` to this source promotion slice. Both bounded discovery edits are now present; the changelog diff was rechecked after an intermediate rewrite error and final diff preserves all historical content plus exactly one new Track A entry.

# Accepted implementation FACT

Production entrypoint:

`./.github/scripts/tibia-official-client-re-canonical-live-lease`

Authoritative state:

`/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime`

The manager provides serialized `acquire`, `renew`, `validate`, `release`, redacted `status`, and lock-held `guard-run`; fixed production state path; task-local token confinement; atomic mode-0600 state; SHA-256 token digest only in shared state; explicit stale takeover reason; generation fencing; and rejection of renew/validate/release by expired holders.

# Exact validation — FACT

Corrected semantic code head:

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

Final task-only release commit is intentionally the remaining protected merge gate; it changes no runtime code or discovery metadata.

# Safety / non-claims

- No canonical live state directory was created or modified by validation.
- No Tibia client process, display `:98`, display `:115`, login/account/session, input, attach, signal, VNC/noVNC, or gameplay state is mutated by this PR.
- `:98` is NOT canonicalized by this PR.
- This is a cooperative same-UID programme-governance fence, not a hostile-user security boundary.
- PR #311 remains fail-closed until this manager is actually on `main` and its policy/review is reconciled.

# Acceptance inventory

- [x] coordinator disposition `ACCEPT_WITH_EDITS` recorded;
- [x] corrected semantic code and stale-release regression validated;
- [x] `MODULE_CATALOG.md` / `CHANGELOG.md` ownership delegated from #300;
- [x] bounded catalogue entry added and patch reviewed;
- [x] bounded changelog entry added; accidental intermediate rewrite repaired and patch reviewed;
- [x] promotion metadata head `CI / Required` SUCCESS;
- [x] review threads zero at promotion review;
- [ ] final task-only release head custom validation terminal SUCCESS;
- [ ] final task-only release head repository `CI / Required` terminal SUCCESS;
- [ ] protected merge #312 to `main`;
- [ ] source task archived in post-merge governance cleanup.

# Next action

Do not edit the source again. Observe only the final task-release head custom validation and repository `CI / Required`; if both are SUCCESS and the PR remains mergeable with no new material review findings, perform the protected merge. Then return to PR #311 governance reconciliation without declaring `:98` canonical.

# Post-merge P1 review remediation

A post-merge review on PR #312 identified two material P1 concurrency defects on merged commit `3575cc0c0a0b4efbcd9fc860d3226002fe40e70f`: guard children could outlive the lock holder, and time-sensitive operations sampled time before blocking on the flock. This continuation repairs both without touching Tibia runtime state, PR #303/#309 paths, Track B, or the production canonical state. PR #311 must remain fail-closed until this remediation is merged and revalidated.
