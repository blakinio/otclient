# TIBIA RE Control Center Adapter Contract v1

```yaml
contract_id: TIBIA-RE-CONTROL-CENTER-ADAPTER-V1
version: 1.1
major_version: 1
status: hardened_design_baseline
producer_repository: blakinio/otclient
runtime_authority: external; never granted by this contract
execution_semantics: docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
```

## Purpose

Define the stable semantic boundary between the Control Center domain/Scenario Engine and concrete client adapters.

This contract deliberately excludes client-specific function addresses, UI coordinates, raw keycodes, QMeta IDs, vtables, packet opcodes and wire layouts from common scenarios.

Normative execution/concurrency/idempotency/cancellation/budget/privacy rules live in `TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md` and apply to every implementation of this adapter contract.

## 1. Version negotiation

Adapters advertise:

```yaml
supported_contracts:
  adapter_contract_major: [1]
  execution_contract_major: [1]
```

The Scenario Engine fails closed when there is no mutually supported major version.

Minor-version additions are additive. Unknown required fields or unsupported required semantics fail closed rather than being silently ignored.

## 2. Adapter identity

```yaml
AdapterIdentity:
  adapter_id: string
  adapter_kind: OFFICIAL_TIBIA | OTERYN_V2 | FAKE_TEST
  adapter_version: string
  adapter_generation: string
  runtime_instance_id: string | null
  session_epoch: string | null
```

`adapter_generation` changes whenever adapter process/runtime binding state changes in a way that can invalidate queued assumptions.

A changed `adapter_generation`, `runtime_instance_id` or `session_epoch` invalidates pending mutation dispatch unless the scenario explicitly revalidates and creates a new action.

## 3. Generic capability model

Generic semantic support is independent for reads and actions:

```yaml
Capability:
  capability_id: string
  semantic_version: string
  read_supported: bool
  action_supported: bool
  source: string
  notes: string | null
```

`read_supported=true` never implies `action_supported=true`.

### 3.1 Official-client evidence extension

Only `OFFICIAL_TIBIA` uses the Track A RE maturity extension:

```yaml
OfficialEvidenceExtension:
  capability_id: string
  read_gate: NONE | R0 | R1 | R2 | R3 | R4
  action_gate: NONE | A0 | A1 | A2 | A3 | A4
  evidence_refs: [string]
```

The gate meanings are inherited from `OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md`.

`OTERYN_V2` and `FAKE_TEST` must not be forced to claim Track A R/A evidence grades.

## 4. Normalized runtime status

```yaml
RuntimeStatus:
  adapter_id: string
  adapter_generation: string
  runtime_state: OFFLINE | DEGRADED | ONLINE | UNKNOWN
  client_state: NOT_FOUND | LOGIN_SCREEN | CHARACTER_SELECTION | IN_GAME | UNKNOWN
  recorder_state: STOPPED | RECORDING | ERROR | UNKNOWN
  authority_state: READ_ONLY | MUTATION_ALLOWED | EXPIRED | DENIED | UNKNOWN
  session_epoch: string | null
  runtime_instance_id: string | null
  observed_monotonic_ns: integer
  freshness: FRESH | STALE | UNKNOWN
  reasons: [string]
```

For `OFFICIAL_TIBIA`, `MUTATION_ALLOWED` is informational status only. It is never standing dispatch authority. The exact operation/target must still pass current Track A authority inside the final dispatch boundary.

## 5. Snapshot model

Adapters return only fields they can source truthfully.

```yaml
GameSnapshot:
  schema_version: 1
  snapshot_id: string
  adapter_id: string
  adapter_generation: string
  session_epoch: string | null
  runtime_instance_id: string | null
  source_timestamp: integer | string | null
  source_clock_domain: string | null
  ingested_monotonic_ns: integer
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
  conditions: object | null
  action_state: object | null
  target: object | null
  inventory: object | null
  containers: object | null
  battle_list: object | null
  source_quality:
    field_sources: object
    unknown_fields: [string]
    stale_fields: [string]
```

Unknown data remains `null`/unknown. Adapters must never synthesize plausible values for UI completeness.

## 6. Dispatch fence

Every action binds immutable expected execution fences:

