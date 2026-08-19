# OTCLIENT Track A — UI/settings current-build report

Date: 2026-08-19  
Programme: `OTCLIENT-TIBIA-RE`  
Alias: `TIBIA-RE-UI-SETTINGS`  
Coordinator promotion source: PR #544 at `7861752c312f77fad0cde28c44c8745aa2806909`

## Status

This report promotes bounded, independently reviewed evidence for current official-client UI/settings models and one causal persistence path. It does **not** claim that all H07-H14 settings semantics are complete.

## Exact official-client fence

```yaml
packed_size: 10214529
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
```

## FACT — H07 action bars

The exact current binary contains dedicated action-bar configuration/controller structures including `TActionBarOptions`, `TActionBarsQMLOptionsPage`, `TActionBarGroup`, `TActionBarManager`, `TActionBarController`, `EActionBarPosition` and action-bar option change signals.

**Boundary:** exact assignment schema, runtime mutation behavior and restart persistence are not proven by this task.

## FACT — H08 hotkeys

The exact current binary contains `THotkeysQMLOptionsPage`, `EHotkeyMode`, `TTibiaHotkeyActionSettingQmlWrapper`, `EHotkeyUseObjectType`, shortcut handler/recorder components and hotkey option change paths.

**Boundary:** binding serialization, profile scope and conflict/precedence runtime semantics are not proven.

## FACT — H09 multi-action and cooldown

The exact current binary contains explicit multi-action and cooldown components including `TMultiActionPrioritySolver::IAction`, `TGameActionCloseAllMultiActionButtons`, `TCooldownStorage`, `TCooldownBarController` and `TCooldownProgressDataForQML`.

**Boundary:** slot association, priority semantics and runtime lifecycle are not proven.

## FACT — H10 graphics options

The exact current binary contains `TGraphicsQMLOptionsPage`, `graphicsOptions`, antialiasing vocabulary and graphics restart-warning text. Static code analysis also finds real `QSettings` read/write callsite clusters adjacent to Qt renderer/Vulkan backend selection/probing.

**Boundary:** this does not connect a specific user-visible graphics option to those `QSettings` calls or prove user-option restart persistence.

## FACT — H11 sound options

The exact current binary contains dedicated general/UI/battle sound option pages and multiple sound configuration/controller families.

A causal runtime path is proven for **Master Volume**:

```text
Options / Sound / Master Volume = 100%
-> UI write 43%
-> immediate readback 43%
-> OK
-> packages/Tibia/conf/clientoptions.json
-> options.soundMasterVolume = 43
-> options.soundMasterVolumeOld = 43
-> restart same HOME
-> UI Master Volume = 43%
-> inverse write 100%
-> both persisted fields = 100
-> second restart
-> UI Master Volume = 100%
```

This is exact-current-build causal persistence evidence with exact rollback.

## FACT — H12 interface/sidebar settings

The exact current binary contains `TInterfaceQMLOptionsPage`, `TSidebarOptions`, action-bar/sidebar managers/controllers and dedicated option change paths.

**Boundary:** per-character/global partition and runtime persistence are not proven.

## FACT — H13 gameplay/control settings

The exact current binary contains `TControlsQMLOptionsPage`, `TGameplayQMLOptionsPage`, keyboard shortcut components and player movement intent/interpreter components.

**Boundary:** concrete option-to-`EClientOption` mapping, local/protocol split and restart persistence are not proven.

## FACT — H14 persistence mechanisms

Static current-build evidence establishes:

- `TClientOptions`, `EClientOption`, `TClientOptionsModeSwitcher`, option-page wrappers and character configuration structures;
- one `clientoptions.json` literal with 38 decoded executable references;
- four used `QSettings` read/write/group targets with 51 direct callsites;
- JSON/file-helper surfaces.

Runtime evidence resolves one previously unknown relationship:

```text
Master Volume UI
-> packages/Tibia/conf/clientoptions.json
-> options.soundMasterVolume
-> options.soundMasterVolumeOld
-> reload on next client start
```

**Boundary:** this relationship is proven for Master Volume only. It does not imply every H10-H13 setting uses this file or that the renderer-adjacent `QSettings` clusters are the same persistence mechanism.

## Negative control — fullscreen

`Alt+Return` was initially evaluated as a low-risk persistence discriminator. After excluding dynamic `packages/Tibia/cache/` false positives, final run `32221978132`, job `95974034787`, produced zero non-cache persistence candidate delta after real input and client stop.

**DISPROVEN:** fullscreen is not a useful persistence discriminator in the tested pre-login isolated state. This is not a general claim that fullscreen behavior does not exist in other window-manager/runtime contexts.

## Lower-priority exact-build leads

Current-build compiled-presence evidence exists for:

- H02 `TDeathDialogController`;
- H04 `TContextMenuController`;
- H05 structured dialog/controller stack;
- H06 `TDragAndDropController`;
- H15 structured sound storage/protocol/controller family;
- H18 lexical `TAntiCheatController` presence only.

H01, H03, H16, H17 semantic state and H19 remain unresolved by this task.

## Evidence classification for matrix owner

```yaml
H07: PARTIAL_STATIC_DEDICATED_MODEL
H08: PARTIAL_STATIC_DEDICATED_MODEL
H09: PARTIAL_STATIC_DEDICATED_MODEL
H10: PARTIAL_STATIC_MODEL_AND_CODE_PERSISTENCE_CONTEXT
H11: PARTIAL_WITH_CAUSAL_RUNTIME_MASTER_VOLUME_PATH
H12: PARTIAL_STATIC_DEDICATED_MODEL
H13: PARTIAL_STATIC_DEDICATED_MODEL
H14: PARTIAL_WITH_CAUSAL_RUNTIME_CLIENTOPTIONS_PATH_FOR_MASTER_VOLUME
```

These labels are a coordinator report mapping, not a direct mutation of the separately owned PR #536 checklist.

## Proven safety / cleanup boundary

The positive runtime experiment used a fresh task-owned isolated HOME/display on `synology-otclient-01`, did not use login/credentials/gameplay/canonical session state, serialized physical input with `/tmp/otclient-track-a-gui-input.lock`, restored the original Master Volume value and ended with:

```text
marker-owned process count = 0
task root removed = true
isolated display removed = true
temporary observation images removed = true
```

## UNKNOWN / follow-up

Remaining setting-specific research must separately prove any desired runtime semantics for graphics, interface, gameplay, hotkeys/action bars/multi-actions, profile/migration behavior and any relation between user-facing options and renderer `QSettings` state. No broad `DONE` claim follows from the Master Volume proof.