# Current-build QMeta recovery — inventory / containers

Task: `OTC-20260819-track-a-inventory-containers-runtime`  
Exact client: `52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`  
ELF Build ID: `d803d9695868713ef6ab0c3cf65f91212c9c6a62`  
Execution: static file analysis only; client not executed; `runtime_access: none`.

## Recovery method

The current binary was inspected as an ELF file only. For each target Qt type:

1. identify the Qt6 moc stringdata block by its `offsetsAndSizes` table and fully qualified class-name first string;
2. locate the ELF `RELA` reference whose addend points to that stringdata block;
3. derive the containing `QMetaObject` record from the stringdata field relocation;
4. recover metadata and `qt_static_metacall` pointers from adjacent current-build relocations;
5. parse Qt metadata revision `13` header and method/property records;
6. compare method/signal/property/enum counts to the retained historical exact-build census.

No historical VA is used as a lookup key for the current build.

## Result

```text
targets requested:                  21
targets recovered:                  21
count-equivalent to historical:     21/21
QMeta record VA changed:            21/21
static-metacall VA changed:         21/21
```

**FACT:** the selected Qt surface shape is stable across the two build-fenced clients for all 21 target types: method, signal, property and enum counts match exactly.

**FACT:** every recovered QMeta record and every recovered static-metacall address moved. Historical addresses are therefore explicitly **not reusable** on the current client.

## Exact current QMeta table

| Type | current QMeta | current metacall | methods | signals | properties | enums | counts vs historical |
|---|---:|---:|---:|---:|---:|---:|---|
| `TContainerProtocolMessageHandler` | `0x30b78c0` | `0xd1a1d0` | 35 | 11 | 0 | 0 | SAME |
| `TInventoryContainer` | `0x30ce3c0` | `0xd0a2c0` | 1 | 1 | 0 | 0 | SAME |
| `TObjectAppearanceInstanceInfoStorage` | `0x30e8a60` | `0xd0a320` | 2 | 1 | 0 | 0 | SAME |
| `TObjectCountStorage` | `0x30dbd20` | `0xd0a390` | 1 | 1 | 0 | 0 | SAME |
| `TContainerStorage` | `0x30c3340` | `0xd0a0c0` | 3 | 3 | 0 | 0 | SAME |
| `TDepotSearchDetailListStorage` | `0x30df860` | `0xd0a260` | 1 | 1 | 0 | 0 | SAME |
| `TContainerStorageController` | `0x30aa940` | `0xd4c4d0` | 9 | 2 | 0 | 0 | SAME |
| `TPlayerInventoryAndStatusController` | `0x2f8fc20` | `0xd9b1c0` | 39 | 14 | 19 | 0 | SAME |
| `TAppearanceTypeHelperQmlService` | `0x3147de0` | `0x16b1410` | 3 | 0 | 0 | 0 | SAME |
| `TObjectAppearanceInstanceInfoQmlType` | `0x2f7f200` | `0x16afa20` | 1 | 1 | 4 | 2 | SAME |
| `TItemInfoDialogController` | `0x2f91640` | `0xd88db0` | 33 | 17 | 21 | 0 | SAME |
| `TStashDialogController` | `0x2f81160` | `0xdcc230` | 16 | 7 | 7 | 0 | SAME |
| `TDepotSearchWidgetController` | `0x2f8f480` | `0xd68480` | 34 | 12 | 23 | 0 | SAME |
| `TLootContainerQMLInfo` | `0x30d8800` | `0xd70ce0` | 16 | 10 | 6 | 0 | SAME |
| `TManageLootContainerDialogController` | `0x2f810a0` | `0xd8c6b0` | 26 | 6 | 6 | 0 | SAME |
| `TProficiencyProtocolMessageHandler` | `0x30b82c0` | `0xde25a0` | 6 | 2 | 0 | 0 | SAME |
| `TProficiencyStorage` | `0x30af1e0` | `0xdd7190` | 5 | 5 | 0 | 0 | SAME |
| `TManagedContainerStorage` | `0x30d8740` | `0xdd5240` | 2 | 2 | 0 | 0 | SAME |
| `TManagedContainersProtocolMessageHandler` | `0x30b8000` | `0xde0e00` | 5 | 3 | 0 | 0 | SAME |
| `TQuickLootBlackWhitelistStorage` | `0x2fa4120` | `0xdd31e0` | 0 | 0 | 0 | 0 | SAME |
| `TQuickLootGameActionHandler` | `0x30ba5c0` | `0xde0c50` | 12 | 1 | 0 | 0 | SAME |

All addresses above are **current-client-build-fenced facts only**.

## Recovered semantic method/property surfaces

### Inventory / status

`TPlayerInventoryAndStatusController` retains current methods including `onPlayerCreatureAdded`, `onPlayerDataChanged`, `onInventoryChanged`, `onSlotClicked`, `onSlotEntered`, `onSlotExited`, `onSlotStartDrag`, `onSlotDragDropped`, `onSlotTargetSelected`, and `onInventoryOptionsChanged`. Recovered properties include `capacity`, `playerStates`, `chaseEnabled`, `secureModeEnabled`, PvP-mode booleans, `hasDualWielding`, `dualWieldingObjectID`, and `showPlayerStatesInBar`.

`TInventoryContainer` exposes the single signal `inventoryChanged`.

### Inbound container handler

`TContainerProtocolMessageHandler` current metadata recovers the same 35-method surface, including:

- signals/actions: `publishGameAction`, close/up/seek/get-object-info/container-action, stash dialog and depot widget requests;
- inventory handlers: `handleSetInventoryMessage`, `handleDeleteInventoryMessage`, `handlePlayerInventoryMessage`;
- container handlers: `handleContainerMessage`, close/change/delete/create/object-info/stash/special-containers/depot result/detail/close;
- requests: close/up/next-page/previous-page/update/get-objects-info/get-object-info/sort/move-content-to-managed-containers.

`requestSortContainer` has QMeta argc `4`; `requestMoveContentToManagedContainers` has argc `2`.

### Container storage/controller

`TContainerStorage` current signals are `containerUpdated(argc=2)`, `containerRemoved(argc=1)`, and `manualSortModeChanged(argc=0)`.

`TContainerStorageController` contains `containerRemovedFromStorage` plus slots `onContainerUpdated(argc=2)`, `onContainerRemoved(argc=1)`, `onOptionsChanged`, `onDisplayContainerAsynchronousTriggerd`, and `onManualSortModeChanged`.

This is stronger structural adjacency than a class-name census, but the actual Qt connection establishing storage→controller propagation remains to be proven by code/live correlation.

### Appearance / item metadata / proficiency

`TAppearanceTypeHelperQmlService` current methods are exactly:

- `getObjectAppearanceTypeNameForID(argc=1)`;
- `getObjectAppearanceTypeDescriptionForID(argc=1)`;
- `getObjectAppearanceTypeIDByName(argc=1)`.

`TObjectAppearanceInstanceInfoQmlType` has properties `cumulativeCount`, `liquidType`, `hookDirection`, `decoItemObjectID`.

`TItemInfoDialogController` has 33 methods/17 signals/21 properties. Recovered properties include `hasWeaponProficiency`, `inspectData`, NPC sell/buy data, market/user/loot value strings, tracking, loot blacklist state, tier/classification selection and available classifications.

`TProficiencyProtocolMessageHandler` contains `sendWeaponProficiencyCommand`, `sendInspectObject`, weapon proficiency message/notification handlers, shaped-perk offers, and resource balance handling. `TProficiencyStorage` exposes `unspentPerkChanged`, `currentProficiencyProgressChanged`, `proficiencyDataChanged`, `resourceBalanceChanged`, and `shapedPerkReshapeOffersChanged`.

### Stash

`TStashDialogController` current methods include `showDialog`, `closeDialog`, `resetFilters`, `slotClicked(argc=3)`, `requestOpenManageQuickLootDialog`, `onRequestShowStashMessageDialog`, `onStashContentChanged`, and `handleGameAction`. Properties: `stashModel`, category/trader filter models, name/category/trader filter values and `sortOrder`.

### Depot search

`TDepotSearchWidgetController` current metadata recovers 34 methods and 23 properties. High-value methods include `requestCategorySelect(argc=6)`, `requestNameSelect(argc=6)`, `requestItemSelect(argc=2)`, `requestItemChosen(argc=2)`, classification/tier/NPC filter handlers, `requestSearch`, `requestRefresh`, `requestRetrieveFromStash`, `requestRetrieveFromDepotInbox`, and slot interaction methods.

Properties include `totalCountDepot`, `totalCountStash`, `totalCountInbox`, string variants of those totals, `isAppearanceAllowedToRetrieve`, `showLockerOnly`, tier/classification selection state, and NPC filter state.

### Managed containers / Quick Loot / Obtain Container

`TManagedContainerStorage` signals:

- `managedContainersUpdated`;
- `useMainBackpackAsFallbackChanged`.

`TManagedContainersProtocolMessageHandler` current methods:

- signals `sendQuickLoot(argc=1)`, `sendManagedContainer(argc=1)`, `sendQuickLootBlackWhitelist(argc=1)`;
- `handleUpdateManagedContainersMessage(argc=1)`;
- `onQuickLootBlackWhitelistConfigurationChanged(argc=0)`.

`TLootContainerQMLInfo` recovers separate loot/obtain state and actions: loot/obtain set + appearance-ID change signals; select/clear/open signals for both roles; matching click handlers. Properties are `categoryName`, `isLockedByPremium`, `isLootContainerSet`, `lootContainerAppearanceTypeID`, `isObtainContainerSet`, `obtainContainerAppearanceTypeID`.

`TManageLootContainerDialogController` includes `useMainBackpackAsFallbackChanged`, loot blacklist state, select/clear/open handlers for both loot and obtain roles, and properties `isPremium`, `lootContainers`, `blackWhiteListType`, `listItems`, `useMainBackpackAsFallback`, `filterString`.

`TQuickLootGameActionHandler` current methods include `handleQuickLootAction`, select/clear/open loot-container actions, select/clear/open obtain-container actions, `handleSetLootContainerFallbackAction`, and add/remove blacklist-status actions.

## Evidence boundary

### FACT

- 21/21 selected current QMeta objects were recovered from current ELF metadata without historical-address lookup;
- all 21 method/signal/property/enum count tuples equal the historical exact-build tuples;
- all 21 QMeta record VAs changed and all 21 static-metacall VAs changed;
- method names, arg counts and property names listed above are current-build QMeta metadata facts.

### INFERENCE

- unchanged Qt surface shapes plus unchanged semantic method/property names provide strong architectural-continuity evidence.

### UNKNOWN / NOT_OBSERVED

- actual QObject connection edges where a sender/receiver relation has not been recovered;
- internal C++ field layouts/ABI identity;
- message payload normalization and serialization beyond named QMeta action boundaries;
- authoritative live state/effects and restart stability.

Historical addresses must remain historical-only; the current addresses in this file must also be re-fenced after the next client update.