```yaml
DispatchFence:
  expected_control_generation: integer
  expected_adapter_generation: string
  expected_runtime_instance_id: string | null
  expected_session_epoch: string | null
```

Official Track A lease/registration/Gate/target identity fields remain official-adapter internals and are validated from current trusted-base sources at final dispatch. They do not become generic scenario fields.

## 7. Semantic action request

```yaml
ActionRequest:
  schema_version: 1
  action_id: string
  run_id: string
  step_id: string
  kind: string
  parameters: object
  timeout_ms: integer
  required_capability: string
  required_authority: READ_ONLY | MUTATION
  dispatch_fence: DispatchFence
  max_effect: object
```

`action_id` is the idempotency key for one logical action and is governed by the execution contract.

`max_effect` is the engine-computed conservative maximum plausible effect reservation for applicable side-effect-budget dimensions.

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

Login/credential-bearing operations are not ordinary action payloads. A future session-capability request may invoke an independently approved external ingress, but credentials must never be serialized into `ActionRequest`, events or artifacts.

## 8. Action lifecycle

Logical lifecycle:

```text
CREATED
VALIDATED
RESERVED
DISPATCHING
DISPATCHED
CONFIRMING
CONFIRMED
```

Terminal/exceptional states:

```text
REFUSED
CANCELLED_BEFORE_DISPATCH
CANCELLED_AFTER_DISPATCH
FAILED_BEFORE_DISPATCH
FAILED_AFTER_DISPATCH
TIMED_OUT_BEFORE_DISPATCH
TIMED_OUT_AFTER_DISPATCH
AMBIGUOUS
```

`AMBIGUOUS` means the platform cannot prove whether the external side effect occurred and must never trigger automatic mutation retry.

## 9. Action result

```yaml
ActionResult:
  schema_version: 1
  action_id: string
  lifecycle_state: string
  status: PASS | FAIL | REFUSED | TIMEOUT | CANCELLED | AMBIGUOUS | UNKNOWN
  dispatch_state: NOT_DISPATCHED | DISPATCHED | POSSIBLY_DISPATCHED
  authoritative_confirmation: PROVEN | DERIVED | NOT_AVAILABLE | UNKNOWN
  control_generation: integer
  adapter_generation: string
  runtime_instance_id: string | null
  session_epoch: string | null
  monotonic_started_ns: integer
  monotonic_finished_ns: integer
  normalized_delta: object | null
  budget_effect: object
  evidence_refs: [string]
  reason_code: string | null
  safe_message: string | null
```

`dispatch_state=NOT_DISPATCHED` is required when refusal/failure is proven before the irreversible boundary.

A successful local function/UI call is not automatically `PASS`; PASS requires the scenario's declared success evidence.

## 10. Required adapter operations

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

### 10.1 Preflight semantics

`preflight()` is advisory/diagnostic only. It may reject impossible work early but never grants standing dispatch authority.

```yaml
PreflightResult:
  allowed_now: bool
  action_id: string
  adapter_generation: string
  runtime_instance_id: string | null
  session_epoch: string | null
  authority_state: string
  capability_state: string
  checked_at_monotonic_ns: integer
  reason_codes: [string]
```

### 10.2 Execute semantics

`execute()` is the only adapter operation permitted to cross a semantic mutation boundary and must implement or delegate to the execution contract's `atomic_dispatch` semantics.

Immediately before irreversible mutation, it revalidates the complete `DispatchFence`, cancellation generation, idempotency ledger/budget reservation through the caller/coordinator, and for `OFFICIAL_TIBIA` all current Track A authority/identity/input-lock requirements inside the existing guarded mutation boundary.

A prior `preflight.allowed_now=true` is never sufficient.

## 11. Typed scenario step contract

A step is exactly one of:

```yaml
snapshot:
  name: string

action:
  kind: string
  parameters: object
  timeout_ms: integer | null

wait:
  condition: Predicate
  timeout_ms: integer

assert:
  condition: Predicate

checkpoint:
  label: string
```

Typed predicate baseline:

```yaml
Predicate:
  field: string
  op: EQ | NE | LT | LTE | GT | GTE | EXISTS | NOT_EXISTS | CHANGED | UNCHANGED | IN_SET | CONTAINS
  value: scalar | list | null
  unknown_policy: FAIL | WAIT | ACCEPT
```

