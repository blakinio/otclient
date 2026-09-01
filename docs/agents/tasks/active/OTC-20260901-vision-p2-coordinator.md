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
updated_at: 2026-09-01T18:07:00+02:00
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
next_action: independently classify exact-head Draft PR #827 against the approved capture-edge contract, then persist ACCEPT/RETURN evidence without merging the worker
invocation_started_at: 2026-09-01T15:35:00+02:00
last_progress_at: 2026-09-01T18:07:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: wave1-dispatch-ready
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
updated_at: 2026-09-01T18:07:00+02:00
head: 2df0aa64c4578832f41acbf66339310c07724fb4
branch: docs/OTC-20260901-vision-p2-wave1-classification
pr: NOT_CREATED
status: implementing
context_routes:
  - phase-2-read-only-coordination
  - autonomous-program
  - delivery-closeout
  - track-a-governance
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
proven:
  - PR 824 merged and refreshed main is 0fe1ecb3569f1d8372209c857ab57f3b626c29ae.
  - five isolated Wave 1 branches/worktrees/tasks and Draft PRs 826-830 were created from exact refreshed main with pairwise and refreshed-main ownership overlap equal to zero.
  - each worker task is PR-bound, status ready, agent unclaimed, runtime_access none and all mutation/effect authorities false with physical action budget/count 0/0.
  - OTC-VISION-P2-RUNTIME-ADMISSION: Draft PR 826 is Draft/CLEAN and live PR head equals published branch head 2d2bb627965e0155e8f52210d1c8c6cab5610b53; CI / Required plus both Track A governance jobs are SUCCESS.
  - OTC-VISION-P2-CAPTURE-EDGE: Draft PR 827 is Draft/CLEAN and live PR head equals published branch head dd40d914fa5d05cdf5ff2957cc798ee7aa336d9b; CI / Required plus both Track A governance jobs are SUCCESS.
  - OTC-VISION-P2-RUNTIME-SIGNALS: Draft PR 828 is Draft/CLEAN and live PR head equals published branch head 11fc18820cc22303d6857361eb3404f5f1844ffa; CI / Required plus both Track A governance jobs are SUCCESS.
  - OTC-VISION-P2-EDGE-TRANSPORT: Draft PR 829 is Draft/CLEAN and live PR head equals published branch head 2ba5a90629c2b3cab3094948bfa3a1fda2b1fb0b; CI / Required plus both Track A governance jobs are SUCCESS.
  - OTC-VISION-P2-CONTROL-BRIDGE: Draft PR 830 is Draft/CLEAN and live PR head equals published branch head 7d5ccdb80aa523c3128bef0b8e4faef4450146fe; CI / Required plus both Track A governance jobs are SUCCESS.
  - the prior GitHub PR-head metadata lag is resolved for all five worker PRs.
  - local codex executable is absent on Molehill-PC; GitHub tools expose no Codex code-worker dispatch; plugin discovery found no executable Codex worker connector (Codex Security is a scanner, not a worker launcher).
derived:
  - repository/GitHub Wave 1 bootstrap is complete and all five workers are safe to start concurrently for repository/static work.
  - actual official-runtime observation remains serialized and is not authorized for any worker at this checkpoint.
unknown:
  - worker implementation, focused test, review, integration and later runtime-evidence outcomes.
conflicts: []
first_failure:
  marker: WORKER-EXECUTION-CHANNEL-UNAVAILABLE
  evidence: coordinator environment can prepare Git/GitHub/worktrees but cannot create the required separate Codex/agent execution sessions; codex CLI is not installed and available connectors/plugins do not expose a code-worker launcher.
rejected_hypotheses:
  - worker PR head metadata is still stale: rejected by live gh PR readback matching all five published remote branch refs.
  - worker bootstrap CI/governance is pending or failed: rejected by exact-head SUCCESS on CI / Required and both Track A governance jobs for PRs 826-830.
  - coordinator may silently implement all five worker lanes in one session: rejected by the binding multi-agent role/ownership/independent-review contract.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
validation:
  - command: pairwise worker plus refreshed-main exact ownership scan
    result: PASS
    evidence: WORKER_OVERLAPS={} and MAIN_ACTIVE_EXACT_CONFLICTS=[].
  - command: five worker PR live head and statusCheckRollup readback
    result: PASS
    evidence: PRs 826-830 each match final binding branch head, remain Draft/CLEAN, and exact-head required CI/governance are SUCCESS.
  - command: worker branch local governance/checkpoint/diff validation
    result: PASS
    evidence: all five workers passed branch-bound Track A governance, checkpoint schema and git diff --check after PR binding.
  - command: worker execution-channel discovery
    result: BLOCKED
    evidence: local codex not installed; no available connector/plugin provides separate Codex code-worker execution.
blockers:
  - separate Codex/agent worker sessions must be launched outside this coordinator session.
next_action: independently classify exact-head Draft PR #827 against the approved capture-edge contract, then persist ACCEPT/RETURN evidence without merging the worker.
```
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
