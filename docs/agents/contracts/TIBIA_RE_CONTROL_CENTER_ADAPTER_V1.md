# TIBIA RE Control Center Adapter Contract v1

```yaml
contract_id: TIBIA-RE-CONTROL-CENTER-ADAPTER-V1
version: 1
status: design_baseline
producer_repository: blakinio/otclient
runtime_authority: external; never granted by this contract
```

## Purpose

Define the stable semantic boundary between the Control Center Scenario Engine and a concrete client adapter. The first implementation target is the official Tibia Track A runtime. A future independently governed implementation may exist in `blakinio/Oteryn-v2`.

The contract deliberately excludes client-specific function addresses, UI coordinates, packet opcodes and wire layouts.

## 1. Adapter identity

Every adapter exposes:

```yaml
adapter_id: string
adapter_kind: OFFICIAL_TIBIA | OTERYN_V2 | FAKE_TEST
adapter_version: string
runtime_instance_id: string | null
session_epoch: string | null
```

`runtime_instance_id` identifies the currently bound runtime instance. A changed instance invalidates outstanding mutation authorization and in-flight assumptions.

## 2. Capability model

Capabilities are explicit and independently versioned for read and action maturity.

```yaml
capability_id: string
available: bool
read_gate: NONE | R0 | R1 | R2 | R3 | R4
action_gate: NONE | A0 | A1 | A2 | A3 | A4
source: string
notes: string | null
```

The gate meanings are inherited from `OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md` for the official adapter. Oteryn may map its own implementation evidence into the same semantic levels for comparison, but must not claim official-client RE proof from Oteryn-only tests.

## 3. Normalized runtime status

```yaml
RuntimeStatus:
  adapter_id: string
  runtime_state: OFFLINE | DEGRADED | ONLINE | UNKNOWN
  client_state: NOT_FOUND | LOGIN_SCREEN | CHARACTER_SELECTION | IN_GAME | UNKNOWN
  recorder_state: STOPPED | RECORDING | ERROR | UNKNOWN
  authority_state: READ_ONLY | MUTATION_ALLOWED | EXPIRED | DENIED | UNKNOWN
  session_epoch: string | null
  runtime_instance_id: string | null
  monotonic_ns: integer
  reasons: [string]
```

For the official Track A adapter, `MUTATION_ALLOWED` is valid only when the current external Track A admission/supervision chain authorizes the exact operation and target. Cached prior success is not sufficient.

## 4. Snapshot model

Adapters return only fields they can source truthfully.

```yaml
GameSnapshot:
  snapshot_id: string
  adapter_id: string
  session_epoch: string | null
  runtime_instance_id: string | null
  monotonic_ns: integer
  client_state: string
  player:
    hp: integer | null
    hp_max: integer | null
    mana: integer | null
    mana_max: integer | null
    soul: integer | null
    capacity: number | null
    stamina_seconds: integer | null
    level: integer | null
    speed: integer | null
    position:
      x: integer | null
      y: integer | null
      z: integer | null
  conditions: object
  action_state: object
  target: object | null
  inventory: object | null
  containers: object | null
  battle_list: object | null
  source_quality:
    field_sources: object
    unknown_fields: [string]
```

Unknown data remains `null`/unknown. Adapters must not synthesize plausible values for UI completeness.

## 5. Semantic action request

```yaml
ActionRequest:
  action_id: string
  run_id: string
  step_id: string
  kind: string
  parameters: object
  timeout_ms: integer
  required_capability: string
  required_authority: READ_ONLY | MUTATION
  expected_runtime_instance_id: string | null
  expected_session_epoch: string | null
```

Initial semantic action kinds:

```text
wait
checkpoint
logout
move
turn
stop_movement
say_controlled_text
cast_spell
use_consumable
eat_food
use_rune
select_target
attack
cancel_attack
follow
cancel_follow
open_container
close_container
use_item
look_item
move_item
equip
unequip
open_panel
close_panel
```

Login/credential-bearing operations are not ordinary action payloads. A future session-capability request may trigger an already-approved external login ingress, but credentials must never be serialized into `ActionRequest` or run artifacts.

## 6. Action result

```yaml
ActionResult:
  action_id: string
  status: PASS | FAIL | REFUSED | TIMEOUT | CANCELLED | UNKNOWN
  dispatched: bool
  authoritative_confirmation: PROVEN | DERIVED | NOT_AVAILABLE | UNKNOWN
  runtime_instance_id: string | null
  session_epoch: string | null
  monotonic_started_ns: integer
  monotonic_finished_ns: integer
  normalized_delta: object | null
  evidence_refs: [string]
  reason_code: string | null
  safe_message: string | null
```

`dispatched=false` is required when a preflight gate refuses the operation.

A successful local function/UI dispatch is not automatically `PASS`; the adapter reports the evidence level available for the requested scenario assertion.

## 7. Required adapter operations

The domain-level adapter surface is logically:

