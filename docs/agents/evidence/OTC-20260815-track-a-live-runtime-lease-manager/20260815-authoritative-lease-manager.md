# Track A canonical-live authoritative lease manager — 2026-08-15

Task: `OTC-20260815-track-a-live-runtime-lease-manager`  
Draft PR: `#312`  
Corrected code-bearing head: `e368173086ba8bb1235218b3ec11e046e2c909cb`  
Base: `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`

## Coordinator disposition history

The first reviewable implementation was **RETURN_FOR_EVIDENCE** after independent coordinator source review found a material stale-fencing defect: an expired controller could call `release` successfully and then reacquire normally, bypassing the required explicit stale-takeover reason/audit path.

The corrected implementation rejects `release` once `expires_at <= now`, leaves the expired active record intact, and therefore makes explicit stale takeover the only ownership-transition path after expiry.

## Why this exists

PR #311 established the owner-approved target model of one reusable canonical persistent Track A live session plus task-specific ephemeral GUI sandboxes. Independent review correctly found that descriptive lease metadata alone was insufficient: without a single authoritative storage location and serialized claim operation, two tasks could concurrently believe they owned the live runtime.

This Draft implements the missing atomic controller-lease primitive without changing #311 governance files or touching any live runtime.

## Production authority boundary — FACT

The production entrypoint is:

`.github/scripts/tibia-official-client-re-canonical-live-lease`

It fixes the authoritative lease state to:

`/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime`

Caller `--state-dir` overrides are rejected. A controller token path is canonicalized and must remain below:

`/home/runner/_work/_otclient_tibia_re_state/tasks/<task-id>/`

so lexical `../` traversal and out-of-task token paths are rejected before the implementation is invoked.

## Lease semantics — FACT

The internal implementation uses one stable `coordination.lock` with POSIX `flock` for all state transitions. It supports:

- `acquire`;
- `renew`;
- `validate`;
- `release`;
- token-redacted `status`;
- `guard-run`, which validates the controller and holds the same coordination lock while the guarded command executes.

State is atomically replaced and mode `0600`; the state directory is mode `0700`. Shared lease state stores only SHA-256 of the capability token. The raw random token remains in a caller task-local mode-`0600` file.

An expired active lease cannot be renewed, validated **or released** by the stale holder. It remains active-but-expired until a new acquisition supplies an explicit stale-takeover reason; takeover increments the generation and issues a new token. Old-generation credentials then fail against the replacement controller identity/token.

## Corrected exact validation — FACT

Custom semantic workflow on corrected head `e368173086ba8bb1235218b3ec11e046e2c909cb`:

```text
run=31907695244
unit_job=95067968895
unit=SUCCESS
selfhosted_job=95067968820
selfhosted_runner=synology-otclient-01
selfhosted=SUCCESS
```

Repository quality gate on the same corrected head:

```text
run=31907697738
CI / Required job=95068323632
CI / Required=SUCCESS
```

Self-hosted proof markers include:

```text
TRACK_A_CANONICAL_LEASE_ENTRYPOINT_FENCED=true
TRACK_A_CANONICAL_LEASE_TOKEN_PATH_TRAVERSAL_REJECTED=true
TRACK_A_CANONICAL_LEASE_EXPIRED_RELEASE_REJECTED=true
TRACK_A_CANONICAL_LEASE_STALE_TAKEOVER_REASON_REQUIRED=true
TRACK_A_CANONICAL_LEASE_CONCURRENT_SERIALIZATION_PROVEN=true
TRACK_A_CANONICAL_LEASE_SELFTEST_COMPLETE=true
TRACK_A_CANONICAL_LEASE_CANONICAL_STATE_UNTOUCHED=true
```

The expired-release discriminator created an isolated active lease, made only that isolated test record expired, proved stale `release` returns `lease_expired` while the record stays active/expired, proved acquisition without a takeover reason returns `stale_takeover_reason_required`, and then proved an explicit reason produces generation 2.

The concurrency discriminator launched two independent acquire processes against the same isolated state directory. Exactly one acquired the lease and the other returned `TRACK_A_CANONICAL_LEASE_ERROR=lease_conflict`.

## Isolation proof — FACT

The self-hosted workflow used only:

`/home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260815-track-a-live-runtime-lease-manager/selftest/<run-id>`

and removed it on exit. It did not create or modify the production canonical-live directory, did not attach to or signal the client, did not read credentials, did not log in, and did not mutate X11/noVNC/Track B state.

## Security / authority boundary

This is a cooperative same-UID programme-governance fence, not a hostile-local-user security boundary. A valid lease grants controller authority only; any task taking over an expired lease must still independently revalidate the actual runtime identity/state before mutation.

## Explicit UNKNOWN / NOT ENABLED

- canonical live Tibia process identity: UNKNOWN;
- canonical display registration: NOT ENABLED;
- `:98` canonical status: NOT PROVEN / NOT REGISTERED;
- exact `6082 -> :98` websockify target relation: UNKNOWN;
- live-session reuse under this manager: NOT ENABLED until promotion + governance integration;
- restart/relogin stability: remains a separate Track A runtime question.

## Promotion requirement

PR #312 remains Draft/unmerged until independent promotion. Coordinator #300 must re-review this corrected exact head and integrate required reusable-tool catalogue/changelog metadata before merge/promotion. PR #311 must remain fail-closed until the authoritative manager is present on `main`, its policy requires that mechanism for canonical-live control/restart/login/input mutations, and the material review finding is explicitly resolved after that integration.
