---
task_id: OTC-20260816-track-a-lane-alias-prompts
status: active
agent: ChatGPT
session_id: chatgpt-20260816-1227-track-a-alias-prompts
session_role: prompt-implementer
session_rotation_count: 0
project_lane: otclient
lane: track-a-governance
track_id: official-client-re
task_kind: documentation
phase: implementation
branch: docs/OTC-20260816-track-a-lane-alias-prompts
base_branch: main
base_main: 2c56f7f2c7c01d8dbc1b66febeea22b1d4aff6e8
risk: medium
related_pr: null
created: 2026-08-16T12:27:00+02:00
updated: 2026-08-16T12:27:00+02:00
lease_expires_at: 2026-08-16T13:12:00+02:00
lease_released_at: null
owned_paths:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_COORDINATOR_ALIAS.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_P2_NETWORK_ALIAS.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_P0_STATE_ALIAS.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_P1_BRIDGE_ALIAS.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_RUNTIME_ALIAS.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_COVERAGE_AUDIT_ALIAS.md
  - docs/agents/tasks/active/OTC-20260816-track-a-lane-alias-prompts.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-lane-alias-prompts.md
modules_touched:
  - agent-prompting
reuses:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_RESEARCH_COORDINATION.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
depends_on:
  - main@2c56f7f2c7c01d8dbc1b66febeea22b1d4aff6e8
  - PR #343 merged persistent-session/hybrid routing as 54e7aa8ce2994238067d39b37d3d807bc10111d3
  - PR #324/#329 merged and archived Track A runtime-agent admission governance
  - PR #303 runtime-owned surfaces remain separately owned and must not be touched
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: alias-prompt documentation only; no live runtime access is needed
run_scope: single_task
continuation_policy: protected_merge_then_archive
task_completion_policy: protected_merge_then_archive
user_communication: milestone_only
implementation_authorized: true
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
runtime_access: none
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
prompt_contract:
  version: 1.0.0
  changed_surfaces:
    - Track A coordinator alias
    - P2-NETWORK alias
    - P0-STATE alias
    - P1-BRIDGE alias
    - RUNTIME alias
    - COVERAGE-AUDIT alias
    - persistent Synology desktop/VNC/session routing preset
  objective: Provide short repository-resolved aliases for all Track A research roles while making one persistent Synology desktop, owner-visible VNC and one reusable canonical client session the RUNTIME default topology without weakening admission gates.
  baseline_version: OTCLIENT-TIBIA-RE canonical 1.2.0 + hybrid routing 1.0.0 + parallel coordination 1.0.0 on main
  eval_suite: manual scenario matrix in this task record
  rollback_version: remove the six alias wrappers
last_progress_at: 2026-08-16T12:27:00+02:00
last_completed_step: claimed prompt-only paths after verifying current main, active tasks and open PRs; no overlapping owner exists for the six new alias paths
next_action: add six additive alias wrappers, run deterministic content audit plus documented manual prompt-eval matrix, open Draft PR, validate exact-head CI/review, protected-merge and archive
---

# Track A lane alias prompts

## Goal

Add short invocation aliases for the Track A promotion coordinator and all five research lanes. The aliases must resolve through current repository state and the existing canonical/hybrid/admission contracts instead of duplicating a second programme prompt.

The RUNTIME alias must encode the owner's desired operational topology on Synology: one long-lived canonical X11 desktop, one stable owner-observable VNC view bound to that desktop, and one reusable canonical exact-client session whose lifecycle is independent from an individual worker or GitHub Actions job. A new worker must prefer safe re-acquisition/reuse rather than rebuilding the login/session from zero.

## Acceptance inventory