```text
identity() -> AdapterIdentity
capabilities() -> CapabilitySet
runtime_status() -> RuntimeStatus
snapshot(request) -> GameSnapshot
preflight(action_request) -> PreflightResult
execute(action_request, cancellation_token) -> ActionResult
wait_for(condition, timeout, cancellation_token) -> WaitResult
capture_start(policy) -> CaptureSession
capture_stop(capture_session) -> CaptureSummary
emergency_stop(reason) -> StopResult
```

The implementation language/API shape may differ, but these responsibilities must remain distinct.

## 8. Preflight result

```yaml
PreflightResult:
  allowed: bool
  action_id: string
  runtime_instance_id: string | null
  session_epoch: string | null
  authority_state: string
  capability_state: string
  checked_at_monotonic_ns: integer
  reason_codes: [string]
```

For mutating official-client actions, preflight occurs immediately before dispatch and verifies all current Track A requirements applicable to that action. Scenario validation performed minutes earlier does not replace dispatch-time preflight.

## 9. Normalized event envelope

Every emitted event uses:

```yaml
Event:
  schema_version: 1
  event_id: string
  seq: integer
  monotonic_ns: integer
  wall_time: string | null
  adapter_id: string
  runtime_instance_id: string | null
  session_epoch: string | null
  run_id: string | null
  experiment_id: string | null
  step_id: string | null
  kind: SYSTEM | AUTHORITY | ACTION | TRACE | NET | STATE | SCREEN | SNAPSHOT | ASSERTION | RESULT | ERROR
  sensitivity: PUBLIC | RESEARCH_INTERNAL | PERSONAL_REDACTED | SECRET_REJECTED
  payload: object
```

`SECRET_REJECTED` records that secret-class material was refused/redacted; the secret value itself is never placed in `payload`.

## 10. Network event minimum

```yaml
payload:
  direction: CLIENT_TO_SERVER | SERVER_TO_CLIENT
  lane: string | null
  sequence: integer | null
  message_type: string | null
  size: integer
  correlation_id: string | null
  payload_capture: NONE | SANITIZED | APPROVED_NON_SECRET
```

Raw payload capture is not the default. Auth/session-secret-bearing payloads are forbidden in persistent artifacts.

## 11. Scenario step contract

A step is exactly one of:

```yaml
snapshot:
  name: string

action:
  kind: string
  parameters: object
  timeout_ms: integer | null

wait:
  condition: object
  timeout_ms: integer

assert:
  condition: object

checkpoint:
  label: string
```

The Scenario Engine assigns stable `step_id` values during validation.

## 12. Side-effect budget

```yaml
SideEffectBudget:
  max_runtime_seconds: integer
  max_actions: integer
  max_movement_tiles: integer | null
  max_spells: integer | null
  max_consumables: integer | null
  max_items_moved: integer | null
  max_gold: integer
  max_tibia_coins: integer
  max_irreversible_changes: integer
```

The platform refuses a scenario if its declared effects cannot be bounded under the current authority and experiment contract.

## 13. Cancellation and STOP ALL

Cancellation is cooperative but mandatory at every bounded wait/dispatch boundary.

`STOP ALL` behavior:

1. latch a global harness cancellation generation;
2. reject new mutations;
3. cancel queued steps;
4. request cancellation of the active adapter action;
5. stop optional captures after bounded cleanup;
6. emit terminal cancellation events;
7. release task-local resources/locks owned by the harness;
8. do not terminate the official client unless explicit current process-control authority separately allows that exact effect.

A new run requires a new cancellation generation and a fresh authority status.

## 14. Browser/CLI Control API semantics

The transport API must expose domain operations without bypass routes. Minimum logical endpoints/commands:

```text
GET  status
GET  capabilities
GET  scenarios
GET  runs
GET  runs/<id>
POST runs                    start validated scenario
POST runs/<id>/pause
POST runs/<id>/resume
POST runs/<id>/abort
POST experiments/one-step   create one-step scenario
POST stop-all
GET  events                  bounded stream/poll
```

The exact HTTP paths are implementation-specific. Browser controls and CLI commands must call the same backend operations.

## 15. Official-client safety invariants

For `adapter_kind=OFFICIAL_TIBIA`:

- a visible client/window is not authority;
- stale registration/lease/generation cannot authorize dispatch;
- target identity mismatch refuses dispatch;
- read-only admission never escalates to mutation;
- GUI input must use the current shared lock/guard contract;
- action parity/evidence gates remain external proof requirements;
- credentials/login secrets never cross this adapter contract;
- authority loss during a scenario aborts subsequent mutation steps.

## 16. Oteryn-v2 invariants

For `adapter_kind=OTERYN_V2`:

- implementation belongs to a separate task/PR in `blakinio/Oteryn-v2`;
- it exposes test semantics without adding Tibia wire compatibility;
- server-authoritative outcomes remain authoritative where Oteryn architecture requires them;
- test-control hooks must not become unauthenticated production remote-control surfaces;
- comparison uses normalized semantic states/transitions, not raw packet equality.

## 17. Compatibility

Contract v1 is additive-only within the major version. Removing/renaming action kinds, event fields or required safety semantics requires a new major contract and migration plan.

Adapters advertise their supported contract versions. The Scenario Engine fails closed when no compatible version exists.
