# Worldmap causal baseline — XRes UI-window boundary

Task: `OTC-20260817-track-a-worldmap-server-delivery-causal-validation`  
PR: #475  
Date: 2026-08-17

## Problem isolated before credential submission

Physical run `32029873507 / 95387243716` passed current-main admission, canonical-controller idle, XWD dynamic-link preflight, exact-client/WARP/XRes bootstrap, target uniqueness and the pre-Storage observer. The first live raw-XWD capture then failed closed with:

```text
WORLDMAP_XWD_CLASSIFIER_ERROR=ValueError:xwd_shape_width:1920!=1020
WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS
WORLDMAP_BASELINE_CLEANUP=COMPLETE
```

`WORLDMAP_BASELINE_LOGIN_SUBMITTED=true` was not emitted. No credential submission or gameplay occurred.

## FACT — 1920x1080 is the runtime identity window

The promoted raw-XRes owner helper on trusted main intentionally filters candidates to `TARGET_WIDTH=1920`, `TARGET_HEIGHT=1080` and resolves ownership through XRes `LocalClientPid`. The `WIN` returned by the task bootstrap is therefore a process/runtime identity fence, not the historical 1020x650 UI-control window.

## FACT — historical exact-client UI window was 1020x650

Historical successful exact-client run `31805408522 / 94783011926` selected a separate visible `Tibia` window with area exactly `663000` (`1020*650`) before capturing XWD and selecting the first character row. Retained exact-client artifacts `9221131366` and `9221234379` independently preserve the 1020x650 login/selection geometry used by the OCR-free classifier.

The historical workflow used an `xdotool --pid` search to locate that UI window. That historical lookup is useful as geometry provenance only; it is **not** promoted as current ownership proof.

## Repair boundary

A task-local resolver `.github/scripts/track-a-worldmap-causal-ui-window.py` now reuses the promoted raw-XRes implementation while narrowing candidate geometry to exactly 1020x650. It accepts a UI XID only if XRes `LocalClientPid` resolves to the same exact task-owned client PID already fenced by the 1920x1080 identity window.

The physical helper therefore requires two distinct identities:

```text
WIN    = XRes-owned 1920x1080 runtime identity fence
UI_WIN = XRes-owned 1020x650 UI-control window for the same exact PID
```

`UI_WIN != WIN` is mandatory. Fixed login/selection points and raw-XWD classification operate only on `UI_WIN`. The 1920x1080 `WIN` remains the authoritative runtime identity fence.

No executable legacy `xdotool search --onlyvisible --pid` selector is allowed in the composed helper. The pre-existing negative grep that detects such a selector is intentionally retained and is not itself an executable selector.

## No-client static validation

Run/job `32030421837 / 95388952750` completed SUCCESS on the repair head. It performed only source checkout and static composition:

- Python compilation of the XRes owner/wire helpers, new 1020x650 resolver, classifier and repair scripts;
- resolver `--help` smoke;
- classifier self-test;
- GDB-environment repair composition followed by UI-window repair composition;
- `bash -n` on the final combined helper;
- required XRes-owner, 1020x650 geometry and XWD library-binding markers;
- no executable legacy PID window selector;
- no OCR/tesseract surface.

No client, X11 runtime, credentials or gameplay were used by this static validation.

## Current classification

```text
RUNTIME_IDENTITY_WINDOW_1920x1080=PROVEN_FROM_PROMOTED_XRES_HELPER_AND_PRIOR_PHYSICAL_RUN
HISTORICAL_UI_WINDOW_1020x650=PROVEN
XRES_1020x650_UI_RESOLVER_STATIC_READY=true
LIVE_XRES_1020x650_UI_WINDOW_FOR_CURRENT_BASELINE=NOT_YET_PROVEN
BASELINE_LOGIN_CONSUMED=false
CLIENT_BYTE_MUTATION_EXECUTED=false
```

Next legal action is one physical baseline generation. Before any secret is typed it must prove `UI_WIN` is a distinct 1020x650 XRes-owned window for the exact task PID and classify its live raw-XWD as `LOGIN_FORM`.
