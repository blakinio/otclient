---
task_id: OTC-20260818-track-a-s8-creature-inbound-static
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: exact-evidence-reuse
execution_mode: github_only
branch: research/OTC-20260818-track-a-s8-creature-inbound-static
base_branch: main
base_main: d53eec81bf718b1128fc8e7f9b0a53d991bf30bf
related_pr: pending
created: 2026-08-18T14:58:00+02:00
updated: 2026-08-18T14:58:00+02:00
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
  - .github/workflows/track-a-s8-creature-inbound-log-reuse.yml
  - docs/agents/tasks/active/OTC-20260818-track-a-s8-creature-inbound-static.md
  - docs/agents/evidence/OTC-20260818-track-a-s8-creature-inbound-static/**
  - docs/agents/reports/OTCLIENT-20260818-track-a-s8-creature-inbound-static.md
modules_touched:
  - official-client-static-re
reuses:
  - docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/**
  - sanitized exhaustive QMeta log from run 31790507112 / job 94736106350
  - S1 exact type/name artifact run 32112814216 / artifact 9315562574
depends_on:
  - OTC-20260818-track-a-s7-inventory-equipment-static
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

Exhaust the useful repo-only exact-SHA creature inbound frontier without new official-client bytes or runtime:

```text
TProtocolMessageQueue receivedCreature* / receivedMoveCreature / receivedConfigureCreaturePodium
  -> test for exact suffix-matched QMeta handle ownership across all retained QMeta classes
  -> TCreatureProtocolMessageHandler exact QMeta negative/positive surface
  -> TCreature exact QMeta surface
  -> TCreatureStorage exact QMeta surface
```

This task must not assume that a non-QMeta `TCreatureProtocolMessageHandler` path can be recovered from class naming alone.

# Questions

1. What is the complete exact queue signal set for `receivedCreature*`, `receivedMoveCreatureMessage`, and `receivedConfigureCreaturePodiumMessage`?
2. Do suffix-matched `handle*` methods exist in any retained QMeta class? If yes, which exact class/index; if no, record that exact QMeta negative result.
3. What is the exact QMeta surface of `TCreatureProtocolMessageHandler`?
4. What are the exact signals of `TCreature` and `TCreatureStorage`?
5. Does retained evidence prove queue->handler, handler->creature/storage mutation, or storage->consumer edges? If not, keep UNKNOWN.
6. After this discriminator, is there any material repo-only exact-SHA frontier left that can improve the model without a missing exact-client code window or active runtime?

# Acceptance

- [ ] already-sanitized exact-build/repository evidence only;
- [ ] complete queue creature signal inventory;
- [ ] global QMeta search for suffix-matched handle methods;
- [ ] exact TCreatureProtocolMessageHandler QMeta classification;
- [ ] exact TCreature and TCreatureStorage QMeta surfaces;
- [ ] typed registration contracts where S1 retains them;
- [ ] explicit FACT / DISPROVEN / UNKNOWN classifications;
- [ ] explicit repo-only exhaustion/resume decision;
- [ ] no new client download/execution;
- [ ] no runtime/Synology/X11/process-memory/credentials/login/gameplay;
- [ ] no PR #528/#475 runtime observation or mutation;
- [ ] temporary producer removed before promotion;
- [ ] exact-head CI/governance and coordinator closeout.

# Checkpoint

```yaml
checkpoint_version: 1
status: investigating
last_completed_step: admitted final repo-only creature static discriminator from current main
blockers: []
next_action: reuse historical exhaustive QMeta log and S1 artifacts to enumerate creature receive/model/storage boundaries and determine repo-only exhaustion.
```
