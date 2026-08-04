# Rust client native gameplay protocol correspondence

Coordination ID: `OTS-20260804-native-protocol-selection`  
Canonical source of truth: `blakinio/Oteryn-Platform/docs/contracts/OTERYN_NATIVE_GAMEPLAY_PROTOCOL_CONTRACT.md`  
Canonical review PR: `blakinio/Oteryn-Platform#519`  
Otheryn producer correspondence: `blakinio/Otheryn/docs/contracts/OTERYN_NATIVE_GAMEPLAY_PROTOCOL_CORRESPONDENCE.md`  
Otheryn review PR: `blakinio/Otheryn#356`

## Status

Contract correspondence only. The Rust workspace still has no `protocol-oteryn` crate and this task adds no dependency, runtime, transport, codec, Gateway request/response or gameplay behavior.

`protocol-canary` remains the current source-proven compatibility adapter. Native `oteryn.native.v1` is a separate future adapter family.

## Normative adoption

The Rust client adopts the canonical contract for:

- bounded client candidate offer and authoritative Gateway selection;
- distinction among Gateway API version, Game Session contract version, adapter family, profile, transport, schema and build metadata;
- Game Session v2 bind-on-first-admission semantics;
- exact native TLS/framing/protobuf identifiers and limits;
- command IDs, client/stream/server sequences, server tick and state revision;
- action result lifecycle and stable reason codes;
- initial snapshot, deltas, prediction reconciliation and bounded resync;
- no native v1 resume or command replay;
- no password fallback, byte sniffing, post-ticket retry or in-session adapter switch;
- exact-pair compatibility evidence and staged rollout.

If this document differs from the merged canonical contract, the canonical revision controls. Every implementation task must pin the exact Platform contract commit, Otheryn producer commit and schema SHA-256.

## Current Rust boundary

The accepted client architecture remains:

```text
application / game-session orchestration
  -> production selection policy
  -> protocol-neutral transport/session supervisor
  -> selected framing/session codec
  -> selected independent protocol adapter
  -> normalized GameCommand / GameEvent
  -> game domain and simulation
```

Current-versus-target:

| Area | Current | Native target |
|---|---|---|
| adapters | `protocol-canary` plus protocol-neutral contracts | independent `protocol-oteryn`; neither depends on the other |
| transport | current worker transport until the separate Tokio package merges | one protocol-neutral runtime/supervisor; native TLS codec selected by profile |
| Gateway request | Gateway API v1 ticket login | optional bounded `gameplay_offer` in the same API request |
| Gateway response | session/worlds/characters | distinct `game_session_contract_version` and authoritative `gameplay_selection` |
| session bootstrap | Canary-compatible session/profile behavior | native `ClientHello` with exact selected binding and character ID |
| action completion | only source-proven effects from Canary packets | explicit native action result lifecycle plus state deltas |
| state entry | Canary packet sequence | complete revisioned native snapshot |
| reconnect | current session policy | fresh ticket/selection/session/full snapshot; no v1 resume |

## Client offer and selection validation

Production `Auto` builds a bounded set from exact compiled support. It does not expose arbitrary user-entered identifiers.

For each offered candidate, the client records:

```text
family
profile
transport
schema_revision
schema_sha256
supported capabilities
compiled adapter/codec availability
exact fixture manifest revision
```

Rules:

1. the offer contains `1..8` unique canonical candidates and `<=64` capabilities per candidate;
2. offer order is not preference; Gateway World Registry order is authoritative;
3. a development force mode restricts the offer but cannot force Gateway acceptance;
4. the selected result must be an exact member of the offer and pass all endpoint, schema, capability and size validation;
5. contradiction or unsupported selection fails before opening the gameplay connection;
6. after ticket consumption/Gateway response, no alternate candidate is attempted;
7. a new attempt obtains a fresh ticket and authoritative selection.

## Rust ownership split

### Gateway/entry consumer

Owns bounded JSON request/response, transient ticket/session secrets, authoritative world/character presentation and exact selection validation. It never treats Gateway API `protocol_version: 1` as gameplay v1.

### Selection policy

