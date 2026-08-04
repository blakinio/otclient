# Dual Protocol and Tokio Execution Plan

Normative decision: [ADR-001](decisions/ADR-001-dual-protocol-selection-and-async-transport.md)  
Coordination ID: `OTS-20260804-native-protocol-selection`

## Purpose

This plan tells future agents how to evolve the Rust client from the current Canary-compatible, synchronous transport state toward:

- a protocol-neutral Tokio networking runtime;
- continued exact Canary compatibility;
- an independent native `protocol-oteryn` adapter;
- server-advertised automatic protocol selection;
- explicit player-action lifecycle and server authority.

It is a roadmap, not a claim that Tokio or `protocol-oteryn` is already implemented.

## Target composition

```text
physical input / UI
        ↓
semantic GameCommand
        ↓
validated session envelope
        ↓
selected protocol adapter
  ┌───────────────┴───────────────┐
  │                               │
protocol-canary              protocol-oteryn
exact compatibility          native semantic protocol
  │                               │
  └───────────────┬───────────────┘
                  ↓
protocol-neutral Tokio transport/session supervisor
                  ↓
server
```

Inbound direction:

```text
server bytes
    ↓
Tokio transport/session supervisor
    ↓
selected protocol adapter
    ↓
validated GameEvent
    ↓
single simulation writer
    ↓
immutable snapshot
    ↓
renderer / UI
```

The UI, renderer and simulation must not know which wire adapter is active.

## Stable ownership boundaries

### Client owns

- physical input and key bindings;
- semantic action creation;
- target-selection presentation;
- camera and reversible visual prediction;
- pending-action presentation;
- protocol selection from authoritative advertised capabilities;
- transport lifecycle, bounded queues and cancellation;
- decoding server events into local snapshots.

### Otheryn server owns

- legality and final result of every action;
- movement and collision;
- combat, damage, healing and conditions;
- spell requirements, mana and cooldowns;
- inventory, item movement, capacity and containers;
- corpse ownership, quick loot and transfer;
- economy, trading and persistence;
- random outcomes and authoritative ordering.

The client sends intent. It never claims damage, mana consumption, loot acquisition or inventory mutation.

## Package sequence

### Package A — protocol-neutral Tokio transport

Repository: `blakinio/otclient`  
Primary ownership: WS-R05

Goals:

- migrate `crates/transport` and game-session supervision from blocking worker I/O to an application-owned Tokio runtime;
- preserve current Canary framing, limits and fail-closed behavior;
- implement bounded full-duplex reader/writer queues;
- implement deadlines, cancellation and deterministic joined shutdown;
- prove no network operation blocks the window/render thread;
- compare latency, CPU and allocation behavior against the existing worker transport.

Non-goals:

- changing Canary opcodes or packet layouts;
- creating native Oteryn packets;
- changing Otheryn server networking;
- claiming lower physical RTT.

Completion evidence:

- partial read/write tests;
- cancellation during connect/read/write;
- timeout and reset tests;
- queue saturation and no-starvation tests;
- no task leakage;
- exact Canary compatibility tests;
- benchmark report;
- exact-head CI and independent audit.

### Package B — cross-repository native protocol contract

Repositories: `blakinio/otclient`, `blakinio/Otheryn`  
Coordination ID: `OTS-20260804-native-protocol-selection`

Before code, define:

- transport and framing;
- handshake and authentication boundary;
- capability advertisement;
- schema/versioning technology;
- action sequence and identifier rules;
- action accepted/rejected/delayed/effect-observed states;
- stable rejection reasons;
- server tick or authoritative ordering semantics;
- snapshot/delta/reconciliation behavior;
- bounded message and decompression limits;
- supported client/server matrix;
- server-first rollout and rollback.

No agent may invent these details from Canary or another client fork.

### Package C — Otheryn server producer

Repository: `blakinio/Otheryn`

Goals:

- advertise exact supported protocol candidates;
- add a native Oteryn service/profile without disrupting Canary sessions;
- decode semantic player-intent commands;
- emit authoritative domain-equivalent events;
- preserve ASIO unless separate profiling proves a networking change is needed;
- provide fixtures and integration evidence for the Rust consumer.

Recommended rollout class: server-first-safe. The server may advertise or expose the native profile while existing Canary clients continue unchanged.

