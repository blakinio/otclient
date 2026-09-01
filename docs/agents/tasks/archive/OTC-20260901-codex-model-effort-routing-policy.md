---
task_id: OTC-20260901-codex-model-effort-routing-policy
status: completed
agent: ChatGPT
session_id: chatgpt-codex-routing-policy-20260901
session_role: closeout
project_lane: otclient
lane: AGENT-ORCHESTRATION
track_id: repository-governance
task_kind: documentation
phase: close
source_branch: docs/OTC-20260901-codex-model-effort-routing-policy
archive_branch: docs/OTC-20260901-codex-model-effort-routing-policy-closeout
base_branch: main
base_sha: ca1a71b5852f6e00ba144ed183af470555c51f56
created: 2026-09-01T17:49:12+02:00
updated: 2026-09-01T18:04:03+02:00
risk: low
related_pr: "831"
implementation_pr: 831
implementation_final_head: 4d270faf28be907eee4ffee68f848b6451a2d009
implementation_merge: 11bb95ebf34ce4fb7d46529393862d493250a202
merged_at: 2026-09-01T16:02:51Z
ownership_released: true
final_ci:
  head: 4d270faf28be907eee4ffee68f848b6451a2d009
  ci_run: 33528955322
  result: PASS
track_a_governance:
  run: 33528955128
  result: PASS
audit:
  result: PASS
  validator: Codex gpt-5.6-luna medium, session 01a05db2-fbb4-79f2-84f4-de27a5d03863
  material_findings_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: documentation-only governance policy; no executable, UI, runtime, network, or product behavior changed
pull_requests:
  implementation: 831
  unresolved_review_threads: 0
owned_paths: []
modules_touched: []
depends_on: []
blocks: []
cross_repository_task_ids: []
policy_version: 2
execution_mode: remote_desktop_plus_github
execution_reason: owner-approved narrow documentation-only persistence of Codex model and reasoning-effort routing policy
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: low
context_growth: stable
decomposition_decision: single
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
track_a_runtime_agent_admission_version: 1
execution_class: local_owner_pc
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
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
gui_input_authorized: false
process_control_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
owner_funded_ai_api_authorized: false
invocation_started_at: 2026-09-01T17:49:12+02:00
last_progress_at: 2026-09-01T18:04:03+02:00
current_blocker: none
next_action: no follow-up is required after this lifecycle-only closeout PR merges
---

# Codex model and reasoning-effort routing policy

## Objective

Persist the owner's routing rule for Codex workers using Luna, Terra and Sol so future coordinators select the smallest sufficient model and reasoning effort instead of defaulting expensive work to Sol/xhigh.

## Acceptance

- Luna is the low-cost route for narrow, low-risk work.
- Terra is the default implementation/debugging worker.
- Sol is available at lower efforts as well as `xhigh`; `xhigh` is the maximum, not the default.
- Selection minimizes token consumption while preserving correctness and risk controls.
- A task that remains unsafe or unresolved after justified Sol/xhigh escalation returns to the supervising Chat/owner instead of retrying beyond that ceiling.
- The routing choice and reason are durable when the executor/task schema supports them.

No product code, runtime observation, credentials, login, GUI input, gameplay action, protected-resource mutation or owner-funded API invocation is part of this documentation task.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T18:04:03+02:00
head: 11bb95ebf34ce4fb7d46529393862d493250a202
branch: docs/OTC-20260901-codex-model-effort-routing-policy-closeout
pr: NOT_ASSIGNED
status: completed
context_routes:
  - agent-governance
  - codex-model-routing
owned_paths: []
proven:
  - PR #831 merged exact head 4d270faf28be907eee4ffee68f848b6451a2d009 as squash 11bb95ebf34ce4fb7d46529393862d493250a202.
  - Exact implementation head passed CI run 33528955322 and Track A governance run 33528955128.
  - Independent Codex gpt-5.6-luna medium review returned REVIEW_PASS with no findings on EXECUTION_PROTOCOL.md lines 286-300.
  - The merged policy makes Sol/xhigh a maximum exceptional effort rather than a default and escalates unresolved Sol/xhigh work to the supervising Chat/owner.
derived:
  - Future workers consume the merged model-family rule through the mandatory EXECUTION_PROTOCOL.md startup path.
unknown: []
conflicts: []
first_failure:
  marker: resolved
  evidence: The initial missing Context checkpoint was repaired before implementation merge; no material closeout failure remains.
rejected_hypotheses:
  - Sol should always run at xhigh; the owner clarified that Sol may use lower efforts and xhigh is only the ceiling.
changed_paths:
  - docs/agents/tasks/archive/OTC-20260901-codex-model-effort-routing-policy.md
validation:
  - command: python tools/agents/checkpoint.py docs/agents/tasks/archive/OTC-20260901-codex-model-effort-routing-policy.md --require-checkpoint
    result: PASS
    evidence: Fresh closeout checkpoint validation passed after archival edits.
  - command: git diff --check
    result: PASS
    evidence: Fresh lifecycle-only closeout diff has no whitespace errors.
  - command: git show origin/main:docs/agents/EXECUTION_PROTOCOL.md
    result: PASS
    evidence: Fresh readback confirms the Codex model family and reasoning-effort routing section is merged on main.
  - command: python tools/agents/control_room.py --format markdown
    result: PASS
    evidence: Fresh closeout Control Room exited 0 with this task removed from active work; metrics showed active_tasks=11 and active_sessions=0.
blockers: []
next_action: no follow-up is required after this lifecycle-only closeout PR merges
```
