# Dual Protocol and Tokio Execution Plan

Normative decision: [ADR-001](decisions/ADR-001-dual-protocol-selection-and-async-transport.md)  
Game-entry boundary: [Oteryn Platform, Game Gateway and gameplay protocol selection](PLATFORM_GATEWAY_GAME_ENTRY.md)  
Coordination ID: `OTS-20260804-native-protocol-selection`

## Purpose

This plan tells future agents how to evolve the Rust client from the current Canary-compatible, synchronous transport state toward:

- a protocol-neutral Tokio networking runtime;
- continued exact Canary compatibility;
- reuse of the existing Oteryn Identity, Game Login Ticket, World Registry and Game Gateway chain;
- an independent native `protocol-oteryn` adapter;
- authoritative automatic protocol selection;
- explicit player-action lifecycle and server authority.

It is a roadmap, not a claim that Tokio, native protocol advertisement, automatic selection or `protocol-oteryn` is already implemented.

## Existing game-entry chain

The Oteryn login path is not one generic login server and must not be recreated in the client:

```text
Rust client
  -> system browser
  -> Oteryn Identity / OAuth Authorization Code + PKCE
  -> short-lived OAuth bootstrap with game:ticket scope
  -> one-time opaque Game Login Ticket
  -> Oteryn Game Gateway
  -> private atomic ticket redeem
  -> authoritative character/world context and World Registry route
  -> Game Session issuance
  -> Otheryn game server
```

`Oteryn Identity`, the Game Login Ticket APIs, World Registry and the separately deployable Go Game Gateway are owned by `blakinio/Oteryn-Platform`.

The existing Gateway JSON `protocol_version: 1` is the Gateway login API version. It is not a Canary or native Oteryn gameplay profile. Future agents must use separate concepts for Gateway API version, Game Session contract version, gameplay adapter family, gameplay profile/version and gameplay capabilities.

## Target composition

Game entry and adapter selection:

```text
Oteryn Identity / Game Login Ticket
        ↓
Oteryn Game Gateway / World Registry
        ↓
authoritative world, character, Game Session and protocol-selection data
        ↓
client validates and binds one exact adapter/profile to the entry attempt
```

Gameplay outbound:

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
Otheryn game server
```

Gameplay inbound:

```text
Otheryn bytes
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

### Rust client owns

- loopback callback, PKCE and transient bootstrap attempt lifecycle;
- Game Login Ticket and Gateway request handling without persistence or logging of bearer material;
- bounded validation and presentation of authoritative characters/worlds;
- local supported adapter/profile set;
- adapter selection according to the accepted three-repository contract;
- physical input and semantic player-intent creation;
- target-selection presentation;
- camera and reversible visual prediction;
- pending-action presentation;
- transport lifecycle, bounded queues and cancellation;
- decoding server events into local snapshots.

### Oteryn Platform and Game Gateway own

- reusable Identity credentials, browser authentication, MFA and security policy;
- OAuth Authorization Code + PKCE and `game:ticket` bootstrap scope;
- Identity-to-game-account binding;
- one-time Game Login Ticket issuance, revocation generation and atomic consume state;
- World Registry and authoritative account-authorized character/world routing;
- Gateway login orchestration and Game Session issuance;
- the future authoritative gameplay protocol candidate/session-binding producer contract.

Gateway never trusts client-supplied account ownership, character ownership or world routing.

### Otheryn server owns

- Game Session validation and consumption;
- acceptance of only a profile allowed for that session;
- legality and final result of every action;
- movement and collision;
- combat, damage, healing and conditions;
- spell requirements, mana and cooldowns;
- inventory, item movement, capacity and containers;
- corpse ownership, quick loot and transfer;
- economy, trading and persistence;
- random outcomes and authoritative ordering;
- native gameplay protocol production after its producer package is implemented.

The client sends intent. It never claims damage, mana consumption, loot acquisition or inventory mutation.

## Package sequence

### Package A — protocol-neutral Tokio transport

Repository: `blakinio/otclient`  
Primary ownership: WS-R05  
May start now: **yes**

Goals:

