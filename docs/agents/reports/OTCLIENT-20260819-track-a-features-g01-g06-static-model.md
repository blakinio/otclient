# OTCLIENT-TIBIA-RE — FEATURES G01-G06 static model package

```yaml
report_date: 2026-08-19
task: OTC-20260819-track-a-features-g01-g06-static-model
pr: 557
alias: TIBIA-RE-FEATURES
status: DRAFT_NOT_PROMOTED
track: official-client-re
execution_class: github_hosted
runtime_access: none
physical_e2e_required: false
base_main: 82e5f435c3aa4172115bf7f6a0cd7a5cc6da3d50
researched_client_version: 15.32.df7b29
researched_client_size: 51965216
researched_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
current_build_authority: UNKNOWN_IN_THIS_TASK
canonical_promotion_authority: coordinator_only
```

## Purpose

This is the first bounded researcher package launched by `TIBIA-RE-FEATURES`. It covers the coherent Cyclopedia/Bestiary/Charm feature group only:

```text
G01 Cyclopedia shell/request-cache model
G02 Cyclopedia map
G03 Cyclopedia houses data/actions
G04 Bestiary kills/unlocks/loot/progress
G05 Charms selection/assignment
G06 Monster Bonus Effects
```

The package is repository-only. It does not access a live official client, canonical runtime, KasmVNC/X11 session, credentials or process memory, and it does not perform any game/account/resource mutation.

The objective is narrower than semantic completion: convert retained exact-build broad capability evidence into a dedicated, falsifiable static map of generated-message names, handler-type xrefs and model/controller/storage leads, while preserving every unresolved semantic edge as `UNKNOWN`.

## Baseline

The current full-client coverage branch represented by PR #536 classifies this group as:

| Row | Baseline status |
|---|---|
| G01 | `NOT_STARTED` |
| G02 | `PARTIAL` |
| G03 | `NOT_STARTED` |
| G04 | `NOT_STARTED` |
| G05 | `NOT_STARTED` |
| G06 | `NOT_STARTED` |

PR #536 is a read-only dependency for this researcher. This task does not edit its shared checklist or matrix.

## Method and evidence boundary

The package triangulates only repository-retained evidence:

1. the complete retained `160` C2S and `189` S2C generated-message registries;
2. the retained direct protocol-handler code-to-type-string xref table;
3. the exact-build capability census;
4. merged PR #435's Cyclopedia structural evidence for G02.

The retained binary fence is `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`. These are historical exact-build static facts only. This report does not establish a current client fence.

A generated-message name proves only that the retained generated-message inventory contains that identifier. A direct handler-type xref proves only code-to-string presence at the retained exact binary address. In particular, the source handler table explicitly marks `semantic_dispatcher_edge_proven=false` for the Cyclopedia and Bestiary tracker rows, so this report does not infer a concrete message-to-handler dispatcher from those xrefs.

## Row-by-row findings

### G01 — Cyclopedia shell/request-cache model

**FACT**

Retained exact-build evidence contains:

```text
C2S  GameclientMessageOpenCyclopediaCharacterInfo
S2C  GameserverMessageCyclopediaCharacterInfo
0xd29a3d  tibia::cyclopedia::TCyclopediaProtocolMessageHandler  DIRECT_CODE_TO_STRING_XREF  false
```

The capability census also records generic Cyclopedia protocol/controller/storage surfaces.

**UNKNOWN**

The request/cache key schema, concrete dispatch edge, handler-to-cache/controller edge, cache lifetime/invalidation, live tab/page state and current-build equivalence remain unproven.

**DRAFT DISPOSITION**: keep `NOT_STARTED`. The package is dedicated but still does not establish request/cache semantics.

### G02 — Cyclopedia map

**FACT**

Retained exact-build evidence contains:

```text
C2S  GameclientMessageCyclopediaMapAction
S2C  GameserverMessageCyclopediaMapData
```

The capability census records `TCyclopediaMapStorage` and map dialog/selection/minimap-renderer surfaces. Merged PR #435 separately preserves exact-client Cyclopedia RTTI/vtable/metadata evidence and explicitly limits that result to structural evidence rather than live semantics.

**UNKNOWN**

The map action enum/payload, message-to-storage edge, storage-to-visible-state causality, cache invalidation, live semantics and current-build equivalence remain unproven.

**DRAFT DISPOSITION**: keep `PARTIAL`; no stronger semantic promotion is justified.

### G03 — Cyclopedia houses data/actions

**FACT**

Retained exact-build evidence contains:

```text
C2S  GameclientMessageCyclopediaHouseAction
S2C  GameserverMessageCyclopediaCurrentHouseData
S2C  GameserverMessageCyclopediaStaticHouseData
S2C  GameserverMessageCyclopediaHouseActionResult
```

The capability census records `THousesStorage` house-info/character-house/limit leads and `THousesInfoDialogController` filter/selection/world-map/action/error leads.

**UNKNOWN**

Static/current-house merge semantics, request/cache schema, `EHouseAction` numeric mapping, action-result error mapping, handler-to-storage causality, live ownership values and current-build equivalence remain unproven.

**DRAFT DISPOSITION**: keep `NOT_STARTED`. No move-out, cancellation or transfer action was executed.

### G04 — Bestiary kills/unlocks/loot/progress

**FACT**

Retained exact-build evidence contains:

