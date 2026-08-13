# Map Observation Contract v1

Coordination ID: `OTS-20260813-world-reconstruction-navigation`.

This is the versioned contract for a local, read-only observation artifact
produced from OTClient's already-decoded `Map`/`Tile` state. It does not define
OTBM IDs, packet parsing, authentication, a network transport, or an action
controller.

## P0 fixture authority

The normative fixture corpus is kept in this repository at
[`fixtures/map_observation_v1`](fixtures/map_observation_v1/README.md). Its
validator is `tools/agents/validate_map_observation_v1_fixtures.py`.

The fixture corpus is the producer's implementation input. A consumer may
adopt the byte-normalized corpus, but P0 does not read, write, or depend on an
external repository to establish this contract: official-Tibia research
coordination is repository-local under `TIBIA_RESEARCH_TRACKS.md`. Therefore,
external consumer integration is a later, separately authorized compatibility
step, not a prerequisite that can block this local contract forever.

## Encoding and common fields

P1 writes one UTF-8 JSON object per line (JSONL), with no BOM. Objects use the
field order shown by the normative fixture. Omit optional fields rather than
serializing `null`. A deterministic fixture never includes a wall-clock value;
runtime records may include `observed_at_unix_ms` as a decimal integer.

Every record contains these fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Literal integer `1`. |
| `record_type` | One of `tile_snapshot`, `tile_delta`, `transition_event`, `navigation_action_result`. |
| `sequence` | Positive, monotonically increasing integer within `session_id`. |
| `session_id` | Opaque non-secret producer-local identifier. It is correlation only, never an account, character, cookie, token, or login value. |
| `producer` | Object with `revision`, `client_version`, and `protocol_version`; all identify the producer/client cut that decoded the observation. |

`producer.revision` is an opaque revision string. `client_version` is a
display/version string and `protocol_version` is a non-negative integer. They
must never be inferred from a packet payload added to an observation.

All `position` values are absolute coordinates: `x` and `y` are integers and
`z` is an integer floor. Relative map offsets are forbidden.

## Tile snapshots and completeness

`tile_snapshot` has `position` and `completeness`.

| Completeness | Required representation | Meaning |
| --- | --- | --- |
| `FULL` | `things` is present and non-empty | The ordered array is the complete observed non-empty tile stack. |
| `EMPTY` | `things: []` | The producer explicitly decoded an empty tile. |
| `PARTIAL` | invalid for a snapshot | Incremental knowledge must use `tile_delta`. |
| `UNKNOWN` | `things` is absent | The producer has no complete tile assertion. |

A `FULL` snapshot with `things: []` is invalid; an explicitly decoded empty tile
must use `EMPTY`. The absence of a record is always `UNKNOWN`; it is never
`EMPTY`. An explicit `UNKNOWN` snapshot is permitted to carry `unknown_reason`,
but it must not carry `things`.

## Ordered things and raw identity

Each `things` element, and each `tile_delta.changes[*].thing` where applicable,
uses this form:

```json
{
  "stack_position": 0,
  "category": "item",
  "identity": { "client_appearance_id": 3031 },
  "subtype": 0,
  "state": {}
}
```

`stack_position` is a non-negative integer and array order is ascending stack
order. `category` is the factual OTClient category (`item`, `creature`,
`effect`, `missile`, or `unknown`). `identity` preserves only raw client-side
identity already decoded by OTClient:

- `client_appearance_id` is an integer appearance/item identifier when known;
- `client_creature_id` is an integer client-local creature identifier when
  known;
- neither is an OTBM ID, a server item ID, or a claim that such a mapping
  exists.

`subtype` and members of `state` are optional factual decoded values. They may
not contain packet blobs, account information, authentication/session material,
or guessed semantic classifications. A producer preserves dynamic things such
as creatures rather than silently treating them as static map content.

## Tile deltas

`tile_delta` has `position`, `completeness: "PARTIAL"`, and a non-empty ordered
`changes` array. Each change has an `operation` of `add`, `change`, or `delete`
and an explicit `stack_position`.

- `add` and `change` require `thing`.
- For `add` and `change`, `thing.stack_position` must equal the enclosing
  `change.stack_position`; disagreement is invalid rather than a precedence
  rule.
- `delete` forbids `thing`.
- A delta is not evidence of the unmentioned stack entries and must not be
  promoted to `FULL` by a producer or consumer.

## Transitions and navigation actions

`transition_event` contains absolute `before_position`, `after_position`, and
`evidence: "decoded_state"`. It records a resulting decoded transition, not
input emission.

`navigation_action_result` contains `requested_action`,
`result` (`succeeded`, `failed`, or `unknown`), and `evidence`. `succeeded`
requires `evidence: "decoded_resulting_state"` plus `result_position`.
Emitting a movement/action input is never success evidence. This record shape
is reserved by P0; P1 does not add movement, interaction, or automation.

## Forbidden data

No record, nested object, diagnostic, filename, or fixture may contain an
account name, email, password, authenticator value, session key, cookie,
authorization header, bearer token, login request/response, raw packet payload,
or proprietary client asset. Persistence failures are local diagnostics only;
they do not create a synthetic observation.

## P1 boundaries

P1 instruments decoded map state around `ProtocolGame::setTileDescription`,
map updates, and `Map`/`Tile` changes. It is disabled by default, failure-safe,
bounded, and local-only. It must not reparse protocol packets, mutate map state,
or directly contact an Atlas service.
