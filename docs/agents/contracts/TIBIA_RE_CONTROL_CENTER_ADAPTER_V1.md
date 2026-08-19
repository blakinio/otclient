# TIBIA RE Control Center Adapter Contract v1

```yaml
contract_id: TIBIA-RE-CONTROL-CENTER-ADAPTER-V1
version: 1.2
major_version: 1
status: hardened_design_baseline
producer_repository: blakinio/otclient
runtime_authority: external; never granted by this contract
execution_semantics: docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
```

## Purpose

Define the stable semantic boundary between the Control Center domain/Scenario Engine and concrete client adapters.

This contract deliberately excludes client-specific function addresses, UI coordinates, raw keycodes, QMeta IDs, vtables, packet opcodes and wire layouts from common scenarios.

Normative concurrency, dispatch-commit, STOP, idempotency, budget, privacy, artifact and restart semantics live in `TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md` and apply to every implementation of this adapter contract.

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

A changed `adapter_generation`, `runtime_instance_id` or `session_epoch` invalidates pending mutation dispatch unless a new action is created after revalidation.

## 3. Generic capability model

```yaml
Capability:
  capability_id: string
  semantic_version: string
  read_supported: bool
  action_supported: bool
  source: string
  notes: string | null
```

Read support never implies action support.

### 3.1 Official-client evidence extension

Only `OFFICIAL_TIBIA` uses Track A RE maturity:

```yaml
OfficialEvidenceExtension:
  capability_id: string
  read_gate: NONE | R0 | R1 | R2 | R3 | R4
  action_gate: NONE | A0 | A1 | A2 | A3 | A4
  evidence_refs: [string]
```

Gate meanings come from `OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md`.

`OTERYN_V2` and `FAKE_TEST` do not pretend to have Track A R/A evidence grades.

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

For `OFFICIAL_TIBIA`, `MUTATION_ALLOWED` is informational status only. It never represents standing authority for a later action.

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

Unknown data remains unknown/null. Adapters never synthesize plausible values for UI completeness.

## 6. Dispatch fence

Every action binds immutable Control Center execution fences:

```yaml
DispatchFence:
  expected_backend_epoch: string
  expected_control_generation: integer
  expected_adapter_generation: string
  expected_runtime_instance_id: string | null
  expected_session_epoch: string | null
```

Official Track A lease/registration/Gate/target identity facts remain official-adapter internals and are re-read from current trusted-base authority sources at final dispatch. They are not serialized into generic scenario files.

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

`action_id` is the mandatory idempotency key for one logical action attempt.

`max_effect` is the conservative maximum plausible effect already admitted/reserved by the engine for each applicable budget dimension.

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

Login/credential-bearing operations are not ordinary action payloads. Credentials must never be serialized into `ActionRequest`, Event or run artifact objects.

## 8. Execution context and one-shot dispatch commit

Mutation-capable adapter execution receives a coordinator-owned execution context conceptually equivalent to:

```text
ExecutionContext:
  cancellation_token
  commit_dispatch() -> DispatchCommitResult
```

`commit_dispatch()` is one-shot and owned by the `MutationCoordinator`.

It performs the execution contract's final local dispatch-gate checks and durable write-ahead transition to `DISPATCH_COMMITTED/POSSIBLY_DISPATCHED` plus `AT_RISK` budget state.

An adapter **must not cross its physical irreversible mutation boundary unless `commit_dispatch()` returned COMMITTED for that exact action**.

Calling `commit_dispatch()` twice returns/refuses deterministically and never creates a second logical dispatch.

For `OFFICIAL_TIBIA`, the adapter must:

1. obtain/enter the current canonical Track A guarded mutation boundary using existing infrastructure;
2. revalidate current Track A identity/authority/input-lock requirements as required by trusted base;
3. while that external guard remains continuously held, invoke `commit_dispatch()` immediately before the physical effect;
4. if commit succeeds, cross the physical irreversible boundary exactly once while the external guard is still held;
5. keep the existing whole-lifetime supervisor/guard semantics for mutation descendants.

This prevents a separate advisory preflight from becoming authority and avoids holding the local dispatch gate while waiting for external Track A locks/guards.

## 9. Action lifecycle

