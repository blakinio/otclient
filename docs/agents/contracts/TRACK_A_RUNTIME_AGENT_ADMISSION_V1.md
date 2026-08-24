# Track A Runtime Agent Admission Contract v1

```yaml
track_a_runtime_agent_admission_version: 1
track_id: official-client-re
repository: blakinio/otclient
runtime_platform: official_native_linux_only
```

## Purpose

This contract is the mandatory operational admission gate for every current and future Track A researcher before claiming, resuming, observing, creating, reusing, controlling, or mutating any official-client runtime.

It does not replace `docs/agents/TIBIA_RESEARCH_TRACKS.md`, `docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md`, or `docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md`. It converts those final governance rules into a small per-worker decision that must be made at claim/resume and re-evaluated before live runtime work.

Static repository research may proceed without a live runtime only after declaring and persisting `runtime_access: none`. Runtime work must use one of the other explicit classes below. There is no implicit or legacy runtime class.

## Mandatory reads before Track A work

A Track A worker MUST read the current trusted-base versions of:

1. `AGENTS.md`, `docs/agents/README.md` and `docs/agents/AGENTS.md`;
2. `docs/agents/TIBIA_RESEARCH_TRACKS.md`;
3. `docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md`;
4. `docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md`;
5. `docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md`;
6. the current task record plus live PR/ownership state for any runtime surface it may inspect or touch.

Stale task text, historical PR prose, a prior agent statement, or a previously working display/port/PID/session never overrides the current trusted-base contracts.

## Required admission record

At Track A task claim/resume/checkpoint, before substantial work in that worker session, persist or emit the compact admission record below. Static/no-runtime work records `runtime_access: none`. Before the first runtime-related operation, and again after any fact that can change target identity or authority, re-evaluate and re-persist the record before proceeding.

```yaml
track_id: official-client-re
runtime_access: none | read_only | ephemeral_isolated | canonical_reuse_or_mutation | canonical_bootstrap | canonical_rebind | canonical_recovery
runtime_owner_task: <task id or NOT_APPLICABLE>
runtime_namespace: <task-owned namespace, canonical namespace, or NOT_APPLICABLE>
canonical_registration: ABSENT | PRESENT | UNKNOWN | NOT_APPLICABLE
canonical_lease_generation: <integer | UNKNOWN | NOT_APPLICABLE>
registration_lease_generation: <integer | UNKNOWN | NOT_APPLICABLE>
gate_a: PASS | REQUIRED_NOT_PROVEN | NOT_APPLICABLE
generation_rebind: PASS | REQUIRED_UNAVAILABLE | REQUIRED_NOT_PROVEN | NOT_APPLICABLE
gate_b: PASS | REQUIRED_NOT_PROVEN | NOT_APPLICABLE
bootstrap: PASS | REQUIRED_UNIMPLEMENTED | REQUIRED_NOT_PROVEN | NOT_APPLICABLE
target_uniqueness: PROVEN | UNKNOWN | NOT_APPLICABLE
mutation_authorized: true | false
```

`mutation_authorized: true` is legal only for the exact cases defined below. An `UNKNOWN`, `REQUIRED_NOT_PROVEN`, `REQUIRED_UNAVAILABLE`, or `REQUIRED_UNIMPLEMENTED` value on a required gate means **REFUSE the mutation**.

The active task checkpoint is the durable admission record. It MUST NOT fabricate PASS from historical evidence merely to continue.

## Exact client fence

Every positive canonical identity, bootstrap identity, rebind identity, or current-runtime claim under this contract is fenced to the official native Linux client exactly as follows:

```yaml
client_version: 15.32
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
runtime_platform: official_native_linux_only
```

A different version, size, SHA-256, platform, unverifiable executable, or contradictory process evidence fails closed. A future build may replace this fence only through a separately reviewed trusted-base governance change with fresh exact-build evidence; a worker must not weaken or reinterpret the fence inside its own task merely to continue runtime work.

## Runtime-access classes

### 1. `none`

Use for static reverse engineering, protocol reconstruction, artifact analysis, documentation, repository tooling, evidence normalization, or any work that does not touch a live official-client runtime.

Required result:

```yaml
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
mutation_authorized: false
```

A `none` worker MUST NOT silently expand into live observation or mutation. Reclassify, re-persist and re-run admission first.

### 2. `read_only`

