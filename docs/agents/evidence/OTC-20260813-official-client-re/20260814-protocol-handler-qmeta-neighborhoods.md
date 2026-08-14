# Protocol handler QMeta/string-neighborhood evidence — 2026-08-14

## Scope

Track A / official native Linux Tibia client only.

Exact client SHA256:

```text
e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Workflow evidence:

```text
.github/workflows/tibia-official-client-re-qmeta-handler-neighborhood.yml
commit: 797c8079b6280644cbbd9ce0641846c6fa0fb21e
run: 31787757301
job: 94727417973
result: SUCCESS
runner: synology-otclient-01
```

This experiment scans exact-binary class-name occurrences and compact nearby `handle*Message` string pools. A tight class-local cluster is useful static ownership evidence, but **string proximity alone is not yet a concrete function address**. Actual handler offsets require static-metacall/jump-table or xref/disassembly confirmation before promotion to runtime probes.

## High-confidence compact clusters

### TChatProtocolMessageHandler

A class occurrence at file/VA `0x1cd83a5` is followed immediately by a compact handler-method sequence:

```text
0x1cd844d handleTalkMessage
0x1cd849c handleMessageMessage
0x1cd84f4 handleOpenChannelMessage
0x1cd8558 handleOpenOwnChannelMessage
0x1cd85af handleCloseChannelMessage
0x1cd8616 handleChannelsMessage
0x1cd8671 handlePrivateChannelMessage
0x1cd86d7 handleChannelEventMessage
0x1cd8737 handleNpcTalkPartersMessage
```

**FACT:** the exact binary contains a coherent class-local chat/channel method-name table, strongly supporting direct structural observation of player/NPC speech and channel lifecycle without OCR.

### TContainerProtocolMessageHandler

A class occurrence at `0x1caef6a` is followed by:

```text
0x1caf27f handleSetInventoryMessage
0x1caf2e6 handleDeleteInventoryMessage
0x1caf356 handlePlayerInventoryMessage
0x1caf3c6 handleContainerMessage
0x1caf424 handleCloseContainerMessage
0x1caf47b handleChangeInContainerMessage
0x1caf4f1 handleDeleteInContainerMessage
0x1caf567 handleCreateInContainerMessage
0x1caf5dd handleObjectInfoMessage
0x1caf63e handleStashMessage
0x1caf690 handleShowMessageDialogMessage
0x1caf706 handleSpecialContainersAvailableMessage
0x1caf797 handleDepotSearchResultMessage
0x1caf80d handleDepotSearchDetailListMessage
0x1caf88f handleCloseDepotSearchMessage
```

**FACT:** inventory, container mutation, stash and depot-search handling form a coherent compact binary surface.

### TEffectProtocolMessageHandler

A class occurrence at `0x1d73fb4` is immediately followed by:

```text
0x1d73fd2 handleRemoveGraphicalEffectMessage
0x1d7404f handleGraphicalEffectsMessage
```

**FACT:** graphical-effect creation/update stream and effect removal have dedicated named handling surfaces.

### TMarketProtocolMessageHandler

A class occurrence at `0x1cb445f` is near the compact market group:

```text
0x1cb46a5 handleMarketEnterMessage
0x1cb4709 handleMarketDetailMessage
0x1cb4770 handleMarketLeaveMessage
0x1cb47c1 handleMarketBrowseMessage
```

The nearby generic `handleMessageMessage` is not assigned to Market without further dispatch proof.

### TNPCTradeProtocolMessageHandler

A class occurrence at `0x1cb5912` is near the compact NPC-trade group:

```text
0x1cb5b29 handleNPCOfferMessage
0x1cb5b84 handlePlayerGoodsMessage
0x1cb5be1 handleResourceBalanceMessage
0x1cb5c51 handleCloseNPCTradeMessage
```

`handleDeadMessage` appears nearby in the global string region but is **not** attributed to NPC trade by proximity alone.

### TPlayerTradeProtocolMessageHandler

A class occurrence at `0x1cb5f46` is immediately followed by the player-trade group:

```text
0x1cb6111 handleOwnOfferMessage
0x1cb616c handleCounterOfferMessage
0x1cb61d3 handleCloseTradeMessage
```

### TQuestLogProtocolMessageHandler

A class occurrence at `0x1cb6c49` is immediately followed by:

```text
0x1cb6d23 handleQuestLogMessage
0x1cb6d7e handleQuestLineMessage
0x1cb6ddc handleTrackedQuestFlagsMessage
```

### TGameEventProtocolMessageHandler

A class occurrence at `0x1cd7f91` is only `+107` bytes from:

```text
0x1cd7ffc handleGameEventMessage
```

This is a strong candidate for direct game-event observation, but concrete code entry still needs static-metacall mapping.

## Unresolved by this technique

### TCreatureProtocolMessageHandler

The class-name occurrences did **not** produce a clean creature-specific `handle*Message` cluster. Nearby matches belonged mostly to effects or unrelated global string pools.

**UNKNOWN:** concrete `TCreatureProtocolMessageHandler` method-name table and static-metacall offsets remain unresolved by the neighborhood heuristic.

### TPlayerProtocolMessageHandler

The class-name occurrences intersect large shared/global method pools. This is too ambiguous to assign player handlers by proximity.

**UNKNOWN:** concrete player handler ownership/offsets remain pending deterministic static-metacall mapping.

### TVipProtocolMessageHandler / TFriendsProtocolMessageHandler

Simple proximity is not sufficient because VIP/friend functionality uses Buddy/FriendSystem vocabulary and nearby shared protocol pools. Do not assign methods from this scan alone.

## Negative result from field-context experiment

A separate exact-binary experiment:

```text
.github/workflows/tibia-official-client-re-protocol-field-context.yml
commit: fa2dd86ce7bad32ef286d563b41fd24d258d3482
run: 31787592680
job: 94726896362
result: SUCCESS
```

showed descriptor/message-order neighborhoods for selected `GameserverMessage*` / `GameclientMessage*` targets, but did **not** expose reliable protobuf field numbers or C++ object layouts.

**FACT:** that technique is insufficient for field-layout claims and is not being promoted as evidence of field offsets.

## Next deterministic gates

1. Resolve class-specific Qt static-metacall functions and jump tables for Chat, Container, Effect, Market, NPC Trade, Player Trade, Quest and Game Event.
2. Map each dispatch index to a concrete executable offset, using the compact method-name order as a candidate ordering only after QMetaObject metadata confirms it.
3. Separately locate outbound serializer/builder xrefs for `MoveObject`, `Attack`, `Follow`, `TradeObject`, `Talk` and `GoPath`.
4. Do not disturb the already armed dynamic-world `raw-v2` observer while no controlled owner-side mutation is available.
