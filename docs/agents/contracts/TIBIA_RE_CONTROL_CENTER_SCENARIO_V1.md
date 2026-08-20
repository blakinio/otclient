# TIBIA RE Control Center Scenario Contract v1

```yaml
contract_id: TIBIA-RE-CONTROL-CENTER-SCENARIO-V1
version: 1.1
major_version: 1
status: normative_design
producer_repository: blakinio/otclient
runtime_authority: none
```

## 1. Purpose

Define one deterministic, bounded, semantic scenario language shared by fake, official-Tibia and future Oteryn adapters.

This contract prevents two implementations from giving materially different meanings to the same scenario file.

It does not grant runtime or mutation authority. Execution safety remains governed by `TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md`.

## 2. Parser safety and normalization

Scenario input may be YAML or JSON, but it is first converted into the same typed domain AST.

Required parser rules:

- reject duplicate mapping keys;
- reject custom YAML tags and executable/object constructors;
- aliases/anchors are disabled by default; if a parser cannot disable them, expansion depth/count must be bounded before semantic validation;
- reject non-finite numbers (`NaN`, `Infinity`, `-Infinity`);
- reject values outside the field's declared integer/decimal domain;
- reject unknown required top-level fields for major version 1;
- permit additive optional fields only where the schema explicitly allows them;
- apply finite limits to document bytes, nesting depth, collection length and string bytes before materializing unbounded structures;
- UTF-8 is required for textual fields.

Package A default parser ceilings, configurable only downward without a contract change:

```yaml
max_document_bytes: 262144
max_nesting_depth: 32
max_collection_items: 4096
max_string_bytes: 8192
max_steps: 1024
```

Action-specific fields may have tighter limits.

## 3. Canonical representation and hashes

After validation, the typed AST is serialized to JSON Canonicalization Scheme (RFC 8785 / JCS) using only schema-valid JSON values.

The canonical scenario hash is:

```text
scenario_hash = lowercase_hex(SHA-256(UTF8(JCS(validated_scenario_ast))))
```

The logical action request hash used for idempotency is:

```text
action_request_hash = lowercase_hex(SHA-256(UTF8(JCS({
  schema_version,
  run_id,
  step_id,
  attempt_index,
  kind,
  parameters,
  timeout_ms,
  required_capability,
  required_authority
}))))
```

Do not include mutable runtime fences, current authority status, timestamps or recorder fields in `action_request_hash`.

The coordinator records effect-plan/fence provenance separately.

## 4. Identifier and field-path types

```yaml
ScenarioId:
  regex: '^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$'

RunId:
  opaque_non_secret: true
  max_bytes: 128

StepId:
  max_bytes: 192

SemanticKey:
  regex: '^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$'

SemanticFieldPath:
  max_bytes: 256
  segment_regex: '^[A-Za-z_][A-Za-z0-9_-]{0,63}$'
  separator: '.'
```

`SemanticFieldPath` is one or more `segment_regex` segments separated by exactly one `.`. Empty segments, `..`, bracket/index syntax, wildcards, JSON Pointer escapes and implementation-private paths are invalid in v1.

Examples:

```text
player.hp
player.position.x
target.state
cooldowns.semantic_state
```

A syntactically valid path is admissible only when the selected normalized snapshot/capability schema declares that exact typed field. Unknown paths fail scenario validation. Collection membership/indexing is expressed by the predicate/operator and typed normalized value, not by implementation-dependent path syntax.

IDs and paths are non-secret and must not contain account names, credentials, tokens or arbitrary chat text.

## 5. Stable step IDs

A scenario step may declare an optional local `id` matching `ScenarioId` syntax.

During validation:

```text
if explicit local step id exists:
    step_id = <scenario.id> + ":" + <local-id>
else:
    step_id = <scenario.id> + ":step-" + zero-padded 4-digit 1-based ordinal
```

Examples:

```text
healing-basic-001:before
healing-basic-001:step-0002
```

Duplicate resulting `step_id` values are rejected.

Insertion/reordering of steps changes generated ordinal IDs; long-lived scenarios should therefore give semantically important steps explicit local IDs.

## 6. Scenario schema

Minimum typed shape:

```yaml
schema_version: 1
id: ScenarioId
name: string
adapter_requirements:
  reads: [SemanticKey]
  actions: [SemanticKey]
preconditions: [Predicate]
side_effect_budget: SideEffectBudget
capture_policy: CapturePolicy
steps: [Step]
abort_conditions: [AbortCondition]
expected_result: [Predicate]
privacy_policy: PrivacyPolicy
```

