# Track A KasmVNC Runtime Access Contract v1

```yaml
track_a_kasmvnc_runtime_access_version: 1
track_id: official-client-re
repository: blakinio/otclient
runtime_platform: official_native_linux_only
purpose: physical_runtime_discovery_and_observation
```

## Purpose

This document tells future Track A agents how to reach the current persistent Linux Tibia desktop when a task genuinely requires physical client testing. It is an operational locator and observation runbook only. It does **not** create runtime ownership, canonical authority, login authority, credential authority, input authority, or mutation authority.

Before any live operation, the worker must still obey the current trusted-base versions of `TIBIA_RESEARCH_TRACKS.md`, `TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`, the canonical-live/bootstrap/rebind contracts, hybrid execution routing, and the current task/PR ownership state. A visible window, reachable KasmVNC page, container name, display number, PID, or previously observed SHA is discovery evidence only.

## Current physical access locator

The owner-designated Track A physical desktop is currently reached through:

```yaml
runner: synology-otclient-01
remote_desktop_commander_device: Synology
remote_host_user: chagpt
container: otclient-track-a-kasmvnc
container_gui_user: kasm-user
display: ':1'
persistent_desktop: KasmVNC
observer_endpoint: https://synology:6902/
container_kasmvnc_port: 6901
container_kasmvnc_host_binding: 127.0.0.1:6901
```

These locators may be changed by maintenance. Revalidate them live at the start of every physical-runtime session; never treat this block as permanent current authority.

## Required read-only access preflight

Use Remote Desktop Commander to connect to the online `Synology` device, then perform only non-invasive discovery first. Equivalent commands are acceptable, but the facts below must be freshly proven before the worker relies on the runtime.

```sh
# Host: prove the intended container exists and is running.
docker ps --filter 'name=^/otclient-track-a-kasmvnc$'
docker inspect -f 'Name={{.Name}} Running={{.State.Running}} Pid={{.State.Pid}} StartedAt={{.State.StartedAt}}' \
  otclient-track-a-kasmvnc

# Container: prove the intended X11 display is alive.
docker exec -u kasm-user -e DISPLAY=:1 otclient-track-a-kasmvnc \
  sh -lc 'xdpyinfo >/dev/null && echo DISPLAY_CONNECT=PASS'

# Container: inspect the window tree without sending input.
docker exec -u kasm-user -e DISPLAY=:1 otclient-track-a-kasmvnc \
  sh -lc 'xwininfo -root -tree | grep -Ei "Tibia|client" || true'
```

If the expected container/display cannot be proven, or multiple plausible official-client targets make uniqueness ambiguous, stop physical targeting and resolve the discrepancy non-destructively. Do not fall back to historical `:98`, `:99`, ports `6082/6083`, an old PID, or another Track A/Track B container merely because it existed before.

## Revalidate the actual official client process

Never reuse a historical PID or SHA. Discover the live official client inside this container and prove its current identity before a test depends on it.

```sh
docker exec otclient-track-a-kasmvnc sh -lc '
  pids=$(pgrep -x client || true)
  printf "CLIENT_PIDS=%s\n" "$pids"
  for pid in $pids; do
    printf "PID=%s\n" "$pid"
    printf "EXE="; readlink -f "/proc/$pid/exe" || true
    printf "CWD="; readlink -f "/proc/$pid/cwd" || true
    stat -Lc "SIZE=%s OWNER=%U:%G MODE=%A MTIME=%y" "/proc/$pid/exe" || true
    sha256sum "/proc/$pid/exe" || true
    tr "\0" "\n" < "/proc/$pid/environ" | grep "^DISPLAY=" || true
  done
'
```

For any state-changing, invasive, login, attach/injection, restart, process-control, or gameplay operation, this process discovery is only preflight. The current task must additionally pass the runtime-admission class and every required Gate A / rebind / Gate B / bootstrap / whole-lifetime-supervisor requirement from trusted-base governance.

## Visual observation

The persistent desktop is intended to remain observable through:

```text
https://synology:6902/
```

A `401` response means the KasmVNC authentication boundary is present; it is not evidence that the Tibia window is absent. Agents must not read, print, copy, commit, or exfiltrate KasmVNC password files or other credentials to bypass that boundary. Use only an already authorized session or access method supplied by the owner/environment.

The X11 desktop can also be captured read-only without interacting with Tibia. The current container has `ffmpeg` with X11 capture support. Determine the current root geometry first instead of hard-coding a historical resolution, then capture one frame, for example:

```sh
docker exec -u kasm-user -e DISPLAY=:1 otclient-track-a-kasmvnc sh -lc '
  geometry=$(xdpyinfo | awk "/dimensions:/{print \$2; exit}")
  test -n "$geometry"
  ffmpeg -hide_banner -loglevel error -y \
    -f x11grab -video_size "$geometry" -i :1 -frames:v 1 /tmp/track-a-observe.png
  stat -c "SCREENSHOT=PASS size=%s" /tmp/track-a-observe.png
'
```

A screenshot is observation evidence only. It does not authorize clicks, keystrokes, login, character selection, or gameplay.

## Input, process control and login are separate permissions

Connecting to the host/container/display or seeing the Tibia window does not authorize mutation. Treat the following as state-changing/invasive and require current task authority plus Track A admission before execution:

- keyboard or mouse injection;
- window activation intended to drive client behavior;
- native-auth invocation or login-form submission;
- reading or using Tibia account credentials, 2FA values, session/auth material, or login Secrets;
- character selection, world entry, relogin or gameplay actions;
- process signals, restart, stop, kill, attach, debugger/instrumentation attach, memory write or injection;
- changing display/VNC configuration, client files, package state, networking, proxy/VPN/WARP state, or canonical registration/lease state.

An owner's current instruction such as **do not log in** is controlling for that invocation and overrides historical login/secret permission. Do not infer standing login authority from a previous task, available environment variables, repository Secrets, an existing authenticated browser/KasmVNC session, or a client window already showing an account state.

## No broad cleanup

Never use broad `pkill`, `killall`, Docker cleanup, display cleanup, volume cleanup, state deletion, or port takeover around this runtime. Target only the exact runtime surface currently owned and admitted by the task. If ownership or uniqueness is uncertain, remain read-only or stop.

## Verified observation snapshot — 2026-08-18

The following was verified non-invasively from the owner-authorized Remote Desktop Commander session and is retained only as evidence that this access route worked at that moment:

```yaml
remote_desktop_commander_device_online: true
container_running: true
display_1_connect: PASS
tibia_window_visible_in_x11_tree: true
tibia_window_geometry_observed: 3440x1174
observer_endpoint_http_status: 401
container_port_mapping_observed: 6901/tcp -> 127.0.0.1:6901
single_frame_x11_capture: PASS
login_performed_by_this_verification: false
client_input_sent_by_this_verification: false
```

Do not reuse this snapshot as current identity or mutation authority. Revalidate the live facts every time.