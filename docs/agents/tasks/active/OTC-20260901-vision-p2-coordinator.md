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
phase: wave_0_final_validation
branch: docs/OTC-20260901-vision-p2-coordinator
base_branch: main
base_main: 21fedc04809f0f78a1ff673edb2804a83ab5fedb
created: 2026-09-01T15:45:26+02:00
updated_at: 2026-09-01T16:08:42+02:00
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
next_action: publish the final Wave 0 checkpoint, refresh PR #824, run exact-head governance/CI plus proportional fresh docs audit, and merge only if every gate passes
invocation_started_at: 2026-09-01T15:35:00+02:00
last_progress_at: 2026-09-01T16:08:42+02:00
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
updated_at: 2026-09-01T16:08:42+02:00
head: 5f7d8dc2b5c37b857c77eac153e04c85c44119b4
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
  - PR 820 is merged; historical Draft PRs 808 and 810 are closed and their stale active task records are archived with ownership released.
  - coordinator Draft PR 824 is limited to three task-lifecycle files and changes no product/runtime code.
  - active coordinator checkpoint and both terminal archive checkpoints pass tools/agents/checkpoint.py --require-checkpoint.
  - tools/agents/resume.py reconstructs the coordinator task and tools/agents/control_room.py lists it as the live PR 824 coordinator.
  - mandatory current Track A research, runtime-admission, Kasm, canonical-runtime, bootstrap, canonical prompt and hybrid-routing contracts were refreshed before Wave 1 planning.
  - trusted current exact-client fence is 15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a.
  - the older parallel-research document fence 52109920 / ed5469... is superseded by the 2026-08-28 canonical advance recorded in CHANGELOG and PR 754; Phase 2 explicitly binds stricter current trusted-base governance.
  - no active task currently claims tools/tibia_re_control_center/** or tools/tibia_re_vision/** after the Wave 0 archive cleanup; shared MODULE_CATALOG.md remains outside this PR and worker ownership.
derived:
  - Wave 1 can use disjoint lane-local modules after PR 824 merges, while any shared Control Center integration files remain exclusive to CONTROL-BRIDGE.
unknown:
  - final exact-head required CI and independent/proportional docs-audit result after this checkpoint is published.
conflicts: []
first_failure:
  marker: FINAL-EXACT-HEAD-GATES-PENDING
  evidence: final checkpoint commit has not yet emitted its exact-head required checks.
rejected_hypotheses:
  - direct Codex CLI dispatch is available on Molehill-PC: codex executable is not installed on the connected host.
  - the older 52109920 / ed5469... fence is current Phase 2 identity authority: superseded by current mandatory contracts and PR 754/CHANGELOG evidence.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
  - docs/agents/tasks/archive/OTC-20260830-local-vision-agent-supervisor-discovery.md
  - docs/agents/tasks/archive/OTC-20260830-local-vision-agent-supervisor-foundation.md
validation:
  - command: python tools/agents/checkpoint.py docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md --require-checkpoint
    result: PASS
    evidence: active coordinator checkpoint validated.
  - command: terminal archive checkpoint validation
    result: PASS
    evidence: both archived discovery/foundation task checkpoints validated.
  - command: python tools/agents/resume.py --task docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
    result: PASS
    evidence: durable branch/PR/next-action recovery succeeded.
  - command: python tools/agents/control_room.py --format markdown
    result: PASS
    evidence: OTC-20260901-vision-p2-coordinator listed RUNNING on PR 824 with no Phase 2 worker duplication.
  - command: git diff --check
    result: PASS
    evidence: no whitespace errors in Wave 0 lifecycle delta.
blockers: []
next_action: publish the final Wave 0 checkpoint, refresh PR #824, run exact-head governance/CI plus proportional fresh docs audit, and merge only if every gate passes.
```

## Planned Wave 1 ownership

This map is coordinator-owned dispatch intent and becomes write-capable only after PR #824 merges, refreshed-main overlap checks pass, and each worker has its own concrete task/branch/worktree/Draft PR. Shared indexes such as `docs/agents/MODULE_CATALOG.md` are excluded.

- `OTC-VISION-P2-RUNTIME-ADMISSION`: new `agent_runtime_admission.py`, its focused test, lane report/task.
- `OTC-VISION-P2-CAPTURE-EDGE`: new `tools/tibia_re_vision/capture_edge.py`, its focused test, lane report/task.
- `OTC-VISION-P2-RUNTIME-SIGNALS`: new `agent_runtime_signals.py`, its focused test, lane report/task.
- `OTC-VISION-P2-EDGE-TRANSPORT`: new `agent_edge_transport.py`, its focused test, lane report/task.
- `OTC-VISION-P2-CONTROL-BRIDGE`: exclusive integration ownership for a new edge bridge plus the existing session/domain/API/CLI/UI/MCP files and their focused tests; no other Wave 1 worker may edit those shared integration files.

Repository/static execution defaults to `github_hosted` with `runtime_access: none`. Actual official-runtime observation is separately admitted, read-only, mutation-disabled and serialized to one observation owner.
