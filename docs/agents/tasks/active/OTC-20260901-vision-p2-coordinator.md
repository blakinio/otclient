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
phase: wave_1_classification
branch: docs/OTC-20260901-vision-p2-wave1-classification
base_branch: main
base_main: 2df0aa64c4578832f41acbf66339310c07724fb4
created: 2026-09-01T15:45:26+02:00
updated_at: 2026-09-01T18:14:25+02:00
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
related_prs:
  - PR #820 merged foundation integration
  - PR #823 merged Phase 2 prompt-package closeout
  - PR #824 merged Wave 0 coordinator cleanup
  - PR #825 Wave 1 coordinator ledger Draft
  - PR #826 runtime-admission worker Draft
  - PR #827 capture-edge worker Draft
  - PR #828 runtime-signals worker Draft
  - PR #829 edge-transport worker Draft
  - PR #830 control-bridge worker Draft
current_blocker: none
next_action: independently classify exact-head Draft PR #828 runtime-signals slice while preserving PR #829 as in-flight in its separate worker
invocation_started_at: 2026-09-01T15:35:00+02:00
last_progress_at: 2026-09-01T18:14:25+02:00
ci_checks_for_current_head: 0
ci_check_generation: wave1-classification
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---


# OTC Vision Phase 2 read-only programme coordinator

## Objective

Reconcile Phase 2 live state, release stale foundation ownership, create exact non-overlapping Wave 1 task/branch/Draft-PR assignments, independently classify worker outputs, integrate accepted slices, serialize real read-only observation, and drive the programme through fresh exact-head audit/E2E closeout without entering Phase 3+.

## Binding authority

- `docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md`
- `docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md`
- `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`
- live Git/GitHub/runtime state overrides stale historical task prose.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T18:14:25+02:00
head: 0dc44ab1d
branch: docs/OTC-20260901-vision-p2-wave1-classification
pr: 835
status: implementing
context_routes:
  - phase-2-read-only-coordination
  - autonomous-program
  - worker-classification
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
proven:
  - current main is 2df0aa64c4578832f41acbf66339310c07724fb4 and changes no capture-edge owned path.
  - PR 827 exact head cc957a25ddb4c40e1416bec60eff03c38fda3ad9 remains Draft, has four worker-owned changed files, zero review threads, and exact-head CI 33529427451 plus Track A governance 33529426895 SUCCESS.
  - independent coordinator execution of the exact-head capture suite passes 11/11; py_compile passes; AST audit finds shell=True count 0 and CaptureEvidence exposes only validated_vision_capture as public handoff.
  - independent diff review confirms pre/post/final runtime binding checks, pre/post geometry checks, in-memory secret masking before persistence, crop-to-full hash binding, content addressing and fixed read-only xdotool/ffmpeg command vocabulary.
  - PR 829 has uncommitted worker-owned implementation in its separate worktree and status validating, so coordinator does not edit or duplicate that lane.
derived:
  - PR 827 repository/static capture-edge slice is classified ACCEPT.
  - shared MODULE_CATALOG/CHANGELOG wiring and real admitted Linux/Synology/Kasm read-only E2E remain coordinator/integration obligations and are not worker defects.
unknown:
  - PR 828 runtime-signals coordinator classification.
  - PR 826 workflow-boundary remediation disposition, PR 829 published outcome, and PR 830 classification/integration outcome.
conflicts: []
first_failure:
  marker: none
  evidence: no current blocker for classifying completed worker slices; runtime_access remains none.
rejected_hypotheses:
  - capture-edge worker self-report is sufficient for acceptance: rejected; coordinator reran focused tests and independently reviewed exact diff/API surface.
  - coordinator may take over in-flight PR 829 implementation: rejected by live dirty validating worker worktree and one-worker-per-branch ownership.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
validation:
  - command: GitHub PR 827 exact-head workflow and review-thread readback
    result: PASS
    evidence: CI 33529427451 SUCCESS; Track A governance 33529426895 SUCCESS; zero review threads.
  - command: python -m unittest tests/tools/tibia_re_vision/test_capture_edge.py on cc957a25
    result: PASS
    evidence: 11 tests, zero failures/errors.
  - command: capture-edge AST/public-surface audit
    result: PASS
    evidence: shell=True=0; one subprocess.run boundary; CaptureEvidence public methods equal validated_vision_capture only.
