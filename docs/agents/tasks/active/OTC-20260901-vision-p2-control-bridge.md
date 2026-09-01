---
task_id: OTC-20260901-vision-p2-control-bridge
status: implementing
agent: chatgpt-gpt-5.6-sol
session_role: phase2_worker
worker_alias: OTC-VISION-P2-CONTROL-BRIDGE
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: implementation
phase: implement
branch: feat/OTC-20260901-vision-p2-control-bridge
base_branch: main
base_main: ca1a71b5852f6e00ba144ed183af470555c51f56
created: 2026-09-01T16:27:39+02:00
updated_at: 2026-09-01T17:01:25+02:00
risk: high
execution_class: github_hosted
execution_mode: isolated_worker_branch
preferred_execution: codex
run_scope: wave_1_worker
continuation_policy: continue_until_real_stop
task_completion_policy: return_to_coordinator_for_classification
prompting_standard_version: 2.1
policy_version: 2
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
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
worktree: C:/Users/barte/otclient-vision-p2-control-bridge
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-control-bridge.md
  - docs/agents/reports/OTC-20260901-vision-p2-control-bridge.md
  - tools/tibia_re_control_center/agent_edge_bridge.py
  - tools/tibia_re_control_center/agent_session.py
  - tools/tibia_re_control_center/control_domain.py
  - tools/tibia_re_control_center/control_api.py
  - tools/tibia_re_control_center/control_ui.py
  - tools/tibia_re_control_center/agent_mcp.py
  - tools/tibia_re_control_center/persistent_store.py
  - tests/tools/tibia_re_control_center/test_agent_edge_bridge.py
  - tests/tools/tibia_re_control_center/test_agent_session.py
  - tests/tools/tibia_re_control_center/test_agent_api.py
  - tests/tools/tibia_re_control_center/test_agent_mcp.py
  - tests/tools/tibia_re_control_center/test_agent_persistence.py
depends_on:
  - PR #820 merged foundation
  - PR #824 merged Wave 0 coordinator cleanup
  - main ca1a71b5852f6e00ba144ed183af470555c51f56
related_prs:
  - PR #830 Wave 1 worker Draft
current_blocker: none
next_action: run focused baseline Control Center agent tests on rebased main, then write the first RED edge-bridge test with runtime_access none
invocation_started_at: 2026-09-01T16:49:00+02:00
last_progress_at: 2026-09-01T17:01:25+02:00
ci_checks_for_current_head: 0
ci_check_generation: pr-bound-bootstrap
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
---

# OTC-VISION-P2-CONTROL-BRIDGE

## Mission

Integrate edge heartbeat/capture/runtime state into the existing Control Center/session backend with fail-closed stale/disconnect behavior while preserving STOP/PAUSE/restart and keeping the production executor Null/unbound.

## Dispatch boundary

This task is bootstrapped by `OTC-VISION-P2-COORDINATOR`. The worker may mutate repository files only after its own isolated session validates the exact task, branch, worktree and Draft PR and confirms the ownership set below remains non-overlapping. Real Official Tibia runtime observation is **not authorized** by this record. Any later transition from `runtime_access: none` to `read_only` requires a coordinator-assigned single observation window, fresh exact-target proof, and a persisted valid read-only admission record before observation.

## Binding reads

- `docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md`
- `docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md`
- `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`
- `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`
- `docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md`
- `docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md`

## Owned paths

- `docs/agents/tasks/active/OTC-20260901-vision-p2-control-bridge.md`
- `docs/agents/reports/OTC-20260901-vision-p2-control-bridge.md`
- `tools/tibia_re_control_center/agent_edge_bridge.py`
- `tools/tibia_re_control_center/agent_session.py`
- `tools/tibia_re_control_center/control_domain.py`
- `tools/tibia_re_control_center/control_api.py`
- `tools/tibia_re_control_center/control_ui.py`
- `tools/tibia_re_control_center/agent_mcp.py`
- `tools/tibia_re_control_center/persistent_store.py`
- `tests/tools/tibia_re_control_center/test_agent_edge_bridge.py`
- `tests/tools/tibia_re_control_center/test_agent_session.py`
- `tests/tools/tibia_re_control_center/test_agent_api.py`
- `tests/tools/tibia_re_control_center/test_agent_mcp.py`
- `tests/tools/tibia_re_control_center/test_agent_persistence.py`

Shared indexes/governance files, including `docs/agents/MODULE_CATALOG.md`, are not owned. Any required path outside this set is a coordinator ownership-extension request, not an implicit permission.

## Implementation discipline

Use RED-to-GREEN TDD for each behavior. Preserve the approved architecture and reuse the existing Control Center/session plane rather than creating a second control plane/store. Fake/hosted evidence can validate repository behavior but can never be reported as real-runtime success. The worker must open no additional implementation PR and must not merge/promote its own result; the coordinator classifies the Draft PR.

## Dispatch contract