`name` is descriptive only and does not participate in authority.

### 6.1 SideEffectBudget

`SideEffectBudget` is the scenario-owned hard ceiling. Every field is required in v1; there are no implicit non-zero defaults.

```yaml
SideEffectBudget:
  max_runtime_seconds: integer
  max_actions: integer
  max_movement_tiles: integer
  max_spells: integer
  max_consumables: integer
  max_items_moved: integer
  max_gold: integer
  max_tibia_coins: integer
  max_irreversible_changes: integer
```

Rules:

- every value is a checked non-negative integer in `0..9223372036854775807`;
- unknown dimensions are rejected rather than ignored;
- `max_tibia_coins` and `max_irreversible_changes` default conceptually to zero and therefore must be written as `0` unless a separately accepted authority explicitly permits a finite non-zero ceiling;
- the sum of admitted/reserved effects for the run may never exceed these values according to Execution v1 `BudgetLedger` semantics;
- an action whose conservative `EffectBound` exceeds any remaining dimension is refused before dispatch;
- a scenario with a mutation step but `max_actions: 0` is valid syntax but cannot admit that action and deterministically refuses before mutation.

This schema is the input budget. `EffectBound` in §11 is the per-action conservative maximum; the two are not interchangeable.

## 7. Predicates

```yaml
Predicate:
  field: SemanticFieldPath
  op: EQ | NE | LT | LTE | GT | GTE | EXISTS | NOT_EXISTS | CHANGED | UNCHANGED | IN_SET | CONTAINS
  value: scalar | list | null
  from_checkpoint: StepId | null
  unknown_policy: FAIL | WAIT | ACCEPT
```

Rules:

- `EQ/NE/LT/LTE/GT/GTE/IN_SET/CONTAINS` require a compatible `value`;
- `EXISTS/NOT_EXISTS/CHANGED/UNCHANGED` require `value=null`;
- `CHANGED/UNCHANGED` compare with `from_checkpoint` when supplied, otherwise with the step's declared baseline;
- UNKNOWN never equals a concrete value;
- mutation preconditions and safety/authority predicates require `unknown_policy=FAIL`;
- assertions default to FAIL on UNKNOWN;
- waits may use WAIT until their deadline;
- ACCEPT is allowed only for explicitly non-safety observation assertions;
- type mismatch is validation failure or deterministic predicate error, never implicit coercion.

Numeric comparisons do not coerce strings to numbers.

## 8. Step union and retry semantics

A step is exactly one of:

```yaml
snapshot:
  id: ScenarioId | null
  name: string

action:
  id: ScenarioId | null
  kind: SemanticKey
  parameters: object
  timeout_ms: integer
  retry:
    max_attempts: integer
    retry_on: [REFUSED | FAILED_BEFORE_DISPATCH | TIMED_OUT_BEFORE_DISPATCH]

wait:
  id: ScenarioId | null
  condition: Predicate
  timeout_ms: integer

assert:
  id: ScenarioId | null
  condition: Predicate

checkpoint:
  id: ScenarioId | null
  label: string
```

Bounds:

```text
1 <= timeout_ms <= 300000
1 <= retry.max_attempts <= 3
```

If `retry` is omitted, `max_attempts=1` and no retry is performed. `max_attempts` is the total number of attempts including the first attempt; zero-attempt actions do not exist in v1. If `max_attempts>1`, `retry_on` must contain at least one declared pre-dispatch state.

For mutation-capable actions, a retry may occur only after positive proof of `NOT_DISPATCHED`. States at or beyond `DISPATCH_COMMITTED`, including AMBIGUOUS, are not retryable by this mechanism.

A retry creates a new action ID and attempt index and requires fresh budget reservation/fences/authority.

## 9. Semantic references

Common scenarios never contain process pointers, heap addresses, X11 coordinates, QMeta IDs, vtable/function addresses or protocol opcodes.

All reference unions are kind-discriminated. Fields not listed for the selected kind are rejected; nullable catch-all representations are not permitted.

### 9.1 EntityRef

```yaml
SELF:
  kind: SELF

SELECTED_TARGET:
  kind: SELECTED_TARGET

CREATURE_ID:
  kind: CREATURE_ID
  creature_id: integer  # 0..18446744073709551615

SNAPSHOT_PATH:
  kind: SNAPSHOT_PATH
  path: SemanticFieldPath
```

A `SNAPSHOT_PATH` must resolve to exactly one retained normalized entity reference at a named/current fenced checkpoint; raw runtime memory is never addressable.