blockers: []
next_action: independently classify exact-head Draft PR #828 runtime-signals slice while preserving PR #829 as in-flight in its separate worker.
```

## Wave 1 classification ledger

| Worker | PR | Coordinator classification | Evidence boundary |
|---|---:|---|---|
| `OTC-VISION-P2-CAPTURE-EDGE` | #827 | **ACCEPT** | Repository/static contract accepted at `cc957a25...`; no live-runtime success claimed; shared docs/integration and real read-only E2E remain coordinator-owned. |

## Planned Wave 1 ownership

This map is coordinator-owned dispatch intent and becomes write-capable only after PR #824 merges, refreshed-main overlap checks pass, and each worker has its own concrete task/branch/worktree/Draft PR. Shared indexes such as `docs/agents/MODULE_CATALOG.md` are excluded.

- `OTC-VISION-P2-RUNTIME-ADMISSION`: new `agent_runtime_admission.py`, its focused test, lane report/task.
- `OTC-VISION-P2-CAPTURE-EDGE`: new `tools/tibia_re_vision/capture_edge.py`, its focused test, lane report/task.
- `OTC-VISION-P2-RUNTIME-SIGNALS`: new `agent_runtime_signals.py`, its focused test, lane report/task.
- `OTC-VISION-P2-EDGE-TRANSPORT`: new `agent_edge_transport.py`, its focused test, lane report/task.
- `OTC-VISION-P2-CONTROL-BRIDGE`: exclusive integration ownership for a new edge bridge plus the existing session/domain/API/CLI/UI/MCP files and their focused tests; no other Wave 1 worker may edit those shared integration files.

Repository/static execution defaults to `github_hosted` with `runtime_access: none`. Actual official-runtime observation is separately admitted, read-only, mutation-disabled and serialized to one observation owner.

## Wave 0 audit findings

- `W0-AUDIT-001` — **material medium**, mandatory Track A admission fields absent from the coordinator task. Evidence: exact-head governance run `33517851944`, job `99889308745`, plus matching local RED. Impact: PR cannot satisfy Track A governance. Disposition: fixed with the canonical `runtime_access:none` admission record; local GREEN confirmed. Final verification: pending fresh exact-head CI.
- `W0-AUDIT-002` — **material medium**, UTF-8 mojibake in the archived foundation task caused by an intermediate Windows text round-trip. Evidence: PR diff exposed changed Unicode punctuation. Impact: historical archive integrity and readability. Disposition: rebuilt both archive files from exact `main` UTF-8 bytes plus only intended lifecycle edits; `MOJIBAKE_MATCHES=[]`, both archive checkpoint validators PASS. Final verification: pending fresh exact-head CI/diff.
- `W0-AUDIT-003` — **material medium**, duplicate `execution_class` keys in the coordinator frontmatter after admission remediation. Evidence: direct fresh task read showed both `github_coordination` and `github_hosted`. Impact: ambiguous machine-readable contract. Disposition: removed the duplicate and retained the routing-contract value `github_hosted`. Final verification: pending fresh exact-head CI/checkpoint validation.
## Wave 1 dispatch ledger

| Alias | Draft PR | Branch | Worktree | Final branch/PR head | Exact-head gates |
|---|---:|---|---|---|---|
| `OTC-VISION-P2-RUNTIME-ADMISSION` | #826 | `feat/OTC-20260901-vision-p2-runtime-admission` | `C:/Users/barte/otclient-vision-p2-runtime-admission` | `2d2bb627965e0155e8f52210d1c8c6cab5610b53` | CI Required + Track A governance: PASS |
| `OTC-VISION-P2-CAPTURE-EDGE` | #827 | `feat/OTC-20260901-vision-p2-capture-edge` | `C:/Users/barte/otclient-vision-p2-capture-edge` | `dd40d914fa5d05cdf5ff2957cc798ee7aa336d9b` | CI Required + Track A governance: PASS |
| `OTC-VISION-P2-RUNTIME-SIGNALS` | #828 | `feat/OTC-20260901-vision-p2-runtime-signals` | `C:/Users/barte/otclient-vision-p2-runtime-signals` | `11fc18820cc22303d6857361eb3404f5f1844ffa` | CI Required + Track A governance: PASS |
| `OTC-VISION-P2-EDGE-TRANSPORT` | #829 | `feat/OTC-20260901-vision-p2-edge-transport` | `C:/Users/barte/otclient-vision-p2-edge-transport` | `2ba5a90629c2b3cab3094948bfa3a1fda2b1fb0b` | CI Required + Track A governance: PASS |
| `OTC-VISION-P2-CONTROL-BRIDGE` | #830 | `feat/OTC-20260901-vision-p2-control-bridge` | `C:/Users/barte/otclient-vision-p2-control-bridge` | `7d5ccdb80aa523c3128bef0b8e4faef4450146fe` | CI Required + Track A governance: PASS |

All five tasks are `status: ready`, `agent: unclaimed`, `runtime_access: none`, and overlap-free. They are repository/GitHub dispatch-ready; the only remaining Wave 1 start dependency is creation of separate worker execution sessions.
