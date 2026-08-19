# H07-H09 current-build action-bar / hotkey / multi-action evidence

Date: 2026-08-19 (Europe/Warsaw)  
Task: `OTC-20260819-track-a-ui-settings-static-model`  
Track: `official-client-re`  
Coverage source: PR #536 checklist rows H07-H09  
Researcher delivery: Draft PR only; coordinator-only promotion

## Exact subject fence

This file uses the same successful bounded static probe recorded by `current-build-static-model.md`:

- workflow run `32194079533`
- job `95894394865`, conclusion `success`
- client SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`
- ELF Build ID `d803d9695868713ef6ab0c3cf65f91212c9c6a62`
- `runtime_access: none`
- `client_executed: false`
- `proprietary_binary_retained: false`

## H07 — action-bar assignment model

### FACT

The exact current binary contains the following dedicated action-bar configuration/model/controller identifiers:

```text
tibia::config::TActionBarOptions
tibia::config::TActionBarsQMLOptionsPage
tibia::gamewindow::TActionBarGroup
tibia::gamewindow::TActionBarManager
tibia::gamewindow::TActionBarController
tibia::qmlcomponents::enums::EActionBarPosition
actionBarOptions
actionBarsOptions
actionBarsOptionsChanged
onActionBarOptionsChanged
onActionBarsOptionsChanged
onActionBarCharacterOptionsChanged
onActionBarCharacterOptionsChangedAsync
```

### INFERENCE

The current official client has a dedicated action-bar options/model surface with position semantics and both general and character-option change notification paths.

### UNKNOWN

- exact slot/assignment schema and value representation;
- per-character versus global field partition;
- exact persistence sink/readback path;
- runtime assignment mutation semantics and restart persistence.

## H08 — hotkey configuration/use mode

### FACT

The exact current binary contains:

```text
tibia::config::THotkeysQMLOptionsPage
tibia::config::THotkeysQMLOptionsPage::EHotkeyMode
tibia::config::TTibiaHotkeyActionSettingQmlWrapper
tibia::config::EHotkeyUseObjectType
tibia::input::TKeyboardShortcutHandler
tibia::input::TRecordKeyboardShortcutHandler
HotkeyOptions
hotkeyOptions
hotkeyOptionsChanged
onHotkeyOptionsChanged
HotkeyActionSettingIndex
ShowOptionsHotkeys
onNewKeySequenceSelectedForCurrentHotkeyActionSetting
```

### INFERENCE

Hotkey configuration is not only a generic input surface in this build: it has a dedicated options page, a named hotkey mode enum, an action-setting QML wrapper, an object-use type enum, change notifications, and explicit keyboard-shortcut recording/handling components.

### UNKNOWN

- exact `EHotkeyMode` numeric/value semantics;
- exact key-sequence serialization schema;
- exact persisted binding store and profile scope;
- runtime conflict resolution/precedence across modes.

## H09 — multi-action buttons / cooldown overlays

### FACT

The exact current binary contains:

```text
tibia::input::TMultiActionPrioritySolver::IAction
tibia::input::TGameActionCloseAllMultiActionButtons
tibia::game::TCooldownStorage
tibia::gamewindow::TCooldownBarController
tibia::gamewindow::TCooldownProgressDataForQML
TTibiaActionSetting::getMultiAction: invalid index
TTibiaActionSetting::setMultiAction: Called for non multi action
```

The same build also contains the action-bar/hotkey configuration objects listed above, providing a shared current-build context for these multi-action and cooldown components.

### INFERENCE

The official client has explicit multi-action validation/priority machinery and a separate cooldown storage/controller/QML-data path. The static evidence is more specific than broad capability-name presence, but it does not yet prove a concrete user action assignment or cooldown lifecycle.

### UNKNOWN

- multi-action entry schema and priority values;
- exact association between an action-bar/hotkey slot and a multi-action record;
- authoritative cooldown start/update/expiry lifecycle;
- persistence of multi-action configuration.

## Coverage recommendation — no self-promotion

PR #536 currently records H07-H09 as `NOT_STARTED` with broad `CAP` evidence and `DEDICATED-G0` remaining.

**RECOMMENDATION:** coordinator review can treat this task as a dedicated, exact-current-build static evidence package for H07-H09. It supports moving those rows beyond broad capability census only if the coordinator judges the row contract satisfied for `PARTIAL`; it does not support `DONE` and does not replace required runtime/semantic proof.

The researcher does not edit the canonical #536 matrix.

## Next discriminator

The smallest safe next step for H07-H09 is a static linkage pass around the action/hotkey configuration objects and persistence anchors already being recovered for H14. A later runtime proof should use only a reversible, non-combat, non-display-critical binding/slot change under fresh admission and shared input lock, with exact before/after/rollback evidence.
