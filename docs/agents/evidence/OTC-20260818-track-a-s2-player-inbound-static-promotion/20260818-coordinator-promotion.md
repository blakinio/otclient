# Track A S2 player inbound static — coordinator promotion

Date: 2026-08-18  
Source task: `OTC-20260818-track-a-s2-player-inbound-static`  
Source Draft: PR #512  
Source final head: `d0c78772294cd6355221cce96f499b85fb7738cf`  
Trusted integration base: `main@a9e7ab21ed0962482e4381aadd50be92714785a6`  
Decision: **ACCEPT_WITH_EDITS**

## Promoted result

Exact official Linux client:

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

### Player protocol-handler QMeta surface

```text
tibia::game::TPlayerProtocolMessageHandler
primary vptr       0x308a008
staticMetaObject   0x30852a0
qt_static_metacall 0xd1a920
method_count       22
signal_count       22
dispatch table     0x1d713d0
full-range guard   cmp edx,0x15
```

The 22 methods are the outbound/control signal surface (`sendEnterWorld`, movement/stop/cancel/path/rotate/tactics, `worldEntered`, outfit/podium/hireling dialogs and `publishGameAction`). None is `receivedPlayer*Message`.

Promoted negative result:

```yaml
RECEIVED_PLAYER_METHODS_DIRECTLY_OWNED_BY_TPlayerProtocolMessageHandler_QMETA: DISPROVEN
```

This does not disprove a typed Qt connection into ordinary non-QMeta members of that handler.

### Exact receive-signal owner

Global relocation-backed Qt metaobject census found `708` valid metaobjects and resolved all five requested player receive methods to one owner:

```text
tibia::protocol::TProtocolMessageQueue
staticMetaObject   0x3085b60
qt_static_metacall 0xdf5fe0
method_count       355
signal_count       192
dispatch table     0x1d8bd6c
```

Exact typed signal contracts:

```text
34  receivedPlayerDataCurrentMessage(GameserverMessagePlayerDataCurrent) @ 0xdf8bc1
43  receivedPlayerDataBasicMessage(GameserverMessagePlayerDataBasic) @ 0xdf8d3b
48  receivedPlayerStateMessage(GameserverMessagePlayerState) @ 0xdf8e0d
49  receivedPlayerSkillsMessage(GameserverMessagePlayerSkills) @ 0xdf8e37
117 receivedPlayerInventoryMessage(GameserverMessagePlayerInventory) @ 0xdf899f
```

Every exact target is a Qt signal stub that invokes `QMetaObject::activate@0x4dedc0` with the matching signal index.

Therefore the source S1 lexical player correlations are promoted to the following bounded static contract:

```text
exact GameserverMessagePlayer* protobuf type
  -> exact TProtocolMessageQueue receivedPlayer* signal signature
  -> exact QMeta signal stub
```

### TPlayerData QMeta boundary

```text
tibia::game::TPlayerData
primary vptr       0x308ca70
staticMetaObject   0x307ea60
qt_static_metacall 0xd19f40
method_count       5
signal_count       5
dispatch table     0x1d7139c
```

Its QMeta surface is `playerDataChanged`, `publishGameAction`, `playerLevelUp`, `vocationSpecificPlayerDataChanged`, `vocationChanged`.

The coordinator does not connect the queue signals to `TPlayerData` from these names/anchors alone.

## Retained UNKNOWNs

```yaml
NETWORK_DECODER_TO_QUEUE_SIGNAL_EMISSION: UNKNOWN
QUEUE_SIGNAL_TO_TPlayerProtocolMessageHandler_CONNECTION: UNKNOWN
EXACT_CONNECTED_RECEIVER_MEMBER: UNKNOWN
HANDLER_TO_TPlayerData_MUTATION: UNKNOWN
TPlayerData_XYZ_CANDIDATE_AS_INBOUND_TARGET: UNKNOWN
RUNTIME_DELIVERY_AND_CAUSAL_STATE_CHANGE: UNKNOWN
```

The open P0 Draft #302 `TPlayerData +0x78/+0x7c/+0x80` XYZ-shaped static candidate is explicitly not promoted as authoritative or as the inbound mutation target by this work.

## Independent evidence review

Phase 1 exact handler/data QMeta producer:

```text
run      32115252111
job      95643199117
head     74433287fa9549361eed3733c513b3f46fd2601c
artifact 9316455906
digest   sha256:434340656a520110ac417fbd1fbd844664e7b2d49da418e7de5bc21b8f830fa5
```

Phase 2 global receive-owner producer:

```text
run      32115662884
job      95644479664
head     ea22c8db751f82fff17ae22c2be4f4fc3cd0420d
artifact 9316573491
digest   sha256:ec97899357f6db77d45cf915d9133c778d48469f03628ea8914d6402ca3aca8f
```

Both runs revalidated the exact client fence, did not execute the client, and removed raw proprietary client bytes before sanitized artifact upload.

## Falsification / accepted edits

1. The initial hypothesis that `receivedPlayer*Message` would appear directly in `TPlayerProtocolMessageHandler` QMeta was falsified by the exact 22-method table; the task followed the evidence to the real QMeta owner instead of forcing the hypothesis.
2. The first producer attempt failed in Capstone skipdata handling; only post-repair successful producer evidence is promoted.
3. The source task's final governance failure was metadata-only: universal Track A admission fields were absent for a static `runtime_access:none` task. They were added as explicit `NOT_APPLICABLE`, after which both governance audits passed. No research/runtime semantics changed.
4. Direct primary-vptr code xrefs are retained only as identity/constructor leads; constructor/destructor and owner roles are not inferred from xref presence alone.

No material finding remains open inside this bounded S2 result.

## Source exact-head validation

```text
source head d0c78772294cd6355221cce96f499b85fb7738cf
Track A governance 32116406977 = SUCCESS
  Deterministic admission-policy audit 95646794390 = SUCCESS
  Fresh admission behavior audit      95646794402 = SUCCESS
CI 32116407136 = SUCCESS
  CI / Required                       95646841777 = SUCCESS
reviews                               0
unresolved review threads             0
main freshness                        PASS at a9e7ab21ed0962482e4381aadd50be92714785a6
```

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

## Next independent static frontier

```text
TProtocolMessageQueue receivedPlayer* signal
  -> exact QObject typed-connect construction
  -> exact receiver object/type
  -> exact receiver member / QSlotObject trampoline
```

Only after that edge is proven should a later task trace the receiver into `TPlayerData`.
