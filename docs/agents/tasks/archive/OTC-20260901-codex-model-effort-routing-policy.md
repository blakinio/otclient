---
task_id: OTC-20260901-codex-model-effort-routing-policy
status: validating
agent: ChatGPT
session_id: chatgpt-codex-routing-policy-20260901
session_role: implementer
project_lane: otclient
lane: AGENT-ORCHESTRATION
track_id: repository-governance
task_kind: documentation
phase: validate
branch: docs/OTC-20260901-codex-model-effort-routing-policy
base_branch: main
base_sha: ca1a71b5852f6e00ba144ed183af470555c51f56
created: 2026-09-01T17:49:12+02:00
updated: 2026-09-01T17:56:35+02:00
risk: low
related_pr: "831"
owned_paths:
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/tasks/active/OTC-20260901-codex-model-effort-routing-policy.md
modules_touched:
  - agent-governance
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
last_progress_at: 2026-09-01T17:56:35+02:00
current_blocker: none
next_action: run independent review and exact-head required checks for PR #831; if clean, mark it ready and merge under repository protection
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
updated_at: 2026-09-01T17:56:35+02:00
head: ca1a71b5852f6e00ba144ed183af470555c51f56
branch: docs/OTC-20260901-codex-model-effort-routing-policy
pr: 831
status: validating
context_routes:
  - agent-governance
  - codex-model-routing
owned_paths:
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/tasks/active/OTC-20260901-codex-model-effort-routing-policy.md
proven:
  - The owner approved persisting a cost-aware Luna/Terra/Sol routing policy.
  - Sol may use lower efforts; xhigh is its maximum permitted effort and is not the default.
  - EXECUTION_PROTOCOL.md is mandatory task governance and already contains the Codex execution-mode decision section.
derived:
  - The model-family rule belongs beside the existing Codex execution-mode policy so future workers consume it automatically.
unknown: []
conflicts: []
first_failure:
  marker: CHECKPOINT_REQUIRED
  evidence: Initial checkpoint validator rejected the new task because the mandatory Context checkpoint section was absent.
rejected_hypotheses:
  - Sol should always run at xhigh; the owner clarified that Sol may use lower efforts and xhigh is only the ceiling.
changed_paths:
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/tasks/active/OTC-20260901-codex-model-effort-routing-policy.md
validation:
  - command: python tools/agents/checkpoint.py docs/agents/tasks/active/OTC-20260901-codex-model-effort-routing-policy.md --require-checkpoint
    result: PASS
    evidence: Fresh targeted checkpoint validation passed after adding the mandatory Context checkpoint.
  - command: git diff --check
    result: PASS
    evidence: Fresh working-tree diff check passed after the checkpoint repair with no whitespace errors.
  - command: python tools/agents/control_room.py --format markdown
    result: PASS
    evidence: Fresh repository-root Control Room run exited 0; unrelated pre-existing stale tasks remain visible but this docs task introduces no ownership conflict.
blockers: []
next_action: run independent review and exact-head required checks for PR #831; if clean, mark it ready and merge under repository protection
```
