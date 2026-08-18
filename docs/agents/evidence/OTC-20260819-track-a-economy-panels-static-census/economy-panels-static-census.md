# TIBIA-RE-ECONOMY-PANELS static census

Task: `OTC-20260819-track-a-economy-panels-static-census`

Scope: G24-G31, repository-only static research.

## Authority and safety boundary

This slice is SAFE_READ. It does not authorize or execute login, credential use, GUI input, gameplay, official-client process control, purchase/sale, market-offer mutation, Tibia Coin transfer, reward claim, character auction/trade commitment, world transfer, main-character change, or due-payment actions.

The candidate alias pack in Draft PR #543 is used only to resolve the intended G24-G31 research scope. Its unmerged permissions are not treated as authority. The trusted base authority is `main` at `a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb` plus the owner's `TIBIA-RE-ECONOMY-PANELS uruchom autonomicznie` instruction.

## Evidence fence

### Current exact-build static evidence

Source: `docs/agents/reports/OTCLIENT-20260818-track-a-s1-unfiltered-static-census.md` and its task-owned evidence directory.

- build: `15.32.14690`
- ELF SHA256: `3491185a3cfb81b942297574752703aaa29827c419b1b174bf595e7f47ad2fe4c`
- client-to-server registered name families: 160
- server-to-client registered name families: 189
- protocol handler class names with code xrefs: 189/189
- source roots recovered by the census: 30/30

This proves static registry/name presence and handler-family code-reference presence only. It does **not** prove live GUI behavior, outgoing dispatcher semantics, message wire encoding, confirmation behavior, or successful server-side transaction semantics.

### Prior-version UI/controller evidence

Source: `docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md`.

- prior snapshot: `15.32.df7b29`
- ELF SHA256: `e6cfa9ff3e04c6d643e79e071d162150678627681072633673eca5b3a1a7116c`

This report is used only as version-fenced evidence that the named UI/controller subtrees existed in that prior snapshot. Persistence of those exact class/controller implementations into `15.32.14690` is not asserted unless independently re-proved.

### Shared full-client matrix

Draft PR #536 owns the shared G24-G31 matrix/checklist paths. This task reads them but does not edit or promote them.

## G24-G31 findings

| Group | Current exact-build protocol-name evidence | Prior-version UI/controller evidence | Static conclusion | Runtime status |
|---|---|---|---|---|
| G24 Market | C2S: `EnterMarket`, `MarketAccept`, `MarketBrowse`, `MarketCancel`, `MarketCreate`, `MarketLeave`, `MarketStatistics`. S2C: `ShowMarket`, `MarketDetail`, `MarketBrowse`, `MarketStatistics`, `MarketEnter`, `MarketLeave`. | `TMarketController`, `TMarketV2Controller`, market presenter/config/item/filter/menu/statistics families. | Market browse/statistics plus transaction-producing offer families are present in the static protocol registry. | UNKNOWN. No live panel, outgoing dispatcher, create/cancel/accept boundary, or server result was exercised. |
| G25 Store / Tibia Coin / transaction UI | C2S: `RequestStoreCategories`, `RequestStoreOffers`, `BuyStoreOffer`, `OpenTransactionHistory`, `GetTransactionHistory`, `GetTransactionDetails`, `TransferCurrency`, `RequestResourceBalance`, `RequestPurchaseData`, `OpenGetCoinsUrl`. S2C: `ShowStore`, `StoreOfferDescriptions`, `TransactionHistory`, `StoreInbox`, `StoreError`, `StorePurchaseSuccessful`, `CoinBalance`, `StoreSummary`. | `TStoreController`, `TStoreEventController`, `TStoreOffer`, `TStoreProduct` and store-related UI/content families. | Catalogue, balance/history and transaction-producing names coexist statically. This task intentionally stops before all spend/transfer/commit paths. | UNKNOWN. No purchase, transfer, confirmation or balance mutation was executed. |
| G26 Daily Reward | C2S: `CollectDailyReward`, `DailyRewardHistory`. S2C: `DailyRewardCollectionState`, `DailyRewardHistory`. | `TDailyRewardController` and Daily Reward UI/state residue. | Reward collection/history protocol families are statically present. | UNKNOWN. No claim was executed. |
| G27 Reward Wall / resting / returner | C2S: `OpenRewardWall`. S2C: `RewardWallOpen`, `RestingAreaState`; Daily Reward state is adjacent. | `TRewardWallPresenter`, `TRewardWallController`, `TRewardWallConfig`, reward-wall list/button/history classes, `TReturnerController`, resting/returner/login-streak residue. | Read-side wall/resting/returner state has static support; live state transitions are not established. | UNKNOWN. No reward claim or state-changing action was executed. |
| G28 Character/account-management related UI | C2S: `OpenCyclopediaCharacterInfo`, `BlessingsDialog`. S2C: `CharacterInfo`, `Blessings`. | `TCharacterInfoController`, character-info dialogs, `TBuyPremiumDialog` and premium-benefit/dialog families. | Character-info/blessings transport names are present in current registry; premium/controller residue is prior-version evidence only. | UNKNOWN. No account/premium mutation or purchase was exercised. |
| G29 Character auction/trade UI | C2S: `CharacterTradeConfigurationAction`. No dedicated current S2C auction/trade family was established by this slice. | `TCharacterAuctionConfig`, `TCharacterAuctionController`, auction filters/buttons; `TCharacterTradeController`, `TCharacterTradeInformationController`, trade filters. | A current client-side trade configuration action name exists. Rich auction/trade UI is version-fenced to the prior census unless re-proved on current build. | UNKNOWN. No auction/trade commitment was executed. |
| G30 World transfer / main-character change | No dedicated current-build protocol family was established by this slice. | `TWorldTransferController`, `TWorldTransferTargetWorldCard`, `TWorldTransferRequest`; `TMainCharacterChangeConfig`, `TMainCharacterChangeController` and related list/detail/dialog subtree. | UI/controller existence is prior-version static evidence; current-build dedicated transport mapping is UNKNOWN. | UNKNOWN. No transfer or main-character-change action was executed. |
| G31 Misc modal/panel flows | C2S: `AnswerModalDialog`, `ClientCheck`. S2C: `ModalDialog`, `ClientCheck`. | `TDuePaymentDialog` plus account-status/site-message/modal residue in the prior capability census. | Generic modal/client-check families are present in the current registry; specific due-payment/account modal semantics are not established for the current build here. | UNKNOWN. No due-payment or state-changing modal action was executed. |

