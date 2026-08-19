# TIBIA-RE-ECONOMY-PANELS — accepted static census

Source task: `OTC-20260819-track-a-economy-panels-static-census`  
Source Draft PR: #546  
Source validated head: `54dca602dfa38f1cc347716cf0f701b22c3fe6e9`

## Exact S1 evidence fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
generated_messages_total: 349
client_to_server: 160
server_to_client: 189
received_message_strings: 189
protocol_handler_type_xrefs: 47
```

Independently re-read durable sources:

- `docs/agents/reports/OTCLIENT-20260818-track-a-s1-unfiltered-static-census.md`
- `docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-client-to-server.txt`
- `docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-server-to-client.txt`
- `docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-handler-code-xrefs.tsv`

## Capability-census provenance correction

The source Draft incorrectly reported a digest conflict for `docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md`.

Fresh coordinator verification found the same exact researched-client SHA in all four relevant locations:

```text
capability census @ source base a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb
  e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe

capability census @ source head 54dca602dfa38f1cc347716cf0f701b22c3fe6e9
  e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe

PR #293 merged research-design record
  e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe

archive OTC-20260814-official-client-capability-experiment-sweep
  consistent with PR #293; no conflicting digest is recorded
```

Therefore `capability_census_digest_provenance=CONFLICT` is rejected. The canonical capability-census report is itself fenced to the same historical exact binary. Its economy/account UI/controller observations may be retained as **exact-build static report leads**. They still do not prove live GUI behavior, normal call paths, dispatcher causality, ABI, confirmation behavior, or server-side effects.

## G24-G31 accepted findings

| Group | Exact S1 generated-message evidence | Same-exact-build capability-census report lead | Accepted conclusion |
|---|---|---|---|
| G24 Market | C2S `MarketAccept`, `MarketBrowse`, `MarketCancel`, `MarketCreate`, `MarketLeave`, `MarketStatistics`; S2C `MarketBrowse`, `MarketDetail`, `MarketEnter`, `MarketLeave`, `MarketStatistics` | Market controller/protocol/storage; offer/history/item-detail UI | Exact transport-name surface proven; static UI/controller lead retained; live dispatch/confirmation/transaction semantics UNKNOWN. |
| G25 Store / coins | C2S `BuyStoreOffer`, `GetTransactionDetails`, `GetTransactionHistory`, `OpenTransactionHistory`, `RequestResourceBalance`, `RequestStoreCategories`, `RequestStoreOffers`, `StoreEvent`, `TransferCurrency`; S2C `CreditBalance`, `RequestPurchaseData`, `ResourceBalance`, `SetStoreButtonDeeplink`, `StoreButtonIndicators`, `StoreCategories`, `StoreError`, `StoreOffers`, `StoreSuccess`, `TransactionDetails`, `TransactionHistory`, `UpdatingShopBalance` | Store protocol/controller, purchase confirmation/success, transaction history, coin-details UI | Exact read and transaction-producing transport names proven; static UI/controller lead retained; no purchase/transfer semantics promoted. |
| G26 Daily Reward | C2S `CollectDailyReward`, `DailyRewardHistory`; S2C `DailyRewardBasic`, `DailyRewardCollectionState`, `DailyRewardHistory` | Daily Reward item-pick/collection UI | Exact reward transport names proven; static UI lead retained; claim semantics UNKNOWN and untested. |
| G27 Reward Wall/resting/returner | C2S `OpenRewardWall`; S2C `OpenRewardWall`, `CloseRewardWall`, `RestingAreaState` | Reward Wall/resting/returner state | Exact wall/resting transport names proven; static lead retained; claim/state-transition semantics UNKNOWN. |
| G28 Character/account UI | C2S `BlessingsDialog`, `OpenCyclopediaCharacterInfo`; S2C `Blessings`, `BlessingsDialog`, `CyclopediaCharacterInfo`, `PremiumTrigger` | Character Info, Blessings and premium-related controllers | Exact character-info/blessings/premium transport names proven; static controller lead retained; live semantics UNKNOWN. |
| G29 Character auction/trade | C2S `CharacterTradeConfigurationAction`; S2C `CharacterTradeConfiguration` | Character auction configuration and character-trade dialog | Exact character-trade configuration transport names proven; static UI lead retained; commitment semantics UNKNOWN. |
| G30 World transfer/main-character change | No dedicated generated-message name identified in the bounded 160/189 S1 review | due-payment, world-transfer, main-character-change controller leads | Dedicated S1 transport mapping UNKNOWN; controller presence is static evidence only. |
| G31 Misc modal/panel | C2S `AnswerModalDialog`, `ClientCheck`; S2C `ClientCheck`, `ShowMessageDialog`, `ShowModalDialog` | server modal handler, generic dialogs/account-economy modal residue | Exact generic modal/client-check names proven; static UI lead retained; specific modal semantics UNKNOWN. |

Full names in the retained registries carry the `GameclientMessage` / `GameserverMessage` prefixes.

## Exact handler-type xrefs

```text
0xd29a3d tibia::cyclopedia::TCyclopediaProtocolMessageHandler DIRECT_CODE_TO_STRING_XREF false
0xd29ffd tibia::dailyreward::TDailyRewardProtocolMessageHandler DIRECT_CODE_TO_STRING_XREF false
0xd2a5ed tibia::game::TBlessingsProtocolMessageHandler DIRECT_CODE_TO_STRING_XREF false
0xd2ae4d tibia::game::TPremiumProtocolMessageHandler DIRECT_CODE_TO_STRING_XREF false
0xd2af1d tibia::game::TServerModalDialogProtocolMessageHandler DIRECT_CODE_TO_STRING_XREF false
0xdd556d tibia::market::TMarketProtocolMessageHandler DIRECT_CODE_TO_STRING_XREF false
0xdfeebd tibia::store::TStoreProtocolMessageHandler DIRECT_CODE_TO_STRING_XREF false
0xdff4ad tibia::trade::TCharacterTradeProtocolMessageHandler DIRECT_CODE_TO_STRING_XREF false
```

All rows prove only direct code-to-type-string references. `semantic_dispatcher_edge_proven=false`; none is a message-specific dispatcher address.

## Runtime/safety boundary

This promotion is repository-only static review with `runtime_access: none`, `mutation_authorized: false`, and `physical_e2e_required: false`. The source Draft recorded a failed Remote Desktop Commander reachability probe, but this promotion does not treat that mutable device status as current evidence and does not rely on it for acceptance.

No login, credentials, GUI input, process control, gameplay, purchase/sale, market mutation, Tibia Coin transfer, reward claim, auction/trade commitment, world transfer, main-character change or due-payment action is part of this promotion.

## Remaining UNKNOWN

- generated-message-to-concrete-handler dispatch;
- outgoing dispatcher functions, payload layouts and wire encoding;
- handler-to-controller/storage mutation edges;
- live GUI labels, state transitions, completeness and confirmation boundaries;
- dedicated G30 generated transport mapping;
- server-side transactional effects.

## Source exact-head validation

```yaml
source_head: 54dca602dfa38f1cc347716cf0f701b22c3fe6e9
source_base: a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb
source_changed_files: 2
source_scope_only: true
Track_A_governance_run: 32219366592
Track_A_governance_result: success
CI_run: 32219366648
CI_result: success
```

Shared matrix/checklist PR #536 was not modified.