- migrate `crates/transport` and game-session supervision from blocking worker I/O to an application-owned Tokio runtime;
- preserve current Gateway, Game Session and Canary behavior;
- preserve current Canary framing, limits and fail-closed behavior;
- implement bounded full-duplex reader/writer queues;
- implement deadlines, cancellation and deterministic joined shutdown;
- prove no network operation blocks the window/render thread;
- compare latency, CPU and allocation behavior against the existing worker transport.

Non-goals:

- changing OAuth, ticket or Gateway APIs;
- changing Canary opcodes or packet layouts;
- creating native Oteryn packets;
- implementing automatic adapter selection;
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

Launchable prompt:

- `docs/agents/prompts/OTC2_TOKIO_TRANSPORT_AGENT.md`

### Package B — exact three-repository native protocol contract

Repositories:

- `blakinio/Oteryn-Platform`;
- `blakinio/Otheryn`;
- `blakinio/otclient`.

Coordination ID: `OTS-20260804-native-protocol-selection`  
May start now: **yes**

Before runtime code, define:

- how Platform/Gateway obtains authoritative world protocol candidates from configuration and Otheryn support;
- whether the client offers supported candidates, Gateway returns candidates, or a dedicated negotiation selects one;
- how the final exact adapter/profile/capabilities are bound to the Game Session;
- distinct Gateway API, Game Session and gameplay protocol versions;
- transport and framing;
- handshake and authentication boundary;
- schema/versioning technology;
- capability advertisement;
- action sequence and identifier rules;
- action accepted/rejected/delayed/effect-observed states;
- stable rejection reasons;
- server tick or authoritative ordering semantics;
- snapshot/delta/reconciliation behavior;
- bounded message and decompression limits;
- supported client/Platform/Gateway/Otheryn matrix;
- server-first rollout and rollback;
- ambiguous failure and downgrade behavior.

No agent may invent these details from Canary or another client fork.

The current Gateway v1 login contract does not provide source-proven native gameplay candidates. Package B must preserve that truth until the Platform/Gateway producer extension exists.

Launchable prompt:

- `docs/agents/prompts/OTS_NATIVE_PROTOCOL_CONTRACT_AGENT.md`

### Package C — Oteryn Platform and Game Gateway protocol-candidate producer

Repository: `blakinio/Oteryn-Platform`  
Depends on: Package B  
May start now: **no**

Goals:

- extend the accepted public/private contracts without changing Identity ownership;
- obtain or maintain authoritative adapter/profile/capability configuration per world/channel;
- include the exact accepted protocol-selection data in the Gateway game-entry flow;
- bind the final exact adapter/profile/capabilities to Game Session authorization;
- preserve one-time ticket and ambiguous redeem semantics;
- preserve fail-closed routing, rate limits, no-store/no-cache and secret redaction;
- provide exact contract fixtures for Otheryn and the Rust client.

Non-goals:

- gameplay packet production;
- client adapter implementation;
- replacing World Registry or Game Gateway;
- sending OAuth tokens to Otheryn;
- production activation.

Recommended rollout class: disabled server-first-safe producer extension.

### Package D — Otheryn native gameplay producer and session enforcement

Repository: `blakinio/Otheryn`  
Depends on: Packages B and C  
May start now: **no**

Goals:

- consume the accepted Game Session profile/capability binding;
- advertise or confirm exact supported native protocol profiles through the accepted producer path;
- add a native Oteryn service/profile without disrupting Canary sessions;
- reject profile/world/character/session mismatches;
- decode semantic player-intent commands;
- emit authoritative domain-equivalent events;
- preserve ASIO unless separate profiling proves a networking change is needed;
- provide fixtures and integration evidence for the Rust consumer.

Recommended rollout class: disabled server-first-safe producer.

### Package E — `protocol-oteryn` Rust adapter

Repository: `blakinio/otclient`  
Primary ownership: WS-R07  
Depends on: Packages B, C and D  
May start now: **no**

Create the crate only after the contract is accepted and the exact Platform/Gateway/Otheryn producers provide source evidence.

Goals:

