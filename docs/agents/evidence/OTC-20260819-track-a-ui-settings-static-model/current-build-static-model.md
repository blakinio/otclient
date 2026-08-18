# Current-build official-client UI/settings static model

Date: 2026-08-19 (Europe/Warsaw)  
Task: `OTC-20260819-track-a-ui-settings-static-model`  
Alias: `TIBIA-RE-UI-SETTINGS`  
Track: `official-client-re`  
Researcher delivery: Draft PR only; coordinator-only promotion

## Evidence source and exact subject identity

The deterministic GitHub-hosted static probe was introduced in:

- workflow: `.github/workflows/track-a-ui-settings-static-model.yml`
- branch commit: `2aaa0fffb9cf90699126d1e227b5ac770a33503d`
- workflow run: `32194079533`
- job: `95894394865`, `Recover official-client UI/settings static model`
- job conclusion: `success`

The probe fetched the official Linux current-package object from `static.tibia.com`, decompressed it as data, inspected the ELF statically, deleted the downloaded/decompressed package files before job completion, and did not execute the Tibia client.

```yaml
runtime_access: none
client_executed: false
proprietary_binary_retained: false
source_object: tibiaclient-linux-current/bin/client.lzma
packed_size: 10214529
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
lzma_envelope: offset45;lc=3;lp=0;pb=2;dict=33554432
```

These identities are the build fence for every current-build fact below. They also independently reproduce the packed/unpacked hashes previously reported by the native-login research lane; this report does not infer that an updated on-disk canonical runtime is currently running this build.

## Evidence classification

- **FACT** — directly emitted by the successful bounded static scan of the exact subject above.
- **INFERENCE** — structural interpretation of multiple current-build facts; not direct runtime proof.
- **UNKNOWN** — not established by this phase and must not be guessed.
- **RECOMMENDATION** — proposed coordinator classification or next discriminator; not self-promotion.

## H10 — graphics options/settings

### FACT

The exact current binary contains the following high-signal identifiers:

```text
tibia::config::TGraphicsQMLOptionsPage
tibia::qmlcomponents::enums::EAntialiasingMode
graphicsOptions
graphics_setting_requires_restart_text
graphics_setting_requires_restart_caption
QmlCacheGeneratedCode::_qt_qml_qmlcomponents_qml_OptionsPageGraphics_qml::...
```

It also contains embedded default action-setting text for fullscreen toggling. That embedded default text is not persistence proof.

### INFERENCE

The graphics options surface has a dedicated compiled QML options page and a `tibia::config`-namespaced backing/controller object. The restart-warning identifiers show that at least some graphics choices have explicit restart-sensitive UI semantics.

### UNKNOWN

- exact option-key enumeration and value types;
- page-to-`TClientOptions` call/data linkage;
- exact persistence sink for each graphics option;
- runtime apply/reload/restart behavior.

## H11 — audio/music/ambient options/settings

### FACT

The exact current binary contains:

```text
tibia::config::TSoundQMLOptionsPage
tibia::config::TUISoundsQMLOptionsPage
tibia::config::TBattleSoundsQMLOptionsPage
tibia::sound::TSoundConfiguration
tibia::sound::TSoundEngine
tibia::sound::TSoundManager
tibia::sound::TSoundController
tibia::sound::TSoundControllerMusic
tibia::sound::TSoundControllerCombatSound
tibia::sound::TSoundControllerAmbienceStream
tibia::sound::TSoundControllerAmbienceObjectSound
tibia::game::TGameWorldVolumeStorage
```

A retained printable/mangled identifier also names `TSoundControllerAmbienceStream::onSoundOptionsChanged`.

### INFERENCE

The current client separates general, UI, battle, music and ambience sound concerns across dedicated options/configuration/controller objects rather than presenting one opaque audio toggle.

### UNKNOWN

- exact option keys/ranges/defaults;
- exact persistence sink for sound options;
- whether individual values apply immediately or require controller/session reinitialization;
- persistence across client restart.

## H12 — interface/sidebar/UI options/settings

### FACT

The exact current binary contains:

