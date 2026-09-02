---
task_id: OTC-20260902-central-current-client-fence
status: validating
agent: ChatGPT
session_role: implementer
worker_alias: OTC-CENTRAL-CURRENT-CLIENT-FENCE
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: refactor
phase: shared_runtime_infrastructure
branch: feat/OTC-20260902-central-current-client-fence
base_branch: main
base_main: 30fc46ce4dbff96d2484e624a58fcd85f2a9ecad
created: 2026-09-02T21:16:00+02:00
updated_at: 2026-09-02T22:31:23+02:00
risk: medium
execution_class: repository_only
execution_mode: chat
execution_reason: centralize weekly current-client identity without widening runtime authority
context_pressure: medium
context_growth: stable
context_score: 5
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one shared exact-fence source plus existing identity consumers
continuation_policy: continue_until_real_stop
task_completion_policy: return_to_coordinator_for_classification
policy_version: 2
invocation_started_at: 2026-09-02T22:18:00+02:00
last_progress_at: 2026-09-02T22:31:23+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
package_a_exception_head: 5bc0b88152ccdd5d2ab32f2a65f0dca688880567
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
implementation_authorized: true
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
red_head: 8d0bccbdc57e1d34f164eaa48a734be7fe47d2f6
implementation_head: 30879f705cfeaf84567356b8f90e35cb886af822
current_blocker: pr_862_exact_head_ci_and_independent_audit_pending
next_action: require terminal exact-head GitHub Actions and an independent exact-diff scope audit for Draft PR #862, then inspect review hygiene and promote only if ACCEPT
owned_paths:
  - docs/agents/contracts/TRACK_A_CURRENT_CLIENT_FENCE_V1.json
  - tools/tibia_re_control_center/current_client_fence.py
  - tools/tibia_re_control_center/agent_runtime_admission.py
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
  - .github/scripts/tibia-official-client-re-canonical-client-fence-reconcile.py
  - .github/scripts/test_tibia_official_client_re_canonical_client_fence_reconcile.py
  - .github/scripts/test_track_a_agent_runtime_governance.py
  - .github/scripts/test_track_a_canonical_current_client_fence.py
  - .github/workflows/track-a-canonical-current-client-fence.yml
  - .github/workflows/track-a-canonical-live-governance.yml
  - .github/workflows/track-a-kasm-canonical-bootstrap.yml
  - .github/workflows/track-a-surveyor-v2-readonly.yml
  - .github/workflows/track-a-canonical-client-fence-reconciliation.yml
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_V1.md
  - docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md
  - tests/tools/tibia_re_control_center/test_current_client_fence.py
  - tests/tools/tibia_re_control_center/test_agent_runtime_admission.py
  - tests/tools/tibia_re_control_center/test_agent_edge_bridge.py
  - tests/tools/tibia_re_control_center/test_vision_p2_trusted_composition.py
  - tests/tools/tibia_re_surveyor/test_operator_semantics.py
  - docs/superpowers/specs/2026-09-02-central-current-client-fence-design.md
  - docs/superpowers/plans/2026-09-02-central-current-client-fence.md
  - .github/workflows/tibia-re-control-center-core.yml
  - docs/agents/tasks/active/OTC-20260902-central-current-client-fence.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_ALIASES.md
  - docs/agents/prompts/OTC_20260902_VISION_P2_CENTRAL_FENCE_FINALIZATION_HANDOFF_ALIAS.md
  - docs/agents/prompts/OTC_20260902_VISION_P2_CENTRAL_FENCE_FINALIZATION_HANDOFF.md
---

# Objective

Replace duplicated active current-client identity constants with one strict canonical manifest so routine official-client releases require one reviewed identity promotion rather than edits across Surveyor, canonical runtime, Vision admission and reconciliation consumers.

# Safety boundary

