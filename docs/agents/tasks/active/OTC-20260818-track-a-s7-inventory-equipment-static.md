---
task_id: OTC-20260818-track-a-s7-inventory-equipment-static
status: validating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: exact-head-validation
execution_mode: github_only
branch: research/OTC-20260818-track-a-s7-inventory-equipment-static
base_branch: main
base_main: 066a5ba8b1811ef61d3aa8ac2ff3fc3601fe7b9d
related_pr: 529
created: 2026-08-18T14:40:00+02:00
updated: 2026-08-18T14:51:00+02:00
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

Recover exact retained static inventory/equipment inbound boundaries without new client bytes or runtime.

# Terminal research result

```yaml
S7_RESULT: ACCEPT_BOUNDED_PARTIAL_CANDIDATE
QUEUE_INVENTORY_SIGNAL_OWNERSHIP: FACT
INVENTORY_HANDLE_OWNER: FACT:TContainerProtocolMessageHandler
TPLAYERPROTOCOLMESSAGEHANDLER_OWNS_INVENTORY_HANDLES: DISPROVEN_QMETA
TINVENTORYCONTAINER_QMETA: FACT
PLAYER_INVENTORY_STATUS_CONTROLLER_QMETA: FACT
QUEUE_TO_CONTAINER_HANDLER_CONNECTION: UNKNOWN
CONTAINER_HANDLER_TO_INVENTORY_MUTATION: UNKNOWN
INVENTORY_CHANGED_TO_UI_CONTROLLER_CONNECTION: UNKNOWN
RUNTIME_INVENTORY_DELIVERY: NOT_OBSERVED
```

## Exact queue signals

```text
TProtocolMessageQueue
  staticMetaObject 0x3085b60
  qt_static_metacall 0xdf5fe0
  355 methods / 192 signals

40  receivedSetInventoryMessage
67  receivedDeleteInventoryMessage
117 receivedPlayerInventoryMessage
```

All three are inside the exact QMeta signal prefix.

## Exact handle owner — key correction

The exhaustive QMeta corpus finds all three matching `handle*Message` methods in:

```text
tibia::container::TContainerProtocolMessageHandler
staticMetaObject   0x3084fe0
qt_static_metacall 0xd1e000
35 methods / 11 signals

11 handleSetInventoryMessage
12 handleDeleteInventoryMessage
13 handlePlayerInventoryMessage
```

The exact `tibia::game::TPlayerProtocolMessageHandler` QMeta record has 22/22 signal methods (`sendEnterWorld`, movement/rotation/tactics, `worldEntered`, UI/game-action signals) and contains none of those three inventory handle methods. Therefore direct QMeta ownership of these inventory handlers by `TPlayerProtocolMessageHandler` is disproven.

## Inventory object

```text
tibia::container::TInventoryContainer
staticMetaObject   0x309a960
qt_static_metacall 0xd15cf0
1 method / 1 signal

0 inventoryChanged [signal]
```

## Player inventory/status controller

```text
tibia::gamewindow::TPlayerInventoryAndStatusController
staticMetaObject   0x2f6e440
qt_static_metacall 0xd8cef0
39 methods / 14 signals
```

Signals 0..13 include:

```text
inventoryMinimizedChanged
soulpointsChanged
capacityChanged
playerStatesChanged
blessingChanged
chaseModeChanged
secureModeEnabledChanged
pvpModeChanged
exportModeButtonEnableChanged
showCapacityWarning
gamesessionDisconnected
dualWieldingChanged
showPlayerStatesInBarChanged
publishGameAction
```

Relevant slots include:

```text
18 onPlayerCreatureAdded
19 onPlayerDataChanged
20 onInventoryChanged
21..26 slot click/enter/exit/drag/drop/target
29 onInventoryOptionsChanged
```

## Typed queue registration contracts

S1 artifact `9315562574` contains exact `TProtocolMessageQueue::registerServerMessage<T>` symbols for:

```text
GameserverMessageSetInventory
GameserverMessageDeleteInventory
GameserverMessagePlayerInventory
```

Each template signature contains a `TProtocolMessageQueue` member-function pointer accepting the corresponding `const T&`. This proves registration type contracts but not the concrete member pointer value at registration call sites.

Therefore:

```text
registered member pointer == suffix-matching received signal
  = INFERENCE_HIGH_NOT_DIRECTLY_PROVEN
```

# Provenance

```text
S7 producer run 32138692915
artifact 9324985568
digest sha256:16b94a26815abcebe049f9e4731d3e1dd19675e4b981665592222358de32286d

historical exact QMeta run/job
31790507112 / 94736106350
log sha256 481600615765a5bbc570888817f23b75ac5cf8b93fab693f3c461872c183ef70

S1 type artifact 9315562574
sha256:583c8c217fa2eaa2411f79995473cd910b8803d8599f80574491ca27b8ab9860
```

# Safety

```yaml
new_client_bytes: false
client_executed: false
runtime_access: none
synology: false
x11_vnc: false
process_memory: false
credentials: false
login: false
gameplay: false
pr528_runtime_touched: false
pr475_runtime_touched: false
```

# Acceptance

- [x] already-sanitized exact-build/repository evidence only;
- [x] exact queue receive indices recovered;
- [x] exact handle owner discovered rather than assumed;
- [x] `TPlayerProtocolMessageHandler` inventory-handle ownership disproven at QMeta boundary;
- [x] `TInventoryContainer` exact QMeta recovered;
- [x] `TPlayerInventoryAndStatusController` exact QMeta recovered;
- [x] S1 registration type contracts confirmed;
- [x] unknown downstream edges retained explicitly;
- [x] no runtime/credentials/login/gameplay or PR #528/#475 observation;
- [ ] temporary workflow removed;
- [ ] final exact-head CI/governance;
- [ ] review/thread audit;
- [ ] coordinator promotion/closeout.

# Checkpoint

```yaml
checkpoint_version: 2
status: validating
last_completed_step: recovered exact inventory queue/handler/container/controller QMeta boundaries and corrected handler ownership
blockers: []
next_action: persist durable result/report, remove temporary producer, run exact-head gates and coordinator-promote if clean.
```
