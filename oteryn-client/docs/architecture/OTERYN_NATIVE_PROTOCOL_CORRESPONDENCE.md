# Rust client native gameplay protocol correspondence

Coordination ID: `OTS-20260804-native-protocol-selection`  
Canonical Platform contract: `blakinio/Oteryn-Platform/docs/contracts/OTERYN_NATIVE_GAMEPLAY_PROTOCOL_CONTRACT.md`  
Canonical contract/schema revision: `2` / `2`  
Canonical schema SHA-256: `9c67f19525400fb9890d2a3541ceb6d02eb955061540ad39ca1c1d891c06eba9`  
Canonical merged Platform revision: `PENDING_PLATFORM_PR_540_MERGE`  
Otheryn correspondence: `blakinio/Otheryn/docs/contracts/OTERYN_NATIVE_GAMEPLAY_PROTOCOL_CORRESPONDENCE.md`  
Canonical merged Otheryn correspondence revision: `PENDING_OTHERYN_PR_365_MERGE`  
Candidate Platform head reviewed by this draft: `19a9b3a27d2b00d4dfb8fd83ebf24dec15233b91`  
Candidate Otheryn correspondence head reviewed by this draft: `82cf07773e8a1e20d90d80a6868b786bffe8a118`

## Status

Contract correspondence only. This PR adds no dependency, crate, runtime, transport, codec, Gateway behavior or gameplay implementation. The workspace still has no `protocol-oteryn` crate.

`protocol-canary` remains the independent source-proven compatibility adapter. Native Oteryn is a separate family with exactly `family = oteryn` and `native_protocol_version = 1`. It must not depend on, translate through or reuse Canary compatibility-profile machinery.

There is no native profile field, alias, placeholder, enum, catalogue, registry, factory, ordering, selector or force-profile mode. This draft must not merge until the exact Platform and Otheryn merge commits replace both pending markers and their candidate heads are verified as ancestors.

## Normative adoption

The Rust client adopts the exact merged revisions and digest above for:

- a bounded `1..8` candidate set in Gateway API v1 and one authoritative Gateway selection;
- strict distinction among Gateway API, offer, Game Session, adapter, transport, native protocol and schema versions;
- opaque Game Session v2 credential and bind-on-first-character-admission semantics;
- exact native tuple `family = oteryn`, `native_protocol_version = 1`, `transport = tcp.tls13.protobuf.be32.v1`;
- TLS 1.3, ALPN `oteryn-game/1`, unsigned 32-bit big-endian framing and protobuf schema revision `2`;
- exact schema SHA-256 and sorted capability digest;
- command IDs, client/server sequences, server tick and state revisions;
- explicit authoritative action lifecycle and stable typed reasons;
- complete digest-checked snapshot, strict deltas, movement reconciliation and one bounded resync;
- no native v1 compression, resume, command replay, password fallback, byte sniffing, post-selection retry or in-session adapter switch;
- exact-pair compatibility evidence and staged rollout.

Every implementation task must pin the exact merged commits, IDL SHA-256 and fixture manifest. A later Platform/Otheryn revision requires an explicit correspondence update before implementation.

## Current and target layering

```text
application / game-session orchestration
  -> production selection policy
  -> protocol-neutral Tokio transport/session supervisor
  -> selected framing/session codec
  -> selected independent protocol adapter
  -> normalized GameCommand / GameEvent
  -> game domain and simulation
```

| Area | Current | Native target |
|---|---|---|
| adapters | protocol-neutral contracts plus `protocol-canary` | independent `protocol-oteryn` with no dependency on Canary |
| transport | existing Tokio-based protocol-neutral transport | same supervisor; native TLS/BE32 codec below it |
| Gateway request | ticket login API v1 | optional bounded `gameplay_offer`, body `<=16 KiB` |
| Gateway response | current session/world/characters | distinct v2 session and authoritative endpoint/family/native-version/schema/capability tuple |
| bootstrap | Canary-compatible flow | native exact-binding `ClientHello` and selected character |
| action evidence | source-proven Canary effects only | typed native results plus authoritative deltas |
| state entry | Canary packet sequence | complete revisioned snapshot |
| reconnect | current policy | fresh ticket/selection/session/snapshot; no resume |

## Offer and selection validation

Production `Auto` constructs candidates only from exact compiled adapter/codec/schema support; player or administrator input cannot invent identifiers.

1. Candidates are unique; offer order has no preference meaning.
2. At most one candidate has `family = oteryn`, and it has `native_protocol_version = 1`.
3. Gateway/World Registry policy is authoritative for the selected family.
4. Development force-family modes may only restrict the offered set and remain non-production; no native profile selection exists.
5. The response tuple must exactly occur in the offer.
6. Sorted capability list, deterministic digest and schema hash must agree.
7. Native connects only to `gameplay_selection.host/port/tls_server_name`; legacy world routing cannot override it.
8. Contradiction fails before connection.
9. After ticket redeem, selection or credential handoff, adapter binding is immutable and no alternate candidate is attempted.
10. `401`, `409`, `503`, transport/TLS/parser/session failure or ambiguous outcome requires a fresh Identity flow and ticket.

