---
task_id: OTC-20260818-track-a-s5-container-inbound-static
status: validating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: exact-head-validation
execution_mode: github_only
branch: research/OTC-20260818-track-a-s5-container-inbound-static
base_branch: main
base_main: be0d3fd5468e70e8d97b66b838cd14ba24c56c73
related_pr: 518
created: 2026-08-18T11:24:00+02:00
updated: 2026-08-18T11:40:00+02:00
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
  - docs/agents/tasks/active/OTC-20260818-track-a-s5-container-inbound-static.md
  - docs/agents/evidence/OTC-20260818-track-a-s5-container-inbound-static/**
  - docs/agents/reports/OTCLIENT-20260818-track-a-s5-container-inbound-static.md
modules_touched:
  - official-client-static-re
reuses:
  - docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/**
  - docs/agents/evidence/OTC-20260818-track-a-s2-player-inbound-static/**
  - sanitized exhaustive QMeta log from run 31790507112 / job 94736106350
  - S1 exact static artifact 9315562574
  - docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/runtime_type_semantics.jsonl
depends_on:
  - OTC-20260818-track-a-s4-creature-container-evidence-census
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

Resolve as far as already-sanitized exact-build evidence permits:

```text
GameserverMessageContainer / CreateInContainer / ChangeInContainer / DeleteInContainer
  -> exact receivedContainer* owner and QMeta signal contracts
  -> exact relationship, if provable, to TContainerProtocolMessageHandler
  -> exact relationship, if provable, to TContainerStorage
```

# Terminal bounded result

```yaml
FOUR_CONTAINER_SERVER_MESSAGE_REGISTRATION_TYPE_CONTRACTS: FACT_TYPEINFO
FOUR_RECEIVED_CONTAINER_QMETA_OWNER: PROVEN_TProtocolMessageQueue
FOUR_RECEIVED_CONTAINER_QMETA_SIGNAL_INDICES: PROVEN
FOUR_CONTAINER_HANDLER_QMETA_METHODS: PROVEN_TContainerProtocolMessageHandler
TCONTAINERSTORAGE_QMETA_SURFACE: PROVEN
REGISTERED_MEMBER_POINTER_EQUALS_MATCHING_RECEIVED_SIGNAL: INFERENCE_HIGH_NOT_DIRECTLY_PROVEN
QUEUE_SIGNAL_TO_CONTAINER_HANDLER_CONNECTION: UNKNOWN
CONTAINER_HANDLER_TO_STORAGE_MUTATION: UNKNOWN
RUNTIME_CONTAINER_DELIVERY: NOT_OBSERVED
```

## Exact queue signals

```text
TProtocolMessageQueue
  staticMetaObject 0x3085b60
  qt_static_metacall 0xdf5fe0
  355 methods / 192 signals

62 receivedContainerMessage         argc=1
64 receivedCreateInContainerMessage argc=1
65 receivedChangeInContainerMessage argc=1
66 receivedDeleteInContainerMessage argc=1
```

All four have QMeta flags `0x6` and indices below the exact `signal_count=192`, so QMeta signal ownership is proven.

## Exact handler methods

```text
TContainerProtocolMessageHandler
  staticMetaObject 0x3084fe0
  qt_static_metacall 0xd1e000
  35 methods / 11 signals

14 handleContainerMessage         argc=1 flags=0xa
18 handleCreateInContainerMessage argc=1 flags=0xa
16 handleChangeInContainerMessage argc=1 flags=0xa
17 handleDeleteInContainerMessage argc=1 flags=0xa
```

The four methods are exact handler-owned QMeta methods and are outside the first 11 signal entries.

## Exact storage surface

```text
TContainerStorage
  primary vptr 0x308a1a0
  staticMetaObject 0x308e720
  qt_static_metacall 0xd15af0
  3 methods / 3 signals

0 containerUpdated       argc=2
1 containerRemoved       argc=1
2 manualSortModeChanged  argc=0
```

## Exact queue registration type contracts

S1 exact artifact `9315562574` contains four `TProtocolMessageQueue::registerServerMessage<T>` instantiations whose function parameter is a queue member pointer accepting the exact corresponding `const GameserverMessageX&` type for Container/Create/Change/DeleteInContainer.

The preserved type information does not identify which concrete queue member pointer was supplied to each instantiation; mapping it specifically to the matching `receivedXMessage` signal remains `INFERENCE_HIGH_NOT_DIRECTLY_PROVEN`.

# Acceptance

- [x] reused only exact-build sanitized/repository evidence;
- [x] resolved owner/metaobject of all four receivedContainer* surfaces;
- [x] recovered exact method/signal indices and argc/QMeta flags;
- [x] exact protobuf type is proven for each `registerServerMessage<T>` member-pointer contract; exact retained QMeta parameter-type/stub VA for the named signal is unavailable and is not claimed;
- [x] decoded exact TContainerProtocolMessageHandler QMeta method names;
- [x] decoded exact TContainerStorage QMeta signal names;
- [x] tested rather than assumed queue -> handler and handler -> storage edges; both remain UNKNOWN in retained evidence;
- [x] explicit FACT / INFERENCE / UNKNOWN classifications persisted;
- [x] no client download/execution by S5;
- [x] no current-task runtime/Synology/X11/process-memory/credentials/login/gameplay;
- [x] no PR #475 observation/mutation;
- [x] temporary log-reuse workflow removed from final branch diff;
- [x] E2E = NOT_APPLICABLE: static exact-evidence reuse only;
- [ ] final diff/path audit;
- [ ] current-main freshness/reconciliation;
- [ ] exact-head CI/governance;
- [ ] zero unresolved material review findings;
- [ ] coordinator promotion/closeout.

# Producer

```text
run      32122620894
job      95666177103
artifact 9319111338
digest   sha256:0e92295e1486540cf82233bdf7eb1c24b9c15c585f815f52a0847b340d4ee745
```

# Durable evidence

```text
docs/agents/evidence/OTC-20260818-track-a-s5-container-inbound-static/result.json
docs/agents/evidence/OTC-20260818-track-a-s5-container-inbound-static/result.md
docs/agents/reports/OTCLIENT-20260818-track-a-s5-container-inbound-static.md
```

# Next discriminator

Search only already-sanitized exact-build connection/call evidence for:

```text
receivedContainer* -> handleContainer*
handleContainer* -> TContainerStorage mutation
```

If no such window exists, stop this exact edge until an admissible exact-build source becomes available. Do not consume PR #475 runtime.

# Checkpoint

```yaml
checkpoint_version: 3
status: validating
phase: exact-head-validation
pr: 518
research_result: PARTIAL_PROVEN_QMETA_BOUNDARIES
last_completed_step: recovered exact queue receive signals, handler methods, storage signals and queue registration type contracts without new client bytes
blockers:
  - no retained exact connection/call window for queue -> handler or handler -> storage
next_action: remove temporary workflow, run exact-head repo gates and coordinator-close bounded result.
```
