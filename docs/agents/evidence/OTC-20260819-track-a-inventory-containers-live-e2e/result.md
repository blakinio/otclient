# TIBIA-RE-INVENTORY-CONTAINERS — authenticated passive live result

## Result

This fresh Track A task successfully used the owner's already authenticated official client for **promotion-grade read-only observation** and strengthened D10/D13/D15 with direct current-session facts. It did not send GUI input because the current controller plane cannot legally adopt the already-running unregistered client.

All D09-D22 rows remain `PARTIAL`; no row is promoted to `DONE`.

## Exact live target

```text
container  otclient-track-a-kasmvnc
display    :1
PID        11365
size       52109920
sha256     ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
state      IN_GAME
targets    exactly one client in target; zero competing host-container clients
```

The active-task scan found no competing owner for this KasmVNC surface. The only active Track A task with non-`none` runtime access owns an unrelated `ephemeral_isolated` Xvfb namespace.

## New live evidence

A single passive X11 frame directly showed the world viewport plus equipment/status UI and an open `Backpack` container.

- **D10:** authenticated capacity `410`, soul `100`, HP `155/155`, mana `60/60`, and multiple populated equipment slots are directly visible.
- **D13:** three stack overlays with concrete live counts `50`, `8`, and `7` are directly visible in the open backpack.
- **D15:** one authenticated `Backpack` panel is open with `8` visible slot cells, `6` occupied and `2` empty.

The task does not guess item names/object IDs from icon appearance. D09/D11 gain endpoint correlation only; no message/change event occurred. D16 has no create/change/delete runtime event because no stimulus was sent. D17-D22 interaction-specific semantics remain unobserved in this task.

## Why agent-driven input is blocked

Fresh controller-plane inspection found:

```text
runtime-registration.json = ABSENT
lease generation file      = 16
lease owner                 = completed/released native-login task
lease expiry                = before this preflight
```

Current trusted-main transition code supports only `bootstrap`, `rebind`, and `gate-b`.

- `bootstrap` explicitly fails if any official-client candidate already exists;
- `rebind` requires an existing authoritative registration;
- `gate-b` likewise requires registration.

Therefore the already-running authenticated client cannot currently be converted into a mutation-authorized canonical runtime by any reviewed trusted-main transition. Manually creating/editing `runtime-registration.json`, pretending the stale lease is current, or invoking X11 input directly would violate the Track A contract.

## Safety

No new login, credential access, keyboard/mouse input, gameplay action, item/container movement, process control, debugger/injection, network mutation, or transaction occurred. Temporary raw screenshots and crops were deleted after extracting sanitized text evidence and were never committed/uploaded.

## Programme gate

The next route to real create/change/delete/navigation/stash/depot/Quick-Loot E2E is an explicit **existing-unregistered-runtime reconciliation/adoption transition**: fail-closed exact identity + target uniqueness + current lease/flock authority + atomic registration of the already-running session, independently reviewed and merged before a later invocation uses it. Until that exists, this logged-in session remains valuable for passive observation only.
