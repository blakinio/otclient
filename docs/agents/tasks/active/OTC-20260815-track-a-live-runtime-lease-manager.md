---
task_id: OTC-20260815-track-a-live-runtime-lease-manager
status: ready
agent: unassigned
session_id: null
session_role: implementation-worker
session_rotation_count: 1
project_lane: otclient
lane: track-a-runtime-governance
track_id: official-client-re
task_kind: implementation
phase: corrected-handoff
branch: feat/OTC-20260815-track-a-live-runtime-lease-manager
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/feat/OTC-20260815-track-a-live-runtime-lease-manager
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: 312
created: 2026-08-15T22:04:00+02:00
updated: 2026-08-15T22:52:00+02:00
lease_released_at: 2026-08-15T22:52:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-live-runtime-lease-manager.md
  - docs/agents/evidence/OTC-20260815-track-a-live-runtime-lease-manager/**
  - .github/scripts/tibia-official-client-re-canonical-live-lease
  - .github/scripts/tibia-official-client-re-canonical-live-lease.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_lease.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_lease_selfhosted.sh
  - .github/workflows/tibia-official-client-re-canonical-live-lease.yml
modules_touched:
  - track-a-runtime-governance
reuses:
  - PR #311 canonical-live governance decision as pending policy input only
  - repository 45-minute stale-lease convention
depends_on:
  - PR #311 must remain fail-closed until this implementation is independently promoted
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
last_progress_at: 2026-08-15T22:52:00+02:00
ci_check_generation: corrected-expired-release-handoff
last_verified_code_head: e368173086ba8bb1235218b3ec11e046e2c909cb
semantic_run: 31907695244
semantic_unit_job: 95067968895
semantic_selfhosted_job: 95067968820
semantic_state: success
repository_ci_run: 31907697738
repository_ci_required_job: 95068323632
repository_ci_state: success
review_threads: 0
stop_reason: corrected reviewable Draft handoff; promotion authority belongs to coordinator
review_finding:
  source: coordinator_review_20260815_2243
  severity: material
  original_classification: RETURN_FOR_EVIDENCE
  issue: expired holder could release stale generation and bypass explicit stale-takeover reason path
  repaired: true
  repair_head: e368173086ba8bb1235218b3ec11e046e2c909cb
---

# Objective

Close PR #311 review finding `discussion_r3790149828` with an enforceable, fail-closed controller lease for a future canonical Track A live Tibia runtime, without touching active #311/#303/#309 runtime-owned paths or processes.

# Coordinator review correction — FACT

Independent source inspection found a material stale-fencing gap in the first handoff: `LeaseManager.release()` checked status, identity and token but did not reject an expired lease. An expired holder could therefore release its stale generation and reacquire normally, bypassing the required explicit stale-takeover reason/audit path.

Corrected head `e368173086ba8bb1235218b3ec11e046e2c909cb` fixes that bounded defect:

- `release` on `expires_at <= now` fails with `lease_expired`;
- the expired active record remains intact;
- acquisition after expiry without a reason fails with `stale_takeover_reason_required`;
- explicit stale takeover increments generation and fences old credentials.

# Implemented FACT

Production entrypoint:

`./.github/scripts/tibia-official-client-re-canonical-live-lease`

The production entrypoint fixes authoritative state to:

`/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime`

and rejects caller state overrides. Controller token paths are canonicalized and must remain under the claiming task's persistent state directory.

The internal Python implementation provides serialized `acquire`, `renew`, `validate`, `release`, redacted `status`, and `guard-run` transitions. A stable POSIX `flock` serializes all lease state operations; `guard-run` keeps that lock for the guarded command. State writes are atomic and mode `0600`. Shared state contains only a SHA-256 token digest; the random capability token remains in a mode-`0600` task-local file.

# Corrected exact validation — FACT

Corrected code-bearing head `e368173086ba8bb1235218b3ec11e046e2c909cb`:

- custom workflow run `31907695244`: SUCCESS;
- unit job `95067968895`: SUCCESS;
- Synology self-hosted job `95067968820`: SUCCESS on `synology-otclient-01`;
- repository CI `31907697738`: SUCCESS;
- required job `95068323632` (`CI / Required`): SUCCESS.

The Synology proof emitted:

```text
TRACK_A_CANONICAL_LEASE_ENTRYPOINT_FENCED=true
TRACK_A_CANONICAL_LEASE_TOKEN_PATH_TRAVERSAL_REJECTED=true
TRACK_A_CANONICAL_LEASE_EXPIRED_RELEASE_REJECTED=true
TRACK_A_CANONICAL_LEASE_STALE_TAKEOVER_REASON_REQUIRED=true
TRACK_A_CANONICAL_LEASE_CONCURRENT_SERIALIZATION_PROVEN=true
TRACK_A_CANONICAL_LEASE_SELFTEST_COMPLETE=true
TRACK_A_CANONICAL_LEASE_CANONICAL_STATE_UNTOUCHED=true
```

# Safety / non-claims

- No canonical live state directory was created or modified by validation.
- No Tibia client process, display `:98`, display `:115`, login state, account state, socket, VNC/noVNC configuration, input, attach, signal, or gameplay state was mutated.
- `:98` remains only the strongest historical/persistent display candidate; this task does not register it as canonical.
- This is cooperative same-UID governance fencing, not a hostile-user security boundary.
- Stale takeover grants lease authority only; runtime provenance/state still must be revalidated before mutation.
- PR #311 remains Draft and its authoritative-lock review finding must stay unresolved until this implementation is independently accepted/promoted and the governance text requires it.
- Shared `MODULE_CATALOG.md` / `CHANGELOG.md` integration is deferred to the promotion coordinator because those paths are part of the coordinator integration scope.

# Acceptance inventory

- [x] stable authoritative production state path;
- [x] atomic serialized acquire/renew/release/status transitions;
- [x] explicit stale takeover with generation fencing;
- [x] private token and redacted shared/status state;
- [x] task-token path confinement and traversal rejection;
- [x] guarded invasive-operation primitive holding the coordination lock;
- [x] expired holder cannot release stale generation;
- [x] regression proves explicit stale takeover remains the only post-expiry ownership transition;
- [x] corrected exact-head unit + Synology custom validation green;
- [x] corrected exact-head repository CI including `CI / Required` green;
- [x] Draft ownership released again for coordinator re-review.

# Next action

Coordinator PR #300 should independently re-review corrected PR #312 and assign a disposition. If accepted, coordinate the reusable-tool `MODULE_CATALOG.md` / `CHANGELOG.md` integration and promote the manager to `main`. Only then may PR #311 resolve its review finding and proceed through exact-head governance CI/merge. Do not make `:98` canonical until a separate read-only provenance/state registration proves the intended runtime identity.
