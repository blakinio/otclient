---
task_id: OTC-20260815-track-a-live-runtime-lease-manager
status: validating
agent: ChatGPT
session_id: automation-track-a-canonical-runtime-20260816-0112
session_role: replacement-integrator
session_rotation_count: 5
project_lane: otclient
lane: track-a-runtime-governance
track_id: official-client-re
task_kind: implementation
phase: integrate
branch: fix/OTC-20260815-track-a-live-runtime-lease-supervisor-p1
base_branch: main
base_main: b433290f48e18270279895ff4abb1a54b4475051
worktree: github-only://blakinio/otclient/refs/heads/fix/OTC-20260815-track-a-live-runtime-lease-supervisor-p1
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: 316
created: 2026-08-15T22:04:00+02:00
updated: 2026-08-16T01:12:00+02:00
lease_expires_at: 2026-08-16T01:57:00+02:00
lease_released_at: null
stale_takeover_count: 1
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-live-runtime-lease-manager.md
  - docs/agents/tasks/archive/OTC-20260815-track-a-live-runtime-lease-manager.md
  - docs/agents/evidence/OTC-20260815-track-a-live-runtime-lease-manager/**
  - .github/scripts/tibia-official-client-re-canonical-live-lease
  - .github/scripts/tibia-official-client-re-canonical-live-lease.py
  - .github/scripts/tibia-official-client-re-canonical-live-guard.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_lease.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_guard.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_lease_selfhosted.sh
  - .github/workflows/tibia-official-client-re-canonical-live-lease.yml
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
modules_touched:
  - track-a-runtime-governance
reuses:
  - PR #311 canonical-live governance decision as pending policy input only
  - repository 45-minute stale-lease convention
  - PR #317 normal-launcher last-close remediation merged as b433290f48e18270279895ff4abb1a54b4475051
depends_on:
  - PR #311 remains fail-closed until final lease-manager remediation is on main and governance is revalidated
  - PR #309 noVNC/display evidence is read-only input only
  - PR #315 canonical-runtime registration is disjoint read-only research only
  - coordinator PR #300 disposition ACCEPT_WITH_EDITS
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: connector-native clean restack, exact-head CI/review and protected merge are sufficient; no runtime mutation is authorized
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: low_noise
implementation_authorized: true
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: phased
decomposition_reason: one sequential governance chain with shared manager state and ordered PR dependencies
last_progress_at: 2026-08-16T01:12:00+02:00
ci_check_generation: postmerge-supervisor-p1-restack
semantic_run: 31910612285
semantic_unit_job: 95074977275
semantic_selfhosted_job: 95074977279
semantic_state: historical-success-pre-restack
audit_run: 31910612285
audit_job: 95074977302
audit_state: historical-pass-pre-restack
audit_evidence: docs/agents/evidence/OTC-20260815-track-a-live-runtime-lease-manager/20260815-independent-final-audit.md
repository_ci_run: null
repository_ci_required_job: null
repository_ci_state: pending-restack
coordinator_disposition: ACCEPT_WITH_EDITS
coordinator_evidence: docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/canonical-live-lease-manager/20260815-pr312-disposition.md
remediation_evidence: docs/agents/evidence/OTC-20260815-track-a-live-runtime-lease-manager/20260815-supervisor-p1-remediation.md
review_threads: 0
stop_reason: null
next_action: clean-restack PR #316 on main@b433290f48e18270279895ff4abb1a54b4475051, preserve PR #317 last-close semantics and PR #316 out-of-band subreaper semantics, fix workflow SC2016, then rerun deterministic unit + isolated Synology + fresh independent audit + exact-head repository CI
---

# Objective

Keep the authoritative Track A canonical-live controller lease manager fail-closed and serial across controller processes and guarded mutation descendants, without claiming or mutating any canonical Tibia runtime.

# Replacement-session takeover — FACT

At 2026-08-16T01:12:00+02:00 the durable manager task had not checkpointed since 2026-08-15T23:54:00+02:00, exceeding the repository `stale_after_minutes: 45` threshold. Live GitHub state showed PR #316 still at exact head `883035cc0f240812442b960a063ae2a900c548a6`, while the previous manager branch PR #317 had already merged and closed as `main@b433290f48e18270279895ff4abb1a54b4475051`. No newer PR #316 branch write or fresh task checkpoint existed. This replacement session therefore took over from the last coherent commit under `EXECUTION_PROTOCOL.md`, incremented the session rotation/takeover counters, and renewed the advisory lease before further writes.

# Final remediation boundary — FACT

PR #312 introduced the authoritative manager and merged as `3575cc0c0a0b4efbcd9fc860d3226002fe40e70f`. PR #313 repaired post-lock time sampling but its inherited-flock-FD design remained vulnerable to a normal guarded command closing unknown descriptors while daemonizing.

PR #317 then merged the lower-level last-close correction on normal launcher return: `LeaseManager.locked()` no longer explicitly issues `LOCK_UN`, so inherited open-file-description users cannot be invalidated by the manager copy closing.

PR #316 provides the stronger production `guard-run` boundary and must be clean-restacked on that current main rather than promoted from its stale pre-#317 base:

1. acquire flock and validate the current lease before any detached process exists;
2. fork a dedicated supervisor only after validation;
3. supervisor alone retains the flock while the caller closes its copy;
4. guarded command receives no flock descriptor (`close_fds=True`);
5. supervisor becomes `PR_SET_CHILD_SUBREAPER`;
6. supervisor waits for the primary command and all orphaned descendants before releasing the flock;
7. caller death after dispatch cannot release serialization;
8. cancellation while waiting for the initial flock cannot detach a future mutation.

# Historical validation — FACT

Pre-restack post-review semantic/audit run:

```text
run=31910612285 SUCCESS
unit=95074977275 SUCCESS
isolated_synology=95074977279 SUCCESS
fresh_independent_audit=95074977302 SUCCESS
```

The adversarial regression combines caller kill, explicit closure of inherited FDs, and fork/`setsid()` daemonization. The independent flock remains unavailable while the daemon survives and becomes available only after the supervisor has reaped the full descendant tree.

Automatic PR review identified one additional P1 safety flaw in the test cleanup: signalling the saved daemon PID after successful reap could hit a reused PID on the shared runner. Commit `024a71f929e331af26b6edc9d03aee3697b412e6` removed that signal path. All semantic, Synology and independent-audit gates were rerun after the repair and passed; the review thread was resolved.

The old exact-head repository CI run `31910752406` failed only actionlint/shellcheck SC2016 in `.github/workflows/tibia-official-client-re-canonical-live-lease.yml`; the root cause must be fixed on the clean-restacked final head rather than rerunning unchanged CI.

Durable evidence:

- `docs/agents/evidence/OTC-20260815-track-a-live-runtime-lease-manager/20260815-supervisor-p1-remediation.md`
- `docs/agents/evidence/OTC-20260815-track-a-live-runtime-lease-manager/20260815-independent-final-audit.md`

# Safety / non-claims

- Production canonical-live state is not created or mutated by validation.
- No Tibia client/login/session/display/input/ptrace/signal/VNC state is touched.
- `:98`, `6082`, PID and session canonical status remain UNKNOWN/NOT_REGISTERED without direct evidence.
- PR #303 runtime paths/processes and Track B remain untouched.
- PR #315 remains disjoint read-only registration research.
- No owner-funded Codex/OpenAI API or paid AI quota is authorized or used by this task.

# Acceptance inventory

- [x] PR #312 manager promoted to main.
- [x] expired-holder stale-release bypass repaired before PR #312 promotion.
- [x] post-lock-time sampling P1 repaired in PR #313.
- [x] inherited-FD/daemonization weakness independently identified after PR #313.
- [x] PR #317 lower-level normal-launcher last-close remediation merged to current main.
- [x] stale manager session replaced under repository takeover protocol before further mutation.
- [ ] PR #316 clean-restacked on current main preserving both #317 last-close and #316 supervisor semantics.
- [ ] SC2016 root cause repaired on final PR #316 head.
- [ ] deterministic unit validation PASS on final combined head.
- [ ] isolated Synology validation PASS on final combined head with canonical state untouched.
- [ ] fresh independent audit PASS on final combined head.
- [ ] PR #316 repository `CI / Required` PASS on exact final head.
- [ ] PR #316 unresolved review threads = 0 on final combined head.
- [ ] PR #316 protected merge to `main`.
- [ ] fresh post-merge manager closeout produced from final corrected main and archived; stale #314 evidence not reused.
- [ ] PR #318 bootstrap contract reconciled/validated against final manager/supervisor and merged only if clean.
- [ ] PR #311 clean-restacked on final main, exact-head CI/review green, protected-merged, task archived and ownership released.

# E2E

Result: `NOT_APPLICABLE`.

Reason: the manager is infrastructure/governance and must not mutate a Tibia runtime during validation. The complete applicable path is lease CLI/production routing -> serialized processing -> isolated state/descendant lifetime -> observable result, proven by deterministic tests, isolated Synology validation and fresh audit.