Rules:

- unknown never silently equals a concrete value;
- mutation-safety predicates cannot use `ACCEPT`;
- assertions default to `FAIL` on unknown;
- waits may use `WAIT` until timeout;
- stable `step_id` is derived deterministically during validation.

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

The normative ledger/accounting rules are in the execution contract.

If an action cannot provide a conservative maximum plausible effect for every applicable hard budget, it is refused before dispatch.

Timeout/failure/cancellation after possible dispatch consumes the conservative uncertain reservation for future admission.

## 13. Cancellation and STOP ALL

Cancellation is mandatory at every engine wait and dispatch boundary.

`STOP ALL` uses the execution contract's linearizable `control_generation` transition.

The adapter's `emergency_stop()` is cooperative cleanup/cancellation assistance only. It must not create a second global STOP implementation or independently kill the official client.

A stale-generation completion may be recorded as evidence but cannot advance a newer run.

## 14. Normalized event envelope

Every emitted event uses:

```yaml
Event:
  schema_version: 1
  event_id: string
  ingest_seq: integer
  ingested_monotonic_ns: integer
  wall_time: string | null
  source_timestamp: integer | string | null
  source_clock_domain: string | null
  source_sequence: integer | null
  source_sequence_scope: string | null
  ordering_confidence: KNOWN | PARTIAL | UNKNOWN
  late: bool
  adapter_id: string
  adapter_generation: string
  runtime_instance_id: string | null
  session_epoch: string | null
  control_generation: integer
  run_id: string | null
  experiment_id: string | null
  step_id: string | null
  stimulus_id: string | BACKGROUND | null
  kind: SYSTEM | AUTHORITY | ACTION | TRACE | NET | STATE | SCREEN | SNAPSHOT | ASSERTION | RESULT | ERROR
  sensitivity: PUBLIC | RESEARCH_INTERNAL | PERSONAL_REDACTED | SECRET_REJECTED
  payload: object
```

`ingest_seq` is recorder persistence order only. It must not be represented as proof of source causality.

`SECRET_REJECTED` contains metadata about rejection only; never the secret value, hash or reversible derivative.

## 15. Causal event payload extension

For causal Track A RE, preserve when observable:

```yaml
message_direction: CLIENT_TO_SERVER | SERVER_TO_CLIENT | LOCAL | null
message_sequence: integer | null
message_type: string | null
connection_lane: string | null
thread_id: string | integer | null
handler: string | null
runtime_object: string | null
object_instance_epoch: string | null
before_state_hash: string | null
after_state_hash: string | null
semantic_delta: object | null
evidence_ref: string | null
```

These fields implement the requirements of `OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md` without implying that every event source can populate every field.

## 16. Network event minimum

```yaml
payload:
  direction: CLIENT_TO_SERVER | SERVER_TO_CLIENT
  lane: string | null
  source_sequence: integer | null
  message_type: string | null
  size: integer
  correlation_id: string | null
  payload_capture: NONE | SANITIZED | APPROVED_NON_SECRET
```

Default is `NONE`.

`message_type` is present only when structurally known. Do not guess it from timing alone.

Raw payload fallback is forbidden. Auth/session-secret-bearing payloads are forbidden in persistent artifacts.

## 17. Privacy construction boundary

Secret/personal classification occurs before normal event/error/artifact construction.

Requirements:

- arbitrary exception/repr/debug output is untrusted and not directly persisted;
- `safe_message` must be sanitized/reviewed safe text;
- environment-variable values are never copied into normal evidence;
- login/auth capture is structural only;
- trace strings are filtered before Event creation;
- private chat is omitted/redacted before Event creation unless explicitly generated test text is permitted;
- screenshots with uncertain login/auth content use a quarantine/refusal path outside normal run artifacts;
- export-time redaction is defense in depth only.

## 18. Run finalization and late events

Run lifecycle:

```text
ACTIVE -> CLOSING -> FINALIZED
```

During bounded `CLOSING`, sources may emit `late=true` events and watermarks where available.

Late events cannot rewrite an already terminal action result or restart execution.

