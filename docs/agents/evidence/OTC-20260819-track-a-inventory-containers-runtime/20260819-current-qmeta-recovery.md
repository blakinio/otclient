# Current-build QMeta recovery — inventory / containers

Task: `OTC-20260819-track-a-inventory-containers-runtime`
Exact client: `52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`
ELF Build ID: `d803d9695868713ef6ab0c3cf65f91212c9c6a62`

## Method

The current official Linux ELF was inspected statically. Each target was recovered from its Qt6 moc string-data table, ELF RELA references, containing `QMetaObject`, metadata record and adjacent `qt_static_metacall` relocation. Historical VAs were not used as current lookup keys.

## Result

```text
targets requested:              21
targets recovered:              21
count-equivalent to historical: 21/21
QMeta record VA changed:        21/21
static-metacall VA changed:     21/21
```

Every address below is current-client-build-fenced only.

| Type | current QMeta | current metacall | methods | signals | properties | enums |
|---|---:|---:|---:|---:|---:|---:|
| `TContainerProtocolMessageHandler` | `0x30b78c0` | `0xd1a1d0` | 35 | 11 | 0 | 0 |
| `TInventoryContainer` | `0x30ce3c0` | `0xd0a2c0` | 1 | 1 | 0 | 0 |
| `TObjectAppearanceInstanceInfoStorage` | `0x30e8a60` | `0xd0a320` | 2 | 1 | 0 | 0 |
| `TObjectCountStorage` | `0x30dbd20` | `0xd0a390` | 1 | 1 | 0 | 0 |
| `TContainerStorage` | `0x30c3340` | `0xd0a0c0` | 3 | 3 | 0 | 0 |
| `TDepotSearchDetailListStorage` | `0x30df860` | `0xd0a260` | 1 | 1 | 0 | 0 |
| `TContainerStorageController` | `0x30aa940` | `0xd4c4d0` | 9 | 2 | 0 | 0 |
| `TPlayerInventoryAndStatusController` | `0x2f8fc20` | `0xd9b1c0` | 39 | 14 | 19 | 0 |
| `TAppearanceTypeHelperQmlService` | `0x3147de0` | `0x16b1410` | 3 | 0 | 0 | 0 |
| `TObjectAppearanceInstanceInfoQmlType` | `0x2f7f200` | `0x16afa20` | 1 | 1 | 4 | 2 |
| `TItemInfoDialogController` | `0x2f91640` | `0xd88db0` | 33 | 17 | 21 | 0 |
| `TStashDialogController` | `0x2f81160` | `0xdcc230` | 16 | 7 | 7 | 0 |
| `TDepotSearchWidgetController` | `0x2f8f480` | `0xd68480` | 34 | 12 | 23 | 0 |
| `TLootContainerQMLInfo` | `0x30d8800` | `0xd70ce0` | 16 | 10 | 6 | 0 |
| `TManageLootContainerDialogController` | `0x2f810a0` | `0xd8c6b0` | 26 | 6 | 6 | 0 |
| `TProficiencyProtocolMessageHandler` | `0x30b82c0` | `0xde25a0` | 6 | 2 | 0 | 0 |
| `TProficiencyStorage` | `0x30af1e0` | `0xdd7190` | 5 | 5 | 0 | 0 |
| `TManagedContainerStorage` | `0x30d8740` | `0xdd5240` | 2 | 2 | 0 | 0 |
| `TManagedContainersProtocolMessageHandler` | `0x30b8000` | `0xde0e00` | 5 | 3 | 0 | 0 |
| `TQuickLootBlackWhitelistStorage` | `0x2fa4120` | `0xdd31e0` | 0 | 0 | 0 | 0 |
| `TQuickLootGameActionHandler` | `0x30ba5c0` | `0xde0c50` | 12 | 1 | 0 | 0 |

All 21 method/signal/property/enum count tuples equal the historical exact-build tuples, while all 21 QMeta and metacall VAs moved. Historical addresses are therefore explicitly not reusable.

## Semantic surfaces

`TPlayerInventoryAndStatusController` retains `onPlayerCreatureAdded`, `onPlayerDataChanged`, `onInventoryChanged`, slot click/enter/exit/drag/target callbacks and inventory-options handling. `TInventoryContainer` exposes `inventoryChanged`.

`TContainerProtocolMessageHandler` retains inventory handlers (`handleSetInventoryMessage`, `handleDeleteInventoryMessage`, `handlePlayerInventoryMessage`), container handlers (open/close/create/change/delete/object-info), stash/special-container/depot handlers, and close/up/page/update/object-info/sort/move-to-managed request surfaces.

`TContainerStorage` exposes `containerUpdated(argc=2)`, `containerRemoved(argc=1)` and `manualSortModeChanged(argc=0)`. `TContainerStorageController` contains matching update/remove/manual-sort slots. Their actual direct current-build connections are proven in `20260819-current-state-propagation-routing.md`.

`TAppearanceTypeHelperQmlService` exposes the exact name/description/ID helper trio. Item-info and appearance QML types retain count/tier/classification/proficiency/inspect/value/tracking metadata surfaces. Proficiency handler/storage retain weapon-proficiency messages, progress/data/resource-balance signals and shaped-perk surfaces.

`TStashDialogController`, `TDepotSearchWidgetController`, `TManagedContainerStorage`, `TManagedContainersProtocolMessageHandler`, `TLootContainerQMLInfo`, `TManageLootContainerDialogController`, and `TQuickLootGameActionHandler` retain the stash/depot/managed-container/Quick-Loot/obtain-container state and action surfaces documented by the task.

## Evidence boundary

### FACT

- 21/21 selected current QMeta objects were recovered without historical-address lookup;
- all selected count tuples match the historical build while every selected QMeta/metacall VA moved;
- listed method names, argument counts and property names are current-build metadata facts;
- storage/controller and inventory/status causal Qt connections are additionally proven in the later state-propagation checkpoint.

### INFERENCE

Stable Qt shapes and semantic names support architectural continuity but do not prove ABI/field-layout identity.

### UNKNOWN / NOT_OBSERVED

- message payload normalization and serialization beyond the recovered boundaries;
- authoritative authenticated live values/effects;
- exact subtype/charges/duration normalization;
- restart/relogin stability.
