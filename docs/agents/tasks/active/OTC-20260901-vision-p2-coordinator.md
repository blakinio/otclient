---
task_id: OTC-20260901-vision-p2-coordinator
status: implementing
agent: ChatGPT
session_role: programme_coordinator
worker_alias: OTC-VISION-P2-COORDINATOR
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: coordination
phase: wave_1_bootstrap
branch: docs/OTC-20260901-vision-p2-coordinator-wave1
base_branch: main
base_main: 0fe1ecb3569f1d8372209c857ab57f3b626c29ae
created: 2026-09-01T15:45:26+02:00
updated_at: 2026-09-01T16:24:14+02:00
risk: high
execution_mode: chat_github
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
prompting_standard_version: 2.1
policy_version: 2
runtime_access: none
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
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
depends_on:
  - PR #820 merged foundation
  - PR #823 merged Phase 2 prompt-package closeout
related_prs:
  - PR #820 merged foundation integration
  - PR #823 merged Phase 2 prompt-package closeout
  - PR #824 merged Wave 0 coordinator cleanup
current_blocker: none
next_action: create five concrete overlap-free Wave 1 worker task records, branches, worktrees and Draft PRs from refreshed main
invocation_started_at: 2026-09-01T15:35:00+02:00
last_progress_at: 2026-09-01T16:24:14+02:00
ci_checks_for_current_head: 0
ci_check_generation: wave1-bootstrap
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
updated_at: 2026-09-01T16:24:14+02:00
head: 0fe1ecb3569f1d8372209c857ab57f3b626c29ae
branch: docs/OTC-20260901-vision-p2-coordinator-wave1
pr: none
status: implementing
context_routes:
  - phase-2-read-only-coordination
  - autonomous-program
  - delivery-closeout
  - track-a-governance
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
proven:
  - PR 824 merged at 2026-09-01T14:23:07Z as 0fe1ecb3569f1d8372209c857ab57f3b626c29ae after exact-head CI and Track A governance passed on 436160306c3b74f2c6d7dbae578aee5a76381d09.
  - refreshed main is 0fe1ecb3569f1d8372209c857ab57f3b626c29ae.
  - refreshed active-task scan shows this coordinator as the only OTC-VISION-P2-READONLY active task.
  - refreshed ownership scan shows no active writer claim on tools/tibia_re_control_center/**, tests/tools/tibia_re_control_center/**, tools/tibia_re_vision/** or tests/tools/tibia_re_vision/**.
  - current trusted exact-client fence remains 15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a.
  - runtime_access remains none and all mutation, credential, login, GUI, process-control, process-memory and payload-capture authorities remain false with physical action budget/count 0/0.
derived:
  - five Wave 1 repository/static workers may be bootstrapped in parallel on disjoint paths from this exact main.
unknown:
  - concrete worker PR numbers and branch heads until bootstrap commits publish.
conflicts: []
first_failure:
  marker: none
  evidence: no current failure; Wave 1 bootstrap is pending.
rejected_hypotheses:
  - stale foundation ownership still blocks Wave 1: rejected by merged PR 824 plus refreshed-main active ownership scan.
  - direct Codex CLI dispatch is available on Molehill-PC: rejected; codex executable is not installed.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
validation:
  - command: gh pr view 824 plus exact-head statusCheckRollup
    result: PASS
    evidence: PR 824 merged; exact head 436160306c3b74f2c6d7dbae578aee5a76381d09 had CI and Track A governance SUCCESS.
  - command: git fetch origin --prune and rev-parse origin/main
    result: PASS
    evidence: refreshed main 0fe1ecb3569f1d8372209c857ab57f3b626c29ae.
  - command: active Phase 2 and control/vision ownership grep on refreshed main
    result: PASS
    evidence: only coordinator active; no active code-path ownership claim found.
blockers: []
next_action: create five concrete overlap-free Wave 1 worker task records, branches, worktrees and Draft PRs from refreshed main.
```
## Planned Wave 1 ownership

This map is coordinator-owned dispatch intent and becomes write-capable only after PR #824 merges, refreshed-main overlap checks pass, and each worker has its own concrete task/branch/worktree/Draft PR. Shared indexes such as `docs/agents/MODULE_CATALOG.md` are excluded.

- `OTC-VISION-P2-RUNTIME-ADMISSION`: new `agent_runtime_admission.py`, its focused test, lane report/task.
- `OTC-VISION-P2-CAPTURE-EDGE`: new `tools/tibia_re_vision/capture_edge.py`, its focused test, lane report/task.
- `OTC-VISION-P2-RUNTIME-SIGNALS`: new `agent_runtime_signals.py`, its focused test, lane report/task.
- `OTC-VISION-P2-EDGE-TRANSPORT`: new `agent_edge_transport.py`, its focused test, lane report/task.
- `OTC-VISION-P2-CONTROL-BRIDGE`: exclusive integration ownership for a new edge bridge plus the existing session/domain/API/CLI/UI/MCP files and their focused tests; no other Wave 1 worker may edit those shared integration files.

Repository/static execution defaults to `github_hosted` with `runtime_access: none`. Actual official-runtime observation is separately admitted, read-only, mutation-disabled and serialized to one observation owner.

## Wave 0 audit findings

- `W0-AUDIT-001` — **material medium**, mandatory Track A admission fields absent from the coordinator task. Evidence: exact-head governance run `33517851944`, job `99889308745`, plus matching local RED. Impact: PR cannot satisfy Track A governance. Disposition: fixed with the canonical `runtime_access:none` admission record; local GREEN confirmed. Final verification: pending fresh exact-head CI.
- `W0-AUDIT-002` — **material medium**, UTF-8 mojibake in the archived foundation task caused by an intermediate Windows text round-trip. Evidence: PR diff exposed changed Unicode punctuation. Impact: historical archive integrity and readability. Disposition: rebuilt both archive files from exact `main` UTF-8 bytes plus only intended lifecycle edits; `MOJIBAKE_MATCHES=[]`, both archive checkpoint validators PASS. Final verification: pending fresh exact-head CI/diff.
- `W0-AUDIT-003` — **material medium**, duplicate `execution_class` keys in the coordinator frontmatter after admission remediation. Evidence: direct fresh task read showed both `github_coordination` and `github_hosted`. Impact: ambiguous machine-readable contract. Disposition: removed the duplicate and retained the routing-contract value `github_hosted`. Final verification: pending fresh exact-head CI/checkpoint validation.