- The manifest is identity data only and grants no runtime authority.
- `approved_history` is reconciliation-source-only; it never admits a historical build as current.
- Build-specific semantic/offset/QMeta workflows stay pinned until separately revalidated.
- No runtime observation, login, GUI input, process control, memory read or client mutation occurs in this repository-only task.
- Direct Codex usage remains zero.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-02T22:26:35+02:00
head: 5bc0b88152ccdd5d2ab32f2a65f0dca688880567
branch: feat/OTC-20260902-central-current-client-fence
pr: 862
status: validating
context_routes:
  - docs/agents/contracts/TRACK_A_CURRENT_CLIENT_FENCE_V1.json
  - tools/tibia_re_control_center/current_client_fence.py
  - .github/scripts/tibia-official-client-re-canonical-client-fence-reconcile.py
  - .github/workflows/track-a-surveyor-v2-readonly.yml
  - .github/workflows/track-a-canonical-client-fence-reconciliation.yml
  - docs/agents/tasks/active/OTC-20260902-central-current-client-fence.md
  - docs/agents/prompts/OTC_20260902_VISION_P2_CENTRAL_FENCE_FINALIZATION_HANDOFF.md
  - docs/agents/prompts/OTC_20260902_VISION_P2_CENTRAL_FENCE_FINALIZATION_HANDOFF_ALIAS.md
owned_paths:
  - docs/agents/contracts/TRACK_A_CURRENT_CLIENT_FENCE_V1.json
  - tools/tibia_re_control_center/current_client_fence.py
  - tools/tibia_re_control_center/agent_runtime_admission.py
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
  - .github/scripts/tibia-official-client-re-canonical-client-fence-reconcile.py
  - .github/scripts/test_tibia_official_client_re_canonical_client_fence_reconcile.py
  - .github/scripts/test_track_a_agent_runtime_governance.py
  - .github/scripts/test_track_a_canonical_current_client_fence.py
  - .github/workflows/track-a-canonical-current-client-fence.yml
  - .github/workflows/track-a-canonical-live-governance.yml
  - .github/workflows/track-a-kasm-canonical-bootstrap.yml
  - .github/workflows/track-a-surveyor-v2-readonly.yml
  - .github/workflows/track-a-canonical-client-fence-reconciliation.yml
  - .github/workflows/tibia-re-control-center-core.yml
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_V1.md
  - docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md
  - tests/tools/tibia_re_control_center/test_current_client_fence.py
  - tests/tools/tibia_re_control_center/test_agent_runtime_admission.py
  - tests/tools/tibia_re_control_center/test_agent_edge_bridge.py
  - tests/tools/tibia_re_control_center/test_vision_p2_trusted_composition.py
  - tests/tools/tibia_re_surveyor/test_operator_semantics.py
  - docs/superpowers/specs/2026-09-02-central-current-client-fence-design.md
  - docs/superpowers/plans/2026-09-02-central-current-client-fence.md
  - docs/agents/tasks/active/OTC-20260902-central-current-client-fence.md
  - docs/agents/prompts/OTC_20260902_VISION_P2_CENTRAL_FENCE_FINALIZATION_HANDOFF.md
  - docs/agents/prompts/OTC_20260902_VISION_P2_CENTRAL_FENCE_FINALIZATION_HANDOFF_ALIAS.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_ALIASES.md
proven:
  - central manifest and strict loader exist with immutable current provenance
  - identity and admission consumers use the manifest; executable current literal scan returned zero outside the manifest
  - reconciliation source is limited to manifest.current or approved_history and target is fresh manifest.current
  - Windows Control Center Vision Surveyor validation passed 66 of 66
  - Linux transition bootstrap adoption reconciliation session plus Kasm workflow validation passed 117 of 117
  - Track A governance central-fence gate YAML Ruff I/F compile and diff-check passed
  - build-specific semantic workflows remain intentionally version-pinned
derived:
  - future ordinary client promotions should update the central manifest instead of each identity consumer
unknown:
  - centralization Package A exact exception is committed at 5bc0b88152ccdd5d2ab32f2a65f0dca688880567 and exact/wrong-branch/wrong-base/fork controls are proven
  - Draft PR #862 exists on the exact task branch; exact-head GitHub Actions and independent final audit have not yet completed
  - canonical runtime registration remains stale until post-merge metadata reconciliation
  - final Vision P2 live capture Qwen reconcile gate has not run
conflicts:
  - none
first_failure:
  marker: weekly current-client updates required duplicated active fence edits
  evidence: Surveyor needed PR 861 and canonical reconciliation still retained an older hardcoded source/current pair
rejected_hypotheses:
  - Windows-worktree WSL transition failure was product regression: rejected after a native-LF detached exact-head worktree passed all 117 Linux/workflow tests; the failure signature was env bash CRLF shebang only
  - centralize build-specific semantic offsets and ABI evidence: rejected because those lanes require separate build revalidation
  - manually edit runtime-registration.json: rejected by canonical recovery contract
