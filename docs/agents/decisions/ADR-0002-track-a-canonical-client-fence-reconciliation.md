# ADR-0002: Track A canonical client-fence reconciliation

- Status: Proposed until merged to protected `main`
- Date: 2026-08-28
- Scope: Track A canonical-live registration metadata
- Extends: `ADR-0001-track-a-canonical-live-runtime.md`
- Contract: `docs/agents/contracts/TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_V1.md`

## Context

Trusted repository authority was advanced to official Linux client `15.32.75d4a0 / 52105824 / d1a16819...` by PR #754 without executing or rewriting the live canonical runtime. That repository-only safety boundary was correct, but it left a durable runtime-registration predecessor possible.

The subsequent gameWindowState memory-free preflight on trusted main stopped before any process-memory observation with `REGISTRATION_CLIENT_VERSION_MISMATCH`. Existing canonical transitions intentionally cannot repair that condition:

- generation rebind requires the same exact registered runtime;
- same-boot stale-registration recovery preserves the accepted client fence;
- boot-epoch recovery preserves the accepted client fence;
- existing-runtime adoption requires registration absence;
- bootstrap must not be used while registration exists.

Manual deletion/editing of `runtime-registration.json` would bypass canonical authority and is forbidden.

## Decision

Add one finite metadata-only `canonical_recovery` subtype named `client_fence_reconciliation_v1`, governed by `TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_V1.md`.

It accepts only the explicitly superseded registration fence:

`15.32 / 52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`

and may replace it only with repeated fresh proof of the already-promoted current exact fence:

`15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`.

The operation runs as a finite worker under the existing canonical lease `guard-run`, so the already-reviewed cancellation-safe supervisor owns `coordination.lock` for the complete state-changing transaction. The worker does not create a second lease/lock/registration authority system.

The source registration is treated only as a bounded predecessor record. It must be an exact known `existing_runtime_adoption_v1`, fail-closed `UNKNOWN` registration with complete singleton inventory evidence and self-consistent fingerprint. It is never accepted as current executable authority.

Current target identity is established only by three matching invocations of the reviewed current Kasm adoption probe around the atomic commit. The canonical Docker container name, display and remote-view mapping remain continuity anchors. Boot/PID/start/container-instance identity may change because an exact-client build transition is precisely the case being reconciled; all of those fields are replaced from fresh proof.

The resulting state is forced to `UNKNOWN`. No prior semantic state is promoted or retained.

## Non-decisions

This ADR does not change or broaden the implementation semantics of:

- `rebind`;
- `stale-registration-recovery`;
- `boot-epoch-registration-recovery`;
- `adopt-existing`;
- `bootstrap`;
- Gate B or guarded client mutation.

It does not establish a generic version-upgrade mechanism. A different predecessor or future target needs a separately reviewed trusted-base change.

It does not authorize login, credentials, GUI input, gameplay, process control, memory observation, ptrace, injection or network payload capture.

## Consequences

A repository implementation must merge first with `runtime_access: none`. Unmerged code cannot be used as runtime authority.

After merge, a trusted-main invocation may acquire the canonical lease and execute the reconciliation worker under `guard-run`. A successful transaction updates only canonical registration metadata and releases authority again.

After reconciliation, downstream runtime work must re-run its own fresh admission. For the gameWindowState lane that means re-running the memory-free `PREFLIGHT_GAME_WINDOW_STATE_QUALIFICATION`; reconciliation success alone is not read-only logger readiness and is not semantic validation.

Any mismatch outside the closed source/target contract remains a terminal fail-closed blocker rather than a reason to delete, rewrite or broaden the registration manually.
