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
phase: wave_1_benchmark_repair_and_final_validation
branch: docs/OTC-20260901-vision-p2-coordinator-benchmark-reconcile
base_branch: main
base_main: d1cb8722c3116a0e0aeb72b9b360712f43151f17
created: 2026-09-01T15:45:26+02:00
updated_at: 2026-09-01T22:54:41+02:00
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
current_blocker: CAPTURE_EDGE_BENCHMARK_REPAIR_AND_FINAL_WORKER_VALIDATION
next_action: consume #827 benchmark repair, #829 current-main exact-head CI, and #830 independent review; then independently classify/promote accepted repository-static slices before any live observation
invocation_started_at: 2026-09-01T17:47:00+02:00
last_progress_at: 2026-09-01T22:54:41+02:00
ci_checks_for_current_head: 0
ci_check_generation: coordinator-benchmark-reconcile
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
updated_at: 2026-09-01T22:54:41+02:00
head: d1cb8722c3116a0e0aeb72b9b360712f43151f17
head_semantics: trusted_main_at_benchmark_reconciliation_before_coordinator_checkpoint_commit
branch: docs/OTC-20260901-vision-p2-coordinator-benchmark-reconcile
pr: PENDING
status: implementing
context_routes:
  - phase-2-read-only-coordination
  - worker-classification
  - benchmark-adjudication
  - track-a-governance
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
proven:
  - trusted main is d1cb8722c3116a0e0aeb72b9b360712f43151f17; it includes runtime-admission promotion #838, runtime-signals promotion #839, benchmark record #841 and benchmark archive #842.
  - runtime-admission and runtime-signals repository/static producers are merged; neither merge authorizes live Official Tibia observation.
  - benchmark evidence on capture-edge target 53b6a7e515c0cd6820857f7910368cdbb0e1978d mechanically reproduced a forgeable public CaptureEvidence path and post-capture freshness timestamp flaw; the publicly constructible ReviewedSecretMaskPolicy remains a trust-boundary concern.
  - promotion #840 carried identical capture_edge.py blob d53cd108c47c5cb9042c173c101d17c945f1b2a7 and test blob 2749a27957d4fdb684110790a07ea3b861c457cf to the benchmark target, so those later findings were not repaired by the promotion generation.
  - coordinator closed #840 without merge, reopened Draft #827, and restored capture-edge classification to RETURN_FOR_REPAIR; a separate Terra/high repair worker is active on the existing #827 lane.
  - #829 now contains the authenticated bounded edge-transport implementation rather than dispatch-only scaffolding; previous exact-head generation obtained green CI, Package A, Package B and Track A after its portability repair, and a separate Terra/medium worker is finalizing a current-main generation.
  - #830 head 97238d35192b4a79e66cd9b58eccb20957568be8 reports the validated-admission/runtime-signal repair and exact-head CI/Package A/Package B/Track A success; coordinator has started an independent read-only Sol/medium review before classification.
  - no Official Tibia/Synology/Kasm live observation, credentials, login, GUI input, process control, process memory, payload capture or physical action occurred; runtime_access remains none and physical action count/budget remain 0/0.
derived:
  - the earlier coordinator ACCEPT for #827 is superseded by later stronger benchmark evidence and cannot support promotion.
  - #829 is no longer an implementation-missing blocker; its remaining gate is exact current-main generation evidence and coordinator classification.
  - #830 must not be promoted solely from its worker self-report; independent coordinator review and fresh-main handling remain required.
  - Wave 2 and all live read-only observation remain blocked while #827 has open material repository/static safety findings.
unknown:
  - final repaired exact head and exact-head checks for #827.
  - final current-main exact head/check outcome and coordinator classification for #829.
  - independent coordinator review disposition and required current-main restack for #830.
conflicts: []
first_failure:
  marker: CAPTURE_EDGE_BENCHMARK_FINDINGS_UNREPAIRED_IN_PROMOTION
  evidence: promotion #840 implementation/test blobs are identical to the benchmarked vulnerable generation despite later mechanically reproduced material findings.
rejected_hypotheses:
  - #840 can safely promote because #827 had an earlier ACCEPT: rejected; the ACCEPT predates stronger benchmark evidence.
  - #829 remains dispatch-only: rejected by live branch/PR implementation, focused tests and hosted checks.
  - #830 worker-declared PRODUCER_COMPLETE is sufficient for coordinator ACCEPT: rejected; independent coordinator review is mandatory.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
validation:
  - command: live git/gh reconciliation of main and PRs #827/#829/#830/#840
    result: PASS
    evidence: #840 closed unmerged; #827 reopened Draft; #829 and #830 remain Draft/open; live heads captured in the ledger below.
  - command: capture-edge blob identity comparison between benchmark target and #840 promotion head
    result: PASS
    evidence: implementation and focused-test blob ids are identical, proving benchmark findings were not repaired in #840.
blockers:
  - #827 must repair benchmark-confirmed forged-evidence and freshness findings and resolve reviewed-policy issuance trust before promotion.
  - #829 must complete one coherent current-main exact-head validation generation and return for classification.
  - #830 must complete independent coordinator review and any resulting current-main restack/repair before promotion.
next_action: consume #827 repair, #829 exact-head CI, and #830 independent review; then independently classify/promote accepted repository-static slices before any live observation.
```

## Wave 1 live ledger

| Alias | PR | Current head / integration | Coordinator state |
|---|---:|---|---|
| `OTC-VISION-P2-RUNTIME-ADMISSION` | #838 promotion | merged `fb0c489f2ed166e872c4f197c6a78375a8576685` | repository/static producer `ACCEPT`; later serialized live evidence still required |
| `OTC-VISION-P2-CAPTURE-EDGE` | #827 Draft | `b4a2664778d001344e3d0fdbd19ff4c9ac118e18` at dispatch | `RETURN_FOR_REPAIR`; #840 closed unmerged; Terra/high repair active |
| `OTC-VISION-P2-RUNTIME-SIGNALS` | #839 promotion | merged `e883543403d5430d7b1d287f59043b23c98f37d6` | repository/static producer `ACCEPT` |
| `OTC-VISION-P2-EDGE-TRANSPORT` | #829 Draft | current-main validation generation actively moving from `fe258ecdb65cbc6802b54d2adff57ecb4357865a` | implementation present; Terra/medium exact-head finalization active |
| `OTC-VISION-P2-CONTROL-BRIDGE` | #830 Draft | `97238d35192b4a79e66cd9b58eccb20957568be8` | worker `PRODUCER_COMPLETE`; independent Sol/medium coordinator review active |

Official runtime observation remains unauthorized at this checkpoint. All Phase 2 mutation/effect authorities remain false and physical action budget/count remain `0/0`.
