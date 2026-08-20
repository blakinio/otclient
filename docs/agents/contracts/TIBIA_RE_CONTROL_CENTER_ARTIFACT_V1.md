# TIBIA RE Control Center Artifact Contract v1

```yaml
contract_id: TIBIA-RE-CONTROL-CENTER-ARTIFACT-V1
version: 1.2
major_version: 1
status: normative_design
producer_repository: blakinio/otclient
contains_secrets: forbidden
```

## 1. Purpose

Define deterministic persistence for Package A tests and Package B+ storage/export while keeping safety authority separate from evidence/presentation.

The storage model separates:

1. global request/resource/control safety state that may exist before a run;
2. per-run action/budget/recovery safety state;
3. evidence state;
4. presentation/export state.

Presentation failure must never erase or downgrade safety state.

## 2. Logical storage roots

The implementation chooses one repository-conformant runtime data root. The logical layout is:

```text
control/
  safety/
    request-ledger.jsonl
    resource-ledger.jsonl
    control-state.json
  runtime/
    current-backend.json

runs/<run-id>/
  safety/
    action-ledger.jsonl
    budget-ledger.json
    recovery.json
    request-projection.jsonl        # optional derived projection only
  stage/
    manifest.json
    scenario.json
    events.jsonl
    actions.jsonl
    state/
    network/
    traces/
    screenshots/
  finalized/
    manifest.json
    scenario.json
    events.jsonl
    actions.jsonl
    state/
    network/
    traces/
    screenshots/
    result.json
    report.md
    agent_bundle.json
  supplements/
    <supplement-id>/...
```

The authoritative RequestLedger and ResourceIdentityLedger are global because request/resource identity must exist before scheduling and may predate a run directory. A per-run request file is projection only and never safety authority.

Physical files may be implemented through a transactional database plus export materialization, but logical records, ordering, uniqueness and atomicity must remain equivalent.

Do not store large/raw capture bytes in Git unless current evidence policy explicitly permits them.

## 3. File and directory safety

Run/artifact/request/resource/transition IDs are validated opaque non-secret IDs, never user-supplied filesystem paths.

Filesystem implementations must:

- construct paths from validated IDs only;
- reject path separators, `..`, NUL and absolute paths in IDs;
- avoid symlink following for run/control-owned files where practical;
- keep temporary/final rename targets inside selected runtime root;
- create local-control/safety metadata owner-only where platform permits;
- never materialize Control API nonce into run/control artifacts.

## 4. Safety-state precedence

Global `control/safety/` plus per-run `runs/<run-id>/safety/`, or transactionally equivalent database state, are authoritative for:

- RequestLedger dedupe;
- stable logical resource identity;
- persistent STOP/control state;
- ActionLedger dispatch state;
- non-time BudgetLedger reserved/at-risk/committed/uncertain state;
- backend/recovery classification.

If presentation/evidence records disagree with safety state:

```text
fail closed
preserve contradiction evidence
never downgrade POSSIBLY_DISPATCHED/AT_RISK
never clear stop_latched
never allocate a replacement resource for an existing request_id/resource_id
```

## 5. Global RequestLedger

```yaml
RequestLedgerRecord:
  schema_version: 1
  request_id: string
  request_hash: lowercase_hex_sha256
  operation: string
  resource_id: string | null
  transition_id: string | null
  backend_epoch_created: string
  status: INTENT_DURABLE | ACCEPTED | COMPLETED | FAILED | RECOVERY_REQUIRED
  response_code: integer | null
  response_body_hash: lowercase_hex_sha256 | null
  created_monotonic_ns: integer
  updated_backend_epoch: string
  updated_monotonic_ns: integer
```

Records are append-only transitions or transactionally equivalent versioned rows.

A later record for the same request ID preserves request hash, operation, resource identity and transition identity. Same request ID with different hash/operation is deterministic conflict.

Monotonic timestamps are meaningful only inside their associated backend epoch and must not be compared across backend epochs as one clock.

## 6. Global ResourceIdentityLedger

A resource-capable POST uses a durable minimal identity record before scheduling:

```yaml
ResourceIdentityRecord:
  schema_version: 1
  resource_id: string
  resource_kind: RUN | ONE_STEP_EXPERIMENT
  creating_request_id: string
  creating_request_hash: lowercase_hex_sha256
  run_id: string
  experiment_id: string | null
  action_ids: [string]
  scenario_id: string
  scenario_hash: lowercase_hex_sha256
  state: CREATED_NOT_SCHEDULED | SCHEDULED | TERMINAL | RECOVERY_REQUIRED
  backend_epoch_created: string
  created_monotonic_ns: integer
  updated_backend_epoch: string
  updated_monotonic_ns: integer
```

