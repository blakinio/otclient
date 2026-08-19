# TIBIA-RE-INVENTORY-CONTAINERS — current-package static revalidation

```yaml
task: OTC-20260819-track-a-inventory-containers-runtime
alias: TIBIA-RE-INVENTORY-CONTAINERS
trusted_main: 2e572789a2bc4b64c5e906c4515c15c625f6bc9e
fence_merge_pr: 555
fence_merge_commit: 2e572789a2bc4b64c5e906c4515c15c625f6bc9e
runtime_access: none
client_executed: false
login: false
credentials_used: false
gui_input: false
process_mutation: false
raw_proprietary_client_retained: false
```

## FACT — exact current public package

A fresh task-local, non-secret fetch of the official current Linux launcher package was performed through the already-provisioned userspace WARP transport. The package was decoded only for bounded static inspection and the packed/unpacked proprietary bytes were deleted immediately after evidence extraction.

```yaml
packed_size: 10214529
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked_size: 52109920
unpacked_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
embedded_version_token: '15.32'
lzma_envelope: offset=45,lc=3,lp=0,pb=2,dict_size=33554432
```

The unpacked identity exactly matches the current Track A fence merged by #555. The client was **not executed**.

## FACT — D09-D22 selected-anchor revalidation

Every selected structural anchor used by this task persists in the current `ed5469b9...` package:

| ID | selected anchors | result |
|---|---:|---|
| D09 | 9 | **9/9 PASS** |
| D10 | 7 | **7/7 PASS** |
| D11 | 4 | **4/4 PASS** |
| D12 | 4 | **4/4 PASS** |
| D13 | 6 | **6/6 PASS** |
| D14 | 6 | **6/6 PASS** |
| D15 | 4 | **4/4 PASS** |
| D16 | 9 | **9/9 PASS** |
| D17 | 7 | **7/7 PASS** |
| D18 | 5 | **5/5 PASS** |
| D19 | 7 | **7/7 PASS** |
| D20 | 9 | **9/9 PASS** |
| D21 | 8 | **8/8 PASS** |
| D22 | 7 | **7/7 PASS** |

This proves **selected structural-anchor persistence on the current build**, not historical address/QMeta-count equivalence and not live behavior.

### Representative exact current-package offsets

- D09: `receivedSetInventoryMessage` `0x1cea810`; `receivedDeleteInventoryMessage` `0x1ceb372`; `receivedPlayerInventoryMessage` `0x1cec8af`; matching handler-name strings at `0x1ccd23f`, `0x1ccd2a6`, `0x1ccd316`.
- D10/D11: `TInventoryContainer` `0x1d12e20`; `TPlayerInventoryAndStatusController` `0x1d12de0`; `inventoryChanged` `0x1d13db6`; `onInventoryChanged` `0x1d139a5`.
- D12: `TAppearanceTypeHelperQmlService` `0x1fe7bc0`; `getObjectAppearanceTypeNameForID` `0x1ff4b9a`; `getObjectAppearanceTypeDescriptionForID` `0x1ff4bbf`; `getObjectAppearanceTypeIDByName` `0x1ff4be7`.
- D13: `TObjectAppearanceInstanceInfoStorage` `0x1d632a0`; `TObjectCountStorage` `0x1d45bc0`; `TItemInfoDialogController` `0x1d39c40`; `objectInfosChanged` `0x1d635eb`; `objectCountsChanged` `0x1d45c96`.
- D14: `TProficiencyStorage` `0x1cb89e0`; `TProficiencyProtocolMessageHandler` `0x1ccc2c0`; `receivedWeaponProficiencyMessage` `0x1cedb2c`; notification `0x1cee733`.
- D15: `TContainerStorage` `0x1d034e0`; `TContainerStorageController` `0x1c8d160`; `containerUpdated` `0x1d0362c`.
- D16: Create/Change/Delete receive strings at `0x1ceb20a`, `0x1ceb282`, `0x1ceb2fa`; handler strings at `0x1ccd527`, `0x1ccd43b`, `0x1ccd4b1`.
- D17: close/up/page request strings at `0x1ccd8c2`, `0x1ccd903`, `0x1ccd916`, `0x1ccd932`; `sendOpenParentContainer` `0x1ccfaee`.
- D18: `sendGetObjectInfoMessage` `0x1ccd0d0`; `requestGetObjectsInfo` `0x1ccd969`; `requestSortContainer` `0x1ccda77`.
- D19: `TStashDialogController` `0x1c90dc0`; `receivedStashMessage` `0x1ced8d4`; `handleStashMessage` `0x1ccd5fe`; `sendStashAction` `0x1ccf95b`.
- D20: `TDepotSearchWidgetController` `0x1d0b640`; `TDepotSearchDetailListStorage` `0x1d4e580`; result/detail/close protocol strings at `0x1ccd791`, `0x1ccd80b`, `0x1ccd888`.
- D21: `TManagedContainerStorage` `0x1d418c0`; `TManagedContainersProtocolMessageHandler` `0x1ccc000`; `receivedUpdateManagedContainersMessage` `0x1ced609`.
- D22: `TQuickLootGameActionHandler` `0x1cf4020`; `TQuickLootBlackWhitelistStorage` `0x1dab520`; `TLootContainerQMLInfo` `0x1d41a00`; `TManageLootContainerDialogController` `0x1c90cc0`.

