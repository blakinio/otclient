---
task_id: OTC-20260819-tibia-re-control-center-hardening
status: validating
agent: ChatGPT
project_lane: otclient
lane: P0-DESIGN-HARDENING
track_id: official-client-re
task_kind: architecture_contract_hardening
risk: medium
execution_mode: Chat/GitHub
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
implementation_pr: 605
restack_base_sha: c9156e72aa3c647054ff9dfc5ffed00e43a7e9cd
modules_touched: []
owned_paths:
  - docs/agents/CHANGELOG.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ARTIFACT_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_COMPARISON_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_CONTROL_API_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_SCENARIO_V1.md
  - docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_INDEPENDENT_AUDIT.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md
  - docs/agents/tasks/active/OTC-20260819-tibia-re-control-center-hardening.md
reuses:
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - canonical Track A lease/registration/Gate A/rebind/Gate B/whole-lifetime supervisor
  - tools/tibia_runtime_bridge/**
  - accepted exact Surveyor producer only after live state confirms acceptance
  - blakinio/Oteryn-v2 docs/architecture/ADR-0007-native-end-to-end-test-platform.md
depends_on:
  - merged Control Center design PR #600
  - merged audit-prompt PR #602
blocks:
  - Package A Control Center implementation until repaired exact head passes fresh independent audit with no P0/P1 and PACKAGE_A_IMPLEMENTATION_READY=YES
external_repositories:
  - blakinio/Oteryn-v2 read-only architecture dependency
invocation_started_at: 2026-08-20T08:52:00+02:00
last_progress_at: 2026-08-20T09:35:30+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 0
stall_warnings: 0
---

# TIBIA RE Control Center architecture hardening

## Objective

Repair the Control Center design/contracts after the independent audit so Package A can be implemented without inventing safety semantics. This task remains documentation/contracts only and `runtime_access:none`; it performs no official-client observation/mutation, KasmVNC input, credentials/login/gameplay or Oteryn-v2 writes.

## Trusted-base reconciliation

Initial repair work started from `main@fdabf235ed4438bd7c376932ed876bd0bbef019a`. During validation `main` advanced to:

```text
c9156e72aa3c647054ff9dfc5ffed00e43a7e9cd
```

The verified `fdabf235...c9156e72` change contains only four Surveyor-v2 prompt/evidence/archive paths and has no overlap with the 12 Control Center owned paths. The final repair will be restacked as one clean commit directly on the latest revalidated main; this checkpoint must be refreshed again if main moves before branch freeze/merge.

## Independent-audit findings

Former #605 head `5e63a0ec988cf4fa7789274f13c9d654254e8e44` failed the independent audit. The repair closes:

- `CC-AUD-001` — Scenario v1 now defines exact `SideEffectBudget`, `AbortCondition`, `SemanticFieldPath`, immutable `SemanticFieldRegistry`, built-in core registry and discriminated semantic references; no free-form destination/predicate schema remains.
- `CC-AUD-002` — `CONFIRMED` is the single successful terminal action lifecycle state; late callbacks are evidence only.
- `CC-AUD-003` — durable `ControlStateRecord`, STOP persistence, fail-closed STOP-write failure, restart latch recovery and explicit durable reset are normative; under `dispatch_gate` only bounded `DISPATCH_COMMIT | STOP_TRANSITION | RESET_TRANSITION` local safety-store I/O is allowed.
- `CC-AUD-004` — global RequestLedger + ResourceIdentityLedger atomically/equivalently persist stable run/experiment/action identity before protected scheduling; crash replay cannot allocate a replacement.
- `CC-AUD-005` — programme/MVP/audit mandatory reads include Artifact and Comparison contracts.
- `CC-AUD-006` — task ownership equals the intended exact 12 paths.
- `CC-AUD-007` — retry attempts are total attempts `1..3`; zero is invalid and omitted retry is one attempt.
- `CC-AUD-008` — authoritative RequestLedger/ResourceIdentityLedger are global `control/safety` state; per-run request data is projection only.
- `CC-AUD-009` — repair was reconciled with the newer trusted main and will be revalidated again at final freeze.
- `CC-AUD-010` — Control API v1 mandates CSP `frame-ancestors 'none'`; ordinary configuration cannot weaken it.

## Additional self-review findings and repairs

The implementing session performed a second full contract review and found additional gaps before freezing the PR:

- `SR-001` FIXED — `SideEffectBudget` had `max_runtime_seconds` but EffectBound/runtime execution semantics were incomplete. Scenario/Execution now define an absolute monotonic run deadline, per-attempt total action timeout/fit check, no extension by pause/retry/ambiguity and non-time-only `AT_RISK/uncertain` accounting.
- `SR-002` FIXED — `SemanticFieldPath` originally referred to a typed schema without a normative registry contract. Scenario v1 now defines immutable `SemanticFieldRegistry` ID/version/descriptors and built-in `control-center.core@1.0.0`.
- `SR-003` FIXED — Adapter v1 originally had no normative registry advertisement/projection boundary. It now defines `SemanticRegistryDescriptor`, JCS/SHA-256 registry hashing, exact registry retrieval and typed passive `SemanticFieldValue` projection; arbitrary snapshot-object predicate traversal is forbidden.
- `SR-004` FIXED — Artifact/Control API originally said "minimum resource record" without defining the record. Artifact v1 now defines global `ResourceIdentityRecord`; run and one-step creation atomically/equivalently persist RequestLedger `INTENT_DURABLE` plus `CREATED_NOT_SCHEDULED` resource identity before scheduling.
- `SR-005` FIXED — programme architecture still described Artifact state as per-run only and omitted newer contracts from the normative stack. Programme v2.1 now models Global Safety Store separately from per-run Artifact/Safety state and includes Scenario/Execution/Adapter/Artifact/Control API/Comparison as mutually normative.
- `SR-006` FIXED — prompts lagged the repaired contracts. MVP/audit prompt contracts are now v2.1.0 and cover semantic-registry drift/hash, resource identity, runtime deadlines, durable STOP/reset and 57 audit falsification cases.

No unresolved material self-review finding is currently known. This is implementer self-review only and is not independent review evidence.

## Prompt evaluation

Prompt changes are treated as behavioural code under `PROMPT_EVAL_STANDARD.md`.

```yaml
prompt_contract_evaluation:
  candidate_surfaces:
    - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md@2.1.0
    - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_INDEPENDENT_AUDIT.md@2.1.0
  baseline:
    head: 5e63a0ec988cf4fa7789274f13c9d654254e8e44
    mvp_blob: 4bae88b542effd26a431b5e90b5ed22d47f15c62
    audit_blob: 4ae856ecf7369c1f8183d74f030eb88f0f1273d3
  eval_suite: manual deterministic contract matrix below
  automation: NOT_AVAILABLE
  repeated_model_trials: NOT_RUN
  reason: no repository-owned executable model/prompt-eval harness was found or authorized for this documentation repair; deterministic contract inspection is used and is not described as automated/model evaluation
  rollback: restore the named baseline blobs/head semantics
  safety_regression_allowed: false
```

### Manual deterministic contract matrix

| Case | Candidate expected contract result | Static result |
|---|---|---|
| ordinary bounded Scenario action | typed schema/registry/budget/capability validation required | PASS |
| `retry.max_attempts=0` | validation rejection | PASS |
| free-form DestinationRef or wrong union fields | discriminated-schema rejection | PASS |
| wildcard/bracket/unregistered SemanticFieldPath | validation rejection | PASS |
| adapter registry descriptor/hash mismatch | reject before scenario execution | PASS |
| same semantic registry ID/version changes descriptor | incompatible/fail closed | PASS |
| `SNAPSHOT_PATH` lacks checkpoint or wrong ENTITY_REF/ITEM_REF type | validation/refusal | PASS |
| runtime deadline expires during pause | no deadline extension; no mutation resume | PASS |
| STOP latched then backend restart | fresh epoch remains STOPPED until durable reset | PASS |
| STOP safety-store write fails | mutation remains fail-closed | PASS |
| reset outcome uncertain after crash | no auto-reset; latched/RECOVERY_REQUIRED | PASS |
| POST run crashes after durable request/resource pair before scheduling | same run ID survives; no replacement/no auto-resume | PASS |
| one-step crashes after durable pair before scheduling | same experiment/run/action IDs survive | PASS |
| contradictory duplicate resource/run identity | fail closed | PASS |
| hostile website directly calls loopback API | Host+Origin+nonce reject | PASS |
| hostile website frames real UI | CSP `frame-ancestors 'none'` rejects framing | PASS |
| Package A attempts official runtime access | refuse; `runtime_access:none` | PASS |
| Package D uses cached Control Center authority | refuse; fresh then-current Track A admission required | PASS |
| exact reviewed head changes after audit | prior audit invalid; new exact-head audit mandatory | PASS |
| Surveyor producer is not accepted | Package C unavailable until accepted exact producer | PASS |
| Oteryn adapter attempts second E2E authority | reuse/extend ADR-0007; refuse parallel authority | PASS |
| related required PR remains open | task cannot be terminally completed | PASS |

`PASS` above means the candidate text contains a deterministic rule matching the expected contract. It is not runtime, CI, implementation, model-trial or independent-audit evidence.

## Safety invariants

```text
scenario validity
!= semantic registry support
!= capability support
!= evidence maturity
!= freshness
!= mutation authority
```

```text
STOP wins dispatch_gate -> durable STOP/new generation -> no stale commit
commit wins dispatch_gate -> POSSIBLY_DISPATCHED + applicable non-time AT_RISK durable before later STOP
```

```text
request_id -> transport/domain dedupe
resource_id -> stable durable run/experiment identity
action_id -> semantic action-attempt dedupe
RequestLedger + ResourceIdentityRecord durable before scheduling
possible dispatch -> no automatic retry
restart -> fresh backend_epoch, never implicit STOP reset
```

Control Center never becomes Track A lease/registration/Gate/GUI-input authority.

## Validation state

Runtime E2E for this documentation-only repair:

```text
NOT_APPLICABLE
reason: this task changes architecture/contracts/prompts only and is explicitly runtime_access:none
```

Still required before readiness:

1. re-fetch current main; reconcile if it moved;
2. create/freeze one clean repair commit directly on that current main;
3. inspect exact changed-file inventory and full diff; require exactly the declared 12 paths;
4. run focused static/document/governance checks on final tree;
5. verify PR #605 still points to the expected old audited head before replacing its branch ref;
6. move #605 to the exact verified repair head and keep it Draft;
7. run/inspect required exact-head CI/governance checks;
8. obtain a genuinely fresh independent audit of the unchanged repaired head;
9. merge/start Package A only if P0/P1 are NONE, every safety-critical falsification is SAFE_DEFINED, `PACKAGE_A_IMPLEMENTATION_READY=YES`, exact-head checks are green, PR is mergeable and all repository gates pass.

No exact-head CI or independent PASS is claimed yet.

## Next action

Freeze the clean restacked head, move PR #605 only after verifying its old head, inspect exact-head checks, then hand the unchanged head to a fresh independent audit.