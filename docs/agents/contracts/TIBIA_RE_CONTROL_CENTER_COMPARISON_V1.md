# TIBIA RE Control Center Comparison Contract v1

```yaml
contract_id: TIBIA-RE-CONTROL-CENTER-COMPARISON-V1
version: 1.0
major_version: 1
status: normative_design
producer_repository: blakinio/otclient
comparison_level: semantic_state_transition
```

## 1. Purpose

Define deterministic semantic comparison between an official Tibia reference run and a candidate run such as Oteryn v2 without requiring identical protocol bytes, internal objects, timing or renderer implementation.

Comparison never upgrades unavailable reference evidence into a candidate failure.

## 2. Inputs

A comparison consumes two finalized/accepted run views:

```yaml
ComparisonInput:
  reference_run_id: string
  candidate_run_id: string
  scenario_id: string
  scenario_hash: string
  profile: ComparisonProfile
```

Both runs must identify the same normalized scenario semantics or an explicitly declared compatible scenario migration.

A scenario-hash mismatch is `SCENARIO_MISMATCH` unless the profile names an approved migration/normalizer.

## 3. Checkpoint alignment

Fields are compared only at explicitly aligned semantic checkpoints.

```yaml
CheckpointPair:
  checkpoint_id: string
  reference_step_id: string
  candidate_step_id: string
  transition: BEFORE | AFTER | ASSERTION | TERMINAL
```

Do not align checkpoints solely by nearest timestamp.

If a required checkpoint cannot be aligned, classify `CHECKPOINT_UNAVAILABLE`, not a field mismatch.

## 4. Observation status

Each side reports per field:

```yaml
NormalizedObservation:
  field: string
  status: OBSERVED | UNKNOWN | NOT_SUPPORTED | NOT_OBSERVABLE | STALE
  value: any | null
  source_quality: object
  checkpoint_id: string
```

Only `OBSERVED` values participate in ordinary equality/tolerance comparison.

`STALE` does not silently become OBSERVED.

## 5. Comparison classes

```text
EXACT
NORMALIZED_EXACT
SET_EQUIVALENT
ORDERED_EQUIVALENT
TOLERANCE
REFERENCE_ONLY
NOT_COMPARABLE
```

### EXACT

Same typed value and representation after schema validation.

### NORMALIZED_EXACT

Both values are first normalized by the declared field normalizer; normalized typed values must then be exact.

### SET_EQUIVALENT

Compare canonical element identities as an unordered set/multiset according to profile configuration.

### ORDERED_EQUIVALENT

Compare normalized element sequence preserving semantic order/index.

### TOLERANCE

Compare numeric/duration values within explicit bounds.

### REFERENCE_ONLY

Reference observation may be retained for investigation but does not create pass/fail parity gate by itself.

### NOT_COMPARABLE

No cross-client parity is expected for this field.

## 6. Comparison profile

```yaml
ComparisonProfile:
  schema_version: 1
  profile_id: string
  profile_version: string
  fields:
    - path: string
      class: EXACT | NORMALIZED_EXACT | SET_EQUIVALENT | ORDERED_EQUIVALENT | TOLERANCE | REFERENCE_ONLY | NOT_COMPARABLE
      normalizer: string | null
      set_key: string | null
      absolute_tolerance: number | null
      relative_tolerance: number | null
      time_tolerance_ms: integer | null
      required: bool
```

A profile is immutable by `profile_id + profile_version`.

Changing field meaning/class/tolerance requires a new profile version.

## 7. Tolerance semantics

For numeric value `r` reference and `c` candidate:

```text
absolute_ok = |c-r| <= absolute_tolerance
relative_ok = |c-r| <= relative_tolerance * max(|r|, epsilon)
```

If both absolute and relative tolerances are declared, the profile must state `ANY` or `ALL`; default is `ANY`.

For durations/timestamps, compare semantic duration/transition delay, not absolute wall-clock epoch, unless the profile explicitly requires wall-clock behavior.

