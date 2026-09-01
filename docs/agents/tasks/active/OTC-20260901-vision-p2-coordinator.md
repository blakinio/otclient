---
task_id: OTC-20260901-vision-p2-coordinator
status: waiting
agent: ChatGPT
session_role: programme_coordinator
worker_alias: OTC-VISION-P2-COORDINATOR
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: coordination
phase: wave_1_worker_repair_and_revalidation
branch: docs/OTC-20260901-vision-p2-coordinator-post-ci-repair
base_branch: main
base_main: 2917dc555e3c5fbd7a755c16f9b50a6c967e30d0
created: 2026-09-01T15:45:26+02:00
updated_at: 2026-09-01T18:24:00+02:00
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
modules_touched:
  - phase_2_coordination_ledger
reuses:
  - merged Package A path-boundary repair PR #833
depends_on:
  - PR #820 merged foundation
  - PR #823 merged Phase 2 prompt-package closeout
  - PR #825 merged Wave 1 dispatch checkpoint
  - PR #833 merged Package A path-boundary repair
blocks:
  - Wave 2 reconciliation
related_prs:
  - PR #826 runtime-admission worker Draft
  - PR #827 capture-edge worker Draft
  - PR #828 runtime-signals worker Draft
  - PR #829 edge-transport worker Draft
  - PR #830 control-bridge worker Draft
  - PR #833 merged Package A path-boundary repair
current_blocker: WAVE_1_WORKER_REPAIR_REVALIDATION_AND_EDGE_TRANSPORT_EXECUTION
next_action: consume the next durable worker handoff; require #826 and #828 to restack/revalidate on repaired main, #827 to repair secret-safe self-certification, #830 to bind validated #826/#828 producer evidence, and #829 to execute its repository/static implementation before Wave 2
invocation_started_at: 2026-09-01T17:47:00+02:00
last_progress_at: 2026-09-01T18:24:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: post-ci-repair-checkpoint
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
context_reconstruction_attempts: 1
stall_warnings: 0
---

# OTC Vision Phase 2 read-only programme coordinator

## Objective

Coordinate the Phase 2 read-only runtime-edge programme through independently reviewed Wave 1 slices, serialized read-only runtime evidence, Wave 2 reconciliation and final independent E2E/audit without entering Phase 3+.

## Binding authority

- `docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md`
- `docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md`
- `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`
- live Git/GitHub/runtime state and stricter trusted-base governance override stale historical prose.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T18:24:00+02:00
head: 2917dc555e3c5fbd7a755c16f9b50a6c967e30d0
head_semantics: trusted_main_after_merged_shared_ci_repair_before_this_checkpoint_commit
branch: docs/OTC-20260901-vision-p2-coordinator-post-ci-repair
pr: NOT_OPEN_YET
status: waiting
context_routes:
  - phase-2-read-only-coordination
  - worker-classification
  - track-a-governance
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
proven:
  - shared Package A path-boundary repair PR 833 merged successfully as 2917dc555e3c5fbd7a755c16f9b50a6c967e30d0 after exact-head Package A, Track A governance, self-hosted boundary and CI / Required all passed on ea8e8fd91f87d0b3caccc71cf9a71348b22d620a; PR was mergeable_state clean with zero review threads/reviews and exactly two changed paths.
  - main readback after merge is exactly 2917dc555e3c5fbd7a755c16f9b50a6c967e30d0.
  - PR 826 current head remains 0dbd823f6c89895e919f9bc07f7e99ecac9f31a6. Coordinator independent review found no material static admission-producer defect; classification is ACCEPT for the static producer and RETURN_FOR_EVIDENCE for the required later real read-only observation. Comment 5496990233 records the decision.
  - PR 828 current checkpoint head is 80a218fa00b4e50823efaffc6af5f9ba28329ce9 with implementation-validation head 426a9aaf15c440531fb9d0bc315f382bf5465ea0. Coordinator independently ACCEPTED the standalone static runtime-signal producer contract in comment 5496967667; it still requires current-main restack/revalidation before promotion.
  - PR 827 current checkpoint head is cc957a25ddb4c40e1416bec60eff03c38fda3ad9 and implementation head remains 8685f7c6a8dae9e41d71f0acbe70a89a35a0ef38. Coordinator found a material secret-safety defect: an unproven empty secret policy can persist unmasked bytes and self-certify secret_safe. RETURN_FOR_REPAIR is recorded in comment 5496909848.
  - PR 830 current head is fc684f62ab9b4e79e23fab58c6fda942b8b969be. The UTF-8 BOM governance defect is fixed and Track A governance passes. Coordinator found a separate material integration defect: caller-declared read_only and opaque runtime refs are accepted without consuming machine-validated #826 admission and #828 runtime-signal producer evidence. RETURN_FOR_REPAIR is recorded in comment 5496928156.
  - PR 829 remains dispatch-only at 2ba5a90629c2b3cab3094948bfa3a1fda2b1fb0b with one changed task file and no implementation handoff.
  - no Official Tibia/Synology/Kasm live observation, credentials, GUI input, process control, process memory access, network payload capture or physical action occurred in this coordinator invocation.
