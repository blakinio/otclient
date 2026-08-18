---
task_id: OTC-20260818-native-auth-with-credentials-bridge
status: completed
agent: ChatGPT
session_role: coordinator_closeout
project_lane: otclient
lane: P1-BRIDGE
track_id: official-client-re
task_kind: implementation
phase: closed
branch: feat/OTC-20260818-native-auth-with-credentials-bridge
base_branch: main
updated: 2026-08-18T09:23:00+02:00
risk: critical
runtime_access: none
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
mutation_authorized: false
implementation_pr: 507
implementation_head: 3084dd8fc44818738639506af042a83d88ec2e7c
implementation_merge_commit: 2e6992da330e8a52d03b94b8d6a9de6fa79a6800
promotion_review_id: 4957882770
ownership_released: true
---

# Terminal result

PR #507 implemented and promoted the repository-side form-less native account-auth primitive required by `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME` while keeping the physical Track A runtime untouched.

The implementation preserves the merged stable runtime bridge server/client byte-for-byte and isolates mutation behind an explicit default-OFF experimental helper:

```text
sealed anonymous credential memfd
  -> exact admitted PeerIdentityExpectation
  -> SCM_RIGHTS
  -> one-shot experimental auth socket
  -> exact client/PIE/instruction fence
  -> unique tibia::client::TGameClient
  -> exact QMeta method 17 / onRequestLoginWithCredentials(QString,QString)
  -> owning Qt thread
  -> Qt named invocation
```

Stable read-only blobs preserved:

```text
tools/tibia_runtime_bridge/bridge.cpp
  c47dc3e81162867692e7608f14a9f53dea52bf3b
tools/tibia_runtime_bridge/ipc_client.py
  63bdb9258ce2c67781f43de8f4a482024fc89672
```

The experimental target is built only with `OTCLIENT_TIBIA_RE_BUILD_EXPERIMENTAL_AUTH=ON`; the default is `OFF`. The helper exposes no arbitrary method/address RPC and does not jump directly to `0xd06850`.

# Secret boundary

- credential values are forbidden in textual IPC, argv, environment, logs, artifacts, screenshots and plaintext temp files;
- the controller accepts only an already-open, fully sealed anonymous memfd and does not read/pread the payload;
- the controller requires an explicit exact runtime identity and verifies the Unix peer before descriptor transfer;
- descriptor transfer uses `SCM_RIGHTS`;
- helper accepts exactly one descriptor and closes received descriptors on rejected/truncated input;
- launcher refuses legacy `TIBIA_TEST_EMAIL` / `TIBIA_TEST_PASSWORD` environment ingress;
- launcher refuses to replace an existing socket path;
- a real credential acquisition/memfd producer is intentionally not implemented by this task.

# Validation and audit

Component proof:

```text
implementation component head=9534b1dd6f5451400e21a12248c1e12faa296cbc
Track A native auth bridge validation run=32108044508
job=95621417173
conclusion=SUCCESS
```

Final exact head:

```text
3084dd8fc44818738639506af042a83d88ec2e7c
native-auth validation=32108280027 SUCCESS
Track A governance=32108280028 SUCCESS
ready-state required CI=32108373298 SUCCESS
review_threads=0
promotion/security audit=ACCEPT_WITH_RUNTIME_NONCLAIMS
merge_commit=2e6992da330e8a52d03b94b8d6a9de6fa79a6800
```

Two bounded component repair cycles were consumed and resolved:

1. missing `python3-pyelftools` in the dedicated validator;
2. non-existent private response helper after restoring stable `ipc_client.py`; the experimental response parser became self-contained.

Final security audit had zero open material findings.

# Non-claims

```text
FORM_UI_USED=false
REAL_CREDENTIAL_ACCESSED=false
OFFICIAL_CLIENT_EXECUTED_BY_TASK=false
RUNTIME_ACCESS=none
ACCOUNT_AUTHENTICATED=false
TWO_FACTOR_COMPLETED=false
CHARACTER_LOGGED_IN=false
IN_GAME=false
```

This repository implementation is not physical-login proof. The next physical RUNTIME phase still requires a legal current Track A runtime owner/admission plus a protected real-credential producer that creates/seals the memfd without first materializing credential values in env/argv/plaintext files.

# Closeout

```yaml
result: DONE
repository_formless_auth_primitive_merged: true
physical_runtime_used: false
ownership_released: true
blocker: none_for_repository_implementation
next_action: in a fresh invocation, re-check current Track A runtime ownership/admission and only when legally free create a separately authorized RUNTIME task for protected real-credential memfd production plus physical native auth/2FA/character-login causal proof
```
