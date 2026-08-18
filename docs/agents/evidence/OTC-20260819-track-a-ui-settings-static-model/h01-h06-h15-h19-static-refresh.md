# H01-H06 / H15-H19 current-build static refresh

Date: 2026-08-19 (Europe/Warsaw)  
Task: `OTC-20260819-track-a-ui-settings-static-model`  
Alias: `TIBIA-RE-UI-SETTINGS`  
Track: `official-client-re`  
Researcher delivery: Draft PR only; coordinator-only promotion

## Scope and exact build fence

The alias owns H01-H19 with H07-H14 as the priority band. This report records only non-overlapping, lower-priority signals already recovered by the same successful bounded current-build scan. It does not expand into another worker's live runtime lane.

Evidence source:

- workflow run `32194426242`
- job `95895411896`, conclusion `success`
- client SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`
- ELF Build ID `d803d9695868713ef6ab0c3cf65f91212c9c6a62`
- `runtime_access: none`
- `client_executed: false`
- `proprietary_binary_retained: false`

## Classification rule

A class/type identifier in this report is **FACT** only for current-build compiled presence. It is not treated as proof of live state, lifecycle semantics, server causality, or persistence.

## H01 — server modal dialogs

**UNKNOWN.** The bounded scan recovered generic dialog/controller infrastructure but no discriminator that tied a specific modal to server-originated modal semantics. Generic dialog presence is intentionally not promoted to H01 evidence.

## H02 — death dialog / fair-fight data

**FACT:** the exact current binary contains:

```text
tibia::gamewindow::TDeathDialogController
```

**INFERENCE:** the current client has a dedicated death-dialog controller rather than relying only on a generic modal.

**UNKNOWN:** fair-fight fields, server payload mapping, controller state layout, live lifecycle/open-close semantics.

## H03 — logout confirmation / close request

**UNKNOWN.** This bounded scan did not recover a dedicated logout-confirmation/close-request semantic discriminator. No claim is made from generic message/dialog classes.

## H04 — generic context-menu semantic actions

**FACT:** the exact current binary contains:

```text
tibia::gamewindow::TContextMenuController
```

**INFERENCE:** context-menu behavior has a dedicated controller object in this build.

**UNKNOWN:** menu-entry semantic action model, enabled/disabled rules, target association, live menu lifecycle.

## H05 — generic dialog/modal/window/tab/selection state

**FACT:** the exact current binary contains a broad dedicated dialog/controller family including:

```text
tibia::gamewindow::TDialogControllerBase
tibia::gamewindow::TDialogStackController
tibia::gamewindow::TMessageDialogController
tibia::gamewindow::TWaitDialogController
tibia::gamewindow::TAboutDialogController
tibia::gamewindow::TOptionsMenuDialogController
tibia::gamewindow::TOptionsMenuDialogController::EDialogCategories
```

It also contains many specialised dialog controllers such as `TNewsDialogController`, `TPreyDialogController`, `TMonsterDialogController`, `TStoreDialogController`, and others.

**INFERENCE:** the current client has a structured controller/dialog-stack architecture with specialised dialog classes and an options-menu category enum.

**UNKNOWN:** authoritative open/closed/focused/selected-tab state representation and lifecycle for generic consumers.

## H06 — drag-and-drop semantic state

**FACT:** the exact current binary contains:

```text
tibia::gamewindow::TDragAndDropController
```

**INFERENCE:** drag-and-drop has a dedicated controller component.

**UNKNOWN:** source/target/object semantic state, acceptance rules, drag lifecycle, cancellation/drop semantics.

## H15 — structured sound-event / world-cue model

**FACT:** the exact current binary contains a structured sound family including:

```text
tibia::sound::TSoundStorage
tibia::sound::TSoundEffectID
tibia::sound::TGameSessionSoundProvider
tibia::sound::TSoundProtocolMessageHandler
tibia::sound::TSoundController
tibia::sound::TSoundControllerMusic
tibia::sound::TSoundControllerCombatSound
tibia::sound::TSoundControllerAmbienceStream
tibia::sound::TSoundControllerAmbienceObjectSound
tibia::protobuf::protocol::GameserverMessageSoundTrigger
tibia::input::gameactions::TGameActionSoundTrigger
tibia::protobuf::sound::MusicTemplate
tibia::protobuf::sound::AmbienceStream
tibia::protobuf::sound::AmbienceObjectStream
```

**INFERENCE:** the current client represents server sound triggers, game-action sound triggers, music, combat and ambience through distinct storage/protocol/controller/model objects.

**UNKNOWN:** authoritative live sound-event state, spatial/world-cue lifecycle, exact trigger-to-controller causality, suppression/mixing semantics.

## H16 — network lane / dual-connection live state

**UNKNOWN.** This settings/UI static task did not run a network-specific or live dual-connection discriminator. Deliberately no overlap with active auth/action/network research lanes.

## H17 — latency / FPS / frame-timing state

**FACT:** the current-build graphics bucket contains renderer timing/update infrastructure including:

```text
tibia::renderer::TNextFrameUpdater
```

and the compiled graphics options page described in `current-build-static-model.md`.

**UNKNOWN:** authoritative FPS, latency, frame-time values, storage/controller ownership for those metrics, and live update semantics. The presence of frame-update infrastructure is not promoted into an H17 semantic-state claim.

## H18 — anti-cheat passive safety/session signals only

**FACT:** the exact current binary contains:

```text
tibia::client::TAntiCheatController
```

**BOUNDARY:** no anti-cheat mechanism, memory, protocol, bypass, evasion, or mutation was inspected. This is compiled-name presence only.

**UNKNOWN:** passive session/safety signals safe and authorized for observation under H18.

## H19 — `TSessiondumpPlayer` research lead

**UNKNOWN.** `TSessiondumpPlayer` did not surface in the bounded current-build settings/UI buckets used by this task. No absence claim is made for the complete binary; only this scan was non-dispositive.

## Coverage recommendation — no self-promotion

The current #536 checklist records H01-H09 and H15-H19 as `NOT_STARTED` with broad `CAP` evidence and a dedicated-G0 transition requirement.

**RECOMMENDATION:** coordinator review can use this file as an exact-current-build static refresh for H02, H04, H05, H06, H15, and passive lexical H18. H01, H03, H16, H17 semantic state, and H19 remain unresolved by this task. None of these rows is claimed `DONE`, and this researcher does not edit the canonical matrix.

## Next action

Any further progress on H01-H06/H15-H19 should be assigned to the specific semantic/runtime worker that owns the relevant surface. This UI/settings task should not consume live runtime authority merely to broaden lexical coverage.
