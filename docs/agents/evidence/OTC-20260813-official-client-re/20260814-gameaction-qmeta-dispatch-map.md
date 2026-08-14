# Track A — verified outbound GameAction QMeta dispatch map

Date: 2026-08-14
Track: Track A / `official-client-re`
Repository: `blakinio/otclient`
Official Linux client SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

## Scope

Static-only reverse engineering of high-value outbound action dispatch in the exact pinned official Linux client. No client process was started by these mapping workflows and no game action or packet was emitted.

## Independent evidence chain

1. QMeta method census: workflow `.github/workflows/tibia-official-client-re-qmeta-gameaction-census.yml`, run `31790921915`, job `94737395183`, SUCCESS.
   - Recovers relocation-backed QMeta records, exact method counts/order and executable `static_metacall` addresses.
2. Static-metacall disassembly: workflow `.github/workflows/tibia-official-client-re-gameaction-dispatch-map.yml`, run `31790967810`, job `94737543252`, SUCCESS.
   - Establishes actual rel32 jump-table bases for Creatures/Chat/Container and direct-branch layouts for PlayerTrade/WorldMap.
3. Fail-closed case mapper: workflow `.github/workflows/tibia-official-client-re-gameaction-jumptable-map.yml`, run `31793073416`, job `94744105956`, SUCCESS on commit `453dd52315ab75e928220a5d0aaa9cb72f427237`.
   - Validates every case entry against the ELF executable LOAD segment and a bounded distance from its independently recovered `static_metacall`.

## Verified high-value mappings

| Class | QMeta method index | Method | Dispatch form | `static_metacall` | Table/direct entry evidence | Executable case entry |
|---|---:|---|---|---:|---|---:|
| `tibia::creatures::TCreaturesGameActionHandler` | 1 | `sendAttack` | rel32 table | `0xd16340` | table `0x1d712dc` | `0xd166f0` |
| `tibia::creatures::TCreaturesGameActionHandler` | 2 | `sendFollow` | rel32 table | `0xd16340` | table `0x1d712dc` | `0xd164e0` |
| `tibia::chat::TChatGameActionHandler` | 9 | `sendTalkMessage` | rel32 table | `0xcff5b0` | table `0x1d6dcbc` | `0xcffb90` |
| `tibia::container::TContainerGameActionHandler` | 1 | `sendMoveObject` | rel32 table | `0xd1dac0` | table `0x1d7145c` | `0xd1df30` |
| `tibia::trade::TPlayerTradeGameActionHandler` | 1 | `sendTradeObject` | direct branches | `0xdecff0` | index 1 branch | `0xded060` |
| `tibia::worldmap::TWorldMapGameActionHandler` | 0 | `sendMoveObject` | direct branches | `0xdeda80` | index 0 branch | `0xdedac0` |

`CRITICAL_MAPPING_COUNT=6` and `TRACK_A_GAMEACTION_DISPATCH_MAP_COMPLETE=true` were emitted by the successful fail-closed mapper.

## Corrected false lead

The first workflow version at commit `5bb97a116e854b488e38b75de12be00115ce4399` used manually entered table addresses and incorrect method lists/counts. Although that workflow itself could produce output, several decoded VAs were outside any plausible executable region. Those values are not evidence and must not be reused.

A subsequent validation run `31793021364`, job `94743944878`, intentionally failed when a raw byte-level tail scanner mistook an `0xe9` byte inside another instruction for an unconditional-jump opcode. The case entry `sendAttack=0xd166f0` was already structurally valid; the failure demonstrated that byte scanning is not instruction decoding. Commit `453dd52315ab75e928220a5d0aaa9cb72f427237` therefore removes tail inference from the mapper entirely.

## Method census details relevant to this checkpoint

- `TCreaturesGameActionHandler`: 13 methods; indices 1/2 are `sendAttack`/`sendFollow`.
- `TChatGameActionHandler`: 38 methods; index 9 is `sendTalkMessage`.
- `TContainerGameActionHandler`: 23 methods; index 1 is `sendMoveObject`.
- `TPlayerTradeGameActionHandler`: 3 methods; index 1 is `sendTradeObject`.
- `TWorldMapGameActionHandler`: 3 methods; index 0 is `sendMoveObject`.

## Boundary / next gate

These mappings prove exact QMeta method-to-executable-case relationships for this exact client binary. They do **not** yet prove wire opcodes, protobuf/wire field layouts, argument semantics, or the final serializer/network-send function.

Next gate: use a real disassembler on the six case entries plus the already recovered Player common tail `0xd1abc0`; trace typed argument loads, calls/jumps, serializer construction and convergence points without executing the client or emitting actions.
