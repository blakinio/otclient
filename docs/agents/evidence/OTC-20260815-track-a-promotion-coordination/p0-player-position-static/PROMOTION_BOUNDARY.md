# Track A coordinator boundary — P0 player-position static slice

Source Draft: PR #302  
Reviewed source head: `6f838d1089968d216e506cd272e7b98680da9fc8`  
Code-bearing semantic/static head: `a3068a6a9460525cb1946186cf439caf7832e176`  
Static workflow: run `31892019505`, job `95029600292` = `SUCCESS` on `synology-otclient-01`  
Source artifact: `9248797952`, digest `sha256:04835ab0bac7ffc43e161e8b2118c90a3d2197f7011385a6758cd7706c93a584`  
Exact reviewed-head PR CI: run `31892202128` = `SUCCESS`  
Review threads at disposition: `0`

Coordinator disposition for this **bounded static slice**: `ACCEPT_WITH_EDITS`.

The overall PR #302 objective remains `RETURN_FOR_EVIDENCE / WAITING_ON_RUNTIME`: direct authoritative player XYZ is not yet proven.

## Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

## FACT — promoted bounded anchors

The successful exact-build static run deterministically fences the binary before build-specific analysis. The following are accepted as exact-file static anchors under that fence:

```text
primary playerPosition literal: 0x1cdde3f
secondary substring:             0x1d2a937 (inside playerPositionChanged context)
TWorldMapRenderProvider strings: 0x1cdb59c, 0x1cddd20
TWorldMapViewport strings:       0x1cabb7c, 0x1ce1b60
IPlayerDataProvider string:      0x1ce1ba0
TPlayerData strings:             0x1cabdbc, 0x1ce1bd0
TPlayerData primary vptr:        0x308ca70
offset-to-top:                   0
typeinfo:                        0x308b5b8
```

RELATIVE relocation-backed type-name references are accepted as structural facts:

```text
0x3089b78 -> 0x1cddd20  TWorldMapRenderProvider
0x308b598 -> 0x1ce1b60  TWorldMapViewport
0x308b5b0 -> 0x1ce1ba0  IPlayerDataProvider
0x308b5c0 -> 0x1ce1bd0  TPlayerData
```

The primary literal corrects the earlier transcription `0x1cddd3f`; that stale transcription is superseded by `0x1cdde3f`.

The Cyclopedia-map `playerPositionChanged` string neighborhood is accepted only as a distinct control context, not as a direct player-state field.

## EDIT — classification correction

The source report labels `0x8367c1` as a FACT instruction/xref. The coordinator narrows that claim.

The task's custom `find_rip_xrefs()` is deliberately a byte-wise, narrow x86-64 pattern decoder rather than a full instruction decoder. It reports overlapping starts `0x8367c1` and `0x8367c2` for the same target. The task-local GDB disassembly step did **not** execute because its runtime library path lacked `libpython3.12.so.1.0`.

Therefore the promoted classification is:

```yaml
playerPosition_literal_0x1cdde3f: FACT
bounded_byte_pattern_candidate_0x8367c1: INFERENCE
candidate_role: STRUCTURAL_XREF_LEAD_REQUIRES_REAL_DISASSEMBLY
0x8367c2: DECODER_OVERLAP_NOT_INDEPENDENT_XREF
instruction_boundary_at_0x8367c1: UNKNOWN
```

Likewise, co-location/string-neighborhood evidence does not by itself prove that `TWorldMapRenderProvider`, `TWorldMapViewport`, `IPlayerDataProvider`, `TPlayerData` and `playerPosition` form one direct runtime ownership/accessor graph. Their individual exact-file anchors and relocation relations are FACT; the semantic graph connecting them to the primary property remains an INFERENCE until disassembly/live object evidence closes it.

## UNKNOWN — unchanged

- direct standalone authoritative player XYZ;
- backing member/accessor offset and encoding;
- whether the primary property resolves direct player state or a render/status/cache copy;
- causal change semantics and negative controls;
- live repeated observations;
- fresh PID/relogin stability;
- bridge R4 exposure.

No P0 read gate is promoted beyond the previously established boundary from this static slice alone.

## Next discriminator

First fix only the task-local static disassembler runtime path and validate the true instruction boundary/control flow around the `0x8367c1` byte-pattern lead. Live semantic validation still requires the separately owned RUNTIME lane to expose a bounded exact-client in-game process window. Do not duplicate login/restart ownership and do not convert viewport-derived XYZ into a direct-field claim.