After `FINALIZED`, additional evidence is append-only supplement material referencing the original run.

## 19. Browser/CLI Control API semantics

Browser and CLI must call the same backend domain operations.

Minimum logical operations:

```text
GET  /v1/status
GET  /v1/capabilities
GET  /v1/scenarios
GET  /v1/runs
GET  /v1/runs/<id>
GET  /v1/actions/<action_id>
POST /v1/runs
POST /v1/runs/<id>/pause
POST /v1/runs/<id>/resume
POST /v1/runs/<id>/abort
POST /v1/experiments/one-step
POST /v1/stop-all
POST /v1/reset-stop
GET  /v1/events
```

Exact HTTP spelling may differ if one equivalent versioned API is chosen, but semantics must include:

- bounded request bodies/collections;
- bounded streams/history;
- idempotency for mutation-capable POSTs;
- duplicate-request result replay;
- deterministic malformed-input errors;
- no raw adapter/action bypass;
- loopback default;
- fail-closed remote-exposure policy.

## 20. Official-client safety invariants

For `adapter_kind=OFFICIAL_TIBIA`:

- visible process/window is not authority;
- stale lease/registration/generation cannot authorize dispatch;
- changed boot/PID/start/executable/window/display/session/runtime identity refuses stale work;
- read-only admission never escalates to mutation;
- final mutation validation occurs inside the current canonical Track A guarded mutation boundary;
- GUI input uses the current shared lock/guard contract;
- action parity/evidence gates remain external proof requirements;
- credentials/login secrets never cross this semantic adapter contract;
- authority loss prevents subsequent mutation steps;
- ambiguous possible dispatch is not automatically retried.

## 21. Oteryn-v2 invariants

For `adapter_kind=OTERYN_V2`:

- implementation belongs to a separate task/PR in `blakinio/Oteryn-v2`;
- it integrates with Oteryn's accepted `ADR-0007` E2E architecture or a versioned cross-repo semantic boundary;
- it exposes semantic test intent without adding Tibia wire compatibility;
- server-authoritative outcomes remain authoritative;
- test hooks cannot create an unauthenticated production control surface;
- production-default builds exclude/disable test-only mutation/control hooks according to Oteryn governance;
- comparison uses normalized semantics, not raw packet/internal-layout equality;
- generic capability support is used without pretending Oteryn has Track A R/A maturity.

## 22. Differential comparison contract

Comparison profiles classify fields using:

```text
EXACT
NORMALIZED_EXACT
SET_EQUIVALENT
ORDERED_EQUIVALENT
TOLERANCE
REFERENCE_ONLY
NOT_COMPARABLE
```

Default baseline:

```text
position                 NORMALIZED_EXACT
hp                       NORMALIZED_EXACT
mana                     NORMALIZED_EXACT
conditions               SET_EQUIVALENT or profile NORMALIZED_EXACT
target_state              NORMALIZED_EXACT
inventory                 NORMALIZED_EXACT
containers                ORDERED_EQUIVALENT when order/index is semantic
equipment                 NORMALIZED_EXACT
cooldown_state            NORMALIZED_EXACT
cooldown_timing           TOLERANCE
visual_effect_semantics   REFERENCE_ONLY unless both sides expose stable semantics
pixel/frame output        NOT_COMPARABLE by default
latency                   TOLERANCE or REFERENCE_ONLY
protocol bytes            NOT_COMPARABLE
internal object layout    NOT_COMPARABLE
renderer implementation  NOT_COMPARABLE
```

A field is a mismatch only when both sides claim the field observable/supported at the same normalized checkpoint, neither is UNKNOWN and the candidate violates the declared comparison rule.

Coverage-gap classifications include:

```text
NOT_OBSERVABLE_REFERENCE
NOT_SUPPORTED_CANDIDATE
UNKNOWN_REFERENCE
UNKNOWN_CANDIDATE
NOT_COMPARABLE
```

## 23. Compatibility

Major version 1 remains additive-only. Removing/renaming required fields, action kinds or safety semantics requires a new major contract and migration plan.

The execution contract is normative for concurrency/safety. An adapter that advertises Adapter v1 but cannot implement the required Execution v1 major must be refused by the Scenario Engine.