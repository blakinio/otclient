# Track A world/minimap static G1 — layout, marker persistence and transform evidence

```yaml
evidence_date: 2026-08-19
repository: blakinio/otclient
task_id: OTC-20260819-track-a-world-minimap-static-g1
pr: 593
execution_class: github_hosted
runtime_access: none
client_executed: false
credentials_accessed: false
login_attempted: false
gameplay_attempted: false
client_byte_mutation: false
evidence_status: historical_unverified_transcription
promotion_authority: false
primary_artifacts_available: false
e2e_result: NOT_APPLICABLE
e2e_reason: documentation-only GitHub-hosted static evidence; no executable, UI, runtime, network, or product behavior changed
remediation_date: 2026-09-01
trusted_main_at_remediation: 54a20bbd8721e92d069974af14d6ebd2f4f5a55d
trusted_track_a_fence_at_remediation: 15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
```

## Producer provenance

On 2026-08-19, two disposable GitHub-hosted producers were used against the then-current public Linux package fence. Their compact text artifacts have since expired, so the sections below are retained as historical transcriptions/hypotheses rather than independently replayable promotion evidence.

### Producer v1 — strict Qt method-ID discriminator + bounded schema scan

```text
head:      eff3ddf9c2054c1398975d1a2939a5cd01259b63
run/job:   32249741341 / 96057873107
result:    SUCCESS
artifact:  9363988901
artifact:  track-a-world-minimap-static-g1-32249741341
zip sha:   68e1864b990742814d11501fbf6757fcf5da4677d3718bf093227173ba4d5745
size:      38862 bytes
artifact_status: EXPIRED (HTTP 410 on 2026-09-01)
files:     fence.txt, marker-protobuf-persistence.txt, qt-dispatch-code.txt
```

The original v1 producer reported several Qt `static_metacall` method-ID jump tables by requiring all of the following simultaneously: method-ID lineage from the Qt metacall argument, an exact `method_count - 1` bounds check, a RIP-relative 32-bit relative table indexed by that method ID, an add-to-table-base step, and the final indirect jump.

One v1 post-processing step was **not** accepted: after identifying a method case, it searched too far through adjacent case code for the first direct `call`. That could attribute a later case's call to the current method. G1 therefore rejects every v1 `first_direct_call=...` field unless a later direct disassembly window independently proves the same edge. This is a producer interpretation repair, not a failure of the strict method-ID table mapping itself.

### Producer v2 — direct focused disassembly, no call-attribution heuristic

```text
head:      91004362eaa5562cf268fff455c161b6f55dc7c2
run/job:   32250742374 / 96060897630
result:    SUCCESS
artifact:  9364339983
artifact:  track-a-world-minimap-static-g1-v2-32250742374
zip sha:   ba5cdae01c702c618a9944de6b4630605ed3eae85b0bed3f0ba66ec69d3ba81f
size:      54292 bytes
artifact_status: EXPIRED (HTTP 410 on 2026-09-01)
files:     fence.txt, focused-disassembly.txt, focused-strings.txt, focused-xrefs.txt
```

The original producer v2 emitted bounded `objdump` windows and exact RIP-relative string/xref inventories only. It performs no semantic call-target inference.

On v2 producer head, repository checks also passed:

```text
Track A agent runtime governance 32250742373 = SUCCESS
CI                               32250742591 = SUCCESS
```

## 2026-09-01 independent-audit remediation

Fresh independent Codex `gpt-5.6-luna` / `medium` audit session `01a05dcd-59a6-7523-94c4-5c6e7d585f11` returned `AUDIT_FAIL` with `WM-G1-AUD-001..003`.

Primary producer artifacts `9363988901` and `9364339983` are confirmed expired by GitHub (`HTTP 410`). Exact historical jobs were rerun without changing their definitions:

