# ADR-0001: Track A canonical live runtime with authority, identity, rebind, recovery and bootstrap gates

- Status: accepted
- Date: 2026-08-16
- Task/PR: `OTC-20260815-track-a-canonical-live-runtime` / `#311`
- Supersedes: the pre-final-manager policy-v4 drafts on PR #311
- Superseded by:

## Context

Track A researches the official native Linux Tibia client on `synology-otclient-01`. A unique X11 `DISPLAY` isolates a GUI namespace; it does not create a separate Tibia Global account/session, character/world session or controller authority.

The target operating model is one reusable persistent live official-client runtime for sequential Track A work, plus task-isolated ephemeral sandboxes for experiments that do not require that runtime. Static reverse engineering, protocol reconstruction and repository work remain parallel.

Six trust transitions must remain separate:

1. **Who may mutate?** A current authoritative controller lease is required.
2. **How may one already-running exact runtime become registered when registration is absent?** A dedicated fail-closed metadata-only adoption transition is required.
3. **How may an already registered unchanged runtime cross into a newer controller lease generation?** A dedicated fail-closed registration rebind is required when generations differ.
4. **How may a stale adoption registration be reconciled when both registered PID and start identity are gone but exactly one current exact same-fence target is freshly proven?** A distinct fail-closed canonical recovery transition is required.
5. **Which existing runtime may be reused/mutated?** A current exact-runtime registration and fresh Gate B preflight are required after any required rebind/recovery.
6. **How may the first runtime be created when registration is absent and no client exists?** Initial creation is a separate fail-closed bootstrap transaction.

The final authority implementation is the manager/supervisor stack promoted through PRs #312, #313, #317, #316 and cancellation hardening PR #321, with fresh final closeout in PR #322. The initial-creation contract is `docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md`, originally promoted by PR #318 and archived by #320, then reconciled by this governance PR to the final cancellation-safe manager and the generation-rebind boundary.

## Decision

### 1. Canonical live runtime target

Track A targets at most **one canonical persistent official-client Tibia Global runtime/session** at a time unless the owner explicitly authorizes a separately isolated additional live-session experiment.

The canonical runtime is a programme resource, not a concurrently shared control surface. State-changing/invasive operations include client start/stop/restart, login/logout/character selection, keyboard/mouse/UI input, invasive attach/injection/observer setup, canonical display/remote-view rebinding, and intentional session termination or leave-running decisions.

Descriptive repository metadata is never control authority and never proves current runtime identity.

### 2. Gate A — authoritative lease plus final cancellation-safe whole-lifetime supervisor

Before any ordinary canonical mutation/reuse, the current task must hold a current lease from:

```text
.github/scripts/tibia-official-client-re-canonical-live-lease
```

The fixed authority namespace is:

```text
/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime
```

The lease record/capability proves controller authority but does not itself continuously hold the coordination flock after an `acquire` call returns. Every state-changing or invasive command must therefore enter the final reviewed supervisor critical section:

1. the supervisor opens/acquires `coordination.lock`;
2. while holding that flock it validates the current task/session token and lease generation;
3. after dispatch, only the dedicated Linux child-subreaper supervisor retains the coordination flock;
4. the guarded command is launched with `close_fds=True` and receives no coordination-flock descriptor;
5. the caller blocks normal cancellation signals across supervisor fork setup and the supervisor installs non-terminating cancellation handlers before restoring the inherited signal mask;
6. cancellation of the foreground process group therefore cannot drop `coordination.lock` while a signal-ignoring guarded descendant remains alive;
7. serialization remains until the primary command and all adopted/orphaned mutation descendants have exited;
8. only then does the supervisor close/release the flock.

PR #321 is the final cancellation-safe implementation on top of PR #316 child-subreaper supervision and PR #317 descriptor-last-close hardening. A standalone `validate`, repository task/PR metadata, manually written timestamps, a visible PID/display/socket/noVNC endpoint, or an agent assertion never authorizes mutation outside this critical section.

If the manager is unavailable, lease validation fails, or the final whole-lifetime supervisor guarantee cannot be used, ordinary canonical mutation is disabled.

### 3. Existing-runtime adoption — metadata-only registration of one exact pre-existing client

If the authoritative registration is absent but exactly one already-running exact-fenced official client is proven, bootstrap creation must not run because its zero-client precondition is false. The reviewed `adopt-existing` transition may instead create registration generation 1 while the current controller continuously owns `coordination.lock`.

