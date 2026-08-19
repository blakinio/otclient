# TIBIA-RE-INVENTORY-CONTAINERS — bounded final evidence result

```yaml
task: OTC-20260819-track-a-inventory-containers-runtime
source_pr: 559
scope: D09-D22
current_client: 15.32 / 52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
selected_current_anchor_rows: 14/14 PASS
recommended_rows: 14 PARTIAL / 0 DONE
```

## Bounded result

The task has exhausted the safe evidence available without a new credential-bearing login attempt. It now contains exact-current-build structural recovery, direct queue→handler routing, direct handler→storage mutation paths, storage→controller Qt connections, and a bounded read-only physical observation.

No D09-D22 row is claimed `DONE`: authenticated live values, per-action server effects and restart/relogin stability remain outside this bounded proof.

## Current-build facts

- 14/14 selected D09-D22 structural anchor sets revalidated on the exact current package.
- 21/21 selected Qt types recovered independently from the current ELF; historical VAs moved and are not reused.
- current `TProtocolMessageQueue` recovered at QMeta `0x30b83c0`, 355 methods / 192 signals.
- direct `QObject::connectImpl` queue→`TContainerProtocolMessageHandler` routes recovered for inventory, container, object-info, stash, managed/special-container and depot families documented in `20260819-current-queue-handler-routing.md`.
- `TContainerStorage` primary vptr `0x30bf7b8`, QMeta `0x30c3340`.
- container open/close/create/change/delete handlers dispatch into current `TContainerStorage` methods which emit `containerUpdated` or `containerRemoved`.
- direct `TContainerStorage`→`TContainerStorageController` connections are proven for `containerUpdated`, `containerRemoved`, and `manualSortModeChanged`.
- Set/DeleteInventory handlers mutate the current `TInventoryContainer` and emit `inventoryChanged`.
- direct `inventoryChanged`→`TPlayerInventoryAndStatusController::onInventoryChanged` connection is proven.

The exact addresses and connection sites are recorded in `20260819-current-state-propagation-routing.md` and `current_state_propagation_routing.json`.

## Row disposition

| ID | Bounded evidence result | Recommendation | Remaining programme proof |
|---|---|---|---|
| D09 | queue→handler FACT; Set/Delete→inventoryChanged FACT | PARTIAL | PlayerInventory bulk-value normalization + authenticated values |
| D10 | current equipment/status slot controller surface FACT | PARTIAL | authoritative live slot payloads |
| D11 | inventoryChanged→onInventoryChanged connection FACT | PARTIAL | authenticated live correlation |
| D12 | current appearance helper API FACT | PARTIAL | lookup return/localization/error semantics |
| D13 | item/count/info metadata surfaces FACT | PARTIAL | subtype/charges/duration normalization |
| D14 | proficiency handler/storage surfaces FACT | PARTIAL | live XP message/value correlation |
| D15 | container handler→storage→controller route FACT | PARTIAL | complete authenticated registry/lifetime values |
| D16 | create/change/delete causal static chain FACT | PARTIAL | live causal value correlation |
| D17 | close/up/parent/pagination surfaces FACT | PARTIAL | serialization/live effects |
| D18 | sort/object-info surfaces FACT | PARTIAL | schema/value normalization |
| D19 | stash queue/handler/controller surfaces FACT | PARTIAL | authenticated stash values/limits |
| D20 | depot queue/handler/storage/controller/action surfaces FACT | PARTIAL | request/result serialization/live response |
| D21 | managed/special storage/handler surfaces FACT | PARTIAL | authenticated assignment/update values |
| D22 | Quick Loot/obtain action/QML/controller surfaces FACT | PARTIAL | serialization/ack/live effects |

## Passive runtime observation

A later invocation re-read the merged current fence and persisted `runtime_access: read_only`. Fresh preflight proved one exact-current `client` in `otclient-track-a-kasmvnc`, `DISPLAY=:1`, with the current size/SHA and no competing host `client` candidate.

One contract-authorized passive X11 capture showed the client at the **login screen**, so inventory/container state was not visible. No keyboard/mouse input, credentials, login, character selection, gameplay, debugger/injection, process control, network mutation or item/container stimulus was performed. The raw capture was deleted.

## Evidence boundary

**FACT:** exact-current static symbols/QMeta, listed direct Qt connections, listed virtual dispatch/mutation routes, and the passive runtime identity/state observations are directly verified.

**INFERENCE:** these paths are the normal current-client architecture for inventory/container state propagation; static proof alone does not establish the authoritative values in a particular authenticated session.

**UNKNOWN / NOT_OBSERVED:** authenticated live values; remaining bulk-value normalization; exact subtype/charges/duration semantics; per-action serialization/server acknowledgements; restart/relogin stability.

## Safety / cleanup

Targeted cleanup verified that task-local raw current-client copies, compressed client staging and passive screenshots were deleted. No raw proprietary binary or screenshot is committed or uploaded by this task.

## Completion meaning

This bounded research task is implementation-complete when its evidence is independently audited and cleanly promoted. That does **not** mean the broader D09-D22 programme is semantically complete; the remaining authenticated/live and stability work stays explicitly recorded above rather than being hidden by a `DONE` label.
