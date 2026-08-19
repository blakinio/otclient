# TIBIA-RE-FEATURES G01-G06 retained exact-build static evidence

```yaml
status: DRAFT_NOT_PROMOTED
task: OTC-20260819-track-a-features-g01-g06-static-model
pr: 557
track: official-client-re
runtime_access: none
execution_class: github_hosted
physical_e2e_required: false
researched_client_version: 15.32.df7b29
researched_client_size: 51965216
researched_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
current_client_fence_authority: UNKNOWN_IN_THIS_TASK
```

This evidence index is a bounded extraction from already-retained repository evidence. It contains no official-client binary bytes and performs no runtime observation. Every address below is valid only for the retained exact researched binary and is not current-build authority.

## Primary sources

| Source | Retained fact used here |
|---|---|
| `docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-client-to-server.txt` | complete retained 160-name C2S generated-message registry |
| `docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-server-to-client.txt` | complete retained 189-name S2C generated-message registry |
| `docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-handler-code-xrefs.tsv` | direct code-to-handler-type-string xrefs; every retained row explicitly has `semantic_dispatcher_edge_proven=false` |
| `docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md` | exact-build QMeta/class/storage/controller/action leads and generated-message summary |
| merged PR #435 (`8c9486e2c6109a7a39b564804c8acd707659b5e0`) | G02 Cyclopedia structural RTTI/vtable/metadata evidence only; no live semantic claim |
| PR #536 checklist/matrix | read-only row names/status baseline; not modified by this task |

## G01 — Cyclopedia shell / request-cache

### FACT

Retained S1 handler evidence contains:

```text
0xd29a3d  tibia::cyclopedia::TCyclopediaProtocolMessageHandler  DIRECT_CODE_TO_STRING_XREF  false
```

The retained generated-message registries contain:

```text
C2S  GameclientMessageOpenCyclopediaCharacterInfo
S2C  GameserverMessageCyclopediaCharacterInfo
```

The exact-build capability census separately records `TCyclopediaProtocolMessageHandler` and generic Cyclopedia controller/storage surfaces.

### UNKNOWN

```yaml
request_cache_key_schema: UNKNOWN
request_to_concrete_handler_dispatch: UNKNOWN
handler_to_cache_or_controller_edge: UNKNOWN
cache_lifetime_and_invalidation: UNKNOWN
live_page_or_tab_state: UNKNOWN
current_build_equivalence: UNKNOWN
```

A direct code-to-type-string xref is not a semantic dispatcher edge; the S1 table explicitly records `semantic_dispatcher_edge_proven=false`.

## G02 — Cyclopedia map

### FACT

Retained generated-message names:

```text
C2S  GameclientMessageCyclopediaMapAction
S2C  GameserverMessageCyclopediaMapData
```

The exact-build capability census records `TCyclopediaMapStorage` plus Cyclopedia map dialog/selection/minimap-renderer surfaces. Merged PR #435 independently preserved exact-client Cyclopedia RTTI/vtable/metadata evidence and explicitly bounded it to structural evidence only.

### UNKNOWN

```yaml
map_action_enum_and_payload_semantics: UNKNOWN
server_message_to_TCyclopediaMapStorage_edge: UNKNOWN
storage_to_visible_map_state_causality: UNKNOWN
cache_invalidation: UNKNOWN
live_semantics: UNKNOWN
current_build_equivalence: UNKNOWN
```

G02 was already `PARTIAL` in the PR #536 baseline; this researcher package does not promote it further.

## G03 — Cyclopedia houses data/actions

### FACT

Retained generated-message names:

```text
C2S  GameclientMessageCyclopediaHouseAction
S2C  GameserverMessageCyclopediaCurrentHouseData
S2C  GameserverMessageCyclopediaStaticHouseData
S2C  GameserverMessageCyclopediaHouseActionResult
```

The exact-build capability census records `THousesStorage` with house info/character houses/limits and `THousesInfoDialogController` with filters, selected house, world-map viewport, house-action/error leads. These are static leads only.

### UNKNOWN

```yaml
house_request_cache_schema: UNKNOWN
static_vs_current_house_merge_semantics: UNKNOWN
EHouseAction_numeric_mapping: UNKNOWN
house_action_result_error_mapping: UNKNOWN
handler_to_THousesStorage_edge: UNKNOWN
live_ownership_values: UNKNOWN
current_build_equivalence: UNKNOWN
```

