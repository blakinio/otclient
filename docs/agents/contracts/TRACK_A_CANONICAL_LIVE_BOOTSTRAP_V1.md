# Track A Canonical Live Bootstrap Contract v1

Status: **DRAFT CONTRACT / FINAL MANAGER RECONCILED / NOT IMPLEMENTED**  
Track: `official-client-re`  
Task: `OTC-20260815-track-a-canonical-live-bootstrap-contract`

## Purpose

Define the only acceptable transition from **no registered canonical live runtime** to **one registered idle persistent official-client runtime**.

This contract exists because two valid gates otherwise deadlock during first creation:

- controller mutation requires authoritative lease ownership;
- reuse/mutation of an existing runtime requires current runtime identity registration;
- when no registered exact-fenced live client exists, initial creation cannot satisfy the ordinary reuse gate before the process is created and proven.

PR #315 previously observed zero exact-fenced client processes/windows during its bounded read-only probe. That observation is historical evidence only; current `:98`, `6082`, PID, process and session canonical status remains `UNKNOWN` / `NOT_REGISTERED` until a new direct preflight proves otherwise.

Bootstrap is therefore a special **creation transaction**, not ordinary reuse and not a relaxation of either gate.

## Promoted manager dependency

The final manager/supervisor stack is already promoted on `main`:

- PR #317 supplies generic descriptor last-close semantics for the manager coordination lock;
- PR #316 supplies the production out-of-band Linux child-subreaper supervisor;
- final PR #316 implementation head: `d61d362c12125e3c70167f09729a0caa8b891e78`;
- merged manager main: `e9df81f50dbb231bc4ac6cc3fc21f260fc358d34`;
- fresh manager closeout/archive: PR #319, merged as `25700f08c3f5729e4ee38bf8c0a3ca04020379be`.

For ordinary guarded mutation, the caller acquires and validates the authoritative lease before dispatch, transfers the coordination flock only to a dedicated child-subreaper supervisor, starts the guarded command with `close_fds=True` so the command receives no flock descriptor, and keeps serialization until the primary command plus all adopted/orphaned descendants have exited.

That final `guard-run` behavior is a required foundation, but it is deliberately **not sufficient by itself for bootstrap**: ordinary `guard-run` completes only after the guarded process tree is gone, while successful bootstrap must leave one exact registered official-client process alive after an explicit verified detach transition. Bootstrap therefore requires a distinct reviewed primitive/state machine that preserves the same authority and anti-escape guarantees through registration and detachment.

## Preconditions

Bootstrap MUST fail closed unless all are true at transaction start:

```yaml
track: official-client-re
platform: official_native_linux_only
current_live_registration: absent
current_exact_live_client_count: 0
current_exact_live_client_count_evidence: fresh_direct_preflight
controller_lease: current_and_valid
lease_generation: known
lease_manager: final_promoted_current_main_version
bootstrap_supervisor: reviewed_current_main_bootstrap_version
canonical_namespace:
  state_root: declared
  display: declared_after_preflight
  remote_view_endpoint: declared_or_null_after_preflight
second_live_session_authorized: false
```

If an exact live client already exists, this contract MUST NOT create another session. The caller must enter the ordinary registration/reuse/recovery path instead. Historical display/process observations are not sufficient to satisfy these preconditions.

## Exact client fence

The created client MUST match:

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

A different official client build requires an explicitly revalidated fence before bootstrap.

## State machine

```text
ABSENT
  |
  | fresh preflight proves no registered/exact live client
  | acquire current controller lease
  v
BOOTSTRAP_LEASED
  |
  | bootstrap supervisor creates task/track-owned launch descendants
  v
PROCESS_CREATED_UNREGISTERED
  |
  | exact executable + boot/PID/start + display/window proof
  | bounded protected login/character/world bootstrap only if separately authorized
  v
PROCESS_VERIFIED
  |
  | atomically publish generation-bound registration candidate
  v
REGISTRATION_PENDING_COMMIT
  |
  | supervisor rechecks lease + descendant identity + exact fence + state
  v
REGISTERED_IDLE_RUNTIME
  |
  | explicit safe-detach proof; no mutation-capable helper remains
  | supervisor intentionally relinquishes bootstrap mutation ownership
  v
IDLE_REUSABLE
```

