# Exact-window XWD geometry causal discriminator

Task: `OTC-20260817-track-a-worldmap-server-delivery-causal-validation`  
PR: `#475`  
Physical run/job: `32046786429 / 95436438152`  
Runner: `synology-otclient-01`  
Arm head: `27b1f98dbdf849b9b9f8fe23998f4694062ad2cb`  
Exact merge: `a816bbba6173f55f3d290a2960333401bf1ae34c`  
Current-main fence: `8a5fcfd72f2554261eef91a2129c9cc076e730ea`

## FACT — admission and safety boundary

Before client launch the physical job proved:

```text
WORLDMAP_PRESECRET_CURRENT_MAIN_FENCE=PASS
WORLDMAP_PRESECRET_ONE_SHOT_ARM=PASS
WORLDMAP_PRESECRET_TASK_NAMESPACE_PROCESS_COUNT=0
WORLDMAP_PRESECRET_OFFICIAL_CLIENT_CANDIDATE_COUNT=0
WORLDMAP_PRESECRET_TARGET_UNIQUENESS=PROVEN
WORLDMAP_PRESECRET_STATIC_COMPOSITION=PASS
```

The armed workflow contained no credential handoff or login-submission path. It composed the GDB repair and the pre-secret-only exact-window proof, ran Python compilation, `bash -n`, a synthetic dynamic-XWD geometry check, and rejected root-capture/window-mutation anchors before launching the exact client.

## FACT — exact runtime/window identity

The physical helper then proved:

```text
WORLDMAP_BASELINE_MANIFEST_FENCE=PASS
WORLDMAP_BASELINE_CLIENT_PID=18402
WORLDMAP_BASELINE_WINDOW_IDENTITY=x11-window:12582929
WORLDMAP_BASELINE_TARGET_UNIQUENESS=PROVEN
WORLDMAP_BASELINE_GDB_ATTACH=PASS
WORLDMAP_BASELINE_PRE_STORAGE_OBSERVER=ARMED
WORLDMAP_BASELINE_UI_WINDOW_IDENTITY=x11-window:12582929
WORLDMAP_BASELINE_UI_WINDOW_XRES_OWNER=MANIFEST_PROVEN
WORLDMAP_BASELINE_UI_WINDOW_EQUALS_RUNTIME_IDENTITY=true
WORLDMAP_UI_EXACT_XID=x11-window:12582929
WORLDMAP_UI_EXACT_XRES_PID_MATCH=PASS
```

The manifest-owned XID was not replaced, rediscovered to a different target, resized, reparented or recreated by the proof.

## FACT — actual X11 topology and geometry

Read-only `XGetWindowAttributes` / `XQueryTree` plus raw XRes on the exact supplied XID reported:

```text
WORLDMAP_UI_EXACT_GEOMETRY=1920x1080
WORLDMAP_UI_EXACT_BORDER_WIDTH=0
WORLDMAP_UI_EXACT_DEPTH=24
WORLDMAP_UI_EXACT_MAP_STATE=2
WORLDMAP_UI_ROOT_GEOMETRY=1920x1080
WORLDMAP_UI_PARENT_RELATION=DIRECT_ROOT_CHILD
WORLDMAP_UI_PARENT_GEOMETRY=1920x1080
WORLDMAP_UI_DIRECT_CHILD_COUNT=0
WORLDMAP_UI_DESCENDANT_COUNT=0
WORLDMAP_UI_SAME_PID_VIEWABLE_DESCENDANT_COUNT=0
WORLDMAP_UI_SAME_PID_VIEWABLE_DESCENDANT_GEOMETRIES=NONE
WORLDMAP_UI_SAME_PID_VIEWABLE_1020X650_COUNT=0
WORLDMAP_UI_EXACT_INSPECT=PASS
```

Therefore there is no observed 1020x650 child/client drawable, decorator frame or same-PID alternate viewable surface under the manifest-owned client window. The exact client window itself is a borderless direct child of the 1920x1080 Xvfb root and has the same 1920x1080 geometry.

## FACT — XWD capture versus parser

The capture command remained `xwd -silent -id "$UI_WIN"`, where `UI_WIN="$WIN"`; root capture was not used. The transient XWD from the exact manifest-owned XID reported:

