# TIBIA-RE-ECONOMY-PANELS static census

Task: `OTC-20260819-track-a-economy-panels-static-census`

Scope: G24-G31, repository-only static research.

## Authority and safety boundary

This slice is SAFE_READ. It does not authorize or execute login, credential use, GUI input, gameplay, official-client process control, purchase/sale, market-offer mutation, Tibia Coin transfer, reward claim, character auction/trade commitment, world transfer, main-character change, or due-payment actions.

The candidate alias pack in Draft PR #543 is used only to resolve the intended G24-G31 research scope. Its unmerged permissions are not treated as authority. The trusted base authority is `main` at `a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb` plus the owner's `TIBIA-RE-ECONOMY-PANELS uruchom autonomicznie` instruction.

## Exact client fence

Both trusted static inputs below target the same official native Linux client:

- version: `15.32.df7b29`
- size: `51965216`
- SHA256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

Sources:

- `docs/agents/reports/OTCLIENT-20260818-track-a-s1-unfiltered-static-census.md`
- `docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-client-to-server.txt`
- `docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-server-to-client.txt`
- `docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-handler-code-xrefs.tsv`
- `docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md`

The S1 census establishes an exact generated-message denominator of `349`: `160` client-to-server plus `189` server-to-client. It also records `189` `received*Message` strings and `47` distinct `*ProtocolMessageHandler` class strings with direct executable code-to-string xrefs. Every handler xref is explicitly classified `DIRECT_CODE_TO_STRING_XREF` with `semantic_dispatcher_edge_proven=false`.

These are static facts. They do **not** prove live GUI behavior, message wire encoding, message-to-handler dispatch, confirmation behavior, or successful server-side transaction semantics.

## G24-G31 findings

| Group | Exact generated-message evidence | Exact-build UI/controller evidence | Static conclusion | Runtime status |
|---|---|---|---|---|
| G24 Market | C2S: `MarketAccept`, `MarketBrowse`, `MarketCancel`, `MarketCreate`, `MarketLeave`, `MarketStatistics`. S2C: `MarketBrowse`, `MarketDetail`, `MarketEnter`, `MarketLeave`, `MarketStatistics`. | Capability census records `TMarketController`, `TMarketProtocolMessageHandler`, `TMarketStorage::marketItemDetailsChanged`, item/category selection, offer cancel, history, own offers and item details. | Browse/statistics and transaction-producing offer families are statically present. | UNKNOWN. No live panel, message dispatch, create/cancel/accept confirmation boundary or server result was exercised. |
| G25 Store / Tibia Coin / transaction UI | C2S: `BuyStoreOffer`, `GetTransactionDetails`, `GetTransactionHistory`, `OpenTransactionHistory`, `RequestResourceBalance`, `RequestStoreCategories`, `RequestStoreOffers`, `StoreEvent`, `TransferCurrency`. S2C: `CreditBalance`, `RequestPurchaseData`, `ResourceBalance`, `SetStoreButtonDeeplink`, `StoreButtonIndicators`, `StoreCategories`, `StoreError`, `StoreOffers`, `StoreSuccess`, `TransactionDetails`, `TransactionHistory`, `UpdatingShopBalance`. | Capability census records Store protocol/controller presence, purchase confirmation/success dialogs, transaction-history opening and a coin-transaction details dialog. | Catalogue/balance/history and transaction-producing families coexist statically. | UNKNOWN. No purchase, transfer, confirmation or balance mutation was executed. |
| G26 Daily Reward | C2S: `CollectDailyReward`, `DailyRewardHistory`. S2C: `DailyRewardBasic`, `DailyRewardCollectionState`, `DailyRewardHistory`. | Capability census records a Daily Reward item-pick controller and fixed-item/pick-item collection request surfaces. | Reward state/history/collection families are statically present. | UNKNOWN. No reward claim was executed. |
| G27 Reward Wall / resting / returner | C2S: `OpenRewardWall`. S2C: `OpenRewardWall`, `CloseRewardWall`, `RestingAreaState`. | Capability census records Reward Wall resting-area bonuses, `TNewsStorage::returnerInformationChanged` and authentication returner-reward state. | Reward Wall open/close and resting-state transport names plus returner-state UI/storage residue are statically present. | UNKNOWN. No reward claim or state-changing action was executed. |
| G28 Character/account-management related UI | C2S: `BlessingsDialog`, `OpenCyclopediaCharacterInfo`. S2C: `Blessings`, `BlessingsDialog`, `CyclopediaCharacterInfo`, `PremiumTrigger`. | Capability census records `TCharacterInfoDialogController` routes to XP boost, Blessings, Item Info, outfit, Skill Wheel and Weapon Proficiency; blessing and premium/store-related controllers are present. | Character-info/blessings/premium-related surfaces are statically present in the exact build. | UNKNOWN. No account/premium mutation or purchase was exercised. |
| G29 Character auction/trade UI | C2S: `CharacterTradeConfigurationAction`. S2C: `CharacterTradeConfiguration`. | Capability census records `TCharacterAuctionConfiguration`, `TCharacterTradeDialogController` and related account/economy UI. | Character-trade configuration transport and auction/trade UI surfaces are statically present. | UNKNOWN. No auction/trade commitment was executed. |
| G30 World transfer / main-character change | No dedicated generated-message name was identified in the exact 160/189 registry by this bounded slice. | Capability census records a due-payment dialog, world-transfer controller and main-character-change controller in the same exact binary. | Exact-build UI/controller presence is established, but a dedicated generated transport-name mapping remains UNKNOWN. | UNKNOWN. No transfer or main-character-change action was executed. |
| G31 Misc modal/panel flows | C2S: `AnswerModalDialog`, `ClientCheck`. S2C: `ClientCheck`, `ShowMessageDialog`, `ShowModalDialog`. | Capability census records `TServerModalDialogProtocolMessageHandler`, generic message dialogs, generic dialog semantics and due-payment/account-economy modal residue. | Generic modal/client-check transport and UI surfaces are statically present. | UNKNOWN. No due-payment or state-changing modal action was executed. |

