# V6 terminal pre-login Xvfb/WSLg evidence

Run `33317265138`, attempt 1, live job `99272880272`, trigger comment `5469298617`, trusted main `5def12f5fbb5f3554b60b894df7257f00dcd39f3`.

## Passed gates

- schema-v3 clean guest provenance and exact seed modes/hashes PASS;
- trusted-main live admission PASS;
- official-launcher seed materialization 8732/8732 PASS;
- one-time owner authorization consumption PASS;
- secret wrapper scrubbed exported credential variables before sourcing the runtime helper;
- task WARP gate PASS.

## Terminal failure

Capture failed with `TRACK_A_FIELD6_RUNTIME_ERROR=xvfb_socket_missing`. The helper ordering is `start_xvfb` -> `start_client` -> `wait_window` inside `prepare()`, and `run()` invokes `prepare` before `submit_login_once`. Therefore the failure occurred before `start_client`, before credential typing and before the login click.

Authoritative terminal state:

```yaml
physical_action_count: 0
login_submit_count: 0
FIELD6_VALUE: UNKNOWN
owner_authorization_consumed: true
official_client_started: false
credentials_typed_into_gui: false
login_button_clicked: false
character_selection: false
world_entry: false
gameplay: false
network_payload_capture: false
```

Package cleanup passed. Ephemeral runner removed `.credentials` and `.runner`, deregistered, and exact `OTClientV6Clean` was destroyed after registry/BasePath proof. V6 must never be rerun.

## Root cause

Direct post-run guest readback proved `/tmp/.X11-unix` was a WSLg tmpfs mount with options `ro,relatime`. Xvfb ran as the unprivileged runner and could not create `/tmp/.X11-unix/X131`; its process remained alive until the bounded socket wait expired. This is a WSLg X11 socket namespace collision, not a Tibia/login/protocol failure.
