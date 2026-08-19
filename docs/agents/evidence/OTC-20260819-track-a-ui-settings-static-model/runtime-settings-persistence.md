# Current-build UI settings persistence proof

Date: 2026-08-19 (Europe/Warsaw)  
Task: `OTC-20260819-track-a-ui-settings-static-model`  
Alias: `TIBIA-RE-UI-SETTINGS`  
Researcher delivery: Draft-only; coordinator-only promotion

## Scope and subject fence

This report closes the researcher's remaining causal settings-persistence discriminator on the official native Linux Tibia client. The positive experiment ran on the Synology host through a task-owned `ephemeral_isolated` runtime, not the canonical KasmVNC/login session.

Exact official-client subject:

```yaml
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
runtime_base_main: 5940913a325288cfd9985be54af1a56b65e5560e
runner: synology-otclient-01
machine: bc3917480db1
runtime_access: ephemeral_isolated
canonical_state_access: NONE
login_attempted: false
credentials_used: false
gameplay_attempted: false
```

`main` advanced after the runtime experiment to `6071b237d70a11ab10e5050cc23730162b0e7e0b` via #551. #551 changed only world-minimap evidence/report/archive paths and does not overlap this task.

## Positive causal experiment: Master Volume

The selected reversible option was the pre-login Options-page **Master Volume** slider. It was chosen because it is non-network-critical, non-renderer-critical, does not require an account or character, has direct visual readback, and has an exact inverse back to the original value.

The shared physical input lock `/tmp/otclient-track-a-gui-input.lock` was held for every mouse/keyboard stimulus.

### FACT — baseline

A new isolated runtime was created with:

```text
namespace: /home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260819-track-a-ui-settings-static-model/ephemeral-9999001-1-v2
display: :271
window: 2097169
initial exact-client PID: 22149
baseline window size: 1020x650
```

The real Welcome/Login UI was visible; no account login was performed. Opening the visible Options button showed **Master Volume: 100%**.

The copied runtime's baseline persistence file was:

```text
.local/share/CipSoft GmbH/Tibia/packages/Tibia/conf/clientoptions.json
size: 158761
sha256: b545e59f01e908b12c878753b0f49514854c601d5e83159a5da8d0ae8b491251
```

### FACT — reversible write and immediate readback

A slider click changed the real Options UI from **100%** to **43%**. The on-screen readback immediately displayed `Master Volume: 43%`.

Clicking `Apply` preserved the 43% UI value but did not yet change the known persistence file. Clicking `OK` committed the option and changed `conf/clientoptions.json` to:

```text
size: 158758
sha256: d84081c78d634ca69897dd3eb15a5257f1445b3ba7f034e4fd449275e0538309
```

A bounded JSON diff against the untouched exact source-package baseline identified exactly two sound/volume fields changed by this persisted state:

```text
options.soundMasterVolume:    100 -> 43
options.soundMasterVolumeOld: 100 -> 43
```

No full configuration content, credential material or private account state was emitted.

### FACT — first restart persistence

The client was closed through the real pre-login Exit control. The task-owned Xvfb/WARP/HOME remained alive for the persistence restart.

The exact same client was launched again with the same isolated HOME:

```text
exact-client PID: 23325
window: 2097169
window size: 1020x650
```

After restart, the real Options UI displayed **Master Volume: 43%**. The persisted JSON fields were still semantically 43/43. The file-level SHA changed during normal startup/exit bookkeeping, so whole-file hash equality is intentionally **not** used as the semantic persistence criterion; the exact option fields and UI readback are.

This establishes the causal chain:

```text
UI Master Volume 100
-> UI write 43
-> OK commit
-> clientoptions.json soundMasterVolume = 43
-> clean client restart with same HOME
-> UI Master Volume 43
```

### FACT — exact rollback and second restart

The same Options slider was returned to **100%**. The immediate UI readback showed `Master Volume: 100%`.

After `OK`, the persistence file was:

```text
size: 158771
sha256: 168ba60edfd417b66bd9980e0a6c38ddc1c7092cac3f42a157b0c15ad52ea02c
options.soundMasterVolume: 100
options.soundMasterVolumeOld: 100
```

After a clean exit, both fields remained 100. The exact same client was launched a third time with the same isolated HOME:

```text
exact-client PID: 23714
window: 2097169
window size: 1020x650
```