```text
WORLDMAP_XWD_PIXMAP_GEOMETRY=1920x1080
WORLDMAP_XWD_WINDOW_GEOMETRY=1920x1080
WORLDMAP_XWD_WINDOW_POSITION=0,0
WORLDMAP_XWD_WINDOW_BORDER_WIDTH=0
WORLDMAP_XWD_BYTES_PER_LINE=7680
WORLDMAP_XWD_GEOMETRY_MATCH=PASS
WORLDMAP_BASELINE_XWD_CAPTURED_GEOMETRY=1920x1080
WORLDMAP_BASELINE_XWD_HEADER_WINDOW_GEOMETRY=1920x1080
WORLDMAP_BASELINE_XWD_CAPTURE_TARGET_EQUALS_RUNTIME_IDENTITY=true
WORLDMAP_BASELINE_XWD_GEOMETRY_PROOF=PASS
```

### Root cause of `1920 != 1020`

The old compare helper treated `1020x650` and stride `4080` as immutable XWD-format expectations. After the native restack, however, the canonical runtime again selected the exact XRes-owned top-level client window in the default `1920x1080` Xvfb surface. Physical inspection now proves that the manifest-owned window itself is `1920x1080`; XWD correctly captures `1920x1080`; its XWD window-header geometry is also `1920x1080`; and there is no 1020x650 child drawable to substitute.

Thus the prior failure

```text
WORLDMAP_XWD_COMPARE_ERROR=XwdError:shape_width:1920!=1020
```

was caused by a stale fixed geometry assertion in the XWD parser/proof, not by XWD selecting a different XID, root-window fallback, a decorator/frame mismatch, a 1020 child drawable, or an XRes ownership failure.

The repaired compare path preserves strict XWD format/depth/mask validation but validates geometry against the physically inspected exact X11 window instead of forcing 1020x650.

## FACT — VNC/window preservation

The same physical runtime emitted the canonical VNC startup pass before client startup and then:

```text
WORLDMAP_BASELINE_VNC_MAPPING_PRESERVED=MANIFEST_RUNTIME_UNCHANGED
```

The proof performed no X11 resize/reparent/recreate operation and retained `x11-window:12582929` as both runtime identity and XWD/UI target. No alternate XID was selected.

## FACT — new pre-secret discriminator

After geometry/capture proof passed, the coordinate-free semantic Tab scan did not classify any unique editable text field:

```text
WORLDMAP_PRELOGIN_ADAPTIVE_FIELD_SCAN_SECRET_ENV=ABSENT
WORLDMAP_PRELOGIN_ADAPTIVE_FIELD_SCAN_MODE=TAB_TEXT_GROWTH_AND_MASK_VARIANT_NO_COORDINATES
unique_field_classes_required:unmasked=0;masked=0
WORLDMAP_BASELINE_ERROR=adaptive_unique_email_password_discriminator_failed
```

This is a new failure boundary after the XWD geometry defect. It does **not** invalidate the exact-window/XWD geometry proof; it means the new coordinate-free semantic classifier did not establish the email/password fields in this 1920x1080 startup surface.

Required credential gates therefore did not pass:

```text
WORLDMAP_BASELINE_EMAIL_FIELD_EDITABLE=NOT_PROVEN
WORLDMAP_BASELINE_PASSWORD_FIELD_EDITABLE=NOT_PROVEN
WORLDMAP_BASELINE_LOGIN_FORM=NOT_PROVEN
WORLDMAP_BASELINE_PRESECRET_READY=false
```

No protected credential was handed off and no login was submitted.

## FACT — fail-closed termination

```text
WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS
WORLDMAP_BASELINE_CLEANUP=COMPLETE
WORLDMAP_PRESECRET_HELPER_EARLY_RESULT=1
WORLDMAP_FINAL_NAMESPACE_PROCESS_COUNT=0
WORLDMAP_FINAL_CLEANUP_FENCE=PASS
```

Baseline login budget remains `0/1`; patched login budget remains `0/1`.

Immediately after this discriminator, the PR workflow was returned to a no-client hold. A materially new UI-state/editability discriminator is required before any further physical retry or any credential path may be armed.