derived:
  - the shared Package A blocker is removed from trusted main, but old exact-head worker failures are not retroactively green; worker branches require fresh validation after restack/rebase.
  - Wave 2 cannot start because capture edge and control bridge have open material findings and edge transport is not implemented.
  - a live observation window should not be assigned yet: #826 first needs current-main revalidation, and downstream consumers are not yet accepted/integrated.
unknown:
  - outcomes of #827 and #830 repair rounds.
  - whether the external #829 worker session will publish implementation without a new owner invocation.
  - current Synology/Kasm target identity and availability; no live read-only admission exists for Phase 2 yet.
conflicts: []
first_failure:
  marker: WAVE_1_NOT_INTEGRATION_READY
  evidence: #827 and #830 have open material coordinator findings and #829 has no implementation handoff.
rejected_hypotheses:
  - merging PR 833 automatically clears old failed worker check generations: rejected because exact-head evidence remains generation-specific.
  - Wave 2 may begin using only #826/#828 accepted producer contracts: rejected because programme requires accepted capture, runtime-signal and Control Center integration contracts plus sufficient edge transport.
  - live runtime observation should be used to compensate for missing repository/static integration: rejected by programme ordering and read-only admission policy.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
validation:
  - command: PR 833 final exact-head workflow and check-run readback
    result: PASS
    evidence: Package A 33530806517, CI 33530806879 with CI / Required 99933414435, Track A governance 33530806667 and self-hosted boundary 33530806658 all SUCCESS on ea8e8fd91f87d0b3caccc71cf9a71348b22d620a.
  - command: PR 833 final hygiene/live-main readback
    result: PASS
    evidence: mergeable_state clean; zero review threads/reviews; exact two-path diff; base/main 2df0aa64c4578832f41acbf66339310c07724fb4 unchanged before merge.
  - command: squash merge PR 833 and post-merge main readback
    result: PASS
    evidence: merge API returned merged=true sha 2917dc555e3c5fbd7a755c16f9b50a6c967e30d0 and branch main resolves to that SHA.
  - command: worker PR 826-830 live reconciliation after PR 833 merge
    result: PASS
    evidence: #826 0dbd823f..., #827 cc957a25..., #828 80a218fa..., #829 2ba5a906..., #830 fc684f62...; all remain Draft/open.
blockers:
  - PR 827 must repair the material secret-safety finding and return fresh exact-head evidence.
  - PR 830 must integrate machine-validated #826 admission and #828 runtime-signal producer contracts and return fresh exact-head evidence.
  - PR 829 must execute its repository/static edge-transport implementation and return a durable handoff.
  - PR 826 and PR 828 must restack/revalidate on repaired current main before promotion.
next_action: consume the next durable worker handoff; require #826 and #828 to restack/revalidate on repaired main, #827 to repair secret-safe self-certification, #830 to bind validated #826/#828 producer evidence, and #829 to execute its repository/static implementation before Wave 2.
```

## Wave 1 live ledger

| Alias | Draft PR | Current head | Coordinator state |
|---|---:|---|---|
| `OTC-VISION-P2-RUNTIME-ADMISSION` | #826 | `0dbd823f6c89895e919f9bc07f7e99ecac9f31a6` | static `ACCEPT`; current-main revalidation + later `RETURN_FOR_EVIDENCE` live gate |
| `OTC-VISION-P2-CAPTURE-EDGE` | #827 | `cc957a25ddb4c40e1416bec60eff03c38fda3ad9` | `RETURN_FOR_REPAIR` secret-safety finding |
| `OTC-VISION-P2-RUNTIME-SIGNALS` | #828 | `80a218fa00b4e50823efaffc6af5f9ba28329ce9` | static `ACCEPT`; current-main revalidation required |
| `OTC-VISION-P2-EDGE-TRANSPORT` | #829 | `2ba5a90629c2b3cab3094948bfa3a1fda2b1fb0b` | no implementation handoff |
| `OTC-VISION-P2-CONTROL-BRIDGE` | #830 | `fc684f62ab9b4e79e23fab58c6fda942b8b969be` | `RETURN_FOR_REPAIR` validated-producer binding gap |

Actual Official Tibia runtime observation remains unauthorized at this checkpoint. All Phase 2 mutation/effect authorities remain false and physical action budget/count remain `0/0`.
