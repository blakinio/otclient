# Coordinator promotion — TIBIA-RE-UI-SETTINGS

Date: 2026-08-19 (Europe/Warsaw)  
Coordinator base: `main@be07623155ac81fa69d618cf277232f6825a7d9e`  
Source Draft: PR #544  
Source head reviewed: `7861752c312f77fad0cde28c44c8745aa2806909`  
Source task: `OTC-20260819-track-a-ui-settings-static-model`  
Alias: `TIBIA-RE-UI-SETTINGS`

## Coordinator decision

**PASS WITH SCOPE NARROWING.**

The coordinator independently re-read the source Draft from the exact source head, rechecked its final changed-file set, final workflow results, exact current-client fence, static evidence, runtime persistence evidence, negative controls, rollback and cleanup. The source is accepted for canonical promotion only at the claim granularity below.

The coordinator did **not** replay a second settings mutation. The promoted runtime claim is bounded to a single reversible causal experiment whose before/write/readback/restart/inverse/restart/cleanup sequence is internally falsifiable and whose source researcher had already dropped runtime authority before final exact-head validation.

## Source identity and final validation

Final source head:

```text
7861752c312f77fad0cde28c44c8745aa2806909
```

Final source PR #544 changed exactly seven task-owned paths and contained no temporary V1-V6 physical-runtime workflow.

Exact-head source validation:

```text
Track A agent runtime governance: run 32223847502 = SUCCESS
Track A UI/settings static model: run 32223847653, job 95979454027 = SUCCESS
CI: run 32223847815, CI / Required = SUCCESS
```

Final static job independently reproduced:

```text
packed_size=10214529
packed_sha256=1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
client_size=52109920
client_sha256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id=d803d9695868713ef6ab0c3cf65f91212c9c6a62
clientoptions_literal_count=1
clientoptions_code_xref_count=38
qsettings_plt_count=4
qsettings_direct_call_count=51
key_adjacency_scan=PASS
proprietary_binary_retained=false
```

## Exact source evidence reviewed

The coordinator reviewed these exact source blobs:

```text
docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/runtime-settings-persistence.md
blob 26d8765f971b98451578f40bc134cbd214848a67

docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/current-build-static-model.md
blob 909da4dd5825efa5f90187158bf8be5a55226d10

docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h07-h09-actionbar-hotkey-multiaction.md
blob 44fbdc4c52a6ec4ab6e1afb51216553e66c0d40d

docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/persistence-xrefs.md
blob 314c823f874f10c3ec862d68cf3222f3433ed152

docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h01-h06-h15-h19-static-refresh.md
blob 4706cce1091ecb2cd5dd8cf40a0ebea3dc0495da
```

## Promoted FACT — exact current-client build fence

```yaml
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
```

## Promoted FACT — H07-H13 compiled model surfaces

For this exact build the source proves dedicated compiled model/controller surfaces for:

- H07 action bars: `TActionBarOptions`, `TActionBarsQMLOptionsPage`, `TActionBarGroup`, `TActionBarManager`, `TActionBarController`, action-bar change paths;
- H08 hotkeys: `THotkeysQMLOptionsPage`, `EHotkeyMode`, `TTibiaHotkeyActionSettingQmlWrapper`, keyboard shortcut record/handler surfaces;
- H09 multi-action/cooldown: `TMultiActionPrioritySolver::IAction`, `TCooldownStorage`, `TCooldownBarController`, `TCooldownProgressDataForQML`;
- H10 graphics settings: `TGraphicsQMLOptionsPage`, graphics options vocabulary, restart-sensitive graphics text, renderer-adjacent QSettings read/write callsites;
- H11 sound settings: `TSoundQMLOptionsPage`, UI/battle sound option pages, sound configuration/controller families;
- H12 interface settings: `TInterfaceQMLOptionsPage`, `TSidebarOptions`, action-bar/sidebar managers/controllers;
- H13 gameplay/controls: `TControlsQMLOptionsPage`, `TGameplayQMLOptionsPage`, keyboard shortcut and movement input components.

These are exact-current-build **STATIC** facts. They do not make H07-H10/H12-H13 runtime-complete.

## Promoted FACT — H11/H14 causal Master Volume persistence path

A fresh task-owned `ephemeral_isolated` Synology runtime used the exact build above, no canonical session, no login, no credentials and no gameplay. Every real UI stimulus was serialized through `/tmp/otclient-track-a-gui-input.lock`.

The accepted causal chain is:

