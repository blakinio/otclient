# Track A Surveyor v2 read-only operator

The trusted workflow `.github/workflows/track-a-surveyor-v2-readonly.yml` performs one bounded passive Surveyor v2 snapshot on `synology-otclient-01`.

It is not login authority or runtime mutation authority. The workflow:

- requires owner actor `blakinio` and exact workflow-dispatch phrase `ONE_SHOT_SURVEYOR_READ_ONLY`;
- requires the caller to name the current/existing Track A runtime task whose runtime may be observed;
- refuses an active canonical lease owned by a different task;
- scopes observation to the declared Track A runtime container `otclient-track-a-kasmvnc`; it requires exactly one `client` PID there, exact current size/SHA and matching X11 ownership, and never enumerates or executes discovery commands in unrelated Docker containers;
- requires exactly one visible Tibia X11 window owned by that exact PID on the designated KasmVNC display;
- validates an existing canonical registration against the fresh PID/start/size/SHA/display identity when present;
- emits the Track A `read_only` admission record before semantic collection and keeps `mutation_authorized=false`;
- optionally checks the current native-helper bridge only after Unix `SO_PEERCRED` proves the socket peer is the exact target PID;
- performs only three read-only `DISCOVER` calls as structural object-presence diagnostics; these calls do not classify gameplay state;
- runs merged Surveyor v2 `--collect-all`, requires `privacy-scan.json = PASS`, and uploads only that sanitized bundle;
- never loads GitHub Secrets and has no keyboard/mouse, login, character-selection, process-control, signal, injection, memory-write, network-mutation, item or economy step.

The current helper cannot decide `OWNER_LOGIN_REQUIRED` or `STRUCTURAL_IN_GAME`. A 2026-08-20 read-only regression observed the visible login form while the exact bridge peer still returned one validated `player_protocol_handler`, `gameserver_game_session`, and `worldmap_handler`. Therefore `BRIDGE_3_OF_3` means only `STRUCTURAL_OBJECTS_PRESENT`; the workflow must emit `STRUCTURAL_IN_GAME=UNKNOWN` and `OWNER_LOGIN_REQUIRED=UNKNOWN` until a separately reviewed semantic/causal discriminator or a bounded independent visual observation proves the current state. Raw credential-bearing screenshots are not retained as evidence.

The runtime task, lease/registration identity and exact declared target are re-evaluated on every dispatch. `target_uniqueness=PROVEN` is explicitly scoped to the declared Track A runtime namespace, not to every Docker container on the shared host. Historical run IDs, PIDs, displays or prior `IN_GAME` state are discovery context only.
