# Track A economy panels — bounded GUI-safe live observation

Date: 2026-08-19  
Task: `OTC-20260819-track-a-economy-panels-runtime-readonly`  
PR: #550  
Runtime: `synology-otclient-01` / `otclient-track-a-kasmvnc` / `DISPLAY=:1`

## Authority boundary

The owner invocation on 2026-08-19 explicitly continued both #528 and #550 and preserved the existing consent. For #550 this invocation was admitted only as bounded, reversible GUI-safe panel navigation on the already-authenticated official-client session.

```yaml
gui_input_authorized: true
mutation_scope: reversible_local_ui_navigation_only
login_authorized_by_550: false
credential_use_authorized_by_550: false
gameplay_authorized: false
process_control_authorized: false
transaction_authorized: false
```

Authentication semantics remain isolated to #528. No credential re-entry was needed because the current #528 runtime was already structurally in-game.

## Fresh exact-runtime fence

Before GUI input and again after the observation sequence, direct runtime inspection proved the same target:

```text
PID=11365
START_TICKS=74970818
XID=0x1a00017
SIZE=52109920
SHA256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
persistent TIBIA_TEST_EMAIL/TIBIA_TEST_PASSWORD environment entries=0
player_protocol_handler validated_hits=1
gameserver_game_session validated_hits=1
worldmap_handler validated_hits=1
```

The visible window remained bound to PID 11365 and the exact expected official client. The three native structural discriminators remained exactly-one after GUI observation, so the retained session stayed structurally in-game.

## Live semantic observations

Only controls whose visible tooltip or already-open panel made the action unambiguous were used. No product purchase/confirmation control, reward claim, market action, transfer confirmation, trade action or gameplay movement was used.

### G25 — Store / Tibia Coin history: LIVE_READ_ONLY_PASS

The visible `Store` control opened the live Store dialog. The dialog exposed read-only category/navigation state including `Home`, `Premium Time`, `Consumables`, `Bundles`, `Cosmetics`, `Houses`, `Boosts`, `Extras`, `History` and `Close`.

The `History` control was invoked as a read-only request. The Store closed and a generic message dialog reported:

```text
Failed to retrieve Coins History
No entries yet.
```

The dialog was acknowledged with its `ok` button. No purchase, currency transfer or other transaction was initiated.

The `Premium Time` category was also opened read-only and displayed premium-time offer rows/details. No `Buy` control was used.

### G28 — Character / premium UI: LIVE_PARTIAL_PASS

The main toolbar was mapped using hover tooltips before clicks. The verified `Open Tibia Cyclopedia` control opened Cyclopedia. Its tab tooltips were observed read-only and included:

```text
Items
Bestiary
Charms
Map
Houses
Character
Bosstiary
Boss Slots
Magical Archive
```

The verified `Character` tab opened the live character page. The page exposed sections including:

```text
General Stats
Battle Results
Achievements
Item Summary
Appearances
Store Summary
Character Titles
```

This proves a live current-build character-information surface. It does not by itself prove the dedicated Blessings controller/subpanel.

Separately, the sidebar `Show Premium Features` control expanded a live premium-features panel. The panel exposed premium-benefit state/text and was then collapsed. Combined with the Store `Premium Time` page, this is live current-build premium-related UI evidence. No purchase path was used.

### G30 — World transfer / main-character-change UI: LIVE_STORE_SURFACE_PASS

The Store `Extras` category was opened read-only. Its visible account-service catalogue included at least:

```text
World Transfer
Express World Transfer
Main Character Change
Name Change
Sex Change
```

The details pane for the default World Transfer selection was visible, including an availability message and service description. No `Configure`, `Buy`, transfer, main-character-change or other commitment control was used.

This proves a live current-build Store account-service surface for G30. It does **not** prove that the dedicated world-transfer/main-character-change controller dialog or commit path was entered.

### G31 — generic modal/dialog flow: LIVE_PASS

The Coin History request above produced and dismissed a real generic message dialog. This is direct live evidence for a generic modal/message-dialog flow associated with a bounded economy read.

## Not reached in this bounded GUI-only window

```yaml
G24_market: NOT_REACHED
G26_daily_reward: NOT_REACHED
G27_reward_wall_resting_returner: NOT_REACHED
G29_character_auction_trade: NOT_REACHED
G28_blessings_subpanel: NOT_REACHED
```

No direct, unambiguous, transaction-free entry for these surfaces was established from the bounded current visible toolbar/Store/Cyclopedia window. `NOT_REACHED` is not evidence that the feature is absent. The worker did not move the character, logout/re-enter character selection, open external account flows, or guess hidden shortcuts merely to force coverage.

## Safety and side effects

```text
GUI_CREDENTIAL_ENTRY=false
CREDENTIAL_REENTRY=false
GAMEPLAY_MOVEMENT=false
PROCESS_CONTROL=false
MARKET_OFFER_CREATE_ACCEPT_CANCEL=false
PURCHASE=false
TIBIA_COIN_TRANSFER=false
REWARD_CLAIM=false
CHARACTER_TRADE_COMMIT=false
WORLD_TRANSFER_COMMIT=false
MAIN_CHARACTER_CHANGE_COMMIT=false
DUE_PAYMENT_ACTION=false
```

Temporary screenshots were used only for immediate human-visible semantic inspection. They are not committed as evidence and are to be deleted from the container/host after extracting the sanitized facts above.

## Current result

The earlier passive-login-screen blocker is obsolete for the current runtime. The exact current #528 client is already in-game, and bounded GUI-safe observation now establishes live current-build evidence for G25, partial G28, G30 Store service UI and G31 without credential re-entry or economy/account transactions. G24/G26/G27/G29 and the G28 Blessings subpanel remain unresolved under the present no-gameplay/no-transaction boundary.