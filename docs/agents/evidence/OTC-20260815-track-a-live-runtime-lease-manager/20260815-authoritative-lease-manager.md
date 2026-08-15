# Track A canonical-live authoritative lease manager — 2026-08-15

Task: `OTC-20260815-track-a-live-runtime-lease-manager`  
Draft PR: `#312`  
Code-bearing head: `b52c464c6f9c1ffc2f22da70fc1c05550904d73f`  
Base: `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`

## Why this exists

PR #311 established the owner-approved model of one reusable canonical persistent Track A live session plus task-specific ephemeral GUI sandboxes. Independent review correctly found that descriptive lease metadata alone was insufficient: without a single authoritative storage location and serialized claim operation, two tasks could concurrently believe they owned the live runtime.

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

State is atomically replaced and mode `0600`; the state directory is mode `0700`. The shared lease state stores only SHA-256 of the capability token. The raw random token is stored in a caller task-local mode-`0600` file.

An expired active lease cannot be silently replaced: takeover requires an explicit reason and increments the generation. Old-generation tokens fail validation against the new token digest.

## Exact validation — FACT

Custom semantic workflow:

```text
run=31906213909
unit_job=95064329724
unit=SUCCESS
selfhosted_job=95064329739
selfhosted_runner=synology-otclient-01
selfhosted=SUCCESS
```

Repository quality gate:

```text
run=31906215762
CI / Required job=95064610764
CI / Required=SUCCESS
```

Self-hosted proof markers:

```text
TRACK_A_CANONICAL_LEASE_ENTRYPOINT_FENCED=true
TRACK_A_CANONICAL_LEASE_TOKEN_PATH_TRAVERSAL_REJECTED=true
TRACK_A_CANONICAL_LEASE_CONCURRENT_SERIALIZATION_PROVEN=true
TRACK_A_CANONICAL_LEASE_SELFTEST_COMPLETE=true
TRACK_A_CANONICAL_LEASE_CANONICAL_STATE_UNTOUCHED=true
```

The concurrency discriminator launched two independent acquire processes against the same isolated state directory. Exactly one acquired the lease and the other returned `TRACK_A_CANONICAL_LEASE_ERROR=lease_conflict`.

## Isolation proof — FACT

The self-hosted workflow used only:

`/home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260815-track-a-live-runtime-lease-manager/selftest/<run-id>`

and removed it on exit. It did not use the production canonical-live directory, did not attach to or signal the client, did not read credentials, did not log in, and did not mutate X11/noVNC/Track B state.

## Explicit UNKNOWN / NOT ENABLED

- canonical live Tibia process identity: UNKNOWN;
- canonical display registration: NOT ENABLED;
- `:98` canonical status: NOT PROVEN / NOT REGISTERED;
- exact `6082 -> :98` websockify target relation: UNKNOWN;
- live-session reuse under this manager: NOT ENABLED until promotion + governance integration;
- restart/relogin stability: remains a separate Track A runtime question.

## Promotion requirement

PR #312 remains Draft/unmerged. Coordinator #300 must independently review the implementation and evidence. If accepted, the coordinator must integrate the manager into canonical policy/tooling and shared catalogue/changelog as appropriate. PR #311 must remain fail-closed until its text requires this authoritative mechanism for all canonical-live control/restart/login/input mutations and its review finding is explicitly resolved after that integration.