# P0 alternate player-position observer route — exact-SHA retained evidence

## Scope

This note records a new hosted-only structural hypothesis from the already-retained exact-client artifact `9248797952` / run `31892019505`. No Synology execution, process-memory access, login, gameplay input or proprietary client bytes were used in this continuation.

Exact client fence from the retained run:

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

## Direct retained strings — FACT

The retained `player-position-graph.txt` contains a second tightly grouped position-related cluster around `tibia::cyclopedia::TCyclopediaMapStorage`:

```text
0x1d2a44c  tibia::minimap::TMinimapRenderInfoStorage
0x1d2a476  renderInfosChanged
0x1d2a48a  onCameraViewportChanged
0x1d2a4f5  onPlayerPositionChanged
0x1d2a580  tibia::cyclopedia::TCyclopediaMapStorage
...
0x1d2a8d8  tibia::cyclopedia::TCyclopediaMapStorage
0x1d2a937  playerPositionChanged
0x1d2a95d  tibia::worldmap::TWorldMapCoordinate
0x1d2a982  WorldMapCoordinate
...
0x1d2aa4a  onPlayerCreatureAddedToGameSession
0x1d2aa6d  std::weak_ptr<tibia::creatures::TCreature>
0x1d2aa98  pPlayer
0x1d2aaa0  onPlayerPositionWasUpdated
```

These strings are preserved by the exact-SHA artifact and are independent of the failed GDB instruction-window step at `0x8367c1`.

## Classification

### FACT

- the exact client contains a `TCyclopediaMapStorage` metadata/string neighborhood containing `playerPositionChanged`;
- the same neighborhood contains `tibia::worldmap::TWorldMapCoordinate` / `WorldMapCoordinate`;
- the same neighborhood contains `onPlayerCreatureAddedToGameSession`, `std::weak_ptr<tibia::creatures::TCreature>`, `pPlayer`, and `onPlayerPositionWasUpdated`;
- the current retained artifact does not contain the executable instruction bodies or member offsets implementing this route.

### DERIVED

The co-located metadata strongly supports an alternate observer-chain hypothesis:

```text
player creature enters game session
-> TCyclopediaMapStorage retains/observes weak_ptr<TCreature> pPlayer
-> player position update callback
-> TWorldMapCoordinate-valued position state/change
-> playerPositionChanged notification
```

This is a more semantically direct candidate for a structural player-position read than treating the `playerPosition` string xref at `0x8367c1` as if it were already a `TPlayerData` member accessor.

### UNKNOWN

- exact object/member offset for `pPlayer`;
- exact `TCreature` position member/accessor;
- exact `TWorldMapCoordinate` storage layout at this observer boundary;
- whether `playerPositionChanged` carries the coordinate directly or only signals a separately stored value;
- exact owning functions and xrefs;
- live correlation and restart/relogin stability.

## Rejected overclaim

Do **not** claim that `0x8367c1` is a direct `TPlayerData::position` accessor. Current evidence proves only that it references the `playerPosition` string. The alternate Cyclopedia/player-creature observer route is now the preferred structural hypothesis because its exact-SHA metadata explicitly binds player lifecycle, player-position update callbacks and `TWorldMapCoordinate` semantics in one local cluster.

## Next hosted action

Prefer a compliant sanitized exact-client evidence bundle containing code/data windows for the `TCyclopediaMapStorage` metadata/object graph, especially xrefs or object-layout evidence for:

- `onPlayerCreatureAddedToGameSession`;
- `pPlayer` / `weak_ptr<TCreature>`;
- `onPlayerPositionWasUpdated`;
- `playerPositionChanged`;
- `TWorldMapCoordinate`.

If such a bundle is unavailable, retain the original `0x8367c1` window as a secondary static target. Physical before/after XYZ correlation, negative controls and fresh-PID/relogin confirmation remain RUNTIME-owned.
