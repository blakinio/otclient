# No-secret Tab focus scan — ambient-confounded result

Task: `OTC-20260817-track-a-worldmap-server-delivery-causal-validation`  
PR: `#475`  
Run/job: `32035922474 / 95406276923`  
Execution: `synology-otclient-01`, exact official client, no secrets

## Admission and runtime fence

The run used an anonymous direct Git checkout after the previous `actions/checkout` attempt was blocked by codeload HTTP 429. It independently passed:

- current-main ancestry/admission on `main@dd54e6d14b214045baa2a67a7a57edaff40e8599`;
- Track A runtime governance;
- canonical controller idle / registration absent;
- task-local XWD and `xdotool`/`libxdo.so.3` dynamic-link closure;
- exact-client manifest fence and XRes window ownership;
- target uniqueness;
- bounded GDB attach;
- pre-Storage observer arm.

The diagnostic contained no credential submission, character activation or gameplay movement path. `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD` were required absent at runtime.

## Aggregate result

The reversible Tab scan reported four whole-window candidates:

```text
round:1 tab:5  bbox:14,11,974,497  typed_changed:1336 overlap:0.973364 equal_length_variant_changed:1282
round:1 tab:10 bbox:13,12,985,527  typed_changed:1312 overlap:1.000000 equal_length_variant_changed:792
round:1 tab:12 bbox:13,12,985,527  typed_changed:1312 overlap:1.000000 equal_length_variant_changed:920
round:1 tab:14 bbox:13,11,983,526  typed_changed:1309 overlap:0.960275 equal_length_variant_changed:792
```

Terminal markers:

```text
WORLDMAP_PRELOGIN_EDITABLE_CANDIDATE_COUNT=4
WORLDMAP_PRELOGIN_FOCUS_SCAN=COMPLETE_NO_SECRET
WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS
WORLDMAP_BASELINE_CLEANUP=COMPLETE
```

No raw XWD was uploaded or retained by the workflow.

## Classification

`EDITABLE_FIELD_DISCOVERY=NOT_PROVEN`.

The four candidate bounding boxes span approximately the whole animated client surface rather than a compact input field. Their changed-pixel counts are tightly clustered around ~1300 despite different Tab indices. Therefore the current whole-window reversible-overlap test is confounded by ambient repaint/animation and these candidates MUST NOT be promoted as email/password controls.

This result does not consume the baseline login budget. `WORLDMAP_BASELINE_LOGIN_SUBMITTED=true` was absent; baseline login remains `0/1`, patched login remains `0/1`.

## Changed-hypothesis continuation

The next no-secret discriminator must measure ambient repaint at each Tab state before typing and require the type/clear cycle to produce a material positive delta above that local idle baseline. Do not rerun the same whole-window candidate rule and do not use the four Tab indices as credential targets without that control.
