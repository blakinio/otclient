# OTC-20260902 Vision P2 fresh E2E audit report

## Current audit target

- programme: `OTC-VISION-P2-READONLY`;
- worker: `OTC-VISION-P2-E2E-AUDIT`;
- trusted main: `27f9bdd5f003c596529e7571343ae8bb053d5cff`;
- accepted Wave 2 integration: `34fbf6e2d693058ce03a583087816b25639e9cb3`;
- coordinator ACCEPT: review `5090102633`;
- Wave 3 remains `implementation_authorized:false`, mutation authority false, physical budget/count `0/0`, direct Codex usage `0`.

## Repository/static result

The fresh security/provenance matrix on the post-Qwen restack passes `184/184`. The repaired Qwen schema contract, trusted client fence and Track A runtime governance also pass. Historical broad-suite Windows-local failures remain classified as baseline/environment limitations rather than Wave 2 regressions.

## Physical result already proven

A fresh exact-target admission proved one official client bound to the current fence, PID/start/XID/display and all-container uniqueness. A new production Kasm/X11/ffmpeg capture completed in `8733 ms`; full-frame zero masking occurred before persistence, raw pixels were not persisted, and physical action count stayed `0`.

The repaired exact-Qwen production path then passed through `AgentVisionSensor` on byte-identical masked physical evidence:

- strict visual class `UNKNOWN`;
- visible-text count `0`;
- exact model-profile / evidence-ref / capture-SHA bindings;
- `visual_only=true`, `structural_authority=false`;
- model residency empty before and after;
- task-owned model host fully stopped after the run.

The former Qwen schema finding is therefore physically resolved.

## Correction of the remaining blocker

The previous report language classified the next step as `BLOCKED_REAL_DEPLOYMENT_MISSING` and suggested a new daemon plus reviewed runtime-signal producer. That conclusion was too broad and is superseded here.

The approved Phase 2 contract requires the **actual read-only edge transport path** to be exercised end-to-end. It does not require a permanently deployed daemon. The existing `EdgeOutboundClient`/channel already implements the approved outbound authenticated private-LAN transport, and the trusted composition already contains verifier/bridge/reconciliation consumers. A bounded one-shot control-side receiver using those production primitives can therefore satisfy the missing transport gate when it receives a real outbound connection and real observation/artifact traffic from Synology.

Likewise, absence of a reviewed-causal runtime producer is not itself a blocker for this Phase 2 E2E. Stronger runtime evidence is required to promote semantic state such as `IN_GAME`; without it, reconciliation may correctly remain `UNKNOWN`. The audit must not manufacture runtime evidence merely to avoid that result.

## Actual remaining gate

Current classification:

- static/security audit: PASS;
- secret-safe physical capture: PASS;
- repaired exact-Qwen physical inference: PASS;
- real authenticated Synology -> Molehill edge transport E2E: **NOT YET EXERCISED**;
- semantic result after that edge path: allowed to be `UNKNOWN` when no stronger reviewed runtime evidence exists;
- final independent audit/closeout: pending the missing edge-path evidence.

At the correction checkpoint the Molehill-PC Remote Desktop Commander execution endpoint is offline, so the one-shot receiver cannot be started from this session. This is an external availability gate, not proof of a missing architecture or a need to implement a new subsystem.

When Molehill is available, the audit must start again from `runtime_access:none`, freshly prove/admit the exact target, then run only the missing authenticated edge path using existing production transport/verifier/bridge/composition. No GUI input, credentials, login, gameplay, process-memory access, packet capture or client mutation is permitted.