Rules:

- `resource_id` is globally unique within the Control Center safety store;
- `RUN`: `resource_id == run_id`, `experiment_id=null`, `action_ids=[]` at creation;
- `ONE_STEP_EXPERIMENT`: `resource_id == experiment_id`; the record fixes `experiment_id`, its `run_id` and all initially materialized one-step `action_ids` before scheduling;
- resource identity, creating request, scenario identity/hash and child IDs never change;
- state may advance but never return to `CREATED_NOT_SCHEDULED`;
- a surviving resource identity does not authorize automatic scheduling/resume after backend restart;
- contradictory duplicate `resource_id` or `run_id` fails closed.

The full per-run manifest/evidence may be created later; this minimal global record is sufficient to prevent duplicate resource allocation after crash.

## 7. Crash-safe request/resource admission

For every POST that can create durable resource identity or schedule work, determine stable logical IDs **before** scheduling or semantic/external side effect.

Then one bounded local safety transaction must atomically/equivalently create:

```text
RequestLedgerRecord(status=INTENT_DURABLE)
+
ResourceIdentityRecord(state=CREATED_NOT_SCHEDULED)
```

For `POST /v1/runs` this fixes one `run_id`.

For `POST /v1/experiments/one-step` this fixes `experiment_id`, `run_id` and initial action IDs.

Only after the durability barrier succeeds may resource state move to `SCHEDULED` and domain scheduling begin.

Crash semantics:

- crash before durable pair -> conforming path was forbidden to schedule/create protected resource; retry may allocate once;
- crash after durable pair but before scheduling -> same request must recover the same resource IDs; no replacement and no mutation auto-resume;
- uncertain/corrupt atomicity -> Request/Resource state becomes `RECOVERY_REQUIRED`; no replacement/re-execution.

For control-only operations such as STOP/reset, RequestLedger uses stable `transition_id`; the corresponding `ControlStateRecord.last_transition_id` proves committed control transition. No ResourceIdentityRecord is required.

## 8. Durable ControlState

```yaml
ControlStateRecord:
  schema_version: 1
  backend_epoch_last_writer: string
  control_generation: integer
  stop_latched: bool
  last_transition_id: string
  last_transition_kind: INITIALIZE | STOP | RESET | RECOVERY_FAIL_CLOSED
  reason_code: string | null
  safety_store_state: HEALTHY | FAILED | RECOVERY_REQUIRED
  updated_monotonic_ns: integer
```

Rules:

- explicit first-ever safety-store bootstrap durably creates `INITIALIZE` before mutation admission;
- STOP writes `stop_latched=true` with its transition ID under Execution-v1 ordering;
- reset writes `stop_latched=false` only after reset preconditions/durability succeed;
- restart reads latest valid state before mutation admission and carries a true latch into fresh backend epoch;
- restart never treats fresh backend epoch as reset;
- missing/corrupt/contradictory state where prior state may exist -> `RECOVERY_REQUIRED`, effectively latched/fail-closed;
- failed STOP/control-state write leaves running backend locally fail-closed;
- ControlState contains no external Track A authority and cannot grant it.

## 9. ActionLedger

```yaml
ActionLedgerRecord:
  schema_version: 1
  action_id: string
  action_request_hash: lowercase_hex_sha256
  run_id: string
  step_id: string
  attempt_index: integer
  lifecycle_state: string
  dispatch_state: NOT_DISPATCHED | POSSIBLY_DISPATCHED | DISPATCHED
  backend_epoch: string
  control_generation: integer
  adapter_id: string
  adapter_generation: string
  runtime_instance_id: string | null
  session_epoch: string | null
  effect_bound: object
  authoritative_confirmation: PROVEN | DERIVED | NOT_AVAILABLE | UNKNOWN
  reason_code: string | null
  created_monotonic_ns: integer
  updated_backend_epoch: string
  updated_monotonic_ns: integer
```

The transition to `DISPATCH_COMMITTED/POSSIBLY_DISPATCHED` is durability-coupled to all applicable non-time BudgetLedger `AT_RISK` transitions as required by Execution v1.

Possible-dispatched cannot move back to not-dispatched without authoritative no-effect reconciliation.