Adoption must freshly prove one exact target and no competing/mismatched/unverifiable official-client candidate, including current boot identity, PID, process start ticks, exact version/size/SHA, display, X11 window ownership and a stable runtime-locator/candidate fingerprint. Window title alone never proves `IN_GAME`; an adoption registration may claim `IN_GAME` only with a current exact-peer structural discriminator, and otherwise records `UNKNOWN`. The current Kasm path uses bridge `PING` plus exactly one validated player-protocol, game-session and worldmap handler. The proof is repeated before registration commit and after commit. Lease drift, registration races or any identity/uniqueness drift abort. Before commit only the candidate file is discarded; after commit only the exact adoption-created registration may be removed on rollback. The existing client is never launched, stopped, signalled, logged in, attached to or injected into by adoption.

Adoption does not itself authorize gameplay/UI mutation. A later invocation based on merged trusted `main` must re-admit, pass Gate B (and rebind if required), and use the final guarded mutation supervisor before input.

### 4. Registration-generation rebind — fail closed before Gate B equality

A registration created by bootstrap or an earlier controller is bound to the lease generation that established or last revalidated it. A later legitimate controller `acquire` advances the manager generation. Therefore **generation mismatch is expected across sequential controller ownership and must not be solved by weakening Gate B or by ad-hoc JSON editing**.

When the authoritative registration exists but its `lease_generation` differs from the current validated controller generation, ordinary mutation remains disabled until a reviewed registration-rebind primitive completes under Gate A and the canonical flock. The rebind transition is a metadata authority transition, not client mutation and not bootstrap.

A valid rebind MUST:

1. acquire and continuously hold the canonical `coordination.lock` through the final manager/supervisor authority boundary;
2. validate the current task/session capability and current lease generation while that flock is held;
3. read only the authoritative registration at `/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json`;
4. freshly prove that every immutable/current runtime identity field still describes exactly one live official client: schema/runtime ID, current boot identity, PID, process start ticks, exact executable version/size/SHA, required display/window identity, mutation-relevant state, and required remote-view mapping;
5. perform a fail-closed inventory proving no competing, mismatched or unverifiable official-client candidate/session makes target uniqueness uncertain;
6. require that the only registration defect being repaired by this transition is the older lease generation; a missing registration, changed/reused process identity, changed exact fence, contradictory display/window/state or target ambiguity is not rebindable;
7. write a mode-restricted candidate in the authoritative state directory that preserves the proven runtime identity, increments `registration_generation`, and changes `lease_generation` only to the current validated generation;
8. atomically rename that candidate to the authoritative registration path while the same flock remains held;
9. re-read the committed record and revalidate current lease generation plus the exact live process/fence/display/window/state and uniqueness evidence before returning success.

A rebind MUST NOT launch, log in, stop, signal, attach to, inject into, replace or otherwise mutate the client. It MUST NOT fabricate a missing registration, bless a new PID, accept a different build, choose a new display merely to make evidence match, or reconcile an ambiguous second client. Those conditions fail closed into explicit recovery or the separately reviewed bootstrap path as applicable.

The reviewed canonical transition controller implements this unchanged-identity rebind path. A lease-generation mismatch keeps ordinary canonical mutation disabled until rebind succeeds.

### 5. Canonical stale-registration recovery — replace only a fully proven stale adoption identity

A registration whose PID/start identity no longer matches the current runtime is **not rebindable**. Rebind proves unchanged identity; it must never bless runtime-instance replacement. For the narrow same-boot case established by terminal PR #692, Track A uses a distinct `canonical_recovery` admission class and `stale-registration-recovery` transition. For the boot-identity discontinuity proven terminally by PR #694, a separate `canonical_boot_epoch_recovery` / `boot-epoch-registration-recovery` lifecycle may replace the prior-boot registration only after repeated current-boot singleton exact-target proof; it is not rebind and does not relax `canonical_recovery`.

A valid recovery MUST keep the existing canonical lease/capability, state root, `coordination.lock` and authoritative registration path. Under current Gate A and the continuously held flock it must require an existing fail-closed `existing_runtime_adoption_v1` registration, a newer controller generation, and a complete fresh adoption probe proving exactly one current exact target across all running Docker containers. The exact client version/size/SHA must remain unchanged.

Recovery additionally requires continuity of boot identity, canonical Docker container name, display and remote-view endpoint/mapping; both PID and process-start ticks must change; the current X11 window proof must bind the fresh PID; and the fresh candidate fingerprint must recompute from the fresh locator/PID/start/fence and differ from the old fingerprint. The complete fresh proof is repeated before commit and after commit.

