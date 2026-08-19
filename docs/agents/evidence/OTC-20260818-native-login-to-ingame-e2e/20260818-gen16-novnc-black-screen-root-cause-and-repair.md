# Gen16 noVNC black-screen root cause and repair

Date: 2026-08-18
Task: `OTC-20260818-native-login-to-ingame-e2e`
Branch: `runtime/OTC-20260818-native-login-to-ingame-e2e-v3`

## Purpose

Persist the verified operational finding from the gen16 remote-view incident so future agents do not misdiagnose a black noVNC canvas as proof that the Tibia client has no visible X11 window.

## Verified facts

The active canonical runtime remained healthy during the incident:

- lease generation: `16`;
- active display: `:99`;
- active client PID: `30067`;
- canonical window identity: `x11-window:12582929`;
- canonical remote-view endpoint: `127.0.0.1:6082`;
- canonical remote-view mapping field: `PROVEN`;
- Gate B passed before and after the VNC repair;
- client restart was not required;
- no authentication mutation was performed;
- no credential Secret was read by the VNC repair path.

Raw XRes ownership validation proved that XID `12582929` was a `VIEWABLE` `1920x1080` window owned by the exact client PID `30067` on `DISPLAY=:99`.

The earlier `xdotool search --onlyvisible --pid ... --name '^Tibia$'` probe failed to find the window even though the canonical raw XRes proof succeeded. Therefore `xdotool --pid` must not be treated as authoritative window-ownership evidence for this runtime.

## Root cause

The black screen was a presentation-path problem, not evidence that the client had no renderable window.

The fresh viewer backend was healthy:

- `x11vnc` on `DISPLAY=:99` -> `127.0.0.1:5901`: PASS;
- `websockify` -> `0.0.0.0:6081` -> `127.0.0.1:5901`: PASS;
- RFB banner probe: PASS;
- WebSocket upgrade probe: PASS.

The critical mismatch was:

`VNC_V2_HOST_6082_TO_CONTAINER_6081=false`

In other words, the historical user-facing endpoint `http://synology:6082/` was not mapped to the newly verified runner-side `6081` presentation service. A black canvas on `6082` could therefore come from a stale or different presentation path even while the active Tibia window on `:99` was valid and viewable.

## Canonical diagnostic order for future incidents

When the noVNC page loads but shows black content, do not restart the client and do not assume that the X11 window is absent.

Use this order:

1. Validate canonical lease/runtime ownership and run Gate B.
2. Read the registered `display`, `pid`, `window_identity`, `remote_view_endpoint`, and `remote_view_mapping` from canonical runtime state.
3. Verify the X socket for the registered display and `kill -0` the registered client PID.
4. Resolve the registered XID through the repository raw XRes helper and require exact PID ownership plus the expected viewable geometry. Prefer:
   - `.github/scripts/tibia-official-client-re-xres-window-owner.py`
   - `.github/scripts/tibia-official-client-re-xres-wire.py`
5. Do not use `xdotool --pid` as the ownership authority when it disagrees with raw XRes.
6. Verify each presentation layer independently:
   - X11 display -> `x11vnc` RFB listener;
   - RFB listener -> `websockify` WebSocket endpoint;
   - runner/container websockify port -> host/user-facing port.
7. Only replace listeners on the dedicated historical viewer ports after resolving their owners and refusing unrelated processes.
8. Preserve the client process, XID, display, authentication state, and canonical runtime authority.
9. Re-run Gate B after repair.

## Known-good historical topology

A previously successful Track A remote-view setup used the following layered topology:

`Tibia/X11 DISPLAY -> x11vnc:5901 -> websockify:6081 -> host-facing synology:6082`

The public/user-facing port is therefore not necessarily the same process or socket as the runner-side websockify listener. Future agents must validate the final host mapping explicitly instead of inferring it from a healthy `6081` listener.

## Evidence runs

- Initial gen16 VNC repair run: `32138756835` / job `95716305700`.
  - Gate B PASS.
  - Confirmed `DISPLAY=:99`, PID `30067`, XID `12582929`.
  - Failed at the non-authoritative `xdotool --pid` visible-window check.
- Raw-XRes repair v2 run: `32138989357` / job `95717041668`.
  - Gate B PASS before repair.
  - `VNC_V2_ACTIVE_DISPLAY=:99`.
  - `VNC_V2_ACTIVE_PID=30067`.
  - `VNC_V2_RAW_XRES_WINDOW=12582929`.
  - `VNC_V2_RAW_XRES_VIEWABLE_1920X1080=true`.
  - `VNC_V2_HOST_6082_TO_CONTAINER_6081=false`.
  - stale dedicated `5901` and `6081` listeners replaced safely.
  - RFB PASS.
  - WebSocket PASS.
  - Gate B PASS after repair.
  - `VNC_V2_SECRET_ACCESS=false`.
  - `VNC_V2_AUTH_MUTATION=false`.
  - `VNC_V2_CLIENT_RESTART=false`.
  - `VNC_V2_RESULT=PASS`.

## Operational rule

A black noVNC screen is not sufficient evidence of an absent Tibia window. Prove the window independently with canonical raw XRes ownership, then prove the remote-view chain layer by layer through the host-facing endpoint.
