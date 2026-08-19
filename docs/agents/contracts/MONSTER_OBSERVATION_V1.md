# MONSTER_OBSERVATION_V1

```yaml
contract: MONSTER_OBSERVATION_V1
version: 1.0.0
programme: OTCLIENT-TIBIA-RE
track: official-client-re
subject: official native Linux Tibia client only
contract_kind: append_only_research_evidence
runtime_producer_status: NOT_IMPLEMENTED
schema: docs/agents/contracts/MONSTER_OBSERVATION_V1.schema.json
```

## Purpose

`MONSTER_OBSERVATION_V1` is the canonical normalized evidence envelope for future Track A monster/world observation. It records what the official client was proven to know at a time boundary without converting an inbound create/delete/update into a server-spawn claim.

The contract is intentionally evidence-first:

```text
official-client semantic/protocol observation
  -> MONSTER_OBSERVATION_V1 append-only records
  -> deterministic offline normalization
  -> spawn inference
  -> mechanics inference
  -> independently validated behavioral fixtures
```

The record stream is not a packet capture and must not contain raw credential/session material, private chat, account identifiers or proprietary binary bytes.

## Authority boundary

A record can prove only its declared source and observation context. It does not prove server implementation internals.

Use these evidence labels consistently:

```text
DIRECT       value/event directly decoded from a proven client model/message/handler
CORRELATED   value/event correlated across two or more proven client layers
DERIVED      deterministic transformation of DIRECT/CORRELATED records
UNKNOWN      evidence is insufficient or contradictory
```

A historical static symbol, address, QMeta hit or message name is not a `DIRECT` live observation on a different client SHA. Every physical producer must be exact-build fenced and re-resolved after restart/update/ASLR as required by current Track A governance.

## Privacy and secret minimization

Forbidden fields or payloads include:

- account email/login;
- password, 2FA or device-confirmation values;
- cookies, tokens, play-session values, session keys or authentication blobs;
- character name or account identity unless a future separately reviewed contract proves it is indispensable;
- private/channel/NPC chat text;
- unrelated player names;
- raw packet payloads when semantic fields are sufficient;
- raw process-memory dumps;
- proprietary official-client binary/assets.

Monster names may be added only when the producer has already classified the entity as `MONSTER` and the name is static/non-personal game metadata. Prefer stable race/type/appearance identifiers when available.

## Record envelope

Every record has the following conceptual envelope. The JSON Schema is normative for machine validation; this document defines semantics.

```yaml
schema: MONSTER_OBSERVATION_V1
record_id: <unique producer-local string>
record_type: <enum>
time:
  monotonic_ns: <non-negative integer>
  wall_time_utc: <optional RFC3339 UTC timestamp>
client:
  version: <exact current official client version string>
  sha256: <64 lowercase hex>
  size: <positive integer>
runtime:
  observation_epoch_id: <unique per structural IN_GAME observation epoch>
  process_epoch_id: <changes after process restart>
  world_key: <non-secret stable label or UNKNOWN>
source:
  evidence: DIRECT | CORRELATED | DERIVED | UNKNOWN
  layer: PROTOCOL | RUNTIME_MODEL | BRIDGE | OBSERVER | INFERENCE
  message_type: <optional semantic type>
  handler_or_model: <optional proven semantic owner>
coverage: <coverage context>
position: <optional world coordinate>
creature: <optional creature state>
player: <optional non-identifying player spatial state>
stimulus: <optional controlled stimulus marker>
notes: <optional bounded non-sensitive code/reason string>
```

`record_id` is evidence identity, not a global creature identity.

## Observation epochs

An observation epoch is the maximum interval in which the producer can prove all required observation prerequisites without an unclassified discontinuity.

Start a new `observation_epoch_id` after at least:

- client process restart;
- client update/change of exact SHA;
- logout/relogin or game-world session replacement;
- disconnect/reconnect whose continuity cannot be structurally proven;
- observer/bridge restart when event loss cannot be excluded;
- loss and reacquisition of authoritative runtime identity;
- any provenance discontinuity that can hide create/delete/move events.

