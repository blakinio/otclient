# Tibia research track isolation

```yaml
tibia_research_tracks_policy_version: 6
```

This contract is mandatory for all current and future official-Tibia research in `blakinio/otclient`.

## Repository boundary

All active coordination, code, scripts, workflows, task state, reports, evidence indexes and continuation state for both tracks live only in:

```text
blakinio/otclient
```

For these tracks, do not search, read, fetch, cite, reference, mutate or depend on `blakinio/Oteryn-Platform`, historical Oteryn branches, Oteryn runners, Oteryn containers or Oteryn state directories. The material historical evidence needed for normal continuation has already been imported/indexed into this repository.

If a detail is absent from `blakinio/otclient`, classify it as `UNKNOWN` and recover/research it inside the appropriate OTClient track. Do not reopen Oteryn as a shortcut.

Historical provenance strings already committed in migration reports may remain as archival text; they are not active research inputs.

## Linux-only client/runtime rule

Both research tracks are **Linux-client-only**.

Allowed runtime/client subjects:

```text
Track A: official Linux Tibia client only
Track B: Linux build/runtime of blakinio/otclient only
```

Workers must not use, launch, install, instrument, analyze, compare against, or substitute any Windows, macOS, Android, iOS, browser/web, Wine/Proton-wrapped Windows, or other non-native-Linux client/runtime for these programmes.

Non-Linux client behavior, binaries, offsets, packet behavior, screenshots, dumps, runtime observations or compatibility results are not admissible evidence for either track. Do not use another platform as a fallback when the Linux client/runtime is unavailable; classify the Linux-dependent work as `WAITING`, `BLOCKED`, or `UNKNOWN` as appropriate and continue other safe Linux/repository work.

Cross-platform source code may be read only when it is part of the same `blakinio/otclient` repository and is necessary to understand shared implementation, but any runtime/compatibility claim for these tracks must be proven on Linux. Do not broaden a Linux-only task into cross-platform support work.

## Track A — official client reverse engineering

```yaml
track_id: official-client-re
alias: OTCLIENT-TIBIA-RE
subject: official Linux Tibia client
objective: structurally analyze the official Linux client runtime and protocol/game-state surface
canonical_prompt: docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
repository: blakinio/otclient
runner: synology-otclient-01
runtime_platform: native_linux_only
```

Track A owns research whose subject is the official Linux Tibia client itself, including:

- official-client login/session recovery needed to establish the Linux research runtime;
- decoded GameState/worldmap/player/inventory/container/creature state;
- inbound/outbound protocol handlers and message builders;
- native official-client actions and structural before/after proof;
- stable official-client runtime bridge/instrumentation;
- OTBM-relevant structural extraction from official-client state;
- exact-version hashes, relocation profiles and protocol/action catalogues.

Track A must not modify or take over Track B's OTClient-to-Global lab, workflow, branch, PR, containers or mutable state.

## Track A canonical live-runtime model

Track A distinguishes **one canonical persistent live official-client runtime** from **task-isolated ephemeral sandboxes**. The architecture decision is `docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md`.

A unique X11 `DISPLAY` isolates a virtual X server, windows, focus, screenshots, GUI automation and process-control namespace. It does **not** create a separate Tibia Global account/session, character/world session or controller authority.

By default there is at most **one canonical persistent official-client Tibia Global runtime/session** for Track A at a time. It is a programme resource that may be reused sequentially; mutation control remains exclusive.

### Six distinct transitions

Do not collapse controller authority, existing-runtime adoption, registration-generation rebind, stale-registration recovery, exact-runtime Gate B and first creation.

#### Gate A — authoritative lease and final cancellation-safe whole-lifetime supervisor

The current task must first hold a current lease from:

```text
.github/scripts/tibia-official-client-re-canonical-live-lease
```

using the fixed canonical authority namespace:

```text
/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime
```

Repository task files, PR bodies/comments, manually written timestamps, a visible display/PID/socket/noVNC endpoint, or an agent statement are discovery metadata only. They never substitute for the authoritative lease.

A successful lease `acquire` call does not mean the coordination flock remains continuously held after that call returns. Every ordinary canonical state-changing or invasive command must execute through the final reviewed supervisor path (`guard-run`, or a later reviewed equivalent preserving the same semantics):

