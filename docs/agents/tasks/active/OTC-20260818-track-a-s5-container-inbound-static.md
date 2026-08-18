---
task_id: OTC-20260818-track-a-s5-container-inbound-static
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: exact-evidence-reuse
execution_mode: github_only
branch: research/OTC-20260818-track-a-s5-container-inbound-static
base_branch: main
base_main: be0d3fd5468e70e8d97b66b838cd14ba24c56c73
related_pr: 518
created: 2026-08-18T11:24:00+02:00
updated: 2026-08-18T11:30:00+02:00
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
  - .github/workflows/track-a-s5-container-inbound-log-reuse.yml
  - docs/agents/tasks/active/OTC-20260818-track-a-s5-container-inbound-static.md
  - docs/agents/evidence/OTC-20260818-track-a-s5-container-inbound-static/**
  - docs/agents/reports/OTCLIENT-20260818-track-a-s5-container-inbound-static.md
modules_touched:
  - official-client-static-re
reuses:
  - docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/**
  - docs/agents/evidence/OTC-20260818-track-a-s2-player-inbound-static/**
  - sanitized S2 global QMeta artifact from run 32115662884
  - sanitized exhaustive QMeta log from run 31790507112 / job 94736106350
  - docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/runtime_type_semantics.jsonl
depends_on:
  - OTC-20260818-track-a-s4-creature-container-evidence-census
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

Resolve as far as already-sanitized exact-build evidence permits:

```text
GameserverMessageContainer / CreateInContainer / ChangeInContainer / DeleteInContainer
  -> exact receivedContainer* owner and typed QMeta signal contracts
  -> exact relationship, if provable, to TContainerProtocolMessageHandler
  -> exact relationship, if provable, to TContainerStorage
```

Do not obtain new official-client bytes. Do not infer queue/handler/storage edges from naming alone.

# Canonical starting anchors

```text
TContainerProtocolMessageHandler
  QMeta 0x3084fe0
  qt_static_metacall 0xd1e000
  35 methods / 11 signals

TContainerStorage
  primary vptr 0x308a1a0
  QMeta 0x308e720
  qt_static_metacall 0xd15af0
  3 methods / 3 signals
```

Promoted S1 lexical names:

```text
GameserverMessageContainer         -> receivedContainerMessage
GameserverMessageCreateInContainer -> receivedCreateInContainerMessage
GameserverMessageChangeInContainer -> receivedChangeInContainerMessage
GameserverMessageDeleteInContainer -> receivedDeleteInContainerMessage
```

# Acceptance

- [ ] reuse only exact-build sanitized/repository evidence;
- [ ] resolve owner/metaobject of all four receivedContainer* surfaces where present;
- [ ] recover exact method/signal indices, protobuf argument types and signal stubs where evidence supports it;
- [ ] decode exact TContainerProtocolMessageHandler QMeta method/signal names from retained evidence where possible;
- [ ] decode exact TContainerStorage QMeta method/signal names from retained evidence where possible;
- [ ] test, not assume, queue -> handler and handler -> storage connection/mutation edges;
- [ ] explicit FACT / DISPROVEN / UNKNOWN classifications;
- [ ] no client download/execution;
- [ ] no runtime/Synology/X11/process-memory/credentials/login/gameplay;
- [ ] no PR #475 observation/mutation;
- [ ] temporary log-reuse workflow removed before promotion;
- [ ] exact-head CI/governance and coordinator closeout.

# Checkpoint

```yaml
checkpoint_version: 2
status: investigating
last_completed_step: proved four container message types have exact TProtocolMessageQueue registerServerMessage<T> type surfaces and located the historical exhaustive QMeta log format
blockers: []
next_action: reuse job 94736106350 log to recover exact method indices/names for TProtocolMessageQueue, TContainerProtocolMessageHandler and TContainerStorage without obtaining client bytes.
```
