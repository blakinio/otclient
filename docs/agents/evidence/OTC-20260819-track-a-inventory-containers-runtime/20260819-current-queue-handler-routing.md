# Current-build inventory/container queue → handler routing

Task: `OTC-20260819-track-a-inventory-containers-runtime`
Exact client: `15.32 / 52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`
ELF Build ID: `d803d9695868713ef6ab0c3cf65f91212c9c6a62`

## Result

The current `tibia::protocol::TProtocolMessageQueue` is QMeta `0x30b83c0`, metacall `0xde7fa0`, 355 methods / 192 signals. The current `tibia::container::TContainerProtocolMessageHandler` is QMeta `0x30b78c0`, metacall `0xd1a1d0`, 35 methods / 11 signals.

A current-build connection setup routine constructs direct `QObject::connectImpl` pairs from queue signal wrappers to matching container-handler callables:

| Queue signal | Queue wrapper | Handler method | Handler callable | setup block |
|---|---:|---|---:|---:|
| `receivedSetInventoryMessage` (40) | `0xdd7aa0` | `handleSetInventoryMessage` (11) | `0xe6ff50` | `0x7ec146` |
| `receivedDeleteInventoryMessage` (67) | `0xdd7fb0` | `handleDeleteInventoryMessage` (12) | `0xe702e0` | `0x7ec1d2` |
| `receivedPlayerInventoryMessage` (117) | `0xdd8910` | `handlePlayerInventoryMessage` (13) | `0xe6c460` | `0x7ec25e` |
| `receivedContainerMessage` (62) | `0xdd7ec0` | `handleContainerMessage` (14) | `0xe71ca0` | `0x7ec2ea` |
| `receivedCloseContainerMessage` (63) | `0xdd7ef0` | close-container adapter | `0xe5dbf0` | `0x7ec376` |
| `receivedChangeInContainerMessage` (65) | `0xdd7f50` | `handleChangeInContainerMessage` (16) | `0xe704a0` | `0x7ec402` |
| `receivedDeleteInContainerMessage` (66) | `0xdd7f80` | `handleDeleteInContainerMessage` (17) | `0xe70610` | `0x7ec48e` |
| `receivedCreateInContainerMessage` (64) | `0xdd7f20` | `handleCreateInContainerMessage` (18) | `0xe70780` | `0x7ec51a` |
| `receivedObjectInfoMessage` (116) | `0xdd88e0` | `handleObjectInfoMessage` (19) | `0xe6c850` | `0x7ec5a6` |
| `receivedStashMessage` (153) | `0xdd8fd0` | `handleStashMessage` (20) | `0xe66e40` | `0x7ec632` |
| `receivedSpecialContainersAvailableMessage` (154) | `0xdd9000` | `handleSpecialContainersAvailableMessage` (22) | `0xe65440` | `0x7ec74a` |
| `receivedDepotSearchResultMessage` (155) | `0xdd9030` | `handleDepotSearchResultMessage` (23) | `0xe66fb0` | `0x7ec7d6` |
| `receivedDepotSearchDetailListMessage` (156) | `0xdd9060` | `handleDepotSearchDetailListMessage` (24) | `0xe708f0` | `0x7ec862` |

Method identities are independently anchored by current QMeta method order/metacall cases; queue identities are independently anchored by queue QMeta signal indices and wrappers activating the same index.

## Strengthened downstream result

This checkpoint originally stopped at queue→handler. The later `20260819-current-state-propagation-routing.md` now additionally proves:

- open/close/create/change/delete handler→`TContainerStorage` mutation and resulting storage signals;
- `TContainerStorage`→`TContainerStorageController` update/remove/manual-sort connections;
- Set/DeleteInventory→`TInventoryContainer::inventoryChanged`;
- `inventoryChanged`→`TPlayerInventoryAndStatusController::onInventoryChanged`.

Those later facts supersede the earlier downstream-UNKNOWN boundary for the listed routes.

## Passive observation

A later read-only admission proved one exact-current client at `otclient-track-a-kasmvnc / DISPLAY=:1`. One passive X11 frame showed the login screen, so inventory/container UI state was unavailable. No GUI input, credentials, login, gameplay, process mutation, debugger/injection or item/container stimulus was used.

## Evidence boundary

### FACT

- current queue/handler QMeta identities and shapes above;
- every listed queue-wrapper→handler-callable `QObject::connectImpl` pair;
- downstream state-propagation routes explicitly referenced above are current-build FACTs in the later checkpoint;
- passive current UI was at the login screen.

### UNKNOWN / NOT_OBSERVED

- full `PlayerInventory` bulk-value normalization;
- authoritative authenticated live inventory/container values;
- remaining action serialization/server effects;
- restart/relogin stability.

No historical VA is reused as current authority. All addresses here are fenced to the exact current client SHA above.
