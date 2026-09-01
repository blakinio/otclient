# OTC-VISION-P2-CAPTURE-EDGE ? worker report

## Result classification

Repository/static implementation slice only. `runtime_access: none`; no Official Tibia runtime observation, screenshot, GUI input, process control, credentials, network payload capture, or physical action occurred. Physical action budget/count remain `0/0`.

## Implemented contract

- `RuntimeBinding` binds admitted read-only runtime provenance, container/display, PID/start identity, XID, exact-client fields and monotonic observation time.
- `KasmX11FfmpegFrameSource` exposes only dynamic `geometry()` and read-only `capture_rgb()` through fixed `xdotool getwindowgeometry --shell` and `ffmpeg -f x11grab`; stdin is disabled and command timeout is bounded.
- `ReviewedSecretMaskPolicy` is immutable and is supplied at trusted `CaptureEdge` composition time. It binds a reviewed policy id, exact expected frame dimensions, deterministic non-empty secret regions and content-addressed `policy_ref`.
- `CaptureEdge.capture()` has no per-call secret-policy parameter. Geometry/policy mismatch fails before RGB capture or persistence; configured regions are masked in memory before PNG encoding or crop derivation.
- Full frame and crop remain content-addressed by SHA-256; evidence binds runtime, geometry, monotonic time, full/crop hashes and `secret_policy_ref`.
- `CaptureEvidence.validated_vision_capture()` remains the only public conversion to existing `SecretSafeCapture` and rechecks current runtime binding, freshness and artifact integrity before vision handoff.

## Coordinator repair history

First review comment `5496909848` found that an empty caller policy could persist an unmasked frame and self-certify `secret_safe=True`. The first repair rejected empty masks.

Fresh re-review comment `5497472188` found the broader remaining gap: a caller could still provide a non-empty but incomplete mask on each capture request. The second repair removes secret-mask choice from the capture request surface entirely and binds the reviewed deterministic mask when the edge is constructed. No caller-authored proof token was added.

## Second repair TDD evidence

A focused RED required `ReviewedSecretMaskPolicy` at composition time and failed because the class did not exist. Additional tests require non-empty reviewed regions, exact policy/frame geometry, absence of `secret_policy` from `CaptureEdge.capture()`, successful in-memory masking and persisted `secret_policy_ref`. The minimal production change then made those tests GREEN.

## Fresh post-restack validation

Trusted base: `main@fb0c489f2ed166e872c4f197c6a78375a8576685` (includes promoted runtime-admission producer #838). Implementation head before this docs checkpoint: `f3b149e38bc1f49808295d6762522ac78e95e859`.

- focused capture-edge: **14/14 PASS**;
- capture-edge + existing vision evidence: **18/18 PASS**;
- targeted `py_compile`: PASS;
- Track A runtime governance against `fb0c489f2ed166e872c4f197c6a78375a8576685`: PASS;
- checkpoint validator: PASS;
- `git diff --check origin/main...HEAD`: PASS;
- changed paths: exactly the four worker-owned paths;
- public API audit: `CaptureEdge.capture()` has no secret-policy argument, `SecretSafetyPolicy` is absent, `ReviewedSecretMaskPolicy` is frozen.

## Nonclaims and handoff

No Linux/Synology/Kasm execution of the backend has been performed or claimed. Real read-only verification remains a later coordinator-assigned serialized observation window with fresh admitted runtime evidence. `docs/agents/MODULE_CATALOG.md` and `docs/agents/CHANGELOG.md` remain coordinator-owned and untouched. PR #827 remains Draft; the worker must not self-promote or merge.

## Exact-head GitHub verification

Earlier generations passed their own CI/governance but were superseded by coordinator secret-safety findings. Exact checkpoint head `1f550b658ca6f17c02f4aeec80fd01cc212122b5` passed GitHub CI run `33545702287` and Track A agent runtime governance run `33545701984`. The worker slice is returned to the coordinator for independent re-review; no live runtime claim or worker self-promotion is made.