- [ ] `OTCLIENT-TIBIA-RE-COORD` resolves to coordinator/promotion authority and does not directly take physical runtime ownership.
- [ ] `OTCLIENT-TIBIA-RE-P2` resolves to P2-NETWORK, GitHub-hosted by default, Draft-only, consuming RUNTIME evidence when physical proof is required.
- [ ] `OTCLIENT-TIBIA-RE-P0` resolves to P0-STATE, GitHub-hosted by default, and does not create a second logged-in session for semantic validation.
- [ ] `OTCLIENT-TIBIA-RE-P1` resolves to P1-BRIDGE, GitHub-hosted by default, and delegates physical reacquisition/restart proof to RUNTIME.
- [ ] `OTCLIENT-TIBIA-RE-RUNTIME` resolves to Synology physical runtime ownership and requires runtime admission on every claim/resume.
- [ ] RUNTIME preserves/reuses one persistent desktop + VNC + canonical client/session across worker/job rotations when current authority/identity gates permit it.
- [ ] RUNTIME never treats historical `:98`, `6082`, PID/session as current authority and never hard-codes them as canonical.
- [ ] RUNTIME does not routinely logout, kill X11/VNC/client, or rebuild login state at task end; it releases controller authority while preserving the programme runtime unless a reviewed recovery/destructive action explicitly requires otherwise.
- [ ] VNC availability gives the owner stable visibility but never grants an agent mutation authority; VNC credentials/endpoints are not committed as secrets or guessed from historical values.
- [ ] `OTCLIENT-TIBIA-RE-AUDIT` resolves to COVERAGE-AUDIT and remains GitHub-hosted/no-runtime.
- [ ] All researcher aliases remain Draft-only; only coordinator may promote/integrate under the current parallel coordination contract.
- [ ] All aliases preserve exact native-Linux client fence, admission classes, Gate A/rebind/Gate B/bootstrap separation, PR #303 ownership, Track B isolation and owner-funded AI prohibition.
- [ ] Documentation E2E is `NOT_APPLICABLE_WITH_REASON`; exact path/content/diff review, manual prompt eval and repository CI are required before merge.

## Manual prompt-eval matrix

| Case | Expected alias behavior | Status |
|---|---|---|
| Coordinator dispatches static P2 work | P2 gets GitHub-hosted + `runtime_access: none`; no Synology session takeover | PENDING |
| P0 needs one causal real-client read | Consume/request bounded RUNTIME evidence; do not create another logged-in session | PENDING |
| P1 needs restart/reacquisition proof | Hosted implementation remains separate; RUNTIME supplies serialized physical proof | PENDING |
| RUNTIME starts and a current authoritative registered session is healthy | Acquire current authority, rebind if required, Gate B, reuse same desktop/client/session; no fresh login/bootstrap | PENDING |
| RUNTIME starts and owner VNC is already mapped to the canonical desktop | Preserve VNC service and mapping through worker/job rotation | PENDING |
| RUNTIME task finishes successfully | Release controller authority; do not routinely destroy desktop/VNC/client or logout | PENDING |
| Authoritative registration is absent | Ordinary reuse refuses launch; only reviewed `canonical_bootstrap` path may create first runtime | PENDING |
| Registration lease generation is stale | Use reviewed `canonical_rebind`; never hand-edit registration | PENDING |
| `:98` exists and `6082` answers but registration/current mapping is not proven | Keep both current claims `UNKNOWN`; do not target them for mutation | PENDING |
| VNC endpoint is reachable | Treat visibility as observation only, not controller authority | PENDING |
| Client is disconnected but persistent desktop/VNC survives | Prefer bounded recovery inside the existing desktop; preserve desktop/VNC; restart client only through current reviewed recovery/creation path | PENDING |
| Another Track A worker owns PR #303 runtime | Do not live-observe or mutate that runtime surface | PENDING |
| Track B has a runtime on the same Synology hardware | Never share Track A canonical state/session/lease/display authority | PENDING |
| Worker sees owner-funded Codex/API availability | Do not use it without exact current owner authorization | PENDING |
| COVERAGE-AUDIT wants fresh runtime data | Consume durable RUNTIME evidence or request a bounded RUNTIME experiment; do not take the live session | PENDING |
| Research worker reaches a strong conclusion | Persist Draft evidence/PR; coordinator remains sole promotion authority | PENDING |

Prompt-eval automation is not available without invoking an external model/harness. Owner-funded AI use is forbidden for this task, so this task uses the repository-permitted documented manual scenario matrix plus deterministic file/content checks. Runtime E2E is not applicable because no runtime behavior is changed by this PR.
