# Track A noVNC display diagnostic — runner probe

Task: `OTC-20260815-track-a-novnc-display-diagnostic`  
Draft PR: `#309`  
Branch: `research/OTC-20260815-track-a-novnc-display-diagnostic`  
Probe head: `fe57c76db37056f3df0e66b5c6bcb71f96565d3b`  
Workflow run: `31903692616`  
Job: `95058202023`  
Runner: `synology-otclient-01`

## Objective

Determine whether the owner's browser endpoint `synology:6082` can be mapped read-only to a concrete X11 display, and compare the observed display state with Track A PR #303's isolated `:115` runtime.

## FACT — probe result

The bounded read-only workflow completed successfully as a diagnostic. It did not launch or signal the Tibia client, use credentials, restart an X/VNC service, control Docker, or touch Track B.

Sanitized markers from the exact job:

```text
TRACK_A_NOVNC_DIAGNOSTIC_RUNNER_VERIFIED=true
SYNLOGY_HOSTNAME_RESOLVED=false
SYNLOGY_RESOLVE_ERROR_CLASS=gaierror
NOVNC_HTTP_REACHABLE=false
NOVNC_HTTP_ERROR_CLASS=URLError
WEBSOCKIFY_RFB_PROBE_COMPLETE=false
WEBSOCKIFY_RFB_ERROR_CLASS=gaierror
X11_SOCKET_DISPLAY_COUNT=1
X11_SOCKET_DISPLAYS=:98
XDPYINFO_AVAILABLE=true
X11_DISPLAY_98_QUERY=unavailable
DIRECT_RFB_DISPLAY_88_REACHABLE=false
DIRECT_RFB_DISPLAY_98_REACHABLE=false
DIRECT_RFB_DISPLAY_115_REACHABLE=false
TRACK_A_NOVNC_READONLY_PROBE_COMPLETE=true
```

### Proven boundaries

- The dedicated runner job cannot resolve the LAN hostname `synology`; therefore it cannot directly reach or identify the backend of the owner's `synology:6082` browser endpoint from this network namespace.
- Exactly one X11 Unix socket was visible in the runner namespace at probe time: `:98`.
- No `:88` or `:115` X11 Unix socket was present at probe time.
- `xdpyinfo` exists but could not query `:98` from this job. Socket presence alone therefore does not establish that this job has usable X authorization/access to the display.
- The conventional direct-RFB markers for displays 88, 98 and 115 are not evidence that the LAN host ports are closed, because hostname resolution failed before those host-side tests could establish a connection.

## Verified historical comparison

PR #303 evidence and the direct historical job log independently establish that the known-good exact-client runtime used persistent `TRACK_DISPLAY=:98` on `synology-otclient-01`.

Historical positive control:

```text
run=31730884814
attempt=14
job=94785048338
TRACK_DISPLAY=:98
TRACK_A_SOFTWARE_BACKEND_CLIENT_RUNNING=true
TRACK_A_KNOWN_GOOD_LOGIN_CLICK_SENT=true
TRACK_A_POST_LOGIN_CHANGED_PIXELS=466099
TRACK_A_FIRST_CHARACTER_ACTIVATION_SENT=true
TRACK_A_WORLD_CHANGED_PIXELS=660094
TRACK_A_LOCAL_SOCKS_ESTABLISHED=7
TRACK_A_DIRECT_ESTABLISHED=0
TRACK_A_UDP_SOCKET_COUNT=0
TRACK_A_PROBABLE_WORLD_VIEW_RENDERED=true
TRACK_A_SESSION_LEFT_RUNNING=true
```

PR #303's fresh isolated display `:115` later failed before login with `client_gen_1_window_missing` and `visible_window_count=0`. Its task-owned `:115` display is cleaned after failed runs, which is consistent with `:115` being absent during this later read-only probe.

## Classification

### FACT

The historical working Track A client path is verified on `:98`; the current fresh reacquisition path is verified as using transient `:115` and currently fails to create a visible Tibia window.

### INFERENCE — high confidence

Because `:98` is both the verified historical positive-control display and the only persistent X11 socket visible in the dedicated runner namespace, it is the strongest current candidate for the persistent GUI that the owner expects to observe.

### UNKNOWN

`6082 -> :98` is **not proven**. The exact noVNC/websockify backend mapping remains unknown because the browser-facing LAN hostname/service is outside the network namespace reachable by this GitHub Actions runner and the repository contains no canonical `6082` mapping.

The owner's earlier observation involving `:88` also remains unverified in current canonical repository/runtime evidence.

## Blocker and next action

A read-only host-side observation is required from the Synology host/LAN namespace: identify the listener/process/config backing TCP `6082`, then read its websockify/RFB target and map that target to the corresponding X display. Do not restart, signal or reconfigure any VNC/X11/runtime process while doing so.
