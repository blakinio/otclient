# OTCLIENT-TIBIA-RE imported historical login/recovery evidence

## Purpose

Persist the material non-OCR official Linux Tibia login/world-entry recovery evidence from the historical `blakinio/Oteryn-Platform` analysis inside the canonical `blakinio/otclient` programme.

This is imported **read-only provenance**, not an instruction to reuse the historical Oteryn runner/container. New execution belongs on the dedicated OTClient runner.

## Source provenance

```yaml
source_repository: blakinio/Oteryn-Platform
source_branch: ops/oteryn-tibia-client-analysis-20260811
source_pr: 1006
source_task: docs/agents/tasks/active/OTERYN-20260811-tibia-client-analysis.md
historical_runner: oteryn-synology-staging
historical_container: oteryn-tibia-client-analysis
historical_display: :99
historical_client_path: /data/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client
```

The runner/container/path above are historical evidence only and must not be used as active `OTCLIENT-TIBIA-RE` runtime dependencies.

## Exact researched client

```yaml
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

All fixed geometry and static offsets below are tied to this exact researched client/runtime. Reverify current upstream identity before reuse.

## Non-OCR login/world entry — PROVEN historically

Historical workflow:

```text
.github/workflows/tibia-client-analysis-cv-world-entry.yml
introduced_at: bd0bb114b8f812d849228ae325f8a5e2d71f6d62
```

Successful evidence:

```yaml
run: 31620129239
attempt_1_job: 94192583991
attempt_2_job: 94202682934
attempt_2_result: success
```

Attempt 2 proved:

```text
CLIENT_LOCAL_SOCKS_MAX=7
CLIENT_DIRECT_TCP_SEEN=0
CLIENT_UDP_SEEN=0
CLIENT_SUSTAINED_TUNNELED_SESSION=1
CONTROLLED_MOVE_ACTION_PROVEN=true
PHYSICAL_WORLD_SESSION_AND_ACTION_PROVEN=true
VIEWPORT_CHANGED_PIXELS_AFTER_RIGHT=117976
```

A Left input was then sent to return toward the starting tile. The historical workflow intentionally left the client process alive after success.

A subsequent active-session check found a surviving session with:

```text
ACTIVE_LOCAL_SOCKS_COUNT=2
ACTIVE_DIRECT_TCP_COUNT=0
```

Related active-session job:

```text
94203489987
```

That job is `PASS_WITH_SEMANTIC_LIMIT`: it proved the surviving tunneled session but did **not** prove a private-message delivery outcome.

## Historical WARP/runtime path

The proven network path was:

```text
client
-> proxychains4
-> SOCKS5 127.0.0.1:25344
-> wireproxy/userspace Cloudflare WARP
-> Tibia
```

Before credential use, `curl --socks5-hostname 127.0.0.1:25344 .../cdn-cgi/trace` had to prove `warp=on`.

The official client launched successfully on Xvfb `:99` with software Vulkan/lavapipe and exposed a `1020x650` Tibia window in that exact runtime.

## Historical fixed-coordinate recovery geometry

For the exact `1020x650` layout:

```yaml
email_field: [535, 275]
password_field: [535, 304]
login_button: [590, 388]
first_character_row: [285, 193]
login_transition_changed_pixel_threshold: 45000
```

The bounded sequence was:

1. resolve the current largest visible `^Tibia$` window from the live client PID;
2. require the expected `1020x650` geometry before using these historical coordinates;
3. click email, Ctrl+A, type email;
4. click password, Ctrl+A, type password;
5. click Login;
6. immediately unset secret variables in the bounded login step;
7. detect a material transition away from the login form using image differencing with `>45000` changed pixels, **not OCR**;
8. activate the first character row near `(285,193)` with click + Return;
9. after 3 seconds, use a deterministic double-click at the same row as bounded fallback;
10. prove world presence separately through sustained tunneled session and structural/runtime evidence.

Qt/Tibia may replace/recreate its X11 window during transitions. Historical window IDs are never durable; always resolve the current visible Tibia window from the current client PID.

## Claim boundaries

### PROVEN

- OCR/Tesseract was not required for the successful historical login/world-entry path.
- Actions secrets intended for the bounded test login became available in the successful workflow and were used without persisting/printing their values.
- WARP confinement and zero direct Tibia TCP/UDP were proven in the successful historical run.
- the fixed-coordinate sequence above worked for the exact researched binary and exact historical `1020x650` layout.
- the successful run produced a real in-world viewport response to Right and a subsequent Left action.

### NOT semantic proof by itself

The following remain recovery/bootstrap aids only:

```text
changed pixels
window transition
successful credential submission
first-row UI activation
socket existence
socket byte counters
```

Current `OTCLIENT-TIBIA-RE` must still accept `IN_GAME` only from structural world/GameState evidence according to the canonical/base programme prompt.

### DISPROVEN / caution

A historical private-message experiment materially changed the UI but the owner observed that the intended message was not delivered and movement occurred instead. Therefore UI pixel change must never be used alone as proof of a semantic action.

A later chat experiment typed a test string and preserved active SOCKS, but lacked independent delivery confirmation; it is not a proven delivered private message.

Starting the client under GDB previously changed timing/UI behavior and failed to reproduce the otherwise proven login path. The preferred historical recovery pattern was normal client startup followed by instrumentation after world entry.

## Historical failed runs not to repeat blindly

```yaml
run_31621938187:
  jobs: [94198656638, 94201117705]
  result: FAIL_FOR_DECODED_CAPTURE
  note: authentication observed but decoded record count remained zero; GDB/UI path did not reproduce character entry
run_31624128761:
  result: failure
  note: failed live-worldmap attach attempt; inspect exact logs/hypothesis before retrying
```

## Historical session-preservation rules

When a valid authenticated session existed, the task required preserving it rather than relogging for convenience. The recovery workflow contained client termination and therefore was not safe to rerun while a useful authenticated process survived.

For long analysis windows, the historical recommendation was the smallest verified reversible keepalive, preferably turn-in-place and restore direction rather than autonomous wandering.

For the canonical OTClient runner, reinterpret these as general lifecycle principles only: verify current process/session structurally, preserve useful state, and never reuse old PID/window/runtime addresses.

## Canonical continuation use

On `synology-otclient-01`:

1. reverify the current official-client version/SHA first;
2. reconstruct the current runtime through the OTClient-owned path;
3. use the historical geometry only if the current exact client/window layout independently matches;
4. consume test-login secrets only through the currently authorized task workflow mechanism;
5. use CV/image differencing only as bounded recovery aid;
6. require decoded structural world/GameState evidence for `IN_GAME`;
7. once in world, prefer the stable bridge/runtime structural paths over screen interaction.

No external Oteryn runtime is required for this recipe to remain discoverable.
