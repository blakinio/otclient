# OTC-20260905 — Control Center native login START

## Objective

Integrate the existing Track A native official-client login lifecycle with TIBIA RE Control Center so an owner can request `START` from the portal and the admitted canonical official Linux client can progress through native account auth, native character selection and causal structural `IN_GAME`, then hand off to the existing post-login Control Center/agent surfaces.

This task is **Track A only**. Track B PR #284 and OTClient direct-wire compatibility are explicitly out of scope and are not dependencies.

## Ownership

```yaml
task_id: OTC-20260905-control-center-native-login-start
track_id: official-client-re
lane: RUNTIME/P1-BRIDGE integration
branch: feat/OTC-20260905-control-center-native-login-start
base_main: b6cf7402b4dbde59b2086f0982c7dcc711c3b5fc
execution_class_static: github_hosted
execution_class_physical: synology_physical_runtime
persistent_session_role: canonical_runtime_owner
physical_e2e_required: true
owned_paths:
  - tools/tibia_re_control_center/native_login_lifecycle.py
  - tools/tibia_re_control_center/control_domain.py
  - tools/tibia_re_control_center/control_api.py
  - tools/tibia_re_control_center/control_ui.py
  - tools/tibia_runtime_bridge/current_sha_native_login_gate.py
  - tools/tibia_runtime_bridge/experimental_auth.cpp
  - tools/tibia_runtime_bridge/experimental_character_control_current.cpp
  - tests/tools/tibia_re_control_center/test_native_login_lifecycle.py
  - tests/tools/tibia_re_control_center/test_package_b.py
  - tests/tools/tibia_runtime_bridge/**current-native-login**
  - docs/agents/tasks/active/OTC-20260905-control-center-native-login-start.md
modules_touched:
  - TIBIA RE Control Center Package B/D integration
  - Track A native runtime bridge
reuses:
  - merged native login E2E promotion #577
  - second one-shot native relogin proof #599
  - CanonicalTrackAAuthorityBridge post-IN_GAME guard
  - sealed memfd / SCM_RIGHTS secret ingress
  - canonical lease/rebind/Gate B/bootstrap transitions
  - exact-current client fence contract
depends_on:
  - current trusted main
  - TRACK_A_CURRENT_CLIENT_FENCE_V1.json
  - current canonical runtime admission
blocks: []
track_b_dependency: NONE
```

## Admission — claim / static implementation

```yaml
track_id: official-client-re
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
```

No live official-client observation or mutation is authorized by this static checkpoint. Reclassify and persist a fresh admission before physical work.

## Current exact client fence

```yaml
version: 15.32.be4f48
size: 52105824
sha256: 552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
platform: official_native_linux_only
```

Historical `ed5469...` native-login helper addresses are discovery evidence only. They must fail closed on `be4f48` until the auth, character selection, game-server progression and structural IN_GAME contracts are re-derived and independently validated for the current exact binary.

## Required architecture

```text
portal START
  -> Control API lifecycle request (no credentials in browser/API/RequestLedger)
  -> NativeLoginLifecycle bridge
  -> current Track A admission / canonical authority
  -> server-side one-shot secret producer
  -> sealed anonymous memfd + SCM_RIGHTS
  -> exact-current native auth helper
  -> original TGameClient authentication state machine
  -> authoritative native character model
  -> semantic character confirmation
  -> original game-server progression
  -> causal structural IN_GAME
  -> existing post-IN_GAME Package D / agent ownership
```

`STOP` must cancel/refuse lifecycle work safely and never manufacture a second session. Legitimate 2FA/CAPTCHA/device confirmation remains external and must surface as a safe blocking state; it is never bypassed.

## Secret boundary

- browser/API never sends email/password;
- RequestLedger never persists credentials;
- portal deployment contains no plaintext Tibia credential;
- no credential in argv, logs, evidence, screenshots, task/PR text or AI context;
- runtime uses the existing one-shot secret ingress only after fresh secret/runtime authority;
- no blind retries.

## Acceptance

1. Current `be4f48` native-login contracts are re-derived and exact-fenced; stale helper addresses cannot execute.
2. Control Center exposes an idempotent START lifecycle and safe status without accepting credentials.
3. Unbound/no-current-authority states fail closed with explicit safe reason codes.
4. STOP cancels/refuses pending lifecycle work and preserves single-session semantics.
5. Fake/synthetic lifecycle tests cover LOGIN -> CHARACTER_SELECTION -> IN_GAME, current-SHA mismatch, multiple-character decision, challenge/external-action, duplicate START, restart/recovery and STOP races.
6. Physical Synology E2E, only after fresh admission, proves one causal run from START to structural IN_GAME or records one exact evidence-backed blocker.
7. Portal is redeployed from the merged exact main and the final LAN URL is reverified.

## Current checkpoint

```yaml
status: IMPLEMENTING_STATIC
runtime_access: none
physical_runtime_touched: false
track_b_touched: false
next_action: implement current-build rebind tooling and lifecycle bridge with fail-closed synthetic tests
```
