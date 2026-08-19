# Current-build UI settings persistence proof

Date: 2026-08-19 (Europe/Warsaw)  
Task: `OTC-20260819-track-a-ui-settings-static-model`  
Alias: `TIBIA-RE-UI-SETTINGS`  
Coordinator disposition: **ACCEPT_WITH_EDITS**

## Scope and exact subject fence

This report records one bounded causal reversible persistence experiment on the official native Linux Tibia client plus the corrected interpretation of the earlier fullscreen candidate.

```yaml
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
runtime_base_main: 5940913a325288cfd9985be54af1a56b65e5560e
runner: synology-otclient-01
runtime_access_during_experiment: ephemeral_isolated
canonical_state_access: NONE
login_attempted: false
credentials_used: false
gameplay_attempted: false
```

The experiment used a task-owned HOME/display, not the canonical KasmVNC/login session. Every GUI stimulus used the shared `/tmp/otclient-track-a-gui-input.lock`.

## Evidence classes used here

- **FACT — coordinator independently verified**: direct deterministic repository/workflow evidence or primary Remote Desktop Commander command/result history was re-read by the coordinator.
- **SOURCE OBSERVATION**: researcher-captured visual UI readback recorded during the experiment; the coordinator verified the surrounding runtime/input/persistence sequence but did not independently re-read the temporary image pixels after those images were deleted.
- **INFERENCE**: conclusion from accepted facts, not a broader per-setting rule.
- **UNKNOWN**: not established and must not be generalized.

## Master Volume causal persistence

### FACT — isolated runtime and baseline persistence object

Primary Remote Desktop Commander history independently confirms the task-owned isolated runtime, exact current-client identity, unique task process/window, display `:271`, baseline window size `1020x650`, no canonical-state access, no login/credentials/gameplay, and use of the shared GUI-input lock.

The copied runtime baseline persistence file was:

```text
.local/share/CipSoft GmbH/Tibia/packages/Tibia/conf/clientoptions.json
size: 158761
sha256: b545e59f01e908b12c878753b0f49514854c601d5e83159a5da8d0ae8b491251
```

### FACT — committed semantic file delta

Primary command/result history independently confirms a real slider mutation followed by `Apply` and then `OK`. `Apply` did not change the known persistence file; `OK` changed it to:

```text
size: 158758
sha256: d84081c78d634ca69897dd3eb15a5257f1445b3ba7f034e4fd449275e0538309
```

A bounded JSON diff against the untouched exact source-package baseline identified exactly these two option changes:

```text
options.soundMasterVolume:    100 -> 43
options.soundMasterVolumeOld: 100 -> 43
UI_SETTINGS_VOLUME_JSON_DIFF_COUNT=2
```

No complete config, credential or private account material is persisted in this evidence record.

### FACT — persistence across restart

The client was cleanly closed and restarted with the same isolated HOME. Primary history independently confirms the replacement exact-client process/window and that, after restart, both semantic JSON fields remained `43`.

Whole-file hashes changed during normal startup/exit bookkeeping, so whole-file equality is deliberately not used as the semantic persistence criterion.

### FACT — inverse rollback and second restart

The same option was changed back through the UI and committed with `OK`. Primary history independently confirms:

```text
options.soundMasterVolume: 100
options.soundMasterVolumeOld: 100
```

After another clean restart with the same isolated HOME, both fields still read `100`.

### SOURCE OBSERVATION — UI readback

The researcher recorded visual UI readbacks consistent with the accepted semantic chain:

```text
Master Volume 100%
-> slider write 43%
-> immediate UI readback 43%
-> restart UI readback 43%
-> inverse write/readback 100%
-> second restart UI readback 100%
```

Temporary observation images were deleted during cleanup and are not durable artifacts, so the coordinator does not elevate the pixel-level readback above the source-observation class. The durable JSON/restart/rollback evidence is independently verified.

### Accepted causal topology

For this exact current build and this concrete sound option, the evidence establishes:

```text
pre-login Options / Sound / Master Volume stimulus
-> OK commit
-> packages/Tibia/conf/clientoptions.json
-> options.soundMasterVolume + options.soundMasterVolumeOld
-> values survive clean restart
-> inverse commit restores both fields
-> restored values survive a second restart
```

This is runtime-backed `PARTIAL` evidence for H11 and H14. It is not evidence that all audio/settings fields use the same sink or save timing.

