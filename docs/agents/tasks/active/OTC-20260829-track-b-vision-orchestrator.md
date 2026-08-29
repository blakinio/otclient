---
task_id: OTC-20260829-track-b-vision-orchestrator
status: validating
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: otclient
track_id: otclient-global-login
task_kind: documentation
phase: validate
branch: docs/OTC-20260829-track-b-vision-orchestrator
base_branch: main
related_pr: 792
created: 2026-08-29T14:46:00+02:00
updated: 2026-08-29T14:53:00+02:00
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
updated_at: 2026-08-29T14:53:00+02:00
head: fba47ea32fc21cc2f1eca38bf50b87dcd8977c74
branch: docs/OTC-20260829-track-b-vision-orchestrator
pr: 792
status: validating
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
  - hosted RED run 33253537309 job 99103214915 failed exactly because the canonical single-window prompt was absent
  - the new prompt requires same-invocation local Qwen post-processing only for accepted secret-safe keyframes and otherwise explicit skip/block statuses without retrying E2E
  - the short-command registry now maps OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE to the canonical coordinator prompt
derived:
  - the safest integration point is the owner-facing coordinator prompt on main, not a Track B runtime/workflow mutation
unknown:
  - whether the next independently legal Track B E2E will yield accepted secret-safe keyframes
conflicts: []
first_failure:
  marker: RED_PROMPT_ALIAS_MISSING
  evidence: run 33253537309 job 99103214915; AssertionError missing canonical prompt docs/agents/prompts/OTCLIENT_TIBIA_GLOBAL_LOGIN_FINAL_CONTINUE.md
rejected_hypotheses:
  - Track B should start a second chat/window for Vision
  - Vision should trigger or justify an otherwise forbidden E2E
  - local Vision host downtime should force or authorize a Track B retry
changed_paths:
  - docs/agents/prompts/OTCLIENT_TIBIA_GLOBAL_LOGIN_FINAL_CONTINUE.md
  - docs/agents/SHORT_COMMANDS.md
  - .github/scripts/test_track_b_vision_orchestrator_prompt.py
  - .github/workflows/track-b-vision-orchestrator-contract.yml
  - docs/agents/tasks/active/OTC-20260829-track-b-vision-orchestrator.md
validation:
  - command: python3 .github/scripts/test_track_b_vision_orchestrator_prompt.py
    result: FAIL
    evidence: TDD RED run 33253537309 job 99103214915 failed exactly on the missing canonical prompt before implementation
blockers: []
next_action: consume exact-head GREEN contract, CI and governance for PR 792; repair only concrete failures, then merge/archive if all repository gates pass
```
