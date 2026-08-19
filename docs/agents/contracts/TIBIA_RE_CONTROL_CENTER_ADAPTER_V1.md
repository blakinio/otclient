# TIBIA RE Control Center Adapter Contract v1

```yaml
contract_id: TIBIA-RE-CONTROL-CENTER-ADAPTER-V1
version: 1.3
major_version: 1
status: hardened_design_baseline
producer_repository: blakinio/otclient
runtime_authority: external; never granted by this contract
execution_semantics: docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
scenario_semantics: docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_SCENARIO_V1.md
```

## 1. Purpose

Define the stable semantic boundary between the Control Center domain/Scenario Engine and concrete client adapters.

Common scenarios express semantic intent only. They do not expose client-specific:

- GUI coordinates;
- raw key presses;
- QMeta IDs;
- function addresses/vtables;
- protocol opcodes;
- wire layouts.

Execution safety is normative in `TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md` and action parameter/canonical-hash semantics in `TIBIA_RE_CONTROL_CENTER_SCENARIO_V1.md`.

## 2. Version negotiation

Adapters advertise:

```yaml
supported_contracts:
  adapter_contract_major: [1]
  execution_contract_major: [1]
  scenario_contract_major: [1]
```

No mutually supported required major version -> fail closed before run execution.

Minor-version additions are additive. Unsupported required semantics are never silently ignored.

## 3. Adapter identity

```yaml
AdapterIdentity:
  adapter_id: string
  adapter_kind: OFFICIAL_TIBIA | OTERYN_V2 | FAKE_TEST
  adapter_version: string
  adapter_generation: string
  runtime_instance_id: string | null
  session_epoch: string | null
```

`adapter_generation` changes whenever adapter process/binding state changes in a way that can invalidate queued assumptions.

Changed adapter/runtime/session identity invalidates stale pending mutation.

## 4. Generic capability model

```yaml
Capability:
  capability_id: string
  semantic_version: string
  read_supported: bool
  action_supported: bool
  source: string
  notes: string | null
```

Read and action support are independent.

### 4.1 Official-client evidence extension

Only `OFFICIAL_TIBIA` exposes Track A research maturity:

```yaml
OfficialEvidenceExtension:
  capability_id: string
  read_gate: NONE | R0 | R1 | R2 | R3 | R4
  action_gate: NONE | A0 | A1 | A2 | A3 | A4
  evidence_refs: [string]
```

Gate meanings come from `OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md`.

Oteryn/fake adapters do not claim Track A R/A grades.

## 5. Runtime status

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

For `OFFICIAL_TIBIA`, `MUTATION_ALLOWED` is status only. It never constitutes standing authority for a later action.

## 6. Snapshot model

Adapters return only truthfully sourced fields:

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

Unknown remains null/UNKNOWN. Never fabricate plausible values for UI completeness.

## 7. DispatchFence

```yaml
DispatchFence:
  expected_backend_epoch: string
  expected_control_generation: integer
  expected_adapter_generation: string
  expected_runtime_instance_id: string | null
  expected_session_epoch: string | null
```

Official Track A lease/registration/Gate/target facts remain adapter-specific current authority inputs, not generic scenario fields.

## 8. ActionRequest

```yaml
ActionRequest:
  schema_version: 1
  action_id: string
  run_id: string
  step_id: string
  attempt_index: integer
  kind: string
  parameters: object
  timeout_ms: integer
  required_capability: string
  required_authority: READ_ONLY | MUTATION
  dispatch_fence: DispatchFence
  effect_bound: EffectBound
  action_request_hash: string
```

`parameters`, `EffectBound` and `action_request_hash` are produced according to Scenario v1.

Login credentials/session secrets are never serialized into ActionRequest.

## 9. ExecutionContext and one-shot commit

Mutation-capable `execute()` receives coordinator-owned context conceptually equivalent to:

```text
ExecutionContext:
  cancellation_token
  commit_dispatch() -> COMMITTED | REFUSED
```

`commit_dispatch()`:

- is one-shot;
- performs final Execution-v1 dispatch-gate/fence checks;
- makes `DISPATCH_COMMITTED/POSSIBLY_DISPATCHED` and budget `AT_RISK` durable;
- refuses if STOP/generation/identity/authority/durability checks fail.

The adapter must not cross a physical mutation boundary unless this exact action's commit returned `COMMITTED`.

## 10. Official-client commit sequence

For `OFFICIAL_TIBIA`:

1. obtain/enter the then-current canonical Track A guarded mutation boundary using existing infrastructure;
2. obtain/retain any current shared GUI/input lock required by trusted base;
3. perform final current Track A identity/authority checks while the guard remains held;
4. invoke coordinator `commit_dispatch()` immediately before the physical effect;
5. if commit succeeds, cross the physical irreversible boundary exactly once while the same external guard remains continuously held;
6. preserve the existing Track A whole-lifetime supervisor semantics for mutation descendants;
7. reconcile result/evidence/budgets conservatively.

The local `dispatch_gate` is not held while waiting to acquire Track A authority/locks. STOP therefore remains able to linearize while an action is blocked on external authority; the action later fails its stale control-generation commit.

## 11. Action lifecycle/result

Execution lifecycle is normative in Execution v1.

Result envelope:

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

`NOT_DISPATCHED` requires positive proof that the irreversible boundary was not crossed.

After successful dispatch commit with uncertain physical outcome, return `POSSIBLY_DISPATCHED/AMBIGUOUS`, not a retryable pre-dispatch failure.

A successful local GUI/function call is not automatically PASS; PASS requires scenario-declared evidence.

## 12. Required logical adapter operations

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

Concrete language/API may differ, but these responsibilities cannot be bypassed.

