# Track A economy panels - GUI-safe diagnostic observation

Date: 2026-08-19
Task: `OTC-20260819-track-a-economy-panels-runtime-readonly`
PR: #550
Runtime locator used: `synology-otclient-01` / `otclient-track-a-kasmvnc` / `DISPLAY=:1`

## Controlling governance classification

The owner invocation explicitly continued #528 and #550 and preserved the prior consent. That established a semantic permission boundary for GUI-safe economy-panel work, but it did not override Track A runtime admission.

The GUI sequence below was executed under a task record that used the unsupported value `runtime_access: bounded_gui_readonly_navigation`. Exact-head Track A governance run `32240817177` failed the deterministic admission-policy job with:

```text
Track A runtime admission invalid: unsupported runtime_access='bounded_gui_readonly_navigation'
```

Therefore every GUI semantic observation below is retained as a factual, secret-free **diagnostic observation only**. It is **not promotion-grade Track A evidence** and must not be used to mark the affected coverage groups PASS/DONE until a minimal revalidation is performed under a supported, actually satisfied runtime admission class.

After this defect was identified, no further GUI input was sent.

## Controller-plane reconciliation

Read-only controller-plane inspection of the authoritative state inside `otclient-synology-runner` established:

```text
state_root=/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime
lease_status=active_but_expired
lease_controller_task=OTC-20260818-native-login-to-ingame-e2e
lease_generation=16
lease_expires_utc=2026-08-18T15:49:15Z
runtime-registration.json=MISSING
```

Current trusted-base rules fail closed for further #550 GUI mutation:

- `read_only` cannot send keyboard/mouse input or change UI state;
- `ephemeral_isolated` requires a task-owned isolated sandbox and cannot take over another task/shared runtime surface;
- `canonical_reuse_or_mutation` requires an authoritative registration and the applicable Gate A/rebind/Gate B chain;
- canonical bootstrap requires registration absence plus an under-lock inventory proving zero existing official-client candidates/sessions, which cannot be true while the already-running exact Kasm client exists.

The current blocker is therefore `TRACK_A_RUNTIME_ADMISSION_UNAVAILABLE_FOR_SHARED_KASM_GUI_MUTATION`.

## Diagnostic exact-target observation before the GUI sequence

At the time of the diagnostic GUI sequence, direct runtime inspection found one intended official client target:

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

The same PID/start/size/SHA and three exactly-one structural discriminators were observed again after the GUI sequence. This is factual diagnostic provenance only; it does not repair the missing runtime admission.

## G25 Store / Tibia Coin history - diagnostic observed, not promotable

The visible Store control opened the Store dialog. Read-only navigation exposed categories including `Home`, `Premium Time`, `Consumables`, `Bundles`, `Cosmetics`, `Houses`, `Boosts`, `Extras`, `History` and `Close`.

Invoking `History` produced a generic message dialog:

```text
Failed to retrieve Coins History
No entries yet.
```

The dialog was dismissed. `Premium Time` was also opened read-only. No purchase or currency transfer was initiated and no `Buy` action was used.

## G28 Character / premium - diagnostic observed, not promotable

Tooltip-confirmed `Open Tibia Cyclopedia` navigation exposed tabs including:

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

The `Character` tab exposed sections including `General Stats`, `Battle Results`, `Achievements`, `Item Summary`, `Appearances`, `Store Summary`, and `Character Titles`.

The sidebar `Show Premium Features` control also expanded a premium-features panel and was then collapsed. The dedicated Blessings subpanel was not reached.

## G30 world transfer / main-character change - diagnostic observed, not promotable

Store `Extras` exposed account-service catalogue entries including:

```text
World Transfer
Express World Transfer
Main Character Change
Name Change
Sex Change
```

The default World Transfer details pane was visible. No `Configure`, `Buy`, transfer, main-character-change or other commitment control was used. The dedicated commit/controller path was not entered.

## G31 generic modal flow - diagnostic observed, not promotable

The Coin History request produced and dismissed a real generic message dialog, diagnostically demonstrating that modal/message flow in the observed current build.

## Not reached

```yaml
G24_market: NOT_REACHED
G26_daily_reward: NOT_REACHED
G27_reward_wall_resting_returner: NOT_REACHED
G28_blessings_subpanel: NOT_REACHED
G29_character_auction_trade: NOT_REACHED
```

`NOT_REACHED` is not evidence of absence. No character movement, logout/relogin, hidden-shortcut guessing or external account-flow navigation was used merely to force coverage.

## Side effects

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

Temporary screenshots used for immediate inspection were deleted from both host and container. No raw screenshot is committed.

## Disposition

G25, partial G28, G30 Store service UI and G31 remain diagnostic observations only. The next legal step is not more GUI exploration: first establish a reviewed admission/reconciliation path for the existing unregistered shared Kasm client, or another lawful task-owned runtime, then minimally revalidate the relevant SAFE_READ observations before coordinator promotion.
