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


## Fresh Synology preflight (2026-09-02T10:14:09Z)

- Remote Desktop Commander device `Synology` / `c47a502e-1b72-4611-b2cd-0b92952ea3a4`: online.
- `otclient-track-a-kasmvnc`: running (`container id 1af4af4d67f5`; started `2026-08-29T06:26:42.111997309Z`).
- `DISPLAY=:1`: `DISPLAY_CONNECT=PASS`; dimensions `1024x768`.
- Tibia/client window grep: no match; root tree showed ordinary XFCE desktop/windows only.
- `pgrep -x client` in the designated container: no PID.
- scan of all running containers for `pgrep -x client`: no candidates.
- canonical `/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json`: `ABSENT`.

Admission consequence: `runtime_access` remains `none`; target uniqueness cannot be `PROVEN` for a non-existent official-client target. Phase 2 audit has no authority to launch/bootstrap/process-control the client, so the real read-only E2E remains blocked until an authorized runtime owner has an exact client already running. No screenshot/model inference/input/login/credential/process-control/memory/network-payload/mutation action occurred.


## Owner-authorized runtime setup and exact-fence recheck

The owner explicitly authorized starting the client and creating a desktop shortcut. The coordinator performed that setup outside the Wave 3 audit boundary. `/home/kasm-user/Desktop/Tibia.desktop` now launches a duplicate-safe wrapper for the current package client; no login/credential/character/gameplay input was performed.

The official launcher updated the package to `15.32.be4f48`. Fresh read-only process evidence after the temporary duplicate self-resolved:

- `CLIENT_PIDS=28379` (exactly one);
- executable: `/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client`;
- size: `52105824`;
- SHA-256: `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`;
- display: `:1.0`;
- visible top-level Tibia window bound to PID `28379`.

Trusted-base fence is still `15.32.75d4a0` / `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`. Therefore read-only admission is refused fail-closed and physical Vision P2 E2E remains blocked pending a separate reviewed fence advance.