## Handler-family code xrefs

The current exact-build `protocol-handler-code-xrefs.tsv` proves code references to handler-family class strings, but explicitly records `semantic_dispatcher_recovered=false`. Relevant examples are:

| Handler family | class string VA | code xref VA | semantic dispatcher recovered |
|---|---:|---:|---|
| `TIpcServerStoreHandler` | `0x0b3123b4` | `0x0dd550e3` | false |
| `TIpcServerCharacterInfoHandler` | `0x0b81c884` | `0x0dd55053` | false |
| `TIpcServerGeneralHandler` | `0x0b60fd3e` | `0x0dd5509b` | false |
| `TIpcServerGameHandler` | `0x0b5cf030` | `0x0dd54fc3` | false |

These are handler-family xrefs. They are **not** message-specific dispatcher addresses and must not be represented as such.

## Evidence classification

**FACT**

- The named G24-G31 protocol families above are present in the trusted current-build S1 registry files where stated.
- The listed handler-family class strings have the listed code xrefs and `semantic_dispatcher_recovered=false`.
- The named market/store/reward/character/auction/trade/world-transfer/main-character-change/due-payment controller families were recorded by the prior-version capability census where stated.
- Draft PR #536 still owns the shared G24-G31 matrix/checklist; this task does not modify those paths.
- No login, credentials, GUI input, process control, purchase/sale, offer mutation, coin transfer, reward claim, auction/trade commitment, world transfer, main-character change or due-payment action was performed by this task.

**INFERENCE**

- The coexistence of browse/read and transaction-producing protocol names indicates a meaningful economy/account transport surface worth deeper exact-build dispatcher recovery. It does not establish live semantics.

**UNKNOWN**

- Current-build persistence of every prior-version UI/controller class listed above.
- Exact outgoing dispatcher functions and wire encodings for the current C2S names.
- Message-specific inbound dispatch functions beyond the recovered handler-family xrefs.
- Live GUI labels, state transitions, panel completeness and confirmation boundaries.
- Current-build dedicated protocol mapping for world transfer/main-character change.
- Server-side acceptance/rejection and transactional effects, intentionally untested.

## Physical runtime blocker

Live revalidation of the configured `synology-otclient-01` / `otclient-track-a-kasmvnc` runtime through Remote Desktop Commander did not produce a verifiably reachable session in this execution. Historical runtime observations are therefore non-authoritative for this report.

Blocker code: `PHYSICAL_RUNTIME_UNAVAILABLE_VIA_REMOTE_DESKTOP_COMMANDER`.

Even if the runtime becomes reachable, this task's authority does not permit login, credentials, GUI input, process control or transaction-producing actions. A separate admissible runtime task with explicit authority is required before those operations can be considered.

## Impact on the shared matrix

This task adds task-local static evidence for G24-G31, but intentionally does not change PR #536 status rows. In particular:

- G24 still needs exact outgoing dispatch plus safe confirmation-boundary proof before create/cancel/accept semantics can be claimed.
- G25 still needs exact outgoing dispatch and safe read-only runtime proof for catalogue/balance/history; purchase and transfer paths remain prohibited without separate authority.
- G26-G31 retain runtime-semantic gaps; static UI residue and registry names alone do not satisfy runtime verification.

## Result

The bounded static research slice is complete. It establishes a version-fenced protocol/UI census for the economy/account panel surface while preserving all confirmation and transaction safety boundaries. Runtime verification is not claimed.