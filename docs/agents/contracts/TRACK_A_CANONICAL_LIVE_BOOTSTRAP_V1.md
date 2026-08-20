# Track A Canonical Live Bootstrap Contract v1

Status: **DRAFT CONTRACT / FINAL MANAGER + REBIND RECONCILED / NOT IMPLEMENTED**  
Track: `official-client-re`  
Task: `OTC-20260815-track-a-canonical-live-bootstrap-contract`

## Purpose

Define the only acceptable transition from **no registered canonical live runtime** to **one registered idle persistent official-client runtime**.

This contract exists because valid gates otherwise deadlock during first creation:

- controller mutation requires authoritative lease ownership;
- reuse/mutation of an existing runtime requires current runtime identity registration;
- when no registered exact-fenced live client exists, initial creation cannot satisfy the ordinary reuse gate before the process is created and proven.

PR #315 previously observed zero exact-fenced client processes/windows during its bounded read-only probe. That observation is historical evidence only; current `:98`, `6082`, PID, process and session canonical status remains `UNKNOWN` / `NOT_REGISTERED` until a new direct preflight proves otherwise.

Bootstrap is therefore a special **creation transaction**, not ordinary reuse, not registration-generation rebinding, and not a relaxation of either authority or identity gates.

## Promoted manager dependency

The final manager/supervisor stack is already promoted on `main`:

- PR #317 supplies generic descriptor last-close semantics for the manager coordination lock;
- PR #316 supplies the production out-of-band Linux child-subreaper supervisor;
- PR #321 supplies cancellation-safe lock ownership so foreground process-group cancellation cannot kill the flock owner while a guarded descendant remains alive;
- final PR #321 implementation head: `d5bff95997e82d4ac5180d0e9c1b85dae8a3c7dd`;
- final manager main: `8828150617d68247be2074b330f4d954e508307b`;
- fresh final manager closeout/archive: PR #322, merged as `b0fd474e34c0252220b773b2304d889821080727`.

For ordinary guarded mutation, the caller first has a current authoritative lease record/capability, then `guard-run` acquires the canonical coordination flock and validates that lease before dispatch. After fork, only a dedicated child-subreaper supervisor retains the flock; it starts the guarded command with `close_fds=True` so the command receives no flock descriptor. The caller blocks normal cancellation signals across fork setup and the supervisor installs non-terminating handlers before restoring its inherited mask. Consequently caller/process-group cancellation cannot release serialization while a signal-ignoring guarded descendant survives. The supervisor keeps serialization until the primary command plus all adopted/orphaned descendants have exited.

That final `guard-run` behavior is a required foundation, but it is deliberately **not sufficient by itself for bootstrap**: ordinary `guard-run` completes only after the guarded process tree is gone, while successful bootstrap must leave one exact registered official-client process alive after an explicit verified detach transition. Bootstrap therefore requires a distinct reviewed primitive/state machine that preserves the same authority, cancellation and anti-escape guarantees through registration and detachment.

## Authoritative namespace

Bootstrap, generation rebind and all later Gate B readers/writers MUST use the manager-owned canonical namespace exactly as promoted by the production wrapper:

```yaml
state_root: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime
coordination_lock: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/coordination.lock
lease_record: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/lease.json
runtime_registration: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json
```

`runtime-registration.json` is the one authoritative current registration path. Bootstrap and later rebind candidates MUST be written as mode-restricted temporary files in the same directory and atomically renamed to that exact path only at commit. Controllers MUST NOT select, override, infer or create an alternative state root or registration path. Absence means that this exact registration is absent or explicitly invalidated while the bootstrap supervisor holds the canonical coordination flock and has just validated the current authoritative lease; absence in any other directory is irrelevant.

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

If a registered client, an exact live client, any mismatched/unverifiable official-client candidate, or any existing official-client session is found, this contract MUST NOT create another session. The caller must enter the ordinary registration/rebind/reuse/recovery path or explicit reconciliation path instead. Historical display/process observations are not sufficient to satisfy these preconditions.