Required logical states:

```text
CREATED
VALIDATED
RESERVED
WAITING_AUTHORITY
DISPATCH_COMMITTED
DISPATCHING
CONFIRMING
CONFIRMED
REFUSED
CANCELLED_BEFORE_DISPATCH
CANCELLED_AFTER_DISPATCH
FAILED_BEFORE_DISPATCH
FAILED_AFTER_DISPATCH
TIMED_OUT_BEFORE_DISPATCH
TIMED_OUT_AFTER_DISPATCH
AMBIGUOUS
```

`DISPATCH_COMMITTED` means possible external side effect must be assumed after crash/uncertain completion.

`AMBIGUOUS` is never automatically retried.

## 10. Action result

```yaml
ActionResult:
  schema_version: 1
  action_id: string
  lifecycle_state: string
  status: PASS | FAIL | REFUSED | TIMEOUT | CANCELLED | AMBIGUOUS | UNKNOWN
  dispatch_state: NOT_DISPATCHED | POSSIBLY_DISPATCHED | DISPATCHED
  authoritative_confirmation: PROVEN | DERIVED | NOT_AVAILABLE | UNKNOWN
  backend_epoch: string
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

`dispatch_state=NOT_DISPATCHED` requires positive proof that the physical irreversible boundary was not crossed.

If dispatch commit succeeded but the implementation cannot prove whether the physical effect happened, report `POSSIBLY_DISPATCHED`/`AMBIGUOUS`.

A successful local function/UI call is not automatically PASS; PASS requires the scenario's declared evidence.

## 11. Required adapter operations

Logical surface:

```text
identity() -> AdapterIdentity
capabilities() -> CapabilitySet
runtime_status() -> RuntimeStatus
snapshot(request) -> GameSnapshot
preflight(action_request) -> PreflightResult
execute(action_request, execution_context) -> ActionResult
wait_for(condition, timeout, cancellation_token) -> WaitResult
capture_start(policy) -> CaptureSession
capture_stop(capture_session) -> CaptureSummary
emergency_stop(reason) -> StopResult
```

The concrete language/API may differ, but semantic responsibilities cannot be bypassed.

### 11.1 Preflight

`preflight()` is advisory/diagnostic only.

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

A `true` result never authorizes future dispatch.

### 11.2 Execute

`execute()` is the only semantic adapter operation that may cross a mutation boundary.

It must use the supplied one-shot `commit_dispatch()` immediately before physical mutation. If final fences, durable commit or external authority fail, execute returns a no-dispatch/refusal result and does not mutate.

## 12. Typed scenario step contract

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

Predicate baseline:

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
- assertions default `FAIL` on unknown;
- waits may use `WAIT` until timeout;
- stable `step_id` is deterministic during validation.

## 13. Side-effect budget

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

Normative reservation, `AT_RISK`, committed and uncertain accounting is in the execution contract.

If an action cannot provide a safe maximum plausible effect for every applicable hard budget, refuse before dispatch.

## 14. Cancellation and STOP ALL

Cancellation is mandatory at every bounded wait/dispatch boundary.

`STOP ALL` linearizes against `commit_dispatch()` through the same coordinator `dispatch_gate`.

The adapter's `emergency_stop()` is cooperative cancellation/cleanup assistance only. It does not create a second STOP authority or independently kill the official client.

A stale old-backend/old-generation completion may be retained as evidence but cannot advance current execution.

## 15. Normalized event envelope

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
  backend_epoch: string
  control_generation: integer
  adapter_id: string
  adapter_generation: string
  runtime_instance_id: string | null
  session_epoch: string | null
  run_id: string | null
  experiment_id: string | null
  step_id: string | null
  stimulus_id: string | BACKGROUND | null
  kind: SYSTEM | AUTHORITY | ACTION | TRACE | NET | STATE | SCREEN | SNAPSHOT | ASSERTION | RESULT | ERROR
  sensitivity: PUBLIC | RESEARCH_INTERNAL | PERSONAL_REDACTED | SECRET_REJECTED
  payload: object
```

`ingest_seq` is persistence order, not proof of source causality.

`SECRET_REJECTED` records rejection metadata only, never value/hash/reversible derivative.

