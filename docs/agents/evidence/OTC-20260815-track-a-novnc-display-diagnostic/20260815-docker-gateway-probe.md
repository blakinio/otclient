# Track A noVNC Docker-gateway probe

Task: `OTC-20260815-track-a-novnc-display-diagnostic`  
PR: `#309`  
Head tested: `dff39e99d4669229a66826e5f51805a95be10185`  
Run: `31904447945`  
Job: `95059984786`  
Runner: `synology-otclient-01`

## Objective

Test a materially new, read-only access path from the dedicated runner container to the browser-facing noVNC service by deriving the container's default IPv4 gateway from `/proc/net/route` without printing the private address, then probing only TCP/HTTP/WebSocket port `6082`.

No Docker API/control, host namespace entry, process inspection, signal, restart, client launch, login, credential use, VNC password, gameplay or Track B access was used.

## FACT

The diagnostic workflow completed successfully and established:

```text
DOCKER_DEFAULT_GATEWAY_FOUND=true
DOCKER_GATEWAY_TCP_6082_REACHABLE=true
DOCKER_GATEWAY_NOVNC_HTTP_RESPONSE=true
DOCKER_GATEWAY_NOVNC_HTTP_STATUS=200
DOCKER_GATEWAY_WEBSOCKIFY_UPGRADE_STATUS=101
DOCKER_GATEWAY_WEBSOCKIFY_REACHABLE=true
DOCKER_GATEWAY_RFB_PROTOCOL_VERSION=003.008
DOCKER_GATEWAY_RFB_SECURITY_NONE_AVAILABLE=true
DOCKER_GATEWAY_RFB_SECURITY_VNC_AUTH_AVAILABLE=false
DOCKER_GATEWAY_RFB_AUTH_REQUIRED=false
DOCKER_GATEWAY_RFB_SECURITY_RESULT=0
DOCKER_GATEWAY_RFB_FRAMEBUFFER_WIDTH=1920
DOCKER_GATEWAY_RFB_FRAMEBUFFER_HEIGHT=1080
DOCKER_GATEWAY_RFB_DISPLAY_HINT=unknown
DOCKER_GATEWAY_RFB_DESKTOP_NAME_HAS_X11_TOKEN=false
DOCKER_GATEWAY_WEBSOCKIFY_RFB_PROBE_COMPLETE=true
X11_SOCKET_DISPLAY_COUNT=1
X11_SOCKET_DISPLAYS=:98
X11_DISPLAY_98_QUERY=unavailable
```

The hostname `synology` still did not resolve in the runner namespace, but bypassing DNS through the runner container's default gateway reached an HTTP service at port `6082`, accepted the noVNC `/websockify` WebSocket upgrade, and completed an unauthenticated RFB 3.8 handshake. The service advertises a `1920x1080` framebuffer.

## Classification

### PROVEN

- The dedicated runner container has a default IPv4 gateway.
- TCP `6082` on that gateway is reachable from `synology-otclient-01`.
- Port `6082` serves the expected noVNC/websockify/RFB protocol surface: HTTP `200`, WebSocket `101`, RFB `003.008`.
- The RFB endpoint requires no VNC authentication for the metadata handshake used here.
- Its advertised framebuffer is `1920x1080`.
- At the same probe time, exactly one X11 Unix socket was visible in the runner namespace: `:98`.

### INFERENCE — high confidence

The gateway endpoint is the same Synology-host noVNC service the owner reaches as `synology:6082`: it is reached on the runner's host-facing default gateway at the same port and presents the expected noVNC/websockify/RFB stack. This avoids dependence on LAN DNS while preserving the browser host header `synology:6082`.

`:98` remains the strongest candidate for the VNC-served GUI because:

1. historical positive-control Track A run `31730884814` attempt 14 / job `94785048338` used `TRACK_DISPLAY=:98`, produced a visible Tibia window and rendered a probable world view;
2. the current persistent X11 socket inventory contains only `:98`;
3. the noVNC RFB endpoint advertises `1920x1080`, matching the historically successful `:98` Xvfb profile recorded in PR #303 evidence.

### UNKNOWN

`6082 -> :98` is still not directly proven. The RFB desktop name exposes neither an X11 token nor a numeric display hint, and this runner namespace cannot successfully query `:98` with `xdpyinfo`. The noVNC/RFB server could theoretically live in a different namespace while presenting the same framebuffer dimensions.

The owner's earlier `:88` observation remains unverified in current canonical evidence.

## Comparison with failing fresh runtime

PR #303's isolated runtime uses task-owned `DISPLAY=:115`. Its latest verified failure remains `client_gen_1_window_missing` with `visible_window_count=0`. The historical positive control on persistent `:98` created the expected visible client window. The gateway probe therefore strengthens the case that the black browser view belongs to the persistent noVNC environment rather than to PR #303's ephemeral `:115`, but it does not provide the final display-number binding.

## Exact next action

The remaining proof requires one read-only host-side discriminator unavailable from the runner container namespace: identify the process/listener/config that owns host TCP `6082` and read its websockify/RFB target (for example the target VNC port/display) without restarting, signalling, authenticating to, or reconfiguring any VNC/X11/runtime process.
