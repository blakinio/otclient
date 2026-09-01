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
phase: wave_1_ci_repair
branch: ci/OTC-20260901-vision-p2-package-a-path-boundary
base_branch: main
base_main: ca1a71b5852f6e00ba144ed183af470555c51f56
created: 2026-09-01T15:45:26+02:00
updated_at: 2026-09-01T17:55:03+02:00
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
worktree: NOT_APPLICABLE_GITHUB_ONLY
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
  - .github/workflows/tibia-re-control-center-core.yml
modules_touched:
  - github_actions_package_a_governance
reuses:
  - existing Package A falsification audit
  - existing Phase 2 programme ownership contract
depends_on:
  - PR #820 merged foundation
  - PR #823 merged Phase 2 prompt-package closeout
  - PR #825 merged Wave 1 dispatch checkpoint
blocks:
  - PR #826 exact-head Package A audit classification
  - equivalent Wave 1 worker documentation paths under Package A audit
related_prs:
  - PR #820 merged foundation integration
  - PR #823 merged Phase 2 prompt-package closeout
  - PR #824 merged Wave 0 coordinator cleanup
  - PR #825 merged Wave 1 coordinator dispatch
  - PR #826 runtime-admission worker Draft
  - PR #827 capture-edge worker Draft
  - PR #828 runtime-signals worker Draft
  - PR #829 edge-transport worker Draft
  - PR #830 control-bridge worker Draft
current_blocker: PR_826_FRESH_PACKAGE_A_PATH_BOUNDARY
next_action: repair the Package A changed-path audit so the exact Phase 2 programme task/report family is admitted without expanding runtime authority, then prove the repair on an exact-head coordinator PR
invocation_started_at: 2026-09-01T17:47:00+02:00
last_progress_at: 2026-09-01T17:55:03+02:00
ci_checks_for_current_head: 0
ci_check_generation: ci-repair-draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
---

# OTC Vision Phase 2 read-only programme coordinator

## Objective

Coordinate Phase 2 read-only runtime-edge integration, classify worker output, repair shared coordination/governance blockers, serialize any real read-only observation and drive the programme through exact-head audit/E2E closeout without entering Phase 3+.

## Binding authority

- `docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md`
- `docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md`
- `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`
- current `main`, live PR/check state and stricter trusted-base governance override stale historical prose.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T17:55:03+02:00
head: ca1a71b5852f6e00ba144ed183af470555c51f56
head_semantics: trusted_base_before_coordinator_repair_commits
branch: ci/OTC-20260901-vision-p2-package-a-path-boundary
pr: NOT_OPEN_YET
status: implementing
context_routes:
  - phase-2-read-only-coordination
  - track-a-governance
  - ci-repair
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
  - .github/workflows/tibia-re-control-center-core.yml
proven:
  - main is ca1a71b5852f6e00ba144ed183af470555c51f56 from merged PR 825.
  - PR 826 advanced to exact head 0dbd823f6c89895e919f9bc07f7e99ecac9f31a6 and contains a completed static runtime-admission implementation.
  - PR 826 focused runtime-admission tests are 14/14 PASS; Ruff and compileall PASS; its wider agent suite reproduces only the previously established current-main baseline error family.
  - PR 826 exact-head CI / Required is SUCCESS, but Fresh Package A falsification audit is FAILURE.
  - the Package A audit computes the complete PR changed-path set and allows control-center/vision code prefixes but not Phase 2 worker task/report documentation.
  - PR 826 changed documentation includes docs/agents/tasks/active/OTC-20260901-vision-p2-runtime-admission.md and docs/agents/reports/OTC-20260901-vision-p2-runtime-admission.md; these are mandatory worker-owned durable artifacts.
  - the same missing programme-documentation boundary would affect later Wave 1 lanes when their task/report files accompany control-center/vision implementation.
  - PRs 827-830 remain open Drafts with no newer durable GitHub implementation checkpoint than their dispatch bootstrap.
  - no Phase 2 live runtime observation has been authorized or performed by this coordinator session.
