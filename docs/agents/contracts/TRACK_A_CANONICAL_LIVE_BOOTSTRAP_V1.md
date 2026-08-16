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

For ordinary guarded mutation, the caller first has a current authoritative lease record/capability, then `guard-run` acquires the canonical coordination flock and validates that lease before dispatch. After fork, only a dedicated child-subreaper supervisor retains the flock; it starts the guarded command with `close_fds=True` so the command receives no flock descriptor, and keeps serialization until the primary command plus all adopted/orphaned descendants have exited.

That final `guard-run` behavior is a required foundation, but it is deliberately **not sufficient by itself for bootstrap**: ordinary `guard-run` completes only after the guarded process tree is gone, while successful bootstrap must leave one exact registered official-client process alive after an explicit verified detach transition. Bootstrap therefore requires a distinct reviewed primitive/state machine that preserves the same authority and anti-escape guarantees through registration and detachment.

## Authoritative namespace

Bootstrap and all later Gate B readers/writers MUST use the manager-owned canonical namespace exactly as promoted by the production wrapper:

```yaml
state_root: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime
coordination_lock: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/coordination.lock
lease_record: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/lease.json
runtime_registration: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json
```

`runtime-registration.json` is the one authoritative current registration path. Bootstrap candidates MUST be written as mode-restricted temporary files in the same directory and atomically renamed to that exact path only at commit. Controllers MUST NOT select, override, infer or create an alternative state root or registration path. Absence means that this exact registration is absent or explicitly invalidated while the bootstrap supervisor holds the canonical coordination flock and has just validated the current authoritative lease; absence in any other directory is irrelevant.

## Preconditions and transaction-start ordering

Static prerequisites may be checked before coordination, but **runtime absence is authoritative only while the canonical coordination flock is already held by the bootstrap supervisor**. A pre-lock inventory may be used for diagnostics but MUST NOT authorize launch.

Before any bootstrap child is created, the controller/bootstrap supervisor MUST perform this exact order:

1. acquire or renew the current authoritative controller lease through the promoted manager and retain its task/session identity plus task-local capability token;
2. start the reviewed bootstrap supervisor, which acquires the canonical `coordination.lock` flock and, while holding it, validates the current lease identity/token/generation exactly as the final manager requires;
3. while that same supervisor-owned flock remains held, perform a fresh fail-closed inventory immediately before launch;
4. prove the exact authoritative registration is absent and prove there is no existing official-client candidate/session that could conflict with a second live session;
5. only then create bootstrap descendants while the supervisor continuously retains the flock.

Acquiring the durable lease record does **not** by itself mean the coordination flock remains held after the manager `acquire` call returns. The decisive absence check and launch authorization therefore belong inside the bootstrap supervisor's flock-held critical section.

The under-lock inventory MUST satisfy all of the following:

```yaml
track: official-client-re
platform: official_native_linux_only
controller_lease: current_and_valid
lease_generation: known_and_revalidated_under_lock
coordination_flock: held_by_bootstrap_supervisor
lease_manager: final_promoted_current_main_version
bootstrap_supervisor: reviewed_current_main_bootstrap_version
canonical_namespace:
  state_root: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime
  runtime_registration: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json
current_live_registration: absent
current_live_registration_evidence: fresh_under_authoritative_lock
current_exact_live_client_count: 0
current_exact_live_client_count_evidence: fresh_under_authoritative_lock
all_official_client_candidate_count: 0
unverifiable_or_mismatched_official_client_candidate_count: 0
existing_official_client_session_count: 0
inventory_completeness: proven_for_permitted_local_process_window_session_evidence
canonical_display: declared_after_under_lock_preflight
remote_view_endpoint: declared_or_null_after_under_lock_preflight
second_live_session_authorized: false
```

The inventory is fail-closed across **all** official native Linux client candidates, not only the exact fenced build. A running official client with a different version/hash, a process/window/session that plausibly belongs to the official client but cannot be verified, or local evidence of an existing official-client account/session is a blocker rather than evidence of absence. If the permitted local evidence cannot establish inventory completeness, bootstrap MUST stop for recovery/reconciliation instead of launching another client.

