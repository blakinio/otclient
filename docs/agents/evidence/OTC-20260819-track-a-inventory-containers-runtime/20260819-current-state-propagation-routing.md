# Current-build inventory/container state propagation routing

Task: `OTC-20260819-track-a-inventory-containers-runtime`
Exact client: `15.32 / 52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`
ELF Build ID: `d803d9695868713ef6ab0c3cf65f91212c9c6a62`

## Result

This checkpoint closes current-build static causal routing from inventory/container inbound handlers into state storages and from the storages into Qt consumers. It is exact-binary static proof; it does not claim authoritative authenticated live values or server effects.

## TContainerStorage identity

The current `TContainerStorage` constructor at `0xe63310` stores primary vptr `0x30bf7b8`. Its meta-object path returns QMeta `0x30c3340` with:

- `containerUpdated(argc=2)`, signal 0, wrapper `0xd0a010`;
- `containerRemoved(argc=1)`, signal 1, wrapper `0xd0a060`;
- `manualSortModeChanged(argc=0)`, signal 2, wrapper `0xd0a0a0`.

Relevant storage operations used by the container handler are vslots `+0x78 -> 0xe63410`, `+0x88 -> 0xe6e9c0`, `+0x98 -> 0xe6ec40`, `+0xa0 -> 0xe6ee10`, and `+0xa8 -> 0xe6f160`.

## Handler → storage mutation

| Handler path | Storage call | Proven emitted signal |
|---|---|---|
| `handleContainerMessage` `0xe71ca0` | handler `+0x10`, vslot `+0x78 -> 0xe63410` at `0xe73141` | `containerUpdated` |
| close-container adapter `0xe5dbf0` | handler `+0x10`, vslot `+0x88 -> 0xe6e9c0` | `containerRemoved` |
| `handleChangeInContainerMessage` `0xe704a0` | vslot `+0x98 -> 0xe6ec40` at `0xe7056a` | `containerUpdated` |
| `handleDeleteInContainerMessage` `0xe70610` | vslot `+0xa0 -> 0xe6ee10` at `0xe706da` | `containerUpdated` |
| `handleCreateInContainerMessage` `0xe70780` | vslot `+0xa8 -> 0xe6f160` at `0xe7084a` | `containerUpdated` |

Storage emission sites are independently anchored by `QMetaObject::activate` against QMeta `0x30c3340`: `0xe63574`, `0xe6ea7b`, `0xe6ed14`, `0xe6eedb`, and `0xe6f1c2`.

## Storage → controller

`TContainerStorageController` QMeta is `0x30aa940`, metacall `0xd4c4d0`. Direct `QObject::connectImpl` setup proves:

| Storage signal | Controller target | connectImpl site |
|---|---|---:|
| `containerUpdated` `0xd0a010` | `onContainerUpdated` callable `0x85c7e0` | `0x85d48a` |
| `containerRemoved` `0xd0a060` | `onContainerRemoved` callable `0x85e1e0` | `0x85d52f` |
| `manualSortModeChanged` `0xd0a0a0` | method-8 callable `0x843850` (`onManualSortModeChanged`) | `0x85d77e` |

The first two target callables are also reached by controller metacall cases 4 and 5. Method 8 is independently identified by QMeta method order and the connection setup.

## Set/DeleteInventory → inventoryChanged

The `TContainerStorage` constructor allocates its `TInventoryContainer`, stores current inventory-container vptr `0x30f2be8`, and retains the object at storage `+0x18`. Its meta-object path anchors QMeta `0x30ce3c0`.

`TInventoryContainer` has one QMeta signal, `inventoryChanged` index 0, wrapper `0xd0a2b0`. Its vslot `+0x60 -> 0xe63ab0` mutates the inventory slot map and emits that signal at `0xe63c99–0xe63ca7`.

- `handleSetInventoryMessage` `0xe6ff50` obtains handler `+0x10` `TContainerStorage`, then its `+0x18` `TInventoryContainer`, and calls vslot `+0x60` at `0xe70125`.
- `handleDeleteInventoryMessage` `0xe702e0` obtains the same inventory container and calls vslot `+0x60` at `0xe7034f` for the delete/empty-object path.

Thus Set/DeleteInventory handler mutation → `TInventoryContainer::inventoryChanged` is a current-build FACT.

## inventoryChanged → status controller

`TPlayerInventoryAndStatusController` QMeta `0x2f8fc20`, metacall `0xd9b1c0`, identifies method index 20 as `onInventoryChanged(argc=0)`. Metacall case 20 tail-dispatches to callable `0xf01250`.

Connection setup around `0xf01f01–0xf02019` materializes the `TInventoryContainer` sender, signal wrapper `0xd0a2b0`, receiver callable `0xf01250`, sender QMeta `0x30ce3c0`, and `QObject::connectImpl` at `0xf02019`.

This closes the D11 storage→status-controller edge statically on the current exact build.

## Evidence boundary

### FACT

- exact current storage/inventory vptr and QMeta anchors above;
- listed handler→storage virtual dispatches and storage-signal emissions;
- all three listed storage→controller connections;
- Set/DeleteInventory→`inventoryChanged`;
- `inventoryChanged`→`onInventoryChanged`.

### INFERENCE

The recovered routing is strong evidence for normal current-client state propagation, but static code does not establish the authoritative values in a particular authenticated session.

### UNKNOWN / NOT_OBSERVED

- authenticated live inventory/container values and causal value changes;
- full `PlayerInventory` bulk-message value normalization;
- exact subtype/charges/duration normalization;
- action serialization/server acknowledgements;
- restart/relogin stability.

A contract-authorized passive X11 observation of the unique exact-current client found it at the login screen. No GUI input, credential access, login, gameplay, debugger/injection, process mutation, or item/container stimulus was used.