## 13. Preflight

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

Preflight is advisory/diagnostic only. `allowed_now=true` never authorizes future dispatch.

## 14. Snapshot/wait purity

`snapshot()` and ordinary `wait_for()` are observational operations.

They must not:

- send GUI input;
- mutate client/network/process state;
- perform a new debugger/instrumentation attach;
- acquire mutation authority on behalf of a caller;
- convert read support into action support.

If the requested observation cannot be produced through currently admitted passive/read-only mechanisms, return UNKNOWN/UNSUPPORTED/REFUSED rather than silently performing an invasive action.

## 15. Capture-control safety

`capture_start()` may start only capture producers whose enablement is already proven passive under current read authority.

Examples that are **not** ordinary passive capture and therefore cannot be hidden inside `capture_start()`:

- new debugger/instrumentation attach;
- process injection;
- GUI input/window activation that changes client behavior;
- process signal/restart;
- network/proxy/client configuration mutation.

If a capture mode requires such an invasive transition, `capture_start()` returns a typed requirement/refusal. The invasive transition needs a separately declared semantic control action/contract and the full MutationCoordinator/commit-dispatch/external-authority path.

`capture_stop()` may close/release harness-owned capture resources. It cannot introduce a new invasive mutation merely to clean up.

## 16. Emergency-stop safety

`emergency_stop()` is cooperative harness cleanup/cancellation assistance only.

It may:

- cancel adapter-owned waits;
- stop/close harness-owned passive capture streams;
- release harness-owned local resources/locks;
- signal cancellation to helper work already operating under prior authority.

It must not use STOP as authority to:

- issue `stop_movement` or any other gameplay command;
- inject keyboard/mouse input;
- kill/signal/restart the official client;
- attach/detach debugger/instrumentation;
- alter networking/proxy/client configuration;
- perform any new external mutation.

A compensating external action, if ever desired, is a normal semantic action with fresh authority/idempotency/budget. STOP itself grants none.

## 17. Scenario step semantics

Scenario structure, typed predicates, semantic selectors, action parameters, retry rules, parser bounds, canonical hashing, EffectBound and privacy/capture policy are normative in `TIBIA_RE_CONTROL_CENTER_SCENARIO_V1.md`.

Unknown action kind/unsupported semantic version fails closed.

## 18. Event envelope

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

`ingest_seq` is persistence order only, never universal causal source order.

## 19. Causal event fields

For Track A causal RE preserve when observable:

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

Do not infer unavailable fields or causal proof from timing.

## 20. Network event minimum

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

`message_type` is set only when structurally known.

Raw payload fallback is forbidden. Auth/session-secret-bearing payload persistence is forbidden.

## 21. Privacy construction boundary

Classification/redaction/rejection occurs before ordinary Event/Error/Artifact construction.

Requirements:

- arbitrary exception/repr/debug output is untrusted and never persisted directly;
- `safe_message` is reviewed static or sanitized safe text;
- environment-variable values are never copied into evidence;
- login/auth capture is structural only;
- trace strings are filtered before Event construction;
- private chat is omitted/redacted unless explicitly test-generated and permitted;
- uncertain login/auth screenshots use quarantine/refusal outside normal artifacts;
- `SECRET_REJECTED` contains category/reason only, never value/hash/reversible derivative;
- export-time redaction is defense in depth only.

## 22. Late events/finalization

```text
ACTIVE -> CLOSING -> FINALIZED
```

Bounded CLOSING may admit `late=true` events/source watermarks.

Late events cannot rewrite terminal action result, resume execution or authorize retry.

Later accepted post-finalization evidence is append-only supplemental material referencing the original run.

## 23. Official-client safety invariants

For `OFFICIAL_TIBIA`:

- visible client/window is not authority;
- stale lease/registration/generation cannot authorize dispatch;
- changed boot/PID/start/executable/window/display/session/runtime identity rejects stale work;
- read-only admission never escalates to mutation;
- Track A guard remains continuously held across final authority checks, durable local commit and physical mutation;
- GUI input uses current shared input lock/guard;
- action parity/evidence gates remain external proof requirements;
- credentials/login secrets never cross this semantic adapter contract;
- ambiguous possible dispatch is never automatically retried;
- passive capture cannot conceal a new invasive attach/input/process action;
- emergency stop cannot create gameplay/process mutation.

## 24. Oteryn v2 invariants

For `OTERYN_V2`:

- implementation belongs to a separate `blakinio/Oteryn-v2` task/branch/PR;
- integrate with accepted Oteryn ADR-0007 or a versioned cross-repo semantic boundary;
- retain `protocol-oteryn`;
- client sends semantic intent;
- server-authoritative outcomes remain authoritative;
- test hooks cannot create unauthenticated production control;
- production-default builds exclude/lock down test-only control according to Oteryn governance;
- use generic semantic capability support, not Track A R/A grades;
- compare normalized semantics rather than packet/internal-layout equality.

## 25. Differential comparison classes

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
visual_effect_semantics   REFERENCE_ONLY unless both expose stable semantics
pixel/frame output        NOT_COMPARABLE by default
latency                   TOLERANCE or REFERENCE_ONLY
protocol bytes            NOT_COMPARABLE
internal object layout    NOT_COMPARABLE
renderer implementation  NOT_COMPARABLE
```

Mismatch requires both sides to support/observe the field at the same normalized checkpoint, neither UNKNOWN, and candidate violation of the selected rule.

Unknown/unobservable reference is a coverage gap, not candidate failure.

## 26. Compatibility

Adapter major version 1 is additive-only.

Changing final commit semantics, passive-observation purity, capture-control safety, emergency-stop safety or external authority relationship requires a new major version or a separately reviewed compatible extension.