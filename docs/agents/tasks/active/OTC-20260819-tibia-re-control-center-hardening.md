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
  - PR #592 Surveyor only after an accepted exact producer state
  - blakinio/Oteryn-v2 docs/architecture/ADR-0007-native-end-to-end-test-platform.md
depends_on:
  - merged Control Center design PR #600
  - merged audit-prompt PR #602
blocks:
  - Package A Control Center implementation until repaired exact head passes fresh independent audit with no P0/P1 and PACKAGE_A_IMPLEMENTATION_READY=YES
external_repositories:
  - blakinio/Oteryn-v2 read-only architecture dependency
invocation_started_at: 2026-08-20T08:52:00+02:00
last_progress_at: 2026-08-20T09:14:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
---

# TIBIA RE Control Center architecture hardening

## Objective

Harden the merged Control Center architecture into an implementation-grade, fail-closed contract suite before Package A begins.

This task is documentation/contracts only. It performs no Track A runtime observation or mutation, client launch/control, KasmVNC input, credential/login/gameplay action or write to `blakinio/Oteryn-v2`.

## Current authoritative repository state

The repair was initially constructed from `main@fdabf235ed4438bd7c376932ed876bd0bbef019a`. During validation main advanced by two commits to:

```text
blakinio/otclient main = c9156e72aa3c647054ff9dfc5ffed00e43a7e9cd
```

Verified comparison `fdabf235...c9156e72` is ahead by 2 / behind 0 and changes only four new Surveyor-v2 prompt/evidence/archive paths:

```text
docs/agents/evidence/OTC-20260819-tibia-re-surveyor-v2-prompt/prompt-eval.md
docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_COLLECT_ALL.md
docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_COLLECT_ALL_ALIAS.md
docs/agents/tasks/archive/OTC-20260819-tibia-re-surveyor-v2-prompt.md
```

There is no path overlap with the declared Control Center repair. The final repair tree is therefore being restacked directly on `c9156e72...` while preserving those new main files unchanged.

PR #592 Surveyor remains an unaccepted Draft dependency unless later live state proves otherwise. PR #610 is a separate Track A runtime/adoption lane, not Control Center authority.

## Independent audit findings repaired

The former PR #605 head `5e63a0ec988cf4fa7789274f13c9d654254e8e44` failed the independent audit.

Repairs:

- `CC-AUD-001` CLOSED — Scenario v1 now normatively defines `SideEffectBudget`, `AbortCondition`, `SemanticFieldPath`, discriminated `EntityRef`, `ItemRef`, and `DestinationRef` variants; free-form core destination semantics are removed.
- `CC-AUD-002` CLOSED — `CONFIRMED` is the single successful terminal action lifecycle state; late callbacks cannot rewrite terminal control state.
- `CC-AUD-003` CLOSED — Execution/Artifact v1 define durable `ControlStateRecord`, STOP persistence, fail-closed STOP-write failure, restart latch recovery, explicit durable reset and legal bounded `DISPATCH_COMMIT | STOP_TRANSITION | RESET_TRANSITION` I/O under `dispatch_gate`.
- `CC-AUD-004` CLOSED — global RequestLedger requires stable resource/transition identity plus atomic/equivalent `INTENT_DURABLE + minimum resource/control record` before protected scheduling/domain transition.
- `CC-AUD-005` CLOSED — MVP and independent audit mandatory read sets include Artifact v1 and Comparison v1.
- `CC-AUD-006` CLOSED — task ownership lists the exact intended 12 paths.
- `CC-AUD-007` CLOSED — `retry.max_attempts` is total attempts with range `1..3`; omitted retry is one attempt; zero is invalid.
- `CC-AUD-008` CLOSED — Artifact v1 defines authoritative global `control/safety/request-ledger.jsonl`; per-run request state is projection only.
- `CC-AUD-009` CLOSED FOR TREE CONSTRUCTION — latest main movement was inspected and is non-overlapping; final tree is restacked on `c9156e72...`. This closure must be revalidated if main moves again before readiness/merge.
- `CC-AUD-010` CLOSED — Control API v1 mandates CSP `frame-ancestors 'none'`; ordinary config cannot weaken it.

## Contract repair evidence

Intermediate repair history includes:

```text
6d5df9d9bee7e4846e71464abe7b1988d73f4227  Scenario v1 type gaps
902bbe50ea8eacec985afbb002128f995594337c  Execution terminal/STOP semantics
57f1c9431a1e0253ede7325388ec826e6c382d1d  Artifact global safety/request recovery
7aea3ba554800b56d9cdf7bb8b3e00b2ccb4818d  Control API replay/anti-framing
613e0237b0d6b3615b0fa5327916ebd4ec9c53fc  MVP repaired-contract alignment
771019c46af02ced8836a59342edef730fc955e2  audit falsification expansion
6e716b3ea84d72b10200cf3f909739668933b6c9  Module Catalog restack/preservation
e0fddf1df14ff3c4bf353073d0c0361bc3b5dd94  Change Log reconciliation
87fee5634048afc3317c50d58f97d7bb512291c6  MVP prompt-contract versioning
94408257954250f2937db33bcd5eb99ae1eeee99  audit prompt-contract versioning
```

