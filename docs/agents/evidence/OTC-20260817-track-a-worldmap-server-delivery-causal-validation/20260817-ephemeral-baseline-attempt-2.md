# OTC-20260817 — isolated baseline attempt 2

```yaml
evidence_date: 2026-08-17
task: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
pr: 475
runtime_access: ephemeral_isolated
namespace: worldmap-causal-baseline-ephemeral-v1
run_id: 32027454382
job_id: 95379752642
head: 11cd1566f9c104a828f62fcddfe974ce5bd7291b
result: FAILED_AT_UI_LOCATOR_BEFORE_SECRET_USE
credentials_used: false
login_submitted: false
gameplay_used: false
client_byte_mutation: false
```

## FACT — GDB environment repair solved the prior observer failure

The run revalidated current main ancestry, Track A admission and an idle canonical controller plane, then generated the previously statically validated GDB-environment repair.

Physical exact-client path again passed:

```text
WORLDMAP_BASELINE_PREEXISTING_NAMESPACE_PROCESS_COUNT=0
TRACK_A_CANONICAL_XRES_ADAPTER=PASS
WORLDMAP_BASELINE_EPHEMERAL_XRES_WORKER=PASS
TRACK_A_CANONICAL_STAGE=warp_egress_probe_pass
TRACK_A_CANONICAL_STAGE=xvfb_pass
TRACK_A_CANONICAL_STAGE=vnc_pass
TRACK_A_CANONICAL_STAGE=client_window_wait_pass
WORLDMAP_BASELINE_MANIFEST_FENCE=PASS
WORLDMAP_BASELINE_WINDOW_IDENTITY=x11-window:12582929
WORLDMAP_BASELINE_TARGET_UNIQUENESS=PROVEN
```

Most importantly, the repaired observer reached:

```text
WORLDMAP_BASELINE_PRE_STORAGE_OBSERVER=ARMED
```

This resolves the attempt-1 `gdb_observer_not_alive` gate and confirms the toolroot library-environment diagnosis from `20260817-gdb-environment-isolation.md`.

## FACT — the next stop was only unavailable OCR bootstrap tooling

Immediately after the observer was proven attached, before any screenshot OCR or secret-use operation, the helper stopped with:

```text
WORLDMAP_BASELINE_ERROR=tesseract_missing_before_secret_use
```

The protected email/password variables are consumed only after the UI-locator tooling gate. Therefore this run did not enter credentials, submit login or issue gameplay input.

The task will not install OCR into the shared runner. Retained exact-client artifacts now provide a bounded OCR-free replacement based on raw XWD geometry and pixel structure; see `20260817-ui-geometry-without-ocr.md`.

## FACT — cleanup remained clean

```text
WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS
WORLDMAP_BASELINE_CLEANUP=COMPLETE
```

No privacy-safe baseline artifact was uploaded because no login/world capture occurred.

## Gate classification

```yaml
pre_storage_observer_gate: PASS
ui_locator_gate: FAILED_TOOLING_UNAVAILABLE
ui_locator_failure_signature: tesseract_missing_before_secret_use
credentials_consumed: 0
login_budget_consumed: 0
semantic_worldmap_attempt_consumed: 0
next_hypothesis: raw_XWD_exact_geometry_classifier_from_retained_exact_client_artifacts
```

This is a new gate, not an observer retry. Any subsequent baseline run must preserve the now-proven GDB environment and replace only the UI locator. World entry remains acceptable only through actual FullMap/map-description structural evidence.
