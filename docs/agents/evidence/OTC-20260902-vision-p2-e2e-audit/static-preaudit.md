# Vision P2 Wave 3 deterministic pre-audit evidence

Target integration: `7d4bae503030a00a51fad409d46bc43a39ad2314`.
Trusted base: `8441fc1cce1600033b505d68ebc5c0141b337394`.
Fresh audit checkout branch: `test/OTC-20260902-vision-p2-e2e-audit`.

## Generation fence

- merge-base(audit checkout, accepted integration) = `7d4bae503030a00a51fad409d46bc43a39ad2314`.
- audit-only diff before this checkpoint: task + report only.
- no implementation file was edited by Wave 3.

## Tests

Security/provenance subset: `184/184 PASS`.
It covers foundation authority, runtime admission, runtime signals, authenticated edge transport/bridge, reconciliation, session persistence, trusted Vision P2 composition, replay atomicity, capture edge/evidence, and Ollama policy.

Broad Control Center discovery: `569 tests`, `5 errors`, `2 skipped`.
The five errors were isolated and each reproduced on clean `main@8441fc1...`:
- 3 route cases in `AgentApiTests.test_all_six_routes_exist_and_nonce_is_checked_before_routing` -> Windows `ConnectionResetError 10054`;
- `AgentApiTests.test_post_body_shapes_commands_and_transport_boundaries_are_preserved` -> Windows `ConnectionResetError 10054`;
- `AgentVisionSensorTests.test_capture_and_snapshot_os_errors_do_not_leak_paths_or_causes` -> `ModelSlotUnavailable: MODEL_INFERENCE_FAILED`.

Classification: baseline/local-environment limitations, not Wave 2 regressions. They remain explicit non-passing evidence.

## Physical runtime availability

At device discovery on 2026-09-02, both authorized Remote Desktop Commander registrations named `Synology` were offline. No physical runtime command was executed. Runtime access therefore remains `none`, physical action count remains `0`, and the mandatory real read-only E2E is blocked pending device availability.

Direct Codex worker/reviewer invocations used by Wave 3 through this evidence point: `0`.