## Rust ownership

### Entry and selection

Owns bounded JSON, transient secret handling, authoritative world/character presentation and exact response validation. Gateway `protocol_version: 1` remains the login API version only. Production preference remains Gateway/World Registry authority.

### Game session

Owns one immutable selected family/native-version/transport/schema/capability identity, endpoint, credential handoff, selected character, command namespace, cancellation and stale-session rejection. Replacement sessions inherit no queue, ID, sequence, snapshot or prediction state.

### Native codec and adapter

The later package owns bootstrap representation, unsigned BE32/protobuf validation, generated IDL mapping, parser state and limits. It owns no sockets, Tokio runtime, UI or authoritative simulation and has no dependency on `protocol-canary`.

### Domain, simulation and UI

Owns protocol-neutral semantics and reversible presentation. Inventory, containers, loot, damage, resources and cooldowns change only from authoritative server events. A socket write never means gameplay success.

## Commands and result evidence

| Intent | Native command | Required evidence |
|---|---|---|
| step/stop | movement command | typed result plus authoritative movement/revision |
| attack/follow | set/clear target command | target/combat state plus terminal result |
| spell | cast command | result lifecycle plus resource/cooldown/effect deltas |
| use/use-with | item-use commands | authoritative item/world/container mutation |
| item move | move-item command | authoritative inventory/container/tile mutation |
| loot | loot command | authoritative transfers or stable rejection |
| chat | chat command | delivered event or rejection |
| logout | logout command | terminal result/session-ended evidence |

Every admitted native command reaches one terminal result unless session termination prevents delivery; termination locally cancels pending commands and never triggers replay. Canary must not fabricate native-style acknowledgements.

## Snapshot, delta and duplicate rules

- stage a snapshot outside committed simulation until chunk indexes, limits and digest over exact received snapshot payload bytes validate;
- apply only deltas whose base revision exactly matches committed state and whose transition is permitted;
- a duplicate, regression, conflict or malformed delta is fatal unless the canonical contract explicitly defines an exact idempotent replay case;
- on a gap send one bounded resync, freeze affected authoritative mutation presentation and accept only contiguous replay or a complete replacement snapshot;
- tag reversible movement prediction by command ID and reconcile from authoritative movement/correction;
- clear all projection, pending-command, resync and prediction state on disconnect/replacement;
- an exact duplicate command result is not reapplied;
- same command ID with different serialized command bytes is fatal;
- no reconnect command replay.

## Parser and backpressure obligations

- validate unsigned 32-bit big-endian frame length before allocation;
- frame/message `<=1 MiB`, complete snapshot `<=16 MiB`, chunks `<=256`, one encoded chunk `<=512 KiB`, protobuf nesting `<=32`;
- reject zero, truncated, oversize, trailing, multiple-envelope, unknown-required-enum, invalid-oneof, invalid UTF-8 and compressed native-v1 input;
- use checked conversions and bounded strings/collections;
- no panic, cursor rewind without progress or busy-loop on external input;
- bounded queues; old-session commands cannot reach replacements;
- cancellation/control cannot starve and semantic commands are not silently dropped or reordered.

## Security and redaction

- no Oteryn password in the client;
- no OAuth token to Gateway/Otheryn;
- Game Login Ticket goes only to Gateway;
- Game Session credential goes only to the selected Otheryn endpoint;
- secrets and account/character/session/command identifiers, chat and payloads do not enter logs, traces, crash reports or fixtures;
- TLS certificate chain, exact SNI and ALPN are validated;
- malformed, ambiguous, replayed, cross-bound or downgrade state fails closed.

## Fixture ownership and rollout

Rust owns cross-language golden encode/decode fixtures, malformed/truncated/oversize/unknown/sequence/snapshot regressions, arbitrary-frame/state-machine fuzzers, deterministic normalized replay, schema provenance and semantic differential Canary journeys where meaningful. Fixtures are synthetic and exclude credentials, identities, endpoints, chat and proprietary captures.

The adapter may merge client-first only while production offers exclude native. Activation requires exact Gateway and Otheryn readiness plus an integrated staging manifest. Rollback removes native from fresh offers/advertisement, drains/closes native sessions and keeps Canary available for fresh explicitly allowed sessions. No active or failed native session switches adapters.

## Later packages

1. corrected Platform/Gateway producer, disabled;
2. Otheryn Game Session v2/native listener and authoritative producer, disabled;
3. Rust `protocol-oteryn` adapter;
4. automatic family selection and exact integrated staging E2E/rollback.

Use the canonical implementation prompts only after Platform correction, Otheryn correspondence and Rust correspondence have merged in that exact order.
