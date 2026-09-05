# Worldmap causal baseline — task-owned 1020x650 desktop normalization

Task: `OTC-20260817-track-a-worldmap-server-delivery-causal-validation`  
PR: #475  
Date: 2026-08-17

## Triggering physical result

Run/job `32030582178 / 95389455836` proved the distinct-window hypothesis false for the current 1920x1080 isolated desktop:

```text
WORLDMAP_BASELINE_TARGET_UNIQUENESS=PROVEN
WORLDMAP_BASELINE_PRE_STORAGE_OBSERVER=ARMED
WORLDMAP_XRES_UI_WINDOW_ERROR=XRes UI-window ownership unresolved: no viewable 1020x650 candidate
WORLDMAP_BASELINE_ERROR=xres_ui_window_unresolved
WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS
WORLDMAP_BASELINE_CLEANUP=COMPLETE
```

No `WORLDMAP_BASELINE_LOGIN_SUBMITTED=true` marker was emitted. The run stopped before credential submission.

## Changed hypothesis

The promoted canonical worker creates Xvfb with `-screen 0 1920x1080x24`; its promoted XRes owner is correspondingly fenced to a 1920x1080 viewable window. Historical successful exact-client login evidence was produced in a 1020x650 window, with retained raw-XWD geometry and safe control points already independently recorded.

For this bounded causal comparison the task therefore normalizes its **task-owned ephemeral** desktop to 1020x650 before client launch. The same transform is required for both experiment arms:

```text
baseline exact [18,14]  -> task-owned Xvfb 1020x650
patched copy [19,14]    -> task-owned Xvfb 1020x650
```

This changes neither the canonical source client nor canonical controller runtime. It removes UI-geometry drift from the experiment rather than introducing an arm-specific variable.

## Fail-closed transform

`.github/scripts/track-a-worldmap-causal-screen-geometry-repair.py` composes the task worker without modifying canonical files:

1. after the canonical worker has been copied into the task namespace, replace exactly one `-screen 0 1920x1080x24` with `-screen 0 1020x650x24`;
2. create a task-temporary copy of the promoted raw-XRes owner helper, retaining its exact basename but replacing exactly one `TARGET_WIDTH = 1920` with `1020` and one `TARGET_HEIGHT = 1080` with `650`;
3. feed that task-temporary owner helper to the existing #465 XRes worker adapter;
4. require the resulting worker to contain the 1020x650 Xvfb geometry and no old 1920x1080 screen command;
5. remove the temporary XRes owner helper during task cleanup.

The UI resolver then independently resolves a 1020x650 XRes `LocalClientPid` match and requires `UI_WIN == WIN`, where `WIN` is already the manifest's XRes-owned 1020x650 runtime identity.

## No-client static validation

Run/job `32030958692 / 95390632587` completed SUCCESS. It:

- Python-compiled the screen-normalization, GDB, XRes UI resolver, raw-XWD classifier and UI repair helpers;
- composed screen normalization -> GDB environment repair -> UI geometry repair;
- passed `bash -n` on the final helper;
- required task-worker 1020x650, task-temporary XRes owner 1020x650, `UI_WIN == WIN`, XWD library binding, and OCR-free surfaces;
- rejected any executable legacy `xdotool search --onlyvisible --pid` selector.

No client process, X11 session, credential or gameplay action occurred in this static run.

## Current boundary

```text
DESKTOP_NORMALIZATION_1020x650_STATIC_READY=true
BASELINE_AND_PATCHED_DESKTOP_MUST_MATCH=true
CANONICAL_SOURCE_MODIFIED=false
CANONICAL_RUNTIME_MODIFIED=false
BASELINE_LOGIN_CONSUMED=false
PATCHED_LOGIN_CONSUMED=false
```

Next legal step is one physical baseline generation. Before credentials it must still pass current-main admission, canonical controller idle, target uniqueness, pre-Storage observer attachment, XRes-owned 1020x650 identity and live raw-XWD `LOGIN_FORM` classification.