Use only for demonstrably non-invasive live observation that cannot alter process, window, input, login/session, network, instrumentation, or gameplay state and does not cross another task's owned runtime surface. Static repository/artifact evidence uses `none`, not `read_only`.

Required result before any live observation:

```yaml
runtime_owner_task: <current task id, or NOT_APPLICABLE only when the target is proven unowned>
runtime_namespace: <explicit non-conflicting observed namespace/target>
target_uniqueness: PROVEN
mutation_authorized: false
```

`runtime_owner_task` MUST NOT name another task, and `runtime_namespace` MUST NOT be `UNKNOWN` or `NOT_APPLICABLE`. Canonical control gates remain `NOT_APPLICABLE`; read-only observation never creates controller authority or canonical identity. If non-invasiveness, ownership, namespace, or target uniqueness cannot be proven, do not observe that surface.

### 3. `ephemeral_isolated`

Use only for a task-owned native-Linux sandbox with a verified unique namespace as required by `TIBIA_RESEARCH_TRACKS.md`.

The worker may mutate only its declared task-owned sandbox. It MUST NOT:

- call the sandbox canonical;
- write the canonical registration or canonical lease state;
- take over another task's display/process/container/state;
- infer a separate Tibia Global account/session merely from a unique X11 display;
- create a second logged-in Track A Global session unless the owner explicitly authorizes that separate live-session experiment.

`ephemeral_isolated` does not require canonical Gate A/Gate B merely to mutate its own isolated sandbox, but its ownership and namespace must be proven first.

### 4. `canonical_reuse_or_mutation`

Ordinary canonical reuse or mutation is allowed only when all of the following are freshly true:

1. **Gate A PASS** — the current task/session holds the authoritative lease and enters the final cancellation-safe supervisor critical section under `coordination.lock`;
2. the one authoritative registration exists at `/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json`;
3. if registration `lease_generation` differs from the current validated controller generation, the dedicated reviewed **generation rebind** completes under the same authority boundary;
4. **Gate B PASS** — boot identity + PID + process start ticks + exact client version/size/SHA + required display/window/state and target uniqueness are freshly revalidated, and registration generation binding matches the current controller;
5. every state-changing/invasive command stays inside the final PR #321 cancellation-safe whole-lifetime supervisor so the canonical flock survives caller/process-group cancellation and remains held through all guarded mutation descendants;
6. canonical GUI/input mutation additionally holds the reviewed canonical `input.lock` through the existing external Track A supervisor. `input.lock` only serializes GUI/input actors; it grants no lease, registration, Gate B, mutation, login, credential, gameplay or session authority. Failure to acquire or revalidate it refuses mutation. The same lock remains held from before final target validation through Control Center commit, the one physical effect and immediate reconciliation.

If any required condition is not proven now:

```yaml
mutation_authorized: false
```

Standalone lease `validate`, task metadata, a visible X11 window, a reachable port, or a historical PID/session is never sufficient.

### 5. `canonical_bootstrap`

Use only when the authoritative current registration is absent. This access class now has two reviewed missing-registration modes: `create_new` for true zero-client initial creation, and `adopt_existing` for metadata-only registration of exactly one already-running exact-fenced client. The modes are mutually exclusive and must not weaken each other.

Missing registration MUST NOT fall through to `canonical_reuse_or_mutation`, manual registration editing, or ordinary `guard-run`. Initial creation is allowed only through the separate reviewed bootstrap transition defined by `TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md`.

The documentation contract by itself is **not** a bootstrap implementation and does not authorize launch/login. Until a reviewed bootstrap implementation is promoted and the concrete live execution is separately authorized, admission must remain:

```yaml
bootstrap: REQUIRED_UNIMPLEMENTED
mutation_authorized: false
```

A future implementation must still re-prove registration absence plus the complete all-official-client candidate/session inventory under the continuously held canonical flock immediately before launch, then register and safely detach exactly as the bootstrap contract requires.


