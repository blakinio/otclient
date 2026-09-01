---
task_id: OTC-20260901-vision-p2-coordinator
status: validating
agent: ChatGPT
session_role: programme_coordinator
worker_alias: OTC-VISION-P2-COORDINATOR
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: coordination
phase: wave_0_cleanup_validation
branch: docs/OTC-20260901-vision-p2-coordinator
base_branch: main
base_main: 21fedc04809f0f78a1ff673edb2804a83ab5fedb
created: 2026-09-01T15:45:26+02:00
updated_at: 2026-09-01T15:55:30+02:00
risk: high
execution_class: github_coordination
execution_mode: chat_github
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
prompting_standard_version: 2.1
policy_version: 2
runtime_access: none
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
worktree: C:/Users/barte/otclient-vision-p2-coordinator
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
  - docs/agents/tasks/archive/OTC-20260830-local-vision-agent-supervisor-discovery.md
  - docs/agents/tasks/archive/OTC-20260830-local-vision-agent-supervisor-foundation.md
depends_on:
  - PR #820 merged foundation
  - PR #823 merged Phase 2 prompt-package closeout
related_prs:
  - PR #808 closed historical discovery Draft; superseded after #820
  - PR #810 closed historical foundation Draft; superseded after #820
  - PR #820 merged foundation integration
  - PR #824 Wave 0 coordinator cleanup Draft
current_blocker: none
next_action: validate coordinator checkpoint/control-room and PR #824 exact-head checks; merge bounded cleanup only if all required gates pass
invocation_started_at: 2026-09-01T15:35:00+02:00
last_progress_at: 2026-09-01T15:55:30+02:00
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


# OTC Vision Phase 2 read-only programme coordinator

## Objective

Reconcile Phase 2 live state, release stale foundation ownership, create exact non-overlapping Wave 1 task/branch/Draft-PR assignments, independently classify worker outputs, integrate accepted slices, serialize real read-only observation, and drive the programme through fresh exact-head audit/E2E closeout without entering Phase 3+.

## Binding authority

- `docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md`
- `docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md`
- `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`
- live Git/GitHub/runtime state overrides stale historical task prose.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T15:55:30+02:00
head: 55f642f5ee0b4d8d2a9bff982af948ceb44b1871
branch: docs/OTC-20260901-vision-p2-coordinator
pr: 824
status: validating
context_routes:
  - phase-2-read-only-coordination
  - autonomous-program
  - delivery-closeout
  - track-a-governance
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
  - docs/agents/tasks/archive/OTC-20260830-local-vision-agent-supervisor-discovery.md
  - docs/agents/tasks/archive/OTC-20260830-local-vision-agent-supervisor-foundation.md
proven:
  - main base for Wave 0 is 21fedc04809f0f78a1ff673edb2804a83ab5fedb.
  - PR 820 is merged; PRs 808 and 810 are now closed historical Drafts.
  - stale discovery/foundation active task records were moved to archive and top-level owned_paths were released in 55f642f5ee0b4d8d2a9bff982af948ceb44b1871.
  - coordinator Draft PR 824 exists against main.
derived:
  - the original stale ownership conflict is resolved on the coordinator branch but not yet on main until PR 824 merges.
unknown:
  - exact required-check result for PR 824 after the cleanup commit publishes.
conflicts: []
first_failure:
  marker: WAVE0-STALE-FOUNDATION-OWNERSHIP
  evidence: resolved by PR closures 808/810 and archive commit 55f642f5ee0b4d8d2a9bff982af948ceb44b1871; main awaits PR 824 merge.
rejected_hypotheses:
  - direct Codex CLI dispatch is available on Molehill-PC: rejected; codex executable not found.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
  - docs/agents/tasks/archive/OTC-20260830-local-vision-agent-supervisor-discovery.md
  - docs/agents/tasks/archive/OTC-20260830-local-vision-agent-supervisor-foundation.md
validation:
  - command: live GitHub lifecycle readback
    result: PASS
    evidence: PR 820 merged; PRs 808 and 810 closed
  - command: git diff --check
    result: PASS
    evidence: no whitespace errors after archive transformation
  - command: isolated coordinator worktree readback
    result: PASS
    evidence: unique worktree C:/Users/barte/otclient-vision-p2-coordinator on coordinator branch
blockers: []
next_action: validate coordinator checkpoint/control-room and PR #824 exact-head checks; merge bounded cleanup only if all required gates pass.
```
