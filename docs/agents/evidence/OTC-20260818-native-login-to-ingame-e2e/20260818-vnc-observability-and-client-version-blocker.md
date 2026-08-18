# Track A native-login E2E — noVNC observability recovery and client-version blocker

Task: `OTC-20260818-native-login-to-ingame-e2e`  
PR: `#528`  
Date: `2026-08-18`

## Purpose

Preserve the operational findings from the successful recovery of the user-visible noVNC path at `http://synology:6082/` and the first reliable visual diagnosis after that recovery.

This checkpoint is intentionally secret-free. It contains no account identifier, password, OTP, token, cookie, session key, screenshot payload, or other credential material.

## Historical remote-GUI pattern recovered from repository history

The prior successful Track A remote-GUI implementation on branch `ci/track-a-remote-gui-access` established the following presentation chain:

```text
active X11 DISPLAY
  -> x11vnc on the exact active DISPLAY
  -> RFB listener 5901
  -> websockify/noVNC listener 6081
  -> host/container publication or bridge
  -> user endpoint http://synology:6082/
```

The historical `tibia-official-client-re-remote-gui-stdlib.yml` explicitly presented `http://synology:6082` while running `x11vnc` on `5901` and `websockify` on `6081`. Therefore port `6082` is a presentation/publication layer, not the X11 display itself and not the direct x11vnc backend.

## Current gen16 diagnosis

The first repair attempt correctly re-proved current authority and runtime identity but used `xdotool search --pid` as an additional visibility check. That check failed even though same-generation Gate B had just passed. This reproduced the already-known class of `xdotool --pid` ownership/visibility ambiguity and was not accepted as evidence that the Tibia window was absent.

The replacement v2 workflow used the canonical raw XRes/X11 ownership proof instead.

Workflow:

```text
run: 32138989357
job: 95717041668
```

Exact results:

```text
TRACK_A_CANONICAL_GATE_B=PASS
TRACK_A_CANONICAL_LEASE_GENERATION=16
VNC_V2_ACTIVE_DISPLAY=:99
VNC_V2_ACTIVE_PID=30067
VNC_V2_RAW_XRES_WINDOW=12582929
VNC_V2_RAW_XRES_VIEWABLE_1920X1080=true
VNC_V2_CANONICAL_ENDPOINT=127.0.0.1:6082
VNC_V2_CANONICAL_MAPPING=PROVEN
VNC_V2_HOST_6082_TO_CONTAINER_6081=false
```

This proved that the official client window was genuinely present and viewable on the active canonical X server:

```text
DISPLAY=:99
PID=30067
XID=12582929
geometry class=VIEWABLE 1920x1080
ownership=raw XRes -> exact client PID
```

The same workflow then replaced only stale dedicated observability listeners on ports `5901` and `6081` and rebuilt the viewer path for the current display:

```text
VNC_V2_REPLACE_STALE_5901=true
VNC_V2_REPLACE_STALE_6081=true
VNC_V2_RFB=PASS
VNC_V2_WEBSOCKET=PASS
VNC_V2_SECRET_ACCESS=false
VNC_V2_AUTH_MUTATION=false
VNC_V2_CLIENT_RESTART=false
VNC_V2_RESULT=PASS
```

The important discriminator was:

```text
VNC_V2_HOST_6082_TO_CONTAINER_6081=false
```

So the black screen observed at `synology:6082` did **not** prove that the client or X11 window was absent. The active client was healthy and viewable on `:99`; the stale/wrong presentation path was the problem.

After the viewer repair, the operator visually confirmed that `http://synology:6082/` again presented the live Tibia client.

## First reliable visual blocker after observability recovery

Once the live client became visible, the client displayed an `Info` dialog with the message:

```text
Your client version is too old.
Restart Tibia to update your client.
```

No account identifier from the visible login form is copied into this evidence.

### FACT

The currently admitted exact binary is still the previously pinned client:

```text
version=15.32.df7b29
size=51965216
sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

The live UI now explicitly reports that this client version is too old and requires an update.

### Consequence

The current `character_list_count=0` after native credential dispatch must not be treated as evidence of a wrong password, missing 2FA, or failed secret delivery. The client has an explicit version gate visible in the real runtime. Further credential retries against this exact old binary would be unproductive and would weaken causal reasoning.

The next legitimate path is:

```text
preserve/record current gen16 evidence
 -> update the official client through the legitimate launcher/update path
 -> identify and fence the new exact version / size / SHA-256
 -> re-prove native QMeta/vptr/offset contracts for the new binary
 -> rebuild/revalidate the native-auth helper against that exact binary
 -> only then perform another bounded secret-bearing authentication attempt
```

Do **not** blindly reuse the 15.32 offsets, vptr addresses, QMeta assumptions, helper binary, or exact-SHA fences after the client update.

## Permanent noVNC recovery rule

For future Track A agents, use this order whenever `synology:6082` is black or stale:

```text
1. Validate current lease/task/session and same-generation Gate B.
2. Read the current canonical registration for DISPLAY, PID and XID.
3. Prove the exact client window with raw XRes/X11 ownership.
4. Do not use `xdotool --pid` failure as authoritative proof that the window is absent.
5. Bind x11vnc to the exact active DISPLAY.
6. Verify the RFB backend handshake.
7. Bind websockify/noVNC to that RFB backend and verify WebSocket 101.
8. Verify the host/container publication path used by `synology:6082`.
9. Replace only dedicated stale VNC/websockify listeners; never broad-pkill unrelated processes.
10. Re-run Gate B after observability-only mutation.
11. Keep Secrets/auth untouched during VNC repair.
```

A black noVNC page is therefore a **presentation symptom**, not sufficient evidence about client-window existence, client health, authentication state, or X11 ownership.

## Terminal checkpoint

```text
VNC_OBSERVABILITY=RESTORED
ACTIVE_DISPLAY=:99
ACTIVE_CLIENT_PID=30067
ACTIVE_WINDOW_XID=12582929
RAW_XRES_WINDOW_PROOF=PASS
USER_VISIBLE_CLIENT=CONFIRMED
CLIENT_VERSION_BLOCKER=PROVEN_BY_LIVE_UI
CLIENT_UPDATE_REQUIRED=true
SECRET_RETRY_BEFORE_UPDATE=false
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=NO
```
