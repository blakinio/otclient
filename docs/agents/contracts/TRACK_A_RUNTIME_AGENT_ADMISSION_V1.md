# Track A Runtime Agent Admission Contract v1

```yaml
track_a_runtime_agent_admission_version: 1
track_id: official-client-re
repository: blakinio/otclient
runtime_platform: official_native_linux_only
```

## Purpose

This contract is the mandatory operational admission gate for every current and future Track A researcher before claiming, resuming, observing, creating, reusing, controlling, or mutating any official-client runtime.

It does not replace `docs/agents/TIBIA_RESEARCH_TRACKS.md`, `docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md`, or `docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md`. It converts those final governance rules into a small per-worker decision that must be made before runtime work.

Static repository research may proceed without a live runtime only after declaring `runtime_access: none`. Runtime work must use one of the other explicit classes below. There is no implicit or legacy runtime class.

## Mandatory reads before Track A runtime work

A Track A worker MUST read the current trusted-base versions of:

1. `AGENTS.md` and `docs/agents/AGENTS.md`;
2. `docs/agents/TIBIA_RESEARCH_TRACKS.md`;
3. `docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md`;
4. `docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md`;
5. `docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md`;
6. the current task record plus live PR/ownership state for any runtime surface it may inspect or touch.

Stale task text, historical PR prose, a prior agent statement, or a previously working display/port/PID/session never overrides the current trusted-base contracts.

## Required admission record

Before the first runtime-related operation in a session, and again after any fact that can change target identity or authority, persist or emit a compact admission record with these fields:

```yaml
track_id: official-client-re
runtime_access: none | read_only | ephemeral_isolated | canonical_reuse_or_mutation | canonical_bootstrap | canonical_rebind
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

A task may store this compact record in its active checkpoint. It MUST NOT fabricate PASS from historical evidence merely to continue.

## Exact client fence

Every positive canonical identity, bootstrap identity, rebind identity, or current-runtime claim under this contract is fenced to the official native Linux client exactly as follows:

```yaml
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
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

A `none` worker MUST NOT silently expand into live observation or mutation. Reclassify and re-run admission first.

### 2. `read_only`

Use only for demonstrably non-invasive observation that cannot alter process, window, input, login/session, network, instrumentation, or gameplay state and does not cross another task's owned runtime surface.

Required result:

```yaml
mutation_authorized: false
```

Read-only evidence may discover candidates; it never creates controller authority or canonical identity. If non-invasiveness, ownership, or target uniqueness cannot be proven, do not observe that surface.

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
5. every state-changing/invasive command stays inside the final PR #321 cancellation-safe whole-lifetime supervisor so the canonical flock survives caller/process-group cancellation and remains held through all guarded mutation descendants.

If any required condition is not proven now:

```yaml
mutation_authorized: false
```

Standalone lease `validate`, task metadata, a visible X11 window, a reachable port, or a historical PID/session is never sufficient.

### 5. `canonical_bootstrap`

Use only when the authoritative current registration is absent and initial creation is actually required.

Missing registration MUST NOT fall through to `canonical_reuse_or_mutation`, manual registration editing, or ordinary `guard-run`. Initial creation is allowed only through the separate reviewed bootstrap transition defined by `TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md`.

The documentation contract by itself is **not** a bootstrap implementation and does not authorize launch/login. Until a reviewed bootstrap implementation is promoted and the concrete live execution is separately authorized, admission must remain:

```yaml
bootstrap: REQUIRED_UNIMPLEMENTED
mutation_authorized: false
```

A future implementation must still re-prove registration absence plus the complete all-official-client candidate/session inventory under the continuously held canonical flock immediately before launch, then register and safely detach exactly as the bootstrap contract requires.

### 6. `canonical_rebind`

Use only for an already authoritative exact runtime whose registration survives unchanged but is bound to an older controller lease generation.

Rebind is a fail-closed metadata authority transition. It MUST NOT launch, login, stop, signal, attach to, inject into, or otherwise mutate the client. It must run under current Gate A + the canonical flock, freshly prove the exact unchanged runtime and target uniqueness, atomically increment `registration_generation`, set `lease_generation` to the current controller, and re-read/revalidate the committed record.

The current governance defines the rebind boundary but does not by itself provide an implementation. Until a reviewed implementation is present on the trusted base, admission is:

```yaml
generation_rebind: REQUIRED_UNAVAILABLE
mutation_authorized: false
```

Manual edits to `runtime-registration.json` are forbidden as a rebind substitute.

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
- Track B never shares Track A's canonical lease, registration, coordination lock, bootstrap/rebind transition, process/session, display ownership, or mutable state.
- Broad `pkill`, Docker cleanup, display cleanup, state deletion, or any target selection that can affect an unproven owner is forbidden.

If ownership or target uniqueness is ambiguous, use non-destructive discovery or stop that live action.

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

The worker analyzes the exact binary and repository artifacts only.

### PASS — isolated startup experiment

```yaml
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-example
runtime_namespace: task-unique
mutation_authorized: true
```

The worker has proven its own unique sandbox and touches only that sandbox. It does not login merely to mirror canonical state and does not publish canonical registration.

### REFUSE — historical display shortcut

A worker sees historical `:98`, reachable `6082`, or an old PID and attempts input/restart/login without current Gate A + required rebind + Gate B. Refuse.

### REFUSE — missing-registration shortcut

A worker sees no authoritative `runtime-registration.json` and tries ordinary `guard-run` launch. Refuse; initial creation belongs to bootstrap.

### REFUSE — generation mismatch shortcut

A worker sees the exact old runtime but registration `lease_generation` differs, then manually edits JSON or proceeds with Gate B. Refuse; the dedicated rebind must exist and pass first.

### Boundary — read-only evidence

A worker may use a bounded non-invasive discriminator outside another task's owned surface to establish a current FACT/UNKNOWN boundary. That observation still does not authorize later mutation; mutation requires a new admission decision.

## Failure mode

When a required gate is unavailable or unproven, preserve the evidence, set the current runtime fact to `UNKNOWN`/the appropriate fail-closed token, persist exactly one next action, and continue only unrelated safe repository/static work. Do not weaken the gate, invent authority, or launch/login merely to make the task progress.