```text
v1 rerun job 99940034906: FAIL_CLOSED at historical package fence
v2 rerun job 99940062914: FAIL_CLOSED at historical package fence
fresh public packed SHA observed by v1: 439db64ead9b62aa0870094fa0ce30e8e0ccaf35844de1a515692770a7019036
raw client retained: false
analysis/disassembly steps: skipped after fence mismatch
```

The current trusted repository fence at remediation is `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`, while these historical transcriptions came from `15.32 / 52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`. The September 1 public URL had already moved again; its unpacked identity was intentionally not derived after the packed fence mismatch. Therefore none of the address/offset/formula transcriptions below are promoted to the current trusted build. They are bounded hypotheses for a future fresh exact-build producer only.

## Historical 2026-08-19 public-package fence (superseded)

Both original producers were fenced to the following 2026-08-19 public package. This fence is now superseded and is not the current trusted Track A client fence:

```text
PACKED_SHA256=1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
UNPACKED_SHA256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
UNPACKED_SIZE=52109920
CURRENT_PACKAGE_FENCE=PASS
RAW_CLIENT_RETAINED=false
```

**HISTORICAL TRANSCRIPTION (not promotion authority):** the official-client package was ephemeral. The packed and unpacked executable bytes were removed before each artifact upload. Only compact text evidence was retained.

---

# F11 — minimap layer and visible-area layout

## Exact Qt method dispatch

For `tibia::gamewindow::TMinimapController` the v1 method-ID discriminator recovered one unique direct jump table:

```text
QMETA  = 0x2f900e0
STATIC = 0xd9e1e0
METHODS= 24
TABLE  = 0x1da27d8

0xd9e200  lea     rcx,[rip+...]
0xd9e209  movsxd  rax,DWORD PTR [rcx+rdx*4]
0xd9e210  add     rax,rcx
0xd9e213  jmp     rax
```

Relevant exact method cases:

```text
index  1 currentLayerChanged                        case 0xd9e336
index  3 updateMinimapVisibleAreaFromQuickitemSize case 0xd9e860
index  4 onPlayerPositionChanged                   case 0xd9e840
index  5 onMinimapDataChanged                      case 0xd9e3ce
index  9 onMoveUpButtonClicked                     case 0xd9e5d0
index 10 onMoveDownButtonClicked                   case 0xd9e390
index 21 currentLayer                              case 0xd9e7c0
index 22 setCurrentLayer                           case 0xd9e880
```

The v2 direct disassembly independently covers the entire controller static-metacall region and the called layout/recompute neighborhoods.

## Layer ownership, representation and bounds

### `currentLayer`

The exact case reads:

```text
state = [controller + 0x48]
layer = int32(state + 0x60)
```

A virtual-slot identity fence is present before the direct read, but this evidence does not assign a source-level C++ type name to the internal state object.

**HISTORICAL TRANSCRIPTION (not promotion authority):** the minimap controller owns/references an internal state object through `controller + 0x48`, and the transcribed minimap layer is a signed 32-bit integer at that object's `+0x60`.

### Floor up/down

The direct cases operate on the same `state + 0x60` field:

```text
onMoveUpButtonClicked:   layer := layer - 1
onMoveDownButtonClicked: layer := layer + 1
```

Both flow into an exact clamp:

```text
if layer < 0:    layer = 0
if layer > 0x0f: layer = 0x0f
```

then call the same viewport/recompute path.

**HISTORICAL TRANSCRIPTION (not promotion authority):** the transcribed 2026-08-19 minimap layer range enforced by these controller paths is **0..15 inclusive**.

### `setCurrentLayer`

The direct method case enters the same setter block and:

1. loads the requested signed 32-bit layer from Qt argv;
2. returns without mutation if it already equals `state + 0x60`;
3. clamps the request to `0..15`;
4. stores it to `state + 0x60`;
5. invokes the viewport/recompute path;
6. invokes the controller refresh path;
7. emits the Qt signal whose metadata identity is `currentLayerChanged`.

