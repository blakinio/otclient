# TIBIA RE Control Center Artifact Contract v1

```yaml
contract_id: TIBIA-RE-CONTROL-CENTER-ARTIFACT-V1
version: 1.1
major_version: 1
status: normative_design
producer_repository: blakinio/otclient
contains_secrets: forbidden
```

## 1. Purpose

Define the deterministic persistence envelope used by Package A tests and Package B+ durable storage/export.

This contract separates:

1. **global safety/control state** that may exist before a run and must survive restart;
2. **per-run safety state** required to prevent duplicate/unsafe mutation after crash;
3. **evidence state** used for analysis;
4. **presentation/export state** used by browser/CLI/agents.

Presentation failure must never erase or downgrade safety state.

## 2. Logical storage roots

The implementation chooses one repository-conformant runtime data root. The logical layout is:

```text
control/
  safety/
    request-ledger.jsonl
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

The authoritative RequestLedger is global under `control/safety/` because a request may exist before a run/resource is created and because operations such as STOP ALL are not run-scoped. A per-run request file, if materialized, is a derived projection and never the safety authority.

Physical files/directories may be implemented through a transactional database plus export materialization, but the logical records, ordering and atomicity semantics must remain equivalent.

Do not store large/raw capture bytes in Git unless current evidence policy explicitly permits them.

## 3. File and directory safety

Run/artifact/request/transition IDs are validated opaque non-secret IDs, never user-supplied filesystem paths.

All filesystem implementations must:

- construct paths from validated IDs only;
- reject path separators, `..`, NUL and absolute paths in IDs;
- use no symlink-following when materializing run-owned/control-owned files where practical;
- keep temporary/final rename targets inside the selected runtime root;
- create local-control/safety metadata with owner-only permissions where the platform permits;
- never materialize the Control API nonce into run/control artifacts.

## 4. Safety-state precedence

Global `control/safety/` plus per-run `runs/<run-id>/safety/`, or transactionally equivalent database state, are authoritative for:

- RequestLedger dedupe and request-to-resource/transition identity;
- persistent STOP/control state;
- ActionLedger dispatch state;
- BudgetLedger reserved/at-risk/committed/uncertain state;
- backend/recovery classification.

If presentation/evidence records disagree with safety state:

```text
fail closed
preserve both as contradiction evidence
never downgrade POSSIBLY_DISPATCHED/AT_RISK
never clear stop_latched
never allocate a replacement resource for an existing request_id
```

## 5. Global RequestLedger

### 5.1 Record

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
  updated_monotonic_ns: integer
```

Records are append-only transitions or transactionally equivalent versioned rows.

A later record for the same request ID must preserve the same request hash, operation, resource identity and transition identity. Same ID with a different hash/operation is a deterministic idempotency conflict.

### 5.2 Crash-safe request-intent rule

For every POST that can create a durable resource identity, schedule work, or change durable control state, the backend must determine the stable logical `resource_id` and/or `transition_id` **before** any domain scheduling or external/semantic side effect.

Then one bounded local safety transaction must durably create:

1. `RequestLedgerRecord(status=INTENT_DURABLE)` with that stable identity; and
2. the minimum corresponding domain/control record needed to prove that the identity exists and can be recovered.

Examples:

```text
POST /v1/runs
  -> RequestLedger INTENT_DURABLE(request_id -> run_id)
  + RunRecord(run_id, CREATED/NOT_SCHEDULED)
  atomically
  -> only then may scheduling begin

POST /v1/experiments/one-step
  -> RequestLedger INTENT_DURABLE(request_id -> experiment/run/action IDs)
  + created logical resource records with NOT_DISPATCHED action state
  atomically
  -> only then may scheduling begin

POST /v1/stop-all or /v1/reset-stop
  -> RequestLedger INTENT_DURABLE(request_id -> transition_id)
  before the transition; the later ControlStateRecord stores the same transition_id
```

An implementation may use one database transaction instead of files. It must provide equivalent atomicity.