```yaml
programme_id: OTC-VISION-P2-READONLY
worker_alias: OTC-VISION-P2-CONTROL-BRIDGE
TASK_ID: OTC-20260901-vision-p2-control-bridge
TASK_RECORD: docs/agents/tasks/active/OTC-20260901-vision-p2-control-bridge.md
PROJECT_LANE: otclient
BASE_MAIN: ca1a71b5852f6e00ba144ed183af470555c51f56
BRANCH: feat/OTC-20260901-vision-p2-control-bridge
WORKTREE: C:/Users/barte/otclient-vision-p2-control-bridge
OWNED_PATHS:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-control-bridge.md
  - docs/agents/reports/OTC-20260901-vision-p2-control-bridge.md
  - tools/tibia_re_control_center/agent_edge_bridge.py
  - tools/tibia_re_control_center/agent_session.py
  - tools/tibia_re_control_center/control_domain.py
  - tools/tibia_re_control_center/control_api.py
  - tools/tibia_re_control_center/control_ui.py
  - tools/tibia_re_control_center/agent_mcp.py
  - tools/tibia_re_control_center/persistent_store.py
  - tests/tools/tibia_re_control_center/test_agent_edge_bridge.py
  - tests/tools/tibia_re_control_center/test_agent_session.py
  - tests/tools/tibia_re_control_center/test_agent_api.py
  - tests/tools/tibia_re_control_center/test_agent_mcp.py
  - tests/tools/tibia_re_control_center/test_agent_persistence.py
DEPENDENCIES:
  - PR #820 merged
  - PR #824 merged
runtime_access: none
```

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T16:52:55+02:00
head: 12a92e636a291aab701248d902ca8a9a14857577
branch: feat/OTC-20260901-vision-p2-control-bridge
pr: 830
status: implementing
context_routes:
  - phase-2-read-only-coordination
  - track-a-governance
  - control-bridge
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-control-bridge.md
  - docs/agents/reports/OTC-20260901-vision-p2-control-bridge.md
  - tools/tibia_re_control_center/agent_edge_bridge.py
  - tools/tibia_re_control_center/agent_session.py
  - tools/tibia_re_control_center/control_domain.py
  - tools/tibia_re_control_center/control_api.py
  - tools/tibia_re_control_center/control_ui.py
  - tools/tibia_re_control_center/agent_mcp.py
  - tools/tibia_re_control_center/persistent_store.py
  - tests/tools/tibia_re_control_center/test_agent_edge_bridge.py
  - tests/tools/tibia_re_control_center/test_agent_session.py
  - tests/tools/tibia_re_control_center/test_agent_api.py
  - tests/tools/tibia_re_control_center/test_agent_mcp.py
  - tests/tools/tibia_re_control_center/test_agent_persistence.py
proven:
  - live Draft PR 830 still targets main from this exact worker branch; pre-rebase remote head was 7d5ccdb80aa523c3128bef0b8e4faef4450146fe.
  - isolated worktree C:/Users/barte/otclient-vision-p2-control-bridge is on the unique worker branch and was clean before claim.
  - current main is ca1a71b5852f6e00ba144ed183af470555c51f56; its only drift from the dispatch base is coordinator task state from merged PR 825.
  - active-task ownership scan found no other owner of this worker's Control Center implementation/test paths.
  - runtime_access is none; all mutation/runtime-effect authorities remain false and physical action budget/count are 0/0.
derived:
  - repository/static RED-to-GREEN implementation may proceed; official-client observation remains forbidden in this invocation.
unknown:
  - implementation GREEN behavior and exact-head CI outcome.
  - exact-head CI and coordinator classification.
conflicts: []
first_failure:
  marker: RUNTIME_ACCESS_UNAVAILABLE
  evidence: first focused RED test fails at the existing repository-foundation runtime_access guard before any edge observation can be accepted.
rejected_hypotheses:
  - real runtime access is needed for this implementation slice: rejected; task is explicitly repository/static with runtime_access none.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-control-bridge.md
  - tests/tools/tibia_re_control_center/test_agent_edge_bridge.py
validation:
  - command: git rebase origin/main
    result: PASS
    evidence: worker branch rebased cleanly onto ca1a71b5852f6e00ba144ed183af470555c51f56.
  - command: active task ownership scan
    result: PASS
    evidence: no overlapping active task owns the declared Control Center paths.
  - command: WSL focused baseline agent_session + agent_api + agent_mcp + agent_persistence
    result: PASS
    evidence: 109 tests passed under Linux-compatible WSL; Windows-only unauthenticated POST reset was isolated as a platform artifact.
  - command: WSL focused RED test_agent_edge_bridge
    result: FAIL
    evidence: RUNTIME_ACCESS_UNAVAILABLE proves the Phase 2 read-only bridge is absent before production changes.
blockers: []
next_action: implement the minimal read-only edge observation bridge to make the first focused RED test GREEN while preserving the Null executor and zero physical budget.
```
