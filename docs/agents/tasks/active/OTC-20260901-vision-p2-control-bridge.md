---
task_id: OTC-20260901-vision-p2-control-bridge
status: ready
agent: chatgpt-gpt-5.6-sol
session_role: phase2_worker
worker_alias: OTC-VISION-P2-CONTROL-BRIDGE
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: implementation
phase: validate
branch: feat/OTC-20260901-vision-p2-control-bridge
base_branch: main
base_main: ca1a71b5852f6e00ba144ed183af470555c51f56
created: 2026-09-01T16:27:39+02:00
updated_at: 2026-09-01T18:01:19+02:00
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
next_action: OTC-VISION-P2-COORDINATOR independently classify Draft PR #830 against live exact-head CI and sibling contracts before any integration promotion
invocation_started_at: 2026-09-01T16:49:00+02:00
last_progress_at: 2026-09-01T18:01:19+02:00
ci_checks_for_current_head: 0
ci_check_generation: worker-ci-repair
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
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
updated_at: 2026-09-01T18:01:19+02:00
head: 3036ee5bc3e05765c4eb6988602cc9b0187b7696
branch: feat/OTC-20260901-vision-p2-control-bridge
pr: 830
status: ready
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
  - implementation commit aa2bfaa8fc47c4c7abdb1ddd28a80e5178ed903e extends the existing Control Center session/event backend with a fail-closed read-only edge bridge; no second store/control plane was added.
  - bounded read_only tasks require zero physical budget, no secret capability and SCREENSHOT-only action vocabulary; all other runtime classes remain refused here.
  - edge heartbeat/capture/runtime evidence is durable through existing AgentEvent storage; disconnect, stale heartbeat, restart, replay and competing edge-instance cases fail closed.
  - owner session/API/MCP/UI can observe edge status while production executor remains NULL, mutation authority NONE and physical action count/budget 0/0.
  - this invocation performed no Official Tibia/Kasm/Synology observation or mutation; runtime_access remained none.
derived:
  - the worker slice is repository/static producer-complete and ready for independent coordinator classification, not Phase 2 programme completion.
unknown:
  - exact-head GitHub CI outcome after publishing the final checkpoint commit.
  - coordinator classification and compatibility with later sibling producer contracts from PRs 826-829.
  - any real admitted read-only runtime evidence; none was authorized or claimed by this worker.
conflicts:
  - unchanged origin/main agent-foundation standalone E2E submits physical_action_budget 1 through an API guard that requires 0; this pre-existing baseline defect is outside this worker ownership.
first_failure:
  marker: TRACK_A_TASK_FRONTMATTER_NOT_DETECTED
  evidence: exact-head governance run 33529055205 job 99927229354 failed because the task file began with UTF-8 BOM before the YAML marker.
rejected_hypotheses:
  - replaying an earlier observation after disconnect is safely equivalent to fresh evidence: rejected by RED and fixed with monotonic run-timeline rejection.
  - a second edge instance may replace the connected instance without disconnect: rejected by RED and fixed fail-closed.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-control-bridge.md
  - docs/agents/reports/OTC-20260901-vision-p2-control-bridge.md
  - tools/tibia_re_control_center/agent_edge_bridge.py
  - tools/tibia_re_control_center/agent_session.py
  - tools/tibia_re_control_center/control_ui.py
  - tests/tools/tibia_re_control_center/test_agent_edge_bridge.py
  - tests/tools/tibia_re_control_center/test_agent_api.py
  - tests/tools/tibia_re_control_center/test_agent_mcp.py
validation:
  - command: ruff 0.16.1 on all changed Python implementation/tests
    result: PASS
    evidence: All checks passed.
  - command: python3 -m compileall -q tools/tibia_re_control_center tests/tools/tibia_re_control_center
    result: PASS
    evidence: compileall completed successfully after final implementation edits.
  - command: focused unittest edge bridge + session + API + MCP + persistence
    result: PASS
    evidence: 121 tests passed under Linux-compatible WSL after replay/instance hardening.
  - command: tests/tools/tibia_re_control_center/audit_agent_foundation.py
    result: PASS
    evidence: AGENT_FOUNDATION_AUDIT, runtime surfaces, authority boundaries and MCP allowlist all PASS.
  - command: tests/tools/tibia_re_control_center/audit_package_b.py
    result: PASS
    evidence: Package B boundary/transport/idempotency/restart/privacy audit PASS on Windows with repository Git available.
  - command: tests/tools/tibia_re_control_center/e2e_package_b.py
    result: PASS
    evidence: backend, CLI, real Chrome browser and restart/idempotency E2E PASS on Molehill Windows; Official client access remained NONE.
  - command: tests/tools/tibia_re_control_center/e2e_agent_foundation.py
    result: FAIL
    evidence: pre-existing origin/main fixture/API contradiction PHYSICAL_ACTION_BUDGET_UNAVAILABLE; both involved files are unchanged from origin/main.
  - command: full unittest discovery under WSL /mnt/c
    result: BLOCKED
    evidence: local Windows-mount I/O stayed in D state and was terminated after 462 seconds without emitting a test failure; exact-head GitHub CI remains authoritative for the full suite.
  - command: python .github/scripts/test_track_a_agent_runtime_governance.py --changed-from ca1a71b5852f6e00ba144ed183af470555c51f56 --expected-branch feat/OTC-20260901-vision-p2-control-bridge
    result: PASS
    evidence: after removing the pre-existing UTF-8 BOM, the exact deterministic governance command reports TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true.
blockers: []
next_action: OTC-VISION-P2-COORDINATOR independently classify Draft PR #830 against live exact-head CI and sibling contracts before any integration promotion.
```
