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

## Corrected real edge transport E2E and narrow composition finding

A fresh full-mask Kasm capture was sent for real from Synology to Molehill through the accepted production `EdgeOutboundClient`. Mutual authentication, durable replay verification, heartbeat, signed artifact transfer, observation verification, artifact SHA/size validation, production PNG decode and authority-neutral `AgentEdgeBridge.accept()` all passed. Physical action count remained `0`; the transport is no longer a blocker.

The remaining failure is narrower. A production-only composition probe used the exact current client identity, successfully admitted read-only runtime and constructed a `RuntimeSignalResolver` with zero reviewed contracts. Issuing the composition-owned read-only authority then failed closed with `EDGE_RUNTIME_COMPOSITION_MISMATCH`. Concrete reviewed-contract instantiations in the checkout are test fixtures only, so the auditor did not import one merely to make `edge.current`. This exposes coupling between basic read-only admission currentness and semantic runtime-contract configuration. A bounded repair should allow admission-only currentness only with a zero-contract resolver; semantic runtime evidence must remain unavailable and reconciliation should safely remain `UNKNOWN` without stronger evidence.

## Post-860 final-generation restack

Admission-only authority repair #860 is merged to trusted `main@a7c7eb8aa2cc69d70442578401d88be9262055e4`. Refreshed Wave 2 head `2346ffb704c213f2e3050f87fc80aaa611454cd3` is coordinator-accepted under review `5091459576` with all associated workflows green. Wave 3 is restacked exactly onto that generation without implementation edits.

Fresh static validation passes `186/186` security/provenance tests, the two admission-only guards and current-client fence. Previous physical capture/Qwen and authenticated cross-host edge transport evidence remain successful historical gates. The only remaining physical check is a fresh admitted end-to-end trusted capture/vision/reconciliation run. Without reviewed semantic runtime evidence, the expected safe reconciliation result is `UNKNOWN` with `runtime_current=false`; no new daemon or runtime producer is required.

## Final observation endpoint interruption

The final post-#860 observation window did not produce a capture or model result. Molehill-PC is available and the task-owned local model host is fully stopped, but the authorized Synology Remote Desktop execution endpoint is offline while the NAS itself remains LAN-reachable. Existing noninteractive SSH/PuTTY authorization is not available, and no credentials or browser/DSM secrets were inspected to bypass that boundary. Existing self-hosted workflows were inspected without modification: the read-only Surveyor is pinned to an obsolete client fence, while the current-fence Kasm dispatch is a mutating bootstrap outside this auditor authority.

The stale `read_only` window is therefore closed fail-closed. `runtime_access` returns to `none`. Previous capture/Qwen and authenticated cross-host transport PASS evidence remains valid historical evidence, but a new fresh exact-target preflight and a new durable read-only admission are required before the single remaining `capture -> exact Qwen -> reconcile_vision()` gate.

## Final Wave 3 live closure ? 2026-09-03T07:54:46+02:00

After central-fence reconciliation and fresh Surveyor run `33718302097`, Wave 3 was restacked on accepted Wave 2 head `9db0ae43ab5b0ce6b0c9504eec723087f13d5271`. Encrypted KasmVNC was connected with `view_only=true`; the exact Qwen digest was verified with an empty model slot. The evidence-bearing capture was decoded only in memory and persisted only after the production full-frame secret mask. The resulting safe PNG is `b73b2b2c6626a91f03744b76f9ba59761c5122f047cfacd4c755bb15467393bc`, `762x272`, and every RGB byte is zero.

The production `AgentVisionSensor` completed on that exact safe evidence and the durable production `VISION_RECONCILED` event records `screen_class=UNKNOWN`, `state=UNKNOWN`, `runtime_state=UNKNOWN`, `runtime_current=false`, empty runtime evidence refs, the exact Qwen profile/digest, and `physical_effect=false`. No semantic runtime evidence was invented. Runtime access is released back to `none`; resident model count is zero, the task-owned model host/viewer are stopped, and physical action count remains `0`.

A first discarded acquisition failed before its consumer read any bytes because `PYTHONPATH` was absent; it produced no Qwen/reconciliation evidence and no raw-frame persistence. The accepted gate later completed; a post-result helper-name error was recovered from the durable SQLite event store without another capture. See `docs/agents/evidence/OTC-20260902-vision-p2-e2e-audit/final-wave3-live-e2e.md`. Classification: `PASS_EXPECTED_UNKNOWN_RUNTIME_NOT_CURRENT`.
