# Track A S2 — player inbound static dispatch result

Task: `OTC-20260818-track-a-s2-player-inbound-static`  
PR: `#512`  
Execution: `github_hosted`, `runtime_access: none`  
Exact client: `15.32.df7b29` / `51965216` / `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

## Bounded result

The five selected inbound player protobuf types are now bound to exact native Qt signal contracts on the exact client:

```text
tibia::protocol::TProtocolMessageQueue
  staticMetaObject 0x3085b60
  qt_static_metacall 0xdf5fe0
  method_count 355
  signal_count 192
  unique full-range dispatch table 0x1d8bd6c

  signal 34  receivedPlayerDataCurrentMessage(GameserverMessagePlayerDataCurrent) @ 0xdf8bc1
  signal 43  receivedPlayerDataBasicMessage(GameserverMessagePlayerDataBasic) @ 0xdf8d3b
  signal 48  receivedPlayerStateMessage(GameserverMessagePlayerState) @ 0xdf8e0d
  signal 49  receivedPlayerSkillsMessage(GameserverMessagePlayerSkills) @ 0xdf8e37
  signal 117 receivedPlayerInventoryMessage(GameserverMessagePlayerInventory) @ 0xdf899f
```

Each exact target is a Qt signal stub that invokes `QMetaObject::activate @ 0x4dedc0` with its corresponding signal index.

This upgrades the S1 player-name correspondence from lexical-only discovery to a **proven static QMeta signal contract**:

```text
exact GameserverMessagePlayer* protobuf type
  -> exact TProtocolMessageQueue receivedPlayer* signal signature
  -> exact QMeta signal stub
```

The network decoder that causes the signal to be emitted is not proven here, and the connected receiver remains a separate edge.

## Negative control — `TPlayerProtocolMessageHandler` does not own these receive signals in QMeta

Phase-1 exact QMeta reconstruction proved:

```text
tibia::game::TPlayerProtocolMessageHandler
primary vptr       0x308a008
staticMetaObject   0x30852a0
qt_static_metacall 0xd1a920
method_count       22
signal_count       22
dispatch table     0x1d713d0
```

Its own QMeta table contains only the following signal/control surface:

```text
sendEnterWorld
sendGoNorth / East / South / West
sendStop / sendCancel
sendGoNorthEast / SouthEast / SouthWest / NorthWest
sendGoPath
sendRotateNorth / East / South / West
sendSetTactics
worldEntered
showSelectOutfitDialog
showConfigureCreaturePodiumDialog
showHirelingNameChangeConfiguration
publishGameAction
```

Therefore:

```text
receivedPlayer*Message is directly a TPlayerProtocolMessageHandler QMeta method
```

is **DISPROVEN** for this exact build.

This does **not** disprove that `TPlayerProtocolMessageHandler` is a connected receiver through Qt's typed connection machinery or that it handles those messages through ordinary non-QMeta member functions.

## `TPlayerData` exact QMeta surface

The same independent phase-1 producer recovered:

```text
tibia::game::TPlayerData
primary vptr       0x308ca70
staticMetaObject   0x307ea60
qt_static_metacall 0xd19f40
method_count       5
signal_count       5
dispatch table     0x1d7139c
```

Its five QMeta signals are:

```text
playerDataChanged
publishGameAction
playerLevelUp
vocationSpecificPlayerDataChanged
vocationChanged
```

No direct receive-message method exists in this QMeta surface either.

The existing P0 Draft #302 contains an exact static XYZ-shaped `TPlayerData` candidate at `+0x78/+0x7c/+0x80`. This S2 task deliberately does **not** promote those offsets as the storage mutated by the queue/handler path because no direct queue -> receiver -> `TPlayerData` dataflow edge has yet been proven.

## Exact static anchor xrefs

Fresh whole-file static xrefs independently reproduce:

```text
TPlayerProtocolMessageHandler vptr 0x308a008:
  0x825681
  0x825991
  0x194e5c6
  0x194e8e4

TPlayerData vptr 0x308ca70:
  0x843e20
  0x843f60
  0x8440b0
  0x8441f2
  0xefd13c
```

These are exact code references to the primary vptr anchors. Constructor/destructor/owner roles are not assigned from xref presence alone.

## Producer evidence

### Phase 1 — handler/data QMeta reconstruction

```text
run      32115252111
job      95643199117
head     74433287fa9549361eed3733c513b3f46fd2601c
result   SUCCESS
artifact 9316455906
digest   sha256:434340656a520110ac417fbd1fbd844664e7b2d49da418e7de5bc21b8f830fa5
```

### Phase 2 — global QMeta owner discriminator

```text
run      32115662884
job      95644479664
head     ea22c8db751f82fff17ae22c2be4f4fc3cd0420d
result   SUCCESS
artifact 9316573491
digest   sha256:ec97899357f6db77d45cf915d9133c778d48469f03628ea8914d6402ca3aca8f
global valid QMetaObjects 708
target matches 5/5
unique target owner tibia::protocol::TProtocolMessageQueue
```

Both producers revalidated the exact client fence before any build-specific address was used. Neither executed the client or accessed runtime/session/account state. Raw proprietary client bytes were removed before artifact upload.

## Repair history

The first phase-1 attempt (`32114891658 / 95642067206`) failed only in producer tooling after both exact hashes passed. Capstone `skipdata` pseudo-instructions raised `CS_ERR_SKIPDATA` when `.operands` was read. The repair separated bounded function decoding from whole-section skipdata scanning and guarded skipdata operand access. No semantic result from the failed run was promoted.

## Classification

```yaml
FACT:
  TPlayerProtocolMessageHandler_QMeta_identity: PROVEN
  TPlayerProtocolMessageHandler_full_method_table: PROVEN
  TPlayerProtocolMessageHandler_full_range_dispatch_table: PROVEN
  TPlayerData_QMeta_identity: PROVEN
  TPlayerData_full_method_table: PROVEN
  TProtocolMessageQueue_received_player_owner: PROVEN
  five_received_player_QMeta_signatures: PROVEN
  five_received_player_signal_stubs: PROVEN
  protobuf_type_to_queue_signal_static_contract: PROVEN

DISPROVEN:
  receivedPlayer_methods_directly_owned_by_TPlayerProtocolMessageHandler_QMeta: true

UNKNOWN:
  network_decoder_to_queue_signal_emission
  queue_signal_to_TPlayerProtocolMessageHandler_connection
  connected_receiver_function_for_each_player_signal
  handler_to_TPlayerData_mutation_edge
  TPlayerData_XYZ_candidate_as_inbound_mutation_target
  runtime_delivery_and_causal_state_change
```

## Next static discriminator

The next non-runtime player frontier is now sharply bounded:

```text
TProtocolMessageQueue receivedPlayer* signal
  -> exact QObject typed-connect construction
  -> exact receiver object/type
  -> exact receiver member function / QSlotObject trampoline
  -> TPlayerProtocolMessageHandler or alternative receiver
```

Only after that edge is proven should a following task trace the receiver into `TPlayerData` storage/mutation. Neither requires PR #475's physical runtime for the static phase.

## Safety / non-overlap

```yaml
runtime_access: none
client_executed: false
synology_used: false
x11_or_vnc_used: false
process_memory_used: false
credentials_used: false
login_performed: false
gameplay_performed: false
raw_client_committed_or_uploaded: false
pr475_runtime_observed: false
pr475_runtime_mutated: false
physical_e2e: NOT_APPLICABLE_STATIC_EXACT_FILE_DISCOVERY_ONLY
```
