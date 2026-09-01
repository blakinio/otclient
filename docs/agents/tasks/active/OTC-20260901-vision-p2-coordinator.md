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
phase: wave_1_post_ci_repair_reconcile
branch: docs/OTC-20260901-vision-p2-post833-reconcile
base_branch: main
base_main: 2917dc555e3c5fbd7a755c16f9b50a6c967e30d0
created: 2026-09-01T15:45:26+02:00
updated_at: 2026-09-01T18:23:00+02:00
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
worktree: C:/Users/barte/otclient-vision-p2-coordinator
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
reuses:
  - existing Phase 2 programme ownership contract
depends_on:
  - PR #820 merged foundation
  - PR #823 merged Phase 2 prompt-package closeout
  - PR #825 merged Wave 1 dispatch checkpoint
  - PR #831 merged Codex routing policy
  - PR #834 merged Codex routing policy closeout
related_prs:
  - PR #824 merged Wave 0 coordinator cleanup
  - PR #825 merged Wave 1 coordinator dispatch
  - PR #826 runtime-admission worker Draft
  - PR #827 capture-edge worker Draft
  - PR #828 runtime-signals worker Draft
  - PR #829 edge-transport worker Draft
  - PR #830 control-bridge worker Draft
  - PR #832 closed superseded coordinator repair Draft
  - PR #833 merged coordinator Package A repair
  - PR #835 closed duplicate coordinator continuation
current_blocker: WORKER_OWNED_REPAIR_AND_REVALIDATION_PENDING
next_action: monitor fresh worker generations: #826/#828 current-main revalidation, #827/#830 worker-owned repairs, and #829 publication; independently classify each new exact head without taking over dirty worker worktrees
invocation_started_at: 2026-09-01T17:47:00+02:00
last_progress_at: 2026-09-01T18:23:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: post833-reconcile
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

Coordinate Phase 2 read-only runtime-edge integration, independently classify workers, repair shared governance blockers, serialize any later real read-only observation, and drive the programme through exact-head integration/E2E closeout without entering Phase 3+.

## Binding authority

- `docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md`
- `docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md`
- `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`
- current Git/GitHub/runtime state and stricter trusted-base governance override stale historical prose.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T18:23:00+02:00
head: 2917dc555e3c5fbd7a755c16f9b50a6c967e30d0
branch: docs/OTC-20260901-vision-p2-post833-reconcile
pr: NOT_CREATED
status: waiting
context_routes:
  - phase-2-read-only-coordination
  - post-ci-repair-reconcile
  - worker-classification
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
proven:
  - PR #833 is merged; current trusted main is 2917dc555e3c5fbd7a755c16f9b50a6c967e30d0 and the bounded Phase 2 durable-doc Package A allowlist repair is now authoritative.
  - PR #826 static runtime-admission producer is coordinator-classified ACCEPT; real serialized read-only evidence remains required, and its clean worker branch must first restack/revalidate on current main.
  - PR #828 static runtime-signals producer is coordinator-classified ACCEPT; one-time rerun of its transient Package B failures completed SUCCESS; its clean tracked branch must restack/revalidate on current main.
  - PR #827 remains RETURN_FOR_REPAIR because caller-declared no_secret_fields can self-certify secret_safe without machine-checkable secret-free proof; no repair generation has been published yet.
  - PR #830 remains RETURN_FOR_REPAIR because caller-declared read_only/opaque refs do not validate #826 admission and #828 typed runtime-signal producers; BOM repair is already proven but integration repair is not published.
  - PR #829 has a separate locally dirty validating worker worktree with implementation/test/report changes not yet published; coordinator does not edit or take over that lane.
  - duplicate coordinator PR #835 was closed without merge after live reconciliation found the more advanced coordinator state in #833.
  - no Official Tibia/Kasm observation, credentials, GUI input, process control, process memory, payload capture or physical effect occurred; runtime_access remains none and physical action budget/count are 0/0.
derived:
  - the shared CI blocker is cleared; remaining Wave 1 blockers are worker-owned repair/revalidation/publication plus later serialized read-only evidence for #826.
  - old Package A failures on #826/#828/#830 are historical and cannot be treated as current-main validation; fresh exact-head runs are required after worker restacks.
unknown:
  - next published heads for #826/#827/#828/#829/#830 after current-main reconcile/repair.
  - current Synology/Kasm exact runtime identity for any later serialized read-only observation.
conflicts: []
first_failure:
  marker: none
  evidence: coordinator has no writable worker-owned repair to perform without violating branch/worktree ownership; safe work is live-state monitoring and independent classification.
rejected_hypotheses:
  - coordinator may repair #827/#830 directly in worker branches: rejected by one-worker-per-branch ownership and existing worker handoff contracts.
  - coordinator may take over #829 because remote PR is bootstrap-only: rejected by the live dirty validating worker worktree.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
validation:
  - command: PR #833 live readback
    result: PASS
    evidence: merged=true; merge commit/current main 2917dc555e3c5fbd7a755c16f9b50a6c967e30d0.
  - command: PR #828 Package B one-time rerun
    result: PASS
    evidence: workflow run 33530126482 now concludes success; code delta from previous Package-B-green head is zero.
  - command: worker worktree ownership reconciliation
    result: PASS
    evidence: #826/#830 tracked clean; #828 tracked clean aside from untracked pycache; #829 actively dirty/validating and left untouched.
blockers:
  - worker-owned repair/revalidation/publication generations are pending.
next_action: monitor fresh worker generations: #826/#828 current-main revalidation, #827/#830 worker-owned repairs, and #829 publication; independently classify each new exact head without taking over dirty worker worktrees.
```

## Wave 1 live ledger

| Alias | Draft PR | Current durable state | Coordinator classification |
|---|---:|---|---|
| `OTC-VISION-P2-RUNTIME-ADMISSION` | #826 | static producer accepted; current-main restack/revalidation pending; later serialized read-only observation required | `ACCEPT` static / `RETURN_FOR_EVIDENCE` live |
| `OTC-VISION-P2-CAPTURE-EDGE` | #827 | static implementation published; independent secret-safety finding open | `RETURN_FOR_REPAIR` |
| `OTC-VISION-P2-RUNTIME-SIGNALS` | #828 | static producer accepted; Package B rerun green; current-main restack/revalidation pending | `ACCEPT` static / revalidation pending |
| `OTC-VISION-P2-EDGE-TRANSPORT` | #829 | local worker implementation is validating but not yet published | pending worker publication/classification |
| `OTC-VISION-P2-CONTROL-BRIDGE` | #830 | BOM fixed; shared Package A repair is merged; missing validated #826/#828 producer binding remains open | `RETURN_FOR_REPAIR` |

Actual Official Tibia runtime observation remains serialized to one worker and requires a fresh persisted `read_only` admission before observation. Mutation, credentials, login/relogin, gameplay, GUI/anti-idle input, process control, process memory, network payload capture and physical actions remain forbidden with budget/count `0/0`.
