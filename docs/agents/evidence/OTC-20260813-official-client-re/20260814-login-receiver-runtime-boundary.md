# Official login receiver runtime boundary

Track: `official-client-re` / `OTCLIENT-TIBIA-RE`  
Evidence date: 2026-08-14  
Exact executable SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`  
Exact executable size: `51965216`

## Objective

Resolve the concrete receiver and the virtual target reached by the already-proven primary login-signal path without using account credentials or sending a game-login request.

Proven static entry into this experiment:

```text
sendLoginMessage signal PMF 0xcf2950
  -> QObject::connectImpl call 0x7d564f
  -> slot PMF 0xbd36a0
  -> adapter virtual dispatch receiver->vtable[+0x68]
```

## Runtime probe — TERMINAL FAILURE WITH VALID SETUP

Workflow:

```text
.github/workflows/tibia-official-client-re-login-receiver-runtime.yml
```

Run/job:

```yaml
run_id: 31825650545
job_id: 94849027826
head: a187797abf128c9d2d021a8960d1ab0429986b11
result: FAILURE
```

The setup portion completed successfully and independently revalidated the exact runtime:

```text
PINNED_PRELOGIN_RECIPE_EXTRACTED=true
WARP_CHANGED_EGRESS_VERIFIED=true
COMPLETE_OFFICIAL_RUNTIME_LAYOUT_VERIFIED=true
EXACT_CLIENT_PRELOGIN_RUNTIME_READY=true
LOAD_BIAS=0x555555554000
CLIENT_MAP_START=0x555555554000
CLIENT_MAP_END=0x5555586e3000
Breakpoint 1 at 0x555555d2964f
```

The probe then continued the client for a bounded 90 seconds. The normal pre-login client startup progressed through asset loading and first-start UI initialization, but the breakpoint corresponding to static RVA `0x7d564f` was never reached before the timeout. Consequently no `PRIMARY_CONNECT_HIT`, receiver pointer, vptr or `vtable+0x68` target was emitted.

This is a semantic boundary, not an exact-client reconstruction failure.

Artifact:

```yaml
name: track-a-login-receiver-runtime-31825650545
artifact_id: 9228801378
zip_sha256: 72e81cb740c377a0e4f41eb697980cdf0f303c383751197fecc50a3da8e59720
```

## Classification

### FACT

- The exact 15.32 executable reconstructed and started successfully on the hosted probe.
- PIE load bias calculation succeeded and the static `0x7d564f` breakpoint was armed at runtime address `0x555555d2964f`.
- A credential-free, ordinary pre-login startup did not execute that connect site within the bounded 90-second observation window.
- Therefore this particular no-credential startup probe cannot resolve the receiver/vtable target.

### INFERENCE

The login-handler wiring containing `0x7d564f` is likely instantiated only after a later authentication/login-related state transition, or through a code path not entered by passive first-start UI initialization. This is not yet proven as the only reason the breakpoint remained unhit.

### DISPROVEN

- Passive exact-client pre-login startup is sufficient, by itself, to observe the primary `sendLoginMessage` connect site within the tested window.

### UNKNOWN

- primary receiver class/vptr;
- `*(receiver_vptr+0x68)` target;
- exact lifecycle transition required to instantiate the wiring;
- whether a later non-secret UI action could instantiate the wiring without authenticating.

## Next evidence path

Do not increase the passive timeout or add credentials merely to make this breakpoint fire. Continue with static origin recovery for the enclosing object and its `[+0x88]` member, while independently converging the already-proven outbound network-owner chain on the final `QIODevice`/socket write sink. If a later Track A-owned authenticated runtime is already active for another accepted experiment, the receiver can be observed there only under the task's isolation and no-secret-persistence rules; do not launch a duplicate login session solely for this probe.
