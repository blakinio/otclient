# OTC-20260813 Track A live-session handover

```yaml
task_id: OTC-20260813-track-a-live-session-handover
project_lane: otclient
track: official-client-re
status: ready
execution_mode: chat-github
branch: docs/OTC-20260813-track-a-live-handover
owned_paths:
  - docs/agents/tasks/active/OTC-20260813-track-a-live-session-handover.md
  - docs/agents/reports/OTCLIENT-20260813-track-a-live-session-login-handover.md
reuses:
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md
depends_on: []
blocks: []
```

## Objective

Persist the material Track A findings from the 2026-08-13 live official-Linux-client session, including the login/session-recovery procedure, Worldmap/action findings, position/pathing correction, exact claim boundaries, and the fresh owner-requested world-login revalidation performed later the same day, so continuation does not depend on chat history.

## Scope and authority

Documentation only. This handover records verified external-runtime evidence but does not broaden runtime, secret, production, Track B, or cross-repository authority. No credential values, account identifiers, session tokens, cookies, or unredacted screenshots may be committed.

## Acceptance inventory

- Track A and Track B are explicitly distinguished according to `docs/agents/TIBIA_RESEARCH_TRACKS.md`.
- The historical login/session-recovery sequence is documented without credentials or secret values.
- The role of Xvfb, SOCKS/WARP confinement, `proxychains4`, `xdotool`, character activation, and post-entry validation is explicit.
- Fresh owner-requested world-entry evidence is recorded with exact run/job/head/artifact references.
- Fresh structural Worldmap `x/y/z` is not claimed until explicit `REC x=... y=... z=...` records are observed.
- Decoded Worldmap, native action, downstream message-name, position, collision/pathing, and passive-logging findings remain bounded by `PROVEN`, `DERIVED`, `OWNER_OBSERVED`, `UNKNOWN`, or `REVALIDATION_REQUIRED` labels.
- No transient heap pointer, password, email address, cookie, token, or proprietary client bytes are promoted as canonical state.

## Evidence status

The repository-owned canonical baseline remains `docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md`.

### Fresh owner-requested physical world login — PROVEN

The following result was directly verified from GitHub Actions after the owner requested a fresh login:

```text
repository: blakinio/Oteryn-Platform
branch: ops/oteryn-tibia-client-analysis-20260811
head: 4392cf4c01703afa344ba074495894a292048eb9
workflow: .github/workflows/tibia-client-analysis-cv-world-entry.yml
run: 31736998731
job: 94570936207
job conclusion: SUCCESS
runner: oteryn-synology-staging
container: oteryn-tibia-client-analysis
client world PID: 32182
```

Verified success markers from the job log:

```text
WARP_VERIFIED=true
FIXED_WINDOW_GEOMETRY=true
LOGIN_SUBMITTED=true
LOGIN_VISUAL_TRANSITION=1
FIRST_CHARACTER_ACTIVATION_SENT=true
FIRST_CHARACTER_DOUBLECLICK_SENT=true
CLIENT_PID_WORLD=32182
CLIENT_LOCAL_SOCKS_MAX=6
CLIENT_DIRECT_TCP_SEEN=0
CLIENT_UDP_SEEN=0
CLIENT_SUSTAINED_TUNNELED_SESSION=1
VIEWPORT_CHANGED_PIXELS_AFTER_RIGHT=123008
CONTROLLED_MOVE_ACTION_PROVEN=true
PHYSICAL_WORLD_SESSION_AND_ACTION_PROVEN=true
```

This proves a fresh physical world-entry flow on the existing Oteryn analysis runtime: the official Linux client progressed through login and character activation, sustained a WARP/SOCKS-only session, accepted a bounded `Right` movement action, and changed the central viewport by `123008` pixels. The workflow then sent the opposite `Left` input as the bounded reversal step. It did not perform logout at the end of the proof.

This is strong reproducibility evidence for Track A, but it is not yet a replacement for the canonical requirement to reproduce structural `IN_GAME` on `synology-otclient-01`.

### Fresh privacy-safe screenshot artifact — PROVEN

