# PR #312 canonical-live lease manager — coordinator disposition

Coordinator task: `OTC-20260815-track-a-promotion-coordination`  
Source PR: `#312`  
Source corrected code head: `e368173086ba8bb1235218b3ec11e046e2c909cb`  
Source final handoff head at review start: `10c584119f1b7c5dcb3211bac425fc8528ed4b76`  
Canonical base: `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`

## Disposition

`ACCEPT_WITH_EDITS`

The first #312 handoff was not accepted merely because CI was green. Coordinator source review found a material stale-fencing defect: an expired holder could release its expired generation and reacquire normally, bypassing the required explicit stale-takeover reason/audit path. The source was returned for evidence and repaired before this disposition.

## Accepted FACT

Corrected implementation:

- fixes production lease state to `/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime` through the public shell entrypoint;
- rejects production `--state-dir` override;
- confines task capability tokens to the canonicalized claiming-task state root;
- serializes all state transitions with one stable POSIX `flock`;
- atomically writes mode-0600 state and stores only a SHA-256 token digest in shared state;
- provides `acquire`, `renew`, `validate`, `release`, redacted `status`, and lock-held `guard-run`;
- requires expiry plus explicit reason for stale takeover and increments generation;
- rejects renew/validate/release from an expired holder;
- leaves an expired active record intact so the holder cannot bypass stale takeover by releasing it first;
- rejects stale credentials after replacement;
- is a cooperative same-UID programme-governance fence, not a hostile-user security boundary.

## Corrected exact evidence

```text
code_head=e368173086ba8bb1235218b3ec11e046e2c909cb
custom_run=31907695244
unit_job=95067968895 SUCCESS
selfhosted_job=95067968820 SUCCESS
runner=synology-otclient-01
repository_ci=31907697738 SUCCESS
ci_required_job=95068323632 SUCCESS
```

Self-hosted markers include:

```text
TRACK_A_CANONICAL_LEASE_ENTRYPOINT_FENCED=true
TRACK_A_CANONICAL_LEASE_TOKEN_PATH_TRAVERSAL_REJECTED=true
TRACK_A_CANONICAL_LEASE_EXPIRED_RELEASE_REJECTED=true
TRACK_A_CANONICAL_LEASE_STALE_TAKEOVER_REASON_REQUIRED=true
TRACK_A_CANONICAL_LEASE_CONCURRENT_SERIALIZATION_PROVEN=true
TRACK_A_CANONICAL_LEASE_SELFTEST_COMPLETE=true
TRACK_A_CANONICAL_LEASE_CANONICAL_STATE_UNTOUCHED=true
```

## Required coordinator edits before promotion

The manager is reusable cross-task governance tooling. Repository policy requires discovery metadata in the same promotion PR. Therefore #312 must add bounded entries to:

- `docs/agents/MODULE_CATALOG.md`;
- `docs/agents/CHANGELOG.md`.

Coordinator ownership of exactly those two paths is delegated to the #312 promotion slice for this bounded edit. No other #300 owned path is delegated.

After those edits, #312 must pass final exact-head custom validation and repository `CI / Required`, have no unresolved material review findings, and then may be promoted/merged. Until it is on `main`, PR #311 policy v3 correctly keeps canonical live mutation/reuse disabled.

## Explicit non-claims

- `:98` is not registered canonical by this disposition.
- Canonical live client PID/session identity remains unproven for current runtime.
- `6082 -> :98` exact backend mapping remains unproven.
- A lease grants authority only; runtime identity/state must still be revalidated before mutation/takeover.
- This disposition does not change Track B ownership or authorize a second live Global session.
