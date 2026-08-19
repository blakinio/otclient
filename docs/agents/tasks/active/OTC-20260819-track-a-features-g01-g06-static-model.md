---
task_id: OTC-20260819-track-a-features-g01-g06-static-model
status: ready
phase: validate
session_id: chatgpt-20260819-features-g01-g06-01
session_role: researcher
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: static_capability_census
execution_mode: github-only
execution_reason: repository evidence synthesis and narrow documentation changes are fully supported by the GitHub connector
execution_class: github_hosted
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
user_communication: terminal_only
policy_version: 2
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: G01-G06 form one coherent Cyclopedia/Bestiary/Charm/Monster-Bonus read-only static package with shared evidence sources
base_main: 82e5f435c3aa4172115bf7f6a0cd7a5cc6da3d50
branch: research/OTC-20260819-track-a-features-g01-g06-static-model
pr: 557
worktree: github-connector-branch
evidence_complete_head: 5bd5a12e58d92b5f45fe19a30121a2823d3b9b07
owned_paths:
  - docs/agents/tasks/active/OTC-20260819-track-a-features-g01-g06-static-model.md
  - docs/agents/evidence/OTC-20260819-track-a-features-g01-g06-static-model/**
  - docs/agents/reports/OTCLIENT-20260819-track-a-features-g01-g06-static-model.md
dependencies:
  - PR #536 shared full-client matrix/checklist is read-only input; this task did not edit its shared coverage paths
  - PR #555 current-client fence advance is separate and unmerged; this task makes no current-runtime/current-fence authority claim
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
physical_e2e_required: false
persistent_session_role: none
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
login_authorized: false
credential_use_authorized: false
gui_input_authorized: false
gameplay_authorized: false
transaction_authorized: false
owner_funded_ai_used: false
invocation_started_at: 2026-08-19T09:24:00+02:00
last_progress_at: 2026-08-19T09:39:20+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# TIBIA-RE-FEATURES — G01-G06 static model package

## Objective

Produce one bounded `DRAFT / NOT PROMOTED` Track A package for:

- `G01` Cyclopedia shell/request-cache model;
- `G02` Cyclopedia map;
- `G03` Cyclopedia houses data/actions;
- `G04` Bestiary kills/unlocks/loot/progress;
- `G05` Charms selection/assignment;
- `G06` Monster Bonus Effects.

The package is repository-only and read-only. It maps retained exact-build generated-message evidence, direct protocol-handler type xrefs, and retained model/storage/controller/action leads into explicit `FACT`, `INFERENCE`, `UNKNOWN`, and `DISPROVEN/SUPERSEDED` classifications. Static presence is not promoted to live semantics, ABI correctness, dispatcher ownership, server acceptance, current-build identity, or current runtime state.

## Safety boundary

No official-client runtime, Synology/KasmVNC session, process memory, login, credentials, GUI input, gameplay, purchase, reroll, charm assignment/removal, monster-bonus assignment/clear, or other character/resource mutation was authorized or performed.

The researched retained static fence is historical exact-build evidence only:

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

Current-build/current-runtime authority remains `UNKNOWN` for this task. PR #555 is not trusted-base authority while unmerged.

## Deliverables

- `docs/agents/evidence/OTC-20260819-track-a-features-g01-g06-static-model/index.md`
- `docs/agents/evidence/OTC-20260819-track-a-features-g01-g06-static-model/classification-summary.md`
- `docs/agents/reports/OTCLIENT-20260819-track-a-features-g01-g06-static-model.md`
- Draft PR #557

## Acceptance

- [x] Preserve the complete Track A `runtime_access: none` admission record.
- [x] Record the exact G01-G06 row names and current pre-package status without editing PR #536 shared paths.
- [x] Enumerate retained exact-build C2S/S2C message evidence for each covered row where present.
- [x] Enumerate direct handler/storage/controller/action leads without claiming an unproven dispatcher or live edge.
- [x] Distinguish `FACT`, `INFERENCE`, `UNKNOWN`, and `DISPROVEN/SUPERSEDED` explicitly.
- [x] State whether this package justifies any row-status promotion; researcher recommendation is no status change.
- [x] Keep E2E `NOT_APPLICABLE` with a concrete repository-only reason.
- [x] Deliver as a Draft PR; researcher did not merge or edit canonical programme coverage.

## Draft disposition

```yaml
G01: keep_NOT_STARTED
G02: keep_PARTIAL
G03: keep_NOT_STARTED
G04: keep_NOT_STARTED
G05: keep_NOT_STARTED
G06: keep_NOT_STARTED
canonical_coverage_modified: false
promotion_decision: PENDING_COORDINATOR
```

## Validation boundary

Focused source validation re-read the retained complete C2S/S2C registries, the direct handler-xref table, the capability census and merged PR #435's structural claim boundary. The report explicitly preserves `semantic_dispatcher_edge_proven=false` and all live/current-build semantic edges as `UNKNOWN`.

`E2E: NOT_APPLICABLE` — this is documentation/evidence-only work with `runtime_access: none`; no product or runtime behavior changed.

Independent coordinator falsification is still required by the parallel researcher contract. This researcher must stop at the Draft PR boundary and must not self-promote or self-merge.

## Checkpoint

```yaml
last_completed_step: persisted the bounded G01-G06 evidence index, explicit classification summary and static report in Draft PR #557
evidence_complete_head: 5bd5a12e58d92b5f45fe19a30121a2823d3b9b07
validation_level: focused_repository_source_reread
evidence_index: docs/agents/evidence/OTC-20260819-track-a-features-g01-g06-static-model/index.md
report: docs/agents/reports/OTCLIENT-20260819-track-a-features-g01-g06-static-model.md
independent_audit: PENDING_COORDINATOR
e2e: NOT_APPLICABLE
blocker: none
next_action: TIBIA-RE-COORDINATOR independently review Draft PR #557 and choose ACCEPT, ACCEPT_WITH_EDITS, RETURN_FOR_EVIDENCE, or REJECT/SUPERSEDE
```
