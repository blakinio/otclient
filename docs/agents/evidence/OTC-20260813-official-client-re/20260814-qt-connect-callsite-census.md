# Exact-version Qt connect callsite census

## Scope

This record preserves a bounded static census for the official native Linux Tibia client `15.32.df7b29`, SHA256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

The scanner enumerated direct x86-64 `E8 rel32` calls from executable `PT_LOAD` segments to three PLT targets recovered by the preceding Qt symbol census. It did not reconstruct sender/receiver objects, signal/slot identities, indirect calls, or semantic ownership.

## Evidence

```yaml
symbol_census:
  run: 31793668176
  head: 6cf46ed2cb1c277c5bde247e7d4ba5cc668ff35b
  result: PASS
callsite_census:
  run: 31799755489
  job: 94764705414
  head: 3d0a54a9edd658555df44929494c902abfd846ec
  runner: synology-otclient-01
  result: PASS
  counts:
    QObject_connectImpl: 2078
    QObject_connect_legacy_string_api: 41
    QObject_disconnectImpl: 65
    total: 2184
```

The exact completion markers were `TOTAL_QT_CONNECT_CALLSITES=2184` and `TRACK_A_QT_CONNECT_CALLSITE_CENSUS_COMPLETE=true`.

## Classification

`PROVEN`: the exact binary contains the counted direct calls to the three exact PLT targets under the scanner's stated instruction boundary.

`UNKNOWN`: which calls are Tibia-owned semantic connections; sender and receiver types/instances; signal and slot identities; connection types; indirect or wrapper-mediated connections; relationships to protocol queues, storages, controllers, or generated messages.

## Next experiment

Run `31800072490` / job `94765746423` successfully produced all 41 bounded GDB neighborhoods after one failed system-`objdump` availability hypothesis (`31799979849`). The neighborhoods prove that candidate legacy calls commonly load signal and slot string pointers into `rdx` and `r8` immediately before the call, but the raw neighborhood log does not itself validate every pointed-to string.

Next, structurally resolve the nearest printable C-string targets loaded into `rdx` and `r8` for every legacy callsite. Classify every callsite as a recovered candidate edge or explicit `UNCLASSIFIED`, then decide whether any edge belongs to a high-value Tibia protocol/storage/controller path before attempting the larger `connectImpl` population.

## Legacy string-edge result

Run `31800240820` completed on exact head `5b72f60a17dc67e2e02901a69362f43da0f4c8c4` and classified 40 of 41 legacy callsites by resolving the nearest printable C strings loaded into the legacy API's signal (`rdx`) and slot (`r8`) arguments. Ordinal 2 / call `0x84e2a0` remains explicitly `UNCLASSIFIED` because only a `positionInSidebarChanged()` slot candidate was recovered.

All ordinals are accounted for:

| Ordinals | Family | Recovered semantic edge group |
|---|---|---|
| 0-1 | chat input | bind/release chat focus |
| 2 | unclassified | incomplete sidebar-position candidate |
| 3-7 | world map UI | click, drag start/drop, target selection, unused width |
| 8 | generic dialog | any-button close request |
| 9-17 | slot/container UI | click/hover/paging/drag/target/search |
| 18-19 | chat UI | primary/secondary chat scroll-to-end |
| 20-23 | context/player UI | context menu, tooltip, store XP boost, stat details |
| 24-25 | mouse filter | enter/exit |
| 26-28 | creature UI | hovered/clicked/target-selected creature |
| 29 | window state | apply window bounds |
| 30-36 | slot/action UI | repeated slot edges plus `stopClicked -> onStopButtonClicked` |
| 37-40 | sidebar/layout | maximize/content-size/sidebar-position edges |

These are static UI/controller signal candidates. They do not prove protocol messages, receiver implementation addresses, ABI layouts, server acceptance, or action gates above `A0`.

The absence of the six high-value `send*` GameAction signals from the legacy string-edge set supports a bounded next hypothesis: their receiver connections use `QObject::connectImpl` or a wrapper/indirect path. Cross-correlate the 2,078 `connectImpl` callsites with nearby exact references to the six version-fenced GameAction static metaobjects before broad disassembly.

## GameAction `connectImpl` correlation

Run `31800490781` / job `94767068361` completed on head `2bebb9615e9cb93fd26014df1f8b36b9ca4bc1ce`. A bounded 384-byte backward window found 86 static-metaobject-reference/callsite pairs across the 2,078 direct `connectImpl` calls. Because one reference can precede several consecutive connections, the 86 pairs are candidates rather than 86 unique proven semantic edges.

The tighter `distance <= 64` subset contains 31 candidates:

```yaml
Chat: 2
Container: 2
Creatures: 2
Player: 22
PlayerTrade: 2
WorldMap: 1
```

This proves a high-information cluster suitable for bounded disassembly. It does not yet map the GameAction signal indices to receivers or distinguish the six target `send*` signals from other signals on the same metaobjects.