**HISTORICAL TRANSCRIPTION (not promotion authority):** `setCurrentLayer` is not an unchecked UI-only assignment. The transcribed 2026-08-19 code clamps the authoritative controller field to the same `0..15` range and triggers recomputation plus a layer-change notification.

## Visible-area pixel-size input

`updateMinimapVisibleAreaFromQuickitemSize` is a direct tail jump from exact case `0xd9e860` into the direct v2-disassembled implementation at `0xf054c0`.

The implementation:

1. loads the internal state object from `controller + 0x48`;
2. loads a `QQuickItem` from `controller + 0x90`;
3. calls `QQuickItem::height()` and `QQuickItem::width()`;
4. converts the two floating-point values to 32-bit integers;
5. in the direct path stores the pair at the state object;
6. enters the viewport/recompute path and the common controller refresh path.

The exact packed ordering is:

```text
state + 0x84 = integer width
state + 0x88 = integer height
```

**HISTORICAL TRANSCRIPTION (not promotion authority):** the transcribed 2026-08-19 minimap visible-area recomputation is directly fed by the actual QML quick-item pixel width/height, with an integer width/height pair stored at internal state offsets `+0x84/+0x88` on the direct expected path.

## Recompute structure

The bounded direct recompute neighborhood reads additional integer state around `+0x58/+0x5c`, reads a floating-point zoom/scale value at `+0x80`, updates transform/matrix state in the following object region and calls matrix scale/translate helpers.

**UNKNOWN:** G1 does not yet prove source-level member names for the complete internal state object, the exact semantic meaning of every matrix/input field, or the full tile/cache loading and eviction transition at visible-area edges.

### F11 disposition

```text
F11 = PARTIAL
```

The values above are retained only as hypotheses transcribed from the expired 2026-08-19 producers. G1 does not promote them into current trusted authority. F11 remains `PARTIAL` on previously promoted evidence, pending a fresh exact-build producer.

---

# F12 — minimap marker persistence boundary

## Exact Qt storage surface

For `tibia::minimap::TMinimapMarkerStorage`, the strict method-ID discriminator recovered one unique direct jump table:

```text
TABLE = 0x1daa3b0

0xde7b19  lea     rsi,[rip+...]
0xde7b22  movsxd  rax,DWORD PTR [rsi+rdx*4]
0xde7b29  add     rax,rsi
0xde7b2c  jmp     rax
```

Qt metadata reports:

```text
SIGNALS=3
METHODS=5
```

Therefore the first three entries are signals, not ordinary implementation slots:

```text
index 0  requestDelayedCallback
index 1  markersChanged
index 2  startSavingMinimapMarkerFileContentToDisk
index 3  onDelayedCallback
index 4  setMarkersFromMinimapMarkerFile
```

This corrects any earlier wording that treated signal entries as ordinary direct native methods.

## Save signal payload

The exact `startSavingMinimapMarkerFileContentToDisk` signal case constructs/retains a shared-ownership payload, emits Qt signal index `2`, and releases its local retained reference afterwards. Exact retained type-name evidence identifies the payload family as `shared_ptr<...MinimapMarkerFileContent>`.

**HISTORICAL TRANSCRIPTION (not promotion authority):** marker-file saving is exposed as a Qt signal carrying a shared `MinimapMarkerFileContent` object rather than as a proven synchronous file write at the signal case itself.

## Load/set and delayed-save gate

`setMarkersFromMinimapMarkerFile` dispatches through an exact virtual slot at object vtable `+0xa0`, passing the Qt argument payload. G1 does not assign a source method name to the vslot target without an independent identity proof.

`onDelayedCallback` has an exact state gate:

```text
if byte(storage + 0x40) == 0:
    return
else:
    dispatch through vtable +0x88
```

**HISTORICAL TRANSCRIPTION (not promotion authority):** a one-byte state/dirty-like gate at `TMinimapMarkerStorage + 0x40` controls whether the delayed callback proceeds to the save-side virtual operation.

