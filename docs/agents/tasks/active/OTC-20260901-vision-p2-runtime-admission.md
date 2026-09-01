---
task_id: OTC-20260901-vision-p2-runtime-admission
status: waiting
agent: ChatGPT
session_role: phase2_worker
worker_alias: OTC-VISION-P2-RUNTIME-ADMISSION
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: implementation
phase: waiting_runtime_observation
branch: feat/OTC-20260901-vision-p2-runtime-admission
base_branch: main
base_main: ca1a71b5852f6e00ba144ed183af470555c51f56
created: 2026-09-01T16:27:39+02:00
updated_at: 2026-09-01T17:35:16+02:00
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
current_blocker: coordinator-assigned serialized read-only observation window not granted; live runtime remains unauthorized
next_action: coordinator assigns one serialized read-only observation window; then freshly prove locator, inventory, exact process fence and X11 ownership through admit_read_only_runtime without mutation
invocation_started_at: 2026-09-01T16:47:00+02:00
last_progress_at: 2026-09-01T17:35:16+02:00
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
updated_at: 2026-09-01T17:35:16+02:00
head: 9d8233528bcf2dd1c4e214d2aee3a8677d3a07ad
head_semantics: implementation_commit_before_checkpoint_docs
branch: feat/OTC-20260901-vision-p2-runtime-admission
pr: 826
status: waiting
phase: waiting_runtime_observation
runtime_access: none
mutation_authorized: false
physical_action_budget: 0
physical_action_count: 0
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
  - live repository state was reconciled and the worker branch was rebased without conflict onto main ca1a71b5852f6e00ba144ed183af470555c51f56.
  - Draft PR 826 remains the exact worker delivery vehicle and no additional implementation PR was created.
  - static read-only admission/provenance producer is implemented at 9d8233528bcf2dd1c4e214d2aee3a8677d3a07ad.
  - exact current client fence is enforced as 15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a.
  - admission fails closed on stale/future evidence, ownership, namespace, uniqueness, locator, process/window identity, forbidden effects, unknown fields and unsafe observer endpoints.
  - Track A read-only canonical fields and gates remain NOT_APPLICABLE and mutation_authorized remains false.
  - focused final tests are 14/14 PASS; ruff and compileall PASS.
  - final test_agent_*.py run executed 219 tests with 215 PASS and 4 known baseline errors outside owned paths.
  - no credentials, GUI input, process control, process memory access, network payload capture or physical action occurred.
derived:
  - the static producer is ready to consume fresh facts only inside a coordinator-assigned read-only observation window.
  - the worker remains waiting until a valid live read_only admission/provenance record is freshly produced and persisted.
unknown:
  - current exact live Synology/Kasm client process identity.
  - current runtime locator reachability and endpoint mapping.
  - current all-container target uniqueness and X11 ownership.
  - any live read_only admission/provenance record; none has been legally produced yet.
conflicts: []
first_failure:
  marker: live_admission_not_authorized
  evidence: runtime_access remains none because no serialized read-only observation window has been assigned.
rejected_hypotheses:
  - historical Package C Surveyor fence can establish current Phase 2 identity: rejected because its client tuple is stale and differs from the trusted-base fence.
  - hosted/static tests can satisfy real-runtime acceptance: rejected by the Phase 2 coordination contract.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-runtime-admission.md
  - docs/agents/reports/OTC-20260901-vision-p2-runtime-admission.md
  - tools/tibia_re_control_center/agent_runtime_admission.py
  - tests/tools/tibia_re_control_center/test_agent_runtime_admission.py
validation:
  - command: focused runtime-admission unittest suite
    result: PASS
    evidence: 14 tests passed on exact-final implementation.
  - command: ruff check implementation and focused test
    result: PASS
    evidence: exact-final implementation and focused test passed Ruff with no findings.
  - command: compileall implementation and focused test
    result: PASS
    evidence: exact-final implementation and focused test compiled successfully.
  - command: test_agent_*.py component suite
    result: FAIL
    evidence: 219 total, 215 PASS, 4 errors within the previously reproduced current-main baseline error set.
  - command: detached origin/main baseline reproduction
    result: PASS
    evidence: current main independently reproduced the same agent_api socket-reset and agent_vision model-slot error family.
blockers:
  - coordinator-assigned serialized read-only observation window is not granted.
  - Synology remote targets were offline during this worker session; this is secondary to the authority blocker.
next_action: coordinator assigns one serialized read-only observation window; then freshly prove locator, inventory, exact process fence and X11 ownership through admit_read_only_runtime without mutation.
```