The bootstrap supervisor MUST keep the canonical coordination flock continuously from before lease revalidation and the authoritative absence inventory through creation, registration commit and safe detach. Therefore two concurrent bootstrap callers cannot both act on the same stale absence observation: after waiting for the flock, a later supervisor must revalidate its lease, repeat the full under-lock inventory and refuse creation if the first caller has already registered or left any conflicting official-client candidate/session.

## Existing-runtime adoption — separate missing-registration transition

Create-bootstrap remains a **zero-client creation transaction**. It must never be relaxed merely because an exact client already exists. When the authoritative registration is absent but exactly one already-running exact-fenced official client is freshly proven, the reviewed `adopt-existing` transition is the separate legal path.

Adoption runs under the same current authoritative lease and continuously held canonical `coordination.lock`, but it creates no client descendants and performs no login/process/UI mutation. Its probe must cover all permitted running Docker containers, require exactly one exact client, reject any official-looking mismatched or unverifiable candidate, and prove boot identity + PID + process start ticks + exact fence + display + X11 window ownership. It hashes rather than persists the character-bearing window title and MUST NOT infer `IN_GAME` from that title. The existing bridge `PING` plus exactly one validated `player_protocol_handler`, `gameserver_game_session` and `worldmap_handler` is current-peer structural presence evidence only. A 2026-08-20 exact-peer login-screen regression still produced all three, so this signal MUST NOT promote `state=IN_GAME`; until a separately reviewed semantic/causal active-world discriminator exists, adoption state remains `UNKNOWN`. The proof also binds a stable Docker runtime locator and candidate fingerprint so later Gate B checks cannot silently reinterpret a same-number PID in another container. The complete proof is repeated before atomic registration commit and after commit; identity, uniqueness, lease or registration drift fails closed.

Adoption writes the same schema-v1 authoritative registration bound to the current lease generation, with additive adoption provenance fields (`proof_kind`, `runtime_locator`, `candidate_fingerprint`, inventory scope/count/completeness and `state_evidence`) that later adoption-aware Gate B probes must reproduce. A pre-commit failure discards only the candidate. A post-commit failure removes only the exact registration created by that adoption transaction and never stops/signals/restarts/attaches to the pre-existing client. After successful adoption, later client mutation is still a separate ordinary reuse step requiring a fresh invocation/trusted base, any required rebind, Gate B PASS and final guarded mutation lifetime.

## Exact client fence

The created client MUST match:

```yaml
version: 15.32
size: 52109920
sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
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
IDLE_REGISTERED
  |
  | a future controller acquisition may advance the lease generation
  | and therefore require the dedicated under-lock registration rebind
  v
REBIND_REQUIRED_OR_GATE_B_READY
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
- allowing foreground process-group cancellation to kill the bootstrap lock owner while mutation descendants remain;
- passing the coordination flock or lease capability into the client or helper;
- writing registration before the exact process identity is proven;
- using a registration path outside `/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json`;
- treating a mismatched or unverifiable official-client candidate as equivalent to absence;
- releasing bootstrap mutation authority before registration is durably committed and revalidated;
- claiming a process from another task/display/track;
- treating PR/task metadata as lease authority;
- manually changing registration generation fields to bypass the reviewed rebind transition.

## Bootstrap supervisor invariant

The implementation must provide an explicit controlled transition distinct from ordinary `guard-run`, for example:

```text
supervise_create_until_registered(...)
```

or an equivalent reviewed primitive whose success condition is not child exit, but verified registration of the still-running exact client followed by safe supervisor detachment.

It MUST preserve the final PR #321 anti-escape/cancellation model during the mutation phase:

- a current authoritative lease record/capability exists before the supervisor critical section;
- the supervisor acquires the canonical coordination flock and validates that lease under the flock before any decisive absence check or dispatch;
- under that continuously held flock, authoritative registration plus all-official-client candidate/session absence is freshly re-proven immediately before launch;
- only the external supervisor holds the coordination flock after dispatch;
- launched command/client/helpers receive no flock descriptor and no lease capability;
- caller/launcher exit cannot release serialization while bootstrap-owned mutation descendants remain;
- foreground process-group cancellation cannot terminate the lock-owning supervisor while any bootstrap-owned mutation descendant survives;
- daemonized/orphaned bootstrap descendants remain supervised/adopted until they are either proven to be the one registered persistent client at the safe-detach boundary or are cleaned up;
- lease/generation changes invalidate the transaction before commit/detach.

A bootstrap implementation is **not authorized by this documentation PR**. It requires its own implementation task, deterministic tests, review, exact-head CI and separately authorized real-client E2E before any live creation/login claim.

## Runtime registration record

The authoritative current record is exactly:

```text
/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json
```

Registration MUST be atomic and mode-restricted. All readers, candidate writers, committers, rebind/recovery logic and Gate B preflight MUST use this namespace/path. Required non-secret fields:

```yaml
schema_version: 1
runtime_id: track-a-canonical-live
registration_generation: <monotonic registration generation>
lease_generation: <controller lease generation that created or last rebound the registration>
registered_at: <timestamp>
boot_id_sha256: <hash>
pid: <current pid>
process_start_ticks: <current /proc starttime>
client_version: 15.32
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
display: <declared canonical display proven now>
window_identity: <non-secret current window evidence>
remote_view_endpoint: <declared endpoint or null>
remote_view_mapping: PROVEN | UNKNOWN
state: LOGIN | CHARACTER_SELECT | IN_GAME | DISCONNECTED | UNKNOWN
source_task: <bootstrap or rebind task id>
source_run: <run id>
```

The record MUST NOT contain credentials, cookies, session keys, packet payloads, framebuffer contents or raw account/character secrets.

## PID reuse and process identity

PID alone is insufficient. Positive identity requires at least:

```text
boot identity + PID + process start ticks + /proc/<pid>/exe exact size/SHA
```

Immediately before registration commit and immediately before supervisor detachment, the exact identity MUST be rechecked. The same minimum identity must be freshly rechecked by any later generation rebind.

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
- supervisor relinquishment is explicit and cannot be triggered merely by launcher/caller exit or process-group cancellation;
- canonical coordination flock is closed/released by the supervisor only after all detach checks succeed;
- canonical controller lease may then be released normally;
- client remains as the registered idle programme resource.

A detached client does not itself hold controller authority. A later controller acquisition may advance the lease generation; when it does, ordinary mutation remains disabled until the dedicated generation-rebind transition succeeds and Gate B then passes on the current generation.

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

## Post-bootstrap controller-generation rebind

Bootstrap intentionally records the creation lease generation. The next legitimate controller can receive a newer manager generation after the bootstrap controller releases its lease. This is **not** evidence that the runtime identity changed, but it is a mandatory authority mismatch that must be reconciled before Gate B current-generation equality can pass.

A reviewed generation-rebind primitive MUST run under the current Gate A authority and continuously held canonical `coordination.lock` before ordinary mutation. It MUST:

1. validate the new current controller lease/capability/generation under the flock;
2. load only the authoritative `runtime-registration.json`;
3. require that a registration exists and is structurally valid;
4. freshly prove the same boot identity, PID, process start ticks, exact version/size/SHA, required display/window/state and target uniqueness recorded by the registration;
5. fail closed if any competing, mismatched or unverifiable official-client candidate/session exists;
6. permit the old `lease_generation` to be the only authority field that differs from the current controller generation;
7. write a mode-restricted candidate preserving all proven runtime identity fields, increment `registration_generation`, set `lease_generation` to the current validated generation and atomically replace the authoritative registration;
8. re-read the committed registration and revalidate the current lease plus exact runtime identity and uniqueness before success.

The rebind transition MUST NOT launch, log in, stop, signal, attach to, inject into or otherwise mutate the client. It cannot create a missing registration, bless a different/reused PID, change the exact client fence, choose a replacement display/window identity, or resolve ambiguous second-client state. Such cases require explicit recovery or bootstrap as applicable and remain fail-closed.

This contract defines the required boundary only. It does **not** implement or authorize generation rebinding. Until a reviewed implementation is promoted, a generation mismatch disables ordinary mutation.

## Post-bootstrap reuse

Ordinary later mutation/reuse requires:

1. acquire or renew the current authoritative lease;
2. enter the final cancellation-safe reviewed supervisor critical section, acquire the canonical coordination flock and validate the lease under that flock;
3. load `/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json` only;
4. if its lease generation differs from the current validated generation, complete the dedicated fail-closed rebind under the same authority boundary; if rebind is unavailable or fails, stop;
5. after any required rebind, freshly revalidate boot/PID/start/exact fence/display/window and required mutation-relevant state, require registration `lease_generation` to equal the current validated generation, and fail closed if any competing or unverifiable official-client candidate/session is present;
6. perform mutation through the final reviewed supervisor for the complete mutation/process-tree lifetime;
7. update/invalidate the authoritative registration if process or identity-bearing state changes materially;
8. release the coordination flock only when no guarded mutation descendants remain.

After stale lease takeover, the same rebind rules apply: an older-generation registration is not self-authenticating, and no mutation is allowed until the exact unchanged runtime is freshly proven and rebound to the replacement generation.

## Evidence requirements

Bootstrap implementation cannot be promoted without deterministic non-live tests proving at least:

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
- foreground process-group cancellation with a signal-ignoring descendant cannot release the canonical flock early;
- helper child remains alive -> detach fails;
- candidate written but identity changes before commit -> abort;
- committed registration changes identity before detach -> detach fails/recovery required;
- registration commit then controller release leaves client but no mutation helper;
- persistent client receives neither flock descriptor nor lease capability;
- second bootstrap refused if a registration, exact client, mismatched/unverifiable official-client candidate, or existing official-client session already exists;
- incomplete inventory fails closed instead of being treated as absence;
- cleanup affects only owned descendants;
- no secret fields in state/log/artifacts.

A separately implemented generation-rebind primitive cannot be promoted without deterministic tests proving at least:

- older registration generation + same exact runtime + current Gate A -> atomic rebind succeeds and increments `registration_generation`;
- missing registration fails rather than creating one;
- changed boot/PID/start/fence/display/window identity fails rather than rebinding;
- competing or unverifiable official-client candidate/session fails closed;
- current lease changes during rebind aborts;
- candidate write followed by identity change before commit aborts;
- exact registration is re-read/revalidated after atomic commit;
- no client process mutation is performed by the rebind primitive.

A later controlled real-client E2E must separately prove the bootstrap transition with the exact fenced client. Test success alone does not prove a current live session.

## Explicit non-claims

This contract does not:

- implement bootstrap;
- implement generation rebinding;
- authorize launch or login now;
- authorize ad-hoc registration editing;
- declare `:98` canonical;
- prove current `6082 -> :98` mapping;
- register a PID/process/session;
- alter PR #303 runtime ownership;
- alter Track B;
- complete P0/P1/A3/A4;
- make Track A complete.

## 2026-08-19 current-client fence provenance boundary

The current public native-Linux package is fenced by size `52109920` and SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`; `15.32` is an embedded version-family token, not a claim of a more specific suffix. The superseded `15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe` binary remains admissible only as explicitly historical build-fenced evidence. Historical addresses, offsets, QMeta/vptr assumptions, serializers, helper binaries and runtime-bridge profiles are **not** promoted to the current binary by this identity update.

This fence change grants no login, credential, GUI input, gameplay, process-control, transaction or mutation authority. All ordinary ownership/admission/lease/Gate A/rebind/Gate B/bootstrap requirements remain unchanged.