derived:
  - the CI failure is a shared governance/path-boundary defect, not a runtime-admission implementation defect.
  - the narrow repair belongs to the coordinator because the workflow is shared governance and is outside worker #826 owned_paths.
  - admitting only the exact OTC-20260901-vision-p2 task/report namespace preserves the Package A audit purpose while avoiding repeated identical blockers for the active Phase 2 programme.
unknown:
  - exact-head result of the coordinator repair PR until GitHub Actions runs it.
  - current Synology/Kasm target identity and availability for a future serialized read-only observation window.
conflicts: []
first_failure:
  marker: PACKAGE_A_CHANGED_PATHS_REJECT_PHASE2_DURABLE_DOCS
  evidence: PR 826 check Fresh Package A falsification audit at exact head 0dbd823f6c89895e919f9bc07f7e99ecac9f31a6 concluded FAILURE while CI / Required and the remaining observed Package A/Package B checks passed.
rejected_hypotheses:
  - runtime-admission implementation paths are outside the Package A boundary: rejected because tools/tibia_re_control_center/ and tests/tools/tibia_re_control_center/ are already allowed prefixes.
  - rerunning the same failed check without repository change can fix the issue: rejected because the failure is deterministic path classification.
  - worker 826 should edit the workflow itself: rejected because the workflow is outside its exact owned_paths and shared governance is coordinator-owned.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
validation:
  - command: inspect PR 826 exact-head check-runs
    result: RED
    evidence: Fresh Package A falsification audit failed on 0dbd823f6c89895e919f9bc07f7e99ecac9f31a6 while CI / Required passed.
  - command: inspect current .github/workflows/tibia-re-control-center-core.yml
    result: PASS_ROOT_CAUSE_IDENTIFIED
    evidence: internal allowed_exact/allowed_prefixes omit the Phase 2 worker task/report namespace.
blockers:
  - deterministic Package A changed-path boundary must be repaired and validated before PR 826 can be reclassified green.
next_action: repair the Package A changed-path audit so the exact Phase 2 programme task/report family is admitted without expanding runtime authority, then prove the repair on an exact-head coordinator PR.
```

## Wave 1 live ledger

| Alias | Draft PR | Current durable state | Coordinator classification |
|---|---:|---|---|
| `OTC-VISION-P2-RUNTIME-ADMISSION` | #826 | static implementation complete; waiting for CI repair and later serialized read-only observation | `RETURN_FOR_EVIDENCE` pending shared CI repair/live observation |
| `OTC-VISION-P2-CAPTURE-EDGE` | #827 | dispatch-ready on GitHub; no newer durable implementation checkpoint | pending |
| `OTC-VISION-P2-RUNTIME-SIGNALS` | #828 | dispatch-ready on GitHub; no newer durable implementation checkpoint | pending |
| `OTC-VISION-P2-EDGE-TRANSPORT` | #829 | dispatch-ready on GitHub; no newer durable implementation checkpoint | pending |
| `OTC-VISION-P2-CONTROL-BRIDGE` | #830 | dispatch-ready on GitHub; no newer durable implementation checkpoint | pending |

Actual official-runtime observation remains serialized to one worker and requires a fresh `read_only` admission before any live observation. All mutation, credentials, login/relogin, gameplay, GUI/anti-idle input, process control, process memory, network payload capture and physical actions remain forbidden with budget/count `0/0`.

## Historical coordinator milestones

- PR #824 merged Wave 0 lifecycle/ownership cleanup.
- PR #825 merged Wave 1 dispatch bootstrap.
- Wave 0 findings W0-AUDIT-001 through W0-AUDIT-003 were remediated before Wave 1 dispatch.
- Five Wave 1 worker branches/tasks/Draft PRs were created with non-overlapping ownership.
