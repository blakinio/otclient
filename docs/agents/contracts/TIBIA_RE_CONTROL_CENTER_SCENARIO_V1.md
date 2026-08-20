# TIBIA RE Control Center Scenario Contract v1

```yaml
contract_id: TIBIA-RE-CONTROL-CENTER-SCENARIO-V1
version: 1.0
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

## 4. Identifier types

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
```

IDs are non-secret and must not contain account names, credentials, tokens or arbitrary chat text.

### 4.1 Semantic field paths

`SemanticFieldPath` is a validated path into the normalized `GameSnapshot`/retained checkpoint model, never a raw adapter/runtime namespace.

```yaml
SemanticFieldPath:
  max_bytes: 256
  max_segments: 8
  segment_regex: '^[a-z][a-z0-9_]{0,63}$'
  roots: [client_state, player, conditions, action_state, target, inventory, containers, battle_list, source_quality]
```

The serialized form is dot-separated, for example `player.hp` or `player.position.x`. Brackets, numeric indexes, wildcards, JSON Pointer syntax, path separators and empty segments are rejected. Collection members are selected through typed semantic references rather than embedded indexes or runtime IDs in a path.

Path validation uses the versioned normalized snapshot schema advertised by the adapter. Missing, unsupported, stale or unobservable values resolve to UNKNOWN; they are never coerced to zero, empty text, `false` or another plausible default. `SNAPSHOT_PATH` references may additionally resolve the same grammar against an explicitly retained normalized checkpoint.

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

### 6.1 Side-effect budget

Every scenario carries one explicit finite hard budget:

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

All fields are required in the validated canonical AST. `1 <= max_runtime_seconds <= 86400`; every other dimension is a checked integer in `0..2147483647`. Implementations/adapters may impose lower ceilings but may not silently raise a scenario value. Read-only scenarios use zero for every external-effect dimension. Gold, Tibia Coin and irreversible-change budgets are zero unless deliberately admitted.

`max_runtime_seconds` is measured from run activation using the backend monotonic clock and bounds scheduling/waiting; expiry stops new dispatch. Action-specific maximum effects are separately produced as `EffectBound` and reserved against these run-level dimensions under Execution v1. No omitted/null/unbounded budget value exists in major version 1.

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
- `CHANGED/UNCHANGED` compare with `from_checkpoint` when supplied, otherwise with the step's declared baseline;
- UNKNOWN never equals a concrete value;
- mutation preconditions and safety/authority predicates require `unknown_policy=FAIL`;
- assertions default to FAIL on UNKNOWN;
- waits may use WAIT until their deadline;
- ACCEPT is allowed only for explicitly non-safety observation assertions;
- type mismatch is validation failure or deterministic predicate error, never implicit coercion.

Numeric comparisons do not coerce strings to numbers.

### 7.1 Abort conditions

```yaml
AbortCondition:
  id: ScenarioId | null
  condition: Predicate
  reason_code: SemanticKey
```

An abort condition is safety-significant: its predicate must use `unknown_policy=FAIL`; `WAIT` and `ACCEPT` are invalid in this context. The engine evaluates abort conditions before each step, on relevant observation changes while waiting, and again immediately before any mutation dispatch commit. A TRUE abort predicate or an UNKNOWN/error at a required safety evaluation stops scheduling new work and records the declared reason.

An abort never rewrites history. If an action has already reached `DISPATCH_COMMITTED`, its possible external effect is reconciled under Execution v1 and remains non-retryable unless authoritative no-effect proof exists. `reason_code` must be one of the standard abort codes in section 13 or a separately negotiated additive extension.

## 8. Step union

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

For mutation-capable actions, default `max_attempts=1` total attempt. A retry may occur only after positive proof of `NOT_DISPATCHED`. States at or beyond `DISPATCH_COMMITTED`, including AMBIGUOUS, are not retryable by this mechanism.

A retry creates a new action ID and attempt index and requires fresh budget reservation/fences/authority.

## 9. Semantic references

Common scenarios never contain process pointers, heap addresses, X11 coordinates, QMeta IDs, vtable/function addresses or protocol opcodes.

Object references are closed discriminated unions. Unknown fields, missing kind-required fields, or fields belonging to another kind are validation errors.

```yaml
EquipmentSlot: HEAD | NECK | BACK | ARMOR | RIGHT_HAND | LEFT_HAND | LEGS | FEET | RING | AMMO | OTHER

WorldPosition:
  x: integer  # 0..65535
  y: integer  # 0..65535
  z: integer  # 0..15

EntityRef:
  kind: SELF | SELECTED_TARGET | CREATURE_ID | SNAPSHOT_PATH
  creature_id: integer | null       # required only for CREATURE_ID, 0..4294967295
  snapshot_path: SemanticFieldPath | null  # required only for SNAPSHOT_PATH

ItemRef:
  kind: INVENTORY_SLOT | CONTAINER_SLOT | EQUIPMENT_SLOT | SNAPSHOT_PATH
  inventory_slot: SemanticKey | null
  container_ref: SemanticKey | null
  slot_index: integer | null        # 0..65535; adapter may advertise a lower maximum
  equipment_slot: EquipmentSlot | null
  snapshot_path: SemanticFieldPath | null
  expected_semantic_item: SemanticKey | null

DestinationRef:
  kind: INVENTORY_SLOT | CONTAINER_SLOT | EQUIPMENT_SLOT | GROUND_POSITION
  inventory_slot: SemanticKey | null
  container_ref: SemanticKey | null
  slot_index: integer | null        # 0..65535; adapter may advertise a lower maximum
  equipment_slot: EquipmentSlot | null
  position: WorldPosition | null
```