Any failure before `REGISTERED_IDLE_RUNTIME` goes to `ABORT_CLEANUP`, which terminates only bootstrap-owned descendants and leaves no registration claiming success.

## Authority invariant

The bootstrap transaction MUST begin with a current authoritative controller lease and MUST remain under one reviewed external supervisor for the entire mutation phase, including process creation, any separately authorized login mutation, identity proof, registration commit and safe-detach checks.

The persistent client MUST NOT receive the coordination flock or lease capability. Only the external supervisor may hold the coordination flock during bootstrap mutation.

Forbidden patterns:

- standalone `validate` then detached launch;
- launcher forks a persistent descendant and exits before supervisor tracks it;
- passing the coordination flock or lease capability into the client or helper;
- writing registration before the exact process identity is proven;
- releasing bootstrap mutation authority before registration is durably committed and revalidated;
- claiming a process from another task/display/track;
- treating PR/task metadata as lease authority.

## Bootstrap supervisor invariant

The implementation must provide an explicit controlled transition distinct from ordinary `guard-run`, for example:

```text
supervise_create_until_registered(...)
```

or an equivalent reviewed primitive whose success condition is not child exit, but verified registration of the still-running exact client followed by safe supervisor detachment.

It MUST preserve the final PR #316 anti-escape model during the mutation phase:

- authoritative lease acquired and validated before dispatch;
- only the external supervisor holds the coordination flock after dispatch;
- launched command/client/helpers receive no flock descriptor and no lease capability;
- caller/launcher exit cannot release serialization while bootstrap-owned mutation descendants remain;
- daemonized/orphaned bootstrap descendants remain supervised/adopted until they are either proven to be the one registered persistent client at the safe-detach boundary or are cleaned up;
- lease/generation changes invalidate the transaction before commit/detach.

A bootstrap implementation is **not authorized by this documentation PR**. It requires its own implementation task, deterministic tests, review, exact-head CI and separately authorized real-client E2E before any live creation/login claim.

## Runtime registration record

Registration MUST be atomic and mode-restricted. Required non-secret fields:

```yaml
schema_version: 1
runtime_id: track-a-canonical-live
registration_generation: <monotonic registration generation>
lease_generation: <current controller lease generation>
registered_at: <timestamp>
boot_id_sha256: <hash>
pid: <current pid>
process_start_ticks: <current /proc starttime>
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
display: <declared canonical display proven now>
window_identity: <non-secret current window evidence>
remote_view_endpoint: <declared endpoint or null>
remote_view_mapping: PROVEN | UNKNOWN
state: LOGIN | CHARACTER_SELECT | IN_GAME | DISCONNECTED | UNKNOWN
source_task: <bootstrap task id>
source_run: <run id>
```

The record MUST NOT contain credentials, cookies, session keys, packet payloads, framebuffer contents or raw account/character secrets.

## PID reuse and process identity

PID alone is insufficient. Positive identity requires at least:

```text
boot identity + PID + process start ticks + /proc/<pid>/exe exact size/SHA
```

Immediately before registration commit and immediately before supervisor detachment, the exact identity MUST be rechecked.

## Display/window identity

A display is not canonical merely because it exists. The bootstrap transaction must prove that the exact client process owns the selected official-client window on the declared canonical X11 display.

Durable historical evidence does not establish current canonical state. The current contract baseline is:

```yaml
display_98_historical_track_a_evidence: FACT_FROM_PRIOR_PROBES
display_98_current_canonical_status: UNKNOWN
rfb_6082_historical_metadata_supports_display_98: FACT_FROM_PRIOR_PROBES
rfb_6082_current_backend_mapping: UNKNOWN
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
```

A bootstrap implementation may select `:98` only after a fresh transaction-start preflight proves that it is available, appropriate and bound to the exact process being registered. This contract does not pre-register `:98` or `6082`.

## Login / credentials boundary

If initial creation requires login:

- login must be separately authorized for that execution; this contract does not grant that authority;
- credentials exist only in a protected bounded login step;
- persistent client/helper environments must be credential-variable-free;
- no credentials/cookies/session values may enter registration or artifact output;
- the login procedure must consume the current reviewed Track A login evidence and fail closed on UI/state mismatch;
- bootstrap must not create a second logged-in Track A session without explicit owner authorization.