## 16. Causal event extension

For causal Track A RE preserve when observable:

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

These fields preserve the normative experiment model without requiring every producer to know every field.

## 17. Network event minimum

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

`message_type` is populated only when structurally known. No timing-based guesses.

Raw payload fallback is forbidden. Auth/session-secret-bearing payloads are forbidden in persistent artifacts.

## 18. Privacy construction boundary

Secret/personal classification occurs before normal Event/Error/Artifact construction.

Requirements:

- arbitrary exception/repr/debug output is untrusted and not directly persisted;
- `safe_message` is reviewed/static or sanitized safe text;
- environment-variable values are never copied into evidence;
- login/auth capture is structural only;
- trace strings are filtered before Event creation;
- private chat is omitted/redacted before Event creation unless deliberately generated test text is permitted;
- screenshots with uncertain login/auth content use quarantine/refusal outside normal run artifacts;
- export-time redaction is defense in depth only.

## 19. Run finalization and late events

```text
ACTIVE -> CLOSING -> FINALIZED
```

Bounded `CLOSING` may admit `late=true` events/source watermarks.

Late events cannot rewrite a terminal action result, resume execution or authorize retry.

After FINALIZED, later accepted evidence is append-only supplement material referencing the original run.

## 20. Browser/CLI Control API semantics

Browser and CLI call the same backend domain service.

Minimum logical API:

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

Equivalent versioned spelling is allowed, but semantics require:

- bounded requests/collections/streams/history;
- mutation idempotency key;
- duplicate request result replay;
- deterministic malformed-input errors;
- no raw adapter/action bypass;
- loopback default;
- fail-closed remote exposure policy.

## 21. Official-client safety invariants

For `OFFICIAL_TIBIA`:

- visible client/window is not authority;
- stale lease/registration/generation cannot authorize dispatch;
- changed boot/PID/start/executable/window/display/session/runtime identity rejects stale work;
- read-only admission never escalates to mutation;
- current external Track A guard remains held continuously across `commit_dispatch()` and physical mutation;
- final Track A authority/identity checks happen inside that guarded boundary;
- GUI input uses the current shared lock/guard;
- action parity/evidence gates remain external proof requirements;
- credentials/login secrets never cross this semantic contract;
- authority loss blocks subsequent mutation;
- ambiguous possible dispatch is not automatically retried.

## 22. Oteryn-v2 invariants

For `OTERYN_V2`:

- implementation is a separate task/PR in `blakinio/Oteryn-v2`;
- integrate with Oteryn accepted ADR-0007 E2E architecture or a versioned cross-repo semantic boundary;
- expose semantic test intent without Tibia wire compatibility;
- server-authoritative outcomes remain authoritative;
- test hooks do not create unauthenticated production control;
- production-default build excludes/locks down test-only control under Oteryn policy;
- use generic capability support, not Track A R/A grades;
- compare normalized semantics, not raw protocol/internal layouts.

## 23. Differential comparison contract

Comparison classes:

```text
EXACT
NORMALIZED_EXACT
SET_EQUIVALENT
ORDERED_EQUIVALENT
TOLERANCE
REFERENCE_ONLY
NOT_COMPARABLE
```

Baseline:

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
visual_effect_semantics   REFERENCE_ONLY unless both expose stable semantics
pixel/frame output        NOT_COMPARABLE by default
latency                   TOLERANCE or REFERENCE_ONLY
protocol bytes            NOT_COMPARABLE
internal object layout    NOT_COMPARABLE
renderer implementation  NOT_COMPARABLE
```

Mismatch requires both sides to support/observe the field at the same normalized checkpoint, neither value UNKNOWN, and candidate violation of the selected rule.

Coverage states include:

```text
NOT_OBSERVABLE_REFERENCE
NOT_SUPPORTED_CANDIDATE
UNKNOWN_REFERENCE
UNKNOWN_CANDIDATE
NOT_COMPARABLE
```

## 24. Compatibility

Major version 1 is additive-only. Removing/renaming required fields, action kinds or safety semantics requires a new major contract and migration plan.

An adapter that claims Adapter v1 but cannot implement Execution v1's durable dispatch-commit semantics must be refused by the Scenario Engine.