changed_paths:
  - .github/scripts/test_tibia_official_client_re_canonical_client_fence_reconcile.py
  - .github/scripts/test_track_a_agent_runtime_governance.py
  - .github/scripts/test_track_a_canonical_current_client_fence.py
  - .github/scripts/tibia-official-client-re-canonical-client-fence-reconcile.py
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
  - .github/workflows/track-a-canonical-client-fence-reconciliation.yml
  - .github/workflows/track-a-canonical-current-client-fence.yml
  - .github/workflows/track-a-canonical-live-governance.yml
  - .github/workflows/track-a-kasm-canonical-bootstrap.yml
  - .github/workflows/track-a-surveyor-v2-readonly.yml
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/contracts/TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/contracts/TRACK_A_CURRENT_CLIENT_FENCE_V1.json
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md
  - docs/superpowers/plans/2026-09-02-central-current-client-fence.md
  - docs/superpowers/specs/2026-09-02-central-current-client-fence-design.md
  - tests/tools/tibia_re_control_center/test_agent_edge_bridge.py
  - tests/tools/tibia_re_control_center/test_agent_runtime_admission.py
  - tests/tools/tibia_re_control_center/test_current_client_fence.py
  - tests/tools/tibia_re_control_center/test_vision_p2_trusted_composition.py
  - tests/tools/tibia_re_surveyor/test_operator_semantics.py
  - tools/tibia_re_control_center/agent_runtime_admission.py
  - tools/tibia_re_control_center/current_client_fence.py
  - docs/agents/tasks/active/OTC-20260902-central-current-client-fence.md
  - docs/agents/prompts/OTC_20260902_VISION_P2_CENTRAL_FENCE_FINALIZATION_HANDOFF.md
  - docs/agents/prompts/OTC_20260902_VISION_P2_CENTRAL_FENCE_FINALIZATION_HANDOFF_ALIAS.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_ALIASES.md
validation:
  - command: Package A exact branch/base/repository boundary simulation
    result: PASS
    evidence: exact base 30fc46ce4dbff96d2484e624a58fcd85f2a9ecad plus exact branch/repo accepted 32 branch paths; wrong branch, wrong base and fork each failed closed
  - command: Package A fresh and P1 falsification audits
    result: PASS
    evidence: PACKAGE_A_FRESH_AUDIT=PASS, MATERIAL_FINDINGS_OPEN=0, RUNTIME_ACCESS_NONE=PASS, FAKE_ONE_STEP_E2E=PASS and all P1 guards PASS
  - command: refreshed focused Windows current-fence/admission/bridge/composition/Surveyor subset
    result: PASS
    evidence: 57 tests OK; canonical current-client fence and Track A runtime governance PASS; Ruff I/F, py_compile, YAML parse and diff-check PASS
  - command: exact committed-head Linux/WSL transition/bootstrap/adoption/reconciliation/session/workflow matrix
    result: PASS
    evidence: detached native-LF worktree at 9e049dca821885e2173b9888ccd80345a965a6b4 ran 58 + 11 + 10 + 17 + 14 + 7 = 117 tests, all OK; cleanup refusal was only generated test artifacts in the disposable worktree and it was force-removed afterward
  - command: Windows Control Center Vision Surveyor focused matrix
    result: PASS
    evidence: 66 tests OK
  - command: Linux transition bootstrap adoption reconciliation canonical-session and Kasm workflow matrix
    result: PASS
    evidence: 117 tests OK
  - command: Track A central current-fence and runtime governance
    result: PASS
    evidence: both deterministic gates returned PASS
  - command: Ruff I/F py_compile YAML parse and git diff --check
    result: PASS
    evidence: all applicable static checks returned zero
  - command: executable current-version and current-SHA duplicate scan
    result: PASS
    evidence: zero active executable copies outside canonical manifest
blockers:
  - Draft PR #862 exact-head GitHub Actions and independent final scope audit are pending
next_action: finish only the exact Package A scope and checkpoint, open one Draft PR, require terminal exact-head CI and merge if accepted; then run existing canonical metadata reconciliation, one fresh Surveyor admission, and the final Vision P2 live E2E
```
