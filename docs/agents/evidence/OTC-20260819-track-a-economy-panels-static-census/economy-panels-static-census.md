# TIBIA-RE-ECONOMY-PANELS static census

Task: `OTC-20260819-track-a-economy-panels-static-census`

Scope: G24-G31, repository-only static research.

## Authority and safety boundary

This slice is SAFE_READ. It does not authorize or execute login, credential use, GUI input, gameplay, official-client process control, purchase/sale, market-offer mutation, Tibia Coin transfer, reward claim, character auction/trade commitment, world transfer, main-character change, or due-payment actions.

The candidate alias pack in Draft PR #543 is used only to resolve the intended G24-G31 research scope. Its unmerged permissions are not treated as authority. The trusted base authority is `main` at `a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb` plus the owner's `TIBIA-RE-ECONOMY-PANELS uruchom autonomicznie` instruction.

## Evidence fences

### S1 generated protocol / handler census — exact binary

The independently re-read S1 sources identify:

- version: `15.32.df7b29`
- size: `51965216`
- SHA256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

Sources:

- `docs/agents/reports/OTCLIENT-20260818-track-a-s1-unfiltered-static-census.md`
- `docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-client-to-server.txt`
- `docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-server-to-client.txt`
- `docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-handler-code-xrefs.tsv`

The S1 census establishes an exact generated-message denominator of `349`: `160` client-to-server plus `189` server-to-client. It also records `189` `received*Message` strings and `47` distinct `*ProtocolMessageHandler` class strings with direct executable code-to-string xrefs. Every handler xref is explicitly classified `DIRECT_CODE_TO_STRING_XREF` with `semantic_dispatcher_edge_proven=false`.

### Capability UI/controller census — provenance conflict

Source: `docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md`.

The capability report declares version `15.32.df7b29` but its header currently declares SHA256:

`e6cfa9ff3e04c6d643e79e071d162150678627681072633673eca5b3a1a7116c`

Two related durable records for the same research-design delivery instead identify the historical researched binary as:

