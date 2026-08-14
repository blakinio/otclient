# Track A capability / observation matrix — 2026-08-14

## Evidence boundary

Track: `official-client-re` / `OTCLIENT-TIBIA-RE`.

Subject: official native Linux Tibia client only.

Exact binary SHA256:

```text
e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Primary exact-binary sources:

- protocol inventory: run `31787489302`, job `94726575137`, head `c63dec6c1329bfb1494de17715956a6815786d66`;
- QMeta/string-neighborhood mapping: run `31787757301`, job `94727417973`, head `797c8079b6280644cbbd9ce0641846c6fa0fb21e`;
- symbol-surface check: run `31787886977`, job `94727824870`, head `923d297ecc49129130b530a9ea6c333de549598f`.

This matrix is deliberately conservative. `present` means the exact binary contains the named protocol surface. `clustered` means class-local QMeta/string evidence also supports ownership. Neither status alone is a wire opcode, callable function offset, field layout, or proof that a specific runtime action succeeded.

## Observation surfaces

| Domain | Exact binary surface | Static status | What can eventually be observed structurally | Remaining gate |
|---|---|---|---|---|
| World map | `FullMap`, row/column/floor strips, `FieldData`, `CreateOnMap`, `ChangeOnMap`, `DeleteOnMap` | present; Worldmap work already separately promoted | map snapshot and dynamic tile/object mutations | preserve existing version-fenced callbacks and add controlled mutation proof |
| Creature movement/state | `CreatureData`, `CreatureUpdate`, `CreatureHealth`, `CreatureLight`, `CreatureMarks`, `CreatureParty`, `CreatureSkull`, `CreatureSpeed`, `CreatureOutfit`, `CreatureUnpass`, `CreatureType`, `MoveCreature` | present; creature handler class present; method ownership unresolved | visible players/NPCs/monsters, movement, health, outfit, speed and relation state | deterministic handler/dispatch or descriptor-layout mapping |
| Player state | `PlayerDataBasic`, `PlayerDataCurrent`, `PlayerSkills`, `PlayerState`, `VocationSpecificPlayerData`, `XpChanged`, `Dead` | present; player handler class present; ownership unresolved | vitals, skills, state flags, XP/death and other player data | deterministic handler/field layout mapping |
| Inventory | `SetInventory`, `DeleteInventory`, `PlayerInventory` | present + clustered | equipment/inventory slot state and changes | concrete dispatch/field layout |
| Containers | `Container`, `CloseContainer`, `CreateInContainer`, `ChangeInContainer`, `DeleteInContainer` | present + clustered | open containers and every create/change/delete mutation | concrete dispatch/field layout |
| Stash/depot | `Stash`, depot search result/detail/close, special containers | present + clustered | stash/depot query results and state changes | concrete field layout |
| Chat/player speech | `Talk`, generic `Message` | present + `handleTalkMessage` clustered | speech from players/NPCs and server text without OCR | concrete dispatch and payload layout |
| Channels | channels/open/close/private/channel-event/NPC partners | present + clustered | channel lifecycle, invitations/events and NPC conversation channels | concrete dispatch and payload layout |
| Game events | `GameEvent` | present + tight `handleGameEventMessage` cluster | event/state notifications delivered by the server | concrete dispatch and event payload enum/layout |
| Effects | `GraphicalEffects`, `RemoveGraphicalEffect` | present + tightly clustered | graphical effect creation/update/removal | concrete dispatch and effect payload layout |
| Sound | `SoundTrigger` + `TSoundProtocolMessageHandler` | present | sound/event notifications independent of pixels | handler/field mapping |
| NPC trade | `NPCOffer`, `PlayerGoods`, `CloseNPCTrade` | present + clustered | vendor offers, player goods/resources and trade closure | concrete dispatch/field layout |
| Player trade | `OwnOffer`, `CounterOffer`, `CloseTrade` | present + clustered | both sides' offered objects and trade lifecycle | concrete dispatch/field layout |
| Market | `MarketEnter`, `MarketDetail`, `MarketBrowse`, `MarketLeave`, statistics | present + clustered | market browse/details/lifecycle/statistics | concrete dispatch/field layout |
| Party | `CreatureParty`, `PartyHuntAnalyser` | present | party relationship state and hunt analyser data | handler/field mapping |
| Quest | `QuestLog`, `QuestLine`, tracked quest flags | present + clustered | quest list, lines and tracked flags | concrete dispatch/field layout |
| VIP/friends | Buddy/FriendSystem messages + `TVipProtocolMessageHandler` / `TFriendsProtocolMessageHandler` | present; vocabulary mapped; ownership unresolved | buddy groups, buddy state changes and friend-system state | deterministic handler mapping |
| Progression systems | prey, bestiary, bosstiary, cyclopedia, skill wheel, taskboard, daily reward | present | structured progression/account/game-system state | select high-value layouts after core world/player gates |

## Action surfaces

| Domain | Exact outbound messages proven present | Current evidence | Remaining gate before native action claim |
|---|---|---|---|
| Step movement | `GoNorth/East/South/West`, diagonals, `GoPath`, `Stop`, `Cancel` | named outbound surfaces present | locate builder/serializer entry and prove one reversible movement transition |
| Rotation | `RotateNorth/East/South/West` | present | builder entry + controlled before/after proof |
| Object movement | `MoveObject` | present | builder/serializer entry + exact source/destination/count fields |
| Object use | `UseObject`, `UseTwoObjects`, `UseOnCreature` | present | builder entry + exact target/object fields |
| Inspection | `Look`, `LookAtCreature`, `InspectObject`, `GetObjectInfo`, `BrowseField` | present | builder entry + payload fields |
| Equipment | `EquipObject` | present | builder entry + slot/object contract |
| Combat | `Attack` | present | builder entry + creature identity/sequence contract; controlled harmless validation only |
| Follow | `Follow` | present | builder entry + creature identity/sequence contract |
| Party | invite/join/revoke/pass leadership/leave/disband/share XP/hunt analyser | present | builder entries + identity/boolean/sequence contracts |
| Chat | `Talk`, channel actions | present | builder entry + message/channel/receiver payload contract |
| NPC trade | look/buy/sell/close | present | builder entry + item/amount/flags payload contract |
| Player trade | `LookTrade`, `TradeObject`, `AcceptTrade`, `RejectTrade` | present | builder entry + object/position/player contract |
| Market | browse/create/accept/cancel/leave/statistics | present | builder entries + market request layouts |
| Container | close/up/seek/action/open parent | present | builder entries + container IDs/index layouts |
| Stash/depot/loot | stash, depot-search and quick-loot actions | present | builder entries + payload layouts |
| Buddy/friends | add/remove/edit/group/friend-system actions | present | builder entries + identity/group/status layouts |

## High-priority next offsets/layouts

The next deterministic static targets are intentionally ordered by research value rather than UI convenience:

1. `GameserverMessageMoveCreature` / creature identity and position transition path;
2. `GameserverMessagePlayerDataCurrent` and `PlayerState`;
3. `GameserverMessageTalk` and generic server `Message`;
4. `GameserverMessageContainer` plus create/change/delete-in-container;
5. `GameclientMessageGoPath` and directional movement builders;
6. `GameclientMessageMoveObject`;
7. `GameclientMessageAttack` and `Follow`;
8. `GameclientMessageTradeObject` and `Talk`;
9. `GameserverMessageGameEvent` and graphical effects.

## Explicit unknowns

- Concrete executable handler offsets outside already separately proven/promoted Worldmap work are still `UNKNOWN`.
- Protobuf/wrapper field numbers and in-memory object offsets for these selected messages are still `UNKNOWN` unless separately promoted by exact-version evidence.
- Wire opcodes are not established by this inventory.
- Message presence does not prove direct packet injection is supported, safe, or desirable.
- Literal absence of a keyword is not absence of functionality; VIP/Friends already demonstrates vocabulary indirection (`Buddy`/`FriendSystem`).

## Current static xref experiment

A new exact-binary metadata-xref experiment was started from head `55dc75c830e571490be30a5c83a922a528c5931f` as workflow run `31788735824`. It walks string VAs, absolute metadata pointers and executable RIP-relative references for selected inbound handler names and outbound `GameclientMessage*` targets. Its result must be recorded separately after the run becomes terminal; this file does not pre-claim its outcome.
