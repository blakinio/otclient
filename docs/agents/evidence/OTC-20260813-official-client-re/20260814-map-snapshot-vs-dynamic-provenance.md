# Map snapshot vs dynamic provenance — 2026-08-14

## Scope

Track A / `official-client-re` only. Subject: official native Linux Tibia client.

Exact client fence:

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runner: synology-otclient-01
state: /home/runner/_work/_otclient_tibia_re_state (legacy image compatibility: /work/_otclient_tibia_re_state)
display: :98
process marker: OTCLIENT_TIBIA_RE_TRACK=official-client-re
```

This document records only Track A evidence. It does not use Track B runtime, Codex, owner API tokens, packet injection, BattlEye bypass/patching, or server modification.

## Research question

Can an object delivered in a full/map-description snapshot be distinguished structurally from an object that was dynamically created on a tile, especially after that tile leaves the client's aware range and is later reloaded?

## FACT — snapshot/map-description and dynamic mutation are separate inbound paths

Direct QMetaObject recovery from this exact binary identifies `tibia::worldmap::TWorldmapProtocolMessageHandler`, static metacall `+0xdf2a60`, and the ordered methods:

```text
handleFullMapMessage
handleLeftColumnMessage
handleRightColumnMessage
handleTopRowMessage
handleBottomRowMessage
handleTopFloorMessage
handleBottomFloorMessage
handleFieldDataMessage
handleCreateOnMapMessage
handleChangeOnMapMessage
handleDeleteOnMapMessage
handleAmbientLightMessage
handleTibiaTimeMessage
```

The corresponding exact handler identities established by the recovered dispatcher include:

```text
+0xcec8d0  FullMap path tail
+0xcd3190  handleFieldDataMessage
+0xcecc70  handleCreateOnMapMessage
+0xcecf40  handleChangeOnMapMessage
+0xcd4e20  handleDeleteOnMapMessage
```

Primary prior evidence:

```text
docs/agents/evidence/OTC-20260813-official-client-re/20260814-dynamic-map-callback-live-discrimination.md
run 31786047410 / job 94722066149
run 31786106136 / job 94722253536
```

Classification: **FACT**.

## REJECTED HYPOTHESIS — old argument interpretation

Earlier runtime records at `+0xcecf40` exposed status/FPS text through pointers chosen by a speculative wrapper interpretation. Direct QMeta evidence proves `+0xcecf40` is `handleChangeOnMapMessage`; therefore the old pointer interpretation, not the handler identity, was wrong.

Do not reuse `event+0x18 = position` or similar field assumptions without new evidence.

Classification: **REJECTED HYPOTHESIS**.

## FACT — structural map-description observation exists

The existing post-login map-description hook `+0x19a8ea3` has produced structural records with:

```text
x y z stack_order type_id_candidate
```

and measured the current-floor aware rectangle as `18 x 14` using directional strip delivery.

Primary prior evidence:

```text
docs/agents/evidence/OTC-20260813-official-client-re/20260814-map-observation-and-dynamic-provenance-checkpoint.md
baseline run 31780838255 / job 94706054275
aware-range run 31778752897 / job 94699702072
```

Classification: **FACT** for coordinates/stack observation and aware-range strip dimensions; `RBX+0x30` remains an exact-build runtime type-id candidate rather than a cross-version ABI contract.

## FACT — previous controlled evidence was insufficient for provenance-after-reload

A previous external item placement plus larger `12 x Right`, `12 x Left` reload produced a WITH_ITEM structural dataset, but common-tile comparison did not isolate the controlled dynamic item. It therefore did not establish whether the reloaded item retained a dynamic marker.

Primary prior evidence:

```text
docs/agents/evidence/OTC-20260813-official-client-re/20260814-map-observation-and-dynamic-provenance-checkpoint.md
post-drop run 31780927846
```

Classification: **FACT** about the negative/inconclusive experiment; provenance-after-reload remains **UNKNOWN** from that run.

## FACT — existing mutation collector baseline is clean but negative

The current named mutation collector was executed with exact Track A fencing:

```text
run 31786366551
job 94773722487
CreateOnMap = 0
ChangeOnMap = 0
DeleteOnMap = 0
```

This is only a zero-event observation window. It is not evidence that dynamic mutations do not exist.

Classification: **FACT**.

## FACT — embedded descriptor limitation

The exact-binary descriptor census (`run 31789613193`, `job 94733342439`) recovered embedded descriptors including `shared.proto`, `appearances.proto`, and `map.proto`. It did **not** recover embedded descriptors for `GameserverMessageCreateOnMap`, `GameserverMessageChangeOnMap`, `GameserverMessageDeleteOnMap`, `WorldmapObjectPosition`, or `ObjectIdentifierAndPosition`.

Therefore absence of a provenance field from that earlier descriptor census cannot be promoted to evidence that no such field exists in the protocol wrapper.

Classification: **FACT**.

## New exact-build experiments prepared

### Complete `map.proto` census

```text
workflow: .github/workflows/tibia-official-client-re-map-provenance-proto-census.yml
commit: 91686dd3cb23c50d5fc19b5dd8a78387dbec23df
run: 31803316941
```

Purpose: enumerate every message/field in the embedded `map.proto` descriptor and separately census provenance-like strings. String hits are never treated as semantic proof by themselves.

### Named handler disassembly

```text
workflow: .github/workflows/tibia-official-client-re-map-provenance-handler-disassembly.yml
commit: 276ecf39b9dbd9b3608a4ff60b4a1878fd481009
run: 31803434560
```

Purpose: exact disassembly of FullMap, CreateOnMap, ChangeOnMap, DeleteOnMap, and map-description neighborhoods to constrain the argument/wrapper layout without invoking gameplay serializers.

### Runtime provenance experiment

```text
workflow: .github/workflows/tibia-official-client-re-map-provenance-runtime.yml
commit: 7433ce3454f498ff3a00c7cf37ccc696de24137f
run: 31803480146
```

Safety properties:

- exact Track A process marker and client SHA fencing;
- fail closed when an unknown/foreign tracer is attached;
- only replaces the previously recorded Track A-owned dynamic observer;
- post-login attach only;
- raw register/pointer bytes are recorded before any semantic field decoding;
- one ordinary adjacent-tile GUI drag is attempted;
- `12 x Right` / `12 x Left` aware-range reload is performed only if the GUI action actually produces at least one named Worldmap mutation event;
- the same run records map-description rows from `+0x19a8ea3` for structural reload evidence;
- the client is left running.

At the time this checkpoint was written, these jobs were queued behind another already-running Track A self-hosted job. No result is claimed before their logs complete.

## Current classification

```yaml
SEPARATE_SNAPSHOT_AND_MUTATION_PATHS: FACT
CREATE_HANDLER: FACT_0xcecc70
CHANGE_HANDLER: FACT_0xcecf40
DELETE_HANDLER: FACT_0xcd4e20
SINGLE_SNAPSHOT_SUFFICIENT_FOR_CANONICAL_OTBM: NOT_PROVEN
DYNAMIC_OBJECT_PAYLOAD_LAYOUT: UNKNOWN
DYNAMIC_MARKER_DURING_CREATE_CHANGE_DELETE: UNKNOWN
PROVENANCE_AFTER_AWARE_RANGE_RELOAD: UNKNOWN
SAME_TYPE_STATIC_VS_DYNAMIC_STRUCTURAL_DIFFERENCE: UNKNOWN
```

## OTBM safety rule pending final experiment

Until provenance-after-reload is directly resolved, a snapshot object whose origin is unknown must not be promoted to permanent OTBM solely because it is present in a map-description snapshot.

Safe interim classes:

```text
STATIC_CANDIDATE
DYNAMIC_OBSERVED
UNKNOWN_ORIGIN
CREATURE
CORPSE
FIELD
TEMPORARY_EFFECT
```

`UNKNOWN_ORIGIN` must not be silently converted to `STATIC_CANDIDATE` or canonical OTBM content.
