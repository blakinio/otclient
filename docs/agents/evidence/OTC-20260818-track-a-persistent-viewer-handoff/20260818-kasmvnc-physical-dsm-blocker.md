# KasmVNC physical deployment checkpoint — DSM 502

Date: 2026-08-18
Task: `OTC-20260818-track-a-persistent-viewer-handoff`
PR: #541

## Verified physical facts

The scheduler/runner issue is resolved. `synology-otclient-01` accepts jobs selected by `[otclient, synology]`; runner group is `Default`.

KasmVNC image:

- `kasmweb/ubuntu-noble-desktop:1.17.0`
- image ID `sha256:d5b39699993adf242896c017080b60f81178973eac31ecf4ac263a3c7584490b`
- repo digest `sha256:26da4f4c0ae5e713f5b6830e744b5ddc837a207b554dbe234cb2dc42f9aa15b4`

Persistent container `otclient-track-a-kasmvnc` exists and is reused across workflow generations. Its identity is stored in the task-private state directory. KasmVNC `Xvnc` is running, `DISPLAY=:1`, `/tmp/.X11-unix/X1` exists, and the container listens on `0.0.0.0:6901`.

Run `32168348502`, job `95813250884` proved the earlier `127.0.0.1:6901` connection-refused result was a test-namespace error: the GitHub runner itself is containerized, so runner-container loopback is not Docker-host loopback. A `--network host` helper directly sharing the Docker daemon host network namespace returned KasmVNC's expected unauthenticated HTTP `401` from `https://127.0.0.1:6901/`. The same job also proved authenticated Kasm content from inside the Kasm container. Therefore:

```text
KASMVNC_HTTPS_BACKEND=PASS
KASMVNC_DOCKER_HOST_LOOPBACK=PASS
KASMVNC_DESKTOP_PROCESS=PASS
```

This is consistent with Docker's documented semantics: publishing `127.0.0.1:6901:6901` binds the service to Docker-host loopback, while a separate container has a separate loopback namespace unless it uses host networking.

## Current blocker

Run `32168604262`, job `95814074520` again passed the Kasm process and Docker-host-loopback backend gate, then reached the configured DSM frontend using the source hostname with explicit local resolution:

```text
https://synology:6902/ -> 192.168.1.2:6902
```

DSM returned HTTP `502` before the public WebSocket test could execute.

Thus the current physical boundary is:

```text
Kasm container/Xvnc                    PASS
Kasm HTTPS inside container            PASS
Docker-host 127.0.0.1:6901 HTTPS       PASS
loopback-only Docker publication       PASS
persistent container identity          PASS
DSM source https://synology:6902       REACHABLE_BUT_502
DSM -> Kasm upstream                    FAIL
DSM WebSocket                           NOT_REACHED
```

The repository contract deliberately does not mutate DSM global Reverse Proxy configuration. Owner action is required on the DSM rule before physical E2E can complete. The required rule remains exactly:

```text
SOURCE      HTTPS / synology / 6902
DESTINATION HTTPS / 127.0.0.1 / 6901
WebSocket   enabled
```

Because KasmVNC is serving HTTPS on host loopback now, an HTTP destination or stale/mismatched destination can produce a DSM 502. Save/reapply the exact rule and ensure no conflicting source rule owns `synology:6902`.

No Kasm password, Tibia credential, canonical lease capability or session secret is recorded here or in CI output.

## Resume condition

After the DSM rule is corrected/re-saved, create a fresh exact-head deploy generation and require all of:

- Docker-host loopback backend PASS;
- authenticated DSM HTTPS Kasm page PASS;
- Kasm backend WebSocket 101 PASS;
- DSM WebSocket 101 PASS;
- independent post-deploy persistence audit PASS;
- hosted controller-handoff/raw-XRes/audit PASS;
- exact-head `CI / Required` PASS.