If a registered client, an exact live client, any mismatched/unverifiable official-client candidate, or any existing official-client session is found, this contract MUST NOT create another session. The caller must enter the ordinary registration/reuse/recovery path or explicit reconciliation path instead. Historical display/process observations are not sufficient to satisfy these preconditions.

The bootstrap supervisor MUST keep the canonical coordination flock continuously from before lease revalidation and the authoritative absence inventory through creation, registration commit and safe detach. Therefore two concurrent bootstrap callers cannot both act on the same stale absence observation: after waiting for the flock, a later supervisor must revalidate its lease, repeat the full under-lock inventory and refuse creation if the first caller has already registered or left any conflicting official-client candidate/session.

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
UNCLAIMED
  |
  | acquire/renew authoritative controller lease record + capability
  v
LEASE_GRANTED
  |
  | reviewed bootstrap supervisor acquires canonical coordination flock
  | and validates lease identity/token/generation while holding it
  v
SUPERVISOR_LOCKED
  |
  | while the same flock remains held: fresh authoritative registration +
  | all-official-client process/window/session inventory proves zero
  | registered/exact/mismatched/unverifiable clients
  v
BOOTSTRAP_LEASED_ABSENT
  |
  | supervisor creates task/track-owned launch descendants
  v
PROCESS_CREATED_UNREGISTERED
  |
  | exact executable + boot/PID/start + display/window proof
  | bounded protected login/character/world bootstrap only if separately authorized
  v
PROCESS_VERIFIED
  |
  | atomically publish generation-bound registration candidate to the authoritative registration path
  v
REGISTRATION_PENDING_COMMIT
  |
  | supervisor rechecks lease + descendant identity + exact fence + state
  v
REGISTERED_IDLE_RUNTIME
  |
  | explicit safe-detach proof; no mutation-capable helper remains
  | supervisor intentionally relinquishes bootstrap mutation ownership and flock
  v