## Cleanup and side-effect boundary

Primary history independently verifies terminal cleanup:

```text
UI_SETTINGS_MANUAL_MARKER_PROCESS_COUNT=0
UI_SETTINGS_MANUAL_ROOT_CLEANED=true
UI_SETTINGS_MANUAL_DISPLAY_CLEANED=true
UI_SETTINGS_V2_CLEANUP=COMPLETE
UI_SETTINGS_HOST_SCREENSHOT_TEMP_CLEANUP=COMPLETE
```

No canonical registration/lease/KasmVNC state, account session, purchase/transfer/gameplay state or shared source-package bytes were mutated.

## Fullscreen / Alt+Return — corrected negative control

### FACT

Run `32221978132`, physical job `95974034787`, established the exact copied client and isolated display and emitted:

```text
UI_SETTINGS_V2_CURRENT_EXACT_SOURCE_PACKAGE=PASS
UI_SETTINGS_V2_COPIED_CLIENT_FENCE=PASS
UI_SETTINGS_V2_XVFB_EMPTY_DISPLAY=PASS
UI_SETTINGS_V2_BASELINE_WINDOW_SIZE=1020x650
UI_SETTINGS_V5_INPUT_1_ALT_RETURN_SENT=PASS
UI_SETTINGS_V5_POST_STOP_CANDIDATE_DELTA_COUNT=0
UI_SETTINGS_V5_SEMANTIC_NEGATIVE=NO_PERSISTENCE_CANDIDATE_DELTA_AFTER_ALT_RETURN_AND_CLIENT_STOP
UI_SETTINGS_V2_CLEANUP=COMPLETE
```

Earlier restart-stable JSON candidates under `packages/Tibia/cache/` were correctly rejected as dynamic background cache false positives.

### Material audit correction `UISET-AUD-001`

The prior report called fullscreen persistence **DISPROVEN**. That is too strong.

Independent coordinator inspection of the experiment harness found that v2 contained an immediate `await_size_change` verification after `toggle_fullscreen_locked`, while v5/v6 cut that effect check and only performed candidate-file scans after sending `Alt+Return`.

Therefore v6 proves:

```text
Alt+Return command sent
AND
no observed non-cache candidate-file delta in the scan
```

but it does **not** prove:

```text
fullscreen state actually changed
```

Correct terminal classification:

```yaml
fullscreen_persistence_discriminator: INCONCLUSIVE
observed_candidate_file_delta: NONE
fullscreen_effect_proven: false
fullscreen_persistence_disproven: false
```

The fullscreen path remains useful negative/harness evidence, not a semantic disproof.

## Model consequence

### FACT

`packages/Tibia/conf/clientoptions.json` is a proven persistence sink for the exact Master Volume option on this build, with exact fields `options.soundMasterVolume` and `options.soundMasterVolumeOld` surviving restart and rollback.

### INFERENCE

Together with the dedicated current-build static model, this supports:

```text
H07 Action-bar assignment model:          NOT_STARTED -> PARTIAL
H08 Hotkey configuration/use mode:        NOT_STARTED -> PARTIAL
H09 Multi-action/cooldown model:          NOT_STARTED -> PARTIAL
H10 Graphics options/settings model:      NOT_STARTED -> PARTIAL
H11 Audio options/settings model:         NOT_STARTED -> PARTIAL (runtime strengthened)
H12 Interface/sidebar/UI settings model:  NOT_STARTED -> PARTIAL
H13 Gameplay/control settings model:      NOT_STARTED -> PARTIAL
H14 Persistence/profile/migration model:  NOT_STARTED -> PARTIAL (runtime strengthened)
```

These are task-local coordinator dispositions under PR #536's status semantics. This task does not edit PR #536.

### UNKNOWN

- whether all H10-H13 settings use `clientoptions.json`;
- per-setting Apply/OK/immediate save timing;
- complete profile/migration semantics;
- character-specific versus global option partition;
- relationship between `QSettings` and `clientoptions.json` for user-visible settings;
- runtime semantics for H10/H12/H13 beyond their dedicated static package;
- fullscreen persistence behavior.

No H07-H14 row is `DONE` from this task.

## Audit disposition

Fresh coordinator review: `4969134238` on source head `7861752c312f77fad0cde28c44c8745aa2806909`.

`UISET-AUD-001` is repaired by this file. Open material findings after this edit: `0`.