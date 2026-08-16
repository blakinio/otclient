---
task_id: OTC-20260816-tibia-re-p1-bridge-health
status: implementing
agent: ChatGPT
session_id: chatgpt-p1-bridge-health-20260816
session_role: researcher_implementer
project_lane: otclient
lane: P1-BRIDGE
track_id: official-client-re
task_kind: implementation
phase: implement
branch: feat/OTC-20260816-tibia-re-p1-bridge-health
base_branch: main
base_main: 0d7b2607912552599ae501891491aab439cfde7b
risk: medium
created: 2026-08-16T13:11:00+02:00
updated: 2026-08-16T13:11:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-tibia-re-p1-bridge-health.md
  - tools/tibia_runtime_bridge/**
  - .github/workflows/tibia-official-client-re-p1-bridge-health.yml
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
modules_touched:
  - official-client Track A read-only runtime bridge
reuses:
  - accepted bounded read-only bridge implementation from closed PR #283; source/tool/test blobs are historical input only until rebuilt and revalidated on current main
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_P1_BRIDGE_ALIAS.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
depends_on: []
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: owner explicitly dispatched OTCLIENT-TIBIA-RE-P1 as GitHub-hosted; deterministic bridge/API and lifecycle validation require no physical runtime
execution_class: github_hosted
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: checkpoint_and_return_for_coordinator_promotion
researcher_delivery: draft_only
coordinator_review_required: true
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: one cohesive P1 bridge package, with current-main reconstruction first and deterministic health/reacquisition/recovery validation second
validation_level: focused
track_a_runtime_agent_admission_version: 1
runtime_access: none
persistent_session_role: consumer_of_runtime_evidence
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
owner_funded_ai_api_authorized: false
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: internal_only
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
---

# Goal

Rebuild the already accepted bounded read-only official-client bridge on current `main`, then add a GitHub-hosted, runtime-independent health/reacquisition/recovery contract that consumes authoritative runtime-registration evidence and fails closed on missing, stale or generation-conflicting identity.

# Boundaries

- No Synology/self-hosted execution.
- No live official-client observation, attach, injection, login/relogin, restart, kill, input, VNC/X11, `/proc`, packet capture or gameplay action.
- No mutation or live observation of PR #303-owned runtime surfaces.
- No current `:98`, `6082`, PID or session claim.
- No Codex/OpenAI API/owner-funded AI quota or owner credential use.
- Historical PR #283 evidence may justify source reuse only; every rebuilt blob and new lifecycle behavior must be revalidated from the exact current branch head.
- Delivery remains `DRAFT_NOT_PROMOTED`; coordinator review is required before merge/promotion.

# Acceptance inventory

- [ ] Reconstruct the accepted read-only `tools/tibia_runtime_bridge/**` source/test surface from PR #283 onto current `main` without importing its stale task ownership.
- [ ] Preserve exact binary/profile fencing and fail-closed unsupported-target behavior.
- [ ] Define a versioned bridge health API whose inputs are authoritative registration/health evidence, never guessed local PID/display/session values.
- [ ] Reject missing registration, incomplete exact identity, stale evidence, namespace mismatch and lease-generation mismatch deterministically.
- [ ] Model reacquisition so old process/session identity is never silently reused after a generation/identity change.
- [ ] Model recovery as an explicit pure state transition; repository tests must cover disconnect/degraded -> reacquire -> ready and rejection paths without touching a real runtime.
- [ ] Keep structural `IN_GAME` evidence separate from runtime/bridge readiness; deterministic tests must not promote historical `session-status` markers to live proof.
- [ ] Add GitHub-hosted deterministic validation with no secrets and no self-hosted runner.
- [ ] Update the module catalogue and changelog for the reusable bridge contract.
- [ ] Full changed-file/diff audit shows no PR #303-owned or unrelated paths.
- [ ] Exact-head P1 validation and repository-required CI are green, or a concrete check/tool blocker is persisted.
- [ ] Independent audit records no open material finding before coordinator handoff.

# Checkpoint

```yaml
status: implementing
last_completed_step: claimed P1-BRIDGE from exact main after active-task/open-PR overlap review
proven:
  - current trusted base is 0d7b2607912552599ae501891491aab439cfde7b
  - current P1 alias defaults to github_hosted/runtime_access:none and excludes PR #303-owned runtime surfaces
  - closed PR #283 has coordinator-accepted bounded read-only bridge source evidence but was intentionally closed unmerged
unknown:
  - current physical runtime existence/identity; intentionally not queried by P1
  - whether historical bridge blobs require current-main adaptation until reconstructed and tested
blockers: []
next_action: open the early Draft PR, reconstruct accepted PR #283 bridge blobs on current main, then add deterministic health/reacquisition/recovery tests and hosted validation
```