A crash after the durable intent but before scheduling never permits allocation of a second logical resource. Recovery/replay returns the same identity. Mutation-capable scheduling does not automatically resume merely because the resource exists; Execution-v1 restart rules still apply.

A crash before `INTENT_DURABLE` means no domain scheduling/resource creation was permitted. Therefore absence of the mapping is positive proof that this request could not have created the protected resource/effect through the conforming path.

If atomicity between the request intent and minimum resource record cannot be proven after crash, mark the request/resource `RECOVERY_REQUIRED` and fail closed; do not allocate/re-execute a replacement.

## 6. Durable ControlState

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

- a first-ever clean safety store must durably create `INITIALIZE` before mutation admission;
- STOP writes `stop_latched=true` with its unique transition ID under Execution-v1 dispatch-gate ordering;
- reset writes `stop_latched=false` only after reset preconditions pass and its durability barrier succeeds;
- restart reads the latest valid record before mutation admission and carries a true latch forward into the fresh backend epoch;
- restart never treats a fresh `backend_epoch` as reset;
- missing/corrupt/contradictory control state when prior state may have existed produces `RECOVERY_REQUIRED`, effectively latched/fail-closed;
- a failed STOP/control-state write leaves the running backend locally fail-closed and any later uncertain store recovery remains fail-closed;
- `ControlStateRecord` contains no external Track A authority and cannot grant it.

## 7. ActionLedger record

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
  updated_monotonic_ns: integer
```

The transition to `DISPATCH_COMMITTED/POSSIBLY_DISPATCHED` is durability-coupled to BudgetLedger `AT_RISK` transition as required by Execution v1.

A later transition cannot legally move from possible-dispatched back to not-dispatched without authoritative reconciliation evidence proving no effect.

`CONFIRMED` is a terminal lifecycle state. Later evidence may supplement it but cannot rewrite it as a different control outcome.

## 8. BudgetLedger

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
  updated_monotonic_ns: integer
```

All values are non-negative checked integers.

Persist the ActionLedger dispatch commit and affected BudgetLedger at-risk transition in one atomic local transaction or a crash-safe protocol with equivalent all-or-conservative recovery semantics.

If atomicity cannot be proven after crash, recover the maximum plausible affected budget into `uncertain` before admitting new overlapping work.

## 9. Recovery record

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

Recovery never invents PASS.

`CONTRADICTORY` fails closed.

## 10. Manifest

```yaml
RunManifest:
  schema_version: 1
  artifact_contract_major: 1
  run_id: string
  scenario_id: string
  scenario_hash: lowercase_hex_sha256
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

Manifest contains no secrets or raw private communication.

## 11. Scenario artifact

Store the validated canonical Scenario-v1 AST as JSON:

```text
scenario.json
```

`scenario_hash` must equal SHA-256 over JCS/RFC-8785 canonical serialization defined by Scenario v1.

Do not persist unvalidated original YAML if it may contain rejected/secret data. A safe normalized source representation may be exported only after privacy/schema validation.

## 12. Events

`events.jsonl` contains one JSON object per normalized Adapter/Execution Event.

Rules:

- UTF-8;
- one complete JSON object per line;
- no secret-class values;
- `ingest_seq` strictly increases within one recorder instance;
- gaps may be represented if a producer/source failed, but no duplicate ingest sequence within one run recorder stream;
- ingestion order is not causal source order.

A write/truncation failure leaves the run incomplete/failed according to required evidence policy; it does not alter safety ledgers.

## 13. Actions evidence

`actions.jsonl` is a non-secret evidence projection of ActionLedger transitions/results.

It may omit internal persistence metadata not needed by later agents, but it must never claim `NOT_DISPATCHED` if safety state says possible/dispatched.

Safety ledger wins on contradiction.

## 14. Screenshot quarantine

Normal run screenshots contain only admitted `SAFE` material.

Potentially secret screenshots are held in a separate quarantine location not included in normal run manifest/export until sanitized/approved.

Quarantine identifiers/metadata may be recorded without secret pixels.

Rejected screenshot bytes are not copied into normal run artifacts.

## 15. Staging/finalization

Run lifecycle:

```text
ACTIVE
-> CLOSING
-> FINALIZED
```

During ACTIVE/CLOSING, evidence is written to staging or transactionally equivalent mutable tables.

Finalization requires:

1. no execution step can still mutate terminal result;
2. bounded late-event drain completed/expired;
3. required safety ledgers flushed;
4. required evidence files flushed;
5. hashes computed from exact final bytes;
6. `result.json` produced from authoritative run/action states;
7. final manifest written;
8. staging is atomically promoted to finalized view where filesystem semantics permit.

If any required finalization step fails:

```text
state = INCOMPLETE or FAILED
PASS is forbidden
```

## 16. Result envelope

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

A run containing unresolved mutation `AMBIGUOUS` cannot be overall PASS.

Unknown/failed required privacy or cleanup/evidence finalization cannot be silently represented as PASS.

## 17. Agent bundle

`agent_bundle.json` is a compact non-secret index, not a raw-artifact dump.

Minimum:

```yaml
AgentBundle:
  schema_version: 1
  run_id: string
  scenario_id: string
  scenario_hash: string
  result_status: string
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