Owns `Auto` intersection support and diagnostic force modes. It receives authoritative selection; it does not inspect gameplay bytes or silently alter family/profile.

### Game session

Owns one immutable selected protocol identity, session credential handoff, selected character, command namespace, cancellation and stale-session rejection. A replacement session cannot inherit queues, IDs, sequences or prediction state.

### Native codec/adapter

The later `protocol-oteryn` package owns TLS/profile bootstrap representation, BE32/protobuf frame validation, exact IDL encode/decode, command/action/state mappings and parser limits. It does not own sockets, Tokio, UI or authoritative simulation.

### Domain/simulation/UI

Own protocol-neutral meaning and reversible presentation. Inventory, containers, loot, damage, resources and cooldowns change only from authoritative server events. UI may show pending intent but cannot claim success from a socket write.

## Native command mapping

| Domain intent | Native wire command | Client completion evidence |
|---|---|---|
| step/stop | `StepCommand` / `StopMovementCommand` | action result plus authoritative entity movement/state revision |
| attack/follow | set/clear target commands | target/combat delta and terminal command result |
| spell | `CastSpellCommand` | accepted/rejected/delayed/effect/completed sequence and authoritative resource/cooldown/effect deltas |
| use/use-with | `UseCommand` / `UseWithCommand` | authoritative item/container/world mutations |
| item move | `MoveItemCommand` | authoritative inventory/container/tile mutation |
| quick/corpse loot | loot commands | authoritative item transfers or stable rejection |
| chat | `SayCommand` | authoritative delivered chat event or rejection |
| logout | `LogoutCommand` | completed/session-ended evidence |

Canary behavior remains honest: it must not fabricate native-style acknowledgements when the exact Canary packets do not provide them.

## Snapshot/delta consumer rules

- hold the initial snapshot outside committed simulation until chunk order, bounds and SHA-256 validate;
- apply deltas only when `base_revision` equals the committed revision;
- ignore only exact duplicate revision/hash; conflicting duplicate is fatal;
- on a gap, send one bounded resync request, freeze authoritative mutation presentation and accept only a complete replacement snapshot;
- tag reversible movement prediction with command ID and reconcile from authoritative movement/delta evidence;
- never merge an incomplete snapshot with old session state;
- clear all session projection, pending commands and prediction on disconnect/replacement.

## Parser and backpressure obligations

- validate frame length before allocation;
- cap frame at 1 MiB, snapshot at 16 MiB/256 chunks and protobuf nesting at 32;
- reject compressed native v1 frames;
- use checked conversions and bounded strings/collections;
- no panic on malformed external input;
- no cursor rewind/busy-loop without progress;
- transport/session queues remain bounded and stale-session commands cannot reach a replacement session;
- control/cancellation cannot be starved; semantic commands are not silently dropped/reordered.

## Fixture ownership

Rust owns:

- cross-language golden decode/encode fixtures for every supported native message;
- malformed/truncated/oversize/unknown/sequence/snapshot regression fixtures;
- arbitrary-frame parser and state-machine fuzz entry points;
- deterministic normalized command/event replay;
- exact schema SHA-256 and generated-code provenance;
- differential semantic journeys against Canary where semantics overlap, without byte-equality claims.

Fixtures are synthetic and exclude credentials, real identifiers, endpoints, chat and proprietary captures.

## Rollout

- the adapter may merge client-first only while production `Auto` does not offer native;
- a client never offers native unless the exact adapter, codec, schema and required capabilities are compiled and tested;
- activation requires exact Platform/Gateway and Otheryn producer readiness plus integrated staging manifest;
- rollback removes native from fresh offers/advertisement, drains or closes active sessions and retains Canary for fresh explicitly selected sessions;
- no active or failed native session switches to Canary.

## Later tasks

After all contract PRs merge and archive:

1. Platform/Gateway producer extension;
2. Otheryn native producer/session enforcement;
3. Rust `protocol-oteryn` adapter;
4. automatic selection and exact integrated E2E.

Use the ready-to-run prompts in `blakinio/Oteryn-Platform/docs/agents/prompts/` at the exact merged contract revision.