- implement native handshake/session state;
- encode `GameCommand` into native messages;
- decode native messages into `GameEvent`;
- implement exact capability mapping;
- keep native concepts out of UI, renderer and simulation;
- fail closed on malformed or unsupported messages;
- provide golden, malformed, truncated, fuzz and replay tests.

`protocol-oteryn` must not wrap or translate through `protocol-canary`.

### Package F — automatic protocol selection and integrated game entry

Repositories:

- `blakinio/otclient` consumer;
- `blakinio/Oteryn-Platform` authoritative Gateway producer;
- `blakinio/Otheryn` session/profile validator.

Depends on: Packages B through E  
May start now: **no**

Production policy:

```text
Auto
ForceCanary(profile)   # development/test only
ForceOteryn(version)   # development/test only
```

The exact Package B contract decides whether Gateway selects from a client offer or the client selects from a Gateway candidate set. Regardless of mechanism:

1. authoritative bounded data is obtained before gameplay;
2. exact adapter family, version/profile, transport requirements and capabilities are validated;
3. one exact result is accepted and bound to the Game Session;
4. the highest mutually supported native Oteryn version is preferred when policy allows;
5. Canary is selected only when explicitly advertised/allowed and supported;
6. no compatible pair fails before gameplay.

Security rules:

- one entry attempt and session bind exactly one adapter;
- no in-session switch;
- no fallback after ticket consumption, Game Session issuance, credential handoff, authentication failure, protocol violation or partial admission;
- reconnect/relog is a new attempt with fresh directory/Gateway data and fresh credential;
- force modes are not ordinary production settings;
- fallback never introduces password authentication;
- Game Login Ticket is sent only to Gateway;
- OAuth tokens are sent only to Platform's token/ticket APIs;
- Game Session credential is sent only to the selected Otheryn endpoint.

### Package G — gameplay action lifecycle

Depends on: accepted domain ownership and the relevant adapter support  
May start now as full cross-adapter delivery: **no**

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

For Canary, expose only source-proven acknowledgements and observable authoritative effects. Native Oteryn may add explicit action identifiers and results through the accepted Package B contract.

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

Every applicable implementation package must cover at least:

- the exact Platform OAuth/ticket/Gateway API pair used by the test;
- a supported Canary pair;
- a supported native Oteryn pair when implemented;
- unsupported version/profile;
- contradictory capability advertisement;
- downgrade attempt after ticket consumption and credential handoff;
- cross-world/character/profile Game Session misuse;
- session replacement with stale queued actions;
- simultaneous inbound/outbound traffic;
- queue saturation and deterministic overflow behavior;
- disconnect during queued movement, spell, item and loot actions;
- exact server-authority preservation;
- no blocking network I/O on the frame thread;
- no bearer credential written to logs, settings, fixtures or replay files.

## Agent start rules

Before starting any package:

1. read repository root and nested agent instructions and all relevant overrides;
2. read ADR-001, `PROTOCOL_BOUNDARY.md`, `PLATFORM_GATEWAY_GAME_ENTRY.md` and this plan completely;
3. for game-entry or authentication work, read the exact current Oteryn Platform contracts and implementation;
4. inspect all active tasks, PRs, ownership and shared-path leases in every affected repository;
5. reuse current Identity, ticket, Gateway, World Registry, Game Session, domain, transport and adapter work rather than creating parallel abstractions;
6. create one bounded task, branch and draft PR per repository;
7. state exact producer and consumer versions for cross-repository work;
8. never claim a later package is complete because an earlier architectural type exists.

## Completion definition

The direction is fully implemented only when:

- the protocol-neutral Tokio transport is merged and measured;
- Platform/Game Gateway safely produces the accepted exact protocol-selection/session-binding contract;
- Otheryn validates the Game Session binding and safely produces a versioned native gameplay protocol;
- `protocol-oteryn` exists with exact producer evidence;
- automatic selection and downgrade-negative tests pass across all three repositories;
- Canary remains independently compatible;
- movement, attacks, spells, item actions and loot use semantic commands with server-authoritative results;
- compatible-pair integration tests, exact-head CI and independent audits pass in all affected repositories.
