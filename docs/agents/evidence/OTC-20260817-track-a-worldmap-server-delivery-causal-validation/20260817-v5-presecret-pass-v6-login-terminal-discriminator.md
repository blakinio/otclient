# V5 pre-secret PASS + V6 baseline-login terminal discriminator

Task: `OTC-20260817-track-a-worldmap-server-delivery-causal-validation`  
PR: `#475`  
Runner: `synology-otclient-01`

## FACT — V5 completed the requested pre-secret gate

Physical run/job:

- run: `32058144974`
- job: `95472948299`
- arm head: `60d185b7f661193b9b4592d8a2e63df30834727a`
- result: `SUCCESS`

Load-bearing markers:

```text
WORLDMAP_BASELINE_WINDOW_IDENTITY=x11-window:12582929
WORLDMAP_BASELINE_UI_WINDOW_IDENTITY=x11-window:12582929
WORLDMAP_BASELINE_UI_WINDOW_XRES_OWNER=MANIFEST_PROVEN
WORLDMAP_BASELINE_UI_WINDOW_EQUALS_RUNTIME_IDENTITY=true
WORLDMAP_UI_EXACT_XRES_PID_MATCH=PASS
WORLDMAP_BASELINE_UI_WINDOW_GEOMETRY_ACTUAL=1920x1080
WORLDMAP_BASELINE_XWD_CAPTURED_GEOMETRY=1920x1080
WORLDMAP_BASELINE_XWD_HEADER_WINDOW_GEOMETRY=1920x1080
WORLDMAP_BASELINE_XWD_CAPTURE_TARGET_EQUALS_RUNTIME_IDENTITY=true
WORLDMAP_BASELINE_XWD_GEOMETRY_PROOF=PASS
WORLDMAP_BASELINE_VNC_MAPPING_PRESERVED=MANIFEST_RUNTIME_UNCHANGED
WORLDMAP_BASELINE_GDB_ATTACH=PASS
WORLDMAP_BASELINE_PRE_STORAGE_OBSERVER=ARMED
WORLDMAP_BASELINE_EMAIL_FIELD_EDITABLE=PASS
WORLDMAP_BASELINE_PASSWORD_FIELD_EDITABLE=PASS
WORLDMAP_BASELINE_LOGIN_FORM=PROVEN_EDITABLE_FIELDS
WORLDMAP_BASELINE_PRESECRET_READY=true
WORLDMAP_PHYSICAL_PRESECRET_V5_GATE=PASS
WORLDMAP_V5_LOGIN_SUBMITTED=false
WORLDMAP_V5_LOGIN_BUDGET_CONSUMED=0
WORLDMAP_FINAL_NAMESPACE_PROCESS_COUNT=0
WORLDMAP_FINAL_CLEANUP_FENCE=PASS
```

V5 local final probes were physically reversible and noise-controlled:

```text
email:    signal=533 overlap=1.000000 residual=0
password: signal=568 overlap=1.000000 residual=0
```

The independent V4 rendering discriminator that feeds V5 repeatedly identified the upper local field as unmasked and the lower local field as masked. No OCR, screenshot artifact, root-window fallback, alternate XID, resize, reparent or window recreation was used.

## FACT — V6 repeated the same gates before credentials

Physical run/job:

- run: `32059988893`
- job: `95478896813`
- arm head: `9f30f7fc8fa558c35c0ee62c76b0d1bf6e357fe8`
- exact current-main fence: `8a5fcfd72f2554261eef91a2129c9cc076e730ea`
- overall job result: `FAILURE` after login submission

Before the credential-bearing step started, the same launch physically emitted:

```text
WORLDMAP_V6_TARGET_UNIQUENESS=PROVEN
WORLDMAP_V6_PHYSICAL_COMPOSITION=PASS
WORLDMAP_BASELINE_MANIFEST_FENCE=PASS
WORLDMAP_BASELINE_WINDOW_IDENTITY=x11-window:12582929
WORLDMAP_BASELINE_GDB_ATTACH=PASS
WORLDMAP_BASELINE_PRE_STORAGE_OBSERVER=ARMED
WORLDMAP_BASELINE_UI_WINDOW_XRES_OWNER=MANIFEST_PROVEN
WORLDMAP_BASELINE_UI_WINDOW_EQUALS_RUNTIME_IDENTITY=true
WORLDMAP_UI_EXACT_XRES_PID_MATCH=PASS
WORLDMAP_BASELINE_XWD_GEOMETRY_PROOF=PASS
WORLDMAP_BASELINE_EMAIL_FIELD_EDITABLE=PASS
WORLDMAP_BASELINE_PASSWORD_FIELD_EDITABLE=PASS
WORLDMAP_BASELINE_LOGIN_FORM=PROVEN_EDITABLE_FIELDS
WORLDMAP_BASELINE_PRESECRET_READY=true
WORLDMAP_V6_PRESECRET_GATE=PASS
WORLDMAP_V6_LOGIN_BUDGET_CONSUMED=0
```