**UNKNOWN:** the byte's exact source member name and every state transition that sets/clears it are not proven by this bounded package.

## Protobuf and disk evidence

Transcribed 2026-08-19 package strings/xrefs include:

```text
tibia.protobuf.minimap.MinimapMarker
tibia.protobuf.minimap.MinimapMarkerFileContent
minimapmarkers.bin
deserializeMinimapMarkerFileContent malformed protobuf data
serializeMinimapMarkerFileContent malformed protobuf data
Did not load any minimap markers from disk due to:
Failed to write minimap markers to disk due to:
TGameActionForMinimapMarkerUsingCoordinate
TGameActionForMinimapMarkerUsingFullMarkerData
```

The bounded v1 raw `FileDescriptorProto` scan returned:

```text
MINIMAP_DESCRIPTOR_CANDIDATES=0
```

This is a **non-recovery result**, not evidence that a protobuf schema or descriptor does not exist. The exact type/serializer/error strings demonstrate protobuf use, but the field-number/type table was not reconstructed by this scan.

Additional transcribed 2026-08-19 QML/render-info strings expose properties such as tooltip text, symbol and last-modified timestamp. They are not promoted as protobuf field numbers merely because they are adjacent semantic concepts.

### F12 disposition

```text
F12 = PARTIAL
```

The storage/save/load details above are retained only as historical hypotheses because their primary artifact expired. G1 does not promote them into current trusted authority. F12 remains `PARTIAL`; exact marker protobuf field schema, duplicate/overwrite policy, marker limits and complete restart/reload transaction remain **UNKNOWN**.

---

# F13 — world/subfield/stretched-pixel transform formulas

## Exact Qt method dispatch

For `tibia::qmlcomponents::TWorldMapCameraViewportQmlType`, the strict method-ID discriminator recovered one unique direct jump table:

```text
TABLE = 0x1fe6a14

0x16b2310  lea     rcx,[rip+...]
0x16b2319  movsxd  rax,DWORD PTR [rcx+rdx*4]
0x16b2320  add     rax,rcx
0x16b2323  jmp     rax
```

Relevant exact cases:

```text
index  1 convertToWorldMapSubfieldCoordinate                 0x16b28b8
index  2 convertToWorldMapSubfieldCoordinateForLayer         0x16b2960
index  3 convertCoordinateToStretchedPixelCoordinate         0x16b29a0
index  4 convertSubfieldCoordinateToStretchedPixelCoordinate 0x16b2620
index  5 zoomAtPoint                                         0x16b2668
index  6 moveWorldMapSubfieldCoordinateToStretchedPixelCoordinate 0x16b2710
index  7 translateToLayer                                    0x16b27a0
index  8 setTopAndBottomLayer                                0x16b27c0
index  9 setAdditionalColumnsAndRows                         0x16b27d8
index 10 translateByStretchedPixelCoordinate                 0x16b2840
index 11 translateBySubfieldOffset                           0x16b2868
```

Unlike the rejected G0/v1 broad target heuristic, the mappings above come from the exact Qt method-ID discriminator itself. The subsequent helper edges below are taken from direct bounded disassembly of those exact cases.

## Forward subfield -> stretched-pixel layer term

Both subfield-to-pixel entry paths were transcribed as calling helper `0xc3a4e0`.

The exact helper reads:

```text
L = int32(subfield + 0x10)
(x,y) = int32x2(subfield + 0x08)
layer_term = 32 * L
(x,y) := (x + layer_term, y + layer_term)
mode = int32(viewport + 0x6c)
```

If `mode == 0`, the helper returns that integer pair immediately.

**HISTORICAL TRANSCRIPTION (not promotion authority):** in projection mode `0`, the transcribed 2026-08-19 forward transform is:

```text
X = x + 32*L
Y = y + 32*L
```

