---
task_id: OTC-20260821-control-center-parallel-agent-prompts
status: implementing
agent: ChatGPT
project_lane: otclient
lane: CONTROL-CENTER-PARALLEL-PROMPTS
track_id: official-client-re
task_kind: prompting_coordination
phase: implementation
risk: medium
branch: docs/control-center-parallel-agent-prompts-20260821
base_branch: main
created: 2026-08-21T17:45:00+02:00
updated: 2026-08-21T17:45:00+02:00
initial_base_sha: 532b54fa60d11ae10227ab16dc02cd0cadf39b23
related_pr: null
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
network_listener_allowed: false
official_client_access: false
policy_version: 2
prompting_standard_version: 2.1
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
user_communication: low_noise
owned_paths:
  - docs/agents/tasks/active/OTC-20260821-control-center-parallel-agent-prompts.md
  - docs/agents/tasks/archive/OTC-20260821-control-center-parallel-agent-prompts.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_PACKAGE_B_PARALLEL_AGENT.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_PACKAGE_B_ALIAS.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_PACKAGE_C_PARALLEL_AGENT.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_PACKAGE_C_ALIAS.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_PACKAGE_D_PREP_PARALLEL_AGENT.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_PACKAGE_D_PREP_ALIAS.md
  - docs/agents/evidence/OTC-20260821-control-center-parallel-agent-prompts/prompt-eval.md
modules_touched: []
reuses:
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md
  - docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_CONTROL_API_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ARTIFACT_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_POLICY_BOUNDARY_V1.md
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPT_EVAL_STANDARD.md
depends_on:
  - main includes terminal Control Center Package A lifecycle closeout at 532b54fa60d11ae10227ab16dc02cd0cadf39b23
blocks:
  - direct owner launch of dedicated Package B, Package C and Package D-preparation workers by short alias
cross_repository_tasks: []
ownership_released: false
prompt_contract:
  version: 1.0.0
  changed_surfaces:
    - worker prompts
    - alias prompts
    - parallel ownership/dependency routing
  objective: permit safe parallel Control Center Package B, Package C and runtime-independent Package D preparation without shared branch/worktree ownership or accidental runtime authority expansion
  baseline_version: docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md@9dee1f97694a591b1f9a784556f1357f966c2e57
  eval_suite: docs/agents/evidence/OTC-20260821-control-center-parallel-agent-prompts/prompt-eval.md
  rollback_version: docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md@9dee1f97694a591b1f9a784556f1357f966c2e57
---

# Control Center parallel worker prompt publication

## Objective

Publish three bounded autonomous worker prompts and short aliases so the owner can launch Package B, Package C and Package D preparation in parallel while preserving current repository ownership, Track A fail-closed authority and Package A contracts.

## Feature scope

```yaml
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
complete_user_facing_feature: false
```

## Parallelization contract

- Package B and Package C may execute concurrently after each performs a fresh live overlap check and claims separate branches/tasks/worktrees.
- Package D worker is preparation-only in this wave: static adapter mapping, contract reconciliation, deterministic fakes/tests and a concrete runtime admission plan are allowed; official-client observation/mutation, GUI input, process access and canonical runtime transitions are forbidden.
- Real Package D runtime work remains a separate future task after current dependencies and authority gates are revalidated.
- No worker may share a branch/worktree or treat these prompt files as task ownership.
- Shared catalogue/changelog edits are not pre-leased by these prompts; each worker must revalidate ownership immediately before any required shared-index edit and defer/serialize on overlap.

## Acceptance

- [ ] Three canonical worker prompts exist for Package B, Package C and Package D preparation.
- [ ] Three owner-facing alias prompts resolve to those canonical worker prompts.
- [ ] Every worker prompt requires current-main/open-PR/active-task/AGENTS revalidation before claiming work.
- [ ] Package B remains `runtime_access:none`, with real Official Tibia mutation impossible and fake mutation only.
- [ ] Package C is read-only and consumes an accepted exact Surveyor producer/schema/interface without copying Surveyor internals or promoting evidence.
- [ ] Package D preparation is `runtime_access:none` and cannot perform official-client process observation, memory access, GUI/gameplay input or mutation.
- [ ] Ownership boundaries are non-overlapping by default and instruct workers to split shared core changes into an explicitly coordinated producer task rather than editing each other's paths.
- [ ] Dependency order makes B/C parallel, D-prep parallel-static, and real D runtime gated after dependency/authority revalidation.
- [ ] Prompts preserve Control Center Scenario/Execution/Artifact/Policy safety and forbid adapter/raw-action bypasses.
- [ ] Prompt evaluation includes success, overlap, stale state, injection, unauthorized runtime, missing Surveyor producer, shared-core change and closeout cases with no safety regression.
- [ ] Full changed-file review shows only declared documentation/evidence/task paths.
- [ ] Exact-head repository checks for this documentation-only publication pass.
- [ ] Fresh proportionate prompt audit finds no material contradiction or authority expansion.
- [ ] PR merges, task is archived, and ownership is released.

## Validation / E2E

Runtime E2E is `NOT_APPLICABLE`: this task publishes documentation/prompting only and performs no Control Center service, network listener, official-client runtime access, credentials, login, GUI input, gameplay or process mutation. Outcome verification is exact file content/path review, manual prompt eval matrix, full diff review, exact-head CI, PR terminal state and archived task lifecycle.

## Next action

Create the three worker prompts, aliases and manual eval matrix; open/update the draft PR; validate exact contents and CI; then terminally close the publication task.
