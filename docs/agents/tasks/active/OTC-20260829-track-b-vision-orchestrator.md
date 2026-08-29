---
task_id: OTC-20260829-track-b-vision-orchestrator
status: implementing
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: otclient
track_id: otclient-global-login
task_kind: documentation
phase: implement
branch: docs/OTC-20260829-track-b-vision-orchestrator
base_branch: main
related_pr: pending
created: 2026-08-29T14:46:00+02:00
updated: 2026-08-29T14:46:00+02:00
risk: low
execution_mode: github_hosted
run_scope: bounded_change
policy_version: 2
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
gui_input_authorized: false
process_control_authorized: false
gameplay_allowed: false
owned_paths:
  - docs/agents/prompts/OTCLIENT_TIBIA_GLOBAL_LOGIN_FINAL_CONTINUE.md
  - docs/agents/SHORT_COMMANDS.md
  - .github/scripts/test_track_b_vision_orchestrator_prompt.py
  - .github/workflows/track-b-vision-orchestrator-contract.yml
  - docs/agents/tasks/active/OTC-20260829-track-b-vision-orchestrator.md
---

# Goal

Make `OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE` a single-window Track B coordinator: continue structural Global Login work and automatically consume the merged local Vision harness in the same invocation when a future independently legal Track B E2E yields accepted secret-safe keyframes.

This task does not modify PR #284, does not trigger an E2E, and grants no additional credential/runtime authority.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-29T14:46:00+02:00
head: 8d7f0e9fdb46a4fe9ac5641a78ed1b1ee9bc29cc
branch: docs/OTC-20260829-track-b-vision-orchestrator
pr: pending
status: implementing
context_routes:
  - track-b-coordination
  - local-vision-postprocessing
owned_paths:
  - docs/agents/prompts/OTCLIENT_TIBIA_GLOBAL_LOGIN_FINAL_CONTINUE.md
  - docs/agents/SHORT_COMMANDS.md
  - .github/scripts/test_track_b_vision_orchestrator_prompt.py
  - .github/workflows/track-b-vision-orchestrator-contract.yml
  - docs/agents/tasks/active/OTC-20260829-track-b-vision-orchestrator.md
proven:
  - PR 284 remains the canonical active Track B lane
  - merged Vision benchmark provides a bounded local Qwen leading profile but cannot authorize protocol mutation
  - current Track B blocker is BLOCKED_REQUIRED_CURRENT_NATIVE_PRE_LOGIN_OUTBOUND_SEQUENCE_EVIDENCE
  - no additional official-service E2E is authorized merely for screenshots
derived:
  - the safest integration point is the owner-facing coordinator prompt on main, not a Track B runtime/workflow mutation
unknown:
  - whether the next independently legal Track B E2E will yield accepted secret-safe keyframes
conflicts: []
first_failure:
  marker: RED_PROMPT_ALIAS_MISSING
  evidence: contract test requires the canonical prompt and registry alias before implementation
rejected_hypotheses:
  - Track B should start a second chat/window for Vision
  - Vision should trigger or justify an otherwise forbidden E2E
changed_paths:
  - .github/scripts/test_track_b_vision_orchestrator_prompt.py
  - .github/workflows/track-b-vision-orchestrator-contract.yml
  - docs/agents/tasks/active/OTC-20260829-track-b-vision-orchestrator.md
validation:
  - command: python3 .github/scripts/test_track_b_vision_orchestrator_prompt.py
    result: NOT_RUN
    evidence: expected RED after PR creation because canonical prompt/alias do not exist yet
blockers: []
next_action: create PR and capture exact RED contract failure, then add the canonical prompt plus short-command alias and require GREEN
```
