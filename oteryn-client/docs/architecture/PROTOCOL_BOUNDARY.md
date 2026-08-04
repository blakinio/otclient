# Protocol and Transport Boundary

Normative decision: [ADR-001: Dual protocol selection and client async transport](decisions/ADR-001-dual-protocol-selection-and-async-transport.md)  
Execution roadmap: [Dual Protocol and Tokio Execution Plan](DUAL_PROTOCOL_EXECUTION_PLAN.md)  
Coordination ID: `OTS-20260804-native-protocol-selection`

## 1. Purpose

The Rust client initially connects through exact Canary compatibility but must not become architecturally dependent on Canary packet layouts. Native Oteryn services later implement the same protocol-neutral gameplay contract through a separate preferred adapter.

This document defines transport ownership, adapter isolation, production selection, downgrade behavior, player-action semantics and the coordinated boundary between client and server work.

## 2. Target layers

```text
application / game-session orchestration
  -> protocol selection policy
  -> protocol-neutral transport/session supervisor
  -> selected framing/session codec
  -> selected protocol adapter
  -> normalized GameEvent/GameCommand
  -> game domain and simulation
```

### Protocol selection policy

Owns the intersection of:

- authoritative server-advertised candidates;
- locally supported adapter versions/profiles;
- the configured selection policy.

It does not guess from malformed gameplay bytes and does not retry another adapter after a later authentication or protocol failure.

### Transport/session supervisor

Owns:

- connection establishment;
- byte transport and socket lifecycle;
- full-duplex reads and writes;
- explicit deadlines and heartbeats;
- bounded inbound and outbound queues;
- cancellation and deterministic joined shutdown;
- connection and queue metrics.

The target client runtime is Tokio, introduced by a separate measured migration package. The current synchronous worker transport remains valid until that package is merged.

Transport does not own credentials, authoritative routing, gameplay opcodes, domain events, production reconnect policy or UI.

### Framing/session codec

Owns:

- message boundaries;
- compression/encryption required by the selected protocol;
- bounded frame assembly;
- transport-level sequence or integrity fields;
- exact session bootstrap framing.

A codec is selected by the bound adapter/profile and does not leak into the domain.

### Protocol adapter

Owns:

- exact message IDs;
- field order, width and signedness;
- optional fields and version gates;
- capability mapping;
- adapter-local session state;
- `GameCommand` encoding;
- `GameEvent` decoding.

### Domain

Owns meaning independent of wire representation. The domain never knows which adapter encoded or decoded a message.

## 3. Stable adapter contract

Representative interface:

```rust
pub trait ProtocolAdapter {
    type Session;

    fn identity(&self) -> ProtocolIdentity;
    fn capabilities(&self) -> AdapterCapabilities;
    fn begin_session(&self, input: SessionBootstrap)
        -> Result<Self::Session, ProtocolError>;
    fn decode(
        &self,
        session: &mut Self::Session,
        frame: &[u8],
    ) -> Result<SmallVec<[GameEvent; 4]>, ProtocolError>;
    fn encode(
        &self,
        session: &mut Self::Session,
        command: &GameCommand,
    ) -> Result<EncodedFrames, ProtocolError>;
}
```

The exact Rust shape is finalized by implementation, but these rules are stable:

- adapters may depend on domain contracts;
- domain contracts never depend on adapters;
- UI and feature crates never receive raw protocol messages;
- transport never interprets gameplay opcodes;
- an adapter never mutates simulation state;
- one gameplay session owns exactly one selected adapter;
- `protocol-canary` and `protocol-oteryn` do not depend on one another.

## 4. Two first-class adapters

### `protocol-canary`

`protocol-canary` is the exact compatibility boundary for source-proven Canary/Otheryn profiles.

It remains supported after native Oteryn exists. It is not deprecated merely because `protocol-oteryn` becomes preferred.

Every supported profile requires:

- exact Canary/Otheryn producer revision;
- protocol/version/features matrix;
- packet or schema evidence;
- positive golden fixtures;
- malformed and truncated fixtures;
- explicit unknown-message behavior;
- supported and unsupported client/server pairs;
- rollout record.

No opcode, field or default may be copied from another client fork without producer proof.

Canary-specific concepts with no domain equivalent remain inside the adapter or an explicitly versioned compatibility extension.

### `protocol-oteryn`