```text
pre-login Options / Sound / Master Volume = 100%
-> real UI slider write to 43%
-> immediate UI readback = 43%
-> OK commit
-> packages/Tibia/conf/clientoptions.json
-> options.soundMasterVolume = 43
-> options.soundMasterVolumeOld = 43
-> clean restart using the same isolated HOME
-> UI readback = 43%
-> inverse UI write to 100%
-> OK commit
-> both persisted fields = 100
-> clean second restart using the same HOME
-> final UI readback = 100%
-> both persisted fields = 100
```

The baseline copied `clientoptions.json` was size `158761`, SHA256 `b545e59f01e908b12c878753b0f49514854c601d5e83159a5da8d0ae8b491251`. The first committed 43% state was size `158758`, SHA256 `d84081c78d634ca69897dd3eb15a5257f1445b3ba7f034e4fd449275e0538309`.

Whole-file SHA equality across restart is **not** promoted as persistence semantics because normal client bookkeeping can change unrelated fields. The promoted semantic anchors are the exact two volume fields plus the corresponding real UI readback across restart.

## Promoted FACT — cleanup / no shared-state mutation

Terminal cleanup verification from the positive experiment:

```text
UI_SETTINGS_MANUAL_MARKER_PROCESS_COUNT=0
UI_SETTINGS_MANUAL_ROOT_CLEANED=true
UI_SETTINGS_MANUAL_DISPLAY_CLEANED=true
UI_SETTINGS_V2_CLEANUP=COMPLETE
UI_SETTINGS_HOST_SCREENSHOT_TEMP_CLEANUP=COMPLETE
```

No canonical KasmVNC/login session, account credential, character/world state, gameplay, purchase, transfer or shared source-package mutation was used.

## Promoted negative control

`Alt+Return` / fullscreen is **DISPROVEN as a persistence discriminator in this pre-login isolated state**. In final cache-excluded run `32221978132`, physical job `95974034787`, real input was sent to the exact current client but the post-stop non-cache persistence candidate delta was exactly zero:

```text
UI_SETTINGS_V5_INPUT_1_ALT_RETURN_SENT=PASS
UI_SETTINGS_V5_POST_STOP_CANDIDATE_DELTA_COUNT=0
UI_SETTINGS_V5_SEMANTIC_NEGATIVE=NO_PERSISTENCE_CANDIDATE_DELTA_AFTER_ALT_RETURN_AND_CLIENT_STOP
UI_SETTINGS_V2_CLEANUP=COMPLETE
```

Earlier restart-stable JSON candidates were all dynamic package cache files and are rejected as causal settings evidence.

## Coordinator coverage mapping

This promotion deliberately does not edit PR #536 because that checklist is a separately owned/shared coordination surface. The following mapping is for the matrix owner:

```yaml
H07: exact-current-build dedicated STATIC model evidence; not runtime-complete
H08: exact-current-build dedicated STATIC model evidence; not runtime-complete
H09: exact-current-build dedicated STATIC model evidence; not runtime-complete
H10: exact-current-build STATIC options model + renderer-adjacent QSettings code evidence; user-option runtime persistence still unproven
H11: exact-current-build STATIC sound model + CAUSAL RUNTIME Master Volume persistence path proven
H12: exact-current-build dedicated STATIC interface model evidence; runtime persistence unproven
H13: exact-current-build dedicated STATIC gameplay/control model evidence; runtime persistence unproven
H14: exact-current-build persistence mechanisms + CAUSAL RUNTIME clientoptions.json persistence proven for Master Volume only
```

Lower-priority H02/H04/H05/H06/H15 and passive lexical H18 may be retained as exact-build compiled-presence leads only. H01/H03/H16/H17 semantic state and H19 remain unresolved by this task.

## INFERENCE accepted with scope fence

For the concrete Master Volume option, `packages/Tibia/conf/clientoptions.json` is a real persistence sink loaded on subsequent client start. This resolves the earlier static `clientoptions.json` ambiguity for this setting only.

## UNKNOWN / explicitly not promoted

- whether every H10-H13 option uses `clientoptions.json`;
- whether all settings commit on `OK`, `Apply`, close or another trigger;
- complete global versus character-specific profile boundaries;
- migration/versioning semantics;
- high-level relation between user-facing H10-H13 options and the separate renderer-adjacent `QSettings` clusters;
- runtime semantics for action bars, hotkeys, multi-actions, graphics, interface and gameplay settings beyond the one sound option.

## Promotion outcome

Coordinator result: **ACCEPTED WITH SCOPE NARROWING**.

The source Draft #544 remains unmerged. After this promotion PR is merged, #544 should be closed as superseded and the task archive should be finalized with promotion/merge/CI identifiers.