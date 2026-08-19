# TIBIA-RE-ECONOMY-PANELS — fresh read-only re-admission v2

Date: 2026-08-19
Task: `OTC-20260819-track-a-economy-panels-runtime-readonly`
Trusted base: `main@08c0b6f89ffddd4c75b8f60060ce3b2a62195d95`
PR head before this evidence: `3eec748dc5e0e7f9306af91e7226c2481a4ed893`

## Authority boundary

```yaml
runtime_access: read_only
mutation_authorized: false
login_authorized: false
credential_use_authorized: false
gui_input_authorized: false
gameplay_authorized: false
process_control_authorized: false
transaction_authorized: false
owner_readonly_window: preserved from prior explicit reconciliation; current owner invocation resumes the same bounded task
```

No permission is inferred for keyboard/mouse input, window-driving activation, login, credentials, process control, gameplay or any economy/account transaction.

## Current trusted exact-client fence

Merged governance PR #555 and closeout #561 establish:

```yaml
version_token: '15.32'
size: 52109920
sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
```

## Fresh Synology/Kasm preflight

Remote Desktop Commander device `Synology` responded to ping. Fresh non-invasive inventory found:

```text
container=otclient-track-a-kasmvnc
image=kasmweb/ubuntu-noble-desktop:1.17.0
container_running=true
container_host_pid=1866
container_started=2026-08-19T06:09:27.336626403Z
restart_policy=unless-stopped
port=127.0.0.1:6901->6901/tcp
DISPLAY=:1
DISPLAY_CONNECT=PASS
dimensions=3440x1229
```

Exactly one official `client` process exists in the intended Kasm container:

```text
PID=17954
START_TICKS=74839161
EXE=/home/kasm-user/otclient-track-a/Tibia-32177065988-1/bin/client
CWD=/home/kasm-user/otclient-track-a/Tibia-32177065988-1/bin
SIZE=52109920
SHA256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
DISPLAY=:1
```

The real top-level Tibia window is:

```text
XID=0x1a00017
_NET_WM_PID=17954
WM_CLASS="client", "Tibia"
WM_NAME="Tibia"
geometry=3440x1174 at X=0 Y=55
```

Two auxiliary windows are not competing full targets:

```text
0x1a00019 name=Tibia size=1x1 _NET_WM_PID=absent WM_CLASS=absent
0x1a00005 name="Qt Selection Owner for client" size=3x3 _NET_WM_PID=absent WM_CLASS=absent
```

Host/container inventory additionally found no `client`/official `/bin/client` process in the native-login relay, Track B global-login lab, or login-analysis containers. PR #475 is released with `runtime_access:none`; PR #528 remains isolated to `native-login-exact-sha-re`; PR #541 owns only Kasm infrastructure under the owner-reconciled shared read-only observation window.

## Admission result

```yaml
target_uniqueness: PROVEN
competing_full_client_candidates: 0
live_exact_client_fence_match: PASS
trusted_base_exact_client_fence_result: PASS
panel_observation_boundary: PASSIVE_ALREADY_VISIBLE_ONLY
```

## Negative controls

```yaml
keyboard_input: false
mouse_input: false
window_activation_for_client_behavior: false
login: false
credentials: false
process_signal_or_restart: false
client_memory_access: false
client_memory_write: false
network_mutation: false
transaction_action: false
panel_navigation: false
```

The next legal operation is a read-only capture/inspection of the already-visible desktop. If the desired G24-G31 panels are not already visible, this task must not open or drive them without a separate authority change.
