# OTC-20260902 Vision P2 fresh E2E audit report

## Audit target

- Programme: `OTC-VISION-P2-READONLY`.
- Worker alias: `OTC-VISION-P2-E2E-AUDIT`.
- Trusted `main` at dispatch: `8441fc1cce1600033b505d68ebc5c0141b337394`.
- Accepted Wave 2 integration head under audit: `7d4bae503030a00a51fad409d46bc43a39ad2314`.
- Wave 2 PR: #856; coordinator classification review: `5087863607` = `ACCEPT` for repository/integration scope only.
- Wave 2 exact-head required CI: terminal with `CI / Required` success and no failed/pending/null check conclusions.

## Independence and authority

This task is a fresh falsification/audit lane. It is not authorized to repair implementation code. Static audit begins with `runtime_access:none`. Real official-client observation may occur only after fresh read-only admission and exact target/runtime identity proof under the trusted Track A contracts.

Frozen authority remains: no credentials, login, relogin, character selection, gameplay, GUI input, anti-idle input, process control, process-memory access, packet/payload capture, mutation, or physical action. Physical action budget/count remain `0/0`.

## Required attacks

Attempt to falsify at minimum:

- exact target/client uniqueness and currentness fences;
- stale capture or runtime evidence becoming current;
- model/OCR content forging provenance, semantic state, or authority;
- secret-bearing capture reaching persistence/model/evidence;
- wrong peer or replayed transport evidence becoming current;
- restart/reconnect restoring stale authority;
- foreign/multiple model residency or parallel inference;
- `WORLD_VISUAL` promoting semantic in-game state without stronger reviewed runtime proof;
- nonzero physical action budget or a bound production executor;
- any forbidden input/login/process/memory/network behavior;
- misleading task/PR/ownership lifecycle.

## Evidence status

- Coordinator deterministic pre-audit: `COMPLETE` on a fresh checkout stacked exactly from `7d4bae503...`.
- Security/provenance subset: `184/184 PASS`.
- Broad Control Center discovery: `569 tests`, `5 errors`, `2 skipped`; all five errors reproduce identically on clean `main@8441fc1...`, so they are not Wave 2 regressions.
- Fresh independent model audit: `DEFERRED` until the physical E2E evidence exists, to avoid consuming the constrained Codex quota twice.
- Fresh runtime preflight/admission: `BLOCKED` because both authorized Remote Desktop Commander devices named `Synology` are offline.
- Real admitted read-only E2E: `BLOCKED` by the same runtime availability condition.
- Material Wave 2 finding from deterministic pre-audit: `NONE`.
- Direct Codex worker/reviewer invocations for Wave 3 so far: `0`.

## Completion rule

`PASS` requires exact-head evidence, fresh independent audit with zero open material findings, a real admitted read-only E2E on the canonical official-client runtime, physical action count `0`, no forbidden side effects, and truthful lifecycle state. Hosted/fake evidence cannot substitute for the physical read-only E2E.


## Deterministic pre-audit notes

The fresh checkout merge-base with the accepted Wave 2 generation is exactly `7d4bae503030a00a51fad409d46bc43a39ad2314`. Before this checkpoint, only the Wave 3 task/report existed above that generation.

The five broad-suite errors are outside Wave 2 changed paths and reproduce individually on clean `main@8441fc1cce1600033b505d68ebc5c0141b337394`: four Windows-local API connection resets and one vision test ending in `MODEL_INFERENCE_FAILED`. They are retained as baseline/environment evidence and are not silently counted as passing.

The required runtime contract was read from trusted base before attempting physical observation. Device discovery found both authorized `Synology` Remote Desktop Commander registrations offline, so no container, display, window, PID, screenshot, admission, model inference, or official-client access was attempted.
