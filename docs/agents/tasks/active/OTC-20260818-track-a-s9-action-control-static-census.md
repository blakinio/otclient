---
task_id: OTC-20260818-track-a-s9-action-control-static-census
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P1-BRIDGE
track_id: official-client-re
task_kind: discovery
phase: exact-evidence-reuse
execution_mode: github_only
branch: research/OTC-20260818-track-a-s9-action-control-static-census
base_branch: main
base_main: a10df477ce88183718ed855386ef96ba25b66320
related_pr: pending
created: 2026-08-18T15:12:00+02:00
updated: 2026-08-18T15:12:00+02:00
risk: low
implementation_authorized: true
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
mutation_authorized: false
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
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
owned_paths:
  - .github/workflows/track-a-s9-action-control-log-reuse.yml
  - docs/agents/tasks/active/OTC-20260818-track-a-s9-action-control-static-census.md
  - docs/agents/evidence/OTC-20260818-track-a-s9-action-control-static-census/**
  - docs/agents/reports/OTCLIENT-20260818-track-a-s9-action-control-static-census.md
modules_touched:
  - official-client-static-re
reuses:
  - sanitized exhaustive QMeta log from run 31790507112 / job 94736106350
  - promoted S8 creature action boundary
  - promoted S6 chat boundary
  - promoted S5/S7 container and inventory boundaries
depends_on:
  - OTC-20260818-track-a-s8-creature-inbound-static
blocks: []
non_overlap:
  - PR #528 native-login-to-ingame runtime is not observed or mutated.
  - PR #475 worldmap runtime is not observed or mutated.
  - PR #302 direct-player-position Draft is not modified.
  - Track B PR #284 is outside scope.
policy_version: 2
context_pressure: low
decomposition_decision: single
validation_level: focused
---

# Objective

Build the final repo-only exact-QMeta catalogue of native action/control boundaries needed by the wider official-client RE programme, without claiming downstream wire/runtime execution.

Required surfaces:

```text
movement intent / movement action / player protocol send boundary
attack / follow / look-at-creature
use / use-with / target selection
container/object move/use actions
chat actions
player generic actions
internal action routing
```

# Required exact classes

At minimum inspect these retained QMeta records where present:

```text
tibia::input::TPlayerMovementGameActionHandler
tibia::input::TPlayerMovementIntentHandler
tibia::game::TPlayerProtocolMessageHandler
tibia::creatures::TCreaturesGameActionHandler
tibia::input::TUseWithGameActionHandler
tibia::input::TGenericGameActionHandler
tibia::container::TContainerGameActionHandler
tibia::chat::TChatGameActionHandler
tibia::game::TPlayerGameActionHandler
tibia::game::TInternalGameActionRouter
```

Also enumerate all retained `*GameActionHandler` QMeta classes to provide a denominator, but promote detailed methods only where relevant to core gameplay control.

# Acceptance

- [ ] retained exact-SHA/QMeta evidence only;
- [ ] enumerate all QMeta classes ending `GameActionHandler`;
- [ ] recover complete method/signal surfaces for required classes;
- [ ] classify concrete capabilities for movement, turn/stop, attack/follow, use/use-with, move-object/container and chat;
- [ ] distinguish input/action-router boundary from protocol/wire boundary;
- [ ] explicitly mark wire effect and runtime execution as UNKNOWN/NOT_OBSERVED unless separately promoted already;
- [ ] no new client download/execution;
- [ ] no runtime/Synology/X11/process-memory/credentials/login/gameplay;
- [ ] no PR #528/#475 observation/mutation;
- [ ] temporary producer removed before promotion;
- [ ] exact-head CI/governance and coordinator closeout;
- [ ] final static-lane stop statement after promotion.

# Checkpoint

```yaml
checkpoint_version: 1
status: investigating
last_completed_step: admitted final action-control QMeta census on current main
blockers: []
next_action: reuse historical exhaustive QMeta log to enumerate action handlers and exact core-control methods.
```
