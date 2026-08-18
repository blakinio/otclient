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
phase: validate
execution_mode: github_only
execution_reason: implement and validate a bounded experimental native-auth helper without touching the serialized physical runtime
branch: feat/OTC-20260818-native-auth-with-credentials-bridge
base_branch: main
base_main: ed6202216886ec31d432e4e7dec56b47626f10c4
related_pr: 507
updated: 2026-08-18T08:31:00+02:00
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
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one bounded experimental helper plus deterministic no-secret tests
validation_level: component
invocation_started_at: 2026-08-18T08:11:00+02:00
last_progress_at: 2026-08-18T08:31:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft-component
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Implement the smallest non-generalized experimental helper needed by `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME` to invoke the original native account-authentication entry **without using the login form**:

```text
AUTH_WITH_CREDENTIALS
  -> one protected sealed-memfd received over Unix SCM_RIGHTS
  -> bounded binary credential frame read only inside the experimental helper
  -> unique exact-build tibia::client::TGameClient
  -> owning Qt thread
  -> exact QMeta method validation for onRequestLoginWithCredentials(QString,QString)
  -> Qt DirectConnection invocation of that named method
```

This task does not execute the official client, does not access credentials, does not log in and does not mutate any physical runtime.

# Isolation decision

Both merged stable surfaces remain byte-for-byte read-only:

```text
tools/tibia_runtime_bridge/bridge.cpp      blob c47dc3e81162867692e7608f14a9f53dea52bf3b
tools/tibia_runtime_bridge/ipc_client.py  blob 63bdb9258ce2c67781f43de8f4a482024fc89672
```

No `AUTH_WITH_CREDENTIALS` command is added to either stable server or stable client API.

Instead:

- CMake option `OTCLIENT_TIBIA_RE_BUILD_EXPERIMENTAL_AUTH` defaults `OFF`;
- only when enabled, build a separate `otclient-tibia-native-auth-experimental.so`;
- `experimental_auth_client.py` owns sealed-memfd validation and `SCM_RIGHTS` transport;
- `experimental_auth_launcher.py` composes the helper beside the unchanged stable bridge and supplies a separate non-secret auth socket path;
- the experimental helper serves exactly one connection/attempt, then closes and unlinks its auth socket;
- no arbitrary method/RPC/call-address surface exists.

# Hard design constraints

- No credential values in textual IPC, command line, environment variables, GitHub logs, artifacts or plaintext temp files.
- Experimental `auth_with_credentials_fd()` accepts an already-open FD and passes only that descriptor using `SCM_RIGHTS`; it does not read/stringify payload bytes.
- Runtime helper requires a sealed anonymous memfd (`F_GET_SEALS` plus write/grow/shrink/seal seals) and rejects ordinary files/pipes.
- Helper accepts exactly one ancillary FD and rejects missing/multiple/unexpected descriptors; received descriptors are closed even when the ancillary request is rejected/truncated.
- Binary secret frame is little-endian length-prefixed, bounded, non-empty, valid UTF-8 and rejects embedded NUL/trailing bytes.
- Helper-owned raw byte/QString buffers receive best-effort zeroing immediately after one invocation attempt.
- Helper independently verifies `/proc/self/exe` size/SHA for exact client `15.32.df7b29` before exposing the auth socket.
- Runtime method validation verifies exact class `tibia::client::TGameClient`, one unique primary-vptr `0x3076908` target, class-local method id `17` / signature `onRequestLoginWithCredentials(QString,QString)`, object thread affinity and exact 32-byte fence at rebased `0xd06850`.
- Invocation uses Qt QMeta machinery on the owning Qt thread; never jump directly to `0xd06850`.
- Success means only that Qt accepted the invocation. It must not fabricate/claim authentication success; later RUNTIME evidence must observe the legitimate auth state machine.
- 2FA/device confirmation remains untouched and proceeds through original client logic.

# Credential memfd frame v1

```text
u32 email_utf8_length
u32 password_utf8_length
email bytes
password bytes
```

Each field must be `1..1024` bytes; memfd size must exactly match the two lengths plus the 8-byte header. No trailing bytes are accepted.

# Current implementation

Implemented on Draft PR #507:

- separate default-OFF CMake target;
- one-shot exact-client-fenced C++ helper;
- separate experimental launcher;
- separate experimental FD client;
- same-UID Unix socket, exact-one-connection/exact-one-FD contract;
- sealed anonymous memfd metadata/seal validation without payload read in Python;
- exact-build vptr/QMeta/thread/instruction-fence runtime gates;
- Qt named invocation rather than raw target jump;
- synthetic Linux `SCM_RIGHTS` tests preserving the source FD offset across handoff;
- automated proof that stable bridge/server blobs remain unchanged;
- dedicated GitHub-hosted build/test workflow.

# Runtime boundary

A later separately admitted RUNTIME task may opt in to the experimental helper only after current Track A ownership/lease/identity gates allow mutation and a protected producer supplies an already-open sealed memfd without first placing credential values in env/argv/plaintext files. This implementation task does not authorize physical execution.

# Checkpoint

```yaml
checkpoint_version: 3
status: validating
last_completed_step: isolated all mutation into separate experimental helper/client/launcher, restored stable bridge and ipc client to exact main blobs, and started no-secret component validation
blockers: []
next_action: inspect the terminal native-auth bridge validation result on the current exact head; repair only the first causal build/test failure if present, otherwise perform final diff/security audit and exact-head closeout
```