```text
artifact name: tibia-cv-world-proof
artifact id: 9195582410
run: 31736998731
size: 443800 bytes
digest: sha256:be052134d159fc0c05e0e834553c98d2f2e51a6d3f428c91ebadb2b6c00658c5
```

The screenshot artifact was produced after the verified movement action. The workflow masks the top, left, right and bottom UI regions before upload and retains the central world viewport as privacy-safe proof.

### Exact fresh procedure that succeeded

1. Verify the owned analysis container on `oteryn-synology-staging`.
2. Use the official native Linux Tibia client from the existing CipSoft package runtime.
3. Verify the task-owned WARP/SOCKS path and require `warp=on`.
4. Launch the official client through `proxychains4` with software Vulkan/lavapipe (`VK_ICD_FILENAMES`, `VK_DRIVER_FILES`, `LIBGL_ALWAYS_SOFTWARE=1`).
5. Use Xvfb display `:99` and select the largest visible `Tibia` window; the successful workflow required `1020x650` geometry.
6. Inject account credentials only from protected Actions secrets into the login shell.
7. Fill the login UI with `xdotool`, submit, then immediately unset the credential environment variables.
8. Require a bounded post-submit visual transition before character activation.
9. Activate the first character row using the validated click + `Return` sequence, with the bounded double-click fallback already present in the workflow.
10. Require sustained local-SOCKS transport with zero direct client TCP and zero client UDP.
11. Capture the central viewport, send one `Right` movement action, capture again, and require changed pixels > 1000.
12. Send `Left` as the bounded reversal action.
13. Upload only the masked privacy-safe world screenshot.
14. Do not perform logout after the successful proof.

### Structural Worldmap follow-up — UNKNOWN until explicit records exist

Immediately after the successful physical world-entry run, a fresh passive structural proof was triggered using the existing live Worldmap attach workflow:

```text
repository: blakinio/Oteryn-Platform
workflow: .github/workflows/tibia-client-live-worldmap-attach.yml
head: 97f8df9e64e1e4f0520440073e497f24dad929ef
run: 31737285734
job: 94571875974
state when this checkpoint was written: QUEUED
```

That workflow is designed to emit records of the exact form:

```text
REC x=<x> y=<y> z=<z> order=<...> raw28=<...> raw30=<...>
```

Do not claim fresh structural `IN_GAME`, fresh `Worldmap x/y/z`, or authoritative current player coordinates until that run produces explicit `REC` records.

### Important correction retained

A previous conversation-level interpretation confused an observation log entry such as `second=83` with a count of 83 decoded Worldmap records. The specifically checked passive run actually reported:

```text
DECODED_CAPTURE_RECORD_COUNT=0
```

Future agents must count only explicit `REC ...` lines or the emitted `DECODED_CAPTURE_RECORD_COUNT` value. An observation-second value is not a Worldmap record count. This correction applies to that mistaken interpretation only and does not automatically invalidate older independently verified canonical Worldmap evidence.

## Claim boundary

`PROVEN`:

- fresh physical world login succeeded in `31736998731 / 94570936207`;
- WARP/SOCKS confinement was maintained with `CLIENT_DIRECT_TCP_SEEN=0` and `CLIENT_UDP_SEEN=0`;
- `CLIENT_SUSTAINED_TUNNELED_SESSION=1`;
- movement produced `VIEWPORT_CHANGED_PIXELS_AFTER_RIGHT=123008`;
- `PHYSICAL_WORLD_SESSION_AND_ACTION_PROVEN=true`;
- privacy-safe screenshot artifact `9195582410` was uploaded;
- the successful proof workflow did not log the character out.

`UNKNOWN`:

- whether the character remains logged in at any later wall-clock time; process/socket liveness alone is insufficient;
- fresh structural Worldmap coordinates until explicit records are captured;
- canonical reproduction of this exact successful procedure on `synology-otclient-01`.

## Next action

Read the completed result of `blakinio/Oteryn-Platform` run `31737285734`. If it contains explicit valid `REC x=... y=... z=...` records, persist those exact coordinates and record fresh structural `IN_GAME`. Then reproduce the now-validated world-entry procedure inside the isolated canonical Track A namespace on `synology-otclient-01` without weakening the structural acceptance gate.