### 9.2 ItemRef

```yaml
INVENTORY_SLOT:
  kind: INVENTORY_SLOT
  slot: SemanticKey
  expected_semantic_item: SemanticKey | null

CONTAINER_SLOT:
  kind: CONTAINER_SLOT
  container_ref: SemanticKey
  slot_index: integer  # 0..65535
  expected_semantic_item: SemanticKey | null

EQUIPMENT_SLOT:
  kind: EQUIPMENT_SLOT
  slot: HEAD | NECK | BACK | ARMOR | RIGHT_HAND | LEFT_HAND | LEGS | FEET | RING | AMMO | OTHER
  expected_semantic_item: SemanticKey | null

SNAPSHOT_PATH:
  kind: SNAPSHOT_PATH
  path: SemanticFieldPath
  expected_semantic_item: SemanticKey | null
```

### 9.3 DestinationRef

```yaml
INVENTORY_SLOT:
  kind: INVENTORY_SLOT
  slot: SemanticKey

CONTAINER_SLOT:
  kind: CONTAINER_SLOT
  container_ref: SemanticKey
  slot_index: integer  # 0..65535

EQUIPMENT_SLOT:
  kind: EQUIPMENT_SLOT
  slot: HEAD | NECK | BACK | ARMOR | RIGHT_HAND | LEFT_HAND | LEGS | FEET | RING | AMMO | OTHER

GROUND_POSITION:
  kind: GROUND_POSITION
  position:
    x: integer  # 0..4294967295
    y: integer  # 0..4294967295
    z: integer  # 0..255
```

Adapters resolve references against the fenced current normalized state and refuse stale, absent or ambiguous selectors. They must not reinterpret one union variant as another or accept implementation-private extension fields without a negotiated versioned extension.

## 10. Atomic semantic action parameter schemas

Unknown action kinds are refused unless negotiated by a newer compatible contract/capability extension.

### 10.1 Movement

```yaml
move:
  direction: NORTH | EAST | SOUTH | WEST
  tiles: 1

turn:
  direction: NORTH | EAST | SOUTH | WEST

stop_movement: {}
```

Atomic `move` is exactly one requested tile. Routes are multiple steps so movement budgets and evidence remain explicit.

### 10.2 Controlled chat

```yaml
say_controlled_text:
  text: string
  text_class: TEST_GENERATED
```

`text` must be non-empty valid UTF-8 and <=256 encoded bytes under Scenario v1. Adapters may impose a stricter target-specific bound and refuse rather than truncate silently.

Only deliberately generated test text may be persisted; arbitrary observed private chat is outside this action schema.

### 10.3 Spells and consumables

```yaml
cast_spell:
  spell_key: SemanticKey
  target: EntityRef | null

use_consumable:
  consumable_key: SemanticKey
  target: EntityRef
  quantity: 1

eat_food:
  food_key: SemanticKey
  quantity: 1

use_rune:
  rune_key: SemanticKey
  target: EntityRef
  quantity: 1
```

Scenario v1 intentionally makes these atomic single-use requests. Multi-use loops are explicit repeated steps/scenarios.

### 10.4 Targeting/combat

```yaml
select_target:
  target: EntityRef

attack:
  target: EntityRef

cancel_attack: {}

follow:
  target: EntityRef

cancel_follow: {}
```

A target must resolve uniquely at final fenced state; ambiguous/stale target resolution refuses before dispatch commit.

### 10.5 Inventory/containers

```yaml
open_container:
  item: ItemRef

close_container:
  container: SemanticKey

use_item:
  item: ItemRef
  target: EntityRef | DestinationRef | null

look_item:
  item: ItemRef

move_item:
  item: ItemRef
  destination: DestinationRef
  count: integer
```

`move_item.count` must be positive and must not exceed the current proven source stack/count or the side-effect reservation.

### 10.6 Equipment

```yaml
equip:
  item: ItemRef
  slot: HEAD | NECK | BACK | ARMOR | RIGHT_HAND | LEFT_HAND | LEGS | FEET | RING | AMMO | OTHER

unequip:
  slot: HEAD | NECK | BACK | ARMOR | RIGHT_HAND | LEFT_HAND | LEGS | FEET | RING | AMMO | OTHER
  destination: DestinationRef
```

The adapter may expose a narrower slot set; unsupported slot/action combinations refuse via capability/preflight/final validation.

### 10.7 UI semantic panels

```yaml
open_panel:
  panel_key: SemanticKey

close_panel:
  panel_key: SemanticKey
```