### Package D — `protocol-oteryn` Rust adapter

Repository: `blakinio/otclient`  
Primary ownership: WS-R07

Create the crate only after Package B is accepted and Package C provides source evidence.

Goals:

- implement native handshake/session state;
- encode `GameCommand` into native messages;
- decode native messages into `GameEvent`;
- implement exact capability mapping;
- keep native concepts out of UI, renderer and simulation;
- fail closed on malformed or unsupported messages;
- provide golden, malformed, truncated, fuzz and replay tests.

`protocol-oteryn` must not wrap or translate through `protocol-canary`.

### Package E — automatic protocol selection

Production policy:

```text
Auto
ForceCanary(profile)   # development/test only
ForceOteryn(version)   # development/test only
```

`Auto` behavior:

1. obtain bounded authoritative candidates for the selected world/channel;
2. validate exact adapter family, version/profile, transport requirements and capabilities;
3. intersect them with locally supported candidates;
4. prefer the highest supported native Oteryn version;
5. otherwise select only an explicitly advertised supported Canary profile;
6. fail before gameplay when no compatible pair exists.

Security rules:

- one entry attempt and session bind exactly one adapter;
- no in-session switch;
- no fallback after credential handoff, authentication failure, ticket consumption, protocol violation or partial admission;
- reconnect/relog is a new attempt with fresh directory data and ticket;
- force modes are not ordinary production settings;
- fallback never introduces password authentication.

### Package F — gameplay action lifecycle

Target vocabulary:

```text
Step
StopMovement
SetAttackTarget
ClearAttackTarget
SetFollowTarget
ClearFollowTarget
CastSpell
Use
UseWith
MoveItem
QuickLoot
LootCorpse
ConfigureLootPolicy
LookAt
Say
Logout
```

Lifecycle:

```text
created
queued
encoded
written
awaiting authoritative effect
accepted / rejected / delayed / effect-observed
completed / expired / cancelled
```

TCP write completion is not gameplay success.

For Canary, expose only source-proven acknowledgements and observable authoritative effects. Native Oteryn may add explicit action identifiers and results through the coordinated contract.

## Player-action division

### Spells

The client creates a semantic cast request and pending presentation. Canary uses its source-proven text-incantation path where required. The server validates requirements, resources, cooldowns, range, line of sight and state, then applies all effects.

### Attack and follow

The client selects and presents a target. The server validates target, path, range, PvP rules and timing and computes every result.

### Loot

The client requests a corpse/position and loot mode and presents pending state. The server validates corpse ownership, range, cooldown, capacity and destination and performs every item transfer. Inventory changes only from server events.

### Item use and movement

The client creates `Use`, `UseWith` or `MoveItem` intent. The server validates identity, location, ownership, quantity, range, capacity and scripts before committing state.

## Testing matrix

Every implementation package must cover at least:

- a supported Canary pair;
- a supported native Oteryn pair when implemented;
- unsupported version/profile;
- contradictory capability advertisement;
- downgrade attempt after credential handoff;
- session replacement with stale queued actions;
- simultaneous inbound/outbound traffic;
- queue saturation and deterministic overflow behavior;
- disconnect during queued movement, spell, item and loot actions;
- exact server-authority preservation;
- no blocking network I/O on the frame thread.

## Agent start rules

Before starting any package:

1. read `AGENTS.md`, `AGENTS.override.md` and `oteryn-client/AGENTS.md`;
2. read ADR-001, `PROTOCOL_BOUNDARY.md` and this plan completely;
3. inspect all active tasks, PRs, ownership and shared-path leases;
4. reuse current domain, transport and adapter work rather than creating parallel abstractions;
5. create one bounded task, branch and draft PR;
6. state exact producer and consumer versions for cross-repository work;
7. never claim a later package is complete because an earlier architectural type exists.

## Completion definition

The direction is fully implemented only when:

- the protocol-neutral Tokio transport is merged and measured;
- Otheryn safely advertises a versioned native protocol;
- `protocol-oteryn` exists with exact producer evidence;
- automatic selection and downgrade-negative tests pass;
- Canary remains independently compatible;
- movement, attacks, spells, item actions and loot use semantic commands with server-authoritative results;
- compatible-pair integration tests, exact-head CI and independent audits pass in both repositories.