1. acquire `coordination.lock`;
2. validate the current task/session token and lease generation while that flock is held;
3. dispatch so only the dedicated Linux child-subreaper supervisor retains the coordination flock;
4. start the guarded command with `close_fds=True`, so the command receives no flock descriptor;
5. block normal cancellation signals across the supervisor fork setup window and install non-terminating handlers in the lock-owning supervisor before restoring its signal mask;
6. keep serialization even when a foreground process-group cancellation kills the caller but a guarded descendant ignores that cancellation;
7. retain the flock through the entire primary command plus all adopted/orphaned mutation descendants;
8. release only after the complete guarded mutation tree is gone.

These are the final PR #321 cancellation-safe semantics, built on PR #316 child-subreaper supervision and PR #317 descriptor-last-close hardening and freshly archived by PR #322. Standalone `validate` is preflight evidence only and never authorizes detached or otherwise unguarded mutation.

If the manager is unavailable, lease validation fails, or the final supervisor whole-lifetime guarantee cannot be used, canonical mutation is disabled.

#### Existing-runtime adoption — missing registration with one exact pre-existing client

When the authoritative registration is absent **and exactly one already-running exact-fenced official client exists**, create-bootstrap is the wrong transition because its zero-client absence precondition is false. A reviewed existing-runtime adoption transition may instead create the first registration without launching, logging in, stopping, signalling, attaching to, injecting into or otherwise mutating that client.

Adoption is a metadata authority transaction. It requires current Gate A authority plus the continuously held canonical `coordination.lock`; fresh fail-closed inventory of all permitted official-client candidate/session evidence; exactly one exact client; boot/PID/start/exact-fence/display/window proof; a persisted runtime-locator/candidate fingerprint; and repeated stable proof before and after atomic registration commit. The character-bearing window title is hashed identity context only and cannot prove gameplay state. Bridge `PING` plus exactly one validated `player_protocol_handler`, `gameserver_game_session` and `worldmap_handler` is current-peer structural lifecycle evidence only and MUST NOT by itself promote `state: IN_GAME`. A 2026-08-20 exact-peer login-screen regression still produced all three validated objects. Until a separately reviewed semantic/causal discriminator proves active world state, adoption records `UNKNOWN`. Ambiguity, a mismatched/unverifiable candidate, registration race, lease change or identity drift fails closed. A post-commit failure removes only the adoption-created registration when it is still byte-for-byte the transaction's own record; it never kills or modifies the pre-existing client.

A successful adoption creates identity evidence, not GUI/gameplay authority. Before any later input or process mutation, a consumer must re-admit from trusted `main`, use `canonical_reuse_or_mutation`, satisfy any required rebind, pass Gate B on the adopted registration and keep the actual mutation inside the final cancellation-safe supervisor.

#### Registration generation rebind — fail closed before Gate B

The authoritative registration is bound to the lease generation that created or last revalidated it. A later legitimate controller acquisition advances the manager generation. Therefore a registration whose exact runtime still exists can require a **dedicated generation-rebind transition** before ordinary reuse.

When the registration exists but `lease_generation` differs from the current validated controller generation, ordinary mutation is disabled until a reviewed rebind primitive completes while the canonical coordination flock remains held under Gate A. The rebind must freshly prove the same exact live runtime and target uniqueness, then atomically change only the authority binding while preserving the proven runtime identity.

A rebind must prove at least:

```yaml
registration_path: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json
schema_version: 1
runtime_id: track-a-canonical-live
previous_lease_generation: <older registered generation>
current_lease_generation: <current validated generation>
boot_id_sha256: <current boot identity hash equal to registration>
pid: <current pid equal to registration>
process_start_ticks: <current start ticks equal to registration>
client_version: 15.32
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
display_window_state: freshly_revalidated
target_uniqueness: proven
competing_or_unverifiable_official_client_candidates: 0
```

Under the same continuously held flock, the rebind writes a mode-restricted candidate, increments `registration_generation`, sets `lease_generation` to the current validated generation, atomically replaces the authoritative registration, then re-reads and revalidates it plus the exact live runtime before success.