`CONFIRMED` is terminal. Later evidence may supplement but cannot rewrite it as another control outcome.

## 10. BudgetLedger

```yaml
BudgetLedger:
  schema_version: 1
  run_id: string
  dimensions:
    <dimension>:
      limit: integer
      reserved: integer
      at_risk: integer
      committed: integer
      uncertain: integer
  runtime:
    limit_seconds: integer
    started_monotonic_ns: integer
    deadline_monotonic_ns: integer
    observed_elapsed_seconds: integer
  updated_backend_epoch: string
  updated_monotonic_ns: integer
```

All numeric values are non-negative checked integers.

The `dimensions` map contains non-time hard dimensions from Scenario/Execution v1. The `runtime` record represents the absolute monotonic run deadline; it is not converted to `AT_RISK` merely because physical dispatch occurred.

Persist ActionLedger dispatch commit and affected non-time BudgetLedger at-risk transition in one atomic local transaction or equivalent conservative crash protocol.

If non-time atomicity cannot be proven after crash, recover maximum plausible affected budget into `uncertain` before admitting overlapping work.

Run runtime never auto-resumes across backend restart.

## 11. Recovery record

```yaml
RecoveryRecord:
  schema_version: 1
  run_id: string
  recovered_by_backend_epoch: string
  prior_backend_epoch: string | null
  classification: CLEAN_NOT_DISPATCHED | AMBIGUOUS | CONFIRMED | INCOMPLETE | CONTRADICTORY
  action_ids: [string]
  reason_codes: [string]
  evidence_refs: [string]
  recovered_monotonic_ns: integer
```

Recovery never invents PASS. `CONTRADICTORY` fails closed.

## 12. Run manifest

```yaml
RunManifest:
  schema_version: 1
  artifact_contract_major: 1
  run_id: string
  scenario_id: string
  scenario_hash: lowercase_hex_sha256
  semantic_schema_id: string
  semantic_schema_version: string
  semantic_schema_hash: lowercase_hex_sha256
  adapter_id: string
  adapter_kind: string
  adapter_version: string
  adapter_generation_at_start: string
  backend_epoch: string
  initial_control_generation: integer
  final_control_generation: integer
  runtime_instance_id_at_start: string | null
  session_epoch_at_start: string | null
  state: ACTIVE | CLOSING | FINALIZED | INCOMPLETE | AMBIGUOUS | FAILED
  started_monotonic_ns: integer
  finished_monotonic_ns: integer | null
  privacy_policy: object
  action_summary: object
  budget_summary: object
  event_summary: object
  artifact_hashes: object
  supplements: [string]
```

For built-in semantic schema, record `control-center.core`, `1.0.0` and its deterministic registry hash. Extension schemas record the exact Adapter-v1 verified descriptor/hash.

Manifest contains no secrets or raw private communication.

## 13. Scenario artifact

Store validated canonical Scenario-v1 AST as `scenario.json`.

`scenario_hash` must equal SHA-256 over Scenario-v1 JCS canonical serialization.

Do not persist unvalidated original YAML if it may contain rejected/secret data.

## 14. Events

`events.jsonl` contains one complete UTF-8 JSON object per line.

Rules:

- no secret-class values;
- `ingest_seq` strictly increases within one recorder instance;
- no duplicate ingest sequence in one run recorder stream;
- source gaps may be represented explicitly;
- ingestion order is not causal source order.

Evidence write/truncation failure leaves run incomplete/failed according to policy and does not alter safety ledgers.

## 15. Actions evidence

`actions.jsonl` is a non-secret evidence projection of ActionLedger transitions/results.

It may omit internal persistence metadata but never claims `NOT_DISPATCHED` when safety state says possible/dispatched. Safety ledger wins on contradiction.

## 16. Screenshot quarantine

Normal run screenshots contain only admitted `SAFE` material.

Potentially secret screenshots stay in separate quarantine not included in normal run manifest/export until sanitized/approved.

Quarantine identifiers/metadata may be recorded without secret pixels. Rejected bytes are not copied into normal artifacts.

## 17. Staging/finalization

Run lifecycle:

```text
ACTIVE -> CLOSING -> FINALIZED
```

Finalization requires:

1. no execution step can still change terminal result;
2. bounded late-event drain completed/expired;
3. required safety ledgers flushed;
4. required evidence files flushed;
5. hashes computed from exact final bytes;
6. `result.json` produced from authoritative states;
7. final manifest written;
8. staging atomically promoted where filesystem semantics permit.

