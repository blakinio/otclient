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

Direct QMetaObject recovery from this exact binary identifies `tibia::worldmap::TWorldmapProtocolMessageHandler`, static metacall `+0xdf2a60`, and ordered methods including:

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
```

Exact handler identities established by the recovered dispatcher include:

```text
+0xcec8d0  FullMap path tail
+0xcd3190  handleFieldDataMessage
+0xcecc70  handleCreateOnMapMessage
+0xcecf40  handleChangeOnMapMessage
+0xcd4e20  handleDeleteOnMapMessage
```

Primary evidence:

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

## FACT — structural map-description observation and aware-range size

The post-login map-description hook `+0x19a8ea3` produced structural records with `x/y/z`, stack order and an exact-build object field candidate. Directional strip delivery measured the current-floor aware rectangle as `18 x 14`.

Primary evidence:

```text
docs/agents/evidence/OTC-20260813-official-client-re/20260814-map-observation-and-dynamic-provenance-checkpoint.md
baseline run 31780838255 / job 94706054275
aware-range run 31778752897 / job 94699702072
```

Classification: **FACT** for coordinates/stack observation and the measured aware-range strip dimensions. `RBX+0x30` remains exact-build evidence rather than a cross-version ABI contract.

## FACT — old WITH_ITEM reload did not isolate the dynamic object

A previous external item placement plus `12 x Right`, `12 x Left` reload produced a WITH_ITEM dataset, but comparison on common coordinates found no isolated added object. It therefore did not prove what happened to the controlled item's provenance after reload.

```text
post-drop run 31780927846
```

Classification: **FACT** for the inconclusive experiment; provenance-after-reload remains **UNKNOWN** from that run.

## FACT — embedded `map.proto` is not the live Worldmap object schema

Workflow:

```text
.github/workflows/tibia-official-client-re-map-provenance-proto-census.yml
commit 91686dd3cb23c50d5fc19b5dd8a78387dbec23df
run 31803316941 / job 94776176176
result SUCCESS
```

The complete embedded `tibia.protobuf.map` descriptor contains four top-level messages: `Map`, `Area`, `Npc`, and `MapFile`. Its fields describe map resource metadata such as areas, NPC coordinates, resource files, map bounds and file geometry. It does not describe live `CreateOnMap` / `ChangeOnMap` / `DeleteOnMap` object payloads.

The provenance-like string census is only a string surface and is not semantic evidence.

Classification: **FACT**.

Rejected hypothesis: embedded `map.proto` would directly expose the live dynamic/snapshot object schema.

## FACT — Create/Change and snapshot normalize the same object-entry representation

Workflow:

```text
.github/workflows/tibia-official-client-re-map-provenance-handler-disassembly.yml
fixed implementation commit c6aa95a18030ba14e8f780b5cd9ec135723a4cc2
run 31804083206 / job 94778661881
result SUCCESS
```

Exact-build disassembly shows:

### `CreateOnMap +0xcecc70`

- the event wrapper supplies position/context through the structure rooted at `rsi`;
- the wrapper supplies stack/context separately;
- the object payload is loaded from the wrapper and its object-entry fields at offsets including `+0x8`, `+0x28`, and `+0x30` are consumed;
- the object is passed to shared normalization helper `+0xceca50` before the worldmap operation.

### `ChangeOnMap +0xcecf40`

- position/stack context and replacement object payload are separately consumed from the event wrapper;
- the replacement object is passed to the same shared normalization helper `+0xceca50`.

### map-description / snapshot path `+0x19a8a80`

- it iterates object entries;
- the same object-entry offsets including `+0x8`, `+0x28`, and `+0x30` are consumed;
- each object entry is passed to the same shared normalization helper `+0xceca50` at `+0x19a8ecc`.

### `DeleteOnMap +0xcd4e20`

Deletion is structurally an event wrapper and does not require the same complete object payload; its disassembly contains alternate delete-by-position/stack-or-identifier forms.

Classification:

- **FACT:** mutation and snapshot delivery paths are different handlers/wrappers.
- **FACT:** the Create/Change object payload and snapshot object entry converge on the same exact-build normalization helper and the same observed object-entry field layout.
- **INFERENCE (high confidence):** dynamic origin is path/history context, not a separate dynamic item representation inside the normalized object payload merely because it arrived via Create/Change.
- **UNKNOWN:** whether the client stores a separate persistent provenance flag elsewhere in runtime state after insertion.

This static result strongly favors event-only provenance, but it is not promoted to MODEL B until a controlled live mutation is captured and the same object is observed after aware-range reload.

## FACT — controlled automatic GUI drag did not generate a mutation

Runtime v1:

```text
.github/workflows/tibia-official-client-re-map-provenance-runtime.yml
commit 7433ce3454f498ff3a00c7cf37ccc696de24137f
run 31803480146 / job 94778101312
```

It fenced the correct Track A client but stopped before any gameplay action because the generated GDB script had a shell quoting defect around `$rsp`. No drag or reload occurred. This is a tooling failure only.

Runtime v2:

```text
.github/workflows/tibia-official-client-re-map-provenance-runtime-v2.yml
commit caa938463356ce9a8ece92e9ae908ba507f501a9
run 31804152128 / job 94778895730
result SUCCESS
client PID 19092
observer armed true
```

The one fixed GUI drag attempt completed, but the named handlers recorded:

```text
CreateOnMap = 0
ChangeOnMap = 0
DeleteOnMap = 0
TRACK_A_CONTROL_ACTION_MUTATION_PROVEN=false
```

The workflow correctly did **not** execute the planned `12 x Right` / `12 x Left` movement because no dynamic event proved that the controlled item operation succeeded.

Classification: **FACT**. This is a clean negative control for that fixed pixel drag only, not evidence that dynamic mutations do not occur.

## FACT — persistent observer prepared for the required physical mutation

Workflow:

```text
.github/workflows/tibia-official-client-re-map-provenance-arm.yml
commit 734f845deace5a26efa09b96a168bea0c05272f0
run 31804340593 / job 94779518010
result SUCCESS
```

The arm job exact-fenced the Track A client and left a post-login GDB collector configured for:

```text
CreateOnMap +0xcecc70
ChangeOnMap +0xcecf40
DeleteOnMap +0xcd4e20
FullMap +0xcec8d0
map-description object hook +0x19a8ea3
```

It records raw inbound registers/pointees for mutation events and 128 bytes of each observed snapshot object entry with structural `x/y/z/stack` context.

Arm-time state:

```text
client PID 19092
observer PID 32587
PIE bias 0x560e600db000
baseline mutation events 0
baseline strip records 0
```

A separate verification workflow exists at `.github/workflows/tibia-official-client-re-map-provenance-verify.yml` to prove that the observer survives GitHub Actions orphan cleanup before owner interaction.

Classification: **FACT** for successful arm-time attachment. Post-job persistence is not a FACT until the verification run succeeds.

## Current provenance model classification

```yaml
SEPARATE_SNAPSHOT_AND_MUTATION_PATHS: FACT
CREATE_HANDLER: FACT_0xcecc70
CHANGE_HANDLER: FACT_0xcecf40
DELETE_HANDLER: FACT_0xcd4e20
CREATE_CHANGE_AND_SNAPSHOT_SHARED_OBJECT_NORMALIZER: FACT_0xceca50
DYNAMIC_ORIGIN_VISIBLE_FROM_EVENT_PATH: FACT
DYNAMIC_MARKER_INSIDE_NORMALIZED_OBJECT_PAYLOAD: NOT_OBSERVED_BY_STATIC_DISASSEMBLY
PERSISTENT_PROVENANCE_FLAG_ELSEWHERE_IN_RUNTIME_STATE: UNKNOWN
PROVENANCE_AFTER_AWARE_RANGE_RELOAD: UNKNOWN
SAME_TYPE_STATIC_VS_DYNAMIC_STRUCTURAL_DIFFERENCE_AFTER_RELOAD: UNKNOWN
SINGLE_SNAPSHOT_SUFFICIENT_FOR_CANONICAL_OTBM: NO_SAFE_BASIS
MODEL_A_PRESERVED: NOT_PROVEN
MODEL_B_EVENT_ONLY: LEADING_INFERENCE_NOT_YET_FINAL
MODEL_C_NO_USEFUL_PROVENANCE: NOT_PROVEN
```

## OTBM consequence now

A single live-world snapshot must **not** be treated as canonical OTBM input without filtering/history. The snapshot is current world state and the object normalization path does not itself prove static origin. In particular, nothing established so far makes snapshot-only presence sufficient evidence that an object belongs permanently to the base map.

Required conservative history classes:

```text
STATIC_CANDIDATE
DYNAMIC_OBSERVED
UNKNOWN_ORIGIN
CREATURE
CORPSE
FIELD
TEMPORARY_EFFECT
```

Interim rules:

1. `CreateOnMap` observation promotes the involved object identity/history to `DYNAMIC_OBSERVED`.
2. A later snapshot occurrence of a history-matched `DYNAMIC_OBSERVED` object must remain dynamic unless independent evidence proves otherwise.
3. Snapshot-only objects start as `UNKNOWN_ORIGIN`, not `STATIC_CANDIDATE`.
4. `UNKNOWN_ORIGIN` must never be silently promoted into canonical OTBM merely from repeated presence in one live session.
5. `CREATURE`, `CORPSE`, `FIELD`, and `TEMPORARY_EFFECT` are excluded or represented separately according to their semantics rather than emitted as permanent terrain/item content.
6. Promotion to `STATIC_CANDIDATE` requires independent corroboration, e.g. repeated clean observations across separated sessions/times plus no dynamic-event history, or comparison with an authoritative/static source.

These filtering rules are a **RECOMMENDATION** constrained by the verified facts and current unknowns. The final promotion/retention rule will be tightened after the live reload experiment.

## Real blocker / next experiment

The remaining decisive runtime experiment requires one genuine item move through the normal client while the persistent observer is armed. The fixed-coordinate automated drag did not produce a mutation, and guessing additional screen coordinates would not be evidence-driven.

After a genuine `CreateOnMap` is captured, the agent can autonomously:

1. decode the event wrapper/object payload from raw evidence;
2. identify the affected coordinate/stack/object entry;
3. move the character far enough to force that coordinate outside the measured aware range;
4. return and capture the object's map-description/snapshot representation;
5. compare the complete observed object-entry fields before/after;
6. test whether any persistent provenance survives reload;
7. if a same-type permanent control is available, compare it using the same collector.

Until that one live mutation exists, items 3–5 cannot be executed without fabricating the controlled object's identity.
