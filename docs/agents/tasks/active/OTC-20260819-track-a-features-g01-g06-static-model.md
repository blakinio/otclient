---
task_id: OTC-20260819-track-a-features-g01-g06-static-model
status: investigating
phase: investigate
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
worktree: github-connector-branch
owned_paths:
  - docs/agents/tasks/active/OTC-20260819-track-a-features-g01-g06-static-model.md
  - docs/agents/evidence/OTC-20260819-track-a-features-g01-g06-static-model/**
  - docs/agents/reports/OTCLIENT-20260819-track-a-features-g01-g06-static-model.md
dependencies:
  - PR #536 shared full-client matrix/checklist is read-only input; this task must not edit its shared coverage paths
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
last_progress_at: 2026-08-19T09:24:00+02:00
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

The package is repository-only and read-only. It will map exact retained generated-message evidence, direct protocol-handler type xrefs, and retained model/storage/controller/action leads into explicit `FACT`, `INFERENCE`, and `UNKNOWN` claims. Static presence must not be promoted to live semantics, ABI correctness, dispatcher ownership, server acceptance, current-build identity, or current runtime state.

## Safety boundary

No official-client runtime, Synology/KasmVNC session, process memory, login, credentials, GUI input, gameplay, purchase, reroll, charm assignment/removal, monster-bonus assignment/clear, or other character/resource mutation is authorized or required by this package.

The researched retained static fence is historical exact-build evidence only:

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

Current-build/current-runtime authority remains `UNKNOWN` for this task. PR #555 is not trusted-base authority while unmerged.

## Primary evidence inputs

- `docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md`;
- `docs/agents/reports/OTCLIENT-20260818-track-a-s1-unfiltered-static-census.md`;
- `docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-client-to-server.txt`;
- `docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-server-to-client.txt`;
- `docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-handler-code-xrefs.tsv`;
- merged P0 Cyclopedia evidence from PR #435 as an existing G02 structural input;
- PR #536 checklist/matrix only as read-only scope/status input.

## Acceptance

- [ ] Preserve the complete Track A `runtime_access: none` admission record.
- [ ] Record the exact G01-G06 row names and current pre-package status without editing PR #536 shared paths.
- [ ] Enumerate retained exact-build C2S/S2C message evidence for each covered row where present.
- [ ] Enumerate direct handler/storage/controller/action leads without claiming an unproven dispatcher or live edge.
- [ ] Distinguish `FACT`, `INFERENCE`, `UNKNOWN`, and `DISPROVEN/SUPERSEDED` explicitly.
- [ ] State whether this package justifies any row-status promotion; default fail-closed when semantic proof is absent.
- [ ] Keep E2E `NOT_APPLICABLE` with a concrete repository-only reason.
- [ ] Deliver as a Draft PR; researcher must not merge or edit canonical programme coverage.

## Checkpoint

```yaml
last_completed_step: resolved TIBIA-RE-FEATURES and selected non-overlapping bounded G01-G06 repository-only package from current main
validation_level: focused
evidence_index: docs/agents/evidence/OTC-20260819-track-a-features-g01-g06-static-model/index.md
blocker: none
next_action: persist the dedicated G01-G06 evidence/report package and open/update the Draft PR for coordinator review
```
