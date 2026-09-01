---
task_id: OTC-20260901-vision-p2-control-bridge
status: validating
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
base_main: d1cb8722c3116a0e0aeb72b9b360712f43151f17
created: 2026-09-01T16:27:39+02:00
updated_at: 2026-09-01T23:04:01+02:00
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
  - main e883543403d5430d7b1d287f59043b23c98f37d6
related_prs:
  - PR #830 Wave 1 worker Draft
current_blocker: exact-head coordinator review 5500323278 returned two material authority/lifetime findings for repair
next_action: run the full relevant hosted-equivalent suite after focused RED-to-GREEN authority and lifetime repair
invocation_started_at: 2026-09-01T16:49:00+02:00
last_progress_at: 2026-09-01T23:04:01+02:00
ci_checks_for_current_head: 4
ci_check_generation: exact-head-green-274955658
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 4
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
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
updated_at: 2026-09-01T22:16:27+02:00
head: 274955658f08c8631d24511be1646a9ec16fff6c
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
  - trusted main e883543403d5430d7b1d287f59043b23c98f37d6 contains merged runtime-admission producer #838 and merged runtime-signals producer #839; neither promotion overlaps this worker's five implementation/test paths.
  - repair commit 7ec06d4d9bdec9f10f76cb7b8b49d5f696e28ecd requires the exact merged ReadOnlyRuntimeAdmission, RuntimeSignalResolver, RuntimeSignalBinding and RuntimeSignalEvidence types before any edge state can become current.
  - caller-declared TaskEnvelope runtime_access read_only is insufficient: without fresh machine-revalidated admission, official_client_access remains NONE and edge reason is RUNTIME_ADMISSION_REQUIRED.
  - direct runtime strings/opaque refs in edge observations are rejected; semantic runtime state is accepted only from current resolver-owned reviewed RuntimeSignalEvidence whose content-addressed provenance digest matches the merged #839 contract.
  - admission is rebound to the same task, run, runtime namespace/binding hash and exact TaskEnvelope client identity; stale, forged, foreign, duck-typed, replayed or silently replaced authority fails closed.
  - disconnect and process restart discard live runtime authority; fresh admission plus reviewed runtime evidence is required again.
  - production executor remains NULL, mutation authority NONE, physical action budget/count 0/0; no second control plane/store was added.
  - this invocation performed no Synology/Kasm/Official Tibia observation or mutation and used runtime_access none.
derived:
  - the coordinator's material RETURN_FOR_REPAIR finding is addressed locally and the worker is ready for hosted exact-head validation.
unknown:
  - independent coordinator reclassification of repaired Draft PR #830.
conflicts: []
first_failure:
  marker: COORDINATOR_RETURN_FOR_REPAIR_RUNTIME_AUTHORITY_NOT_BOUND
  evidence: live PR #830 required machine validation of accepted #826/#838 admission and #828/#839 typed runtime-signal evidence; initial REDs proved caller-declared read_only and duck-typed/fabricated runtime evidence could pass the prior bridge boundary.
rejected_hypotheses:
  - caller-declared read_only is sufficient runtime authority: rejected; official client access stays NONE until a fresh canonical admission is bound.
  - arbitrary runtime status plus opaque refs is acceptable semantic evidence: rejected; edge payload runtime semantics are forbidden.
  - structural/duck-typed lookalikes are equivalent to accepted producer contracts: rejected; exact merged #839 classes are required.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-control-bridge.md
  - docs/agents/reports/OTC-20260901-vision-p2-control-bridge.md
  - tools/tibia_re_control_center/agent_edge_bridge.py
  - tools/tibia_re_control_center/agent_session.py
  - tools/tibia_re_control_center/control_ui.py
  - tests/tools/tibia_re_control_center/test_agent_edge_bridge.py
  - tests/tools/tibia_re_control_center/test_agent_api.py
validation:
  - command: git rebase --autostash origin/main
    result: PASS
    evidence: worker restacked conflict-free onto trusted main e883543403d5430d7b1d287f59043b23c98f37d6; main drift was only merged runtime-signals promotion #839 and had no worker-path overlap.
  - command: ruff 0.16.1 on all changed Python implementation/tests
    result: PASS
    evidence: All checks passed after exact #839 type integration.
  - command: python3 -m compileall -q tools/tibia_re_control_center tests/tools/tibia_re_control_center
    result: PASS
    evidence: compileall completed successfully on the final local repair tree.
  - command: WSL python3 -m unittest discover -s tests/tools/tibia_re_control_center -p test_agent*.py -q
    result: PASS
    evidence: 260 tests passed, 1 skipped on Linux-compatible WSL.
  - command: Windows agent suite
    result: FAIL
    evidence: only established platform baseline remained: four WinError 10054 loopback POST resets and one existing MODEL_INFERENCE_FAILED vision test in the broader run; no bridge-specific failure signature.
  - command: audit_agent_foundation.py
    result: PASS
    evidence: runtime surfaces, authority boundaries and MCP allowlist PASS.
  - command: audit_package_a.py plus audit_package_a_p1.py
    result: PASS
    evidence: MATERIAL_FINDINGS_OPEN=0, RUNTIME_ACCESS_NONE=PASS and all Package A/P1 safety fences PASS.
  - command: audit_package_b.py
    result: PASS
    evidence: boundary, transport, idempotency, restart and privacy audit PASS with OFFICIAL_CLIENT_ACCESS=NONE.
  - command: e2e_package_b.py
    result: PASS
    evidence: backend, CLI, real Chrome browser and restart/idempotency E2E PASS with OFFICIAL_CLIENT_ACCESS=NONE.
  - command: git diff --check
    result: PASS
    evidence: no whitespace errors on the repair diff.
  - command: exact-head GitHub Actions on 274955658f08c8631d24511be1646a9ec16fff6c
    result: PASS
    evidence: Track A governance 33554082006 SUCCESS; Package A 33554082232 SUCCESS; Package B 33554082117 SUCCESS including full regression and real-browser E2E; CI 33554082565 SUCCESS with CI / Required PASS.
blockers: []
next_action: OTC-VISION-P2-COORDINATOR independently reclassify repaired Draft PR #830 against exact-head green evidence and current live integration state.
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 1
  session_id: control-bridge-repair-20260901T230401+0200
  session_started_at: 2026-09-01T22:16:27+02:00
  checkpointed_at: 2026-09-01T23:04:01+02:00
  last_progress_at: 2026-09-01T23:04:01+02:00
  phase: validating
  exact_head: working-tree-on-5e615ee27c50edb827bc2bdd4a718f6dbc052706
  pull_request: 830
  active_operation: repair commit and deterministic safety audit
  external_run_ids: []
  operation_started_at: null
  wait_deadline_at: null
  check_generation: repair-pending-local-audit
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: repair commit is published and deterministic safety audits have completed
  next_action: commit and push the bounded authority/lifetime repair, then run Package A, Package B and Track A validation
```
