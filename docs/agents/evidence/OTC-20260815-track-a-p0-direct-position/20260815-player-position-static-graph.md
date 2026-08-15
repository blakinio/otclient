# Track A P0 — exact-ELF `playerPosition` static graph

Task: `OTC-20260815-track-a-p0-direct-position`
Run: `31892019505`
Job: `95029600292`
Code-bearing head: `a3068a6a9460525cb1946186cf439caf7832e176`
Runner: `synology-otclient-01`
Mode: side-effect-free static ELF analysis only

## Exact client fence

```text
version mapping: 15.32.df7b29
size: 51965216
SHA-256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TPlayerData primary vptr: 0x308ca70
```

The exact fence passed before any build-specific address was used.

## FACT — bounded semantic anchors

The run resolved the following exact-file anchors:

```text
playerPosition[0]              0x1cdde3f
playerPosition[1]              0x1d2a937  (substring of playerPositionChanged)
TWorldMapRenderProvider RTTI   0x1cdb59c, 0x1cddd20
TWorldMapViewport RTTI         0x1cabb7c, 0x1ce1b60
IPlayerDataProvider RTTI       0x1ce1ba0
TPlayerData RTTI               0x1cabdbc, 0x1ce1bd0
```

This corrects the earlier task-record transcription `0x1cddd3f`: the exact run proves the primary literal is `0x1cdde3f`.

The narrow executable RIP-reference decoder found exactly one unique code site for the primary literal (reported twice because the bounded byte decoder can begin at the REX prefix or opcode byte):

```text
0x8367c1 -> 0x1cdde3f  lea  playerPosition[0]
0x8367c2 -> 0x1cdde3f  lea  same instruction / decoder overlap
```

No direct code xref was recovered to the Cyclopedia `playerPositionChanged` substring in this bounded decoder.

## FACT — typeinfo relationships

RELATIVE relocation-backed type-name references were recovered in `.data.rel.ro`:

```text
0x3089b78 -> 0x1cddd20  TWorldMapRenderProvider
0x308b598 -> 0x1ce1b60  TWorldMapViewport
0x308b5b0 -> 0x1ce1ba0  IPlayerDataProvider
0x308b5c0 -> 0x1ce1bd0  TPlayerData
```

The exact `TPlayerData` primary vtable remains `0x308ca70`, offset-to-top `0`, typeinfo `0x308b5b8`.

Selected executable slots retained for later bounded decoding include:

```text
slot 0  0xd1cbd0
slot 1  0xd2ac70
slot 2  0xd2ef30
slot 3  0x843e20
slot 4  0x843f60
slot 12 0xeda3c0
slot 13 0xee0010
slot 14 0xeda3e0
slot 15 0xee0100
```

## FACT — semantic neighborhood / negative control

The local string neighborhood around the primary `playerPosition` literal includes:

```text
TWorldMapRenderProvider
bad optional access
statusBarData
%1,%2,%3
playerPosition
characterName
worldName
lightEffectsActive
frameRateLimitActive
vsyncActive
```

This makes the literal a high-value game-window/render/provider property lead, but the string alone is not proof that its backing value is authoritative player state.

The second `playerPosition` substring is explicitly distinguishable as a Cyclopedia-map signal context:

```text
onPlayerPositionChanged
playerPositionChanged
tibia::worldmap::TWorldMapCoordinate
onPlayerCreatureAddedToGameSession
pPlayer
onPlayerPositionWasUpdated
```

It is retained as a negative/control context and must not be promoted as the direct player field without live causal evidence.

## Tooling discriminator

The exact task-local GDB was discovered at:

```text
/work/_otclient_tibia_re_state/toolroot/usr/bin/gdb
```

but the bounded static disassembly command did not execute because that invocation lacked the toolroot runtime library path and failed on `libpython3.12.so.1.0`. The overall static job remained successful because the structural graph itself was complete and the disassembly failure was explicitly recorded. No runtime attach was attempted.

## Classification

### FACT

- `playerPosition` primary literal exact VA is `0x1cdde3f`;
- its unique bounded direct executable reference is the instruction at `0x8367c1`;
- `TWorldMapRenderProvider`, `TWorldMapViewport`, `IPlayerDataProvider`, `TPlayerData` and the primary property are now linked by exact-file structural provenance;
- the Cyclopedia `playerPositionChanged` context is separately identifiable and should be treated as a negative/control context;
- exact client identity and P0 `TPlayerData` vptr provenance remain reproducible.

### INFERENCE

`0x8367c1` is the highest-information static code site to decode next, followed by the selected `TPlayerData` virtual functions. A live read should prioritize provider/owner storage reached from these structurally justified paths before broader typed-owner candidate enumeration.

### UNKNOWN / INCONCLUSIVE

- the member/accessor reached by `0x8367c1`;
- exact backing storage offset/encoding for authoritative player XYZ;
- whether the property is direct player state versus a render/status copy;
- causal change semantics;
- fresh PID/relogin stability.

No direct authoritative XYZ is promoted from this static evidence.

## Side effects

```text
process-memory writes: 0
movement stimuli:      0
gameplay actions:      0
runtime attach:        0
```

The live acceptance gate remains dependent on a bounded exact in-game process from the separately owned RUNTIME lane / Draft PR #303.