`protocol-oteryn` is the preferred future native Oteryn game-session adapter.

It starts only after a coordinated producer/consumer contract and rollout order are accepted under `OTS-20260804-native-protocol-selection`.

It must implement semantic player-intent commands and authoritative result events without mirroring server storage into the client domain.

It must not:

- wrap `protocol-canary`;
- translate native messages through Canary packets;
- own sockets or the Tokio runtime;
- bypass Oteryn Identity or one-shot ticket rules;
- redesign UI or simulation merely to match server schema.

The coordinated contract must decide:

- exact transport and framing;
- schema and versioning technology;
- capability advertisement;
- action identifiers and sequencing;
- accepted/rejected/delayed/effect-observed semantics;
- server tick or authoritative ordering where available;
- snapshot, delta and reconciliation behavior;
- resume/reconnect behavior;
- message, collection and decompression limits;
- supported-pair matrix and rollout.

## 5. Production protocol selection

Conceptual policy:

```text
Auto
ForceCanary(profile)   # development/test only
ForceOteryn(version)   # development/test only
```

`Auto` is the production default.

Before gameplay, the authoritative world directory, gateway or a dedicated bounded pre-authentication negotiation provides exact candidates for the selected world/channel. Each candidate identifies:

- adapter family;
- exact version/profile;
- transport requirements;
- capability set;
- authentication/session requirements.

The client:

1. validates and bounds the advertisement;
2. intersects it with locally supported candidates;
3. selects the highest permitted native Oteryn version;
4. otherwise selects an explicitly advertised supported Canary profile;
5. otherwise returns a typed incompatibility result before gameplay.

The normal player-facing UI does not expose an unrestricted protocol chooser. Force modes are development/test diagnostics and must be visibly non-production.

## 6. Session binding and downgrade resistance

The selected adapter, exact version/profile, capabilities and transport requirements are bound to the game-entry attempt before credential handoff whenever the producer contract permits it, and always before gameplay messages are accepted.

For one gameplay session:

- exactly one adapter is active;
- selection cannot change after session creation;
- authentication failure does not trigger another adapter;
- a consumed one-shot ticket does not trigger another adapter;
- protocol violation or partial admission does not trigger another adapter;
- reconnect/relog destroys session-scoped state and performs a new selection using fresh authoritative data;
- contradictory or unsupported advertisements fail closed;
- fallback never introduces password login.

Native-to-Canary fallback is a pre-authentication `Auto` selection result, not an error-recovery mechanism.

## 7. Tokio transport target

A separate WS-R05 implementation package may migrate the current synchronous client transport before the native protocol exists because Tokio remains protocol-neutral.

The accepted implementation must prove:

- one application-owned runtime lifecycle;
- bounded reader and writer queues;
- full-duplex operation;
- explicit deadlines;
- deterministic cancellation and joined shutdown;
- partial read/write handling;
- timeout and connection-reset handling;
- deterministic queue-overflow policy;
- no window/render-thread blocking;
- no unbounded task spawn or allocation;
- exact compatibility with existing Canary framing and errors;
- comparative latency, CPU and allocation evidence.

Tokio APIs must not escape upward into domain, simulation, renderer, UI or feature contracts.

Tokio does not guarantee lower physical RTT. Its purpose is controlled concurrency, backpressure, cancellation and frame-thread isolation.

The Otheryn C++ server retains asynchronous ASIO unless a separate profiling-backed ADR authorizes a server networking change.

## 8. Protocol-neutral commands

Target command vocabulary includes:

```text
Step
StopMovement
LookAt
Use
UseWith
MoveItem
SetAttackTarget
ClearAttackTarget
SetFollowTarget
ClearFollowTarget
CastSpell
QuickLoot
LootCorpse
ConfigureLootPolicy
Say
Logout
```

Commands express player intent, not encoded bytes or claimed results.

Application/domain validation catches stale or impossible local references, but the server remains authoritative.

## 9. Protocol-neutral events

Representative events include:

```text
SessionStarted
SessionEnded
ActionAccepted
ActionRejected
ActionDelayed
ActionEffectObserved
MapRegionLoaded
TileChanged
EntityAppeared
EntityMoved
EntityRemoved
PlayerStatsChanged
CooldownChanged
ContainerOpened
ContainerDelta
InventoryChanged
CombatStateChanged
ChatMessageReceived
ServerNotice
FeatureCapabilitiesChanged
```

