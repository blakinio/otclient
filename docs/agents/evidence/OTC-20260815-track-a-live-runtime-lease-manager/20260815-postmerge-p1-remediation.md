# Canonical live lease manager — post-merge P1 remediation

Task: `OTC-20260815-track-a-live-runtime-lease-manager`  
Source merge: PR #312 / `main@3575cc0c0a0b4efbcd9fc860d3226002fe40e70f`  
Remediation: PR #313 / `fix/OTC-20260815-track-a-live-runtime-lease-postmerge-p1`

## Material findings

Two P1 review threads were posted on merged PR #312 after merge:

- `PRRT_kwDOTVmdjs6Zizo2`: a `guard-run` parent could die while its child continued; Python would unwind the context and release the flock, so a second controller could proceed while the first guarded mutation still ran.
- `PRRT_kwDOTVmdjs6Zizo4`: time-sensitive operations sampled the clock before potentially blocking on the flock, so a lease that expired during the wait could still be accepted using stale pre-lock time.

Both findings are material to the manager's single-controller guarantee. PR #311 therefore remains fail-closed until this remediation reaches `main` and governance is revalidated.

## Remediation

`LeaseManager.locked()` now yields the live coordination lock file descriptor.

`guard_run()` passes that descriptor to the guarded command with `pass_fds=(lock_fd,)`. The child therefore retains the same `flock` open file description if the guard parent terminates, so serialization persists until the guarded child exits or closes the inherited descriptor.

`acquire`, `renew`, `release`, `validate`, `status`, and `guard_run` now call `_now_epoch()` only after entering the serialized lock. Expiry decisions therefore use time observed after lock acquisition rather than before any blocking wait.

## Regression coverage

The unit suite adds:

- `test_all_time_sensitive_operations_recheck_time_after_lock_acquisition` — advances mocked time only after the lock is acquired and proves expired `renew`, `release`, `validate`, and `guard-run` fail; `status` reports expired; `acquire` requires explicit stale-takeover reason.
- `test_guard_child_inherits_lock_if_guard_parent_is_killed` — kills the guard parent while its child remains alive and proves a nonblocking second flock cannot be acquired until the child exits.

## Validation

Focused transformation/test run:

```text
run=31908781559
job=95070594733
result=SUCCESS
```

This run applied the bounded remediation on the isolated branch, ran the full lease unit suite, ran `py_compile`, committed the fix, and did not touch production canonical state.

Independent branch validation:

```text
run=31908930698
head=2d548c67c0b0d9e39c5d8a51cd72fd1bba878d9a
unit_job=95070957976 SUCCESS
isolated_selfhosted_job=95070958055 SUCCESS
run_result=SUCCESS
```

The self-hosted job used the existing task-owned self-test root and preserves `TRACK_A_CANONICAL_LEASE_CANONICAL_STATE_UNTOUCHED=true`; it does not create or mutate `/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime`.

The temporary validation workflow was deleted before the final PR diff. PR #313 final changed paths remain limited to manager code, regression tests, task/evidence state.

## Safety / non-claims

- No Tibia client process, login, input, attach, signal, display, VNC/noVNC endpoint, or gameplay state was mutated.
- `:98` is not registered or claimed canonical.
- PR #303 and #309 owned paths/processes remain untouched.
- Track B remains untouched.
- No owner-funded Codex/OpenAI API or paid AI quota was invoked by this remediation.

## Remaining closeout gate

PR #313 must still pass required repository CI on its exact final head, have zero unresolved material review findings, and merge under repository protection. Only after that merge may the two post-merge PR #312 threads be resolved and the manager task archived/released. PR #311 governance reconciliation follows afterward.
