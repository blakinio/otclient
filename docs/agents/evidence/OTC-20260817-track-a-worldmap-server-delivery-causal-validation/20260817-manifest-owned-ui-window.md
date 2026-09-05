# Worldmap causal baseline — manifest-owned 1020x650 UI window

Task: `OTC-20260817-track-a-worldmap-server-delivery-causal-validation`  
PR: #475  
Date: 2026-08-17

## Trigger

Normalized physical run `32031119012 / 95391127666` proved the task-local 1020x650 raw-XRes owner could pass the canonical worker's `client_window_wait` and persist an XRes-owned manifest `window_identity` for the exact task PID. The same run then failed closed only because a redundant second XRes discovery attempted to rediscover the already-proven window and returned no candidate.

The run stopped before credential submission and ended with original-source rehash PASS and cleanup COMPLETE.

## Corrected boundary

For the normalized task-owned 1020x650 desktop:

```text
WIN = manifest window_identity
    = accepted only after raw-XRes LocalClientPid == exact task-owned client PID
    = accepted only under task-local TARGET_WIDTH=1020 / TARGET_HEIGHT=650 owner helper
```

The UI helper now directly uses:

```text
UI_WIN="$WIN"
```

There is no second XRes rediscovery. Immediately before any credential is typed, a fresh raw-XWD capture of `UI_WIN` must still pass the strict exact-header check (`1020x650`) and classify as `LOGIN_FORM`. Thus ownership comes from the manifest XRes proof, while current geometry/UI state is independently revalidated live before secret use.

## No-client validation

Run/job `32031499662 / 95392314668` completed SUCCESS. It composed:

1. task-owned 1020x650 screen normalization;
2. GDB toolroot environment repair;
3. manifest-owned raw-XWD UI path.

The final helper passed `bash -n` and required:

```text
WORLDMAP_BASELINE_DESKTOP_GEOMETRY=1020x650
WORLDMAP_BASELINE_UI_WINDOW_XRES_OWNER=MANIFEST_PROVEN
WORLDMAP_BASELINE_UI_WINDOW_GEOMETRY_EXPECTED=1020x650
WORLDMAP_BASELINE_UI_WINDOW_EQUALS_RUNTIME_IDENTITY=true
UI_WIN="$WIN"
```

It also retained the XWD toolroot library binding and contained no redundant `track-a-worldmap-causal-ui-window.py` reference, OCR/tesseract path, or executable legacy `xdotool search --onlyvisible --pid` selector.

No client, X11 runtime, credentials or gameplay were used by this validation.

## Current classification

```text
MANIFEST_XRES_1020_IDENTITY=PROVEN_BY_PRIOR_PHYSICAL_BOOTSTRAP
REDUNDANT_SECOND_XRES_DISCOVERY=REMOVED
LIVE_PRE_SECRET_XWD_GEOMETRY_GATE=REQUIRED
LIVE_PRE_SECRET_LOGIN_FORM_GATE=REQUIRED
BASELINE_LOGIN_CONSUMED=false
PATCHED_LOGIN_CONSUMED=false
```

Next legal action is one physical normalized baseline generation. It must stop before secret submission unless the manifest-owned window still produces an exact 1020x650 raw-XWD classified as `LOGIN_FORM`.