Success atomically increments `registration_generation`, binds `lease_generation` to the current controller, and replaces the stale adoption runtime-instance fields with the freshly proven values while keeping `state: UNKNOWN`. If post-commit validation fails, rollback may restore the old record only when the current record is still exactly the transaction's own committed record. Any concurrent change fails closed.

Recovery MUST NOT create a second authority namespace or registration, launch/login/restart/stop/signal/attach/inject the client, access credentials, or send gameplay/UI input. It grants no mutation authority and is not Gate B. A later trusted-main invocation must re-admit and independently pass Gate B before reuse or mutation.

### 6. Gate B — authoritative current-runtime registration and fresh preflight

A current lease does not prove what process is being targeted. After any required generation rebind or canonical recovery, ordinary reuse/mutation requires the one authoritative registration record:

```text
/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json
```

All registration readers, writers, rebind/recovery logic and Gate B preflight use that exact path. Alternative state roots or registration paths are not canonical.

A positive Gate B preflight must freshly revalidate at least:

```yaml
schema_version: 1
runtime_id: track-a-canonical-live
registration_generation: <current registration generation>
lease_generation: <current validated controller generation>
boot_id_sha256: <current boot identity hash>
pid: <current pid>
process_start_ticks: <current /proc starttime>
client_version: 15.32
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
display: <current proven canonical X11 display>
window_identity: <current official-client window evidence>
remote_view_endpoint: <endpoint or null>
remote_view_mapping: PROVEN | UNKNOWN
state: LOGIN | CHARACTER_SELECT | IN_GAME | DISCONNECTED | UNKNOWN
```

PID alone is never identity. Boot identity + PID + process start ticks + exact executable fence are the minimum process identity boundary. When a display/window/state or remote-view mapping is required for the intended mutation, it must also be directly proven now.

Gate B is fail-closed if the registration is absent, stale, contradictory, malformed, still bound to another lease generation after the allowed rebind point, or fails fresh process identity/fence/display/window/state checks. It also fails closed if a competing or unverifiable official native Linux client candidate/session is present and safe target uniqueness cannot be established.

After stale lease takeover or any ordinary new controller generation, prior registration is evidence to be freshly falsified, not self-authenticating current authority. If all exact-runtime facts remain unchanged, the dedicated rebind transition may bind that verified registration to the current lease generation; otherwise mutation stays disabled.

### 7. Initial creation/bootstrap is a separate transition

Gate B governs reuse of an already registered runtime. Generation rebind governs an already registered exact runtime crossing into a newer controller lease generation. Neither may be weakened or repurposed to solve initial creation.

When no authoritative current registration exists, creation is allowed only through the separately reviewed fail-closed bootstrap contract:

```text
docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
```

The bootstrap transaction requires a current authoritative lease, then a reviewed bootstrap supervisor that acquires the canonical coordination flock and validates the lease under that flock. While continuously holding the flock it must re-prove authoritative registration absence and a fail-closed inventory of **all** official-client candidates/sessions immediately before launch, create/supervise only bootstrap-owned descendants, prove the exact client/process/display/window identity, atomically commit the authoritative registration, revalidate it, and perform an explicit safe-detach transition.

Ordinary `guard-run` is deliberately insufficient for successful bootstrap because ordinary `guard-run` releases only after the guarded process tree exits, while successful bootstrap must leave one registered persistent exact client alive after reviewed safe detachment.

Bootstrap commits the first registration bound to its creation lease generation. After safe detach and later acquisition of a newer controller lease, the runtime remains unusable for ordinary mutation until the dedicated generation-rebind transition has freshly proven the unchanged exact runtime and rebound the registration to the new current generation.

This ADR does not itself authorize any live bootstrap, rebind or recovery execution and does not authorize a live client launch/login.

### 8. Exact client fence and current non-claims

The accepted Track A official-client fence is exactly:

```yaml
version: 15.32
size: 52109920
sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
platform: official_native_linux_only
```

No current canonical runtime identity is established merely by this governance decision. Until direct evidence is produced through the applicable registration/bootstrap boundary:

```yaml
display_98_current_canonical_status: UNKNOWN
rfb_6082_current_backend_mapping: UNKNOWN
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
```

Historical observations may guide discovery but cannot satisfy Gate B, rebind, recovery or bootstrap absence/identity checks.

### 9. Ephemeral isolated runtimes

A Track A task may create a task-owned ephemeral native-Linux runtime for startup, loader, rendering, GUI, recovery-harness or instrumentation-harness experiments when its task separately authorizes that work.

Ephemeral runtimes require task-unique state/display/ports/process markers, are not the canonical registered live runtime, and may be cleaned up only by their owner. A different `DISPLAY` is a different GUI namespace, not separate Global authority. World login is not implied.

