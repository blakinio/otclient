# Rust client native gameplay protocol correspondence

Coordination ID: `OTS-20260804-native-protocol-selection`  
Canonical source of truth: `blakinio/Oteryn-Platform/docs/contracts/OTERYN_NATIVE_GAMEPLAY_PROTOCOL_CONTRACT.md`  
Canonical review PR: `blakinio/Oteryn-Platform#519`  
Otheryn correspondence: `blakinio/Otheryn/docs/contracts/OTERYN_NATIVE_GAMEPLAY_PROTOCOL_CORRESPONDENCE.md`  
Otheryn review PR: `blakinio/Otheryn#356`

## Status

Contract correspondence only. This PR adds no dependency, crate, runtime, transport, codec, Gateway behavior or gameplay implementation. The workspace still has no `protocol-oteryn` crate.

`protocol-canary` remains the current source-proven compatibility adapter. `oteryn.native.v1` is a separate future family and must not depend on or translate through Canary.

## Normative adoption

The Rust client adopts the canonical contract for:

- a `1..8` candidate bounded set in Gateway API v1 and one authoritative Gateway selection;
- strict distinction among Gateway API, offer, Game Session, adapter, transport and schema versions;
- opaque Game Session v2 credential and bind-on-first-character-admission semantics;
- `oteryn.native.v1` over TLS 1.3, ALPN `oteryn-game/1`, BE32 framing and protobuf schema revision 1;
- deterministic schema and sorted-capability digest rules;
- command IDs, client/stream/server sequences, server tick and state revision;
- explicit action lifecycle and stable reasons including `STALE_COMMAND`;
- complete digest-checked snapshot, strict deltas, movement reconciliation and one bounded resync;
- no native v1 resume, command replay, password fallback, byte sniffing, post-ticket retry or in-session adapter switch;
- exact-pair compatibility evidence and staged rollout.

If this document differs from the merged canonical contract, the exact canonical revision controls. Every implementation task must pin the exact Platform contract commit, Otheryn producer commit, IDL SHA-256 and fixture manifest.

## Current and target layering

```text
application / game-session orchestration
  -> production selection policy
  -> protocol-neutral transport/session supervisor
  -> selected framing/session codec
  -> selected independent protocol adapter
  -> normalized GameCommand / GameEvent
  -> game domain and simulation
```

| Area | Current | Native target |
|---|---|---|
| adapters | protocol-neutral contracts plus `protocol-canary` | independent `protocol-oteryn` |
| transport | current worker until separate Tokio task merges | protocol-neutral supervisor; native TLS/profile codec selected below it |
| Gateway request | ticket login API v1 | optional bounded `gameplay_offer`, target body `<=16 KiB` |
| Gateway response | session/world/characters | distinct v2 session and authoritative selected endpoint/profile/schema/list/digest |
| session bootstrap | Canary-compatible flow | `ClientHello` exact binding and character ID |
| action evidence | source-proven Canary effects only | typed native results plus authoritative deltas |
| state entry | Canary packet sequence | full revisioned snapshot |
| reconnect | current policy | fresh ticket/selection/session/snapshot; no resume |

## Offer and selection validation

Production `Auto` constructs candidates only from exact compiled adapter/codec/schema support; player input cannot invent identifiers.

For each candidate the build records family, profile, transport, schema revision/hash, sorted capabilities/digest and exact fixture manifest. Rules:

1. candidates are unique and order has no preference meaning;
2. Gateway World Registry order is authoritative;
3. development force modes only restrict the offered set;
4. the response candidate must exactly occur in the offer;
5. sorted capability list, deterministic digest and schema hash must all agree;
6. native uses `gameplay_selection.host/port/tls_server_name`; legacy world route cannot override it;
7. contradiction fails before the gameplay connection;
8. after redeem/selection no alternate candidate is attempted;
9. `401`, `409`, `503` or ambiguous failure requires a fresh ticket.

## Rust ownership

### Entry consumer

Owns bounded JSON, transient secrets, authoritative world/character presentation and exact response validation. Gateway `protocol_version: 1` remains the login API version only.

### Selection/session

