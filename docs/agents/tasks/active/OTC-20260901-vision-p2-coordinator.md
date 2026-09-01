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
phase: wave_1_dispatch_validation
branch: docs/OTC-20260901-vision-p2-coordinator-wave1
base_branch: main
base_main: 0fe1ecb3569f1d8372209c857ab57f3b626c29ae
created: 2026-09-01T15:45:26+02:00
updated_at: 2026-09-01T16:34:17+02:00
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
current_blocker: GITHUB_PR_HEAD_SYNC_PENDING
next_action: reconcile GitHub PR #826-#830 head metadata to the already-published final worker branch refs and verify exact-head required checks before dispatch
invocation_started_at: 2026-09-01T15:35:00+02:00
last_progress_at: 2026-09-01T16:34:17+02:00
ci_checks_for_current_head: 0
ci_check_generation: wave1-worker-pr-head-reconciliation
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
updated_at: 2026-09-01T16:34:17+02:00
head: 52d0134fe72a7fd8a42b82841fe9a9f03cca49ff
branch: docs/OTC-20260901-vision-p2-coordinator-wave1
pr: 825
status: validating
context_routes:
  - phase-2-read-only-coordination
  - autonomous-program
  - delivery-closeout
  - track-a-governance
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
proven:
  - PR 824 merged and refreshed main remains 0fe1ecb3569f1d8372209c857ab57f3b626c29ae.
  - five isolated Wave 1 worktrees/branches were created from exact refreshed main.
  - pairwise worker ownership scan returned WORKER_OVERLAPS={} and refreshed-main exact ownership scan returned MAIN_ACTIVE_EXACT_CONFLICTS=[].
  - all five bootstrap task records pass checkpoint validation, Track A runtime governance and git diff --check locally.
  - Draft PRs 826 through 830 exist and remain Draft.
  - OTC-VISION-P2-RUNTIME-ADMISSION: Draft PR 826, branch feat/OTC-20260901-vision-p2-runtime-admission, worktree C:/Users/barte/otclient-vision-p2-runtime-admission, remote branch head 2d2bb627965e0155e8f52210d1c8c6cab5610b53; current PR API head 751eda3b7bc0d790e35971f99f7c37b2d2520627 is stale and does not yet match.
  - OTC-VISION-P2-CAPTURE-EDGE: Draft PR 827, branch feat/OTC-20260901-vision-p2-capture-edge, worktree C:/Users/barte/otclient-vision-p2-capture-edge, remote branch head dd40d914fa5d05cdf5ff2957cc798ee7aa336d9b; current PR API head 9b98779ba8844c7b014d1ee62c3097831383729d is stale and does not yet match.
  - OTC-VISION-P2-RUNTIME-SIGNALS: Draft PR 828, branch feat/OTC-20260901-vision-p2-runtime-signals, worktree C:/Users/barte/otclient-vision-p2-runtime-signals, remote branch head 11fc18820cc22303d6857361eb3404f5f1844ffa; current PR API head 160f8d1d93e8f09a05c58cd2f3d0f388ac322035 is stale and does not yet match.
  - OTC-VISION-P2-EDGE-TRANSPORT: Draft PR 829, branch feat/OTC-20260901-vision-p2-edge-transport, worktree C:/Users/barte/otclient-vision-p2-edge-transport, remote branch head 2ba5a90629c2b3cab3094948bfa3a1fda2b1fb0b; current PR API head 2f79d907f3372f7c8215fb6f4e2034547038ecb8 is stale and does not yet match.
  - OTC-VISION-P2-CONTROL-BRIDGE: Draft PR 830, branch feat/OTC-20260901-vision-p2-control-bridge, worktree C:/Users/barte/otclient-vision-p2-control-bridge, remote branch head 7d5ccdb80aa523c3128bef0b8e4faef4450146fe; current PR API head 4cfc3a94fd4bff9a6548f9fce6cd185d8bccbaae is stale and does not yet match.
  - git ls-remote proves all five final PR-binding commits are published on their source branches.
  - runtime_access remains none for coordinator and all five workers; no real-runtime observation is authorized or claimed.
