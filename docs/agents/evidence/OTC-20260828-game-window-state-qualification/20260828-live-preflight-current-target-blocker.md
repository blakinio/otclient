# Live gameWindowState readiness preflight — BLOCKED_FAIL_CLOSED

Date: 2026-08-28

## Identity

- owner trigger comment: `5456931858` on PR #756
- workflow run: `33204467524`
- job: `98961872769`
- runner: `synology-otclient-01`
- exact trusted main: `1d9e69ba1afb369dbef911771d240a9633ff6798`
- command: `PREFLIGHT_GAME_WINDOW_STATE_QUALIFICATION`

## Fresh memory-free proof

The trusted-main preflight revalidated the repository runtime-none checkpoint and exact canonical client fence for official Linux client:

```yaml
client_version: 15.32.75d4a0
client_size: 52105824
client_sha256: d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
```

`Resolve canonical registration and current ownership` passed, which proves the authoritative registration was structurally valid, exact-fenced to the build above, carried a Docker locator plus PID/start identity, and had no conflicting unexpired canonical lease owned by another task.

The subsequent fresh inventory reached the singleton-count gate and then failed closed with the exact reason:

```text
REGISTERED_TARGET_NOT_CURRENT_UNIQUE_CANDIDATE
```

Because the workflow tests `OFFICIAL_CLIENT_CANDIDATE_COUNT == 1` before this reason can be emitted, the live inventory proved exactly one exact-fenced official-client candidate existed, but it did not match the canonical registration's container/PID/start identity.

The registration supplied to the failed inventory step was:

```text
container_name=otclient-track-a-kasmvnc
container_id=1af4af4d67f5
pid=13947
process_start_ticks=51652120
```

No replacement live identity is recorded here: governance forbids guessing or ad-hoc canonical registration edits.

## Fail-closed boundary

The failure occurred in `Re-prove global unique exact target` before these steps could execute:

- `Persist and validate fresh read-only admission` — skipped;
- `Revalidate admission immediately before any observation` — skipped;
- `Report memory-free logger readiness preflight` — skipped;
- resolver bundle construction — skipped;
- continuous bounded state capture — skipped;
- artifact validation/upload — skipped.

Therefore:

```text
PROCESS_MEMORY_OBSERVATION_PERFORMED=false
READ_ONLY_ADMISSION_CREATED=false
GAME_WINDOW_STATE_LOGGER_PREFLIGHT=NOT_READY
IN_GAME_CLAIMED=false
semantic_promotion_performed=false
```

No `/proc/<pid>/mem` access, GUI/input, login, credentials, character selection, gameplay, packet/payload capture, process mutation or semantic promotion occurred.

The repository task remained `runtime_access: none`; this preflight created no reusable runtime authority that requires release.

## Terminal result

```text
LIVE_GAME_WINDOW_STATE_CAUSAL_VALIDATION=BLOCKED_FAIL_CLOSED
BLOCKER=REGISTERED_TARGET_NOT_CURRENT_UNIQUE_CANDIDATE
```

Owner UI interaction is not authorized because the logger never reached READY.

`next_action`: under a separate fresh canonical-live governance admission, reconcile or re-admit the authoritative registration to the exact currently unique official-client container/PID/start identity without ad-hoc metadata edits; release that temporary authority; then rerun a new `PREFLIGHT_GAME_WINDOW_STATE_QUALIFICATION`. Only a fresh READY result may authorize the owner sequence `LOGIN_SCREEN -> CHARACTER_SELECT -> WORLD -> WORLD_EXIT`.