The non-zero mode continues through scale/offset/projection and explicit floating-point-to-integer rounding code. G1 does not assign source-level semantic names to all of those terms yet.

## Inverse stretched-pixel -> subfield layer term

`convertToWorldMapSubfieldCoordinate` and `convertToWorldMapSubfieldCoordinateForLayer` were transcribed as entering helper `0xc39e50` with the target layer supplied either from the viewport state or the explicit method argument.

At the output boundary, the exact helper:

1. stores the requested layer `L` in the subfield output;
2. computes `32*L`;
3. subtracts that same value from both transformed integer coordinates before storing subfield `x/y`.

For projection mode `0`, no extra projected coordinate change precedes this final subtraction.

**HISTORICAL TRANSCRIPTION (not promotion authority):** in projection mode `0`, the inverse is:

```text
x = X - 32*L
y = Y - 32*L
layer = L
```

## Deterministic static round-trip oracle

The two direct mode-0 formulas form an exact algebraic round trip for the same layer:

```text
(x,y,L)
 -> (x + 32L, y + 32L)
 -> ((x + 32L) - 32L, (y + 32L) - 32L, L)
 = (x,y,L)
```

Concrete vector derived from the exact code:

```text
input subfield:       (3, 5, 7)
32*layer:             224
forward stretched:   (227, 229)
inverse same layer:  (3, 5, 7)
```

This is a deterministic **static formula oracle**, not a claim of live UI/runtime E2E.

## Additional viewport state

Direct exact cases establish additional bounded layout facts:

- `setAdditionalColumnsAndRows` packs its four signed 32-bit arguments into the viewport object at `+0xa0..+0xaf` and schedules delayed recomputation through a `QTimer` when needed;
- `translateBySubfieldOffset` adds the supplied two-component integer offset component-wise to the viewport pair stored at `+0x88` before entering the common translation path;
- `moveWorldMapSubfieldCoordinateToStretchedPixelCoordinate` was transcribed as using the inverse/forward helper family together with layer and viewport-offset state, but G1 does not promote a simplified global formula for that compound path.

## Projection-mode boundary

**UNKNOWN:** G1 does not yet assign complete semantic names/formulas to every non-zero projection mode, shearing/scale term, clipping decision and rounding boundary. It also does not provide a live click/pick round trip on a governed `IN_GAME` runtime.

### F13 disposition

```text
F13 = PARTIAL
```

The formula/offset details above are retained only as historical hypotheses because their primary artifact expired. G1 does not promote them into current trusted authority. F13 remains `PARTIAL`; full projection semantics and any required live interaction/stability boundary remain incomplete.

---

# Coverage consequence

After audit remediation, this G1 package retains **no new canonical semantic promotion**. The prior promoted row statuses remain:

```text
F11 PARTIAL -> PARTIAL  (historical hypotheses retained; no new canonical promotion)
F12 PARTIAL -> PARTIAL  (historical hypotheses retained; exact protobuf fields still UNKNOWN)
F13 PARTIAL -> PARTIAL  (historical hypotheses retained; no new canonical promotion)
F08 BLOCKED -> BLOCKED  (unchanged; #475-owned causal frontier)
F10 BLOCKED -> BLOCKED  (unchanged; #475-owned causal frontier)
```

The absence of a status delta is intentional. The expired primary artifacts prevent the transcribed internal fields/formulas from serving as current promotion authority.

# Safety / non-claims

This evidence does **not** establish facts for the current trusted client `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a` or any later public package. It also does **not** establish:

- a current canonical live runtime;
- live minimap movement or marker persistence;
- server-delivered map extent;
- `[19,14]` worldmap patch causality;
- a complete marker protobuf field schema;
- complete non-zero projection formulas;
- a full live picker/click round trip;
- restart/relogin stability.

No credentials, secrets, login, gameplay, GUI input, Synology/KasmVNC observation, process-memory access or client-byte mutation were used.