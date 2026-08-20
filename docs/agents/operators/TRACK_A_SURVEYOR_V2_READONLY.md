# Track A Surveyor v2 read-only operator

The trusted workflow `.github/workflows/track-a-surveyor-v2-readonly.yml` performs one bounded passive Surveyor v2 snapshot on `synology-otclient-01`.

It is not login authority or runtime mutation authority. The workflow:

- requires owner actor `blakinio` and exact workflow-dispatch phrase `ONE_SHOT_SURVEYOR_READ_ONLY`;
- requires the caller to name the current/existing Track A runtime task whose runtime may be observed;
- refuses an active canonical lease owned by a different task;
- inventories all running Docker containers for the exact current native-Linux client fence and requires exactly one candidate globally;
- requires exactly one visible Tibia X11 window owned by that exact PID on the designated KasmVNC display;
- validates an existing canonical registration against the fresh PID/start/size/SHA/display identity when present;
- emits the Track A `read_only` admission record before semantic collection and keeps `mutation_authorized=false`;
- optionally checks the current native-helper bridge only after Unix `SO_PEERCRED` proves the socket peer is the exact target PID;
- performs only three read-only `DISCOVER` calls to classify structural in-game state as `PASS`, `NO`, or `UNKNOWN`;
- runs merged Surveyor v2 `--collect-all`, requires `privacy-scan.json = PASS`, and uploads only that sanitized bundle;
- never loads GitHub Secrets and has no keyboard/mouse, login, character-selection, process-control, signal, injection, memory-write, network-mutation, item or economy step.

A workflow result of `OWNER_LOGIN_REQUIRED=YES` is valid only when `COLLECTOR_READY=YES` and the current structural helper produced a successful scan proving `BRIDGE_NOT_3_OF_3`. `UNKNOWN` never requests owner login. `OWNER_LOGIN_REQUIRED=NO` means a current exact-peer `BRIDGE_3_OF_3` observation can be reused.

The runtime task, lease/registration identity and exact target are re-evaluated on every dispatch. Historical run IDs, PIDs, displays or prior `IN_GAME` state are discovery context only.