Generated-message names above are written without their `GameclientMessage` / `GameserverMessage` prefixes for readability; the durable registry files contain the full names.

## Protocol-handler direct code-to-string xrefs

Relevant exact rows from `protocol-handler-code-xrefs.tsv`:

| instruction VA | type string | evidence strength | semantic dispatcher edge proven |
|---:|---|---|---|
| `0xd29a3d` | `tibia::cyclopedia::TCyclopediaProtocolMessageHandler` | `DIRECT_CODE_TO_STRING_XREF` | false |
| `0xd29ffd` | `tibia::dailyreward::TDailyRewardProtocolMessageHandler` | `DIRECT_CODE_TO_STRING_XREF` | false |
| `0xd2a5ed` | `tibia::game::TBlessingsProtocolMessageHandler` | `DIRECT_CODE_TO_STRING_XREF` | false |
| `0xd2ae4d` | `tibia::game::TPremiumProtocolMessageHandler` | `DIRECT_CODE_TO_STRING_XREF` | false |
| `0xd2af1d` | `tibia::game::TServerModalDialogProtocolMessageHandler` | `DIRECT_CODE_TO_STRING_XREF` | false |
| `0xdd556d` | `tibia::market::TMarketProtocolMessageHandler` | `DIRECT_CODE_TO_STRING_XREF` | false |
| `0xdfeebd` | `tibia::store::TStoreProtocolMessageHandler` | `DIRECT_CODE_TO_STRING_XREF` | false |
| `0xdff4ad` | `tibia::trade::TCharacterTradeProtocolMessageHandler` | `DIRECT_CODE_TO_STRING_XREF` | false |

These rows prove executable references to handler-type strings only. They are not message-specific dispatch addresses.

## Evidence classification

**FACT**

- The exact client fence is `15.32.df7b29`, SHA256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- The exact generated-message denominator is 349: 160 client-to-server and 189 server-to-client.
- The named G24-G31 generated-message families above occur in those durable registry files where stated.
- The eight listed handler-type strings have the listed executable xrefs, `DIRECT_CODE_TO_STRING_XREF` evidence and `semantic_dispatcher_edge_proven=false`.
- The UI/controller observations above are recorded by the exact-build capability census, not inferred from a different client version.
- Draft PR #536 owns the shared G24-G31 matrix/checklist; this task does not modify those paths.
- No login, credentials, GUI input, process control, purchase/sale, offer mutation, coin transfer, reward claim, auction/trade commitment, world transfer, main-character change or due-payment action was performed by this task.

**INFERENCE**

- The coexistence of read/browse state and transaction-producing generated-message names indicates a meaningful economy/account transport surface worth deeper exact-build dispatcher recovery. It does not establish live semantics.

**UNKNOWN**

- Generated-message-to-concrete-handler dispatch edges.
- Exact outgoing dispatcher functions, payload layouts and wire encodings for current C2S names.
- Handler-to-controller/storage mutation edges for these economy/account families.
- Live GUI labels, state transitions, panel completeness and confirmation boundaries.
- Dedicated generated-message mapping for world transfer/main-character change.
- Server-side acceptance/rejection and transactional effects, intentionally untested.

## Physical runtime blocker

Live revalidation of the configured `synology-otclient-01` / `otclient-track-a-kasmvnc` runtime through Remote Desktop Commander did not produce a verifiably reachable session in this execution. Historical runtime observations are therefore non-authoritative for this report.

Blocker code: `PHYSICAL_RUNTIME_UNAVAILABLE_VIA_REMOTE_DESKTOP_COMMANDER`.

Even if the runtime becomes reachable, this task's authority does not permit login, credentials, GUI input, process control or transaction-producing actions. A separate admissible runtime task with explicit authority is required before those operations can be considered.

## Impact on the shared matrix

This task adds task-local static evidence for G24-G31, but intentionally does not change PR #536 status rows.

- G24 still needs generated-message-to-outgoing-dispatch proof plus a safe confirmation-boundary runtime experiment before create/cancel/accept semantics can be claimed.
- G25 still needs generated-message-to-outgoing-dispatch proof and safe read-only runtime proof for catalogue/balance/history; purchase and transfer paths remain prohibited without separate authority.
- G26-G31 retain runtime-semantic gaps; exact-build static UI residue and generated-message names alone do not satisfy runtime verification.

## Result

The bounded static research slice is complete. It establishes an exact-build static protocol/UI census for the economy/account panel surface while preserving all confirmation and transaction safety boundaries. Runtime verification is not claimed.
