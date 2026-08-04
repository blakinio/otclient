# ADR-001: Dual protocol selection and client async transport

Status: Accepted  
Date: 2026-08-04  
Scope: `oteryn-client/` and future coordinated `blakinio/Otheryn` protocol work  
Coordination ID: `OTS-20260804-native-protocol-selection`

## Context

The Rust client already contains an exact Canary compatibility adapter and protocol-neutral gameplay contracts. The architecture also reserves a future native Oteryn adapter, but it previously did not state precisely how the adapters coexist, how one is selected, whether a normal player chooses it, how fallback is secured, or which runtime owns client networking.

The current Rust transport is a bounded synchronous implementation executed by application-owned workers. It is sufficient for the completed technical-login slice, but the playable client needs full-duplex reads and writes, cancellation, timers, heartbeats, bounded backpressure and deterministic shutdown without blocking the window or render thread.

The Otheryn C++ server already uses asynchronous ASIO. Selecting Tokio for the Rust client does not justify replacing the server networking library.

## Decision

### Two independent first-class adapters

The client will support two separately versioned protocol adapters:

- `protocol-canary` remains the exact compatibility adapter for source-proven Canary/Otheryn profiles;
- `protocol-oteryn` becomes the preferred native adapter after a coordinated client/server contract is implemented.

Neither adapter wraps, translates through or depends on the other. Both map between wire data and the same protocol-neutral `GameCommand` and `GameEvent` contracts.

The domain, simulation, UI, input and renderer must compile and test without either adapter and must not branch on Canary or Oteryn packet layouts.

### One protocol-neutral transport owner

The target client async I/O runtime is Tokio. A separate implementation package will migrate protocol-neutral transport and game-session supervision to an application-owned Tokio runtime with:

- bounded full-duplex read and write ownership;
- explicit connect, read, write and idle deadlines;
- `TCP_NODELAY` where applicable;
- bounded inbound and outbound queues;
- explicit cancellation and joined shutdown;
- no hidden global runtime;
- no blocking network work on the window/render thread;
- no unbounded task spawning;
- stable transport errors independent of gameplay opcodes.

Tokio is a client execution decision, not a wire protocol and not a server requirement. Both adapters use the same transport boundary unless a later accepted ADR proves that a native Oteryn transport needs a different implementation.

The current synchronous transport remains valid until the dedicated migration package passes comparative tests and exact-head validation. This ADR does not claim that Tokio is already implemented or that it reduces physical network RTT.

### Server-advertised selection

Production selection uses a typed policy:

```text
Auto
ForceCanary(profile)   # development/test only
ForceOteryn(version)   # development/test only
```

`Auto` is the production default. The authoritative directory, gateway or bounded pre-authentication negotiation advertises the exact protocol candidates for the selected world/channel. The client intersects them with locally supported versions and selects:

1. the highest mutually supported native Oteryn version allowed by policy;
2. otherwise an explicitly advertised and supported Canary profile;
3. otherwise a typed incompatibility failure before gameplay.

The normal player-facing UI does not expose an unrestricted protocol switch. Manual forcing is restricted to development, testing and controlled diagnostics.

### Session binding and downgrade resistance

The selected adapter, exact version/profile, transport requirements and capability set are bound to the game-entry attempt before credential handoff whenever the producer contract permits it, and always before gameplay messages are accepted.

For one gameplay session:

- exactly one adapter is active;
- no in-session adapter switch is allowed;
- no automatic retry with another adapter occurs after authentication failure, ticket consumption, protocol violation or partial admission;
- reconnect or relog creates a new attempt and performs selection again using fresh authoritative data and, when required, a fresh one-shot ticket;
- unsupported or contradictory advertisements fail closed;
- protocol fallback never introduces password login or bypasses Oteryn Identity and ticket rules.

Native-to-Canary fallback is therefore a pre-authentication `Auto` selection result, not an error-recovery mechanism.

### Native Oteryn contract goals

The first native Oteryn contract must be semantic and versioned. The coordinated producer/consumer design will decide exact framing and schema technology, but it must cover:

- session generation and protocol version;
- capability negotiation;
- client action sequence and stable action identifier;
- server tick or authoritative ordering where available;
- accepted, rejected, delayed or effect-observed action lifecycle;
- stable rejection reasons;
- snapshot, delta and reconciliation semantics;
- bounded collections, strings, decompression and message sizes;
- compatibility matrix, rollout and rollback behavior.

The client sends player intent. The server remains authoritative for movement legality, combat, spells, cooldowns, resources, inventory, loot, economy, random outcomes and persistence.

### Cross-repository implementation boundary

Creating `protocol-oteryn` product code requires a separate authorized programme under `OTS-20260804-native-protocol-selection` with linked tasks in both repositories.

The Otheryn server task may add a native service/profile, capability advertisement, command decoding and event encoding. It does not replace ASIO merely to mirror Tokio. Server networking changes require independent profiling evidence and a separate ADR.

The Rust client task may create the crate, adapter/session implementation, selection policy and integration tests only after the producer contract and rollout order are accepted.

## Consequences

### Positive

- Canary compatibility remains usable while Oteryn can evolve a cleaner first-party protocol.
- Domain, simulation, UI and renderer avoid protocol-specific forks.
- Tokio transport migration can proceed independently from native protocol design.
- Production selection is deterministic and resistant to silent downgrade.
- Native Oteryn can provide explicit action acknowledgement, reconciliation and diagnostics rather than inferring them from Canary behavior.

### Costs

- Two adapters require separate fixtures, compatibility matrices and maintenance.
- Native Oteryn work is cross-repository and cannot be completed by a client-only task.
- The client must maintain selection, capability and incompatibility handling.
- Tokio migration requires comparative evidence and careful application-runtime integration.

## Rejected alternatives

### Replace Canary immediately

Rejected because the playability programme currently depends on source-proven Canary compatibility and the native server contract does not yet exist.

### Make `protocol-oteryn` a wrapper around `protocol-canary`

Rejected because that would preserve Canary wire constraints, couple lifecycles and defeat the native semantic boundary.

### Let players freely select any protocol in production

Rejected because the server is authoritative for supported profiles and unrestricted forcing increases failed admission and downgrade risk.

### Switch adapters after failed login or during a session

Rejected because one-shot credentials may already be consumed and partial state makes fallback ambiguous and unsafe.

### Rewrite Otheryn networking in Tokio

Rejected because Tokio is a Rust client runtime. Otheryn is C++ and already uses asynchronous ASIO.

## Required follow-up packages

1. Protocol-neutral Tokio transport and game-session supervisor migration in `blakinio/otclient`.
2. Cross-repository native Oteryn protocol contract and server capability advertisement.
3. `protocol-oteryn` client adapter plus Otheryn server producer implementation.
4. Automatic selection and controlled development overrides.
5. Differential domain/replay tests and staged rollout evidence.

Each package requires its own task, ownership, tests, audit and exact-head CI. This ADR authorizes direction, not implementation claims.