Rebind is not client mutation and must not launch, log in, stop, signal, attach to or inject into the client. It cannot create a missing registration, bless a new/reused PID, accept a changed fence, repair contradictory display/window/state evidence or reconcile an ambiguous second official client. Any such condition fails closed into explicit recovery/bootstrap as applicable. Ad-hoc manual editing of `runtime-registration.json` is never a substitute.

The reviewed canonical transition controller implements this unchanged-identity rebind path. A generation mismatch still keeps ordinary canonical mutation disabled until that reviewed rebind succeeds.

#### Canonical stale-registration recovery — exact singleton replacement without client mutation

When an authoritative adoption registration exists but its registered PID **and** process-start ticks no longer identify the current singleton exact client, ordinary rebind is the wrong transition: rebind must preserve runtime identity. The only reviewed reconciliation path is `canonical_recovery` / `stale-registration-recovery`.

Recovery runs under current Gate A and the same canonical coordination flock, reads/writes only the authoritative `runtime-registration.json`, and requires the reviewed adoption probe to prove a complete all-running-Docker inventory with exactly one current target on the accepted exact fence. It additionally requires continuity of host boot identity, canonical container name, display, remote-view endpoint/mapping, a fresh window proof bound to the fresh PID, and a recomputed changed candidate fingerprint. Both PID and start ticks must be replaced together. Any fence, boot, namespace, display, endpoint, mapping, uniqueness, state, fingerprint, lease or proof drift fails closed.

The proof is repeated before and after atomic commit. Success increments `registration_generation`, binds the record to the current lease generation and persists only the freshly proven adoption identity while keeping state fail-closed `UNKNOWN`. Post-commit failure rolls back the exact transaction-owned record only. Recovery never launches, logs in, restarts, signals, attaches to, injects into or sends input to the client, and never grants gameplay or mutation authority. A later consumer must re-admit and pass Gate B separately.

#### Gate B — authoritative exact-runtime registration and fresh preflight

A current lease proves who may control; it does not prove what live process is canonical. After any required generation rebind or canonical recovery, ordinary reuse/mutation requires the one authoritative current registration:

```text
/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json
```

All Gate B readers/writers/rebind/recovery logic use that exact path. Alternative roots or registration files are not canonical.

Immediately before ordinary reuse/mutation, the controller must freshly prove the registered process at least by:

