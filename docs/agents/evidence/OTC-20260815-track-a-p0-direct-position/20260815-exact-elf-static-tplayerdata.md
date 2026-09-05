# Track A P0 exact-ELF `TPlayerData` static evidence

Task: `OTC-20260815-track-a-p0-direct-position`
Track: `official-client-re`
Draft PR: `#302`
Execution head: `eec9f6fcb065dd7762fa098ad78d1661b0060bd3`
Workflow run: `31883967070`
Job: `95010405800` (`static-elf-re`)
Runner: `synology-otclient-01`, runner id `21`
Result: `SUCCESS`
Artifact: `track-a-p0-static-elf-31883967070`, id `9246756211`, uploaded ZIP SHA-256 `2d3e423d05eef2e370e10c1dcc6afeab27ad2d3a04fe8ccfb2ba635575dabe74`

## Scope and safety

The run analyzed the already present official native Linux client ELF only. It did not require a live Tibia process, did not read `/proc/<pid>/mem`, did not write process memory and did not issue gameplay input. The workflow was changed so push-triggered P0 work executes only this static path; the live process probe now requires explicit `workflow_dispatch` with `mode=live` and retains the serialized `official-client-re-runtime` gate.

Side-effect usage remains: **0 memory writes, 0 movement stimuli, 0 gameplay actions**.

## Exact client fence — FACT

```text
version mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_P0_EXACT_CLIENT_FENCE=true
```

The ELF is ET_DYN (`e_type=3`) with entry `0x6afb50`.

## `TPlayerData` primary vtable — FACT

The accepted exact-build primary-vptr offset `0x308ca70` resolves inside `.data.rel.ro`.

```text
vptr:            0x308ca70
offset-to-top:   0
typeinfo:        0x308b5b8
typeinfo reloc:  R_X86_64_RELATIVE / .rela.dyn
```

Resolved executable slots observed in the first 32 qwords include:

```text
0  0xd1cbd0
1  0xd2ac70
2  0xd2ef30
3  0x843e20
4  0x843f60
12 0xeda3c0
13 0xee0010
14 0xeda3e0
15 0xee0100
16 0xeda400
17 0xedfd00
18 0xeda420
19 0xedfd40
20 0xeda440
21 0xedfd80
22 0xeda460
23 0xee0140
24 0xeda480
25 0xee0180
26 0xeda4a0
27 0xee01f0
28 0x9e5830
29 0xee0230
30 0xeda4d0
31 0xee02b0
```

Slots 5-11 contain dynamic symbol relocations that the deliberately bounded RELATIVE-only resolver did not attempt to resolve. They are not classified semantically here.

## Type and meta-object context — FACT

Two exact `tibia::game::TPlayerData` strings were found at virtual/file offsets:

```text
0x1ca2c30
0x1ca2d78
```

Nearby strings include `playerDataChanged`, `playerLevelUp`, `vocationSpecificPlayerDataChanged` and `vocationChanged`. There was no direct `position`/`playerPosition` string in this immediate `TPlayerData` meta-string neighborhood. Therefore this run does **not** establish a `TPlayerData` `position` Q_PROPERTY or equivalent direct property.

## Structural xrefs — FACT

The bounded RIP-relative scanner found structural references to the primary vptr/type string at these relevant instruction addresses:

```text
0x843e20 -> 0x308ca70
0x843f60 -> 0x308ca70
0x8440b0 -> 0x308ca70
0x8441f2 -> 0x308ca70
0xd2ac7d -> 0x1ca2d78
0xefd13c -> 0x308ca70
```

The scanner also reported overlapping `+1` byte detections for several patterns; those are scanner artifacts until instruction boundaries are independently decoded. `objdump` was unavailable on the runner, so this run intentionally does not assign method names or member semantics to these addresses.

## `playerPosition` lead — FACT and INFERENCE

A global semantic-string inventory from the exact binary found the literal:

```text
playerPosition @ 0x1cddd3f
```

The same broad static region also contains RTTI/type strings for:

```text
tibia::worldmap::TWorldMapRenderProvider
N5tibia8worldmap17TWorldMapViewportE
N5tibia4game19IPlayerDataProviderE
N5tibia4game11TPlayerDataE
```

Additional coordinate-related exact-binary strings include `tibia::worldmap::TWorldMapCoordinate`, `positionWasUpdated`, `N6shared11TCoordinateE`, `N5tibia8worldmap19TWorldMapCoordinateE`, `GameserverMessagePlayerDataCurrent` and `receivedPlayerDataCurrentMessage`.

**INFERENCE:** `playerPosition` is a materially stronger static lead than arbitrary XYZ-shaped bytes and appears associated with the worldmap/player-data-provider graph. It may identify an accessor/property used by rendering/provider code.

**UNKNOWN:** the owning class/function of `playerPosition`, the backing member/access path, whether it is direct authoritative player state or a viewport/render/cache copy, and its exact relation to `TPlayerData`. No static string correlation is promoted as authoritative XYZ.

## Runner-selector observation relevant to RUNTIME — FACT

At the same time:

- RUNTIME run `31883846172` / job `95010096196` requested labels `[self-hosted, otclient, synology]` and remained queued with `runner_id=0`;
- this P0 static job requested `[otclient, synology]` and was assigned to runner id `21`, `synology-otclient-01`, where it completed successfully.

This proves the runner was reachable during the RUNTIME queue interval. The extra `self-hosted` label is therefore a concrete selector mismatch candidate for RUNTIME, not evidence that the runner itself was offline.

## Classification

### FACT

- exact ELF fence passed;
- `TPlayerData` vtable/typeinfo provenance is relocation-backed and reproducible;
- bounded structural xrefs and `playerPosition` provider/worldmap lead were recovered without gameplay/runtime side effects;
- no live process was required for this static run.

### INFERENCE

The most useful next static/runtime bridge is no longer a blind object-byte scan: prioritize the `IPlayerDataProvider` / `playerPosition` access path and independently decoded `TPlayerData` xrefs before live causal validation.

### UNKNOWN / INCONCLUSIVE

Direct standalone authoritative player XYZ remains **UNKNOWN / INCONCLUSIVE**. A live exact in-game process is still required to demonstrate value identity, change semantics and discrimination from camera/map-origin/viewport copies.

## Next action

Release the P0 lease and repair/resume the separately owned RUNTIME lane. Once RUNTIME can create a bounded live exact-client observation window, run the live P0 typed-owner/provider probe first without movement. Only if repeated passive observations cannot distinguish the candidate may the previously authorized single adjacent step plus inverse be considered after rechecking RUNTIME ownership.