An adapter emits only events supported by its exact wire contract.

Canary must not fabricate explicit acknowledgements, rejection reasons or server ticks when packets do not provide them. Native Oteryn may define these explicitly through the coordinated contract.

## 10. Player-action authority

### Movement

The client may perform reversible visual prediction. The server decides collision, speed, legality and final position. Server events reconcile prediction.

### Attack and follow

The client selects and highlights a target. The server validates target, visibility, range, path, PvP rules and timing, and computes all results.

### Spell casting

The client creates a semantic cast request and may show reversible pending feedback. Canary uses the source-proven text-incantation path where necessary. The server validates spell knowledge, resources, cooldowns, range, line of sight and state, then applies all authoritative effects.

### Loot

The client requests loot for a corpse/position and mode. The server validates corpse ownership, party rules, range, cooldown, capacity and destination containers, and performs every item transfer. Inventory changes only from server events.

### Item use and movement

The client sends `Use`, `UseWith` or `MoveItem` intent. The server validates real identity, ownership, location, quantity, range, capacity and scripts before committing state.

The client never sends claimed damage, healing, mana consumption, loot acquisition or completed inventory mutations.

## 11. Action lifecycle

The internal client lifecycle distinguishes:

```text
created
queued
encoded
written
awaiting authoritative effect
accepted / rejected / delayed / effect-observed
completed / expired / cancelled
```

TCP write completion proves only that bytes reached the local socket path. It does not prove gameplay success.

For Canary, action completion is inferred only from source-proven authoritative events. Where the protocol provides no explicit acknowledgement, state is reported honestly as unconfirmed or effect-observed.

Native Oteryn may provide explicit action IDs, sequences, acknowledgements and stable rejection reasons.

## 12. Queue and backpressure rules

Transport and session queues are bounded.

Required behavior:

- control/cancellation cannot be starved;
- movement and other latency-sensitive commands cannot be starved by background requests;
- spell, item, loot, trade and chat commands are not silently dropped or reordered;
- command coalescing is allowed only when the semantic contract proves replacement is safe;
- overflow becomes a typed error/metric, never unbounded memory growth;
- stale-session queued commands never reach a replacement session.

## 13. Gameplay channels versus transport streams

`WorldChannelId` identifies a parallel gameplay instance selected at login or relog.

A transport stream is an implementation mechanism that may carry control, world, chat or other messages. These concepts use different types and names.

## 14. Validation and limits

Adapters enforce:

- maximum frame and collection sizes;
- validated lengths before allocation;
- checked numeric conversion;
- bounded strings and encoding policy;
- duplicate and out-of-order policy;
- legal enum values or explicit unknown handling;
- recursion/depth limits;
- decompression ratio and output limits;
- no panic on malformed external input.

Parser errors are typed as recoverable message rejection, session-fatal protocol violation or implementation fault. Busy-loop recovery and cursor rewind without progress are forbidden.

## 15. Sequencing and time

Normalized envelopes may carry:

```text
server_tick
sequence
baseline/revision
receive_timestamp
client_action_id
```

Only when supported by the exact adapter. The domain must not fabricate server ticks or explicit action results.

Client presentation time, estimated server time and simulation step are distinct types or wrappers.

## 16. Recording, replay and fuzzing

Evidence levels:

1. sanitized raw framed data when collection and licensing permit;
2. normalized commands/events for deterministic replay.

Recorded material excludes authentication secrets. Synthetic fixtures are preferred for repository commits.

Each adapter exposes parser entry points for:

- arbitrary frame bytes;
- truncated valid frames;
- length and collection-count mutation;
- compression bombs;
- state-machine ordering mutation;
- contradictory capability advertisements.

Fuzz findings become minimized regression fixtures.

Differential domain/replay tests may compare Canary and native Oteryn journeys where both represent the same semantics. Byte equality is neither expected nor required.

## 17. Compatibility failure behavior

Unsupported combinations fail before credential handoff or gameplay whenever possible. The client reports a typed action such as update client, choose another channel, refresh directory or contact support.

The client never:

- silently falls back from Oteryn Identity/game-ticket authentication to password login;
- guesses an adapter from failed gameplay bytes;
- switches adapters during one session;
- claims compatibility without an exact tested client/server pair.
