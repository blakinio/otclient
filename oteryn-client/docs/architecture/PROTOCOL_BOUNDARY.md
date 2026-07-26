# Protocol and Transport Boundary

## 1. Purpose

The new client initially connects to Canary but must not become architecturally dependent on Canary packet layout. Native Oteryn services later implement the same client-facing domain contract through a separate adapter.

## 2. Layers

```text
transport
  -> framing/session codec
  -> protocol adapter validation
  -> normalized GameEvent/GameCommand
  -> game domain and simulation
```

### Transport

Owns connection establishment, encrypted byte transport, stream/socket lifecycle, timeouts, heartbeats, bounded reads/writes and connection metrics.

### Framing/session codec

Owns message boundaries, sequencing, compression/encryption steps required by the selected protocol and bounded message assembly.

### Protocol adapter

Owns exact message IDs, field order, widths, signedness, optional fields, version gates, feature negotiation and translation.

### Domain

Owns meaning independent of wire representation.

## 3. Core contracts

Representative interfaces:

```rust
pub trait ProtocolAdapter {
    type Session;

    fn capabilities(&self) -> AdapterCapabilities;
    fn begin_session(&self, input: SessionBootstrap) -> Result<Self::Session, ProtocolError>;
    fn decode(&self, session: &mut Self::Session, frame: &[u8])
        -> Result<SmallVec<[GameEvent; 4]>, ProtocolError>;
    fn encode(&self, session: &mut Self::Session, command: &GameCommand)
        -> Result<EncodedFrames, ProtocolError>;
}
```

The exact Rust shape is finalized during implementation, but the boundary is stable:

- adapters may depend on domain contracts;
- domain contracts never depend on adapters;
- UI and features never receive raw adapter messages.

## 4. Domain commands

Examples:

```text
Move(direction)
StopMovement
UseItem(item_ref)
UseItemOn(item_ref, target_ref)
Attack(entity_id)
Follow(entity_id)
OpenContainer(item_ref)
CloseContainer(container_id)
MoveItem(request)
SendChat(request)
Logout(reason)
```

Commands express user intent, not encoded packet bytes. Application/domain validation catches impossible local references, but server validation remains authoritative.

## 5. Domain events

Examples:

```text
SessionStarted
SessionEnded
MapRegionLoaded
TileChanged
EntitySpawned
EntityMoved
EntityRemoved
PlayerStatsChanged
ContainerOpened
ContainerDelta
InventoryChanged
CombatStateChanged
ChatMessageReceived
ServerNotice
FeatureCapabilitiesChanged
```

Events are validated and bounded. Large snapshots use owned/borrowed batch structures designed to avoid pathological allocation.

## 6. Canary adapter

`protocol-canary` is a compatibility boundary, not a template for the domain.

Every supported revision requires:

- exact Canary producer reference;
- protocol/version/features matrix;
- packet or schema evidence;
- positive golden fixtures;
- malformed and truncated fixtures;
- explicit unknown-message behavior;
- supported and unsupported client/server pairs;
- cross-repository rollout record.

No opcode, field or default may be copied from another client fork without Canary proof.

Canary-specific concepts that have no domain equivalent remain inside the adapter or an explicitly versioned compatibility extension. They must not pollute unrelated features.

## 7. Oteryn adapter

`protocol-oteryn` will implement native Oteryn game-session contracts. The architecture does not prematurely mandate QUIC, Protobuf or another technology.

The audit and later cross-repository ADR must decide:

- transport;
- message schema technology;
- snapshot/delta model;
- session resume semantics;
- stream prioritization;
- compatibility/versioning policy.

The client domain remains unchanged if the native transport changes.

## 8. Gameplay channels versus transport streams

`WorldChannelId` identifies a parallel gameplay instance selected at login/relog.

A transport stream is an implementation mechanism that may carry control, world, chat or other messages. These are unrelated concepts and use different names/types throughout code and documentation.

## 9. Validation and limits

Adapters enforce:

- maximum frame and collection sizes;
- validated lengths before allocation;
- checked numeric conversion;
- bounded string lengths and valid encoding policy;
- duplicate/out-of-order policy;
- legal enum values or explicit unknown handling;
- recursion/depth limits for structured messages;
- decompression ratio and output limits;
- no panic on malformed external input.

Parser errors are typed as recoverable message rejection, session-fatal protocol violation or implementation fault. Busy-loop recovery and cursor rewind without progress are forbidden.

## 10. Sequencing and time

Normalized events may carry:

```text
server_tick
sequence
baseline/revision
receive timestamp
```

Only when supported by the exact adapter. The domain must not fabricate server ticks for protocols that do not provide them.

Client presentation time, estimated server time and simulation step are distinct types or wrappers to prevent accidental mixing.

## 11. Recording and replay

The protocol recorder supports two evidence levels:

1. sanitized raw framed data where collection and licensing permit;
2. normalized domain events for deterministic replay.

Recorded material excludes authentication secrets and follows privacy/provenance rules. Synthetic fixtures are preferred for repository commits.

## 12. Fuzzing

Each adapter exposes parser entry points suitable for fuzzing:

- arbitrary frame bytes;
- truncated valid frames;
- length-field mutation;
- collection-count mutation;
- compression bombs;
- state-machine ordering mutation.

Fuzz findings become minimized regression fixtures.

## 13. Compatibility failure behavior

Unsupported combinations fail before entering gameplay when possible. The client reports a typed action such as update client, choose another channel, refresh directory or contact support.

The client never silently falls back from Oteryn Identity/game-ticket authentication to main-password login.