For `adopt_existing`, the transition itself is not client mutation: it MUST NOT launch, login, stop, signal, attach to, inject into or otherwise alter the client. It must run under the current authoritative lease plus continuously held canonical flock, prove exactly one exact target and zero conflicting/unverifiable candidates, bind the exact Docker runtime locator/candidate fingerprint, repeat stable boot/PID/start/fence/display/window proof around atomic registration commit, and roll back only its own registration on failure. Window title is identity evidence only. The current Kasm bridge `PING` plus one validated player-protocol, game-session and worldmap handler is also structural presence evidence only: a 2026-08-20 exact-peer login-screen regression still produced all three. It MUST NOT promote `IN_GAME`; absent a separately reviewed semantic/causal active-world discriminator the registration state is `UNKNOWN`. A successful adoption still leaves `mutation_authorized: false` for that transaction. Any later GUI/process mutation requires a fresh task checkpoint/re-admission as `canonical_reuse_or_mutation` with Gate B PASS and the final whole-lifetime supervisor.

The current task should record `bootstrap_mode: create_new | adopt_existing` when this distinction applies. The deterministic admission validator intentionally keeps both modes inside `canonical_bootstrap`; adoption is not ordinary reuse and never bypasses Gate B for subsequent mutation.

### 6. `canonical_rebind`

Use only for an already authoritative exact runtime whose registration survives unchanged but is bound to an older controller lease generation.

Rebind is a fail-closed metadata authority transition. It MUST NOT launch, login, stop, signal, attach to, inject into, or otherwise mutate the client. It must run under current Gate A + the canonical flock, freshly prove the exact unchanged runtime and target uniqueness, atomically increment `registration_generation`, set `lease_generation` to the current controller, and re-read/revalidate the committed record.

The current governance defines the rebind boundary but does not by itself provide an implementation. Until a reviewed implementation is present on the trusted base, admission is:

```yaml
generation_rebind: REQUIRED_UNAVAILABLE
mutation_authorized: false
```

Manual edits to `runtime-registration.json` are forbidden as a rebind substitute.

### 7. `canonical_recovery`

Use only when the authoritative registration exists but no longer identifies the current runtime instance: the registered PID **and** process-start ticks are stale, while a fresh reviewed adoption probe proves exactly one current exact-fenced target. Recovery is a distinct metadata reconciliation transaction. It is not generation rebind, bootstrap, adoption, Gate B, or client mutation.

Recovery MUST run under current Gate A plus the continuously held canonical `coordination.lock` and MUST reuse the one authoritative registration path. It may replace runtime-instance identity only when all of the following are freshly true:

- the old registration is `existing_runtime_adoption_v1`, remains `state: UNKNOWN`, and carries only fail-closed adoption state evidence;
- the current controller generation is newer than the registration lease generation;
- the reviewed adoption probe proves complete inventory across all running Docker containers, exactly one exact target, the accepted client version/size/SHA fence, and a self-consistent candidate fingerprint;
- both fresh PID and fresh process-start ticks differ from the registered pair;
- boot identity, canonical Docker container **name** (container instance ID may change), display, remote-view endpoint and remote-view mapping remain continuous;
- the fresh X11 window proof binds the fresh PID;
- the full fresh adoption proof is identical before commit and after commit.

Under the same authority boundary, recovery atomically increments `registration_generation`, binds `lease_generation` to the current controller and replaces only the stale runtime-instance/adoption proof fields with the freshly proven values. The recovered state remains `UNKNOWN`; recovery MUST NOT promote `IN_GAME`. A post-commit failure rolls back only when the committed record is still exactly the transaction's own record, otherwise it fails closed without overwriting concurrent state.

Recovery MUST NOT launch, login, stop, signal, attach to, inject into, restart, move, click, type into or otherwise mutate the client. It creates no new state root, registration path, lock, lease, token or authority system. `mutation_authorized` remains `false` for the recovery transaction. Any later reuse or mutation requires a fresh invocation from trusted `main`, current Gate A, any then-required authority transition, and Gate B PASS.

The reviewed implementation is the `stale-registration-recovery` operation in `.github/scripts/tibia-official-client-re-canonical-live-transition.py`. An unmerged task cannot use its own implementation or governance edits as runtime authority.

## Canonical current-state non-claims

Historical observations are discovery input only. Until fresh authoritative evidence proves otherwise, every worker must preserve:

```yaml
display_98_current_canonical_status: UNKNOWN
rfb_6082_current_backend_mapping: UNKNOWN
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
```

Therefore:

- `:98` may not be targeted as canonical merely because it exists or worked historically;
- `6082` may not be assumed to map to the canonical display merely because it is reachable or its metadata references `98`;
- a numeric PID is never canonical identity by itself;
- an observed client/session is not reusable until the authoritative registration and fresh Gate B preflight prove it.