## Current-build semantic lexical strengthening

### D13 — object/item metadata

The current package exposes directly adjacent QML/model fields including:

- `TContainerSlotQmlInformation`: `slotID`, `objectID`, `objectCount`, `upgradeTier`, `liquidType`, `hookDirection`, `decoItemObjectID`;
- action-button object metadata: `objectID`, `objectCount`, `objectUpgradeTier`, `liquidType`, `hookDirection`;
- `TInspectObjectQMLData`: `objectName`, `objectInformation`, `appearanceID`, `objectCount`, `objectUpgradeTier`, `slotID`, `hasProficiency`;
- additional current-package literals: `proficiencyXP`, `proficiencyLevel`, `hasProficiencyMastery`, `remainingDurationMilliseconds`, `totalDurationMilliseconds`, `market_stats_charges`, `market_stats_tier`.

**Boundary:** this strengthens the static semantic model for count/tier/proficiency/duration/charge-related metadata. It does not by itself prove the exact protocol field mapping, subtype normalization, charge semantics, or authoritative live values.

### D20 — depot filtering surface

The current `TDepotSearchWidgetController` lexical neighborhood includes `showLockerOnlyChanged`, `filterChanged`, `typeIdEnumValue`, `filterByLevel`, `filterByVocation`, `onlyOneHandWeapons`, and `onlyTwoHandWeapons`.

**Boundary:** filter/control presence is FACT; query serialization/result semantics remain UNKNOWN.

### D21/D22 — managed, loot and obtain containers

The current package places `TManagedContainerStorage` with `managedContainersUpdated` and `useMainBackpackAsFallbackChanged`. `TLootContainerQMLInfo` exposes separate state/actions for loot and obtain containers:

- `isLootContainerSetChanged`, `lootContainerAppearanceTypeIDChanged`;
- `isObtainContainerSetChanged`, `obtainContainerAppearanceTypeIDChanged`;
- `requestSelectLootContainer`, `requestClearLootContainer`, `requestOpenLootContainer`;
- `requestSelectObtainContainer`, `requestClearObtainContainer`, `requestOpenObtainContainer`;
- `categoryName`, `isLockedByPremium`, `isLootContainerSet`, `lootContainerAppearanceTypeID`, `isObtainContainerSet`, `obtainContainerAppearanceTypeID`.

The current `TQuickLootGameActionHandler` context also retains `TGameActionSelectLootContainer`, `TGameActionQuickLoot`, `handleSetLootContainerFallbackAction`, `TGameActionSetLootContainerFallback`, `handleAddToBlackWhitelistStatusAction`, `TGameActionToggleBlackWhitelistStatus`, and `handleRemoveFromBlackWhitelistStatusAction`.

**Boundary:** existence and lexical ownership are FACT. Category-to-container serialization, server acknowledgement, live fallback behavior and whitelist/blacklist effects remain NOT_OBSERVED.

## Classification

### FACT

- current public-package identity above;
- all selected D09-D22 anchor sets are present on the current build;
- current-package QML/model/action lexical fields listed above;
- no client execution, login, credentials, GUI input or runtime mutation occurred;
- raw packed/unpacked client bytes were deleted after bounded evidence extraction.

### INFERENCE

- persistence of the same semantically named surfaces strongly supports architectural continuity from the historical G0 package, but it does not prove identical internal addresses, method counts, ABI layout or connection wiring.

### UNKNOWN / NOT_OBSERVED

- exact current queue → handler → storage → controller causal wiring;
- authoritative live inventory/equipment/container/stash/depot/managed/quick-loot state;
- per-action serialization and causal server/client effects;
- exact subtype/charges/duration normalization;
- restart/relogin stability.

## Live continuation boundary

PR #555 is now merged, but its own acceptance contract requires live consumers to re-read trusted `main` and perform a **fresh later-invocation admission** before using the new live authority. This invocation therefore intentionally remains `runtime_access: none` and does not attempt Gate A/rebind/Gate B or GUI stimulation.
