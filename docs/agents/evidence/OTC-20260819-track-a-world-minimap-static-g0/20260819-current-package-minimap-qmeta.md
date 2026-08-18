# OTC-20260819 Track A world/minimap G0 — current-package static evidence

```yaml
evidence_date: 2026-08-19
repository: blakinio/otclient
task_id: OTC-20260819-track-a-world-minimap-static-g0
pr: 545
producer_head: 715b4c63271e16ff97ff3bd18498f74a652bae7c
workflow_run: 32194443653
job: 95895463554
artifact_id: 9345368809
artifact_name: track-a-world-minimap-static-g0-32194443653
artifact_digest: sha256:c3c32ad9ce527e5ff7d469ae41914f3802fb55d465a993c8dbb32be2840e9755
artifact_size_bytes: 5368
runtime_access: none
client_executed: false
credentials_accessed: false
login_attempted: false
client_byte_mutation: false
raw_client_retained: false
```

## Exact current public package fence

The GitHub-hosted producer fetched the current public Linux package from CipSoft's launcher endpoint through the repository's existing WARP pattern, decompressed the exact fetched bytes in the ephemeral runner, and failed closed against the durable candidate fence from PR #528.

```text
PACKED_SHA256=1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
UNPACKED_SHA256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
UNPACKED_SIZE=52109920
CURRENT_PACKAGE_FENCE=PASS
MINIMAP_STRING_LINES=291
RAW_CLIENT_RETAINED=false
```

**FACT:** all producer steps completed successfully, including deletion of the packed and unpacked client before artifact upload. The uploaded artifact contains only `fence.txt`, `minimap-qmeta.txt` and `minimap-strings.txt`.

## Current exact-build minimap controller / visible-area surface

```text
CLASS=tibia::gamewindow::TMinimapController
QMETA=0x2f900e0 STATIC=0xd9e1e0 SIGNALS=3 METHODS=24
  currentLayerChanged                         target=0xd9e336
  updateMinimapVisibleAreaFromQuickitemSize  target=0xd9e860
  onPlayerPositionChanged                    target=0xd9e840
  onMinimapDataChanged                       target=0xd9e3ce
  onZoomOutButtonClicked                     target=0xd9e6e8
  onZoomInButtonClicked                      target=0xd9e4c0
  onMoveUpButtonClicked                      target=0xd9e5d0
  onMoveDownButtonClicked                    target=0xd9e390
  onCenterButtonClicked                      target=0xd9e5b0
  onMinimapDragged                           target=0xd9e978
  onMinimapClick                             target=0xd9e8c0
  onMinimapMouseMoved                        target=0xd9e410
  onMinimapMarkerClick                       target=0xd9eab8
  currentLayer                               target=0xd9e7c0
  setCurrentLayer                            target=0xd9e880
```

The omitted controller rows are also retained in the producer artifact; the list above is the semantic subset used by this task.

Additional current exact-build surfaces:

```text
CLASS=tibia::minimap::TMinimapVisibleArea METHODS=1
  restoreZoomLevelFromOptions target=0xde15a0

CLASS=tibia::minimap::TMinimapRenderInfoStorage METHODS=8
  renderInfosChanged
  onCameraViewportChanged
  onPassagesChanged
  onViewpointsChanged
  onActiveRaidsChanged
  onMinimapMarkersChanged
  onPlayerPositionChanged
  onClickedAreaChanged

CLASS=tibia::minimap::TMinimapTileStorage METHODS=8
  startLoadingMinimapTileFromDisk
  startSavingMinimapTileToDisk
  minimapTileChanged
  reloadVisibleMinimap
  loadingMinimapTileSucceeded
  loadingMinimapTileFailed
  saveAllTilesToDisk
  onAsyncEmitTileChangedTimerTimeout
```

Current exact strings also include:

```text
MinimapFloorUp
MinimapFloorDown
MinimapScrollNorth
MinimapScrollEast
MinimapScrollSouth
MinimapScrollWest
MinimapZoomIn
MinimapZoomOut
Alt+PgUp -> MinimapFloorUp
Alt+PgDown -> MinimapFloorDown
```

**FACT:** a current-build controller layer property, visible-area object, floor up/down action names, zoom/scroll actions, player-position callback, tile storage and render-info update surfaces are present.

**INFERENCE (high confidence):** `currentLayer` / `setCurrentLayer`, the move-up/down controller slots and `MinimapFloorUp` / `MinimapFloorDown` form the static control surface for minimap floor/layer movement. Static names do not yet prove the exact layer numeric representation, bounds, or runtime transition semantics.

## Current exact-build minimap marker surface

Controller and game-action bridge:

