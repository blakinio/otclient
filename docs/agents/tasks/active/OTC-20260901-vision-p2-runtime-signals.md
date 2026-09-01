---
task_id: OTC-20260901-vision-p2-runtime-signals
status: ready
agent: ChatGPT
session_role: phase2_worker
worker_alias: OTC-VISION-P2-RUNTIME-SIGNALS
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: implementation
phase: worker_revalidation_ready_for_coordinator
branch: feat/OTC-20260901-vision-p2-runtime-signals
base_branch: main
base_main: 54a20bbd8721e92d069974af14d6ebd2f4f5a55d
created: 2026-09-01T16:27:39+02:00
updated_at: 2026-09-01T18:54:35+02:00
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
worktree: C:/Users/barte/otclient-vision-p2-runtime-signals
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-runtime-signals.md
  - docs/agents/reports/OTC-20260901-vision-p2-runtime-signals.md
  - tools/tibia_re_control_center/agent_runtime_signals.py
  - tests/tools/tibia_re_control_center/test_agent_runtime_signals.py
depends_on:
  - PR #820 merged foundation
  - PR #824 merged Wave 0 coordinator cleanup
  - main 0fe1ecb3569f1d8372209c857ab57f3b626c29ae
related_prs:
  - PR #828 Wave 1 worker Draft
current_blocker: none
next_action: return current-main-green Draft PR #828 to OTC-VISION-P2-COORDINATOR for integration classification; worker must not self-promote or merge
invocation_started_at: 2026-09-01T17:02:17+02:00
last_progress_at: 2026-09-01T18:54:35+02:00
ci_checks_for_current_head: 4
ci_check_generation: current-main-green-9d751f340e0a
terminal_ci_wait_started_at: 2026-09-01T18:52:09+02:00
terminal_ci_checks_for_current_generation: 4
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

# OTC-VISION-P2-RUNTIME-SIGNALS

## Mission

Implement trusted reviewed runtime-signal ingestion with provenance/freshness/run/runtime binding; model output must never become authority and process-memory or payload capture remains forbidden.

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

- `docs/agents/tasks/active/OTC-20260901-vision-p2-runtime-signals.md`
- `docs/agents/reports/OTC-20260901-vision-p2-runtime-signals.md`
- `tools/tibia_re_control_center/agent_runtime_signals.py`
- `tests/tools/tibia_re_control_center/test_agent_runtime_signals.py`

Shared indexes/governance files, including `docs/agents/MODULE_CATALOG.md`, are not owned. Any required path outside this set is a coordinator ownership-extension request, not an implicit permission.

## Implementation discipline

Use RED-to-GREEN TDD for each behavior. Preserve the approved architecture and reuse the existing Control Center/session plane rather than creating a second control plane/store. Fake/hosted evidence can validate repository behavior but can never be reported as real-runtime success. The worker must open no additional implementation PR and must not merge/promote its own result; the coordinator classifies the Draft PR.

## Dispatch contract

```yaml
programme_id: OTC-VISION-P2-READONLY
worker_alias: OTC-VISION-P2-RUNTIME-SIGNALS
TASK_ID: OTC-20260901-vision-p2-runtime-signals
TASK_RECORD: docs/agents/tasks/active/OTC-20260901-vision-p2-runtime-signals.md
PROJECT_LANE: otclient
BASE_MAIN: 0fe1ecb3569f1d8372209c857ab57f3b626c29ae
BRANCH: feat/OTC-20260901-vision-p2-runtime-signals
WORKTREE: C:/Users/barte/otclient-vision-p2-runtime-signals
OWNED_PATHS:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-runtime-signals.md
  - docs/agents/reports/OTC-20260901-vision-p2-runtime-signals.md
  - tools/tibia_re_control_center/agent_runtime_signals.py
  - tests/tools/tibia_re_control_center/test_agent_runtime_signals.py
DEPENDENCIES:
  - PR #820 merged
  - PR #824 merged
runtime_access: none
```

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T18:54:35+02:00
head: d240e63c51d672356e1f9b396f14cfda10b0dc45
branch: feat/OTC-20260901-vision-p2-runtime-signals
pr: 828
status: ready
context_routes:
  - phase-2-read-only-coordination
  - track-a-governance
  - runtime-signals
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-runtime-signals.md
  - docs/agents/reports/OTC-20260901-vision-p2-runtime-signals.md
  - tools/tibia_re_control_center/agent_runtime_signals.py
  - tests/tools/tibia_re_control_center/test_agent_runtime_signals.py
proven:
  - coordinator independent review comment 5496967667 accepts the bounded repository/static runtime-signal producer contract with no live-runtime claim.
  - shared Package A durable-doc repair #833 and coordinator checkpoint #836 are merged into trusted current main 54a20bbd8721e92d069974af14d6ebd2f4f5a55d.
  - worker branch restacked conflict-free onto trusted current main; main changes none of the four worker-owned paths.
  - accepted runtime-signal contract is unchanged: sample payload cannot author semantic authority, reviewed-source handles are resolver-owned, exact runtime/admission hash and clock-domain binding remain fail-closed.
  - fresh post-restack focused runtime-signals suite passes 21/21; Ruff and py_compile pass.
  - fresh frozen vision benchmark passes 34/34.
  - fresh Track A runtime governance, checkpoint validation and git diff --check pass; changed paths remain exactly four worker-owned files.
  - exact head 9d751f340e0a9d1331d7f854795a7aa9d4b93425 passed CI 33534363910, Package A 33534363711, Package B 33534363817 and Track A governance 33534363709.
  - no Official Tibia observation, model inference, credentials, GUI input, process control, process memory, payload capture or physical action occurred.
derived:
  - current-main repository/static revalidation is green locally and on exact-head hosted checks.
  - consumer/integration must still construct runtime-signal binding only from an accepted current #826 admission; this worker does not self-grant that authority.
unknown:
  - coordinator promotion/integration disposition after fresh hosted validation.
conflicts: []
first_failure:
  marker: historical-package-a-path-boundary
  evidence: prior exact generation failed only the old Phase-2 durable-doc allowlist; repair #833 is merged and fresh validation is required.
rejected_hypotheses:
  - old Package A failure remains current after #833: rejected; this restack must obtain new exact-head results.
  - sample/model payload may self-select runtime state or evidence class: rejected by accepted typed contract and focused tests.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-runtime-signals.md
  - docs/agents/reports/OTC-20260901-vision-p2-runtime-signals.md
  - tools/tibia_re_control_center/agent_runtime_signals.py
  - tests/tools/tibia_re_control_center/test_agent_runtime_signals.py
validation:
  - command: python -m unittest tests.tools.tibia_re_control_center.test_agent_runtime_signals -q
    result: PASS
    evidence: 21 tests, zero failures/errors after current-main restack.
  - command: Ruff and py_compile on runtime-signals implementation and test
    result: PASS
    evidence: both static checks pass.
  - command: frozen vision benchmark
    result: PASS
    evidence: 34 tests, zero failures/errors.
  - command: Track A governance checkpoint validator and git diff --check
    result: PASS
    evidence: governance and checkpoint pass; exact changed paths remain four worker-owned files.
  - command: GitHub exact-head hosted gates on 9d751f340e0a9d1331d7f854795a7aa9d4b93425
    result: PASS
    evidence: CI 33534363910, Package A 33534363711, Package B 33534363817 and Track A governance 33534363709 all conclude success.
blockers: []
next_action: return current-main-green Draft PR #828 to OTC-VISION-P2-COORDINATOR for integration classification; worker must not self-promote or merge.
```
