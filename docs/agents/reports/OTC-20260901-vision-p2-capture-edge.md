# OTC-VISION-P2-CAPTURE-EDGE — worker report

## Result classification

Repository/static implementation slice only. `runtime_access: none`; no Official Tibia runtime observation, screenshot, GUI input, process control, credentials, network payload capture, or physical action occurred. Physical action budget/count remain `0/0`.

## Implemented contract

- `RuntimeBinding` requires an explicit read-only admitted/unique runtime identity and binds provenance, container/display, PID/start identity, XID, exact-client fields, and monotonic observation time.
- `KasmX11FfmpegFrameSource` exposes only `geometry()` and `capture_rgb()`. It uses a fixed read-only command vocabulary: exact-bound `xdotool getwindowgeometry --shell` plus `ffmpeg -f x11grab` raw RGB capture through `docker exec`; stdin is disabled and command timeout is bounded.
- `CaptureEdge.capture()` rechecks runtime binding freshness before capture and equality/freshness after capture. Stale or changed binding fails before artifact persistence.
- Secret regions are masked in memory before PNG encoding or persistence. An empty caller policy is rejected with `CAPTURE_SECRET_POLICY_UNPROVEN` before frame-source use or persistence; optional crop bytes are derived only from the already-masked full frame and retain the parent full-frame SHA-256 binding.
- Full frame and crop are content-addressed by SHA-256. Deterministic metadata records blank/black classification and optional change-vs-previous-full-frame digest.
- `CaptureEvidence.validated_vision_capture()` is the only public conversion to the existing `SecretSafeCapture`; it rechecks current runtime binding, capture freshness, full/crop byte integrity, and crop-to-full parent binding before vision handoff.

## TDD evidence

Focused RED→GREEN cycles proved missing behavior before implementation for: module creation; secret masking/crop; stale binding; runtime binding drift; downstream integrity/currentness; blank/black classification; previous-frame change binding; fixed Kasm/X11/ffmpeg backend; geometry-drift refusal; final binding-race refusal; removal of an unchecked public vision-conversion bypass; and the coordinator-returned unproven empty secret-policy path.

## Local validation

Post-repair, post-restack validation on implementation head `87dd4b914f471fd70e5e632fad69edbfce86f888`:

- `python -m unittest tests/tools/tibia_re_vision/test_capture_edge.py -q` — PASS, 12/12.
- `python -m unittest tests/tools/tibia_re_vision/test_evidence.py tests/tools/tibia_re_vision/test_capture_edge.py -q` — PASS, 16/16.
- targeted `py_compile` — PASS.
- Track A runtime governance against trusted main `54a20bbd8721e92d069974af14d6ebd2f4f5a55d` — PASS.
- `git diff --check origin/main...HEAD` — PASS; exact changed paths remain the four worker-owned paths.
- AST/surface audit — PASS: `shell=True=0`, production `no_secret_fields()` calls = 0, fail-closed unproven-policy guard present.

## Coordinator repair cycle

Coordinator comment `5496909848` correctly found that the previous generation allowed `SecretSafetyPolicy.no_secret_fields()` to persist an unmasked frame and self-certify `secret_safe=True`. A focused RED reproduced that exact behavior. The minimal repair rejects any empty `secret_regions` policy before runtime binding/frame-source use or persistence. Existing success fixtures now use explicit deterministic masking; no caller-authored proof token or new authority surface was introduced.

The branch was restacked conflict-free onto trusted `main@54a20bbd8721e92d069974af14d6ebd2f4f5a55d` before final local verification. No live capture was performed. Exact-head GitHub verification is pending publication of this repair generation.

## Broader baseline findings

`tests/tools/tibia_re_control_center/test_agent_vision.py` produced 55 passing tests and one error in `test_capture_and_snapshot_os_errors_do_not_leak_paths_or_causes`. The identical error (`ModelSlotUnavailable: MODEL_INFERENCE_FAILED`) reproduces from a clean archive of committed head `dd40d914fa5d05cdf5ff2957cc798ee7aa336d9b`, with no capture-edge files present; it is therefore a pre-existing baseline failure outside this worker ownership.

`tests/tools/tibia_re_control_center/e2e_agent_foundation.py` stops in scenario A with `the repository foundation has no physical action budget` followed by Windows sqlite temporary-directory cleanup errors. The same failure reproduces from the clean committed baseline. This worker does not repair or reinterpret that existing E2E.

## Nonclaims and coordinator handoff

No Linux/Synology/Kasm runtime execution of the new backend has been performed or claimed. Real read-only verification requires a future coordinator-assigned observation window with fresh `runtime_access: read_only` admission and exact-target proof.

`docs/agents/MODULE_CATALOG.md` and `docs/agents/CHANGELOG.md` are shared coordinator-owned paths and are deliberately untouched despite the new reusable module. The coordinator must classify the worker slice and perform any required shared catalogue/changelog/integration update after acceptance. PR #827 must remain Draft and must not be self-merged by this worker.
## Exact-head GitHub verification

Historical implementation head `8685f7c6a8dae9e41d71f0acbe70a89a35a0ef38` and checkpoint head `cc957a25ddb4c40e1416bec60eff03c38fda3ad9` passed their earlier CI/governance, but that generation is superseded by coordinator secret-safety finding `5496909848`.

Current repair implementation head before this docs checkpoint is `87dd4b914f471fd70e5e632fad69edbfce86f888`. Exact-head GitHub CI/governance is pending after publication; no success is claimed until those workflows complete.
