# OTC-VISION-P2-CAPTURE-EDGE — worker report

## Result classification

Repository/static implementation slice only. `runtime_access: none`; no Official Tibia runtime observation, screenshot, GUI input, process control, credentials, network payload capture, or physical action occurred. Physical action budget/count remain `0/0`.

## Implemented contract

- `RuntimeBinding` requires an explicit read-only admitted/unique runtime identity and binds provenance, container/display, PID/start identity, XID, exact-client fields, and monotonic observation time.
- `KasmX11FfmpegFrameSource` exposes only `geometry()` and `capture_rgb()`. It uses a fixed read-only command vocabulary: exact-bound `xdotool getwindowgeometry --shell` plus `ffmpeg -f x11grab` raw RGB capture through `docker exec`; stdin is disabled and command timeout is bounded.
- `CaptureEdge.capture()` rechecks runtime binding freshness before capture and equality/freshness after capture. Stale or changed binding fails before artifact persistence.
- Secret regions are masked in memory before PNG encoding or persistence. Optional crop bytes are derived only from the already-masked full frame and retain the parent full-frame SHA-256 binding.
- Full frame and crop are content-addressed by SHA-256. Deterministic metadata records blank/black classification and optional change-vs-previous-full-frame digest.
- `CaptureEvidence.validated_vision_capture()` is the only public conversion to the existing `SecretSafeCapture`; it rechecks current runtime binding, capture freshness, full/crop byte integrity, and crop-to-full parent binding before vision handoff.

## TDD evidence

Focused RED→GREEN cycles proved missing behavior before implementation for: module creation; secret masking/crop; stale binding; runtime binding drift; downstream integrity/currentness; blank/black classification; previous-frame change binding; fixed Kasm/X11/ffmpeg backend; geometry-drift refusal; final binding-race refusal; and removal of an unchecked public vision-conversion bypass.

## Local validation

- `python -m unittest tests/tools/tibia_re_vision/test_capture_edge.py` — PASS, 11/11.
- `python -m py_compile tools/tibia_re_vision/capture_edge.py tests/tools/tibia_re_vision/test_capture_edge.py` — PASS.
- `python -m unittest tests/tools/tibia_re_vision/test_evidence.py tests/tools/tibia_re_vision/test_capture_edge.py` — PASS, 15/15.
- `python .github/scripts/test_track_a_agent_runtime_governance.py --changed-from 0fe1ecb3569f1d8372209c857ab57f3b626c29ae --expected-branch feat/OTC-20260901-vision-p2-capture-edge` — PASS.
- `python tools/agents/checkpoint.py docs/agents/tasks/active/OTC-20260901-vision-p2-capture-edge.md --require-checkpoint` — PASS before this report checkpoint update.
- `git diff --check` — PASS before this report checkpoint update.

## Broader baseline findings

`tests/tools/tibia_re_control_center/test_agent_vision.py` produced 55 passing tests and one error in `test_capture_and_snapshot_os_errors_do_not_leak_paths_or_causes`. The identical error (`ModelSlotUnavailable: MODEL_INFERENCE_FAILED`) reproduces from a clean archive of committed head `dd40d914fa5d05cdf5ff2957cc798ee7aa336d9b`, with no capture-edge files present; it is therefore a pre-existing baseline failure outside this worker ownership.

`tests/tools/tibia_re_control_center/e2e_agent_foundation.py` stops in scenario A with `the repository foundation has no physical action budget` followed by Windows sqlite temporary-directory cleanup errors. The same failure reproduces from the clean committed baseline. This worker does not repair or reinterpret that existing E2E.

## Nonclaims and coordinator handoff

No Linux/Synology/Kasm runtime execution of the new backend has been performed or claimed. Real read-only verification requires a future coordinator-assigned observation window with fresh `runtime_access: read_only` admission and exact-target proof.

`docs/agents/MODULE_CATALOG.md` and `docs/agents/CHANGELOG.md` are shared coordinator-owned paths and are deliberately untouched despite the new reusable module. The coordinator must classify the worker slice and perform any required shared catalogue/changelog/integration update after acceptance. PR #827 must remain Draft and must not be self-merged by this worker.
## Exact-head GitHub verification

Implementation head `8685f7c6a8dae9e41d71f0acbe70a89a35a0ef38` passed GitHub `CI` run `33529034080` and `Track A agent runtime governance` run `33529033773`. PR #827 remained open, mergeable and Draft with exactly four changed files at the verified implementation head.
