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
updated_at: 2026-09-01T18:27:00+02:00
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
  - PR #833 merged shared CI repair
  - PR #836 coordinator post-repair checkpoint
current_blocker: WAVE_1_WORKER_REPAIR_REVALIDATION_AND_EDGE_TRANSPORT_EXECUTION
next_action: consume the next durable worker handoff; require #826 and #828 to restack/revalidate on repaired trusted main, #827 to repair secret-safe self-certification, #830 to bind validated #826/#828 producer evidence, and #829 to execute its repository/static implementation before Wave 2
invocation_started_at: 2026-09-01T17:47:00+02:00
last_progress_at: 2026-09-01T18:27:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: post-ci-repair-pr-bound
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

Coordinate independently reviewed Wave 1 slices through current-main validation, then serialize any required read-only runtime observation and continue to Wave 2 reconciliation and final independent E2E/audit without entering Phase 3+.

## Binding authority

- `docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md`
- `docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md`
- `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`
- live Git/GitHub/runtime state and stricter trusted-base governance override stale historical prose.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T18:27:00+02:00
head: 43e927df67412ab9d04831f2bae88af979c665c5
head_semantics: post-repair ledger commit before PR-binding checkpoint
branch: docs/OTC-20260901-vision-p2-coordinator-post-ci-repair
pr: 836
status: waiting
context_routes:
  - phase-2-read-only-coordination
  - worker-classification
  - track-a-governance
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
proven:
  - PR 833 merged the bounded Package A durable-doc path repair as main 2917dc555e3c5fbd7a755c16f9b50a6c967e30d0 after exact-head Package A, Track A governance, self-hosted boundary and CI / Required success; final PR state was clean with zero review threads/reviews.
  - PR 826 head 0dbd823f6c89895e919f9bc07f7e99ecac9f31a6 is independently ACCEPTED as the static runtime-admission producer; real read-only acceptance remains RETURN_FOR_EVIDENCE and requires current-main revalidation before any observation window.
  - PR 828 checkpoint head 80a218fa00b4e50823efaffc6af5f9ba28329ce9 is independently ACCEPTED as a static runtime-signal producer and requires current-main revalidation before promotion.
  - PR 827 checkpoint head cc957a25ddb4c40e1416bec60eff03c38fda3ad9 still carries implementation 8685f7c6a8dae9e41d71f0acbe70a89a35a0ef38; coordinator RETURN_FOR_REPAIR finding 5496909848 requires eliminating unproven empty-policy self-certification of secret_safe.
  - PR 830 head fc684f62ab9b4e79e23fab58c6fda942b8b969be has its prior BOM fixed and Track A governance green; coordinator RETURN_FOR_REPAIR finding 5496928156 requires machine-valid #826 admission and #828 runtime-signal binding rather than caller-declared read_only/opaque refs.
  - PR 829 remains dispatch-only at 2ba5a90629c2b3cab3094948bfa3a1fda2b1fb0b with no implementation handoff.
  - PR 836 is the single-path durable coordinator checkpoint for this post-repair state.
  - no Official Tibia/Synology/Kasm live observation or mutation occurred; credentials/login/GUI input/process control/process memory/payload capture remain unused and physical action count is 0.
derived:
  - the old shared Package A failures are obsolete as a root cause but are not valid fresh pass evidence for worker heads; accepted workers must revalidate after restack onto repaired trusted main.
  - Wave 2 is blocked by the open #827/#830 material findings and missing #829 implementation.
  - no live observation window should be assigned before #826 is current-main validated and downstream repository/static integration is ready to consume admitted evidence safely.
unknown:
  - repair outcomes for #827 and #830.
  - implementation outcome for #829.
  - current Synology/Kasm target identity/availability; no Phase 2 live read-only admission exists yet.
conflicts: []
first_failure:
  marker: WAVE_1_NOT_INTEGRATION_READY
  evidence: #827 and #830 have open material coordinator findings and #829 has no implementation handoff.
rejected_hypotheses:
  - PR 833 merge automatically converts prior failed worker check generations to PASS: rejected because exact-head validation is generation-specific.
  - Wave 2 can start with only #826/#828 static producers: rejected by the programme acceptance/dependency graph.
  - live runtime evidence can compensate for unresolved repository/static trust-boundary findings: rejected by Phase 2 ordering and admission policy.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
validation:
  - command: PR 833 final exact-head workflows/check-runs and hygiene
    result: PASS
    evidence: Package A 33530806517, Track A governance 33530806667, self-hosted boundary 33530806658, CI 33530806879 and CI / Required 99933414435 all SUCCESS on ea8e8fd91f87d0b3caccc71cf9a71348b22d620a; mergeable_state clean, exact two-path diff, zero review threads/reviews.
  - command: squash merge PR 833 plus post-merge main readback
    result: PASS
    evidence: merge returned 2917dc555e3c5fbd7a755c16f9b50a6c967e30d0 and main resolves to that SHA.
  - command: post-merge worker PR 826-830 reconciliation
    result: PASS
    evidence: all five worker PRs remain Draft/open at the exact heads recorded above.
  - command: PR 836 diff inspection
    result: PASS_PENDING_EXACT_HEAD_CI
    evidence: one changed path only, the coordinator task ledger.
blockers:
  - PR 827 secret-safety repair and fresh evidence.
  - PR 830 validated producer binding repair and fresh evidence.
  - PR 829 repository/static edge-transport implementation and durable handoff.
  - PR 826 and PR 828 current-main restack/revalidation before promotion.
next_action: consume the next durable worker handoff; require #826 and #828 to restack/revalidate on repaired trusted main, #827 to repair secret-safe self-certification, #830 to bind validated #826/#828 producer evidence, and #829 to execute its repository/static implementation before Wave 2.
```

## Wave 1 live ledger

| Alias | Draft PR | Current head | Coordinator state |
|---|---:|---|---|
| `OTC-VISION-P2-RUNTIME-ADMISSION` | #826 | `0dbd823f6c89895e919f9bc07f7e99ecac9f31a6` | static `ACCEPT`; current-main revalidation + later live `RETURN_FOR_EVIDENCE` |
| `OTC-VISION-P2-CAPTURE-EDGE` | #827 | `cc957a25ddb4c40e1416bec60eff03c38fda3ad9` | `RETURN_FOR_REPAIR` secret-safety finding |
| `OTC-VISION-P2-RUNTIME-SIGNALS` | #828 | `80a218fa00b4e50823efaffc6af5f9ba28329ce9` | static `ACCEPT`; current-main revalidation required |
| `OTC-VISION-P2-EDGE-TRANSPORT` | #829 | `2ba5a90629c2b3cab3094948bfa3a1fda2b1fb0b` | no implementation handoff |
| `OTC-VISION-P2-CONTROL-BRIDGE` | #830 | `fc684f62ab9b4e79e23fab58c6fda942b8b969be` | `RETURN_FOR_REPAIR` validated-producer binding gap |

Official runtime observation remains unauthorized at this checkpoint. All Phase 2 mutation/effect authorities remain false and physical action budget/count remain `0/0`.
