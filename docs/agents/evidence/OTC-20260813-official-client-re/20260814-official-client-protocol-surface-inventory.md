# Official Linux client protocol surface inventory — 2026-08-14

## Scope and evidence boundary

Track: `official-client-re` / `OTCLIENT-TIBIA-RE`.

Subject: official native Linux Tibia client only.

Exact binary SHA256:

```text
e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Evidence source:

```text
workflow: .github/workflows/tibia-official-client-re-protocol-surface-inventory.yml
run: 31787489302
job: 94726575137
head: c63dec6c1329bfb1494de17715956a6815786d66
runner: synology-otclient-01
result: PASS
```

This is a **static exact-version binary inventory**. Presence of a class/message string proves that the exact binary contains that named protocol surface. It does **not** by itself prove wire opcode, runtime frequency, field layout, or that a specific UI action successfully emits the message. Those remain separate runtime/static-disassembly gates.

## Inventory totals

The exact binary contains the following unique ASCII protocol identifiers recovered by the workflow:

- `47` `*ProtocolMessageHandler` classes;
- `146` `handle*Message` method names;
- `189` inbound `GameserverMessage*` names;
- `160` outbound `GameclientMessage*` names.

## Handler classes directly recovered

Relevant handler classes include:

- `TWorldmapProtocolMessageHandler`
- `TCreatureProtocolMessageHandler`
- `TEffectProtocolMessageHandler`
- `TMinimapProtocolMessageHandler`
- `TChatProtocolMessageHandler`
- `TContainerProtocolMessageHandler`
- `TPlayerProtocolMessageHandler`
- `TNPCTradeProtocolMessageHandler`
- `TPlayerTradeProtocolMessageHandler`
- `TMarketProtocolMessageHandler`
- `TVipProtocolMessageHandler`
- `TFriendsProtocolMessageHandler`
- `TQuestLogProtocolMessageHandler`
- `TGameEventProtocolMessageHandler`
- `TPreyProtocolMessageHandler`
- `TImbuingProtocolMessageHandler`
- `TCyclopediaProtocolMessageHandler`
- `TBestiaryTrackerProtocolMessageHandler`
- `TBossBestiaryProtocolMessageHandler`
- `TDailyRewardProtocolMessageHandler`
- `TManagedContainersProtocolMessageHandler`
- `TExivaOptionsProtocolMessageHandler`
- `TTeamFinderProtocolMessageHandler`
- `TCharacterTradeProtocolMessageHandler`
- `TNetworkQualityProtocolMessageHandler`
- `TSoundProtocolMessageHandler`

The workflow recovered all 47 class names; this file highlights the surfaces most relevant to current reconstruction/capability work.

## World/map state

### FACT — inbound map snapshot and dynamic mutation are separate named surfaces

Recovered inbound names include:

- `GameserverMessageFullMap`
- `GameserverMessageLeftColumn`
- `GameserverMessageRightColumn`
- `GameserverMessageTopRow`
- `GameserverMessageBottomRow`
- `GameserverMessageTopFloor`
- `GameserverMessageBottomFloor`
- `GameserverMessageFieldData`
- `GameserverMessageCreateOnMap`
- `GameserverMessageChangeOnMap`
- `GameserverMessageDeleteOnMap`
- `GameserverMessageMoveCreature`
- `GameserverMessageAmbientLight`
- `GameserverMessageTibiaTime`
- `GameserverMessageWorldEntered`

Recovered `TWorldmapProtocolMessageHandler` method names include:

- `handleFullMapMessage`
- `handleLeftColumnMessage`
- `handleRightColumnMessage`
- `handleTopRowMessage`
- `handleBottomRowMessage`
- `handleTopFloorMessage`
- `handleBottomFloorMessage`
- `handleFieldDataMessage`
- `handleCreateOnMapMessage`
- `handleChangeOnMapMessage`
- `handleDeleteOnMapMessage`
- `handleAmbientLightMessage`
- `handleTibiaTimeMessage`

This independently confirms the current research model: full/strip/floor map delivery and later dynamic create/change/delete mutations are distinct official-client protocol paths.

## Creature state

### FACT — exact binary contains explicit creature-state messages

Recovered inbound names include:

- `GameserverMessageCreatureData`
- `GameserverMessageCreatureUpdate`
- `GameserverMessageCreatureHealth`
- `GameserverMessageCreatureLight`
- `GameserverMessageCreatureMarks`
- `GameserverMessageCreatureParty`
- `GameserverMessageCreatureSkull`
- `GameserverMessageCreatureSpeed`
- `GameserverMessageCreatureOutfit`
- `GameserverMessageCreatureUnpass`
- `GameserverMessageCreatureType`
- `GameserverMessageMoveCreature`
- `GameserverMessageConfigureCreaturePodium`

This is directly useful for reconstructing visible players/NPCs/monsters and their dynamic state without OCR. Exact payload layouts and creature identity keys remain to be decoded.

## Player state

Recovered inbound names include:

- `GameserverMessagePlayerDataBasic`
- `GameserverMessagePlayerDataCurrent`
- `GameserverMessageVocationSpecificPlayerData`
- `GameserverMessagePlayerSkills`
- `GameserverMessagePlayerState`
- `GameserverMessagePlayerInventory`
- `GameserverMessagePlayerGoods`
- `GameserverMessageBlessings`
- `GameserverMessagePremiumTrigger`
- `GameserverMessagePvpSituations`
- `GameserverMessageXpChanged`
- `GameserverMessageDead`

### RESEARCH CONSEQUENCE

The official client has explicit structural surfaces for current player data and skills in addition to map/creature data. These should be preferred over OCR/pixel inference when proving player identity, position-correlated transitions, vitals, skills and state flags.

## Inventory, containers, stash and loot

Recovered inbound names include:

- `GameserverMessageSetInventory`
- `GameserverMessageDeleteInventory`
- `GameserverMessagePlayerInventory`
- `GameserverMessageContainer`
- `GameserverMessageCloseContainer`
- `GameserverMessageCreateInContainer`
- `GameserverMessageChangeInContainer`
- `GameserverMessageDeleteInContainer`
- `GameserverMessageStash`
- `GameserverMessageSpecialContainersAvailable`
- `GameserverMessageDepotSearchResult`
- `GameserverMessageDepotSearchDetailList`
- `GameserverMessageCloseDepotSearch`
- `GameserverMessageUpdateManagedContainers`
- `GameserverMessageItemLooted`
- `GameserverMessageItemWasted`

Recovered outbound names include:

- `GameclientMessageCloseContainer`
- `GameclientMessageUpContainer`
- `GameclientMessageSeekInContainer`
- `GameclientMessageContainerAction`
- `GameclientMessageOpenParentContainer`
- `GameclientMessageOpenDepotSearch`
- `GameclientMessageCloseDepotSearch`
- `GameclientMessageDepotSearchType`
- `GameclientMessageDepotSearchRetrieve`
- `GameclientMessageStashAction`
- `GameclientMessageManagedContainer`
- `GameclientMessageQuickLoot`
- `GameclientMessageQuickLootBlackWhitelist`
- `GameclientMessageEquipObject`

This establishes a broad non-OCR inventory/container observation and action surface, but does not yet establish exact builder entry points or wire fields.

## Object interaction and movement

Recovered outbound names include:

- `GameclientMessageMoveObject`
- `GameclientMessageUseObject`
- `GameclientMessageUseTwoObjects`
- `GameclientMessageUseOnCreature`
- `GameclientMessageLook`
- `GameclientMessageLookAtCreature`
- `GameclientMessageInspectObject`
- `GameclientMessageGetObjectInfo`
- `GameclientMessageBrowseField`
- `GameclientMessageTurnObject`
- `GameclientMessageToggleWrapState`
- `GameclientMessageEquipObject`

Movement/action builders named in the binary include:

- `GameclientMessageGoNorth`
- `GameclientMessageGoEast`
- `GameclientMessageGoSouth`
- `GameclientMessageGoWest`
- `GameclientMessageGoNorthEast`
- `GameclientMessageGoSouthEast`
- `GameclientMessageGoSouthWest`
- `GameclientMessageGoNorthWest`
- `GameclientMessageGoPath`
- `GameclientMessageStop`
- `GameclientMessageCancel`
- `GameclientMessageRotateNorth`
- `GameclientMessageRotateEast`
- `GameclientMessageRotateSouth`
- `GameclientMessageRotateWest`

This substantially strengthens the static basis for future native-action experiments. Presence is proven; safe runtime invocation and payload contracts still require separate validation.

## Combat, follow and party

Recovered outbound names include:

- `GameclientMessageAttack`
- `GameclientMessageFollow`
- `GameclientMessageInviteToParty`
- `GameclientMessageJoinParty`
- `GameclientMessageRevokeInvitation`
- `GameclientMessagePassLeadership`
- `GameclientMessageLeaveParty`
- `GameclientMessageDisbandParty`
- `GameclientMessageShareExperience`
- `GameclientMessagePartyHuntAnalyser`

Inbound party-related names include:

- `GameserverMessageCreatureParty`
- `GameserverMessagePartyHuntAnalyser`

### FACT

Attack, follow and the principal party actions explicitly exist as named outbound protocol messages in this exact official Linux client binary.

## Chat, channels and world communication

Recovered inbound names include:

- `GameserverMessageTalk`
- `GameserverMessageChannels`
- `GameserverMessageOpenChannel`
- `GameserverMessageOpenOwnChannel`
- `GameserverMessageCloseChannel`
- `GameserverMessagePrivateChannel`
- `GameserverMessageChannelEvent`
- `GameserverMessageNpcTalkParters`
- `GameserverMessageMessage`

`TChatProtocolMessageHandler` exposes named methods including:

- `handleTalkMessage`
- `handleOpenChannelMessage`
- `handleOpenOwnChannelMessage`
- `handleCloseChannelMessage`
- `handleChannelsMessage`
- `handlePrivateChannelMessage`
- `handleChannelEventMessage`
- `handleNpcTalkPartersMessage`

Recovered outbound names include:

- `GameclientMessageTalk`
- `GameclientMessageGetChannels`
- `GameclientMessageJoinChannel`
- `GameclientMessageOpenChannel`
- `GameclientMessagePrivateChannel`
- `GameclientMessageCloseNPCChannel`
- `GameclientMessageLeaveChannel`
- `GameclientMessageInviteToChannel`
- `GameclientMessageExcludeFromChannel`
- `GameclientMessageGuildMessage`

This directly supports the planned capture of messages from other players/NPCs and channel/event changes without OCR.

## NPC trade, player trade and market

Recovered inbound names include:

- `GameserverMessageNPCOffer`
- `GameserverMessagePlayerGoods`
- `GameserverMessageCloseNPCTrade`
- `GameserverMessageOwnOffer`
- `GameserverMessageCounterOffer`
- `GameserverMessageCloseTrade`
- `GameserverMessageMarketEnter`
- `GameserverMessageMarketDetail`
- `GameserverMessageMarketBrowse`
- `GameserverMessageMarketLeave`
- `GameserverMessageMarketStatistics`
- `GameserverMessageCharacterTradeConfiguration`

Recovered outbound names include:

- `GameclientMessageLookNPCTrade`
- `GameclientMessageBuyObject`
- `GameclientMessageSellObject`
- `GameclientMessageCloseNPCTrade`
- `GameclientMessageLookTrade`
- `GameclientMessageTradeObject`
- `GameclientMessageAcceptTrade`
- `GameclientMessageRejectTrade`
- `GameclientMessageMarketBrowse`
- `GameclientMessageMarketCreate`
- `GameclientMessageMarketAccept`
- `GameclientMessageMarketCancel`
- `GameclientMessageMarketLeave`
- `GameclientMessageMarketStatistics`
- `GameclientMessageCharacterTradeConfigurationAction`

## VIP / buddy / friends

The exact binary contains `TVipProtocolMessageHandler` and `TFriendsProtocolMessageHandler`. The current protocol names use `Buddy`/`FriendSystem` terminology rather than consistently using `Vip` in message names.

Recovered inbound examples:

- `GameserverMessageBuddyGroupData`
- `GameserverMessageBuddyStatusChange`
- `GameserverMessageBuddyData`
- `GameserverMessageFriendSystemData`

Recovered outbound examples:

- `GameclientMessageAddBuddy`
- `GameclientMessageRemoveBuddy`
- `GameclientMessageEditBuddy`
- `GameclientMessageBuddyGroup`
- `GameclientMessageFriendSystemAction`

Therefore a zero literal `Vip` keyword count must not be interpreted as absence of VIP functionality.

## Effects, environment and sound

Recovered inbound names include:

- `GameserverMessageGraphicalEffects`
- `GameserverMessageRemoveGraphicalEffect`
- `GameserverMessageAmbientLight`
- `GameserverMessageTibiaTime`
- `GameserverMessageSoundTrigger`

The binary contains dedicated `TEffectProtocolMessageHandler` and `TSoundProtocolMessageHandler` classes.

This supports a separate dynamic-world stream for graphical effects, ambient state and sound notifications. No `Missile`-named message was recovered by the literal-string scan; projectile encoding may therefore be represented under another message/type and remains `UNKNOWN`.

## Quests, game events and progression

Recovered inbound surfaces include:

- `GameserverMessageQuestLog`
- `GameserverMessageQuestLine`
- `GameserverMessageTrackQuestFlags`
- `GameserverMessageGameEvent`
- `GameserverMessageDailyRewardBasic`
- `GameserverMessageDailyRewardHistory`
- `GameserverMessageDailyRewardCollectionState`
- `GameserverMessagePreyData`
- `GameserverMessagePreyTimeLeft`
- `GameserverMessageBestiaryTracker`
- multiple Monster Cyclopedia / Bosstiary / Taskboard / SkillWheel messages

Recovered outbound surfaces include corresponding quest, prey, daily reward, bestiary, cyclopedia, taskboard and skill-wheel requests/actions.

This is directly relevant to the research requirement to observe world/game events and state transitions beyond the visible map.

## Important corrections and interpretation

1. The previous dynamic-world hypothesis that full-map state and later object mutations might use separate paths is now directly supported by official binary names.
2. `MoveCreature` is explicitly present as an inbound message even though the generic `handle*Message` ASCII scan did not recover a literal `handleMoveCreatureMessage`; handler dispatch ownership therefore requires separate QMetaObject/disassembly mapping rather than assuming missing functionality.
3. Literal keyword searches are not semantic completeness tests. Example: VIP functionality uses `Buddy`/`FriendSystem` message names.
4. This inventory proves a large protocol/action surface but **does not** claim bot-safe or anti-cheat-safe invocation, packet opcode values, or direct packet injection capability.

## Next autonomous static gates

No owner interaction is required for the following next gates:

1. map `TCreatureProtocolMessageHandler`, `TChatProtocolMessageHandler`, `TContainerProtocolMessageHandler`, `TPlayerProtocolMessageHandler`, `TEffectProtocolMessageHandler` and trade handlers from QMetaObject dispatch indices to concrete function offsets;
2. recover exact-version C++ protobuf/wrapper field layouts for selected high-value inbound messages;
3. locate outbound builder/serialization entry points for movement, `MoveObject`, `Attack`, `Follow`, party and trade actions;
4. promote only validated layouts/offsets into the version-fenced Track A capability catalogue;
5. keep the already armed `raw-v2` Create/Change/Delete observer untouched until a controlled real mutation is available.