No move-out, transfer or other house mutation is performed or authorized.

## G04 — Bestiary kills/unlocks/loot/progress

### FACT

Retained S1 handler evidence contains:

```text
0xd2989d  tibia::cyclopedia::TBestiaryTrackerProtocolMessageHandler  DIRECT_CODE_TO_STRING_XREF  false
```

Retained generated-message names include:

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
```

The exact-build capability census records Bestiary open-entry/tracker controller leads.

### UNKNOWN

```yaml
race_id_schema: UNKNOWN
kill_count_field_mapping: UNKNOWN
unlock_stage_mapping: UNKNOWN
loot_entry_schema: UNKNOWN
progress_threshold_semantics: UNKNOWN
tracker_storage_edge: UNKNOWN
live_values: UNKNOWN
current_build_equivalence: UNKNOWN
```

The direct handler-type xref does not prove that any listed generated message dispatches to that handler.

## G05 — Charms selection/assignment

### FACT

The retained C2S registry contains:

```text
GameclientMessageApplyClearingCharm
```

The exact-build capability census records a `removeSelectedCharm` controller/action lead in the Bestiary/charms surface.

### UNKNOWN

```yaml
charm_id_schema: UNKNOWN
selected_charm_state_location: UNKNOWN
assignment_request_message: UNKNOWN
assignment_cost_or_validation_fields: UNKNOWN
server_confirmation_message: UNKNOWN
handler_storage_controller_edge: UNKNOWN
live_assignment_semantics: UNKNOWN
current_build_equivalence: UNKNOWN
```

No charm is selected, assigned, cleared or paid for by this task. `GameclientMessageApplyClearingCharm` is an exact retained message-name fact; interpreting its payload or relation to all charm assignment flows would be an inference and is not promoted here.

## G06 — Monster Bonus Effects

### FACT

Retained generated-message names:

```text
C2S  GameclientMessageMonsterBonusEffectAction
S2C  GameserverMessageMonsterCyclopediaBonusEffects
```

The exact-build capability census records `TMonsterBonusEffectStorage` and `TMonsterBonusEffectsDialogController`, including static leads for changed state, remaining assignable effects, unlock/clear/assign-to-monster and selected-effect state.

### INFERENCE

The co-occurrence of Cyclopedia protocol ownership, monster-Cyclopedia transport names and monster-bonus storage/controller surfaces makes Cyclopedia-family dispatch a plausible investigation target. This package does **not** prove that dispatch edge.

### UNKNOWN

```yaml
bonus_effect_id_schema: UNKNOWN
remaining_assignable_effects_schema: UNKNOWN
unlock_clear_assign_action_values: UNKNOWN
message_to_storage_edge: UNKNOWN
storage_to_dialog_controller_edge: UNKNOWN
server_confirmation_or_rejection_semantics: UNKNOWN
live_values: UNKNOWN
current_build_equivalence: UNKNOWN
```

No effect is unlocked, cleared, assigned or changed by this task.

## Negative controls / non-claims

```yaml
semantic_dispatcher_edge_from_S1_handler_xrefs: NOT_PROVEN
outbound_action_to_wire_serialization: NOT_PROVEN
inbound_message_to_storage_mutation: NOT_PROVEN
storage_to_controller_causality: NOT_PROVEN
live_GUI_semantics: NOT_TESTED
server_acceptance: NOT_TESTED
restart_or_relogin_repeatability: NOT_TESTED
current_build_equivalence: NOT_PROVEN
current_runtime_identity: NOT_APPLICABLE
credentials_used: false
runtime_or_gui_mutation: false
```

## Researcher disposition

This package does **not** edit canonical coverage. The fail-closed researcher recommendation is:

| Row | PR #536 baseline | Draft recommendation |
|---|---|---|
| G01 | `NOT_STARTED` | keep until request/cache semantics are directly recovered |
| G02 | `PARTIAL` | keep `PARTIAL`; structural evidence still lacks live/storage causality |
| G03 | `NOT_STARTED` | keep until concrete data/action/storage semantics are recovered |
| G04 | `NOT_STARTED` | keep until message/handler/model field semantics are recovered |
| G05 | `NOT_STARTED` | keep; current retained evidence is especially sparse |
| G06 | `NOT_STARTED` | keep until message/storage/controller edges and field semantics are recovered |

Only the coordinator may promote/reclassify canonical rows.