The helper process environment was separately checked not to contain `TIBIA_TEST_EMAIL` or `TIBIA_TEST_PASSWORD` before the handoff step.

## FACT — credential handoff and login submission

The protected GitHub secret values were supplied only in the next workflow step and written through the already-created mode-0600 FIFO. Values were not printed or uploaded.

Markers:

```text
WORLDMAP_WORKFLOW_CREDENTIAL_HANDOFF=COMPLETE_AFTER_V5_PRESECRET_GATE
WORLDMAP_BASELINE_CREDENTIAL_HANDOFF=RECEIVED_AFTER_PRESECRET_GATES
WORLDMAP_BASELINE_LOGIN_SUBMISSION_METHOD=PASSWORD_TAB_RETURN
WORLDMAP_BASELINE_LOGIN_SUBMITTED=true
```

The single baseline login budget is therefore consumed:

```text
baseline_ephemeral_login_max: 1
baseline_ephemeral_login_consumed: 1
```

No further baseline login retry is legal under the task's existing contract.

## FACT — login reached character selection, but not structural IN_GAME

After submission the helper physically observed a >5000-pixel aggregate transition from the blank pre-login reference:

```text
WORLDMAP_BASELINE_CHARACTER_SELECTION_TRANSITION=PROVEN_AGGREGATE
```

This proves the UI left the pre-login form and reached the expected post-auth transition boundary. It is not by itself an IN_GAME claim.

The post-transition historical row coordinate was used only as a target after the live UI/window state had already been proven. It was translated from the two same-launch discovered field positions:

```text
WORLDMAP_BASELINE_CHARACTER_ROW_TARGET=685,408
WORLDMAP_BASELINE_CHARACTER_ROW_ROI=500,380,1300,445
```

No candidate in the bounded translated target neighborhood produced the required localized row-selection change. Terminal discriminator:

```text
WORLDMAP_BASELINE_ERROR=character_row_interaction_not_observed
```

Therefore the following remain NOT PROVEN / not emitted:

```text
WORLDMAP_BASELINE_CHARACTER_ROW_SELECTION=PROVEN_AGGREGATE
WORLDMAP_BASELINE_STRUCTURAL_IN_GAME=PASS
WORLDMAP_BASELINE_STRUCTURAL_FULLMAP_COUNT=<not obtained>
WORLDMAP_BASELINE_STRUCTURAL_PRE_MOVE_STRIP_COUNT=<not obtained>
WORLDMAP_BASELINE_TRANSPORT_CONFINEMENT=PASS  # post-IN_GAME gate not reached
WORLDMAP_BASELINE_PHYSICAL_CAPTURE=PASS
```

No claim of successful world entry is made.

## FACT — cleanup and source integrity

The failed post-submit generation terminated fail-closed:

```text
WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS
WORLDMAP_BASELINE_CLEANUP=COMPLETE
WORLDMAP_FINAL_NAMESPACE_PROCESS_COUNT=0
WORLDMAP_FINAL_CLEANUP_FENCE=PASS
```

The manifest/runtime/UI XID remained `x11-window:12582929` throughout the generation; there was no resize, reparent, recreate, alternate-XID selection or root-window substitution. VNC was started by the unchanged canonical bootstrap path and the same manifest window identity was retained.

## Terminal task consequence

Under the existing task contract, any failure after `WORLDMAP_BASELINE_LOGIN_SUBMITTED=true` consumes the one baseline login budget and must not be silently retried. That condition occurred here.

Current legal runtime state is therefore a **terminal no-client hold** for the baseline arm. The baseline authoritative worldmap extent was not obtained, so the baseline-versus-`[19,14]` causal comparison cannot be completed from this task without an explicit new authorization that changes the exhausted baseline-login budget/contract. The separate patched login budget remains `0/1`, but spending it cannot repair the missing authoritative baseline comparator.
