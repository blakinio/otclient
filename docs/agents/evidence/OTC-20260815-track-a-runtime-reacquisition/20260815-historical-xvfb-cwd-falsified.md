# Track A RUNTIME — historical Xvfb cwd discriminator falsified

Task: `OTC-20260815-track-a-runtime-reacquisition`  
Run: `31893122418`  
Job: `95032257726`  
Head: `4cb98e0b149a5eae21261be468618ec269a8a976`  
Artifact: `9249089941`  
Artifact SHA-256: `ed6c4adc716bcd46236e8fd497e172de7404e22b72a6165e6a009e3920119f59`  
Runner: `synology-otclient-01`

## Hypothesis

Historical successful software-world login attempts used the persistent Track A Xvfb after it had originally been launched from `$toolroot/usr/bin`. Because that private Xvfb binary had historical `/usr/bin\0 -> .\0` patching, run #29 changed only the task-owned Xvfb bootstrap cwd to the historically proven `$toolroot/usr/bin` cwd while preserving the isolated display `:115` and the existing exact-client, WARP/SOCKS, HOME/package, software-backend and cleanup fences.

## FACT

The run established:

```text
TRACK_A_RUNTIME_XVFB_BOOTSTRAP_CWD=/work/_otclient_tibia_re_state/toolroot/usr/bin
TRACK_A_UPSTREAM_WARP_VERIFIED=true
TRACK_A_EXACT_CLIENT_VERIFIED size=51965216 sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_TASK_SOCKS_RELAY_VERIFIED=true port=25415
TRACK_A_TASK_XVFB_VERIFIED=true display=:115
TRACK_A_RUNTIME_PHYSICAL_CANONICAL_PACKAGE_READY generation=1 .../home-gen-1/.local/share/CipSoft GmbH/Tibia/packages/Tibia
TRACK_A_RUNTIME_PHYSICAL_CANONICAL_PACKAGE_LAUNCH generation=1 .../home-gen-1/.local/share/CipSoft GmbH/Tibia/packages/Tibia
TRACK_A_CREDENTIAL_ENV_CLEAR role=client-gen-1 pid=8433
TRACK_A_RUNTIME_ERROR=client_gen_1_window_missing
TRACK_A_RUNTIME_CURRENT_RUN_CLEANUP_COMPLETE=true
```

The sanitized display-wide X11 artifact contained:

```text
visible_window_count=0
```

The client log reached asset loading and proxied public Tibia HTTP requests, but no visible X11 window was created. It also recorded Qt/XCB/OpenGL-context warnings and a cross-thread QQmlEngine/QSGSoftwareRenderThread warning. Those lines are diagnostics only; this run does not assign them root-cause status.

Protected login, generation 2, movement and all gameplay/economic actions were skipped. Task-owned cleanup completed.

## Classification

### DISPROVEN / SUPERSEDED

Changing only the fresh task-owned Xvfb launch cwd to the historically proven `$toolroot/usr/bin` cwd is insufficient to reproduce the historical visible-window path. Do not repeat this discriminator unchanged.

### STILL UNKNOWN

- why the historical persistent Xvfb `:98` produces a visible exact-client window while freshly provisioned task-owned `:115` does not;
- whether an allowlisted Xvfb runtime-environment/process-state difference is causal;
- whether task-local HOME state beyond the already bounded launcher/package surface is required;
- structural `IN_GAME`, restart/relogin reacquisition, bridge session epoch, A3 and A4.

## Next bounded discriminator

Before changing any renderer/client option, compare only **allowlisted, non-secret process metadata** for the currently live historical Track A Xvfb `:98` (if it still exists and its Track A ownership marker is verifiable) against fresh task-owned `:115`:

- executable path/hash;
- command line;
- cwd;
- selected environment keys only: `HOME`, `PATH`, `LD_LIBRARY_PATH`, `XKB_CONFIG_ROOT`, `XDG_DATA_DIRS`;
- X11 socket/lock presence and process age/start-time metadata.

Do not dump the full environment and do not signal, restart or mutate `:98`. If `:98` is absent or ownership cannot be verified, record that prerequisite as UNKNOWN and do not infer a difference.
