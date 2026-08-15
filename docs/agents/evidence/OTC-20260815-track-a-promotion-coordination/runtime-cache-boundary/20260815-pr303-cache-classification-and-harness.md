# Coordinator classification — PR #303 cache metadata and seed discriminator

Date: 2026-08-15
Programme: `OTCLIENT-TIBIA-RE`
Track: `official-client-re`
Source Draft PR: #303
Coordinator PR: #300
Disposition: `RETURN_FOR_EVIDENCE / CACHE_CAUSALITY_UNKNOWN`

## Exact client fence

```text
version mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runner: synology-otclient-01
```

## Metadata-only classification — accepted bounded fact

Run `31903484499` / job `95057696652` completed successfully and verified the exact client before inspecting only path metadata under the persistent HOME cache root.

It emitted:

```text
TRACK_A_CACHE_FILE_COUNT=4
TRACK_A_CACHE_TOTAL_BYTES=6937
TRACK_A_CACHE_SENSITIVE_PATH_KEYWORD_HITS=0
TRACK_A_CACHE_PAYLOAD_READ=false
```

The sanitized metadata classes/sizes were:

- three `.qsb` files, sizes `2309`, `2162`, `2386`, classified by path as `shader`;
- one 80-byte file classified by path as `gpu+generic_cache`.

This supports only the claim that the known persistent-HOME delta is consistent at the metadata level with shader/GPU cache state. It does **not** prove payload purpose, non-account semantics, non-secret contents, or causal relevance to the missing isolated window.

## Cache seed run — harness failure, not causal evidence

Run `31903627907` / job `95058043269` reached:

```text
TRACK_A_CACHE_WINDOW_EXACT_CLIENT_VERIFIED=true
TRACK_A_CACHE_WINDOW_UPSTREAM_WARP_VERIFIED=true
TRACK_A_CACHE_WINDOW_CLASSIFIED_CACHE_SEEDED=true files=4 bytes=6937
TRACK_A_CACHE_WINDOW_TASK_RELAY_VERIFIED=true
TRACK_A_CACHE_WINDOW_XVFB_VERIFIED=true
TRACK_A_CACHE_WINDOW_CLIENT_RUNNING=true pid=12468
```

and then terminated with exit code `127` before emitting either:

```text
TRACK_A_CACHE_WINDOW_ALL_PID_WINDOWS=...
TRACK_A_CACHE_WINDOW_VISIBLE_PID_WINDOWS=...
```

Therefore the run is classified:

```yaml
cache_seed_performed: true
exact_client_running: true
window_observation_completed: false
cache_causality: UNKNOWN
semantic_result: INCONCLUSIVE_HARNESS_FAILURE
```

It must not be cited as evidence that cache seeding restored a window or failed to restore a window.

## Privacy / trust-boundary correction

The seed workflow read each cache payload using `read_bytes()` and searched a short denylist before copying the directory into a task-local HOME. A small negative keyword scan over arbitrary binary bytes is not a proof that opaque payload is non-secret or non-account state.

The coordinator therefore does not authorize further persistent-HOME cache payload reads/copies for this RUNTIME lane based only on the current metadata census. The source cache itself was not mutated, and the task-local seeded copy was ephemeral, but this experiment should not be repeated merely to repair the observation harness.

Coordinator PR comment `5303842133` records the return-for-evidence gate on source PR #303.

## Required next RUNTIME discriminator

Use a fresh task-owned HOME without canonical cache payload seeding and preserve the current exact-client, WARP/SOCKS, no-secret child environment, no-login-before-window, display/port ownership and cleanup fences.

Repair the observation harness and capture, without gameplay input:

1. all client-owned X11 windows, including mapped and unmapped state rather than only `--onlyvisible`;
2. sanitized window geometry/properties where available;
3. relevant X server extension capability/state for the task-owned display;
4. sanitized Qt platform/plugin diagnostics already enabled by `QT_DEBUG_PLUGINS=1`.

If an actual hidden/unmapped Tibia window exists, follow that evidence. If no client-owned X11 window exists, select the next single-variable launch hypothesis from runtime diagnostics. Do not touch persistent display `:98`, Track B, gameplay/movement, or canonical cache payloads.
