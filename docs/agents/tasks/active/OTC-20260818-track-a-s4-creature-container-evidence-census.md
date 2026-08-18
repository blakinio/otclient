---
task_id: OTC-20260818-track-a-s4-creature-container-evidence-census
status: validating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: exact-head-validation
execution_mode: github_only
branch: research/OTC-20260818-track-a-s4-creature-container-evidence-census
base_branch: main
base_main: 13c5939ef89900a0998d56d2bf625c3906c9a68e
related_pr: 517
created: 2026-08-18T11:04:00+02:00
updated: 2026-08-18T11:20:00+02:00
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
  - docs/agents/tasks/active/OTC-20260818-track-a-s4-creature-container-evidence-census.md
  - docs/agents/evidence/OTC-20260818-track-a-s4-creature-container-evidence-census/**
  - docs/agents/reports/OTCLIENT-20260818-track-a-s4-creature-container-evidence-census.md
modules_touched:
  - official-client-static-re
reuses:
  - docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/**
  - docs/agents/evidence/OTC-20260818-track-a-s2-player-inbound-static/**
  - docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/runtime_type_semantics.jsonl
  - docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md
depends_on:
  - OTC-20260818-track-a-s1-unfiltered-static-census
blocks: []
non_overlap:
  - PR #475 runtime/worldmap/native-login surfaces were not observed or mutated.
  - PR #302 direct-player-position Draft was not modified.
  - Track B PR #284 is outside scope.
policy_version: 2
context_pressure: low
decomposition_decision: single
validation_level: focused
---

# Objective

Inventory already-committed exact-client/static evidence for the independent creature and container inbound/storage frontiers and choose the one with the strongest next repo-only discriminator.

# Producer

```yaml
run: 32120910903
job: 95660747269
artifact: 9318473016
artifact_digest: sha256:2759b4ec6e010485205f974bb726c2be350ffeed20a2417707cb207efd0b491d
result: SUCCESS
runtime_access: none
client_downloaded: false
client_executed: false
pr475_runtime_touched: false
```

# Result

The broad repository occurrence census is effectively tied, so lexical density is not used as the semantic discriminator.

Exact retained QMeta evidence selects **container**:

```text
TContainerProtocolMessageHandler
  QMeta 0x3084fe0
  qt_static_metacall 0xd1e000
  35 methods / 11 signals
TContainerStorage
  QMeta 0x308e720
  qt_static_metacall 0xd15af0
  3 methods / 3 signals

TCreatureProtocolMessageHandler
  QMeta 0x30cec80
  qt_static_metacall 0xd12510
  0 methods / 0 signals
TCreatureStorage
  QMeta 0x3085ba0
  qt_static_metacall 0xd25b70
  3 methods / 3 signals
```

Promoted S1 primary-vptr anchors remain:

```text
TContainerStorage 0x308a1a0
TCreatureStorage  0x308d078
```

## Selection

```yaml
S4_CENSUS: COMPLETED
NEXT_STATIC_FRONTIER: CONTAINER
CREATURE_FRONTIER: DEFERRED_NOT_DISPROVEN
```

This selects the next research target only. It does not promote message -> handler -> storage dataflow.

# Acceptance

- [x] deterministic repository evidence inventory generated for creature and container terms;
- [x] current-main exact evidence paths/history inventoried;
- [x] evidence categorized by heuristic strength and then manually bounded;
- [x] exact retained QMeta discriminator reviewed;
- [x] no external client download;
- [x] no runtime/Synology/X11/process-memory/login/credential access;
- [x] no PR #475 observation/mutation;
- [x] next frontier selected: container;
- [x] temporary census workflow removed from final branch diff;
- [x] E2E = NOT_APPLICABLE: repository/static evidence census only;
- [ ] final diff/path audit;
- [ ] current-main freshness/reconciliation;
- [ ] exact-head CI/governance;
- [ ] zero unresolved material review findings;
- [ ] coordinator promotion/closeout.

# Durable evidence

```text
docs/agents/evidence/OTC-20260818-track-a-s4-creature-container-evidence-census/result.md
docs/agents/reports/OTCLIENT-20260818-track-a-s4-creature-container-evidence-census.md
```

# Next bounded task

Open a separate container-only static task to recover the exact owner/typed QMeta contracts for:

```text
receivedContainerMessage
receivedCreateInContainerMessage
receivedChangeInContainerMessage
receivedDeleteInContainerMessage
```

and then follow only already-proven static edges toward `TContainerProtocolMessageHandler` and `TContainerStorage`. Stop at `UNKNOWN` if committed exact evidence does not contain the next edge.

# Checkpoint

```yaml
checkpoint_version: 2
status: validating
phase: exact-head-validation
pr: 517
last_completed_step: selected container as the next non-runtime static frontier from exact retained evidence
blockers: []
next_action: remove the temporary workflow, validate exact head, coordinator-close S4, then open container-only S5.
```
