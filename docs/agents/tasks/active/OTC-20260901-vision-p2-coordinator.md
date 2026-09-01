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
phase: wave_0_audit_remediation
branch: docs/OTC-20260901-vision-p2-coordinator
base_branch: main
base_main: 21fedc04809f0f78a1ff673edb2804a83ab5fedb
created: 2026-09-01T15:45:26+02:00
updated_at: 2026-09-01T16:15:20+02:00
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
  - docs/agents/tasks/archive/OTC-20260830-local-vision-agent-supervisor-discovery.md
  - docs/agents/tasks/archive/OTC-20260830-local-vision-agent-supervisor-foundation.md
depends_on:
  - PR #820 merged foundation
  - PR #823 merged Phase 2 prompt-package closeout
related_prs:
  - PR #808 closed historical discovery Draft; superseded after #820
  - PR #810 closed historical foundation Draft; superseded after #820
  - PR #820 merged foundation integration
  - PR #824 Wave 0 coordinator cleanup Draft
current_blocker: none
next_action: publish the Wave 0 audit remediation, run fresh exact-head governance/CI and PR-hygiene checks, then merge PR #824 only if every gate passes
invocation_started_at: 2026-09-01T15:35:00+02:00
last_progress_at: 2026-09-01T16:15:20+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
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
updated_at: 2026-09-01T16:15:20+02:00
head: 7145e17b6b8fdbf5b88a4ed9cbc9ec75326bbde3
branch: docs/OTC-20260901-vision-p2-coordinator
pr: 824
status: validating
context_routes:
  - phase-2-read-only-coordination
  - autonomous-program
  - delivery-closeout
  - track-a-governance
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
  - docs/agents/tasks/archive/OTC-20260830-local-vision-agent-supervisor-discovery.md
  - docs/agents/tasks/archive/OTC-20260830-local-vision-agent-supervisor-foundation.md
proven:
  - PR 820 is merged; historical Draft PRs 808 and 810 are closed and their stale active task records are archived with ownership released.
  - coordinator Draft PR 824 remains limited to three task-lifecycle files and changes no product/runtime implementation.
  - current Track A trusted-base contracts were refreshed; current exact-client fence is 15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a.
  - the older 52109920 / ed5469... parallel-research fence is superseded by the 2026-08-28 canonical advance recorded in CHANGELOG / PR 754 and is not Phase 2 identity authority.
  - exact head 313415e124941cac4c07599d6d4c94acadb950a1 passed general CI but failed Track A governance run 33517851944 job 99889308745 solely because the coordinator task omitted ten mandatory runtime_access=none admission fields.
  - the governance failure was reproduced locally, the ten fields were added using the repository working pattern, and the same validator now passes locally.
  - proportional diff audit found UTF-8 mojibake in the foundation archive introduced by a Windows text round-trip; both archives were reconstructed from exact main bytes plus only intended lifecycle changes and now contain no mojibake markers.
  - active coordinator plus both terminal archive checkpoints pass tools/agents/checkpoint.py --require-checkpoint after remediation.
  - no active task claims tools/tibia_re_control_center/** or tools/tibia_re_vision/** after the archive cleanup; shared MODULE_CATALOG.md remains excluded.
derived:
  - Wave 1 can use disjoint lane-local modules only after PR 824 merges and refreshed-main overlap checks repeat.
unknown:
  - fresh exact-head GitHub governance/CI outcome and final review-thread/PR-hygiene state after this audit-remediation commit is published.
conflicts: []
first_failure:
  marker: FINAL-EXACT-HEAD-GATES-PENDING
  evidence: local RED-to-GREEN and archive-integrity remediation pass, but the remediated exact head has not yet run required GitHub checks.
rejected_hypotheses:
  - direct Codex CLI dispatch is available on Molehill-PC: codex executable is not installed on the connected host.
  - the older 52109920 / ed5469... fence is current Phase 2 identity authority: superseded by current mandatory contracts and PR 754/CHANGELOG evidence.
  - the exact-head governance failure was caused by runtime state: rejected; CI log and local reproduction isolate it to missing task admission fields.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-coordinator.md
  - docs/agents/tasks/archive/OTC-20260830-local-vision-agent-supervisor-discovery.md
  - docs/agents/tasks/archive/OTC-20260830-local-vision-agent-supervisor-foundation.md
validation:
  - command: GitHub Actions exact head 313415e124941cac4c07599d6d4c94acadb950a1
    result: FAIL
    evidence: CI success; Track A governance failure run 33517851944 job 99889308745 identified W0-AUDIT-001.
  - command: python .github/scripts/test_track_a_agent_runtime_governance.py --changed-from 21fedc04809f0f78a1ff673edb2804a83ab5fedb --expected-branch docs/OTC-20260901-vision-p2-coordinator
    result: PASS
    evidence: TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true after W0-AUDIT-001 remediation.
  - command: terminal archive byte reconstruction and mojibake scan
    result: PASS
    evidence: source bytes decoded strict UTF-8 from main; MOJIBAKE_MATCHES=[] after W0-AUDIT-002 remediation.
  - command: tools/agents/checkpoint.py --require-checkpoint for coordinator and both archived tasks
    result: PASS
    evidence: all three current checkpoint records validate.
  - command: git diff --check
    result: PASS
    evidence: no whitespace errors in the remediated Wave 0 lifecycle delta.
blockers: []
next_action: publish the Wave 0 audit remediation, run fresh exact-head governance/CI and PR-hygiene checks, then merge PR #824 only if every gate passes.
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
