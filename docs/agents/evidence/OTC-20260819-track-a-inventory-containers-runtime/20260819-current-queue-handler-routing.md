# Current-build inventory/container queue → handler routing

Task: `OTC-20260819-track-a-inventory-containers-runtime`  
Exact client: `15.32 / 52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`  
ELF Build ID: `d803d9695868713ef6ab0c3cf65f91212c9c6a62`

## Result

The current build's `tibia::protocol::TProtocolMessageQueue` QMeta was independently recovered as:

```text
QMeta record       0x30b83c0
qt_static_metacall 0xde7fa0
methods            355
signals            192
```

The current `tibia::container::TContainerProtocolMessageHandler` remains:

```text
QMeta record       0x30b78c0
qt_static_metacall 0xd1a1d0
methods            35
signals            11
```

A current-build connection setup routine around `0x7ec1xx–0x7ec8xx` constructs repeated `QObject::connectImpl` calls. In each connection block, the queue signal wrapper and the corresponding container-handler callable are materialized together before the `connectImpl` call. This closes the previously-UNKNOWN queue→handler edge for the listed inventory/container families.

| Queue signal | Queue wrapper | Handler method | Handler callable | setup block |
|---|---:|---|---:|---:|
| `receivedSetInventoryMessage` (40) | `0xdd7aa0` | `handleSetInventoryMessage` (11) | `0xe6ff50` | `0x7ec146` |
| `receivedDeleteInventoryMessage` (67) | `0xdd7fb0` | `handleDeleteInventoryMessage` (12) | `0xe702e0` | `0x7ec1d2` |
| `receivedPlayerInventoryMessage` (117) | `0xdd8910` | `handlePlayerInventoryMessage` (13) | `0xe6c460` | `0x7ec25e` |
| `receivedContainerMessage` (62) | `0xdd7ec0` | `handleContainerMessage` (14) | `0xe71ca0` | `0x7ec2ea` |
| `receivedChangeInContainerMessage` (65) | `0xdd7f50` | `handleChangeInContainerMessage` (16) | `0xe704a0` | `0x7ec402` |
| `receivedDeleteInContainerMessage` (66) | `0xdd7f80` | `handleDeleteInContainerMessage` (17) | `0xe70610` | `0x7ec48e` |
| `receivedCreateInContainerMessage` (64) | `0xdd7f20` | `handleCreateInContainerMessage` (18) | `0xe70780` | `0x7ec51a` |
| `receivedObjectInfoMessage` (116) | `0xdd88e0` | `handleObjectInfoMessage` (19) | `0xe6c850` | `0x7ec5a6` |
| `receivedStashMessage` (153) | `0xdd8fd0` | `handleStashMessage` (20) | `0xe66e40` | `0x7ec632` |
| `receivedSpecialContainersAvailableMessage` (154) | `0xdd9000` | `handleSpecialContainersAvailableMessage` (22) | `0xe65440` | `0x7ec74a` |
| `receivedDepotSearchResultMessage` (155) | `0xdd9030` | `handleDepotSearchResultMessage` (23) | `0xe66fb0` | `0x7ec7d6` |
| `receivedDepotSearchDetailListMessage` (156) | `0xdd9060` | `handleDepotSearchDetailListMessage` (24) | `0xe708f0` | `0x7ec862` |

The handler method identities are independently anchored by its recovered QMeta method order and `qt_static_metacall` jump-table cases. The queue identities are independently anchored by the recovered queue QMeta method order and wrappers whose `QMetaObject::activate` signal index matches the listed index.

## Passive live observation

A fresh later invocation re-read trusted main, admitted this lane as `runtime_access: read_only`, and proved a unique current target:

```text
container: otclient-track-a-kasmvnc
DISPLAY: :1
client PID: 17954
client count in target: 1
other host containers with process named client: 0
size: 52109920
sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
```

One contract-authorized passive X11 frame showed the client at the login screen. Therefore inventory/container UI was not observable in the current session. No GUI input, credentials, login, gameplay, process mutation, debugger/injection or item/container stimulus was used.

## Evidence boundary

### FACT

- current queue QMeta shape and addresses above;
- current handler QMeta shape and addresses above;
- all listed queue-signal-wrapper → handler-callable `QObject::connectImpl` pairs;
- passive current GUI is at the login screen, so no inventory/container state is presently visible.

### UNKNOWN

- handler → storage mutation for the listed inbound messages;
- storage → controller QObject connections;
- authoritative live inventory/container values and causal state changes;
- action serialization/server effects and restart/relogin stability.

No historical VA is reused as current authority. All addresses in this checkpoint are fenced to the exact current client SHA above.