Owns one immutable selected identity, endpoint, session handoff, selected character, command namespace, cancellation and stale-session rejection. Replacement sessions inherit no queues, IDs, sequences, snapshots or prediction.

### Native adapter/codec

The later package owns bootstrap representation, BE32/protobuf validation, exact IDL mapping, parser state and limits. It owns no sockets, Tokio runtime, UI or authoritative simulation.

### Domain/simulation/UI

Owns protocol-neutral semantics and reversible presentation. Inventory, containers, loot, damage, resources and cooldowns change only from authoritative server events. A socket write never means gameplay success.

## Commands and completion evidence

| Domain intent | Native command | Completion evidence |
|---|---|---|
| step/stop | `StepCommand` / `StopMovementCommand` | typed result plus authoritative movement/revision |
| attack/follow | set/clear commands | target/combat state plus terminal result |
| spell | `CastSpellCommand` | accepted/rejected/delayed/effect/completed plus resource/cooldown/effect deltas |
| use/use-with | `UseCommand` / `UseWithCommand` | authoritative item/world/container mutation |
| item move | `MoveItemCommand` | authoritative inventory/container/tile mutation |
| loot | quick/corpse commands | authoritative transfers or stable rejection |
| chat | `SayCommand` | delivered event or rejection |
| logout | `LogoutCommand` | terminal result/session-ended evidence |

Every admitted native command must reach a terminal result unless session termination prevents delivery; termination locally cancels pending commands and never triggers automatic replay. Canary must not fabricate native-style acknowledgement semantics.

## Snapshot/delta consumer rules

- stage snapshot data outside committed simulation until all chunk indexes, limits and the hash over exact received `SnapshotChunk` envelope payload bytes validate;
- apply a delta only when `base_revision` equals the current committed revision;
- any duplicate, regression, conflict or malformed delta is fatal;
- on a gap send one bounded resync request, freeze authoritative mutations and accept only a complete replacement snapshot;
- tag reversible movement prediction by command ID and reconcile from authoritative movement;
- never merge incomplete/old-session projection state;
- clear projection, pending actions and prediction on disconnect/replacement.

## Command duplicate policy

The adapter validates command ID and sequence. Otheryn's duplicate identity uses SHA-256 of the exact received serialized `CommandEnvelope` submessage bytes, excluding the outer envelope; command unknown fields are rejected.

- a cached exact duplicate returns the known latest result and is not reapplied;
- ID/sequence reuse with another payload is fatal;
- a duplicate outside the bounded result cache is rejected as `STALE_COMMAND`;
- no command is replayed after reconnect.

## Parser and backpressure obligations

- validate length before allocation;
- cap frame/message at 1 MiB, snapshot at 16 MiB/256 chunks and protobuf depth at 32;
- reject compressed native v1 input;
- enforce checked conversions and bounded strings/collections;
- no panic, cursor rewind without progress or busy-loop on external input;
- queues remain bounded and old-session commands cannot reach a replacement;
- cancellation/control cannot starve; semantic commands are not silently dropped or reordered.

## Fixture ownership

Rust owns cross-language golden encode/decode fixtures, malformed/truncated/oversize/unknown/sequence/snapshot regressions, arbitrary-frame/state-machine fuzzers, deterministic normalized replay, schema/generated-code provenance and differential semantic journeys against Canary where meaningful. Byte equality and fabricated acknowledgements are not expected.

Fixtures are synthetic and exclude credentials, real identities, endpoints, chat and proprietary captures.

## Rollout

The adapter may merge client-first only while production offers exclude native. Activation requires exact Gateway and Otheryn readiness plus integrated staging manifest. Rollback removes native from fresh offers/advertisement, drains/closes native sessions and keeps Canary available for fresh explicitly selected sessions. No active or failed native session switches adapters.

## Later packages

After all contract PRs merge and archive:

1. Platform/Gateway producer extension;
2. Otheryn v2 consumer/native producer;
3. Rust `protocol-oteryn` adapter;
4. automatic selection and exact integrated E2E.

Use the ready prompts in `blakinio/Oteryn-Platform/docs/agents/prompts/` at the exact merged contract revision.
