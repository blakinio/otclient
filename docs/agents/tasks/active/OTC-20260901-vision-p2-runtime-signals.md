---
task_id: OTC-20260901-vision-p2-runtime-signals
status: validating
agent: ChatGPT
session_role: phase2_worker
worker_alias: OTC-VISION-P2-RUNTIME-SIGNALS
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: implementation
phase: repository_static_validation
branch: feat/OTC-20260901-vision-p2-runtime-signals
base_branch: main
base_main: 0fe1ecb3569f1d8372209c857ab57f3b626c29ae
created: 2026-09-01T16:27:39+02:00
updated_at: 2026-09-01T17:56:26+02:00
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
next_action: publish the admission-bound runtime-signals follow-up to Draft PR #828, inspect exact-head GitHub CI, then return the worker result to OTC-VISION-P2-COORDINATOR
invocation_started_at: 2026-09-01T17:02:17+02:00
last_progress_at: 2026-09-01T17:56:26+02:00
ci_checks_for_current_head: 0
ci_check_generation: admission-bound-followup-pending-publish
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
updated_at: 2026-09-01T17:56:26+02:00
head: 16f9af0123e4ead21d2f97c1919a92826427fe95
branch: feat/OTC-20260901-vision-p2-runtime-signals
pr: 828
status: validating
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
  - Draft PR 828 remains open, Draft, mergeable and bound to feat/OTC-20260901-vision-p2-runtime-signals; PR 820 and PR 824 are merged prerequisites.
  - refreshed origin/main ca1a71b5852f6e00ba144ed183af470555c51f56 changes none of this worker's owned paths.
  - repository/static RED-to-GREEN implementation provides reviewed-source, session/run/runtime/runtime-instance, admission runtime_binding_sha256, clock-domain, freshness, content-addressing, supersession and causal-conflict fail-closed behavior.
  - semantic IN_GAME or WORLD_EXIT output is accepted only from REVIEWED_CAUSAL contract rules; STRUCTURAL_ONLY and UNKNOWN rules may emit only UNKNOWN.
  - RuntimeSignalSample cannot supply runtime_state, evidence_class, producer_id or contract_id, so sample/model payload cannot self-select semantic authority through this interface.
  - RuntimeSignalBinding requires the exact lowercase 64-hex runtime_binding_sha256 from the sibling admission contract, preventing a signal from crossing to a different freshly admitted target.
  - focused runtime-signals suite passes 21 tests and Ruff passes on both owned Python files.
  - filtered Control Center regression passes 476 tests with 2 skips after excluding exactly three pre-existing failing test methods; frozen vision benchmark passes 34 tests.
  - the three excluded methods reproduce with identical failure classes on clean branch head 11fc18820 before local implementation is restored.
  - runtime_access remains none; no Official Tibia observation, process-memory read, packet/payload capture, model inference, GUI input, credentials, login, process control or physical action occurred.
derived:
  - no production REVIEWED_CAUSAL producer is hard-coded because current repository evidence does not safely qualify one under this task authority; later coordinator integration must bind only separately reviewed current producers.
  - the local slice is coherent for publication and exact-head hosted validation; clean-head baseline failures are not owned by this worker and must not be repaired here.
unknown:
  - exact-head GitHub CI outcome after the implementation checkpoint is published.
  - coordinator classification and any later serialized real read-only observation evidence.
conflicts: []
first_failure:
  marker: EXACT_HEAD_CI_NOT_RUN
  evidence: admission-binding follow-up is locally validated but has not yet been committed/pushed from implementation head 16f9af0123e4ead21d2f97c1919a92826427fe95.
rejected_hypotheses:
  - the five full-suite errors were introduced by runtime-signals changes: rejected because the exact three failing test methods reproduce on clean head 11fc18820 with the local implementation stashed.
  - structural/QMeta/window/model evidence may assert IN_GAME: rejected by the binding Phase 2 contract and enforced by contract validation.
  - fake/hosted evidence can satisfy real-runtime acceptance: rejected; this report makes no real-runtime claim.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-runtime-signals.md
  - docs/agents/reports/OTC-20260901-vision-p2-runtime-signals.md
  - tools/tibia_re_control_center/agent_runtime_signals.py
  - tests/tools/tibia_re_control_center/test_agent_runtime_signals.py
validation:
  - command: python -m unittest tests.tools.tibia_re_control_center.test_agent_runtime_signals -q
    result: PASS
    evidence: 21 tests passed.
  - command: filtered Control Center discovery excluding the three clean-head baseline-failing methods
    result: PASS
    evidence: 476 tests passed, 2 skipped; TOTAL_DISCOVERED=479, EXCLUDED=3.
  - command: python -m unittest discover -s tools/tibia-re-vision-benchmark/tests -p test_*.py -q
    result: PASS
    evidence: 34 tests passed.
  - command: python -m ruff check tools/tibia_re_control_center/agent_runtime_signals.py tests/tools/tibia_re_control_center/test_agent_runtime_signals.py
    result: PASS
    evidence: All checks passed.
  - command: clean-head reproduction with local implementation stashed
    result: PASS
    evidence: all three excluded baseline methods fail on clean 11fc18820 with the same ConnectionResetError / ModelSlotUnavailable classes.
  - command: git diff 0fe1ecb..origin/main -- <owned paths>
    result: PASS
    evidence: no owned-path overlap on refreshed main ca1a71b5852f6e00ba144ed183af470555c51f56.
blockers: []
next_action: publish the admission-bound runtime-signals follow-up to Draft PR #828, inspect exact-head GitHub CI, then return the worker result to OTC-VISION-P2-COORDINATOR.
```
