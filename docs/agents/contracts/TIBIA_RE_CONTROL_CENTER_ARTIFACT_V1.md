# TIBIA RE Control Center Artifact Contract v1

```yaml
contract_id: TIBIA-RE-CONTROL-CENTER-ARTIFACT-V1
version: 1.0
major_version: 1
status: normative_design
producer_repository: blakinio/otclient
contains_secrets: forbidden
```

## 1. Purpose

Define the deterministic per-run persistence envelope used by Package A tests and Package B+ durable storage/export.

This contract separates:

1. **safety state** required to prevent duplicate/unsafe mutation after crash;
2. **evidence state** used for analysis;
3. **presentation/export state** used by browser/CLI/agents.

Presentation failure must never erase or downgrade safety state.

## 2. Logical storage root

The implementation chooses a repository-conformant runtime data root. Under that root, one run owns:

```text
runs/<run-id>/
  safety/
    request-ledger.jsonl
    action-ledger.jsonl
    budget-ledger.json
    recovery.json
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

Physical filenames/directories may be implemented through a transactional database plus export materialization, but the logical records and atomicity semantics must remain equivalent.

Do not store large/raw capture bytes in Git unless current evidence policy explicitly permits them.

## 3. File and directory safety

Run/artifact IDs are validated opaque non-secret IDs, never user-supplied filesystem paths.

All filesystem implementations must:

- construct paths from validated IDs only;
- reject path separators, `..`, NUL and absolute paths in IDs;
- use no symlink-following when materializing run-owned files where practical;
- keep temporary/final rename targets inside the selected runtime root;
- create sensitive local-control/safety metadata with owner-only permissions where the platform permits;
- never materialize the Control API nonce into run artifacts.

## 4. Safety-state precedence

`safety/` or its database equivalent is the authoritative local source for:

- RequestLedger dedupe;
- ActionLedger dispatch state;
- BudgetLedger reserved/at-risk/committed/uncertain state;
- backend/recovery classification.

If presentation/evidence records disagree with safety state:

```text
fail closed
preserve both as contradiction evidence
never downgrade POSSIBLY_DISPATCHED/AT_RISK based on presentation text
```

## 5. RequestLedger record

```yaml
RequestLedgerRecord:
  schema_version: 1
  request_id: string
  request_hash: lowercase_hex_sha256
  operation: string
  resource_id: string | null
  backend_epoch_created: string
  status: ACCEPTED | COMPLETED | FAILED
  response_code: integer
  response_body_hash: lowercase_hex_sha256 | null
  created_monotonic_ns: integer
  updated_monotonic_ns: integer
```

Records are append-only transitions or transactionally equivalent versioned rows.

A later record for the same request ID must preserve the same request hash/operation/resource identity.

## 6. ActionLedger record

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

## 7. BudgetLedger

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

## 8. Recovery record

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

## 9. Manifest

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

## 10. Scenario artifact

Store the validated canonical Scenario-v1 AST as JSON:

```text
scenario.json
```

`scenario_hash` must equal SHA-256 over JCS/RFC-8785 canonical serialization defined by Scenario v1.

Do not persist unvalidated original YAML if it may contain rejected/secret data. A safe normalized source representation may be exported only after privacy/schema validation.

## 11. Events

`events.jsonl` contains one JSON object per normalized Adapter/Execution Event.

Rules:

- UTF-8;
- one complete JSON object per line;
- no secret-class values;
- `ingest_seq` strictly increases within one recorder instance;
- gaps may be represented if a producer/source failed, but no duplicate ingest sequence within one run recorder stream;
- ingestion order is not causal source order.

A write/truncation failure leaves the run incomplete/failed according to required evidence policy; it does not alter safety ledgers.

## 12. Actions evidence

`actions.jsonl` is a non-secret evidence projection of ActionLedger transitions/results.

It may omit internal persistence metadata not needed by later agents, but it must never claim `NOT_DISPATCHED` if safety state says possible/dispatched.

Safety ledger wins on contradiction.

## 13. Screenshot quarantine

Normal run screenshots contain only admitted `SAFE` material.

Potentially secret screenshots are held in a separate quarantine location not included in normal run manifest/export until sanitized/approved.

Quarantine identifiers/metadata may be recorded without secret pixels.

Rejected screenshot bytes are not copied into normal run artifacts.

## 14. Staging/finalization

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

## 15. Result envelope

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

## 16. Agent bundle

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

## 17. Report

`report.md` is derived presentation only.

It must not be the source of truth for safety/recovery.

Any contradiction between report prose and machine-readable ledgers/results is a validation failure.

## 18. Supplements

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

## 19. Hashing

Artifact hashes use SHA-256 lowercase hex over exact stored bytes.

Hash maps identify relative logical artifact path -> digest.

Do not hash secret material merely to include it; secret-class material is excluded before artifact construction.

## 20. Retention/bounds

Package B must define finite configurable retention limits for completed runs and large evidence, while never evicting safety records still required to prevent duplicate/unsafe recovery of an active/ambiguous run.

Eviction itself must not convert UNKNOWN/AMBIGUOUS into safe-to-retry.

Git stores normalized durable evidence summaries/hashes only where current repository evidence policy permits it.

## 21. Package A deterministic artifact tests

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
15. report contradiction with machine-readable result is validation failure.

## 22. Compatibility

Artifact major version 1 is additive-only.

Changing safety-state precedence, dispatch-journal durability, finalization immutability or secret exclusion requires a new major contract or separately reviewed compatible extension.