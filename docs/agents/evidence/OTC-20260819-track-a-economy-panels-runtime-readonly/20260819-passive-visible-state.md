# TIBIA-RE-ECONOMY-PANELS — passive visible-state observation

Date: 2026-08-19
Task: `OTC-20260819-track-a-economy-panels-runtime-readonly`
Trusted base at re-admission: `main@08c0b6f89ffddd4c75b8f60060ce3b2a62195d95`

## Admission prerequisite

Fresh re-admission evidence is recorded in `20260819-kasm-readonly-preflight-v2.md` and proves one exact current official client on Kasm `DISPLAY=:1`, PID `17954`, start ticks `74839161`, XID `0x1a00017`, size `52109920`, SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`, with zero competing official-client candidates.

## Passive observation result

A single X11 frame was captured according to the trusted KasmVNC observation runbook without activating or driving the client.

Sanitized result:

```yaml
client_visible_state: LOGIN_SCREEN
character_select_visible: false
in_game_visible: false
G24_market_visible: false
G25_store_or_coin_transactions_visible: false
G26_daily_reward_visible: false
G27_reward_wall_or_resting_visible: false
G28_character_info_blessings_premium_visible: false
G29_character_auction_trade_visible: false
G30_world_transfer_main_character_visible: false
G31_generic_economy_confirmation_modal_visible: false
```

No G24-G31 panel is already visible in the current client state. Therefore passive observation cannot advance panel semantics further without changing the current UI state.

## Sensitive-data handling

The raw observation frame showed a login form and was treated as potentially sensitive account UI. Its contents are intentionally not reproduced, quoted, OCRed, committed or retained. The temporary image was deleted from both the container and Synology host immediately after classification.

```yaml
host_capture_deleted: true
container_capture_deleted: true
raw_capture_committed: false
ocr_used: false
credential_value_copied_or_recorded: false
```

## Side effects

```yaml
keyboard_input: false
mouse_input: false
window_activation_for_client_behavior: false
login: false
credentials_used: false
process_signal_or_restart: false
client_memory_access: false
client_memory_write: false
network_mutation: false
transaction_action: false
panel_navigation: false
```

## Exact blocker

The task explicitly has `gui_input_authorized: false` and `login_authorized: false`. Opening any G24-G31 panel from the current LOGIN screen would require changing client/UI/session state. That is outside this read-only admission.

```text
BLOCKER=NO_GUI_INPUT_OR_LOGIN_AUTHORITY_FOR_PANEL_NAVIGATION_FROM_LOGIN_STATE
```

No absence above is converted into a semantic statement that a feature/panel does not exist. It only states that the corresponding UI is not visible in the current passive observation state.