## 18. Report

`report.md` is derived presentation only.

It must not be the source of truth for safety/recovery.

Any contradiction between report prose and machine-readable ledgers/results is a validation failure.

## 19. Supplements

After FINALIZED, the original finalized bytes/result remain immutable.

Later admitted evidence uses:

```text
supplements/<supplement-id>/manifest.json
```

with:

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

## 20. Hashing

Artifact hashes use SHA-256 lowercase hex over exact stored bytes.

Hash maps identify relative logical artifact path -> digest.

Do not hash secret material merely to include it; secret-class material is excluded before artifact construction.

## 21. Retention/bounds

Package B must define finite configurable retention limits for completed runs and large evidence, while never evicting:

- RequestLedger records still required to prevent duplicate domain work;
- ControlState/STOP state required for safe restart;
- Action/Budget records still required to prevent duplicate/unsafe recovery of an active/ambiguous run.

Eviction itself must not convert UNKNOWN/AMBIGUOUS into safe-to-retry and must not turn a latched STOP into unlatched state.

Git stores normalized durable evidence summaries/hashes only where current repository evidence policy permits it.

## 22. Package A deterministic artifact tests

At minimum:

1. validated scenario hash matches manifest;
2. run ID path traversal rejected;
3. Action/Budget dispatch commit atomicity or conservative crash recovery;
4. presentation write failure cannot erase safety state;
5. crash before finalization -> INCOMPLETE, never PASS;
6. unresolved ambiguous action prevents PASS;
7. corrupt contradictory safety/evidence state -> fail closed;
8. event JSONL ingest sequence validation;
9. secret-shaped Event rejected before write;
10. quarantined screenshot absent from normal manifest/export;
11. final artifact hashes match exact bytes;
12. finalized view cannot be silently mutated;
13. supplement cannot rewrite original result;
14. agent bundle contains only bounded non-secret references/summaries;
15. report contradiction with machine-readable result is validation failure;
16. global RequestLedger exists before a run and same request cannot allocate a second run after restart;
17. RequestLedger INTENT_DURABLE and minimum resource record are atomic/equivalent;
18. crash after request intent but before scheduling preserves the same resource identity without auto-resuming mutation;
19. first-ever ControlState initialization is durable before mutation admission;
20. STOP latch survives backend restart;
21. corrupt/missing ControlState fails closed rather than implicitly resetting STOP;
22. failed reset durability leaves STOP latched.

## 23. Compatibility

Artifact major version 1 is additive-only.

Changing safety-state precedence, request-intent atomicity, STOP/control-state durability, dispatch-journal durability, finalization immutability or secret exclusion requires a new major contract or separately reviewed compatible extension.