```text
tibia::config::TActionBarOptions
tibia::config::TActionBarsQMLOptionsPage
tibia::config::TSidebarOptions
tibia::config::TInterfaceQMLOptionsPage
tibia::gamewindow::TActionBarGroup
tibia::gamewindow::TActionBarManager
tibia::gamewindow::TActionBarController
tibia::gamewindow::TSidebarManager
tibia::gamewindow::TSidebarController
tibia::gamewindow::TSidebarPanelsManager
tibia::gamewindow::TSidebarWidgetsManager
tibia::gamewindow::TStatusBarController
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

The current interface model includes distinct configuration objects for action bars and sidebars, dedicated UI options pages, and change-notification paths consumed by game-window controllers/managers.

### UNKNOWN

- exact serialization schema for action bars/sidebars;
- per-character versus global persistence boundaries for each field;
- exact reconstruction order after reload/restart.

## H13 — gameplay/control options/settings

### FACT

The exact current binary contains:

```text
tibia::config::TControlsQMLOptionsPage
tibia::config::TGameplayQMLOptionsPage
tibia::gamewindow::TOptionsMenuDialogController
tibia::input::TKeyboardStatusStorage
tibia::input::TKeyboardShortcutHandler
tibia::input::TRecordKeyboardShortcutHandler
tibia::input::TPlayerMovementIntentHandler
tibia::input::TPlayerMovementInputInterpreter
```

### INFERENCE

The controls/gameplay settings surface is represented by dedicated QML options pages and is adjacent to explicit keyboard shortcut and player-movement input components in the current binary.

### UNKNOWN

- exact mapping of gameplay/control toggles to `EClientOption` values;
- whether individual controls are local-only or also represented by protocol messages;
- exact persistence/readback/restart behavior.

## H14 — options persistence/profile/migration

### FACT: general options model

The exact current binary contains:

```text
tibia::config::TClientOptions
tibia::config::EClientOption
tibia::config::TClientOptionsModeSwitcher
tibia::config::TOptionPageQMLWrapperBase
tibia::config::TCharacterConfigurationManager
tibia::config::ICharacterConfigurationBase
```

It also exposes a broad current options-page family, including:

```text
THotkeysQMLOptionsPage
TActionBarsQMLOptionsPage
THudQMLOptionsPage
TMiscQMLOptionsPage
TSoundQMLOptionsPage
TConsoleQMLOptionsPage
TEffectsQMLOptionsPage
TControlsQMLOptionsPage
TGameplayQMLOptionsPage
TGraphicsQMLOptionsPage
TUISoundsQMLOptionsPage
TButtonBarQMLOptionsPage
TInterfaceQMLOptionsPage
TGameWindowQMLOptionsPage
TScreenshotsQMLOptionsPage
TBattleSoundsQMLOptionsPage
```

### FACT: persistence-capable APIs/artifacts

The exact current binary contains/imports identifiers for:

```text
QSettings::QSettings(QString const&, QSettings::Format, QObject*)
QSettings::beginGroup(QAnyStringView)
QSettings::endGroup()
QSettings::value(QAnyStringView, QVariant const&) const
QSettings::setValue(QAnyStringView, QVariant const&)
std::_Sp_counted_ptr_inplace<QSettings,...>
clientoptions.json
virtual QJsonDocument shared::TFileSystemHelper::readJsonFileAsQJsonDocument(const QString&, bool&) const
QJsonDocument / QJsonObject / QJsonArray read/write-capable API surface
```

The exact current binary also contains protocol/model identifiers including:

```text
tibia::protobuf::protocol::GameclientMessageSetClientOptions
tibia::protobuf::protocol::ClientOptionSetMovement
```

### INFERENCE

The current client has at least two persistence-capable technology families available to its configuration code: `QSettings` and JSON/file helpers, and it contains a literal `clientoptions.json`. `TClientOptions`, option-page wrappers and specialised option structs form strong candidates for the backing model used by UI pages.

### UNKNOWN — critical boundary

This static scan does **not** yet prove any of the following:

1. that `TClientOptions` is serialized specifically to `clientoptions.json`;
2. which options use `QSettings` versus JSON versus another storage path;
3. the exact path, group names or keys supplied to `QSettings`;
4. exact code-level call/data flow from each `T*QMLOptionsPage` to a persistence sink;
5. profile/migration versioning semantics;
6. runtime read/write/reload/restart persistence.

String, RTTI and imported-API coexistence is not treated as call-flow proof.

## Hotkeys, action bars, multi-action and cooldown surface

### FACT

The exact current binary contains additional high-signal identifiers relevant to the alias priority list:

```text
tibia::config::THotkeysQMLOptionsPage
tibia::config::THotkeysQMLOptionsPage::EHotkeyMode
tibia::config::TTibiaHotkeyActionSettingQmlWrapper
tibia::config::EHotkeyUseObjectType
tibia::input::TKeyboardShortcutHandler
tibia::input::TRecordKeyboardShortcutHandler
tibia::input::TMultiActionPrioritySolver::IAction
tibia::input::TGameActionCloseAllMultiActionButtons
tibia::gamewindow::TActionBarGroup
tibia::gamewindow::TActionBarManager
tibia::gamewindow::TActionBarController
tibia::game::TCooldownStorage
tibia::gamewindow::TCooldownBarController
tibia::gamewindow::TCooldownProgressDataForQML
HotkeyOptions
hotkeyOptions
hotkeyOptionsChanged
onHotkeyOptionsChanged
HotkeyActionSettingIndex
ShowOptionsHotkeys
onNewKeySequenceSelectedForCurrentHotkeyActionSetting
```

The binary includes default action/hotkey JSON-like literals and multi-action validation/error strings. These prove embedded configuration vocabulary and object names, not user-specific persisted values.

## Coverage recommendation — no self-promotion

The researcher does not edit PR #536's canonical coverage matrix and does not mark any row `READY`.

**RECOMMENDATION:** coordinator review can now treat H10, H11, H12 and H13 as having non-`NONE`, exact-current-build **STATIC** evidence for their UI/controller/model surfaces. H14 now has non-`NONE`, exact-current-build **STATIC** evidence for candidate persistence mechanisms and option models, but not for the required persistence semantics.

No runtime completeness claim is made for H10-H14.

## Smallest next discriminators

### Static discriminator — authorized under current admission

Recover code xrefs/callsites for:

- the literal `clientoptions.json`;
- `QSettings::value` and `QSettings::setValue` import/GOT targets;
- where feasible, nearby `TClientOptions`/option-page identity anchors.

The goal is to replace coexistence with concrete code-level linkage while still keeping `runtime_access: none`.

### Later live persistence discriminator — requires fresh admission

After static evidence is exhausted, use a low-risk, non-display-critical, non-network-critical, fully reversible setting. Under a fresh runtime admission and shared input lock:

1. record exact before value and storage observation;
2. make one bounded UI change;
3. record immediate readback and storage delta;
4. reload/restart only if separately admitted and safe;
5. verify persistence;
6. restore the exact before value and verify rollback.

No such live mutation was performed by this phase.
