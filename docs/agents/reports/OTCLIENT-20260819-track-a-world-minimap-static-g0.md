# OTCLIENT-TIBIA-RE — world/minimap current-package static G0

```yaml
report_date: 2026-08-19
repository: blakinio/otclient
task_id: OTC-20260819-track-a-world-minimap-static-g0
pr: 545
alias: TIBIA-RE-WORLD-MINIMAP
alias_primary_coverage: F01-F15
execution_class: github_hosted
runtime_access: none
physical_e2e_required: false
producer_run: 32194443653
producer_job: 95895463554
producer_artifact: 9345368809
```

## Result

This package closes the previous dedicated-evidence gap for the minimap rows without acquiring any Track A live-runtime authority.

**FACT:** the exact public Linux package fetched during producer run `32194443653` matched the current-official fingerprint previously retained by PR #528:

```text
packed_sha256   1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked_sha256 ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
unpacked_size   52109920
```

**FACT:** the current exact package exposes a dedicated minimap graph containing controller, visible-area, tile manager/storage, marker controller/storage/overlay/render-info, protocol handler, disk I/O and QML renderer surfaces. It also exposes current exact-build world-map camera/viewport conversion helpers.

**INFERENCE:** this is sufficient to move `F11` and `F12` from `NOT_STARTED` to `PARTIAL`, because the programme's `NOT_STARTED` definition means no dedicated semantic proof package exists and broad static presence is insufficient. The new package is dedicated and exact-build, but it still lacks the data-layout/runtime-semantic proof required for `DONE`.

## Current package minimap graph

### F11 — controller / visible area / floor state

Current exact-build evidence establishes:

- `tibia::gamewindow::TMinimapController`, 24 QMeta methods, including `currentLayerChanged`, `currentLayer`, `setCurrentLayer`, `updateMinimapVisibleAreaFromQuickitemSize`, `onPlayerPositionChanged`, zoom, center, drag, click and move-up/down slots;
- `tibia::minimap::TMinimapVisibleArea` with `restoreZoomLevelFromOptions`;
- `tibia::minimap::TMinimapTileStorage` with load/save/change/reload-visible operations;
- `tibia::minimap::TMinimapRenderInfoStorage` with camera-viewport, marker, passage, viewpoint, active-raid, player-position and clicked-area update inputs;
- static action names `MinimapFloorUp`, `MinimapFloorDown`, directional scrolling and zoom, including current QML/default binding strings for floor up/down.

`F11=PARTIAL`.

Remaining semantic proof for `DONE`:

1. exact `currentLayer` representation and valid range;
2. exact visible-area coordinate/size representation;
3. exact relationship between floor/layer changes and loaded tile/render-info selection;
4. current-build cache/eviction/loading behavior at visible-area boundaries;
5. runtime correlation only if later required by the row contract, under a separately admitted legal runtime package.

### F12 — minimap markers

Current exact-build evidence establishes separate marker responsibilities:

- create/edit/delete game-action type names, including coordinate and full-marker-data variants;
- `TEditMinimapMarkerDialogController` game-action publish/handle path;
- `TMinimapMarkerGameActionHandler`;
- `TMinimapMarkerStorage` with `markersChanged`, disk-save trigger and load-from-file setter;
- `TMinimapMarkerOverlayController` refresh/update path;
- `TMinimapMarkerQmlRenderInfo` fields exposed as `tooltiptext`, `symbol`, and `lastModifiedTimestamp` change signals;
- protobuf types `tibia.protobuf.minimap.MinimapMarker` and `MinimapMarkerFileContent`;
- persistent file-name string `minimapmarkers.bin` and load/serialize/deserialize surfaces.

`F12=PARTIAL`.

Remaining semantic proof for `DONE`:

1. protobuf field schema and coordinate representation;
2. storage key/order/duplicate and overwrite behavior;
3. symbol range and marker limits;
4. exact create/edit/delete serialization path and persistence transaction;
5. restart/reload equivalence if required by the final row contract.

### F13 — world <-> screen coordinate transforms

The exact current package contains:

- `TWorldMapCameraQmlType::coordinateAtPoint` and layer/isometric camera helpers;
- `TWorldMapCameraViewportQmlType::{convertToWorldMapSubfieldCoordinate, convertToWorldMapSubfieldCoordinateForLayer, convertCoordinateToStretchedPixelCoordinate, convertSubfieldCoordinateToStretchedPixelCoordinate, moveWorldMapSubfieldCoordinateToStretchedPixelCoordinate, translateToLayer, translateByStretchedPixelCoordinate, translateBySubfieldOffset}`;
- renderer `TWorldMapCamera` / `TWorldMapCameraViewport` metaobjects;
- `TWorldMapViewport::worldMapVolumeChanged`.

`F13=PARTIAL` remains unchanged, but its evidence is now current-build rather than historical-only for this surface.

Remaining proof: exact field layout/formulas, shearing/scale/zoom/layer terms, clipping/rounding, and a deterministic round-trip oracle.

## F01-F15 coverage after this package

The starting status is PR #536's 2026-08-18 169-row coverage matrix. This package changes only F11 and F12.

