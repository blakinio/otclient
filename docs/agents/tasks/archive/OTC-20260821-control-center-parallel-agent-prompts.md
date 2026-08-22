---
task_id: OTC-20260821-control-center-parallel-agent-prompts
status: completed
agent: ChatGPT
project_lane: otclient
lane: CONTROL-CENTER-PARALLEL-PROMPTS
track_id: official-client-re
task_kind: prompting_coordination
phase: closeout
risk: medium
branch: docs/control-center-parallel-agent-prompts-20260821
base_branch: main
created: 2026-08-21T17:45:00+02:00
updated: 2026-08-22T17:56:00+02:00
initial_base_sha: 532b54fa60d11ae10227ab16dc02cd0cadf39b23
related_pr: 650
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
blocks: []
cross_repository_tasks: []
ownership_released: true
prompt_contract:
  version: 1.0.1
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

- [x] Three canonical worker prompts exist for Package B, Package C and Package D preparation.
- [x] Three owner-facing alias prompts resolve to those canonical worker prompts.
- [x] Every worker prompt requires current-main/open-PR/active-task/AGENTS revalidation before claiming work.
- [x] Package B remains `runtime_access:none`, with real Official Tibia mutation impossible and fake mutation only.
- [x] Package C is read-only and consumes an accepted exact Surveyor producer/schema/interface without copying Surveyor internals or promoting evidence.
- [x] Package D preparation is `runtime_access:none` and cannot perform official-client process observation, memory access, GUI/gameplay input or mutation.
- [x] Ownership boundaries are non-overlapping by default and instruct workers to coordinate/serialize shared core changes rather than editing each other's paths.
- [x] Dependency order makes B/C parallel, D-prep parallel-static, and real D runtime gated after dependency/authority revalidation.
- [x] Prompts preserve Control Center Scenario/Execution/Artifact/Policy safety and forbid adapter/raw-action bypasses.
- [x] Prompt evaluation includes success, overlap, stale state, injection, unauthorized runtime, missing Surveyor producer, shared-core change and closeout cases with no intended safety regression.
- [x] Full changed-file review shows only declared documentation/evidence/task paths.
- [x] Exact-head repository checks for this documentation-only publication pass.
- [x] Fresh independent prompt audit finds no material contradiction or authority expansion.
- [x] PR merges, task is archived, and ownership is released.

## Validation evidence

- Current trusted base at task start: `main@532b54fa60d11ae10227ab16dc02cd0cadf39b23`, Package A lifecycle closeout merged in PR #649.
- Publication PR: #650.
- Exact reviewed head before audit remediation: `e958379388429c07ba7bace062e1e8f70b756193`.
- Full PR diff review at that head: 8 changed files, all inside the declared prompt/evidence/task paths; no runtime/source/workflow/module files changed.
- Manual deterministic prompt regression matrix: `docs/agents/evidence/OTC-20260821-control-center-parallel-agent-prompts/prompt-eval.md`; E01-E15 static contract comparison PASS. This is explicitly not an automated model-behaviour evaluation and not an independent audit.
- GitHub checks at `bc45419eb7bc6590f19d4f32add2ded593f39bde`: CI run `32577080151` SUCCESS and Track A agent runtime governance run `32577080122` SUCCESS.
- Final metadata-only independent Codex audit of `bc45419eb7bc6590f19d4f32add2ded593f39bde` returned `Didn't find any major issues`.
- After Draft -> Ready transition, branch protection correctly required a fresh `CI / Required` context; a direct merge attempt was rejected with `Required status check "CI / Required" is expected`. This metadata-only successor exists solely to trigger the required ready-state validation generation without weakening protection.
- Current Surveyor source was inspected for discovery values and the C prompt requires revalidation rather than hard authority reuse.
- Current Track A admission and Control Center adapter contracts were inspected so D-prep remains strictly no-runtime and cannot silently expand into real Package D execution.

## Fresh independent audit findings - 2026-08-22

Codex independent review `PRR_kwDOTVmdjs8AAAABKgpUnQ` audited exact head `06a422162adf5207875ee4c800b372c25d84033a` and opened two material P1 findings:

- `PRRT_kwDOTVmdjs6bZDWd`: D-prep routing used autonomous-program continuation fields that could permit a follow-on real Package D task despite this alias being preparation-only and `runtime_access:none`. Repaired by making both D-prep canonical and alias metadata `single_task` / `stop_at_task_boundary` / `finalize_archive_and_stop`.
- `PRRT_kwDOTVmdjs6bZDWe`: Package C normalization wording could allow a candidate/pending-causal Surveyor player position into normalized `GameSnapshot`. Repaired so normalized position requires explicit accepted causal semantic promotion; candidate/pending-causal values remain provenance/source-quality only and normalized position stays unknown.

Fresh re-audit `PRR_kwDOTVmdjs8AAAABKgp-nw` on repaired head `442c299dc417962a11c20f395a16512b1eacea45` confirmed those two threads as outdated/closed-by-change but opened two analogous P1 routing findings: `PRRT_kwDOTVmdjs6bZFdt` for Package B and `PRRT_kwDOTVmdjs6bZFdu` for Package C. Both canonical+alias metadata were repaired to `single_task` / `stop_at_task_boundary` / `finalize_archive_and_stop`; E01/E02 encode the task-boundary requirement.

Synchronized exact-head audit on `9fc73d490d66678b84c2e3f58ebda17cf9113c7d` found one additional P1: `finalize_archive_and_stop` was not a Prompting Standard 2.1 enum value. All six worker/alias headers now retain `single_task` / `stop_at_task_boundary` but use supported `finalize_archive_and_continue`; the stop-at-boundary contract prevents follow-on task selection while preserving archive semantics.

Third fresh independent Codex review of exact head `b8ff280ec47036df30cca64059fa0eca81d37a21` returned no major/material issues. All four prior P1 threads are resolved and outdated after the corresponding fixes.

Final fresh independent Codex review of metadata-only successor `bc45419eb7bc6590f19d4f32add2ded593f39bde` also returned no major/material issues. This successor changes only task validation evidence and creates the pull-request synchronization event required for a fresh ready-state branch-protection check generation.

## Validation / E2E

Runtime E2E is `NOT_APPLICABLE`: this task publishes documentation/prompting only and performs no Control Center service, network listener, official-client runtime access, credentials, login, GUI input, gameplay or process mutation. Outcome verification is exact file content/path review, manual prompt eval matrix, full diff review, exact-head CI, PR terminal state and archived task lifecycle.

## Next action

NONE — terminal.
## Terminal closeout — 2026-08-22

- Publication PR #650 merged as `9c54c1a4e22db974109298a23be39d9b04305e76`.
- Post-merge repair PR #661 merged as `2239f787ab9c03b80f399d83c21275d92a008148`.
- Final repair head `f103b15cab151d605020381ab1cde1b03c8a82ab`: CI run `32583016941` SUCCESS; Track A governance run `32583016806` SUCCESS; fresh Codex exact-head audit reported no major issues.
- PR #661 final changed-file set: 9 declared prompt/eval/task paths; its only review thread is resolved.
- Runtime E2E: NOT_APPLICABLE because this lifecycle is documentation/prompt publication only and had `runtime_access:none`.
- Ownership is released; the Package B/C/D-prep aliases are unblocked on trusted main at prompt contract `1.0.1`.