```text
CLASS=tibia::gamewindow::TEditMinimapMarkerDialogController METHODS=5
  publishGameAction        target=0xd70190
  onCancelClicked          target=0xd701d0
  onOkClicked              target=0xd701f0
  onControllerFinished     target=0xd70210
  handleGameAction         target=0xd70160

CLASS=tibia::minimap::TMinimapMarkerGameActionHandler METHODS=1
  handleGameAction         target=0xde7e28

CLASS=tibia::minimap::TMinimapMarkerOverlayController METHODS=2
  refreshMinimapMarkers    target=0xde1380
  update                   target=0xde13b0
```

Storage / render-info:

```text
CLASS=tibia::minimap::TMinimapMarkerStorage METHODS=5
  requestDelayedCallback                         target=0xde98f0
  markersChanged                                 target=0xde9850
  startSavingMinimapMarkerFileContentToDisk      target=0xde9861
  onDelayedCallback                              target=0xde988b
  setMarkersFromMinimapMarkerFile                target=0xde98b5

CLASS=tibia::minimap::TMinimapMarkerQmlRenderInfo METHODS=3
  tooltiptextChanged             target=0xde6e38
  symbolChanged                  target=0xde6e28
  lastModifiedTimestampChanged   target=0xde6da0
```

Current exact strings include the following neutral type/data-path names:

```text
TGameActionDeleteMinimapMarker
TGameActionShowDialogEditMinimapMarker
TGameActionShowDialogCreateMinimapMarker
TGameActionForMinimapMarkerUsingCoordinate
TGameActionForMinimapMarkerUsingFullMarkerData
MinimapMarker.qml
EditMinimapMarkerDialog.qml
tibia.protobuf.minimap.MinimapMarker
tibia.protobuf.minimap.MinimapMarkerFileContent
minimapmarkers.bin
loadingMinimapMarkersSucceeded
serializeMinimapMarkerFileContent malformed protobuf data
deserializeMinimapMarkerFileContent malformed protobuf data
```

**FACT:** the current package has separate create/edit/delete marker game-action types, a coordinate/full-marker-data bridge, edit-dialog controller, marker controller/storage/overlay/render-info types, protobuf marker persistence and a disk marker file name.

**UNKNOWN:** protobuf field numbers/semantics, marker coordinate serialization details, conflict/overwrite policy, maximum marker count, and runtime persistence behavior across restart were not recovered by this G0 package.

## Current exact-build coordinate-transform surface

```text
CLASS=tibia::qmlcomponents::TWorldMapCameraQmlType METHODS=6
  cameraViewportChanged                  target=0x16b1dc0
  onTopLeftCoordinateChanged             target=0x16b1de0
  coordinateAtPoint                      target=0x16b1df0
  changeLayerWithIsometricProjection     target=0x16b1ea0
  moveDistanceRelativeToReferencePoint   target=0x16b1f70
  centerAtSubfieldCoordinateDelayed      target=0x16b1d60

CLASS=tibia::qmlcomponents::TWorldMapCameraViewportQmlType METHODS=12
  viewportChanged                                      target=0x16b24f8
  convertToWorldMapSubfieldCoordinate                  target=0x16b24c0
  convertToWorldMapSubfieldCoordinateForLayer          target=0x16b2488
  convertCoordinateToStretchedPixelCoordinate          target=0x16b2368
  convertSubfieldCoordinateToStretchedPixelCoordinate  target=0x16b2368
  zoomAtPoint                                          target=0x16b2368
  moveWorldMapSubfieldCoordinateToStretchedPixelCoordinate target=0x16b2478
  translateToLayer                                     target=0x16b2450
  setTopAndBottomLayer                                 target=0x16b2fd0
  setAdditionalColumnsAndRows                         target=0x16b2e90
  translateByStretchedPixelCoordinate                 target=0x16b2eb0
  translateBySubfieldOffset                           target=0x16b2ef0
```

Additional current exact-build metaobjects:

```text
tibia::renderer::TWorldMapCamera
  cameraViewportChanged
  geometryIntialized

tibia::renderer::TWorldMapCameraViewport
  viewportChanged

tibia::worldmap::TWorldMapViewport
  worldMapVolumeChanged target=0xe00130
```

**FACT:** current-package world-map camera/QML viewport conversion and layer-translation surfaces exist with direct static-metacall targets for the QML layer.

**UNKNOWN:** this package did not recover the mathematical field layout/formulas or prove a semantic round-trip `world -> screen -> world` on a live state.

## Bounded coverage consequence

Compared with the 2026-08-18 coverage matrix on PR #536:

```text
F11 Minimap controller / visible area / floor state  NOT_STARTED -> PARTIAL
F12 Minimap markers                                  NOT_STARTED -> PARTIAL
F13 World <-> screen coordinate transforms           PARTIAL -> PARTIAL (strengthened by current exact-build evidence)
```

No other F-row is promoted by this producer. In particular:

```text
F08 server-delivered extent  remains BLOCKED
F10 map mutation causality   remains BLOCKED
```

The current package census does not authorize or replace PR #475's separate physical causal proof.
