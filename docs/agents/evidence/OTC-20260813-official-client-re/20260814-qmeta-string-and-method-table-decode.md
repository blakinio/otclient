# QMeta string and method table decode — 2026-08-14

## Scope

Track A / `official-client-re` only. Subject: exact official native Linux Tibia client SHA256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

Primary evidence:

```text
workflow: .github/workflows/tibia-official-client-re-qmeta-data-dump.yml
head: 16862d5a9d9978179e52eff0bfa256ff2e8af6bc
run: 31790262928
job: 94735347525
result: SUCCESS
runner: synology-otclient-01
```

## FACT — QMeta stringdata format is decoded

The relocation-backed record field at `+0x08` points to a table of 8-byte `(offset,length)` pairs. The first pair's offset is also the byte size of that pair table, so `first_offset / 8 = number_of_strings`. Each offset is relative to the stringdata base.

Examples directly recovered:

```text
Worldmap stringdata base 0x1cd8a54:
  pair 0: offset 0x160, len 48 -> tibia::worldmap::TWorldmapProtocolMessageHandler
  pair 5: offset 0x1db, len 20 -> handleFullMapMessage
  pair 29: offset 0x4c8, len 24 -> handleCreateOnMapMessage
  pair 32: offset 0x52c, len 24 -> handleChangeOnMapMessage
  pair 35: offset 0x590, len 24 -> handleDeleteOnMapMessage

Chat stringdata base 0x1cd8268:
  pair 0: offset 0x130, len 40 -> tibia::chat::TChatProtocolMessageHandler
  pair 8: offset 0x1e5, len 17 -> handleTalkMessage
  pair 11: offset 0x234, len 20 -> handleMessageMessage
  pair 14: offset 0x28c, len 24 -> handleOpenChannelMessage
  ...

Effect stringdata base 0x1d73f64:
  pair 0 -> tibia::effects::TEffectProtocolMessageHandler
  pair 1 -> handleRemoveGraphicalEffectMessage
  pair 5 -> handleGraphicalEffectsMessage
```

The earlier failure of the classic-layout heuristic was caused by searching backward from an interior class-name occurrence rather than using the relocation-backed stringdata base. The actual representation is the expected relative `(offset,length)` pair table once the correct base is known.

## FACT — QMeta metadata header is decoded

The relocation-backed `+0x10` field points to a uint32 metadata table. The successful Worldmap calibration matches the Qt meta-object header representation:

```text
word[0] = revision = 13
word[1] = class-name string index
word[4] = method_count
word[5] = method_table_offset
```

Observed exact method counts:

```text
GameEvent: 2
Chat:      13
Worldmap:  14
Effect:    2
Container: 35
```

Method descriptors begin at `method_table_offset` and use six uint32 words per method. The first word is the method-name string index. This is enough to deterministically recover method ordering from the exact binary before case-mapping the static metacall code.

## FACT — actual Container QMeta record is proven

The candidate record at base `0x3084fe0` is now directly associated with `TContainerProtocolMessageHandler`:

```text
record base:      0x3084fe0
stringdata:       0x1caec88
metadata:         0x1cae760
static_metacall:  0xd1e000
```

At stringdata base `0x1caec88`:

```text
pair 0: offset 0x2d0, len 50 -> tibia::container::TContainerProtocolMessageHandler
```

The same table contains the outbound and inbound Container protocol surface, including:

```text
sendCloseContainerMessage
sendUpContainerMessage
sendSeekInContainerMessage
sendGetObjectInfoMessage
sendContainerActionMessage
handleSetInventoryMessage
handleDeleteInventoryMessage
handlePlayerInventoryMessage
handleContainerMessage
handleCloseContainerMessage
handleChangeInContainerMessage
handleDeleteInContainerMessage
handleCreateInContainerMessage
handleObjectInfoMessage
handleStashMessage
handleShowMessageDialogMessage
handleSpecialContainersAvailableMessage
handleDepotSearchResultMessage
handleDepotSearchDetailListMessage
handleCloseDepotSearchMessage
```

The metadata table reports `method_count=35`. Therefore `+0xd1e000` is promoted as the exact-version Container static-metacall entry.

This supersedes the earlier unproven Container-region candidates `+0xdcb130` and `+0xcf2aa0`, which belong to other nearby QMeta records.

## FACT — exact static-metacall entries now version-fenced

```text
TGameEventProtocolMessageHandler:  +0xd20800
TChatProtocolMessageHandler:       +0xd05f20
TWorldmapProtocolMessageHandler:   +0xdf2a60
TEffectProtocolMessageHandler:     +0xd338d0
TContainerProtocolMessageHandler:  +0xd1e000
```

Worldmap is independently calibrated by its already-reconstructed dispatch table. The others are linked by the same relocation-backed QMeta record format plus directly decoded class-name stringdata.

## Additional structural discovery

The Container-region stringdata also exposes exact native game-action class/type surfaces without OCR or protocol guessing, including:

```text
TContainerGameActionHandler
TWorldMapGameActionHandler
TPlayerGameActionHandler
TChatGameActionHandler
TPlayerMovementGameActionHandler
TGameActionMoveObject
TGameActionSendChatMessageToNpc
TGameActionSendChatMessageWithRecipient
TGameActionSendChatMessageWithChannelID
TGameActionSendChatMessage
```

These are presence/association facts from the exact stringdata region; executable action-handler offsets still require separate QMeta/static/code mapping before runtime invocation claims.

## Next gate

Workflow `.github/workflows/tibia-official-client-re-qmeta-method-map.yml`, head `54c378a85f886b48a8843b1dee1ec006009e43a8`, run `31790364366`, decodes all six-word method descriptors for GameEvent/Chat/Worldmap/Effect/Container and disassembles their static-metacall functions. The next promotion gate is an exact mapping from QMeta method index/name to executable case/handler offsets.