`UNKNOWN` does not mean offline, and `NOT_REGISTERED` does not mean not running. It means mutation cannot rely on that fact.

## Cross-task and cross-track ownership

Track A workers MUST preserve current task ownership before any live operation.

- PR #303 and any replacement runtime-research task own only the runtime surfaces explicitly declared in their current task records. Other workers may consume durable evidence but MUST NOT stop, signal, attach to, reconfigure, clean, or reuse those owned surfaces.
- Track B never shares Track A's canonical lease, registration, coordination lock, bootstrap/rebind/recovery transitions, process/session, display ownership, or mutable state.
- Broad `pkill`, Docker cleanup, display cleanup, state deletion, or any target selection that can affect an unproven owner is forbidden.

If ownership or target uniqueness is ambiguous, use non-destructive repository/artifact discovery or stop that live observation/action.

## Re-admission triggers

Repeat admission before continuing when any of these changes:

- worker/session or task ownership;
- lease generation, lease holder, lease expiry, or capability;
- registration generation or registration contents;
- host boot identity;
- PID or process start ticks;
- exact client version/size/SHA;
- display/window identity or mutation-relevant state;
- competing official-client candidate/session inventory;
- runtime namespace ownership;
- trusted-base governance after restack/rebase.

A prior PASS is not standing authority after one of these facts changes.

## Evaluation examples

### PASS — static P2 worker

```yaml
runtime_access: none
mutation_authorized: false
```

The worker analyzes the exact binary and repository artifacts only after persisting the `none` admission at claim/resume.

### PASS — isolated startup experiment

```yaml
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-example
runtime_namespace: task-unique
target_uniqueness: PROVEN
mutation_authorized: true
```

The worker has proven its own unique sandbox and touches only that sandbox. It does not login merely to mirror canonical state and does not publish canonical registration.

### PASS — bounded read-only live observation

```yaml
runtime_access: read_only
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: canonical-live-runtime
target_uniqueness: PROVEN
mutation_authorized: false
```

This is legal only when the target is freshly proven unowned/non-conflicting and the observation is technically non-invasive. It still creates no canonical authority.

### REFUSE — historical display shortcut

A worker sees historical `:98`, reachable `6082`, or an old PID and attempts input/restart/login without current Gate A + required rebind + Gate B. Refuse.

### REFUSE — missing-registration shortcut

A worker sees no authoritative `runtime-registration.json` and tries ordinary `guard-run` mutation. Refuse. If no client exists, use reviewed create-bootstrap; if exactly one exact pre-existing client exists, use reviewed metadata-only adoption; ambiguous/mismatched candidates remain fail-closed.

### REFUSE — generation mismatch shortcut

A worker sees the exact old runtime but registration `lease_generation` differs, then manually edits JSON or proceeds with Gate B. Refuse; the dedicated rebind must exist and pass first.

### REFUSE — stale registered PID shortcut

A worker sees one current exact client whose PID/start pair differs from the authoritative adoption registration and tries ordinary rebind, Gate B, or a manual JSON rewrite. Refuse. Use `canonical_recovery` only after current Gate A and the full reviewed singleton exact-target proof; otherwise leave the stale registration unchanged.

### REFUSE — ambiguous read-only target

A worker cannot prove target uniqueness/ownership or the observed namespace, but tries to proceed because it intends no mutation. Refuse; use `none` for static evidence or obtain a proven non-conflicting live target first.

## Failure mode

When a required gate or target proof is unavailable/unproven, preserve the evidence, set the current runtime fact to `UNKNOWN`/the appropriate fail-closed token, persist exactly one next action, and continue only unrelated safe repository/static work. Do not weaken the gate, invent authority, or launch/login merely to make the task progress.

## 2026-08-19 current-client fence provenance boundary

The current public native-Linux package is fenced by size `52109920` and SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`; `15.32` is an embedded version-family token, not a claim of a more specific suffix. The superseded `15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe` binary remains admissible only as explicitly historical build-fenced evidence. Historical addresses, offsets, QMeta/vptr assumptions, serializers, helper binaries and runtime-bridge profiles are **not** promoted to the current binary by this identity update.

This fence change grants no login, credential, GUI input, gameplay, process-control, transaction or mutation authority. All ordinary ownership/admission/lease/Gate A/rebind/recovery/Gate B/bootstrap requirements remain unchanged.
