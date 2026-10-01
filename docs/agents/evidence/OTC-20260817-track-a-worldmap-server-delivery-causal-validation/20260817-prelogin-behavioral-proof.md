# Worldmap causal baseline — behavioral pre-login proof

Task: `OTC-20260817-track-a-worldmap-server-delivery-causal-validation`  
PR: #475  
Date: 2026-08-17

## Why the prior grayscale gate was retired

Two normalized exact-client runs reached the fully proven pre-secret physical boundary but the retained grayscale classifier continued to return `OTHER`:

- `32031603546 / 95392645496`;
- `32031856344 / 95393435891` (an already-triggered duplicate generation caused by the pull-request workflow path filter continuing to match the workflow file in the PR diff).

Both runs proved, before the UI gate:

```text
current-main admission = PASS
canonical controller = released / registration absent
XWD toolroot dynamic-link = PASS
task-owned desktop = 1020x650
manifest XRes window fence = PASS
target uniqueness = PROVEN
pre-Storage worldmap observer = ARMED
raw XWD shape = 1020x650
```

The stable live frame then had aggregate grayscale ratio `0.006818181818` and did not satisfy the retained color/style thresholds. Neither run emitted `WORLDMAP_BASELINE_LOGIN_SUBMITTED=true`; both ended with original-source rehash PASS and cleanup COMPLETE.

The earlier evidence label that treated artifact `9221131366` as an empty login-form reference is corrected here. Its producing run/job `31805408522 / 94783011926` captured an already-running character-selection window immediately before selecting the first row. Therefore its color distribution is not an authoritative login-form signature.

Historical exact-client control coordinates remain useful because the effective software-world workflow used them operationally:

```text
email      535,275
password   535,304
login      590,388
first row  285,193
```

The successful character-row entry path in `31805408522 / 94783011926` independently confirms the first-row coordinate family on a 1020x650 exact-client window. No OCR-derived text is promoted.

## Replacement pre-secret discriminator

The UI gate now proves **behavior**, not theme/color. Before any real credential is exposed, the task:

1. uses the already manifest-proven XRes-owned 1020x650 `WIN` as `UI_WIN`;
2. focuses the historical email coordinate, clears it, captures a transient raw XWD, types harmless `wm-probe@example.invalid`, captures again, clears it, and captures again;
3. requires an aggregate localized changed-pixel cycle in the email ROI;
4. repeats the same process at the password coordinate using harmless `wm-probe-7`;
5. deletes all transient raw XWDs immediately;
6. only after both probes pass emits:

```text
WORLDMAP_BASELINE_EMAIL_FIELD_EDITABLE=PASS
WORLDMAP_BASELINE_PASSWORD_FIELD_EDITABLE=PASS
WORLDMAP_BASELINE_LOGIN_FORM=PROVEN_EDITABLE_FIELDS
```

The dummy strings are not credentials and no login/Enter action is sent during these probes.

`.github/scripts/track-a-worldmap-causal-xwd-compare.py` parses only exact 1020x650 XWD geometry and emits aggregate changed-pixel counts. It emits no screenshot text, pixel payload or account identity.

## Post-submit bounded gates

After both editable-field probes pass, a blank no-secret reference is captured transiently. The single authorized baseline credential submission then uses the historical exact coordinates and immediately unsets the secret environment variables.

The helper requires:

- more than 5000 changed pixels versus the blank pre-login reference before treating the UI as transitioned;
- after a bounded settle interval, a localized aggregate pixel change in the historical first-character-row ROI caused by one selection click;
- only then is `Return` sent;
- actual world entry remains **structural only**: `FullMap` plus at least 10 map-description strip records from the pre-Storage observer.

If any gate after `WORLDMAP_BASELINE_LOGIN_SUBMITTED=true` fails, that baseline login budget is consumed and the task must not silently retry.

## Workflow duplicate protection

Because GitHub pull-request `paths` filtering continued to match the workflow file already present in the PR diff, script-only synchronize events could trigger another generation. The workflow was therefore switched to a no-client safety hold before further helper development, then to a no-client static validator.

No physical client can run while that static workflow is present.

## Static validation

Run/job `32032410153 / 95395158148` completed SUCCESS on helper head `8181fe41abe8fcad5b38d26c624b29075ba4ede6`.

It validated, without client/runtime/secrets:

- screen normalization -> GDB environment repair -> behavioral UI repair composition;
- Python compilation and final `bash -n`;
- manifest-owned 1020x650 UI identity;
- aggregate editable email/password probes;
- historical exact control coordinates;
- aggregate post-login transition gate;
- aggregate first-row interaction gate;
- no obsolete grayscale login-form gate;
- no OCR/tesseract path;
- no executable legacy `xdotool search --onlyvisible --pid` selector.

```text
WORLDMAP_PRELOGIN_BEHAVIOR_STATIC=PASS
WORLDMAP_PRELOGIN_BEHAVIOR_CLIENT_EXECUTED=false
WORLDMAP_PRELOGIN_BEHAVIOR_SECRET_USED=false
```

## Current boundary

```text
PRELOGIN_BEHAVIORAL_PROOF_STATIC_READY=true
BASELINE_LOGIN_CONSUMED=false
PATCHED_LOGIN_CONSUMED=false
PHYSICAL_BASELINE_RESULT=NOT_YET_OBTAINED
```

Next legal action is exactly one physical baseline generation using this statically validated helper. Before real credentials it must pass both harmless editable-field probes. After submission, any failure consumes the single baseline login budget and is terminal for silent retry.
