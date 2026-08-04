# Rust client native gameplay protocol correspondence

Coordination ID: `OTS-20260804-native-protocol-selection`  
Canonical Platform contract: `blakinio/Oteryn-Platform/docs/contracts/OTERYN_NATIVE_GAMEPLAY_PROTOCOL_CONTRACT.md`  
Canonical Platform revision: `9035ae987db67c062a8778721a2c8e686ce76750`  
Otheryn correspondence: `blakinio/Otheryn/docs/contracts/OTERYN_NATIVE_GAMEPLAY_PROTOCOL_CORRESPONDENCE.md`  
Otheryn correspondence revision: `1807b6210375f6a18afabc817a01ccdfee80ddce`

## Status

Contract correspondence only. This PR adds no dependency, crate, runtime, transport, codec, Gateway behavior or gameplay implementation. The workspace still has no `protocol-oteryn` crate.

`protocol-canary` remains the current source-proven compatibility adapter. `oteryn.native.v1` is a separate future family and must not depend on or translate through Canary.

## Normative adoption

The Rust client adopts the exact revisions above for:

- a `1..8` candidate bounded set in Gateway API v1 and one authoritative Gateway selection;
- strict distinction among Gateway API, offer, Game Session, adapter, transport and schema versions;
- opaque Game Session v2 credential and bind-on-first-character-admission semantics;
- `oteryn.native.v1` over TLS 1.3, ALPN `oteryn-game/1`, BE32 framing and protobuf schema revision 1;
- deterministic schema and sorted-capability digests;
- command IDs, client/stream/server sequences, server tick and state revision;
- explicit action lifecycle and stable reasons including `STALE_COMMAND`;
- complete digest-checked snapshot, strict deltas, movement reconciliation and one bounded resync;
- no native v1 resume, command replay, password fallback, byte sniffing, post-ticket retry or in-session adapter switch;
- exact-pair compatibility evidence and staged rollout.

Every implementation task must pin these exact commits, the IDL SHA-256 and fixture manifest. A later Platform/Otheryn contract revision requires an explicit correspondence update before implementation.

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
| transport | current worker until separate Tokio task merges | protocol-neutral supervisor; native TLS/profile codec below it |
| Gateway request | ticket login API v1 | optional bounded `gameplay_offer`, target body `<=16 KiB` |
| Gateway response | session/world/characters | distinct v2 session and authoritative endpoint/profile/schema/list/digest |
| bootstrap | Canary-compatible flow | native exact-binding `ClientHello` and selected character |
| action evidence | source-proven Canary effects only | typed native results plus authoritative deltas |
| state entry | Canary packet sequence | full revisioned snapshot |
| reconnect | current policy | fresh ticket/selection/session/snapshot; no resume |

## Offer and selection validation

Production `Auto` constructs candidates only from exact compiled adapter/codec/schema support; player input cannot invent identifiers.

1. Candidates are unique; offer order has no preference meaning.
2. Gateway World Registry order is authoritative.
3. Development force modes only restrict the offered set.
4. The response tuple must exactly occur in the offer.
5. Sorted capability list, deterministic digest and schema hash must agree.
6. Native connects to `gameplay_selection.host/port/tls_server_name`; legacy world routing cannot override it.
7. Contradiction fails before connection.
8. After redeem/selection no alternate candidate is attempted.
9. `401`, `409`, `503` or ambiguous failure requires a fresh ticket.

## Rust ownership

### Entry and selection

Owns bounded JSON, transient secrets, authoritative world/character presentation and exact response validation. Gateway `protocol_version: 1` remains the login API version only. Production preference remains Gateway/World Registry authority.

### Game session

Owns one immutable selected identity, endpoint, credential handoff, selected character, command namespace, cancellation and stale-session rejection. Replacement sessions inherit no queue, ID, sequence, snapshot or prediction state.

### Native codec/adapter

The later package owns bootstrap representation, BE32/protobuf validation, IDL mapping, parser state and limits. It owns no sockets, Tokio runtime, UI or authoritative simulation and has no dependency on `protocol-canary`.

### Domain/simulation/UI

Owns protocol-neutral semantics and reversible presentation. Inventory, containers, loot, damage, resources and cooldowns change only from authoritative server events. A socket write never means gameplay success.

## Commands and result evidence

| Intent | Native command | Required evidence |
|---|---|---|
| step/stop | step/stop commands | typed result plus authoritative movement/revision |
| attack/follow | set/clear commands | target/combat state plus terminal result |
| spell | cast command | result lifecycle plus resource/cooldown/effect deltas |
| use/use-with | use commands | authoritative item/world/container mutation |
| item move | move command | authoritative inventory/container/tile mutation |
| loot | quick/corpse commands | authoritative transfers or stable rejection |
| chat | say command | delivered event or rejection |
| logout | logout command | terminal result/session-ended evidence |

Every admitted native command reaches a terminal result unless session termination prevents delivery; termination locally cancels pending commands and never triggers replay. Canary must not fabricate native-style acknowledgements.

## Snapshot, delta and duplicate rules

- stage snapshot outside committed simulation until chunk indexes, limits and the hash over exact received `SnapshotChunk` envelope payload bytes validate;
- apply only `base_revision == committed_revision` deltas;
- any duplicate, regression, conflict or malformed delta is fatal;
- on a gap send one bounded resync, freeze authoritative mutation presentation and accept only a complete replacement snapshot;
- tag reversible movement prediction by command ID and reconcile from authoritative movement;
- clear all projection/pending/prediction state on disconnect/replacement;
- cached exact duplicate command returns the known result without reapply;
- same ID/sequence with another exact serialized command payload is fatal;
- duplicate outside the bounded server cache returns `STALE_COMMAND`;
- no reconnect command replay.

## Parser and backpressure obligations

- validate frame length before allocation;
- frame/message `<=1 MiB`, snapshot `<=16 MiB` and `<=256` chunks, protobuf nesting `<=32`;
- reject compressed native v1 input;
- checked conversions and bounded strings/collections;
- no panic, no cursor rewind without progress and no busy-loop on external input;
- bounded queues; old-session commands cannot reach replacements;
- cancellation/control cannot starve and semantic commands are not silently dropped/reordered.

## Fixture ownership and rollout

Rust owns cross-language golden encode/decode fixtures, malformed/truncated/oversize/unknown/sequence/snapshot regressions, arbitrary-frame/state-machine fuzzers, deterministic normalized replay, schema provenance and semantic differential journeys against Canary where meaningful. Fixtures are synthetic and exclude credentials, identities, endpoints, chat and proprietary captures.

The adapter may merge client-first only while production offers exclude native. Activation requires exact Gateway and Otheryn readiness plus integrated staging manifest. Rollback removes native from fresh offers/advertisement, drains/closes native sessions and keeps Canary available for fresh explicitly selected sessions. No active or failed native session switches adapters.

## Later packages

1. Platform/Gateway producer extension;
2. Otheryn v2 consumer/native producer;
3. Rust `protocol-oteryn` adapter;
4. automatic selection and exact integrated E2E.

Use the ready prompts in `blakinio/Oteryn-Platform/docs/agents/prompts/` at Platform revision `9035ae987db67c062a8778721a2c8e686ce76750`.