derived:
  - repository-side worker bootstrap is structurally complete, but worker dispatch is not yet valid until PR metadata points at each final branch head and fresh exact-head checks exist for that generation.
unknown:
  - exact convergence time/state of GitHub PR head metadata for PRs 826 through 830.
  - exact-head GitHub CI/governance results for the final PR-binding commits after PR metadata convergence.
conflicts:
  - Git remote branch refs are ahead of current GitHub pull-request REST head metadata for all five worker Draft PRs.
first_failure:
  marker: WAVE1-PR-HEAD-METADATA-STALE
  evidence: direct git ls-remote versus gh api pulls/{pr} head.sha comparison returned match=False for PRs 826-830 after successful pushes.
rejected_hypotheses:
  - worker binding commits were not pushed: rejected by git ls-remote exact refs.
  - workers overlap each other or current main ownership: rejected by pairwise and refreshed-main exact ownership scans.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
validation:
  - command: five worker checkpoint validators
    result: PASS
    evidence: every worker task checkpoint validates after PR binding edits.
  - command: five local Track A governance validations after binding commits
    result: PASS
    evidence: each lane reported TRACK_A_AGENT_RUNTIME_CHANGED_TASKS=1, BRANCH_BOUND_TASKS=1 and GOVERNANCE_PASS=true.
  - command: git ls-remote plus gh api PR head comparison
    result: FAIL
    evidence: five remote source refs are final binding commits but PR REST head.sha values still show first bootstrap commits.
blockers:
  - GITHUB_PR_HEAD_SYNC_PENDING for PRs 826-830.
next_action: reconcile GitHub PR #826-#830 head metadata to the already-published final worker branch refs and verify exact-head required checks before dispatch.
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

| Alias | Draft PR | Branch | Worktree | Published final branch head | Current PR API head at checkpoint |
|---|---:|---|---|---|---|
| `OTC-VISION-P2-RUNTIME-ADMISSION` | #826 | `feat/OTC-20260901-vision-p2-runtime-admission` | `C:/Users/barte/otclient-vision-p2-runtime-admission` | `2d2bb627965e0155e8f52210d1c8c6cab5610b53` | `751eda3b7bc0d790e35971f99f7c37b2d2520627` |
| `OTC-VISION-P2-CAPTURE-EDGE` | #827 | `feat/OTC-20260901-vision-p2-capture-edge` | `C:/Users/barte/otclient-vision-p2-capture-edge` | `dd40d914fa5d05cdf5ff2957cc798ee7aa336d9b` | `9b98779ba8844c7b014d1ee62c3097831383729d` |
| `OTC-VISION-P2-RUNTIME-SIGNALS` | #828 | `feat/OTC-20260901-vision-p2-runtime-signals` | `C:/Users/barte/otclient-vision-p2-runtime-signals` | `11fc18820cc22303d6857361eb3404f5f1844ffa` | `160f8d1d93e8f09a05c58cd2f3d0f388ac322035` |
| `OTC-VISION-P2-EDGE-TRANSPORT` | #829 | `feat/OTC-20260901-vision-p2-edge-transport` | `C:/Users/barte/otclient-vision-p2-edge-transport` | `2ba5a90629c2b3cab3094948bfa3a1fda2b1fb0b` | `2f79d907f3372f7c8215fb6f4e2034547038ecb8` |
| `OTC-VISION-P2-CONTROL-BRIDGE` | #830 | `feat/OTC-20260901-vision-p2-control-bridge` | `C:/Users/barte/otclient-vision-p2-control-bridge` | `7d5ccdb80aa523c3128bef0b8e4faef4450146fe` | `4cfc3a94fd4bff9a6548f9fce6cd185d8bccbaae` |

All five tasks are `status: ready`, `agent: unclaimed`, `runtime_access: none`. They are not dispatched while the PR-head mismatch above remains.
