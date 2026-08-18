---
task_id: OTC-20260818-native-auth-with-credentials-bridge
status: implementing
agent: ChatGPT
session_id: chatgpt-native-auth-bridge-20260818
session_role: implementer
project_lane: otclient
lane: P1-BRIDGE
track_id: official-client-re
task_kind: implementation
phase: implement
execution_mode: github_only
execution_reason: implement and validate a bounded experimental native-auth bridge surface without touching the serialized physical runtime
branch: feat/OTC-20260818-native-auth-with-credentials-bridge
base_branch: main
base_main: ed6202216886ec31d432e4e7dec56b47626f10c4
updated: 2026-08-18T08:11:00+02:00
risk: critical
implementation_authorized: true
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
mutation_authorized: false
research_status: IMPLEMENTATION_NOT_RUNTIME_PROVEN
ROUTING_CONTRACT: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: consumer_of_runtime_evidence
PHYSICAL_E2E_REQUIRED: false
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
owned_paths:
  - tools/tibia_runtime_bridge/CMakeLists.txt
  - tools/tibia_runtime_bridge/bridge.cpp
  - tools/tibia_runtime_bridge/ipc_client.py
  - tools/tibia_runtime_bridge/README.md
  - tests/tools/tibia_runtime_bridge/test_bridge.py
  - docs/agents/tasks/active/OTC-20260818-native-auth-with-credentials-bridge.md
  - docs/agents/evidence/OTC-20260818-native-auth-with-credentials-bridge/**
modules_touched:
  - tibia_runtime_bridge
reuses:
  - merged PR #505 exact native cold-auth QMeta contract
  - merged P1 runtime bridge from PR #414
  - tools/tibia_runtime_bridge/profiles/tibia-15.32.df7b29.json game_client target
blocks: []
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one bounded experimental bridge operation plus deterministic no-secret tests
validation_level: focused
invocation_started_at: 2026-08-18T08:11:00+02:00
last_progress_at: 2026-08-18T08:11:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Implement the smallest non-generalized bridge primitive needed by `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME` to invoke the original native account-authentication entry **without using the login form**:

```text
AUTH_WITH_CREDENTIALS
  -> one protected credential FD received over Unix SCM_RIGHTS
  -> bounded binary credential frame read only inside the injected bridge
  -> unique exact-profile tibia::client::TGameClient
  -> owning Qt thread
  -> exact QMeta method validation for onRequestLoginWithCredentials(QString,QString)
  -> Qt DirectConnection invocation of that named method
```

This task does not execute the official client, does not access credentials, does not log in and does not mutate any physical runtime.

# Hard design constraints

- Existing stable bridge remains read-only by default.
- `AUTH_WITH_CREDENTIALS` is compiled only when an explicit experimental CMake option is enabled; default build must not expose the mutating command.
- No arbitrary method/RPC/call-address surface.
- No credential values in textual IPC, command line, environment variables, GitHub logs, artifacts or plaintext temp files.
- The Python client API accepts an already-open credential FD and passes that descriptor with `SCM_RIGHTS`; it must not read or stringify the secret payload.
- Bridge accepts exactly one ancillary FD for the auth command and rejects unexpected/multiple descriptors.
- Binary secret frame is length-prefixed, bounded, non-empty, valid UTF-8 and rejects embedded NUL.
- Bridge-owned byte/QString buffers receive best-effort clearing immediately after one invocation attempt.
- Runtime method validation must verify exact class `tibia::client::TGameClient`, exactly one validated `game_client`, class-local QMeta method id 17/signature `onRequestLoginWithCredentials(QString,QString)`, object thread affinity and the exact 32-byte `0xd06850` instruction fence after PIE rebinding.
- Invocation uses Qt's QMeta machinery on the owning Qt thread; do not jump directly to `0xd06850`.
- Success means only `QMetaMethod::invoke` accepted the call. It must not fabricate or claim authentication success; later RUNTIME evidence must observe the legitimate auth state machine.
- 2FA/device confirmation remains untouched and must proceed through the original client logic.

# Credential FD frame

Proposed v1 frame, little-endian:

```text
u32 email_utf8_length
u32 password_utf8_length
email bytes
password bytes
```

Each field must be `1..1024` bytes; exact frame size must match the declared lengths. No trailing bytes are accepted.

# Acceptance

Deterministic GitHub-hosted tests must prove at least:

- default CMake configuration leaves experimental auth disabled;
- Python client rejects invalid FD values and does not read the supplied credential FD before sending it;
- synthetic Unix server receives exactly one SCM_RIGHTS FD and can read a framed payload from it;
- normal `request()` commands never send ancillary FDs;
- source contract contains exact QMeta class/method/id/fence constants and no arbitrary execute command;
- bridge rejects auth when experimental build is disabled, FD missing/multiple, target zero/multiple, wrong class, method mismatch, thread mismatch, instruction fence mismatch, malformed frame, invalid UTF-8/NUL or invoke failure;
- no real credential values or official-client runtime are used.

# Runtime boundary

A later separately admitted RUNTIME task may build the experimental option and use it only after current Track A ownership/lease/identity gates allow mutation and after a protected producer supplies the already-open credential FD. This task does not authorize that physical execution.

# Checkpoint

```yaml
checkpoint_version: 1
status: implementing
last_completed_step: claimed isolated P1-BRIDGE implementation paths after confirming no open bridge PR owns them and PR #505 lifecycle is terminal
blockers: []
next_action: open the early Draft PR, then implement the compile-time-gated SCM_RIGHTS auth primitive and deterministic no-secret tests
```
