---
task_id: OTC-20260818-track-a-s4-creature-container-evidence-census
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: evidence-census
execution_mode: github_only
branch: research/OTC-20260818-track-a-s4-creature-container-evidence-census
base_branch: main
base_main: 592e193a5ada1c40d23193038f350e23c539898b
related_pr: pending
created: 2026-08-18T11:04:00+02:00
updated: 2026-08-18T11:04:00+02:00
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
  - .github/workflows/track-a-s4-creature-container-evidence-census.yml
  - docs/agents/tasks/active/OTC-20260818-track-a-s4-creature-container-evidence-census.md
  - docs/agents/evidence/OTC-20260818-track-a-s4-creature-container-evidence-census/**
  - docs/agents/reports/OTCLIENT-20260818-track-a-s4-creature-container-evidence-census.md
modules_touched:
  - official-client-static-re
reuses:
  - docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/**
  - docs/agents/evidence/OTC-20260818-track-a-s2-player-inbound-static/**
  - current main Git history and already-committed exact-client evidence only
depends_on:
  - OTC-20260818-track-a-s1-unfiltered-static-census
blocks: []
non_overlap:
  - PR #475 runtime/worldmap/native-login surfaces are not observed or mutated.
  - PR #302 direct-player-position Draft is not modified.
  - Track B PR #284 is outside scope.
policy_version: 2
context_pressure: low
decomposition_decision: single
validation_level: focused
---

# Objective

Inventory all already-committed exact-client/static evidence that can support either of these next independent frontiers without requiring the now-drifted public client source:

```text
A. TCreatureProtocolMessageHandler / receivedCreature* / TCreatureStorage
B. TContainerProtocolMessageHandler / receivedContainer* / TContainerStorage
```

This is an evidence availability/provenance census, not a runtime experiment and not a semantic promotion by itself.

# Canonical starting facts

From promoted S1:

```text
TCreatureStorage primary vptr = 0x308d078
TContainerStorage primary vptr = 0x308a1a0
exact handler-class type strings exist for:
  tibia::creatures::TCreatureProtocolMessageHandler
  tibia::container::TContainerProtocolMessageHandler
exact receive-name strings exist for creature/container generated messages
```

# Questions

1. Which current-main files/evidence packages contain exact-build creature/container handler or storage anchors?
2. Which contain bounded disassembly, QMeta metadata, vptr xrefs, constructor/storage layouts, signal/slot evidence or before/after structural facts?
3. Which evidence is canonical-main versus historical/rejected/superseded?
4. Can one next static proof proceed entirely from already-sanitized evidence, or does it require an unavailable exact-client byte window?
5. Choose only one best next frontier based on actual evidence density; do not open both if neither is sufficiently grounded.

# Acceptance

- [ ] deterministic repository evidence inventory generated for creature and container terms;
- [ ] current-main exact evidence paths and history commits recorded;
- [ ] evidence categorized by strength: name-only / QMeta / exact-address / bounded-disassembly / runtime-proven;
- [ ] no external client download;
- [ ] no runtime/Synology/X11/process-memory/login/credential access;
- [ ] no PR #475 observation/mutation;
- [ ] next frontier selected or both marked blocked with exact reason;
- [ ] temporary workflow removed before closeout.

# Checkpoint

```yaml
checkpoint_version: 1
status: investigating
last_completed_step: claimed a repo-only evidence census after public exact-client source drift blocked fresh binary scanning
blockers: []
next_action: open Draft PR and run deterministic checkout/history census for creature/container exact evidence.
```