Failure of required finalization -> `INCOMPLETE` or `FAILED`; PASS forbidden.

## 18. Result envelope

```yaml
RunResult:
  schema_version: 1
  run_id: string
  status: PASS | FAIL | REFUSED | CANCELLED | TIMEOUT | AMBIGUOUS | INCOMPLETE
  first_failure_step_id: string | null
  reason_codes: [string]
  assertions: object
  action_outcomes: object
  budget_outcome: object
  recorder_outcome: object
  privacy_outcome: object
  cleanup_outcome: object
  evidence_refs: [string]
```

Unresolved mutation AMBIGUOUS cannot be overall PASS. Unknown/failed required privacy, cleanup or evidence finalization cannot silently become PASS.

## 19. Agent bundle

`agent_bundle.json` is compact non-secret index, not raw dump.

Minimum:

```yaml
AgentBundle:
  schema_version: 1
  run_id: string
  scenario_id: string
  scenario_hash: string
  result_status: string
  semantic_schema:
    id: string
    version: string
    hash: string
  adapter_identity: object
  backend_epoch: string
  runtime_session_fences: object
  capability_refs: [string]
  action_summary: object
  budget_summary: object
  causal_evidence_summary: object
  artifact_refs: [string]
  artifact_hashes: object
  coverage_gaps: [string]
  privacy_status: string
```

Do not embed credentials, raw private chat, raw packet payloads, quarantined screenshot bytes or arbitrary exception text.

## 20. Report

`report.md` is derived presentation only and never safety/recovery source of truth.

Contradiction between report prose and machine-readable ledgers/results is validation failure.

## 21. Supplements

After FINALIZED, original finalized bytes/result remain immutable.

Later admitted evidence uses append-only `supplements/<supplement-id>/manifest.json`:

```yaml
SupplementManifest:
  schema_version: 1
  supplement_id: string
  parent_run_id: string
  created_monotonic_ns: integer
  reason: string
  artifact_hashes: object
  evidence_refs: [string]
```

Supplements cannot rewrite original action/budget/result truth.

## 22. Hashing

Artifact hashes use SHA-256 lowercase hex over exact stored bytes.

Hash maps identify relative logical artifact path -> digest.

Do not hash secret material merely to include it; secret-class material is excluded before artifact construction.

## 23. Retention/bounds

Package B defines finite configurable retention limits for completed runs/large evidence while never evicting safety records still required to prevent:

- duplicate Request/Resource identity;
- unsafe action recovery;
- ambiguous budget reuse;
- implicit STOP clearing.

Eviction cannot convert UNKNOWN/AMBIGUOUS into safe-to-retry and cannot turn latched STOP into unlatched state.

Git stores normalized durable evidence summaries/hashes only where current repository evidence policy permits it.

## 24. Deterministic artifact/safety tests

At minimum:

1. validated scenario/semantic-schema hashes match manifest;
2. run/resource ID path traversal rejected;
3. Action/non-time Budget dispatch commit atomicity or conservative crash recovery;
4. presentation failure cannot erase safety state;
5. crash before finalization -> INCOMPLETE, never PASS;
6. unresolved ambiguous action prevents PASS;
7. corrupt contradictory safety/evidence state -> fail closed;
8. event JSONL ingest sequence validation;
9. secret-shaped Event rejected before write;
10. quarantined screenshot absent normal manifest/export;
11. final hashes match exact bytes;
12. finalized view cannot silently mutate;
13. supplement cannot rewrite original result;
14. agent bundle contains only bounded non-secret references/summaries;
15. report contradiction is validation failure;
16. global RequestLedger exists before run scheduling;
17. RequestLedger INTENT_DURABLE + ResourceIdentityRecord are atomic/equivalent;
18. crash after durable pair before scheduling preserves same run/experiment/action IDs without auto-resume;
19. duplicate resource/run identity conflict fails closed;
20. first-ever ControlState initialization durable before mutation admission;
21. STOP latch survives backend restart;
22. corrupt/missing ControlState fails closed rather than implicitly resetting STOP;
23. failed reset durability leaves STOP latched;
24. semantic registry ID/version/hash survive staging/finalization unchanged;
25. runtime deadline representation is separate from non-time AT_RISK accounting.

## 25. Compatibility

Artifact major version 1 is additive-only.

Changing safety-state precedence, request/resource intent atomicity, STOP/control-state durability, dispatch-journal durability, finalization immutability or secret exclusion requires a new major contract or separately reviewed compatible extension.