---
task_id: OTC-20260816-track-a-lane-alias-prompts
status: validating
agent: ChatGPT
session_id: chatgpt-20260816-1227-track-a-alias-prompts
session_role: prompt-implementer
session_rotation_count: 0
project_lane: otclient
lane: track-a-governance
track_id: official-client-re
task_kind: documentation
phase: exact-head-validation
branch: docs/OTC-20260816-track-a-lane-alias-prompts
base_branch: main
base_main: 2c56f7f2c7c01d8dbc1b66febeea22b1d4aff6e8
risk: medium
related_pr: 349
created: 2026-08-16T12:27:00+02:00
updated: 2026-08-16T12:36:00+02:00
lease_expires_at: 2026-08-16T13:21:00+02:00
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
  - PR #303 runtime-owned surfaces remain separately owned and untouched
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
  eval_suite: manual scenario matrix below
  rollback_version: remove the six alias wrappers
last_progress_at: 2026-08-16T12:36:00+02:00
last_completed_step: six alias wrappers added; exact seven-file diff reviewed; deterministic content audit and manual prompt-eval matrix passed
next_action: require exact-head Track A governance/repository CI and zero material review findings, then protected-merge PR #349 and archive/release this task
---

# Track A lane alias prompts

## Delivered aliases

```text
OTCLIENT-TIBIA-RE-COORD
OTCLIENT-TIBIA-RE-P2
OTCLIENT-TIBIA-RE-P0
OTCLIENT-TIBIA-RE-P1
OTCLIENT-TIBIA-RE-RUNTIME
OTCLIENT-TIBIA-RE-AUDIT
```

Each file is an additive wrapper: it resolves the current canonical programme, runtime-admission, hybrid-routing and parallel-research contracts, then adds only the concrete lane preset. No second master programme prompt was created.

## Persistent Synology desktop/session invariant

The coordinator/RUNTIME aliases encode the requested topology as a target/invariant, not an invented current runtime fact:

```text
one long-lived canonical X11 desktop on synology-otclient-01
+ one long-lived private owner VNC view mapped to that same desktop
+ one reusable canonical exact-client runtime/session
```

When a healthy authoritative registration exists, RUNTIME must prefer Gate A -> required rebind -> Gate B -> reuse instead of fresh bootstrap/login. Normal worker/job/task completion releases controller authority without routinely logging out, killing the client, stopping X11/VNC or deleting canonical state. If the authenticated session remains safe/idle, preserve it for the next authorized RUNTIME worker. If disconnected while desktop/VNC survives, prefer bounded recovery within the existing desktop and preserve VNC continuity.

Historical `:98`, `6082`, PID/session remain non-authoritative and are never hard-coded as canonical. VNC visibility is not mutation authority. Missing registration still routes only to reviewed bootstrap and a lease-generation mismatch only to reviewed rebind.

## Acceptance / deterministic content audit

- PASS — all six alias files exist on PR #349 and expose unique short owner invocations.
- PASS — COORD owns promotion/integration and defaults to hosted/no-runtime coordination.
- PASS — P2/P0/P1/AUDIT default to GitHub-hosted `runtime_access: none` and consume/request RUNTIME evidence instead of starting independent live sessions.
- PASS — RUNTIME is pinned to `synology-otclient-01`, requires fresh admission at claim/resume and is the serialized physical evidence provider.
- PASS — RUNTIME explicitly preserves persistent X11 + VNC + client/session across worker/job rotation and forbids routine logout/kill/recreate at task end.
- PASS — aliases preserve Gate A/rebind/Gate B/bootstrap separation and current UNKNOWN/NOT_REGISTERED semantics.
- PASS — PR #303 ownership, Track B isolation, secrets and owner-funded AI restrictions are preserved.
- PASS — changed-file inventory is exactly six new alias prompts plus this task record; no runtime/workflow/Track B path changed.

## Manual prompt-eval matrix

```yaml
manual_prompt_eval:
  automation_available: false
  reason: no repository executable model harness is available; owner-funded external AI use is forbidden
  deterministic_checks: 1
  cases: 16
  passed: 16
  failed: 0
```

PASS cases:

1. Static P2 dispatch -> hosted + none, no Synology takeover.
2. P0 causal real-client read -> bounded RUNTIME evidence, no duplicate login/session.
3. P1 restart/reacquisition proof -> hosted implementation plus serialized RUNTIME proof.
4. Healthy authoritative canonical runtime -> Gate A/rebind/Gate B and reuse; no fresh login/bootstrap.
5. Existing owner VNC mapping -> preserve VNC through worker/job turnover.
6. Successful RUNTIME task finish -> release authority, preserve desktop/VNC/client/session.
7. Missing registration -> refuse ordinary launch; bootstrap only.
8. Stale registration generation -> reviewed rebind only; no manual JSON edits.
9. Historical `:98`/reachable `6082` without current proof -> UNKNOWN; no mutation target inference.
10. Reachable VNC -> visibility only, not controller authority.
11. Disconnected client with persistent desktop/VNC -> bounded recovery in same desktop; preserve VNC.
12. PR #303-owned runtime -> unrelated worker refuses live observation/mutation.
13. Track B runtime on same hardware -> no shared Track A authority/state/session.
14. Owner-funded Codex/API is available -> refuse use without exact current authorization.
15. COVERAGE-AUDIT needs physical evidence -> request RUNTIME; never take canonical session.
16. Research worker has strong result -> Draft evidence only; coordinator remains promotion authority.

Runtime E2E: `NOT_APPLICABLE_WITH_REASON` — this task changes prompt/documentation only and intentionally performs no Tibia/X11/VNC/runtime operation.