| ID | Status after G0 | Evidence boundary / reason |
|---|---|---|
| F01 | PARTIAL | inbound map-family inventory exists; semantic reconstruction remains incomplete |
| F02 | DONE | promoted historical exact worldmap handler/storage dependency graph |
| F03 | PARTIAL | storage semantics/bounds evidence exists; current-build refresh/runtime semantics not complete |
| F04 | PARTIAL | viewport evidence exists; full semantic/current-build proof incomplete |
| F05 | PARTIAL | render-provider evidence exists; full semantic/current-build proof incomplete |
| F06 | PARTIAL | picker evidence exists; full semantic/current-build proof incomplete |
| F07 | PARTIAL | camera evidence exists; this G0 adds current exact-build QML/renderer camera surface |
| F08 | BLOCKED | server-delivered extent causality remains owned by PR #475's separate legal proof path |
| F09 | DONE | the exact historical `[19,14]` one-byte patched-client startup canary is proven by WM-CANARY; this G0 does not reinterpret it as current-build semantic propagation |
| F10 | BLOCKED | map-mutation causality remains unresolved on PR #475 |
| F11 | **PARTIAL** | current exact-build controller/visible-area/floor/layer/tile/render-info package recovered here |
| F12 | **PARTIAL** | current exact-build marker action/storage/overlay/render-info/protobuf/disk package recovered here |
| F13 | PARTIAL | current exact-build transform helper surface strengthened; formulas/round-trip remain open |
| F14 | PARTIAL | World Observation Index design/evidence remains separate and incomplete |
| F15 | PARTIAL | OTBM reconstruction/static-dynamic classification remains incomplete |

### Net delta

```text
before F-area: DONE=2 PARTIAL=9 NOT_STARTED=2 BLOCKED=2 TOTAL=15
after  F-area: DONE=2 PARTIAL=11 NOT_STARTED=0 BLOCKED=2 TOTAL=15
```

This report is a task-local delta. PR #536 remains the owner of the programme-wide 169-row matrix and is not modified by this task.

## World-state boundary

The following states must remain separate:

1. **Minimap UI/controller state** — current layer, visible area, zoom/scroll, markers and tile/render-info caches recovered by this package.
2. **Worldmap Storage state** — world coordinate information, bounds and eviction semantics promoted by earlier static work.
3. **Render/picker/camera projection state** — visible/clipped representation and coordinate transforms.
4. **Server-delivered map extent** — what the server actually sends and under what request/control semantics; still `BLOCKED/UNKNOWN` where PR #475 requires causal physical evidence.
5. **World Observation Index / OTBM reconstruction** — derived reconstruction consumers; they must not reinterpret local minimap persistence as proof of authoritative server extent.

**FACT:** no observation in this G0 package proves that `minimapmarkers.bin`, local minimap tiles, or the minimap visible area are authoritative substitutes for server-delivered world extent.

## Safety / isolation result

```yaml
synology_observed: false
kasmvnc_observed: false
official_client_executed: false
credentials_accessed: false
login_attempted: false
gameplay_attempted: false
client_byte_mutation: false
raw_official_client_committed: false
raw_official_client_artifact_uploaded: false
raw_client_retained_after_producer: false
```

The temporary producer ran only on a GitHub-hosted ephemeral runner. Its uploaded artifact was 5,368 bytes of compact text evidence; the raw packed/unpacked executable was removed before upload.

## Durable evidence

Primary retained evidence:

- `docs/agents/evidence/OTC-20260819-track-a-world-minimap-static-g0/20260819-current-package-minimap-qmeta.md`
- workflow run/job `32194443653 / 95895463554`
- artifact `9345368809`, digest `sha256:c3c32ad9ce527e5ff7d469ae41914f3802fb55d465a993c8dbb32be2840e9755`

Promoted/historical inputs consumed without branch modification:

- `docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md`
- `docs/agents/reports/OTCLIENT-20260816-official-client-map-viewport-feasibility.md`
- `docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md`
- PR #439 World Observation / Atlas boundary
- PR #462 bounded mutation/startup canary boundary
- PR #473 server map extent static boundary
- PR #475 server-delivery causal frontier (read-only dependency)
- PR #528 current-official package fingerprint (read-only dependency)
- PR #536 programme coverage matrix (read-only dependency)
- PR #543 alias mission wording (scope data only; no authority expansion)

## Next discriminators

The highest-value next static package for `F11/F12/F13` is a bounded current-build code/data-layout harvest around the direct static-metacall case targets retained here:

1. `TMinimapController::{currentLayer,setCurrentLayer,updateMinimapVisibleAreaFromQuickitemSize,onMinimapDataChanged}` -> object fields / `TMinimapVisibleArea` ownership and layer bounds;
2. `TMinimapMarkerStorage::{setMarkersFromMinimapMarkerFile,startSavingMinimapMarkerFileContentToDisk}` plus protobuf descriptors -> exact marker schema, coordinate representation and persistence rules;
3. `TWorldMapCameraViewportQmlType` conversion dispatch targets -> exact transform formulas and deterministic round-trip vectors.

That follow-up can remain `RUNTIME_ACCESS:none` unless its own evidence proves that a live discriminator is necessary. It must not inherit PR #475 mutation/login rights.
