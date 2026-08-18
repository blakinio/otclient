# Native `AUTH_WITH_CREDENTIALS` implementation result

Status: **IMPLEMENTED / NOT PHYSICAL-RUNTIME PROVEN**  
Task: `OTC-20260818-native-auth-with-credentials-bridge`  
PR: `#507`

## Implemented boundary

This task implements a deliberately separate, opt-in form-less account-auth primitive while preserving the merged stable bridge server and client byte-for-byte.

```text
already-open sealed anonymous memfd
  -> exact PeerIdentityExpectation gate
  -> SCM_RIGHTS descriptor transfer
  -> one-shot mode-0600 experimental auth socket
  -> exact client size/SHA + PIE target fence
  -> unique tibia::client::TGameClient (vptr 0x3076908)
  -> exact local QMeta method 17 / onRequestLoginWithCredentials(QString,QString)
  -> owning Qt thread
  -> QMetaObject::invokeMethod(... Qt::DirectConnection ...)
```

The helper never jumps directly to `0xd06850`; that address and its 32-byte sequence remain an exact-build runtime fence only.

## Stable API isolation

The task automatically proves these merged blobs remain unchanged:

```text
tools/tibia_runtime_bridge/bridge.cpp
  c47dc3e81162867692e7608f14a9f53dea52bf3b
tools/tibia_runtime_bridge/ipc_client.py
  63bdb9258ce2c67781f43de8f4a482024fc89672
```

Neither stable surface contains `AUTH_WITH_CREDENTIALS`. The experimental helper is built only with:

```text
OTCLIENT_TIBIA_RE_BUILD_EXPERIMENTAL_AUTH=ON
```

and the default is `OFF`.

## Secret boundary

The experimental Python client accepts only an already-open descriptor. It does not accept email/password values, does not read or pread the credential payload, and refuses to transfer the descriptor without an explicit exact runtime `PeerIdentityExpectation`.

The descriptor must be an anonymous memfd with exact bounded size and seals:

```text
F_SEAL_SEAL | F_SEAL_SHRINK | F_SEAL_GROW | F_SEAL_WRITE
```

Synthetic tests prove the descriptor arrives by `SCM_RIGHTS` with the original offset unchanged and the receiver can read the complete synthetic frame.

The experimental launcher fails closed when legacy `TIBIA_TEST_EMAIL` / `TIBIA_TEST_PASSWORD` are present and refuses to replace an already-existing socket path. Credential values remain forbidden in textual IPC, argv, environment, logs, artifacts, screenshots and plaintext temporary files.

A real producer that obtains credentials and creates/seals the memfd is intentionally **not** implemented here.

## Component validation

The implementation code was fully built/tested on head `9534b1dd6f5451400e21a12248c1e12faa296cbc`:

```text
Track A native auth bridge validation
run: 32108044508
job: 95621417173
conclusion: SUCCESS

steps:
- dependency install: SUCCESS
- no-secret bridge unit tests: SUCCESS
- stable bridge/client read-only proof: SUCCESS
- default build: SUCCESS, experimental helper absent
- explicit experimental build: SUCCESS with -Werror
```

The only later implementation-branch change before this evidence checkpoint was validation hardening that requires launcher secret-env and socket-replacement fail-closed markers; no runtime/auth algorithm changed.

Two bounded repair cycles preceded the green component gate:

1. workflow lacked `python3-pyelftools` required by the existing resolver;
2. experimental client referenced a non-existent private response helper after the stable client was restored byte-for-byte; response parsing was made self-contained.

## Security audit

Final implementation review found and repaired before closeout:

- stable bridge/server mutation surface was removed entirely from the task;
- stable `ipc_client.py` was restored exactly to main;
- auth requires explicit exact peer identity before FD transfer;
- memfd identity matching is anchored to `/memfd:` / `memfd:`;
- received ancillary descriptors are closed even on rejected/truncated requests;
- existing socket paths are refused rather than unlinked;
- legacy credential-bearing environment variables are refused;
- no arbitrary method/address/RPC command exists;
- `invocation_dispatched=true` is not treated as authentication success.

Open material security findings after these repairs: **0**.

## Non-claims

```text
FORM_UI_USED=false
OCR_USED=false
COORDINATE_CLICK_USED=false
BLIND_TAB_RETURN_USED=false
REAL_CREDENTIAL_ACCESSED=false
OFFICIAL_CLIENT_EXECUTED_BY_TASK=false
RUNTIME_ACCESS=none
ACCOUNT_AUTHENTICATED=false
TWO_FACTOR_COMPLETED=false
CHARACTER_LOGGED_IN=false
IN_GAME=false
```

Physical use remains a later separately admitted RUNTIME operation. It requires a current legal runtime owner plus a protected real-credential memfd producer. This task does not grant or exercise that authority.