```yaml
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

PID alone is insufficient; boot identity + PID + process start ticks + exact executable fence are the minimum process identity boundary. Required display/window/state/mapping facts must be proven for the mutation being attempted.

Registration is evidence, not authority. Gate B fails closed when the record is missing, malformed, stale, contradictory, still tied to a different lease generation after the rebind point, or does not match fresh process/fence/display/window/state evidence. It also fails closed when a competing or unverifiable official native Linux client candidate/session exists and unique safe targeting cannot be proven.

After stale lease takeover or any normal new controller generation, the prior registration must be freshly falsified under replacement authority. If all exact-runtime facts remain unchanged, only the dedicated rebind transition may bind it to the current generation. The previous controller's registration is never self-authenticating authority.

#### Initial creation/bootstrap — separate fail-closed transition

When no authoritative registration exists, **do not weaken Gate B**, do not use generation rebind, and do not treat an earlier absence probe as launch authority. Initial creation is governed only by:

```text
docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
```

The bootstrap contract requires a current lease, then a reviewed bootstrap supervisor that acquires the canonical coordination flock and validates the lease under that flock. While continuously holding the flock it re-proves absence of the authoritative registration and performs a fresh fail-closed inventory of **all** official-client candidates/sessions immediately before launch. It then owns creation descendants, proves exact process/fence/display/window identity, atomically commits the authoritative registration, revalidates it, and performs explicit safe detach.

Ordinary `guard-run` is not a bootstrap safe-detach primitive: ordinary `guard-run` holds serialization until its process tree is gone, while successful bootstrap must leave one exact registered client alive after the explicit safe-detach boundary.

Bootstrap binds the first registration to its creation lease generation. A later controller generation must perform the dedicated under-lock rebind before Gate B current-generation equality can pass for sequential reuse.

The bootstrap contract does not itself implement or authorize client launch/login. A live creation/login execution requires its own implementation, deterministic validation and separately authorized runtime execution.

### Exact fence and current non-claims

Track A's current exact official-client fence is:

```yaml
version: 15.32
size: 52109920
sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
platform: official_native_linux_only
```

Historical runtime evidence does not establish current canonical identity. Until direct Gate B/bootstrap evidence proves otherwise:

```yaml
display_98_current_canonical_status: UNKNOWN
rfb_6082_current_backend_mapping: UNKNOWN
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
```

No mutation may treat `:98`, `6082`, a PID or a session as canonical merely because it existed or worked historically.

### Ephemeral isolated runtime

A Track A task may create a task-owned ephemeral native-Linux runtime for startup, loader, rendering, GUI, recovery-harness, instrumentation-harness or similar experiments when that task authorizes it.

Ephemeral runtimes use task-unique namespaces:

```yaml
runtime_class: ephemeral_isolated
container_names: unique per track/task when used
named_volumes: unique per track/task when used
state_directory: unique per task
display: unique per task when X11 is used
loopback_ports: unique per task
process_ownership_marker: task-specific where technically available
remote_view_endpoint: task-specific when provided
runtime_platform: native_linux_only
```

An ephemeral runtime is not the canonical registered live session. World login is not implied and should not be performed merely to mirror canonical state. Its owner may clean up only its own sandbox.

### Parallel Track A research

Static reverse engineering, binary analysis, protocol reconstruction, artifact/replay analysis, evidence normalization, tooling and documentation may proceed concurrently without canonical live control.

Read-only live observation without Gate A is allowed only when it is demonstrably non-invasive, cannot alter process/session state and does not overlap another task's owned runtime surface. If those conditions cannot be proven, acquire current authority or do not observe.

A second logged-in Track A Global session is not created merely because another task has a unique display. A genuinely independent additional live-session experiment requires explicit owner authorization and a separately declared safety/ownership boundary.

## Track B — OTClient to Tibia Global compatibility

```yaml
track_id: otclient-global-login
alias: OTCLIENT-GLOBAL-LOGIN
subject: native Linux build/runtime of this blakinio/otclient fork
objective: make this Linux OTClient authenticate to and enter official Tibia Global
canonical_pr: 284
active_branch_while_pr_open: feat/OTC-20260813-tibia-global-login-lab
active_task_while_pr_open: docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md
repository: blakinio/otclient
runner: synology-otclient-01
runtime_platform: native_linux_only
```

While PR #284 remains active, the Track B task is intentionally resolved from that exact PR-local branch/path rather than falsely assumed to exist on `main`. Always verify the live PR head before use. After #284 becomes terminal, resolve Track B from the resulting `main` task/archive or explicitly recorded replacement PR/task.

Track B owns compatibility work whose subject is this repository's native Linux OTClient, including:

- HTTP login/session handoff into Linux OTClient;
- OTClient 15.32 feature/version compatibility required for Global login;
- OTClient game-server connection and login packet compatibility;
- OTClient parser/schema compatibility required for world entry;
- structural OTClient callbacks proving login/pending/enter/start;
- minimal lab-only compatibility experiments needed to establish world entry.

Track B must not claim the `OTCLIENT-TIBIA-RE` alias, must not become the canonical official-client reverse-engineering lane, and must not modify or take over Track A's official-client runtime/bridge/worldmap tasks or mutable state.

## Runtime isolation on the shared runner

Both tracks may use `synology-otclient-01`, but shared runner hardware does not imply shared runtime ownership. The runner/runtime used for these experiments must remain native Linux.

For task-owned ephemeral runtimes, every live task must declare and verify its own unique namespace before mutation or process control:

```yaml
container_names: unique per track/task when used
named_volumes: unique per track/task when used
state_directory: unique per track/task
display: unique per track/task when X11 is used
loopback_ports: unique per track/task
process_ownership_marker: task-specific where technically available
runtime_platform: native_linux_only
```

The Track A canonical live runtime is the deliberate exception to per-task state/display uniqueness: it is a persistent programme resource governed by Gate A + any required generation rebind + Gate B for reuse and by the separate bootstrap transaction for first creation. Its runtime identifiers may remain stable across sequential controller tasks; **control ownership never does**.

Track B never shares Track A's canonical live runtime, lease/token, `coordination.lock`, runtime registration, rebind transition, bootstrap supervisor or mutable state.

An agent may stop, restart, remove, clean, attach to, inject into, signal or reconfigure only processes/containers/displays/ports/state that its own task explicitly owns. For the Track A canonical live runtime, ordinary action additionally requires Gate A, any required rebind and Gate B to pass now, and mutation to stay under the final cancellation-safe supervisor for its whole process-tree lifetime. Initial creation requires the bootstrap contract instead.

Never use broad `pkill`, Docker cleanup, shared display cleanup or state deletion that can affect another task/track. If ownership, identity, authority or target uniqueness is ambiguous, stop the action and choose non-destructive discovery.

PR #303 runtime-owned paths/processes remain separately owned. Track A canonical-live governance may consume its durable evidence only within the recorded factual boundary and must not mutate its runtime surface.

## Path and PR isolation

One task, one branch, one worktree and one PR remains the default. Each track must declare exact `owned_paths`.

Cross-track edits are forbidden unless a dedicated coordination task explicitly owns the shared path. A normal Track A worker must not edit Track B task/workflow/lab paths; a normal Track B worker must not edit Track A prompt/bridge/worldmap/runtime-analysis paths.

Shared governance/index paths may be edited only by a dedicated coordination task after overlap inspection.

## Evidence sharing contract

The tracks may share only promoted repository-owned contracts/evidence, never mutable runtime ownership.

Allowed examples:

- exact official Linux client version/hash already recorded in an OTClient report;
- a version-fenced Linux protocol fact promoted into a repository-owned report/tool;
- a Linux OTClient parser incompatibility recorded by Track B and consumed as a hypothesis by another OTClient task;
- stable read-only helper tooling with explicit ownership and interface.

Before consuming cross-track evidence, verify its exact version/claim boundary and that it was established on the Linux runtime required by this contract. Do not treat another track's live container, active session, transient PID, heap address, socket, display or secret-bearing handoff as shared state.

Within Track A, the canonical runtime's mutable process/session state is not generic concurrently owned evidence merely because several workers can observe repository metadata about it.

## Coordination rule

If both tracks are active simultaneously:

1. preserve both as independent tasks/PRs;
2. verify disjoint `owned_paths` and runtime namespaces; Track A's canonical programme resource is governed only by its authority/rebind/identity/bootstrap gates and is never Track B state;
3. verify both are using only native Linux client/runtime targets;
4. do not reassign one track's task to the other;
5. do not merge their objectives into a single worker context;
6. checkpoint only track-local findings in the owning task;
7. promote genuinely reusable facts through a deliberate repository-owned report/contract;
8. resolve any overlap before mutation.

A worker discovering a scope collision or a non-Linux runtime path must stop the conflicting action, record the condition, and continue only with work inside its own declared Linux ownership.

## Current lane mapping

At the time this contract was created:

```text
Track A / official-client-re:
  alias: OTCLIENT-TIBIA-RE
  client/runtime: official native Linux Tibia client only
  canonical prompt: docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  imported state: docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md
  canonical authority root: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime
  canonical registration: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json
  bootstrap contract: docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  supporting lanes include official-client runtime/bridge/worldmap work as live state determines

Track B / otclient-global-login:
  alias: OTCLIENT-GLOBAL-LOGIN
  client/runtime: native Linux blakinio/otclient only
  PR: #284
  branch while active: feat/OTC-20260813-tibia-global-login-lab
  task on that branch: docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md
  owned implementation: tools/tibia-global-login-lab/** and .github/workflows/tibia-global-login-lab.yml
```

Revalidate exact live PR/task state on every continuation, but preserve the repository boundary, Linux-only rule, Track A Gate A/rebind/recovery/Gate B/bootstrap separation and Track B isolation unless the owner explicitly changes them.

## 2026-08-19 current-client fence provenance boundary

The current public native-Linux package is fenced by size `52109920` and SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`; `15.32` is an embedded version-family token, not a claim of a more specific suffix. The superseded `15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe` binary remains admissible only as explicitly historical build-fenced evidence. Historical addresses, offsets, QMeta/vptr assumptions, serializers, helper binaries and runtime-bridge profiles are **not** promoted to the current binary by this identity update.

This fence change grants no login, credential, GUI input, gameplay, process-control, transaction or mutation authority. All ordinary ownership/admission/lease/Gate A/rebind/recovery/Gate B/bootstrap requirements remain unchanged.