Never join respawn intervals across epochs merely because the same monster type or coordinate appears later.

## Record types

Normative `record_type` values:

```text
EPOCH_START
EPOCH_END
COVERAGE_START
COVERAGE_UPDATE
COVERAGE_END
PLAYER_POSITION
CONTROL_STIMULUS
CREATURE_CREATE
CREATURE_MOVE
CREATURE_UPDATE
CREATURE_HEALTH
CREATURE_TYPE
CREATURE_DELETE
```

Additional types require a contract version change.

### `EPOCH_START` / `EPOCH_END`

Mark the structural observation epoch. `EPOCH_START` is valid only after the physical producer has independently proven the exact current client/runtime identity and the task's required live-state gate. `EPOCH_END` records a reason code when known.

### Coverage records

Coverage records exist because `CREATURE_CREATE` alone cannot distinguish a true spawn from first synchronization after the player/viewport arrives.

A coverage record declares a region/tile continuity token and one of:

```text
UNKNOWN
VISIBLE_RENDERED
DECODED_CURRENT
DECODED_CACHE
CONTINUOUS_CONFIRMED
```

`CONTINUOUS_CONFIRMED` is the only state that may support an exact observed respawn interval. It requires the producer to prove that no relevant event for the declared tile/region could have been missed since `continuous_since_monotonic_ns`.

`VISIBLE_RENDERED` by itself is weaker than decoded semantic coverage and must not be treated as complete event coverage.

### Creature records

`CREATURE_CREATE`, `MOVE`, `UPDATE`, `HEALTH`, `TYPE`, and `DELETE` describe client-observed lifecycle events.

The producer assigns an `observation_instance_id` at the first locally observed lifecycle event. A protocol/client `creature_id` is retained only as an ephemeral source identifier. It must never be assumed to identify one persistent server monster across deletion, relog, epoch change or ID reuse.

Recommended fields when proven:

```yaml
creature:
  observation_instance_id: <local lifecycle id>
  client_creature_id: <optional non-negative integer>
  class: MONSTER | PLAYER | NPC | SUMMON | UNKNOWN
  race_id: <optional non-negative integer>
  type_id: <optional non-negative integer>
  appearance_id: <optional non-negative integer>
  semantic_name: <optional, MONSTER only>
  hp_percent: <optional 0..100>
  speed: <optional non-negative integer>
  direction: NORTH | EAST | SOUTH | WEST | UNKNOWN
  target_relation: ATTACKING_LOCAL_PLAYER | ATTACKED_BY_LOCAL_PLAYER | OTHER | UNKNOWN
```

A field omitted or marked unknown is better than a guessed value.

## Position semantics

World coordinates are represented as integer `x`, `y`, `z` plus position evidence:

```text
DIRECT
CORRELATED
DERIVED
UNKNOWN
```

A creature event may be recorded without XYZ if current authoritative position is not proven. The producer must not copy a render/camera/minimap coordinate and label it world XYZ without causal validation.

## Coverage context on creature events

Every creature lifecycle record must state the coverage context for the affected position or `UNKNOWN`.

Required semantics:

```yaml
coverage:
  mode: UNKNOWN | VISIBLE_RENDERED | DECODED_CURRENT | DECODED_CACHE | CONTINUOUS_CONFIRMED
  continuity_token: <string or UNKNOWN>
  tile_observed: true | false | null
  continuous_since_monotonic_ns: <integer or null>
  last_gap_reason: NONE | VIEWPORT_EXIT | FLOOR_CHANGE | DISCONNECT | RELOGIN | CLIENT_RESTART | CACHE_EVICTION | OBSERVER_RESTART | TARGET_UNPROVEN | UNKNOWN
```

Any non-`NONE` gap invalidates exact continuity until a new `COVERAGE_START` establishes a fresh token.