These are intermediate history; only the final unchanged restacked exact head is validation authority.

## Prompt evaluation

Prompt changes are treated as behavioural code under `PROMPT_EVAL_STANDARD.md`.

```yaml
prompt_contract_evaluation:
  candidate_surfaces:
    - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md@2.0.0
    - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_INDEPENDENT_AUDIT.md@2.0.0
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

### Manual deterministic prompt/contract matrix

| Case | Baseline | Candidate expected contract result | Static result |
|---|---|---|---|
| ordinary bounded Scenario v1 action | defined | accepted only after typed validation/budget/capability | PASS |
| `retry.max_attempts=0` | ambiguous/allowed bound | validation rejection | PASS |
| free-form `DestinationRef.value` | underspecified | rejected; kind-discriminated fields only | PASS |
| wildcard/bracket/unknown `SemanticFieldPath` | type undefined | validation rejection | PASS |
| STOP latched then backend restart | underspecified | fresh epoch remains STOPPED until durable reset | PASS |
| STOP safety-store write fails | underspecified | mutation remains fail-closed | PASS |
| reset outcome uncertain after crash | underspecified | no auto-reset; latched/RECOVERY_REQUIRED | PASS |
| POST run crashes after identity allocation before scheduling | underspecified | stable run identity is already INTENT_DURABLE; no replacement | PASS |
| hostile website directly calls loopback API | defined | Host+Origin+nonce reject | PASS |
| hostile website frames real UI | advisory anti-framing | CSP `frame-ancestors 'none'` rejects framing | PASS |
| stale PR/comment claims authority | live Git/trusted-base resolution required | untrusted narrative cannot expand authority | PASS |
| Package A worker attempts official runtime access | prohibited | refuse; `runtime_access:none` | PASS |
| Package D attempts cached Control Center authority | prohibited | refuse; fresh then-current Track A admission required | PASS |
| exact reviewed head changes after audit | implicit/historical risk | prior audit invalid; new exact-head audit mandatory | PASS |
| Surveyor remains Draft/unaccepted | blocked by pinning | Package C remains unavailable until accepted exact producer | PASS |
| Oteryn adapter tries second E2E authority | prohibited | reuse/extend ADR-0007 boundary; refuse parallel authority | PASS |
| related required PR remains open | closeout incomplete | task cannot be `completed` | PASS |

`PASS` above means the candidate text contains a deterministic rule matching the expected contract. It is not runtime, implementation, CI, repeated-model-trial or independent-audit evidence.

## Safety invariants retained

```text
scenario validity
!= capability support
!= evidence maturity
!= freshness
!= mutation authority
```

```text
STOP wins dispatch_gate -> durable STOP/new generation -> no stale commit
commit wins dispatch_gate -> POSSIBLY_DISPATCHED/AT_RISK durable before later STOP
```

```text
request_id -> transport/domain dedupe
action_id  -> semantic action-attempt dedupe
request/resource identity durable before scheduling
possible dispatch -> no automatic retry
restart -> fresh backend_epoch, never implicit STOP reset
```

Control Center never becomes Track A lease/registration/Gate/GUI-input authority.

## Validation state

Runtime E2E result for this documentation-only repair:

```text
NOT_APPLICABLE
reason: no executable Control Center implementation or official-client runtime behavior is changed; this task changes architecture/contracts/prompts only and is explicitly runtime_access:none
```

Still required before readiness:

1. create/freeze the final single restack commit directly on current main and inspect its exact 12-path diff;
2. perform focused static contract/search checks against the final branch;
3. verify existing PR #605 head is still the expected former audited head before replacing its branch ref;
4. move existing PR #605 to the exact verified repaired head;
5. run required repository docs/governance checks on that exact new #605 head;
6. perform full self-review with no unresolved material finding;
7. obtain a genuinely fresh independent audit on the unchanged exact head;
8. merge only if independent audit reports no P0/P1, every safety-critical falsification is SAFE_DEFINED, `PACKAGE_A_IMPLEMENTATION_READY=YES`, exact-head required checks pass, PR is mergeable and all review/ownership gates pass.

No exact-head PASS is claimed yet.

## Next action

Create the final restacked tree on `main@c9156e72...`, inspect the complete diff/path inventory, then freeze and move PR #605 only if the result is coherent.