Final restart readback:

```text
UI Master Volume: 100%
options.soundMasterVolume: 100
options.soundMasterVolumeOld: 100
```

Therefore the full reversible acceptance chain is proven for this setting:

```text
safe read 100
-> reversible UI write 43
-> immediate UI readback 43
-> persistence sink + exact fields identified
-> restart readback 43
-> inverse UI write 100
-> persisted fields restored 100/100
-> second restart readback 100
```

## Cleanup and side-effect boundary

After final readback, the task-owned runtime was stopped by its cleanup trap. Direct terminal verification returned:

```text
UI_SETTINGS_MANUAL_MARKER_PROCESS_COUNT=0
UI_SETTINGS_MANUAL_ROOT_CLEANED=true
UI_SETTINGS_MANUAL_DISPLAY_CLEANED=true
UI_SETTINGS_V2_CLEANUP=COMPLETE
UI_SETTINGS_HOST_SCREENSHOT_TEMP_CLEANUP=COMPLETE
```

Temporary XWD/JPEG observation files were deleted from the Synology host and were not committed. No canonical Track A registration, lease, KasmVNC state, account login, credential, character/world state, purchase, transfer, gameplay action or shared source-package mutation was used.

## Negative controls and superseded discriminators

### FACT — fullscreen persistence candidate disproven

`Alt+Return` / `ToggleFullscreen` was tested first because static evidence exposed that action. After removing dynamic cache false positives, run `32221978132`, physical job `95974034787`, produced:

```text
UI_SETTINGS_V2_CURRENT_EXACT_SOURCE_PACKAGE=PASS
UI_SETTINGS_V2_COPIED_CLIENT_FENCE=PASS
UI_SETTINGS_V2_XVFB_EMPTY_DISPLAY=PASS
UI_SETTINGS_V2_CLIENT_START_1=PASS;PID=21428;START_TICKS=73847371
UI_SETTINGS_V2_BASELINE_WINDOW_SIZE=1020x650
UI_SETTINGS_V5_INPUT_1_ALT_RETURN_SENT=PASS
UI_SETTINGS_V5_POST_STOP_CANDIDATE_DELTA_COUNT=0
UI_SETTINGS_V5_SEMANTIC_NEGATIVE=NO_PERSISTENCE_CANDIDATE_DELTA_AFTER_ALT_RETURN_AND_CLIENT_STOP
UI_SETTINGS_V2_CLEANUP=COMPLETE
```

**DISPROVEN for this pre-login isolated state:** `Alt+Return` is not a useful persistence discriminator. This does not disprove the existence of fullscreen UI behavior in other runtime/window-manager contexts.

### FACT — cache false positives rejected

Earlier run `32221521375`, job `95972797342`, initially found three restart-stable JSON files after fullscreen input, but all were under `packages/Tibia/cache/` (`boostedcreature.json`, `eventschedule.json`, `onlinenumbers.json`) and did not respond to inverse input. They were classified as dynamic background cache and excluded before the terminal fullscreen negative control.

## Model consequence

### FACT

For the exact current official client build above, the following concrete high-level topology is now proven for Master Volume:

```text
pre-login Options UI / Sound / Master Volume
-> persisted option state
-> packages/Tibia/conf/clientoptions.json
-> options.soundMasterVolume
-> options.soundMasterVolumeOld
-> reload on next client start
```

The same setting has a demonstrated exact rollback path.

### INFERENCE

This is strong runtime evidence for H11 (audio/sound settings) and H14 (options persistence). It also converts the earlier static `clientoptions.json` artifact from an unresolved persistence candidate into a proven persistence sink for at least this concrete sound option.

### UNKNOWN

This experiment does **not** prove that every H10-H13 option uses `clientoptions.json`, nor that all UI settings share the same save timing (`Apply` versus `OK`/close), profile/migration rules, character-specific configuration behavior, or QSettings relationship. Those claims remain setting-specific until separately tested.

## Researcher coverage recommendation — no self-promotion

**RECOMMENDATION:** coordinator/fresh-validator review may promote H11/H14 from static-only evidence to causal runtime-backed evidence for the Master Volume persistence path. H10-H13 should not be globally marked complete merely because one sound option is proven.

The researcher does not modify the canonical coverage matrix and does not merge its own Draft PR.