Panel actions are semantic UI intents; raw window/widget coordinates do not enter scenarios.

### 10.8 Session

```yaml
logout: {}
```

`logout` is a mutation/session effect and requires an explicit effect budget/authority appropriate to the adapter.

`login_request` and `enter_game_request` remain capability placeholders only in Scenario v1 and are **not executable ordinary action payloads**. Authentication/session ingress requires a separately accepted contract and authority boundary before these become executable.

## 11. Effect-bound contract

Before reservation, the adapter/domain effect model returns a conservative bound:

```yaml
EffectBound:
  max_actions: integer
  max_movement_tiles: integer
  max_spells: integer
  max_consumables: integer
  max_items_moved: integer
  max_gold: integer
  max_tibia_coins: integer
  max_irreversible_changes: integer
  measurable_after: bool
  reason_codes: [string]
```

Every numeric field is a checked non-negative integer. Package A fake adapter provides deterministic EffectBound fixtures.

Official/Oteryn adapters may provide tighter bounds but never larger effects than the admitted bound.

If a safe hard bound cannot be produced, the action is refused before reservation/dispatch.

Examples:

```text
move one tile          max_actions=1 max_movement_tiles=1
cast one spell         max_actions=1 max_spells=1
use one potion         max_actions=1 max_consumables=1
move stack count=N     max_actions=1 max_items_moved=N
```

Gold/TC/irreversible dimensions remain zero unless the action can prove a finite non-zero maximum and current scenario/authority explicitly admits it.

## 12. Capture policy

```yaml
CapturePolicy:
  state: bool
  events: bool
  screenshots: NONE | BEFORE_AFTER | CHECKPOINTS
  network: NONE | METADATA
  traces: NONE | TARGETED
```

This policy requests desired evidence only. It does **not** authorize an invasive capture mechanism.

If satisfying a requested capture policy would require process attach/injection, GUI input, network mutation or another state-changing mechanism, the adapter must report that requirement and the engine must refuse until a separately authorized capture-control action/contract exists.

Read-only capture methods must independently satisfy the current adapter/Track A read authority.

## 13. Abort conditions

`AbortCondition` is a discriminated rule. Unknown fields for the selected form are rejected.

```yaml
AbortCondition:
  code: STOP_LATCHED | CONTROL_GENERATION_CHANGED | BACKEND_EPOCH_CHANGED | ADAPTER_GENERATION_CHANGED | RUNTIME_INSTANCE_CHANGED | SESSION_EPOCH_CHANGED | AUTHORITY_LOST | CAPABILITY_LOST | TARGET_IDENTITY_CHANGED | CLIENT_NOT_IN_GAME | BUDGET_EXHAUSTED | TIMEOUT | PRIVACY_REJECTION | RECORDER_FATAL | ARTIFACT_FATAL | SCENARIO_ABORT_PREDICATE
  condition: Predicate | null
```

Rules:

- for `SCENARIO_ABORT_PREDICATE`, `condition` is required and must use `unknown_policy=FAIL`; when it evaluates true the run aborts with that code;
- for every other code, `condition` must be `null`; the code refers to the corresponding engine/adapter/system condition defined by Execution v1;
- unknown abort codes are validation failures unless negotiated by an additive extension;
- a triggered abort stops scheduling subsequent steps but does not assert that a previously dispatch-committed external effect was reversed.

## 14. Privacy policy

```yaml
PrivacyPolicy:
  secret_material: REJECT
  private_chat: OMIT | REDACT
  identities: KEEP_TEST_ONLY | HASH_NON_SECRET | OMIT
  screenshots: SAFE_ONLY | QUARANTINE_UNKNOWN
```

`secret_material` is fixed to `REJECT` in major version 1.

Scenario policy cannot weaken the execution contract's construction-time secret exclusion.

## 15. Validation result

Validation returns structured, non-secret errors:

```yaml
ScenarioValidationResult:
  valid: bool
  schema_version: integer
  scenario_id: string | null
  scenario_hash: string | null
  normalized_step_ids: [string]
  required_reads: [SemanticKey]
  required_actions: [SemanticKey]
  errors:
    - code: string
      step_id: string | null
      field: string | null
      safe_message: string
```

Validation does not contact or mutate the official client and does not grant runtime authority.

## 16. Compatibility

Scenario major version 1 is additive-only.

Changing the meaning of an existing action, predicate, field or hash canonicalization requires a new major version or an explicit versioned extension.

Adapters and the Scenario Engine fail closed on unsupported required semantic versions.