## Network boundary

Any live client created by a future authorized bootstrap must preserve the currently accepted Track A egress confinement (WARP/SOCKS or a separately approved successor boundary). Direct unapproved client transport fails closed.

Network liveness alone is never `IN_GAME` authority.

## Registration commit

Registration commit is a two-phase operation:

1. write a candidate record atomically under the bootstrap supervisor;
2. re-read/revalidate the exact live process, current lease generation, display/window and required state;
3. promote candidate to current registration atomically;
4. re-read the committed registration and revalidate exact process identity and lease generation;
5. only then allow the explicit safe-detach transition.

If the current controller lease changes during the transaction, bootstrap aborts. A registration created under an older generation cannot be committed under a replacement lease.

## Safe detachment / idle transition

The persistent exact client must not inherit the controller coordination flock or lease capability. The external supervisor owns mutation serialization until the detach boundary succeeds.

After successful registration commit, supervisor detachment must prove:

- client exact identity still matches the committed registration;
- committed registration still names the current boot/PID/start/exact fence/display/window identity;
- no bootstrap/login/helper process capable of mutation remains untracked;
- any remaining process is either the exact registered persistent client or explicitly classified non-mutating and owned;
- the persistent client itself has no controller-lock FD/capability token;
- registration is current and bound to the lease generation used for creation;
- supervisor relinquishment is explicit and cannot be triggered merely by launcher/caller exit;
- canonical controller lease may then be released normally;
- client remains as the registered idle programme resource.

A detached client does not itself hold controller authority. Later external mutation requires a fresh/current lease plus current exact-runtime registration/preflight.

## Abort cleanup

Before registration commit, any error must:

- mark candidate registration absent/invalid;
- terminate only descendants whose bootstrap ownership/provenance is proven;
- wait/reap boundedly where safe;
- never use broad `pkill`/display cleanup;
- not kill Track B or PR #303 task-owned runtime;
- release controller lease only after bootstrap mutation descendants are gone or demonstrably unable to continue mutation.

If safe cleanup cannot be proven, retain/fail closed rather than releasing authority around an untracked descendant.

After registration commit but before safe detach, any failure must fail closed and treat the committed registration as requiring recovery/revalidation; it must not silently release authority while a mutation-capable bootstrap descendant remains.

## Post-bootstrap reuse

Ordinary later mutation/reuse requires:

1. acquire current authoritative lease;
2. load current registration;
3. revalidate boot/PID/start/exact fence/display/window and required mutation-relevant state;
4. perform mutation through the final reviewed supervisor for the complete mutation/process-tree lifetime;
5. update/invalidate registration if process or identity-bearing state changes materially;
6. release lease only when no guarded mutation descendants remain.

After stale lease takeover, the registration must be revalidated before any mutation.

## Evidence requirements

Implementation cannot be promoted without deterministic non-live tests proving at least:

- no-registration -> exact-child -> atomic registration -> safe detach;
- wrong SHA abort;
- PID reuse/start mismatch abort;
- lease-generation change during bootstrap abort;
- immediate launcher exit with surviving child remains supervised;
- daemonized child cannot escape supervision;
- caller death cannot release serialization around a mutation descendant;
- helper child remains alive -> detach fails;
- candidate written but identity changes before commit -> abort;
- committed registration changes identity before detach -> detach fails/recovery required;
- registration commit then controller release leaves client but no mutation helper;
- persistent client receives neither flock descriptor nor lease capability;
- second bootstrap refused if a registered/exact live client already exists;
- cleanup affects only owned descendants;
- no secret fields in state/log/artifacts.

A later controlled real-client E2E must separately prove the transition with the exact fenced client. Test success alone does not prove a current live session.

## Explicit non-claims

This contract does not:

- implement bootstrap;
- authorize launch or login now;
- declare `:98` canonical;
- prove current `6082 -> :98` mapping;
- register a PID/process/session;
- alter PR #303 runtime ownership;
- alter Track B;
- complete P0/P1/A3/A4;
- make Track A complete.