## Appearance context

For every `CREATURE_CREATE`, classify the strongest supported appearance context:

```text
INITIAL_SYNC
VISIBILITY_GAIN
AFTER_COVERAGE_GAP
CONTINUOUS_COVERAGE_CREATE
UNKNOWN
```

Only `CONTINUOUS_COVERAGE_CREATE` can become a direct input to a same-epoch exact respawn observation. It is still not itself proof that the server's internal spawn timer created that creature; the spawn inference layer additionally needs a preceding terminal lifecycle/death boundary and repeated controls.

## Disappearance context

For every `CREATURE_DELETE`, classify:

```text
SERVER_DELETE_DURING_COVERAGE
VISIBILITY_LOSS
FLOOR_CHANGE
DISCONNECT
RELOGIN
CLIENT_RESTART
CACHE_EVICTION
UNKNOWN
```

`SERVER_DELETE_DURING_COVERAGE` does not automatically mean death. Death evidence is separate.

## Death evidence

When the client exposes enough evidence, record one of:

```text
NONE
EXPLICIT_SERVER_EVENT
ZERO_HP_CORRELATED
CORPSE_TRANSITION_CORRELATED
COMBAT_EVENT_CORRELATED
UNKNOWN
```

A mechanics/spawn inference may require a minimum death evidence class. `CREATURE_DELETE` alone is not a death event.

## Controlled stimulus markers

`CONTROL_STIMULUS` may mark a harmless, separately authorized and already-performed physical action so offline inference can align observations. It contains semantic labels only, for example:

```text
PLAYER_STEP_NORTH
PLAYER_STEP_EAST
PLAYER_STOP
TARGET_MONSTER
CANCEL_TARGET
NO_STIMULUS_BASELINE
```

The evidence contract never authorizes the action. Physical stimuli remain RUNTIME-owned and must satisfy then-current Track A admission, safety and side-effect budgets.

## Append-only ordering and loss detection

A producer should emit a strictly increasing `producer_sequence` in addition to `monotonic_ns` when technically possible. Sequence gaps, queue overflow, observer restart or backpressure loss must emit an epoch/coverage discontinuity rather than be hidden.

Rules:

1. never reorder source observations to make a cleaner lifecycle;
2. deterministic offline normalization may add `DERIVED` records but must preserve source record IDs;
3. duplicate source delivery is retained or deterministically deduplicated with an explicit provenance link;
4. any unknown record-loss window invalidates continuity-dependent respawn claims;
5. clock changes do not affect intervals because monotonic time is authoritative.

## Spawn inference inputs

The raw contract never writes `spawn=true`. Spawn inference consumes only normalized records and may produce a separate result with one of:

```text
OBSERVED_APPEARANCE
RESPAWN_CANDIDATE
RESPAWN_OBSERVED
SPAWN_REGION_INFERRED
SERVER_SPAWN_RULE_UNKNOWN
```

Promotion rules are defined in `docs/agents/programs/OTCLIENT_TIBIA_RE_MONSTER_SPAWN_MECHANICS.md`.

## Mechanics inference inputs

Mechanics inference may consume position/lifecycle/health/speed/target/stimulus evidence and output empirical models. It must keep the following distinction explicit:

```text
OBSERVED_BEHAVIOR != PROVEN_SERVER_ALGORITHM
```

For example, repeated return-to-area behavior can support an empirical leash model; it does not prove the server variable name, home-coordinate representation, pathfinder implementation or exact hidden range rule.

## Versioning

Breaking changes to field meaning, required fields, record types, continuity semantics or privacy rules require a major contract version. Additive optional semantic fields require at least a minor version.

Every evidence artifact records the exact contract version and the exact client SHA from which the source records were produced.

## Completion boundary

This contract defines research evidence only. It does not implement a recorder, prove a current live creature resolver, authorize physical observation, establish a current client ABI, extract a server spawn table or implement any Oteryn server behavior.
