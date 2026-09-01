---
task_id: OTC-20260901-vision-p2-runtime-admission
status: validating
agent: ChatGPT
session_role: phase2_worker
worker_alias: OTC-VISION-P2-RUNTIME-ADMISSION
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: implementation
phase: current_main_revalidation_complete
branch: feat/OTC-20260901-vision-p2-runtime-admission
base_branch: main
base_main: 54a20bbd8721e92d069974af14d6ebd2f4f5a55d
created: 2026-09-01T16:27:39+02:00
updated_at: 2026-09-01T18:46:29+02:00
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
worktree: C:/Users/barte/otclient-vision-p2-runtime-admission
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-runtime-admission.md
  - docs/agents/reports/OTC-20260901-vision-p2-runtime-admission.md
  - tools/tibia_re_control_center/agent_runtime_admission.py
  - tests/tools/tibia_re_control_center/test_agent_runtime_admission.py
depends_on:
  - PR #820 merged foundation
  - PR #824 merged Wave 0 coordinator cleanup
  - main ca1a71b5852f6e00ba144ed183af470555c51f56
related_prs:
  - PR #826 Wave 1 worker Draft
current_blocker: exact-head CI Package A and Track A governance pending on current-main restack; live observation remains unauthorized
next_action: publish current-main restack and obtain fresh exact-head CI Package A and Track A governance; after green coordinator may assign one serialized read-only observation window
invocation_started_at: 2026-09-01T16:47:00+02:00
last_progress_at: 2026-09-01T18:46:29+02:00
ci_checks_for_current_head: 0
ci_check_generation: current-main-restack-79fa5fbca652
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

# OTC-VISION-P2-RUNTIME-ADMISSION

## Mission

Implement the repository/static runtime-admission boundary that can later prove and bind one exact current read-only Synology/Kasm target without granting mutation authority.

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

- `docs/agents/tasks/active/OTC-20260901-vision-p2-runtime-admission.md`
- `docs/agents/reports/OTC-20260901-vision-p2-runtime-admission.md`
- `tools/tibia_re_control_center/agent_runtime_admission.py`
- `tests/tools/tibia_re_control_center/test_agent_runtime_admission.py`

Shared indexes/governance files, including `docs/agents/MODULE_CATALOG.md`, are not owned. Any required path outside this set is a coordinator ownership-extension request, not an implicit permission.

## Implementation discipline

Use RED-to-GREEN TDD for each behavior. Preserve the approved architecture and reuse the existing Control Center/session plane rather than creating a second control plane/store. Fake/hosted evidence can validate repository behavior but can never be reported as real-runtime success. The worker must open no additional implementation PR and must not merge/promote its own result; the coordinator classifies the Draft PR.

## Dispatch contract

```yaml
programme_id: OTC-VISION-P2-READONLY
worker_alias: OTC-VISION-P2-RUNTIME-ADMISSION
TASK_ID: OTC-20260901-vision-p2-runtime-admission
TASK_RECORD: docs/agents/tasks/active/OTC-20260901-vision-p2-runtime-admission.md
PROJECT_LANE: otclient
BASE_MAIN: 0fe1ecb3569f1d8372209c857ab57f3b626c29ae
BRANCH: feat/OTC-20260901-vision-p2-runtime-admission
WORKTREE: C:/Users/barte/otclient-vision-p2-runtime-admission
OWNED_PATHS:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-runtime-admission.md
  - docs/agents/reports/OTC-20260901-vision-p2-runtime-admission.md
  - tools/tibia_re_control_center/agent_runtime_admission.py
  - tests/tools/tibia_re_control_center/test_agent_runtime_admission.py
DEPENDENCIES:
  - PR #820 merged
  - PR #824 merged
runtime_access: none
```

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T18:46:29+02:00
head: 79fa5fbca652048e6fb9408d03140d5d707d075d
branch: feat/OTC-20260901-vision-p2-runtime-admission
pr: 826
status: validating
context_routes:
  - phase-2-read-only-coordination
  - track-a-governance
  - runtime-admission
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-runtime-admission.md
  - docs/agents/reports/OTC-20260901-vision-p2-runtime-admission.md
  - tools/tibia_re_control_center/agent_runtime_admission.py
  - tests/tools/tibia_re_control_center/test_agent_runtime_admission.py
proven:
  - coordinator independent review comment 5496990233 accepts the bounded static ReadOnlyRuntimeAdmission/provenance producer and keeps real-runtime acceptance at RETURN_FOR_EVIDENCE.
  - shared Package A durable-doc repair #833 and coordinator checkpoint #836 are merged into trusted current main 54a20bbd8721e92d069974af14d6ebd2f4f5a55d.
  - worker branch restacked conflict-free onto trusted current main; main changes none of the four worker-owned paths.
  - accepted static admission contract is unchanged by the restack and remains fail-closed on freshness, uniqueness, locator, process/X11 identity, ownership, namespace and forbidden effects.
  - fresh post-restack focused runtime-admission suite passes 14/14; Ruff and py_compile pass.
  - fresh post-restack Track A runtime governance, checkpoint validator and git diff --check pass; changed paths remain exactly the four worker-owned paths.
  - no credentials, GUI input, process control, process memory access, network payload capture, runtime observation or physical action occurred.
derived:
  - current-main repository/static revalidation is locally green and ready for hosted exact-head checks.
  - live read-only observation remains illegal until hosted revalidation is green and the coordinator separately assigns one serialized observation window.
unknown:
  - exact-head CI Package A and Track A governance outcome after publishing the restack.
  - current exact live Synology/Kasm client process identity, locator reachability, inventory uniqueness and X11 ownership.
conflicts: []
first_failure:
  marker: historical-package-a-path-boundary
  evidence: prior exact head failed only the old durable-doc allowlist; coordinator repair #833 is now merged and this restack must obtain a fresh result.
rejected_hypotheses:
  - old Package A failure can be treated as current after #833: rejected; fresh exact-head validation is required.
  - static acceptance authorizes live observation: rejected; coordinator still owns serialized read-only admission.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-runtime-admission.md
  - docs/agents/reports/OTC-20260901-vision-p2-runtime-admission.md
  - tools/tibia_re_control_center/agent_runtime_admission.py
  - tests/tools/tibia_re_control_center/test_agent_runtime_admission.py
validation:
  - command: python -m unittest tests.tools.tibia_re_control_center.test_agent_runtime_admission -q
    result: PASS
    evidence: 14 tests, zero failures/errors after current-main restack.
  - command: Ruff and py_compile on implementation and focused test
    result: PASS
    evidence: static checks pass after restack.
  - command: Track A runtime governance validator changed-from trusted current main
    result: PASS
    evidence: TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true.
  - command: checkpoint validator and git diff --check origin/main...HEAD
    result: PASS
    evidence: checkpoint valid and exact changed paths remain four worker-owned files.
blockers:
  - exact-head hosted CI Package A and Track A governance pending after publication.
  - real runtime observation remains separately coordinator-gated.
next_action: publish current-main restack and obtain fresh exact-head CI Package A and Track A governance; after green coordinator may assign one serialized read-only observation window.
```