### 10. Parallel research and Track B isolation

Static reverse engineering, binary analysis, protocol reconstruction, artifact/replay analysis, evidence normalization, tooling and documentation may proceed concurrently when they do not require canonical live mutation.

Read-only live observation without Gate A is permitted only when it is demonstrably non-invasive, cannot alter process/session state and does not overlap another task's runtime ownership. Otherwise acquire current authority or do not observe.

Track B never shares Track A's canonical live runtime, authority namespace, registration, rebind transition or supervisor ownership. PR #303 runtime-owned paths/processes remain separately owned factual input and must not be stopped, attached to, signalled, reconfigured or cleaned by this governance task.

## Alternatives considered

| Alternative | Decision |
|---|---|
| Fresh logged-in client/display per agent | Rejected: multiplies sessions/recovery and a DISPLAY is not Global authority |
| Concurrent control of one persistent client | Rejected: unsafe input/process/instrumentation races |
| Repository task/PR metadata as controller lock | Rejected: not atomic authority |
| Lease-only authorization | Rejected: authority does not prove runtime identity |
| Registration-only authorization | Rejected: identity does not prove mutation authority |
| `validate` then detached/unguarded mutation | Rejected: mutation can outlive validated authority |
| Treat old `lease_generation` as current forever | Rejected: later controller generations would inherit stale authority semantics |
| Require current generation without a rebind transition | Rejected: deadlocks legitimate sequential reuse immediately after bootstrap/controller release |
| Rewrite `lease_generation` without exact-runtime proof under lock | Rejected: could bless stale/reused PID or wrong client |
| Treat exact-fence absence before locking as bootstrap authority | Rejected: stale preflight can race another bootstrap |
| Merge bootstrap into ordinary Gate B reuse/rebind | Rejected: initial creation has no pre-existing registration and needs a different supervised commit/detach transaction |
| Gate A + fail-closed rebind/recovery + Gate B for reuse, separate bootstrap for creation | Accepted |

## Consequences

- Known-good live state may be reused sequentially without multiplying Global sessions, but only after the current controller has both authority and a current-generation exact registration.
- Controller split-brain is fenced by the current lease plus final cancellation-safe supervisor-owned coordination lock.
- Target split-brain/stale-PID risk is fenced by the authoritative registration, the fail-closed rebind rules and fresh exact-runtime preflight.
- Normal controller-generation advancement no longer creates a policy deadlock: an unchanged exact runtime has one defined, narrow rebind path; any other mismatch fails closed.
- Initial creation cannot weaken Gate B or rebind and must use the reviewed bootstrap boundary.
- Live control remains serialized; inability to prove authority, identity, uniqueness or whole-lifetime serialization disables mutation.
- `:98`, `6082`, PID and session remain unknown/not registered until direct evidence.

## Validation basis

- Final cancellation-safe manager/supervisor implementation: PR #321 exact head `d5bff95997e82d4ac5180d0e9c1b85dae8a3c7dd`, merged as `8828150617d68247be2074b330f4d954e508307b`; deterministic unit `95120629666`, isolated Synology `95120629639`, fresh independent audit `95120629610` and repository `CI / Required` `95120881462` passed. Fresh terminal manager archive/ownership release: PR #322 merged as `b0fd474e34c0252220b773b2304d889821080727`.
- Bootstrap contract: PR #318 merged as `9d3b94d4f06a1eba1dacca91a9dd288e1a8af56a`, with task closeout in PR #320; this PR reconciles that contract to final PR #321/#322 semantics and defines the required post-bootstrap generation-rebind boundary without implementing live bootstrap/rebind.
- This governance PR requires a fresh post-restack independent audit, exact-head `CI / Required`, zero unresolved material review findings, protected merge, and post-merge archival/ownership release.
- Runtime E2E is `NOT_APPLICABLE` to this documentation/governance decision; no live runtime is created, registered, rebound or mutated by this PR.

## 2026-08-19 current-client fence provenance boundary

The current public native-Linux package is fenced by size `52109920` and SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`; `15.32` is an embedded version-family token, not a claim of a more specific suffix. The superseded `15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe` binary remains admissible only as explicitly historical build-fenced evidence. Historical addresses, offsets, QMeta/vptr assumptions, serializers, helper binaries and runtime-bridge profiles are **not** promoted to the current binary by this identity update.

This fence change grants no login, credential, GUI input, gameplay, process-control, transaction or mutation authority. All ordinary ownership/admission/lease/Gate A/rebind/recovery/Gate B/bootstrap requirements remain unchanged.