`e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

Those records are PR #293 and `docs/agents/tasks/archive/OTC-20260814-official-client-capability-experiment-sweep.md`.

This task does not silently choose which metadata value is the typo. Therefore UI/controller observations from the capability report are retained as **version-fenced capability-census evidence with an unresolved digest-provenance conflict**. They are not promoted here as exact-hash proof for the S1 binary until that historical metadata conflict is explicitly reconciled.

These are static observations. They do **not** prove live GUI behavior, message wire encoding, message-to-handler dispatch, confirmation behavior, or successful server-side transaction semantics.

## G24-G31 findings

| Group | Exact S1 generated-message evidence (`e6c244bd…`) | Capability-census UI/controller evidence (digest provenance unresolved) | Static conclusion | Runtime status |
|---|---|---|---|---|
| G24 Market | C2S: `MarketAccept`, `MarketBrowse`, `MarketCancel`, `MarketCreate`, `MarketLeave`, `MarketStatistics`. S2C: `MarketBrowse`, `MarketDetail`, `MarketEnter`, `MarketLeave`, `MarketStatistics`. | Capability census records `TMarketController`, `TMarketProtocolMessageHandler`, `TMarketStorage::marketItemDetailsChanged`, item/category selection, offer cancel, history, own offers and item details. | Exact S1 transport-name surface is present; controller evidence is a separate provenance-fenced lead. | UNKNOWN. No live panel, message dispatch, create/cancel/accept confirmation boundary or server result was exercised. |
| G25 Store / Tibia Coin / transaction UI | C2S: `BuyStoreOffer`, `GetTransactionDetails`, `GetTransactionHistory`, `OpenTransactionHistory`, `RequestResourceBalance`, `RequestStoreCategories`, `RequestStoreOffers`, `StoreEvent`, `TransferCurrency`. S2C: `CreditBalance`, `RequestPurchaseData`, `ResourceBalance`, `SetStoreButtonDeeplink`, `StoreButtonIndicators`, `StoreCategories`, `StoreError`, `StoreOffers`, `StoreSuccess`, `TransactionDetails`, `TransactionHistory`, `UpdatingShopBalance`. | Capability census records Store protocol/controller presence, purchase confirmation/success dialogs, transaction-history opening and a coin-transaction details dialog. | Exact S1 catalogue/balance/history and transaction-producing transport names coexist; UI/controller evidence remains provenance-fenced. | UNKNOWN. No purchase, transfer, confirmation or balance mutation was executed. |
| G26 Daily Reward | C2S: `CollectDailyReward`, `DailyRewardHistory`. S2C: `DailyRewardBasic`, `DailyRewardCollectionState`, `DailyRewardHistory`. | Capability census records a Daily Reward item-pick controller and fixed-item/pick-item collection request surfaces. | Exact S1 reward state/history/collection names are present; UI/controller evidence remains provenance-fenced. | UNKNOWN. No reward claim was executed. |
| G27 Reward Wall / resting / returner | C2S: `OpenRewardWall`. S2C: `OpenRewardWall`, `CloseRewardWall`, `RestingAreaState`. | Capability census records Reward Wall resting-area bonuses, `TNewsStorage::returnerInformationChanged` and authentication returner-reward state. | Exact S1 Reward Wall open/close/resting names are present; returner/UI evidence remains provenance-fenced. | UNKNOWN. No reward claim or state-changing action was executed. |
| G28 Character/account-management related UI | C2S: `BlessingsDialog`, `OpenCyclopediaCharacterInfo`. S2C: `Blessings`, `BlessingsDialog`, `CyclopediaCharacterInfo`, `PremiumTrigger`. | Capability census records `TCharacterInfoDialogController` routes to XP boost, Blessings, Item Info, outfit, Skill Wheel and Weapon Proficiency; blessing and premium/store-related controllers are present. | Exact S1 character-info/blessings/premium transport names are present; controller evidence remains provenance-fenced. | UNKNOWN. No account/premium mutation or purchase was exercised. |
| G29 Character auction/trade UI | C2S: `CharacterTradeConfigurationAction`. S2C: `CharacterTradeConfiguration`. | Capability census records `TCharacterAuctionConfiguration`, `TCharacterTradeDialogController` and related account/economy UI. | Exact S1 character-trade configuration transport names are present; richer auction/trade UI evidence remains provenance-fenced. | UNKNOWN. No auction/trade commitment was executed. |
| G30 World transfer / main-character change | No dedicated generated-message name was identified in the exact S1 160/189 registry by this bounded slice. | Capability census records a due-payment dialog, world-transfer controller and main-character-change controller. | Dedicated S1 transport mapping remains UNKNOWN; UI/controller existence is only a provenance-fenced lead in this task. | UNKNOWN. No transfer or main-character-change action was executed. |
| G31 Misc modal/panel flows | C2S: `AnswerModalDialog`, `ClientCheck`. S2C: `ClientCheck`, `ShowMessageDialog`, `ShowModalDialog`. | Capability census records `TServerModalDialogProtocolMessageHandler`, generic message dialogs, generic dialog semantics and due-payment/account-economy modal residue. | Exact S1 generic modal/client-check transport names are present; UI semantics remain provenance-fenced. | UNKNOWN. No due-payment or state-changing modal action was executed. |

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

- The S1 exact client fence is `15.32.df7b29`, SHA256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- The S1 generated-message denominator is 349: 160 client-to-server and 189 server-to-client.
- The named G24-G31 generated-message families above occur in those durable S1 registry files where stated.
- The eight listed handler-type strings have the listed executable xrefs, `DIRECT_CODE_TO_STRING_XREF` evidence and `semantic_dispatcher_edge_proven=false`.
- The capability-census report records the UI/controller observations above, but its header SHA conflicts with PR #293 and the archived design task's historical binary SHA.
- Draft PR #536 owns the shared G24-G31 matrix/checklist; this task does not modify those paths.
- No login, credentials, GUI input, process control, purchase/sale, offer mutation, coin transfer, reward claim, auction/trade commitment, world transfer, main-character change or due-payment action was performed by this task.

**INFERENCE**

- The coexistence of read/browse state and transaction-producing generated-message names indicates a meaningful economy/account transport surface worth deeper exact-build dispatcher recovery. It does not establish live semantics.

**UNKNOWN**

- Whether the capability report's SHA mismatch is a report-header typo or reflects a different retained binary.
- Exact S1-hash persistence of every capability-census UI/controller observation until the digest provenance is reconciled or the classes are re-proved independently.
- Generated-message-to-concrete-handler dispatch edges.
- Exact outgoing dispatcher functions, payload layouts and wire encodings for S1 C2S names.
- Handler-to-controller/storage mutation edges for these economy/account families.
- Live GUI labels, state transitions, panel completeness and confirmation boundaries.
- Dedicated generated-message mapping for world transfer/main-character change.
- Server-side acceptance/rejection and transactional effects, intentionally untested.

## Physical runtime blocker

Fresh live revalidation of the configured `synology-otclient-01` device through Remote Desktop Commander returned the device as `offline`; ping returned `ok: false` with `Remote device unreachable: http://100.111.121.111:3001/mcp`. Historical runtime observations are therefore non-authoritative for this report.

Blocker code: `PHYSICAL_RUNTIME_UNAVAILABLE_VIA_REMOTE_DESKTOP_COMMANDER`.

This task is admitted as `runtime_access: none` and `physical_e2e_required: false`. Runtime unavailability therefore does not block the bounded static closeout, but runtime semantics remain explicitly unverified. Transaction-producing actions remain outside this task's safety boundary in every case.

## Impact on the shared matrix

This task adds task-local static evidence for G24-G31, but intentionally does not change PR #536 status rows.

- G24 still needs generated-message-to-outgoing-dispatch proof plus a safe confirmation-boundary runtime experiment before create/cancel/accept semantics can be claimed.
- G25 still needs generated-message-to-outgoing-dispatch proof and safe read-only runtime proof for catalogue/balance/history; purchase and transfer paths remain prohibited without separate authority.
- G26-G31 retain runtime-semantic gaps; static names and provenance-fenced UI/controller leads alone do not satisfy runtime verification.
- No current-S1 exact-build UI/controller claim should be promoted from the capability report until its digest metadata is reconciled or independently re-proved.

## Coordinator-review result

A fresh review re-read the durable S1 registries, the protocol-handler xref catalogue, the capability report, PR #293 metadata, the archived capability-design task, PR #536 ownership and the Track A admission contract. It found two material issues in the initial Draft: missing `runtime_access: none` admission fields and an unsupported same-exact-binary claim across conflicting SHA metadata. Both are corrected in the source task/evidence before promotion.

## Result

The bounded static research slice is complete after correction. It establishes exact-S1 generated-message and handler-type evidence for the economy/account panel surface, preserves separately provenance-fenced UI/controller leads, and keeps all runtime and transaction semantics unclaimed.
