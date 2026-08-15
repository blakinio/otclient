---
task_id: OTC-20260815-track-a-live-runtime-lease-manager
status: active
agent: ChatGPT
session_id: chatgpt-live-runtime-lease-manager-repair-20260815-2243
session_role: implementation-worker
session_rotation_count: 1
project_lane: otclient
lane: track-a-runtime-governance
track_id: official-client-re
task_kind: implementation
phase: repair-after-coordinator-review
branch: feat/OTC-20260815-track-a-live-runtime-lease-manager
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/feat/OTC-20260815-track-a-live-runtime-lease-manager
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: 312
created: 2026-08-15T22:04:00+02:00
updated: 2026-08-15T22:43:00+02:00
lease_released_at: null
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
last_progress_at: 2026-08-15T22:43:00+02:00
ci_check_generation: expired-release-fencing-repair
last_verified_code_head: b52c464c6f9c1ffc2f22da70fc1c05550904d73f
semantic_run: 31906213909
semantic_unit_job: 95064329724
semantic_selfhosted_job: 95064329739
semantic_state: superseded_by_review_finding
repository_ci_run: 31906215762
repository_ci_required_job: 95064610764
repository_ci_state: superseded_by_review_finding
review_threads: 0
stop_reason: null
review_finding:
  source: coordinator_review_20260815_2243
  severity: material
  classification: RETURN_FOR_EVIDENCE
  issue: expired holder can release stale generation and bypass explicit stale-takeover reason path
---

# Objective

Close PR #311 review finding `discussion_r3790149828` with an enforceable, fail-closed controller lease for a future canonical Track A live Tibia runtime, without touching active #311/#303/#309 runtime-owned paths or processes.

# Coordinator review correction

Independent source inspection found a material stale-fencing gap in the prior handoff: `LeaseManager.release()` checked status, identity and token but did not reject an expired lease. An expired holder could therefore release its stale generation and immediately acquire again as a normal post-release generation, bypassing the required explicit stale-takeover reason/audit path.

This rotation must repair only that bounded defect:

- `release` on `expires_at <= now` must fail closed with `lease_expired`;
- the expired active record must remain intact until explicit stale takeover;
- deterministic unit coverage must prove expired release rejection and subsequent takeover reason/generation fencing;
- Synology self-hosted validation must emit an explicit marker for expired-release rejection while using task-owned temporary state only;
- all previous entrypoint/path/concurrency/non-mutation fences remain unchanged.

# Implemented FACT from prior handoff

Production entrypoint:

`./.github/scripts/tibia-official-client-re-canonical-live-lease`

The production entrypoint fixes authoritative state to:

`/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime`

and rejects caller state overrides. Controller token paths are canonicalized and must remain under the claiming task's persistent state directory.

The internal Python implementation provides serialized `acquire`, `renew`, `validate`, `release`, redacted `status`, and `guard-run` transitions. A stable POSIX `flock` serializes all lease state operations; `guard-run` keeps that lock for the guarded command. State writes are atomic and mode `0600`. Shared state contains only a SHA-256 token digest; the random capability token remains in a mode-`0600` task-local file.

Expired takeover requires an explicit reason and increments a generation. A previous generation token cannot renew, validate, or release the replacement lease.

# Safety / non-claims

- No canonical live state directory may be created or modified by validation.
- No Tibia client process, display `:98`, display `:115`, login state, account state, socket, VNC/noVNC configuration, input, attach, signal, or gameplay state may be mutated.
- `:98` remains only the strongest historical/persistent display candidate; this task does not register it as canonical.
- This is cooperative same-UID governance fencing, not a hostile-user security boundary.
- Stale takeover grants lease authority only; runtime provenance/state still must be revalidated before mutation.
- PR #311 remains Draft and its authoritative-lock review finding must stay unresolved until this implementation is independently accepted/promoted and the governance text requires it.
- Shared `MODULE_CATALOG.md` / `CHANGELOG.md` integration remains deferred to the promotion coordinator.

# Acceptance inventory

- [x] stable authoritative production state path;
- [x] atomic serialized acquire/renew/release/status transitions;
- [x] explicit stale takeover with generation fencing;
- [x] private token and redacted shared/status state;
- [x] task-token path confinement and traversal rejection;
- [x] guarded invasive-operation primitive holding the coordination lock;
- [ ] expired holder cannot release stale generation;
- [ ] regression proves explicit stale takeover remains the only post-expiry ownership transition;
- [ ] corrected exact-head unit + Synology custom validation green;
- [ ] corrected exact-head repository CI including `CI / Required` green;
- [ ] Draft ownership released again for coordinator re-review.

# Next action

Patch expired-release fencing and its unit/self-hosted regression only, then execute exact-head custom validation and repository CI before releasing the Draft for coordinator re-review.
