---
task_id: OTC-20260901-vision-p2-coordinator
status: validating
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
updated_at: 2026-09-01T17:58:00+02:00
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
  - PR #832 coordinator Package A path-boundary repair Draft
current_blocker: PR_832_EXACT_HEAD_VALIDATION_PENDING
next_action: inspect PR #832 full diff and exact-head required checks once; if clean and green, complete proportional audit, mark ready and squash-merge the shared CI repair before refreshing PR #826
invocation_started_at: 2026-09-01T17:47:00+02:00
last_progress_at: 2026-09-01T17:58:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: ci-repair-draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
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
updated_at: 2026-09-01T17:58:00+02:00
head: caec10f85839f0304743e64c6d767cace8473ed9
head_semantics: workflow_repair_commit_before_checkpoint_docs
branch: ci/OTC-20260901-vision-p2-package-a-path-boundary
pr: 832
status: validating
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
  - the Package A audit computes the complete PR changed-path set and previously allowed control-center/vision code prefixes but not Phase 2 worker task/report documentation.
  - PR 826 mandatory durable documentation paths are under docs/agents/tasks/active/OTC-20260901-vision-p2-* and docs/agents/reports/OTC-20260901-vision-p2-*.
  - the same missing programme-documentation boundary would recur for later Wave 1 lanes when their task/report files accompany Control Center or vision implementation.
  - coordinator-owned repair commit caec10f85839f0304743e64c6d767cace8473ed9 adds only the bounded active-task, archive-task and report prefixes for the OTC-20260901-vision-p2 programme family to the existing Package A changed-path allowlist.
  - Draft PR 832 targets main from the dedicated coordinator CI repair branch and contains only the workflow plus coordinator task record.
  - PRs 827-830 remain open Drafts with no newer durable GitHub implementation checkpoint than their dispatch bootstrap.
  - no Phase 2 live runtime observation has been authorized or performed by this coordinator session.
derived:
  - the CI failure is a shared governance/path-boundary defect, not a runtime-admission implementation defect.
  - the narrow repair belongs to the coordinator because the workflow is shared governance and outside worker #826 owned_paths.
  - the programme-scoped prefixes preserve the audit's fail-closed boundary while preventing identical deterministic failures for current Phase 2 durable artifacts.
unknown:
  - exact final PR 832 head after this checkpoint commit and its GitHub Actions results.
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
  - .github/workflows/tibia-re-control-center-core.yml
validation:
  - command: inspect PR 826 exact-head check-runs
    result: RED
    evidence: Fresh Package A falsification audit failed on 0dbd823f6c89895e919f9bc07f7e99ecac9f31a6 while CI / Required passed.
  - command: inspect current .github/workflows/tibia-re-control-center-core.yml
    result: PASS_ROOT_CAUSE_IDENTIFIED
    evidence: internal allowed_exact/allowed_prefixes omitted the Phase 2 worker task/report namespace.
  - command: bounded workflow repair construction
    result: PENDING_EXACT_HEAD_CI
    evidence: repair commit caec10f85839f0304743e64c6d767cace8473ed9 adds only three programme-scoped documentation prefixes.
blockers:
  - PR 832 exact-head diff/audit/CI must pass before the repair can merge and unblock PR 826.
next_action: inspect PR #832 full diff and exact-head required checks once; if clean and green, complete proportional audit, mark ready and squash-merge the shared CI repair before refreshing PR #826.
```

## Wave 1 live ledger

| Alias | Draft PR | Current durable state | Coordinator classification |
|---|---:|---|---|
| `OTC-VISION-P2-RUNTIME-ADMISSION` | #826 | static implementation complete; waiting for shared CI repair and later serialized read-only observation | `RETURN_FOR_EVIDENCE` pending shared CI repair/live observation |
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
