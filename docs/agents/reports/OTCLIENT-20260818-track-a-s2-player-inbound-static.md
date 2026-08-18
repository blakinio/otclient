# OTCLIENT Track A — player inbound static dispatch

Date: 2026-08-18  
Task: `OTC-20260818-track-a-s2-player-inbound-static`  
PR: `#512`  
Execution: GitHub-hosted exact-file analysis only (`runtime_access: none`)

## Executive result

The inbound player-message architecture is now materially clearer than the S1 lexical census.

The exact official Linux Tibia `15.32.df7b29` client exposes the five selected player messages as **typed Qt signals on `tibia::protocol::TProtocolMessageQueue`**:

```text
receivedPlayerDataCurrentMessage(GameserverMessagePlayerDataCurrent)
receivedPlayerDataBasicMessage(GameserverMessagePlayerDataBasic)
receivedPlayerStateMessage(GameserverMessagePlayerState)
receivedPlayerSkillsMessage(GameserverMessagePlayerSkills)
receivedPlayerInventoryMessage(GameserverMessagePlayerInventory)
```

The same static reconstruction proves that these receive signals are **not** QMeta methods owned by `tibia::game::TPlayerProtocolMessageHandler`. Its own 22-method QMeta table is an outbound/control signal surface (`sendGo*`, `sendStop`, `sendRotate*`, `sendSetTactics`, `worldEntered`, etc.).

Therefore the correct next problem is no longer “which message name belongs to `TPlayerProtocolMessageHandler`?” It is:

```text
TProtocolMessageQueue receivedPlayer* signal
  -> exact typed Qt connection
  -> receiver object/member
  -> player handler/data mutation path
```

## Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

## `TProtocolMessageQueue` player receive contract

Global relocation-backed Qt metaobject census recovered `708` valid exact-binary metaobjects. All five requested receive methods resolve uniquely to:

```text
class             tibia::protocol::TProtocolMessageQueue
staticMetaObject  0x3085b60
qt_static_metacall 0xdf5fe0
methods           355
signals           192
dispatch table    0x1d8bd6c
```

Exact player entries:

| Index | Method | Exact protobuf parameter | Stub |
|---:|---|---|---:|
| 34 | `receivedPlayerDataCurrentMessage` | `GameserverMessagePlayerDataCurrent` | `0xdf8bc1` |
| 43 | `receivedPlayerDataBasicMessage` | `GameserverMessagePlayerDataBasic` | `0xdf8d3b` |
| 48 | `receivedPlayerStateMessage` | `GameserverMessagePlayerState` | `0xdf8e0d` |
| 49 | `receivedPlayerSkillsMessage` | `GameserverMessagePlayerSkills` | `0xdf8e37` |
| 117 | `receivedPlayerInventoryMessage` | `GameserverMessagePlayerInventory` | `0xdf899f` |

Every stub calls `QMetaObject::activate @ 0x4dedc0` with the matching signal index. This establishes an exact static generated-protobuf-type -> queue-signal contract, not merely a same-looking string.

## `TPlayerProtocolMessageHandler` QMeta negative control

Exact reconstruction:

```text
primary vptr       0x308a008
staticMetaObject   0x30852a0
qt_static_metacall 0xd1a920
methods            22
signals            22
dispatch table     0x1d713d0
```

Its 22 QMeta entries are outbound/control signals. No `receivedPlayer*Message` appears.

This disproves direct QMeta ownership of the inbound player receive methods by `TPlayerProtocolMessageHandler`. It does not disprove a typed connection from `TProtocolMessageQueue` into ordinary non-QMeta player-handler members.

## `TPlayerData` QMeta boundary

Exact reconstruction:

```text
primary vptr       0x308ca70
staticMetaObject   0x307ea60
qt_static_metacall 0xd19f40
methods            5
signals            5
dispatch table     0x1d7139c
```

Its QMeta surface is:

```text
playerDataChanged
publishGameAction
playerLevelUp
vocationSpecificPlayerDataChanged
vocationChanged
```

The existing Draft #302 static candidate at `TPlayerData +0x78/+0x7c/+0x80` remains useful later, but this task does not connect those fields to the inbound queue and therefore does not promote them as the mutated player-message storage.

## Exact code anchors

`TPlayerProtocolMessageHandler` primary-vptr code refs:

```text
0x825681
0x825991
0x194e5c6
0x194e8e4
```

`TPlayerData` primary-vptr code refs:

```text
0x843e20
0x843f60
0x8440b0
0x8441f2
0xefd13c
```

Their constructor/destructor roles remain unassigned until bounded function decoding proves them.

## Producer evidence

Phase 1 — exact handler/data QMeta:

```text
run      32115252111
job      95643199117
artifact 9316455906
digest   sha256:434340656a520110ac417fbd1fbd844664e7b2d49da418e7de5bc21b8f830fa5
```

Phase 2 — global owner census:

```text
run      32115662884
job      95644479664
artifact 9316573491
digest   sha256:ec97899357f6db77d45cf915d9133c778d48469f03628ea8914d6402ca3aca8f
global QMetaObjects 708
target owner classes [tibia::protocol::TProtocolMessageQueue]
all five targets found true
```

Both producers removed raw client bytes before artifact upload and did not execute the client.

## Classification

```yaml
FACT:
  player_queue_signal_owner: tibia::protocol::TProtocolMessageQueue
  queue_static_metaobject: 0x3085b60
  queue_static_metacall: 0xdf5fe0
  queue_method_count: 355
  queue_signal_count: 192
  five_player_receive_signatures: exact
  five_player_receive_signal_stubs: exact
  TPlayerProtocolMessageHandler_qmeta: exact
  TPlayerData_qmeta: exact

DISPROVEN:
  receivedPlayer_methods_are_direct_TPlayerProtocolMessageHandler_QMeta_methods: true

UNKNOWN:
  network_decoder_to_queue_signal_emission
  queue_signal_to_receiver_connect_edge
  exact_receiver_member_function
  handler_to_TPlayerData_mutation
  authoritative_player_XYZ_storage
  runtime_delivery_semantics
```

## Next safe static frontier

The next bounded non-runtime task should recover the Qt connection graph for these exact signal methods:

```text
TProtocolMessageQueue signal PMF / signal index
  -> QObject::connect construction
  -> QSlotObject / receiver object
  -> exact receiver member function
```

If the receiver is proven to be `TPlayerProtocolMessageHandler`, the following task can trace that member into `TPlayerData`. If a different receiver is proven, the architecture should follow the evidence rather than forcing the prior handler hypothesis.

This continuation remains independent of PR #475 physical runtime/worldmap/native-login work.