Tolerance values must be finite/non-negative.

## 8. Default semantic profile

Baseline recommendation:

```text
player.position                 NORMALIZED_EXACT
player.hp                       NORMALIZED_EXACT
player.hp_max                   NORMALIZED_EXACT
player.mana                     NORMALIZED_EXACT
player.mana_max                 NORMALIZED_EXACT
conditions                      SET_EQUIVALENT or profile-declared NORMALIZED_EXACT
target.state                    NORMALIZED_EXACT
inventory                       NORMALIZED_EXACT
containers                      ORDERED_EQUIVALENT when order/index is semantic
equipment                       NORMALIZED_EXACT
cooldowns.semantic_state        NORMALIZED_EXACT
cooldowns.remaining_time        TOLERANCE
visual_effect.semantic_event    REFERENCE_ONLY until both sides expose stable semantics
pixel_frame                     NOT_COMPARABLE by default
step_latency                    TOLERANCE or REFERENCE_ONLY
protocol_bytes                  NOT_COMPARABLE
internal_object_layout          NOT_COMPARABLE
function_address                NOT_COMPARABLE
renderer_implementation         NOT_COMPARABLE
thread_identity                 NOT_COMPARABLE
```

Individual scenarios may use a narrower profile.

## 9. Normalizers

Normalizers are versioned named pure functions over non-secret normalized values.

Examples:

```text
position_xyz_v1
condition_semantic_key_v1
inventory_slots_v1
container_contents_v1
equipment_slots_v1
cooldown_key_v1
```

A normalizer:

- cannot inspect client-private implementation addresses/opcodes;
- cannot fill UNKNOWN fields with defaults;
- cannot silently drop a difference solely to make parity pass;
- must have deterministic tests and version identity.

## 10. Coverage outcomes

When ordinary comparison cannot run, use explicit non-mismatch classifications:

```text
NOT_OBSERVABLE_REFERENCE
NOT_SUPPORTED_REFERENCE
UNKNOWN_REFERENCE
STALE_REFERENCE
NOT_OBSERVABLE_CANDIDATE
NOT_SUPPORTED_CANDIDATE
UNKNOWN_CANDIDATE
STALE_CANDIDATE
CHECKPOINT_UNAVAILABLE
NOT_COMPARABLE
REFERENCE_ONLY
```

Missing/weak official reference evidence is a coverage gap, not Oteryn mismatch.

## 11. Field result

```yaml
FieldComparisonResult:
  field: string
  checkpoint_id: string
  class: string
  status: MATCH | MISMATCH | COVERAGE_GAP | REFERENCE_ONLY | NOT_COMPARABLE
  reference_status: string
  candidate_status: string
  normalized_reference: any | null
  normalized_candidate: any | null
  delta: any | null
  tolerance_used: object | null
  reason_code: string | null
  evidence_refs: [string]
```

Never persist secret-class source values in comparison output.

## 12. Mismatch definition

A field is `MISMATCH` only when all are true:

1. field class is parity-bearing (`EXACT`, `NORMALIZED_EXACT`, `SET_EQUIVALENT`, `ORDERED_EQUIVALENT` or `TOLERANCE`);
2. both runs are aligned to the same semantic checkpoint;
3. both sides report `OBSERVED` non-stale values;
4. required normalizer/profile version is available;
5. the normalized candidate violates the declared equality/tolerance rule.

Otherwise use an explicit coverage/reference/not-comparable status.

## 13. Run-level result

```yaml
ComparisonResult:
  schema_version: 1
  comparison_id: string
  profile_id: string
  profile_version: string
  reference_run_id: string
  candidate_run_id: string
  scenario_id: string
  status: PASS | FAIL | COVERAGE_INCOMPLETE | INVALID_INPUT
  mismatches: [FieldComparisonResult]
  coverage_gaps: [FieldComparisonResult]
  reference_only: [FieldComparisonResult]
  not_comparable: [FieldComparisonResult]
  evidence_refs: [string]
```

Run-level classification:

- `FAIL` — at least one required parity-bearing field is MISMATCH;
- `PASS` — no required mismatch and every required parity-bearing field is comparably OBSERVED;
- `COVERAGE_INCOMPLETE` — no proven mismatch, but at least one required field/checkpoint cannot be compared;
- `INVALID_INPUT` — incompatible scenario/profile/run provenance prevents valid comparison.

Coverage incomplete is never promoted to PASS.

## 14. Timing

Official Tibia and Oteryn are not expected to have identical wall-clock timings.

Timing fields are parity-bearing only when the selected profile declares TOLERANCE.

Avoid comparing:

- scheduler/thread timing;
- frame pacing;
- network packet timestamps;
- rendering implementation timing;

unless the hypothesis explicitly requires them and both sides expose comparable semantic measurements.

## 15. Protocol/internal implementation

Cross-client differential E2E does **not** require identity of:

- packet bytes;
- opcodes/framing/encryption;
- object layouts;
- pointers/function addresses;
- thread model;
- renderer architecture;
- UI widget hierarchy.

These may exist as reference-only research evidence but are not default semantic parity gates.

Oteryn retains `protocol-oteryn`.

## 16. Server-authoritative Oteryn outcomes

Where Oteryn architecture declares server authority, candidate final gameplay truth comes from the supported server-authoritative observation/projection, not a hidden client-side test override.

Client observation may be compared separately as client-presentation/reconciliation evidence.

A client-side observation cannot overwrite an authoritative server mismatch or manufacture authoritative PASS.

## 17. Visual effects

Visual/game effects are compared semantically only when both sides expose a stable semantic observation such as effect type/key and relevant world position/target.

Raw pixels remain NOT_COMPARABLE by default.

Optional screenshot/pixel regression is a separate renderer/UI test profile and does not redefine semantic gameplay parity.

## 18. Containers/inventory ordering

Inventory/equipment slots are normally `NORMALIZED_EXACT` by semantic slot identity.

Containers use:

- `ORDERED_EQUIVALENT` when slot/index order is gameplay-visible/meaningful;
- `SET_EQUIVALENT` only when the selected subsystem/profile proves order irrelevant.

Do not erase ordering differences by choosing SET_EQUIVALENT for convenience.

## 19. Conditions

Conditions compare using stable semantic keys plus normalized attributes declared by profile.

Unknown implementation-specific flags are not silently synthesized.

If one side cannot observe a required condition attribute, classify coverage gap.

## 20. Evidence/provenance

Comparison output references:

- exact run IDs;
- scenario hash;
- adapter versions;
- comparison profile/version;
- relevant snapshot/event evidence refs;
- source-quality/coverage states.

It must remain possible to reproduce which exact normalized values produced the mismatch.

## 21. Privacy

Comparison operates only on already admitted normalized non-secret data.

It must not re-open quarantined screenshots/raw packet material or bypass artifact privacy policy to obtain parity.

## 22. Package A tests

Package A may implement profile/result types and pure comparator tests without Oteryn runtime.

At minimum:

1. exact match/mismatch;
2. normalized exact deterministic normalizer;
3. unordered set equivalence;
4. ordered difference detected;
5. absolute tolerance boundary;
6. relative tolerance boundary;
7. UNKNOWN reference -> coverage gap, not mismatch;
8. NOT_SUPPORTED candidate -> coverage gap;
9. required coverage gap -> run `COVERAGE_INCOMPLETE`, not PASS;
10. optional/reference-only field cannot fail parity;
11. NOT_COMPARABLE cannot fail parity;
12. checkpoint mismatch -> invalid/coverage classification, not nearest-time comparison;
13. scenario hash mismatch -> INVALID_INPUT absent declared migration;
14. deterministic profile versioning;
15. secret-shaped input rejected upstream/not admitted into comparison result.

## 23. Compatibility

Comparison major version 1 is additive-only.

Changing mismatch criteria, coverage-vs-failure semantics or existing comparison-class meaning requires a new major version.