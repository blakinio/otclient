---
task_id: OTC-20260818-native-auth-with-credentials-bridge
status: validating
agent: ChatGPT
session_id: chatgpt-native-auth-bridge-20260818
session_role: implementer
project_lane: otclient
lane: P1-BRIDGE
track_id: official-client-re
task_kind: implementation
phase: final_exact_head
execution_mode: github_only
execution_reason: implement and validate a bounded experimental native-auth helper without touching the serialized physical runtime
branch: feat/OTC-20260818-native-auth-with-credentials-bridge
base_branch: main
base_main: ed6202216886ec31d432e4e7dec56b47626f10c4
related_pr: 507
updated: 2026-08-18T08:45:00+02:00
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
  - tools/tibia_runtime_bridge/experimental_auth.cpp
  - tools/tibia_runtime_bridge/experimental_auth_client.py
  - tools/tibia_runtime_bridge/experimental_auth_launcher.py
  - tools/tibia_runtime_bridge/EXPERIMENTAL_AUTH.md
  - tests/tools/tibia_runtime_bridge/test_bridge.py
  - .github/workflows/track-a-native-auth-bridge.yml
  - docs/agents/tasks/active/OTC-20260818-native-auth-with-credentials-bridge.md
  - docs/agents/evidence/OTC-20260818-native-auth-with-credentials-bridge/**
read_only_exact_blobs:
  tools/tibia_runtime_bridge/bridge.cpp: c47dc3e81162867692e7608f14a9f53dea52bf3b
  tools/tibia_runtime_bridge/ipc_client.py: 63bdb9258ce2c67781f43de8f4a482024fc89672
modules_touched:
  - tibia_runtime_bridge
reuses:
  - merged PR #505 exact native cold-auth QMeta contract
  - merged P1 runtime bridge from PR #414 without changing its stable read-only API
  - tools/tibia_runtime_bridge/profiles/tibia-15.32.df7b29.json game_client evidence
blocks: []
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one bounded experimental helper plus deterministic no-secret tests
validation_level: full
invocation_started_at: 2026-08-18T08:11:00+02:00
last_progress_at: 2026-08-18T08:45:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft-final-evidence
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Provide the smallest isolated experimental primitive required by `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME` to enter the official Linux client's original account-authentication logic **without using the login form**.

```text
sealed credential memfd
  -> exact admitted runtime identity
  -> SCM_RIGHTS
  -> one-shot experimental helper
  -> exact client + PIE/fence + unique TGameClient + QMeta/thread gates
  -> onRequestLoginWithCredentials(QString,QString)
```

# Final implementation boundary

The merged stable bridge surfaces are preserved byte-for-byte and contain no mutating command:

```text
tools/tibia_runtime_bridge/bridge.cpp
  c47dc3e81162867692e7608f14a9f53dea52bf3b
tools/tibia_runtime_bridge/ipc_client.py
  63bdb9258ce2c67781f43de8f4a482024fc89672
```

Mutation is isolated into:

- default-OFF CMake option `OTCLIENT_TIBIA_RE_BUILD_EXPERIMENTAL_AUTH`;
- separate `otclient-tibia-native-auth-experimental.so`;
- separate `experimental_auth_client.py`;
- separate `experimental_auth_launcher.py`;
- one separate auth socket and one connection/attempt.

The helper is exact-build fenced to client `15.32.df7b29`, size `51965216`, SHA `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`, `TGameClient` vptr `0x3076908`, local QMeta method count `44`, method id `17`, signature `onRequestLoginWithCredentials(QString,QString)`, and the promoted `0xd06850` 32-byte instruction fence.

The address is never exposed as a call primitive. Invocation is through Qt named QMeta machinery on the object's owning Qt thread.

# Secret and ownership boundary

- no credential value may enter textual IPC, argv, environment, logs, artifacts, screenshots or plaintext temporary files;
- the controller accepts only an already-open fully sealed anonymous memfd;
- the controller does not read/pread the credential payload;
- the controller requires explicit `PeerIdentityExpectation` and verifies the Unix peer before sending the descriptor;
- helper accepts exactly one `SCM_RIGHTS` descriptor and closes received descriptors even when the request is rejected/truncated;
- launcher refuses legacy `TIBIA_TEST_EMAIL/PASSWORD` in its environment;
- launcher refuses to replace an existing socket path;
- real credential acquisition/memfd creation remains a separate future RUNTIME producer and is not implemented here.

# Validation

Green component gate on implementation head `9534b1dd6f5451400e21a12248c1e12faa296cbc`:

```text
Track A native auth bridge validation
run=32108044508
job=95621417173
conclusion=SUCCESS
```

All job stages passed:

```text
no-secret synthetic unit tests=SUCCESS
stable bridge/client exact-blob proof=SUCCESS
default build=SUCCESS; experimental auth helper absent
explicit experimental build=SUCCESS with -Werror
```

The only later implementation-branch change before the final evidence checkpoint was validator hardening for launcher credential-env and socket-replacement fail-closed markers; no runtime/auth algorithm changed.

Two repair cycles were consumed and resolved:

1. missing `python3-pyelftools` in the dedicated workflow;
2. attempted import of a non-existent private response helper after restoring the stable client; the experimental response parser is now self-contained.

# Audit

Final diff/security audit after those repairs:

```text
stable_bridge_mutation=ABSENT
stable_ipc_client_mutation=ABSENT
arbitrary_rpc=ABSENT
raw_address_call_surface=ABSENT
explicit_runtime_identity_required=true
sealed_memfd_required=true
legacy_secret_env=REFUSED
existing_socket_replacement=REFUSED
real_credentials_used=false
official_client_executed=false
open_material_findings=0
```

Durable implementation evidence:

`docs/agents/evidence/OTC-20260818-native-auth-with-credentials-bridge/result.md`

# Non-claims

This task does not prove account authentication, 2FA, character login or `IN_GAME`. It has `runtime_access:none` and cannot satisfy physical E2E. A later RUNTIME consumer needs fresh legal Track A ownership plus a protected real-credential memfd producer.

# Checkpoint

```yaml
checkpoint_version: 4
status: validating
last_completed_step: full no-secret component build/test passed; final security audit has zero material findings; implementation frozen for final exact-head validation
blockers: []
next_action: require final exact-head native-auth validation, Track A governance and repository CI; if all pass, perform independent promotion review, ready-state required CI and protected merge without physical runtime execution
```