```text
C2S  GameclientMessageOpenMonsterCyclopedia
C2S  GameclientMessageOpenMonsterCyclopediaMonsters
C2S  GameclientMessageOpenMonsterCyclopediaRace
C2S  GameclientMessageTrackBestiaryRace
S2C  GameserverMessageBestiaryTracker
S2C  GameserverMessageMonsterCyclopedia
S2C  GameserverMessageMonsterCyclopediaMonsters
S2C  GameserverMessageMonsterCyclopediaNewDetails
S2C  GameserverMessageMonsterCyclopediaRace
0xd2989d  tibia::cyclopedia::TBestiaryTrackerProtocolMessageHandler  DIRECT_CODE_TO_STRING_XREF  false
```

The capability census additionally records open-Bestiary/open-entry/tracker controller leads.

**UNKNOWN**

Race-ID schema, kill count fields, unlock-stage mapping, loot entry schema, progress thresholds, tracker/storage edge, live values and current-build equivalence remain unproven.

**DRAFT DISPOSITION**: keep `NOT_STARTED`.

### G05 — Charms selection/assignment

**FACT**

Retained exact-build evidence contains:

```text
C2S  GameclientMessageApplyClearingCharm
```

The capability census records a `removeSelectedCharm` controller/action lead in the Bestiary/charms surface.

**UNKNOWN**

Charm-ID schema, selected-charm storage, complete assignment request family, cost/validation fields, server confirmation mapping, handler/storage/controller edges, live assignment semantics and current-build equivalence remain unproven.

**DRAFT DISPOSITION**: keep `NOT_STARTED`. No charm was assigned, removed or paid for.

### G06 — Monster Bonus Effects

**FACT**

Retained exact-build evidence contains:

```text
C2S  GameclientMessageMonsterBonusEffectAction
S2C  GameserverMessageMonsterCyclopediaBonusEffects
```

The capability census records `TMonsterBonusEffectStorage` and `TMonsterBonusEffectsDialogController` leads, including changed state, remaining assignable effects, unlock/clear/assign-to-monster and selected-effect concepts.

**INFERENCE**

Because the transport names and storage/controller names are in the monster-Cyclopedia family, Cyclopedia ownership is a plausible target for the next dispatcher investigation. The concrete edge is not proven.

**UNKNOWN**

Bonus-effect ID schema, remaining-effects schema, unlock/clear/assign values, inbound message-to-storage edge, storage-to-dialog edge, server confirmation/rejection semantics, live values and current-build equivalence remain unproven.

**DRAFT DISPOSITION**: keep `NOT_STARTED`. No bonus effect was unlocked, cleared or assigned.

## Cross-row conclusions

### FACT

The retained complete generated-message registries contain dedicated transport identifiers across all six rows except that G05 has only a narrow clearing-charm lead in this bounded registry extraction. The retained handler-xref table provides Cyclopedia and Bestiary tracker type xrefs but explicitly does not prove semantic dispatcher edges.

### INFERENCE

The strongest next repository-only discriminator is not another broad lexical census. It is exact retained code-window/dataflow recovery that connects selected generated-message handling to concrete handler/storage/controller updates, especially for G01/G03/G04/G06. G05 first needs a fuller charm-specific code/message/controller inventory because the current dedicated evidence is sparse.

### UNKNOWN

```yaml
concrete_message_dispatch: UNKNOWN
inbound_message_to_storage_mutation: UNKNOWN
storage_to_controller_causality: UNKNOWN
outbound_action_serialization: UNKNOWN
server_acceptance_or_rejection: UNKNOWN
live_gui_values: UNKNOWN
restart_relogin_repeatability: UNKNOWN
current_build_equivalence: UNKNOWN
```

## Promotion recommendation

This researcher does not change canonical coverage. Fail closed:

| Row | Baseline | Researcher recommendation |
|---|---|---|
| G01 | `NOT_STARTED` | unchanged |
| G02 | `PARTIAL` | unchanged |
| G03 | `NOT_STARTED` | unchanged |
| G04 | `NOT_STARTED` | unchanged |
| G05 | `NOT_STARTED` | unchanged |
| G06 | `NOT_STARTED` | unchanged |

A coordinator may accept the static package as useful dedicated evidence without promoting a row status. Status promotion requires evidence at the checklist's semantic gate, not merely a dedicated document.

## Recommended next experiment

After coordinator review, the next bounded G01-G06 package should remain repository-only unless trusted current-build/runtime gates materially change. Recommended order:

1. recover concrete dispatcher/code windows for the retained Cyclopedia and Bestiary generated-message families;
2. recover handler-to-storage/controller write/read edges for Cyclopedia house/map and Bestiary/monster-bonus models;
3. run a fuller charm-specific QMeta/type/message census to identify the non-clearing assignment/read state surface;
4. only after a current official-client fence is promoted on trusted `main`, revalidate any address-sensitive result before live semantic work;
5. live/resource-mutating proofs remain separate and must preserve the Track A admission and no-spend/no-irreversible-action rules.

## Validation / audit boundary

The exact source registries and handler-xref table were re-read from current `main` and the row-level facts above were copied only from those retained repository sources plus the exact-build capability census and merged PR #435 boundary.

This is a researcher Draft PR, not canonical promotion. Independent coordinator falsification is still required before any promotion decision.

`E2E: NOT_APPLICABLE` — this package changes documentation/evidence only, has `runtime_access: none`, and does not change product or runtime behavior.

## Side effects

```yaml
credentials_accessed: false
official_client_launched_or_observed: false
canonical_runtime_touched: false
gui_input: false
gameplay_action: false
account_or_character_resource_mutation: false
market_store_payment_or_transfer_action: false
shared_PR_536_paths_modified: false
```
