# OTC-20260819 Track A UI/settings static model

```yaml
task_id: OTC-20260819-track-a-ui-settings-static-model
project_lane: otclient
programme: OTCLIENT-TIBIA-RE
alias: TIBIA-RE-UI-SETTINGS
track_id: official-client-re
subject: official native Linux Tibia client only
status: investigating
phase: investigate
task_kind: discovery
implementation_authorized: false
run_scope: single_task
researcher_delivery: draft_pr_only
promotion_authority: coordinator_only
base_main: a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb
branch: docs/OTC-20260819-track-a-ui-settings-static-model
session_id: chatgpt-20260819-ui-settings-001
session_role: researcher
execution_mode: chat_github
execution_reason: bounded repository/static evidence discovery with GitHub connector; no live runtime required for the first phase
decomposition_decision: phased
decomposition_reason: first prove a static settings/controller/persistence topology; any later live reversible proof is a separate phase of the same task and requires fresh admission
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
invocation_started_at: 2026-08-19T00:33:00+02:00
updated_at: 2026-08-19T00:33:00+02:00
last_progress_at: 2026-08-19T00:33:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
session_rotation_count: 0
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 0
```

## Invocation and authority

Owner invocation: `TIBIA-RE-UI-SETTINGS` autonomously.

Alias source used for this invocation: PR #543 head `981febf4bf8f60896c5c09f8f30ad2859f6ca67c`, `docs/agents/prompts/OTCLIENT_TIBIA_RE_PARALLEL_RUNTIME_AGENT_PROMPTS_V1.md`. PR #543 is Draft and is not represented as merged governance. The owner named the alias directly; trusted-base repository safety/admission rules remain authoritative and stricter rules win.

This researcher owns discovery/evidence only and must stop repository delivery at a Draft PR. It must not update the canonical coverage matrix or promote its own claims.

## Coverage and objective

Primary coverage ownership for the alias is `H01-H19`, with priority `H07-H14`. This first phase is intentionally narrower:

- H10 graphics options/settings model;
- H11 audio/music/ambient options/settings model;
- H12 interface/sidebar/UI options/settings model;
- H13 gameplay/control options/settings model;
- H14 options persistence/profile/migration model.

Objective: recover the first durable, falsifiable topology for:

```text
UI/controller -> backing model -> persistence -> read
```

using static/repository/current-package evidence where safely available. Historical exact-build evidence must remain build-fenced. Reversible write/reload/restart persistence is explicitly deferred until a later phase with fresh runtime admission and rollback authority.

## Runtime admission

```yaml
track_id: official-client-re
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
```

No live official-client observation, GUI input, anti-idle input, login, credential use, process control, instrumentation, memory mutation, client-byte mutation, network mutation, purchase or transfer is authorized in this phase.

## Ownership and non-overlap

Owned writable paths:

- `docs/agents/tasks/active/OTC-20260819-track-a-ui-settings-static-model.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/**`

Optional, only if a deterministic GitHub-hosted static probe becomes necessary:

- `.github/workflows/track-a-ui-settings-static-model.yml`

Do not edit `docs/agents/ACTIVE_WORK.md` from this task. Do not edit #528 native-login, #539 action-protocol, #475 worldmap, #302 player-position, #536 coverage-matrix, or #543 prompt-package owned paths.

Dependencies/evidence inputs:

- PR #536 coverage checklist/matrix (H10-H14 currently `NOT_STARTED`; required transition `SETTINGS`);
- promoted/current repository Track A capability/static reports;
- current trusted-base runtime/admission/hybrid-routing governance;
- PR #543 alias mission text only as owner-invoked task input, not as merged authority.

## Acceptance for this phase

1. Identify concrete settings/UI/controller/persistence artifacts or prove the bounded static evidence is insufficient.
2. Separate `FACT`, `INFERENCE`, `UNKNOWN`, `DISPROVEN`, and build-sensitive historical evidence.
3. Persist compact evidence under the task namespace; do not commit proprietary client binaries, secrets or raw private state.
4. State exactly which of H10-H14 can move beyond `NONE` evidence and which cannot; do not self-promote matrix status.
5. Record the smallest safe next discriminator for the later read/reversible-write/reload proof.
6. Validate the Draft PR exact head with applicable repository checks and leave it unmerged for coordinator review.

## Checkpoint

```yaml
last_completed_step: claimed disjoint task/branch with static-only runtime admission
validation_level: focused
facts:
  - current main at claim is a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb
  - PR #536 records H10-H14 as NOT_STARTED with remaining step SETTINGS
unknown:
  - concrete official-client settings controller/backing model/persistence topology
  - current-build equivalence of any historical settings artifacts
blockers: []
next_action: inspect retained Track A capability/static evidence for concrete settings, controller and persistence identifiers and classify H10-H14 evidence boundaries
```
