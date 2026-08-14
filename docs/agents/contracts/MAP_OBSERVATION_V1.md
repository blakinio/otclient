# Map Observation Contract v1

Coordination ID: `OTS-20260813-world-reconstruction-navigation`.

This is a producer-neutral, versioned contract for local, read-only semantic world observations. For the current reconstruction programme the authoritative live producer is **Track A `official-client-re`**, whose subject is the official native Linux Tibia client. Track B (`blakinio/otclient` -> Tibia Global compatibility) is not the producer for this programme and is not required for P1.

The contract does not define OTBM IDs, authentication, network transport, autonomous movement, or a particular extraction mechanism. Track A may produce these records only from structurally decoded/verified official-client state with exact client-version evidence. A future OTClient producer may adopt the same format in a separate task without changing Track A ownership.

## Existing Track A reuse

Implementation must reuse rather than duplicate current Track A work where applicable:

- PR #279 / `OTC-20260812-worldmap-reconstruction`: fail-closed official-client worldmap reconstruction pipeline, provenance, repeated-observation merge, static/dynamic separation, client-to-OTB mapping gates, comparisons and OTBM-ready planning.
- PR #283 / `OTC-20260813-tibia-runtime-bridge`: exact-version official Linux client runtime bridge and structural session/state integration boundary.
- current Track A runtime/login continuation resolved from live repository state.

The observation producer must integrate with those lanes through deliberate repository-owned contracts/evidence; it must not take over their mutable runtime or paths.

## P0 fixture authority

The normative fixture corpus is kept in this repository at [`fixtures/map_observation_v1`](fixtures/map_observation_v1/README.md). Its validator is `tools/agents/validate_map_observation_v1_fixtures.py`.

The fixture corpus freezes record semantics. It is not proof that the official client currently exposes every field; unavailable fields remain UNKNOWN until Track A proves them on the exact native-Linux client version.

## Encoding and common fields

P1 writes one UTF-8 JSON object per line (JSONL), with no BOM. Objects use the field order shown by the normative fixture. Omit optional fields rather than serializing `null`. A deterministic fixture never includes a wall-clock value; runtime records may include `observed_at_unix_ms` as a decimal integer.

Every record contains:

- `schema_version`: literal integer `1`;
- `record_type`: `tile_snapshot`, `tile_delta`, `transition_event`, or `navigation_action_result`;
- `sequence`: positive monotonically increasing integer within `session_id`;
- `session_id`: opaque non-secret correlation identifier, never an account/character/cookie/token/login value;
- `producer`: `revision`, `client_version`, and `protocol_version` identifying the exact producer/client cut.

All positions are absolute `x/y/z`. Relative offsets are forbidden in the normalized artifact.

## Tile completeness

- `FULL`: `things` is present and non-empty; complete observed non-empty stack.
- `EMPTY`: `things: []`; producer explicitly proved an empty tile.
- `PARTIAL`: invalid for snapshot; incremental knowledge uses `tile_delta`.
- `UNKNOWN`: `things` absent; producer has no complete assertion.

Absence of a record is UNKNOWN, never EMPTY. A FULL snapshot with an empty `things` array is invalid.

## Ordered things and raw identity

Each thing preserves explicit non-negative `stack_position`, factual category, raw identity already structurally established by Track A, and optional factual decoded subtype/state. Array order is ascending stack order.

Raw identities may include `client_appearance_id` and `client_creature_id`. They are not OTBM IDs or server item IDs. Mapping to OTBM/server identity remains a separately verified step and should reuse the fail-closed mapping policy from PR #279.

Dynamic things such as creatures remain observations and are not silently promoted to static map content.

## Tile deltas

A `tile_delta` has absolute position, `completeness: "PARTIAL"`, and ordered changes with operation `add`, `change`, or `delete` and explicit stack position. Add/change require a matching thing; delete forbids a fabricated thing. A delta cannot be promoted to FULL without separate complete-state evidence.

## Transitions and navigation actions

A `transition_event` requires structurally verified absolute before/after positions and `evidence: "decoded_state"`.

A `navigation_action_result` records semantic requested action plus `succeeded`, `failed`, or `unknown`. Success requires decoded resulting-state evidence and result position. Input emission alone never proves success.

P1 is observation-only. It does not add autonomous movement or interaction. Later navigation work must build on Track A's independently verified native action/state transition capabilities.

## Forbidden data

No observation, diagnostic, filename or fixture may persist account names, email, password, authenticator values, session keys, cookies, authorization headers, bearer tokens, login request/response material, raw secret-bearing packet payloads, or proprietary client assets.

## P1 boundary — Track A

P1 creates an observation producer for the official native Linux Tibia client by extending/reusing the current Track A runtime/worldmap surfaces. It must:

- exact-version fence all structural claims;
- consume verified decoded state rather than screenshots/OCR where structural state is available;
- preserve UNKNOWN when a field is not structurally proven;
- remain local, bounded and failure-safe;
- avoid changing canonical OTBM;
- avoid duplicating PR #279 reconstruction logic;
- avoid duplicating PR #283 bridge/runtime discovery;
- keep Track B PR #284 and its runtime namespace completely independent.

The downstream Otheryn Atlas may consume sanitized promoted observation artifacts in its separately owned project. Live Track A runtime ownership remains in `blakinio/otclient`.
