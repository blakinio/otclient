# Tibia research track isolation

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

Every live task must declare and verify its own unique namespace before mutation or process control:

```yaml
container_names: unique per track/task
named_volumes: unique per track/task
state_directory: unique per track/task
display: unique per track/task when X11 is used
loopback_ports: unique per track/task
process_ownership_marker: task-specific where technically available
runtime_platform: native_linux_only
```

An agent may stop, restart, remove, clean, attach to, inject into, signal or reconfigure only processes/containers/displays/ports/state that its own task explicitly owns. Never use broad `pkill`, Docker cleanup, shared display cleanup or state deletion that can affect the other track.

Before any destructive or invasive runtime action, verify the target belongs to the current task. If ownership is ambiguous, stop that action and choose a non-destructive discovery method.

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

## Coordination rule

If both tracks are active simultaneously:

1. preserve both as independent tasks/PRs;
2. verify disjoint `owned_paths` and runtime namespaces;
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
  supporting lanes include official-client runtime/bridge/worldmap work as live state determines

Track B / otclient-global-login:
  alias: OTCLIENT-GLOBAL-LOGIN
  client/runtime: native Linux blakinio/otclient only
  PR: #284
  branch while active: feat/OTC-20260813-tibia-global-login-lab
  task on that branch: docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md
  owned implementation: tools/tibia-global-login-lab/** and .github/workflows/tibia-global-login-lab.yml
```

Revalidate exact live PR/task state on every continuation, but preserve the track boundary and Linux-only rule above unless the owner explicitly changes them.