Per-kind rules:

- `SELF` and `SELECTED_TARGET` carry no selector payload; `CREATURE_ID` requires only `creature_id`; entity `SNAPSHOT_PATH` requires only `snapshot_path`.
- inventory item/destination requires only `inventory_slot`; container item/destination requires `container_ref` + `slot_index`; equipment item/destination requires only `equipment_slot`; item `SNAPSHOT_PATH` requires only `snapshot_path`.
- `GROUND_POSITION` requires only `position`. A ground destination always reserves at least one `max_irreversible_changes` unit in addition to other effect dimensions; the official adapter may refuse ground movement entirely when safe rollback/value risk cannot be bounded.
- `expected_semantic_item` is an optional additional identity fence for an `ItemRef`; mismatch/UNKNOWN refuses at final resolution.

Adapters resolve references against the fenced current normalized snapshot/state and refuse stale, missing or ambiguous selectors. A `SNAPSHOT_PATH` names only a retained normalized checkpoint/object and never raw runtime memory.

## 10. Atomic semantic action parameter schemas

Unknown action kinds are refused unless negotiated by a newer compatible contract/capability extension.

### 10.1 Movement

```yaml
move:
  direction: NORTH | EAST | SOUTH | WEST
  tiles: 1
```

Atomic `move` is exactly one requested tile. Routes are multiple steps so movement budgets and evidence remain explicit.

```yaml
turn:
  direction: NORTH | EAST | SOUTH | WEST
```

```yaml
stop_movement: {}
```

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
```

```yaml
use_consumable:
  consumable_key: SemanticKey
  target: EntityRef
  quantity: 1
```

```yaml
eat_food:
  food_key: SemanticKey
  quantity: 1
```

```yaml
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
```

```yaml
attack:
  target: EntityRef
```

```yaml
cancel_attack: {}
```

```yaml
follow:
  target: EntityRef
```

```yaml
cancel_follow: {}
```

A target must resolve uniquely at final fenced state; ambiguous/stale target resolution refuses before dispatch commit.

### 10.5 Inventory/containers

```yaml
open_container:
  item: ItemRef
```

```yaml
close_container:
  container: SemanticKey
```

```yaml
use_item:
  item: ItemRef
  target: EntityRef | DestinationRef | null
```

```yaml
look_item:
  item: ItemRef
```

```yaml
move_item:
  item: ItemRef
  destination: DestinationRef
  count: integer
```

`move_item.count` must be positive and must not exceed the current proven source stack/count or the side-effect reservation. A `GROUND_POSITION` destination additionally consumes the conservative irreversible-change reservation defined in section 9.

### 10.6 Equipment

```yaml
equip:
  item: ItemRef
  slot: EquipmentSlot
```

```yaml
unequip:
  slot: EquipmentSlot
  destination: DestinationRef
```

The adapter may expose a narrower slot set; unsupported slot/action combinations refuse via capability/preflight/final validation.

### 10.7 UI semantic panels

```yaml
open_panel:
  panel_key: SemanticKey
```

```yaml
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

Every numeric EffectBound dimension is a checked non-negative integer and must fit the corresponding `SideEffectBudget` dimension. `max_actions` counts this semantic action once when it can cross an external-effect boundary. Runtime is bounded by the run-level `max_runtime_seconds` rather than by individual EffectBound records.

Package A fake adapter provides deterministic EffectBound fixtures.

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

Scenario v1 standard abort codes:

```text
STOP_LATCHED
CONTROL_GENERATION_CHANGED
BACKEND_EPOCH_CHANGED
ADAPTER_GENERATION_CHANGED
RUNTIME_INSTANCE_CHANGED
SESSION_EPOCH_CHANGED
AUTHORITY_LOST
CAPABILITY_LOST
TARGET_IDENTITY_CHANGED
CLIENT_NOT_IN_GAME
BUDGET_EXHAUSTED
TIMEOUT
PRIVACY_REJECTION
RECORDER_FATAL
ARTIFACT_FATAL
```

Unknown abort code is validation failure unless negotiated by an additive extension. Each entry in `abort_conditions` uses the typed `AbortCondition` schema from section 7.1; arbitrary code-only strings are not scenario abort conditions.

A triggered abort stops scheduling subsequent steps. It does not assert that a previously dispatch-committed external effect was reversed.

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