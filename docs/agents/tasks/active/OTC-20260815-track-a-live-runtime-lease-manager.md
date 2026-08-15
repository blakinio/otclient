---
task_id: OTC-20260815-track-a-live-runtime-lease-manager
status: active
agent: ChatGPT
session_id: chatgpt-live-runtime-lease-promotion-20260815-2257
session_role: promotion-worker
session_rotation_count: 2
project_lane: otclient
lane: track-a-runtime-governance
track_id: official-client-re
task_kind: implementation
phase: coordinator-accepted-promotion-edits
branch: feat/OTC-20260815-track-a-live-runtime-lease-manager
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/feat/OTC-20260815-track-a-live-runtime-lease-manager
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: 312
created: 2026-08-15T22:04:00+02:00
updated: 2026-08-15T22:57:00+02:00
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
last_progress_at: 2026-08-15T22:57:00+02:00
ci_check_generation: promotion-discovery-metadata
last_verified_code_head: e368173086ba8bb1235218b3ec11e046e2c909cb
semantic_run: 31907695244
semantic_unit_job: 95067968895
semantic_selfhosted_job: 95067968820
semantic_state: success
repository_ci_run: 31907697738
repository_ci_required_job: 95068323632
repository_ci_state: success
coordinator_disposition: ACCEPT_WITH_EDITS
coordinator_evidence: docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/canonical-live-lease-manager/20260815-pr312-disposition.md
delegated_paths:
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
review_threads: 0
stop_reason: null
---

# Objective

Promote the coordinator-accepted canonical-live controller lease manager by adding only the required same-PR reusable-tool discovery metadata, then pass final exact-head validation and protected merge.

# Coordinator disposition — FACT

Coordinator PR #300 independently re-reviewed the corrected implementation and assigned `ACCEPT_WITH_EDITS`. The prior material stale-release bypass was repaired on code head `e368173086ba8bb1235218b3ec11e046e2c909cb` and validated by custom run `31907695244` plus repository CI `31907697738`, both SUCCESS.

The only required promotion edits are bounded entries to `docs/agents/MODULE_CATALOG.md` and `docs/agents/CHANGELOG.md`. Coordinator #300 explicitly removed those paths from its active ownership and delegated them to this PR before releasing its lease. No other #300 path is owned here.

# Accepted implementation FACT

Production entrypoint:

`./.github/scripts/tibia-official-client-re-canonical-live-lease`

Authoritative state:

`/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime`

The manager provides serialized `acquire`, `renew`, `validate`, `release`, redacted `status`, and lock-held `guard-run`; fixed production state path; task-local token confinement; atomic mode-0600 state; SHA-256 token digest only in shared state; explicit stale takeover reason; generation fencing; and rejection of renew/validate/release by expired holders.

# Safety / non-claims

- No canonical live state directory was created or modified by validation.
- No Tibia client process, display `:98`, display `:115`, login/account/session, input, attach, signal, VNC/noVNC, or gameplay state is mutated by this promotion edit.
- `:98` is NOT canonicalized by this PR.
- This is a cooperative same-UID programme-governance fence, not a hostile-user security boundary.
- PR #311 remains fail-closed until this manager is actually on `main` and its policy/review is reconciled.

# Acceptance inventory

- [x] coordinator disposition `ACCEPT_WITH_EDITS` recorded;
- [x] corrected semantic code and stale-release regression validated;
- [x] `MODULE_CATALOG.md` / `CHANGELOG.md` ownership delegated from #300;
- [ ] add bounded catalogue entry;
- [ ] add bounded changelog entry;
- [ ] final exact-head custom validation SUCCESS;
- [ ] final exact-head repository `CI / Required` SUCCESS;
- [ ] review threads zero/material findings resolved for #312;
- [ ] protected merge #312 to `main`;
- [ ] source task archived/released after merge.

# Next action

Add only the delegated discovery metadata, then require final exact-head custom validation and repository CI before protected merge. After #312 reaches `main`, return to PR #311 governance reconciliation; do not register `:98` canonical in this PR.
