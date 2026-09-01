---
task_id: OTC-20260901-vision-p2-coordinator-codex-dispatch-prompt
status: ready
agent: ChatGPT
session_role: prompt_maintainer
project_lane: otclient
lane: AGENT-ORCHESTRATION
track_id: repository-governance
task_kind: documentation
phase: exact_head_ready
branch: docs/OTC-20260901-vision-p2-coordinator-codex-dispatch-prompt
base_branch: main
base_sha: d1cb8722c3116a0e0aeb72b9b360712f43151f17
created: 2026-09-01T22:55:00+02:00
updated_at: 2026-09-01T23:11:51+02:00
risk: low
execution_class: local_owner_pc
execution_mode: remote_desktop_plus_github
preferred_execution: chat_github
execution_reason: persist owner-requested coordinator-managed Codex worker dispatch semantics
context_pressure: low
decomposition_decision: single
user_communication: low_noise
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: merge_then_archive
prompting_standard_version: 2.1
policy_version: 2
track_a_runtime_agent_admission_version: 1
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
anti_idle_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
process_memory_access_allowed: false
physical_action_budget: 0
physical_action_count: 0
owner_funded_ai_api_authorized: false
worktree: C:/Users/barte/otclient-vision-p2-coordinator-codex-dispatch-prompt
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator-codex-dispatch-prompt.md
  - docs/agents/reports/OTC-20260901-vision-p2-coordinator-codex-dispatch-prompt.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_ALIASES.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_PROMPT_EVAL_V1.md
modules_touched: []
depends_on:
  - merged Codex model/effort benchmark PR #841
  - merged benchmark closeout PR #842
blocks: []
cross_repository_task_ids: []
related_pr: 844
invocation_started_at: 2026-09-01T22:55:00+02:00
last_progress_at: 2026-09-01T23:11:51+02:00
ci_checks_for_current_head: 2
ci_check_generation: green-9502e4023a6c
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
audit_result: PASS
audit_evidence: deterministic static prompt regression plus exact GitHub diff/readback; no material prompt-authority or safety regression found
e2e_result: NOT_APPLICABLE
e2e_reason: prompt/documentation-only coordinator routing change; no executable, UI, runtime, network or product behavior changed
current_blocker: none
next_action: publish this readiness checkpoint, require final task-only exact-head CI/governance and unchanged PR hygiene/main freshness, then mark Ready and squash-merge PR #844
---

# Vision P2 coordinator-managed Codex dispatch prompt

## Objective

Make a newly started `OTC-VISION-P2-COORDINATOR` understand that it is the supervising coordinator and should itself select, dispatch, supervise and verify subordinate Codex workers for ordinary execution/audit work when execution tooling is available; the owner should not need to manually select Luna/Terra/Sol or open worker windows.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T23:11:51+02:00
head: 9502e4023a6c011fe9d539349ca409b588c609a4
head_semantics: last_verified_full_prompt_head_before_readiness_checkpoint
branch: docs/OTC-20260901-vision-p2-coordinator-codex-dispatch-prompt
pr: 844
status: ready
context_routes:
  - agent-governance
  - prompting-v2.1
  - vision-p2-coordination
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator-codex-dispatch-prompt.md
  - docs/agents/reports/OTC-20260901-vision-p2-coordinator-codex-dispatch-prompt.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_ALIASES.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_PROMPT_EVAL_V1.md
proven:
  - current alias registry tells the owner to open separate worker windows after coordinator dispatch.
  - current coordinator mode text says Codex is used only for integration edits, which conflicts with the owner-approved supervising-coordinator workflow and empirical routing policy.
  - EXECUTION_PROTOCOL.md now contains empirical model/effort calibration from PR #841.
  - prompt contract 1.1.0 static regression passed with exactly eight aliases and manual worker windows fallback-only.
  - exact prompt head 9502e4023a6c011fe9d539349ca409b588c609a4 passed CI run 33559601723 and Track A governance run 33559601426; PR #844 had zero review threads/reviews and was behind=0 from main.
derived:
  - coordinator prompt surfaces must explicitly distinguish supervising Chat coordinator from subordinate Codex workers and make manual worker windows a fallback only.
unknown: []
conflicts: []
first_failure:
  marker: resolved
  evidence: prompt contract 1.1.0 now makes coordinator-managed Codex dispatch explicit and manual worker windows fallback-only.
rejected_hypotheses:
  - owner should manually choose a Codex model/effort for each ordinary worker task.
  - a Codex worker DONE/green narrative is sufficient coordinator evidence.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator-codex-dispatch-prompt.md
  - docs/agents/reports/OTC-20260901-vision-p2-coordinator-codex-dispatch-prompt.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_ALIASES.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_PROMPT_EVAL_V1.md
validation:
  - command: python verify_coord_prompt_v11.py
    result: PASS
    evidence: prompt contract 1.1.0, exactly 8 aliases, coordinator-managed Codex dispatch present, manual worker windows fallback-only.
  - command: git diff --check
    result: PASS
    evidence: no whitespace errors in candidate prompt delta.
  - command: Track A agent runtime governance changed-from d1cb8722c3116a0e0aeb72b9b360712f43151f17
    result: PASS
    evidence: TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true.
  - command: python tools/agents/control_room.py --format markdown
    result: PASS
    evidence: task recognized as policy-v2 documentation task; active_sessions=0.
blockers: []
next_action: publish this readiness checkpoint, require final task-only exact-head CI/governance and unchanged PR hygiene/main freshness, then mark Ready and squash-merge PR #844
```
