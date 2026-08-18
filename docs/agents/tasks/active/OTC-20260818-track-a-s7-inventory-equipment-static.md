---
task_id: OTC-20260818-track-a-s7-inventory-equipment-static
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: exact-evidence-reuse
execution_mode: github_only
branch: research/OTC-20260818-track-a-s7-inventory-equipment-static
base_branch: main
base_main: 066a5ba8b1811ef61d3aa8ac2ff3fc3601fe7b9d
related_pr: pending
created: 2026-08-18T14:40:00+02:00
updated: 2026-08-18T14:40:00+02:00
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
owned_paths:
  - .github/workflows/track-a-s7-inventory-equipment-log-reuse.yml
  - docs/agents/tasks/active/OTC-20260818-track-a-s7-inventory-equipment-static.md
  - docs/agents/evidence/OTC-20260818-track-a-s7-inventory-equipment-static/**
  - docs/agents/reports/OTCLIENT-20260818-track-a-s7-inventory-equipment-static.md
modules_touched:
  - official-client-static-re
reuses:
  - docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/**
  - docs/agents/evidence/OTC-20260818-track-a-s2-player-inbound-static/**
  - sanitized exhaustive QMeta log from run 31790507112 / job 94736106350
  - S1 exact type/name artifact run 32112814216 / artifact 9315562574
depends_on:
  - OTC-20260818-track-a-s6-chat-inbound-static
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

Recover the exact retained static boundaries for official-client inventory/equipment inbound state without new client bytes or runtime:

```text
GameserverMessageSetInventory
GameserverMessageDeleteInventory
GameserverMessagePlayerInventory
  -> exact TProtocolMessageQueue received* QMeta surfaces
  -> exact QMeta owner(s) of handleSetInventoryMessage / handleDeleteInventoryMessage / handlePlayerInventoryMessage
  -> exact TInventoryContainer QMeta surface
  -> exact TPlayerInventoryAndStatusController QMeta surface
```

The discriminator must discover handler ownership from the exhaustive QMeta corpus; do not assume `TPlayerProtocolMessageHandler`.

# Questions

1. Are all three `received*Inventory*` names exact `TProtocolMessageQueue` signals and at which indices?
2. Which exact QMeta class owns each corresponding `handle*Message` method?
3. What are the complete QMeta surfaces of `tibia::container::TInventoryContainer` and `tibia::gamewindow::TPlayerInventoryAndStatusController`?
4. Which exact `registerServerMessage<T>` type contracts exist for the three protobuf messages?
5. Does retained evidence prove any queue->handler, handler->inventory-object or inventory-object->UI/controller state edge? If not, keep it UNKNOWN.

# Acceptance

- [ ] use only already-sanitized exact-build/repository evidence;
- [ ] no new official-client download/execution;
- [ ] exact queue receive indices for SetInventory/DeleteInventory/PlayerInventory;
- [ ] exact QMeta owner(s) and indices for the three `handle*Message` names;
- [ ] exact `TInventoryContainer` QMeta methods/signals;
- [ ] exact `TPlayerInventoryAndStatusController` QMeta methods/signals;
- [ ] exact registration type contracts where retained S1 evidence supports them;
- [ ] explicit FACT / INFERENCE / UNKNOWN classifications;
- [ ] no runtime/Synology/X11/process-memory/credentials/login/gameplay;
- [ ] no PR #528/#475 runtime observation or mutation;
- [ ] temporary workflow removed before promotion;
- [ ] exact-head CI/governance and coordinator closeout.

# Checkpoint

```yaml
checkpoint_version: 1
status: investigating
last_completed_step: admitted inventory/equipment static frontier from current main with no runtime overlap
blockers: []
next_action: reuse historical exact-SHA exhaustive QMeta log to discover queue/handler/inventory/controller ownership and indices.
```
