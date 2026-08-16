# Canonical live lease supervisor P1 remediation

Task: `OTC-20260815-track-a-live-runtime-lease-manager`  
Source finding: merged PR #313 review thread `PRRT_kwDOTVmdjs6Zi34b`  
Remediation PR: #316  
Base: `main@f6fa2264904c6ffb3734d4a63e1edbb29260fcc1`

## Finding — FACT

PR #313 preserved the canonical coordination flock by passing its file descriptor into the guarded command. That is insufficient for the documented cooperative runtime contract because a normal daemonizing or security-conscious executable may close unknown inherited file descriptors. If the `guard-run` caller then dies while that command or a daemonized descendant continues mutating, the flock can disappear even though the mutation is still alive.

The finding is material. Canonical-live mutation/reuse remains fail-closed until this remediation reaches `main` and the governance policy is revalidated.

## Remediation — FACT

PR #316 moves lock ownership outside the guarded command:

- the caller opens/acquires the canonical coordination flock and validates the current lease before any detached process exists;
- only after successful validation does the caller fork a dedicated supervisor;
- the supervisor inherits the held flock; the caller closes its own copy without an explicit unlock;
- the guarded command is launched by the supervisor with `close_fds=True`, so it never receives the flock descriptor;
- the supervisor becomes a Linux child subreaper using `PR_SET_CHILD_SUBREAPER`;
- the supervisor waits for the primary command and all orphaned descendants before it closes the flock;
- caller death after dispatch cannot release the supervisor-owned flock;
- cancellation while waiting for the initial flock cannot leave a future detached mutation because the supervisor does not yet exist.

The production shell entrypoint routes only `guard-run` through the new supervisor helper. Existing fixed-state and token-path fencing remains unchanged. Existing post-lock time sampling from PR #313 remains unchanged.

## Regression proof — FACT

Exact code-bearing head `4f127eec10da67f225bb7ff191f05b1389637494`:

```text
semantic_run=31910171592
semantic_state=SUCCESS
unit_job=95073745901 SUCCESS
isolated_synology_job=95073745877 SUCCESS
runner=synology-otclient-01
```

The new deterministic regression combines all three conditions that defeated the PR #313 design:

1. kill the `guard-run` caller after dispatch;
2. the guarded program explicitly closes inherited FDs `3..511`;
3. the guarded program forks/`setsid()` and continues as a daemonized descendant.

The independent nonblocking flock attempt remains rejected while the daemon is alive and succeeds only after the daemon lifetime ends.

The isolated Synology run also re-executed the pre-existing lease-manager self-test and emitted:

```text
TRACK_A_CANONICAL_LEASE_ENTRYPOINT_FENCED=true
TRACK_A_CANONICAL_LEASE_TOKEN_PATH_TRAVERSAL_REJECTED=true
TRACK_A_CANONICAL_LEASE_EXPIRED_RELEASE_REJECTED=true
TRACK_A_CANONICAL_LEASE_STALE_TAKEOVER_REASON_REQUIRED=true
TRACK_A_CANONICAL_LEASE_CONCURRENT_SERIALIZATION_PROVEN=true
TRACK_A_CANONICAL_LEASE_SELFTEST_COMPLETE=true
TRACK_A_CANONICAL_LEASE_CANONICAL_STATE_UNTOUCHED=true
```

No production canonical-live state was created or mutated by validation.

## Final-tree cleanup — FACT

The temporary push trigger for the remediation branch was removed after semantic validation. Durable workflow coverage retains the new supervisor unit/regression test paths and executes them in both unit and isolated Synology validation when the canonical lease workflow is explicitly run or its retained historical branch trigger applies.

Production supervisor/wrapper/test behavior is unchanged by that cleanup.

## Safety boundary

- no Tibia client/runtime process was launched, stopped, signalled, attached, logged in, or given input;
- no production canonical-live state was modified;
- no PR #303/#309 runtime-owned path/process was touched;
- Track B was not touched;
- `:98` was not declared canonical;
- no owner-funded Codex/OpenAI API or paid AI quota was invoked by this remediation.

## Remaining gates

This evidence is implementation/validation evidence, not terminal audit evidence. Before closeout:

1. exact-final-head repository `CI / Required` must pass;
2. a fresh independent audit must attempt to falsify the supervisor/lease acceptance and prior P1 repairs;
3. any material review finding must be repaired before merge;
4. PR #316 must reach `main` under normal repository protection;
5. only then may PR #313's material thread be resolved, closeout PR #314 be reconciled, and PR #311 governance be revalidated.
