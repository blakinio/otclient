---
task_id: OTC-20260816-track-a-agent-runtime-governance
status: validating
agent: ChatGPT
session_id: chatgpt-20260816-0805-track-a-agent-governance
session_role: governance-implementer
session_rotation_count: 0
project_lane: otclient
lane: track-a-governance
track_id: official-client-re
task_kind: implementation
phase: validate
branch: docs/OTC-20260816-track-a-agent-runtime-governance
base_branch: main
base_main: 3a5568f36ebc326afd246d0d2da45b5d8eecabfa
risk: medium
related_pr: 324
created: 2026-08-16T08:05:00+02:00
updated: 2026-08-16T08:23:00+02:00
lease_expires_at: 2026-08-16T09:08:00+02:00
lease_released_at: null
owned_paths:
  - docs/agents/AGENTS.md
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  - .github/scripts/test_track_a_agent_runtime_governance.py
  - .github/workflows/track-a-agent-runtime-governance.yml
  - docs/agents/tasks/active/OTC-20260816-track-a-agent-runtime-governance.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-agent-runtime-governance.md
modules_touched:
  - agent-governance
reuses:
  - docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - final Gate A/rebind/Gate B/bootstrap policy merged by PR #311
  - final cancellation-safe manager merged by PR #321
  - current Track A research isolation contract policy v5
depends_on:
  - main@3a5568f36ebc326afd246d0d2da45b5d8eecabfa
  - active coordinator PR #300 remains separately owned; this task does not edit its owned paths
  - runtime research PR #303 remains separately owned; this task does not access or mutate its runtime surface
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: narrow repository-governance and deterministic policy-audit changes can be completed through the GitHub connector without live runtime access
run_scope: single_task
continuation_policy: protected_merge_then_archive
task_completion_policy: protected_merge_then_archive
user_communication: milestone_only
implementation_authorized: true
context_pressure: medium
context_growth: stable
context_score: 6
estimate_confidence: high
decomposition_decision: single
validation_level: component
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 0
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
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
last_progress_at: 2026-08-16T08:23:00+02:00
material_review_findings:
  - PRRT_kwDOTVmdjs6ZlHWz: remediated in branch; authorized canonical mutation now requires positive equal lease generations after any rebind, with fresh negative regressions
  - PRRT_kwDOTVmdjs6ZlHW1: remediated in branch; every canonical access class is bound to runtime_owner_task == current task_id and the canonical namespace
  - PRRT_kwDOTVmdjs6ZlHW2: remediated in branch; ephemeral_isolated rejects the reserved canonical-live-runtime namespace and aliases, with fresh negative regressions
last_completed_step: fresh review P1s were repaired fail-closed in the admission validator and fresh behavior audit; no runtime access was used
next_action: require fresh exact-head admission-policy audit, behavior audit and repository CI after the three P1 repairs; then resolve only verified review threads, protected-merge PR #324 and archive/release the task
---

# Track A agent runtime-governance enforcement

## Goal

Make the final Track A canonical-live runtime rules unavoidable at the normal agent entrypoints, so every current or future Track A researcher classifies runtime access before work and fails closed instead of treating historical `:98`, `6082`, PID/session evidence as current authority.

## Acceptance criteria

- Track A agent instructions require workers to read the admission contract and classify runtime access before any runtime operation.
- The canonical Track A wrapper requires the same admission before claim/resume/observation/control/mutation.
- The Track A contract defines a mandatory admission record for `none`, `read_only`, `ephemeral_isolated`, `canonical_reuse_or_mutation`, `canonical_bootstrap`, and `canonical_rebind` work.
- Canonical mutation requires current Gate A plus any required rebind plus Gate B, target ownership/uniqueness, equal current lease-generation binding and the final whole-lifetime supervisor.
- Missing registration never falls through to ordinary reuse; it requires the separately implemented/authorized bootstrap transition.
- Lease-generation mismatch never falls through to ordinary reuse; it requires the reviewed rebind primitive and post-rebind equality before mutation.
- Ephemeral runtimes cannot use or alias the reserved canonical namespace.
- Historical `:98`, `6082`, PID or session evidence never satisfies current canonical identity.
- Track A workers may not mutate PR #303-owned runtime or Track B state through these rules.
- A deterministic repository test prevents removal/regression of the mandatory policy invariants.
- Future added/modified Track A active tasks must declare the complete runtime admission record; runtime-sensitive Track A implementation changes without such a task record fail the policy audit.
- No live Tibia client is launched, logged in, signalled, attached to or mutated by this task.
- Exact-head CI/review are green before merge; task is archived and ownership released afterward.

## Evaluation cases

### Positive

A static P2 researcher records `runtime_access: none`, performs no runtime operation and proceeds without a lease.

A read-only researcher records `runtime_access: read_only` and may inspect only demonstrably non-invasive evidence outside another task's owned runtime surface.

A task-owned ephemeral sandbox may mutate only its proven unique non-canonical namespace.

### Negative

A researcher sees historical `:98` or reachable `6082` and attempts to send input, attach, restart, login or otherwise mutate without Gate A + current identity. The policy requires refusal.

A researcher finds no `runtime-registration.json` and tries to launch through ordinary `guard-run`. The policy requires bootstrap instead.

A researcher finds an older registration generation and edits the JSON or proceeds anyway. The policy requires the dedicated rebind transition or refusal; even a claimed rebind cannot authorize mutation until the registration generation binding equals the current lease generation.

A canonical admission names another task as runtime owner. CI rejects it.

An ephemeral admission uses `canonical-live-runtime` or an alias containing that reserved namespace. CI rejects it.

A runtime-sensitive Track A PR updates code/workflow paths without an added/modified active Track A task containing an admission record. CI rejects it.

### Boundary

An existing Track A task is not mass-migrated merely because this policy merges. The admission fields become mandatory when that active task is next added/modified/claimed, matching the repository's migrate-on-next-checkpoint execution policy.

## Current overlap check

- PR #300 task is `waiting`, `session_id: null`, and its declared `owned_paths` do not include this task's changed governance entrypoints.
- PR #303 changed paths are limited to its runtime scripts/workflows/evidence/task record; none overlap this task.
- `docs/agents/CHANGELOG.md` is intentionally excluded because PR #300 currently changes it.

## Safety

This task itself has `runtime_access: none`. It does not inspect or mutate current X11, RFB/noVNC, Tibia process, login/session, credentials, canonical state directory, PR #303 runtime, or Track B runtime.