IDLE_REUSABLE
```

Any failure before `REGISTERED_IDLE_RUNTIME` goes to `ABORT_CLEANUP`, which terminates only bootstrap-owned descendants and leaves no registration claiming success.

## Authority invariant

The bootstrap transaction MUST begin with a current authoritative controller lease. Before making any runtime-absence decision, its reviewed external bootstrap supervisor MUST acquire the canonical coordination flock and validate the current lease identity/token/generation under that flock. The decisive runtime-absence inventory, process creation, any separately authorized login mutation, identity proof, registration commit and safe-detach checks all occur while that one supervisor continuously owns the flock.

The persistent client MUST NOT receive the coordination flock or lease capability. Only the external supervisor may hold the coordination flock during bootstrap mutation.

Forbidden patterns:

- standalone `validate` then detached launch;
- checking absence before the bootstrap supervisor acquires the coordination flock and later launching from that stale observation;
- assuming a successful manager `acquire` call itself keeps `coordination.lock` held across subsequent work;
- launcher forks a persistent descendant and exits before supervisor tracks it;
- passing the coordination flock or lease capability into the client or helper;
- writing registration before the exact process identity is proven;
- using a registration path outside `/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json`;
- treating a mismatched or unverifiable official-client candidate as equivalent to absence;
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

- a current authoritative lease record/capability exists before the supervisor critical section;
- the supervisor acquires the canonical coordination flock and validates that lease under the flock before any decisive absence check or dispatch;
- under that continuously held flock, authoritative registration plus all-official-client candidate/session absence is freshly re-proven immediately before launch;
- only the external supervisor holds the coordination flock after dispatch;
- launched command/client/helpers receive no flock descriptor and no lease capability;
- caller/launcher exit cannot release serialization while bootstrap-owned mutation descendants remain;
- daemonized/orphaned bootstrap descendants remain supervised/adopted until they are either proven to be the one registered persistent client at the safe-detach boundary or are cleaned up;
- lease/generation changes invalidate the transaction before commit/detach.

A bootstrap implementation is **not authorized by this documentation PR**. It requires its own implementation task, deterministic tests, review, exact-head CI and separately authorized real-client E2E before any live creation/login claim.

## Runtime registration record

The authoritative current record is exactly:

```text
/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json
```

Registration MUST be atomic and mode-restricted. All readers, candidate writers, committers, recovery logic and Gate B preflight MUST use this namespace/path. Required non-secret fields:

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

A bootstrap implementation may select `:98` only after the supervisor-owned under-lock transaction-start inventory proves that it is available, appropriate and bound to the exact process being registered. This contract does not pre-register `:98` or `6082`.

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

Registration commit is a two-phase operation inside the authoritative state directory while the bootstrap supervisor still continuously owns the canonical coordination flock and the validated lease generation remains current:

1. write a mode-restricted candidate as a uniquely named temporary file in `/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/`;
2. re-read/revalidate the exact live process, current lease generation, display/window and required state;
3. atomically rename the candidate to `/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json`;
4. re-read that exact committed registration and revalidate exact process identity and lease generation;
5. only then allow the explicit safe-detach transition.

If the current controller lease changes during the transaction, bootstrap aborts. A registration created under an older generation cannot be committed under a replacement lease.

## Safe detachment / idle transition

The persistent exact client must not inherit the controller coordination flock or lease capability. The external supervisor owns mutation serialization until the detach boundary succeeds.

After successful registration commit, supervisor detachment must prove:

- client exact identity still matches the committed authoritative registration;
- committed registration still names the current boot/PID/start/exact fence/display/window identity;
- no bootstrap/login/helper process capable of mutation remains untracked;
- any remaining process is either the exact registered persistent client or explicitly classified non-mutating and owned;
- the persistent client itself has no controller-lock FD/capability token;
- registration is current and bound to the lease generation used for creation;
- supervisor relinquishment is explicit and cannot be triggered merely by launcher/caller exit;
- canonical coordination flock is closed/released by the supervisor only after all detach checks succeed;
- canonical controller lease may then be released normally;
- client remains as the registered idle programme resource.

A detached client does not itself hold controller authority. Later external mutation requires a fresh/current lease plus current exact-runtime registration/preflight.

## Abort cleanup

Before registration commit, any error must:

- remove/mark invalid only the bootstrap candidate; it MUST NOT fabricate or preserve a current registration claiming success;
- terminate only descendants whose bootstrap ownership/provenance is proven;
- wait/reap boundedly where safe;
- never use broad `pkill`/display cleanup;
- not kill Track B or PR #303 task-owned runtime;
- keep the supervisor-owned coordination flock until bootstrap mutation descendants are gone or demonstrably unable to continue mutation.

If safe cleanup cannot be proven, retain/fail closed rather than releasing authority around an untracked descendant.

After registration commit but before safe detach, any failure must fail closed and treat the authoritative committed registration as requiring recovery/revalidation; it must not silently release authority while a mutation-capable bootstrap descendant remains.

## Post-bootstrap reuse

Ordinary later mutation/reuse requires:

1. acquire or renew the current authoritative lease;
2. enter the final reviewed supervisor critical section, acquire the canonical coordination flock and validate the lease under that flock;
3. load `/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json` only;
4. revalidate boot/PID/start/exact fence/display/window and required mutation-relevant state, and fail closed if any competing or unverifiable official-client candidate/session is present;
5. perform mutation through the final reviewed supervisor for the complete mutation/process-tree lifetime;
6. update/invalidate the authoritative registration if process or identity-bearing state changes materially;
7. release the coordination flock only when no guarded mutation descendants remain.

After stale lease takeover, the registration must be revalidated before any mutation.

## Evidence requirements

Implementation cannot be promoted without deterministic non-live tests proving at least:

- no-registration -> exact-child -> atomic registration -> safe detach;
- manager lease acquisition alone is not treated as continuous flock ownership;
- bootstrap supervisor acquires the canonical coordination flock and validates the lease before the authoritative absence check;
- authoritative absence check occurs under that flock immediately before launch;
- two concurrent bootstraps cannot both act on one stale absence observation: the second waits for the flock, revalidates its lease, repeats under-lock inventory, then refuses once the first registers or leaves a conflicting client;
- all registration readers/writers use `/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json` and alternative roots/paths fail closed;
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
- second bootstrap refused if a registration, exact client, mismatched/unverifiable official-client candidate, or existing official-client session already exists;
- incomplete inventory fails closed instead of being treated as absence;
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
