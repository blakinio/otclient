# OTCLIENT-TIBIA-RE — world/minimap static G0 promotion

```yaml
report_date: 2026-08-19
repository: blakinio/otclient
source_task: OTC-20260819-track-a-world-minimap-static-g0
source_pr: 545
source_head: 55034d31a3cfd55c597f463c97ebf97065192c8b
promotion_decision: ACCEPT_WITH_EDITS
execution_class: github_hosted
runtime_access: none
physical_e2e_required: false
```

## Result

The bounded `TIBIA-RE-WORLD-MINIMAP` static package is accepted with coordinator edits for F11/F12 and current-public-package strengthening of F13.

Independent artifact verification confirms:

```text
artifact 9345368809
artifact sha256 c3c32ad9ce527e5ff7d469ae41914f3802fb55d465a993c8dbb32be2840e9755
packed sha256  1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked sha256 ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
unpacked size   52109920
CURRENT_PACKAGE_FENCE=PASS
RAW_CLIENT_RETAINED=false
```

The artifact contains exactly three compact text files and no raw client binary.

## Coordinator correction

`WM-MINIMAP-AUD-001` rejects the producer's per-method `target=... direct=true` values. The jump-table selection heuristic is not sufficient to bind a particular relative table to Qt method dispatch, and the artifact itself shows unrelated metaobjects receiving identical reported targets.

Promoted evidence therefore includes exact package fingerprint, Qt class/method ownership, QMeta/static-metacall identity and static strings, but **not** the heuristic per-method code destinations.

## F11 — Minimap controller / visible area / floor state

Accepted exact-package structural evidence includes:

- `TMinimapController` with 24 QMeta methods covering `currentLayer`, `setCurrentLayer`, visible-area refresh, player-position updates, zoom, scrolling, center, drag/click and marker click;
- `TMinimapVisibleArea`;
- `TMinimapTileManager` and `TMinimapTileStorage` load/save/change/reload surfaces;
- `TMinimapRenderInfoStorage` camera/marker/passage/viewpoint/raid/player/click update surfaces;
- exact action strings `MinimapFloorUp`, `MinimapFloorDown`, directional scroll and zoom, including `Alt+PgUp/PgDown` bindings.

Disposition: `F11 NOT_STARTED -> PARTIAL`.

Still UNKNOWN: layer representation/range, visible-area field layout, tile/cache boundary behavior and live causal semantics.

## F12 — Minimap markers

Accepted exact-package structural evidence includes:

- create/edit/delete marker action-type strings;
- coordinate and full-marker-data marker action variants;
- marker edit dialog controller and game-action handler;
- marker storage, overlay controller and QML render-info metaobjects;
- protobuf type strings for `MinimapMarker` and `MinimapMarkerFileContent`;
- `minimapmarkers.bin` plus load/serialize/deserialize/save surfaces.

Disposition: `F12 NOT_STARTED -> PARTIAL`.

Still UNKNOWN: protobuf fields, coordinate encoding, duplicate/overwrite rules, limits, symbol range and restart/reload equivalence.

## F13 — World/screen coordinate transforms

Current public-package Qt metadata confirms world-map camera/viewport method-name surfaces including `coordinateAtPoint`, conversion to world-map subfield coordinates, conversion to stretched pixel coordinates, `translateToLayer`, zoom and relative translations.

Disposition: `F13 PARTIAL -> PARTIAL` with current-public-package evidence strengthening.

Still UNKNOWN: exact formulas/layout, projection terms, rounding/clipping and deterministic round-trip behavior.

## Coverage boundary

Against PR #536's status contract:

```text
before F-area: DONE=2 PARTIAL=9  NOT_STARTED=2 BLOCKED=2
local delta:   F11 -> PARTIAL; F12 -> PARTIAL; F13 unchanged PARTIAL
after local:   DONE=2 PARTIAL=11 NOT_STARTED=0 BLOCKED=2
```

This report does not edit PR #536's shared coverage matrix. F08 server-delivery causality and F10 patch propagation remain blocked and unchanged.

## Important non-claims

The exact fetched public package fingerprint is not proof of the bytes of a currently installed/canonical runtime. The package establishes no:

- live minimap behavior;
- current canonical runtime identity;
- per-method native entry addresses;
- server-delivered extent change;
- worldmap mutation propagation;
- marker persistence transaction semantics;
- world/screen formula correctness;
- OTBM/global-map completeness.

## Validation and audit

Source exact head:

```text
55034d31a3cfd55c597f463c97ebf97065192c8b
Track A governance 32194785639 = SUCCESS
CI 32194785866 = SUCCESS
```

Fresh coordinator audit review: `4969045959`.

Material finding `WM-MINIMAP-AUD-001` is repaired by this promotion package. Open material findings after repair: `0`.

E2E: `NOT_APPLICABLE` — static GitHub-hosted package with `runtime_access: none`.

## Next bounded discriminator

A future static package may inspect exact data/code around:

1. minimap layer/visible-area object fields and bounds;
2. marker protobuf descriptors/storage rules;
3. world-map camera/viewport conversion formulas and round-trip vectors.

That follow-up should remain `runtime_access: none` unless direct evidence shows a live discriminator is required. It must not inherit PR #475 mutation/login authority.