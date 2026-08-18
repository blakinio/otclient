# Native `AUTH_WITH_CREDENTIALS` bridge evidence

Task: `OTC-20260818-native-auth-with-credentials-bridge`  
PR: `#507`  
Status: **IMPLEMENTATION / NOT RUNTIME PROVEN**

## Objective

Implement a bounded experimental consumer of the promoted PR #505 form-less cold-auth contract while keeping the stable runtime bridge read-only.

```text
sealed anonymous credential memfd
  --SCM_RIGHTS-->
experimental one-shot local auth helper
  -> exact client/fence/TGameClient/QMeta/thread gates
  -> Qt invocation of onRequestLoginWithCredentials(QString,QString)
```

No official client is executed by this task and no real credential is accessed.

## Non-claims

This task does not prove:

- that a real account authenticated;
- that 2FA/device confirmation completed;
- that a character was selected or logged in;
- that the physical Track A runtime can currently load the helper;
- that a protected real-credential producer exists;
- that `CHARACTER ACTUALLY LOGGED INTO GAME` has been reached.

## Stable bridge isolation

The canonical stable source `tools/tibia_runtime_bridge/bridge.cpp` is intentionally outside this task's writable paths and must retain git blob:

```text
c47dc3e81162867692e7608f14a9f53dea52bf3b
```

It must not contain `AUTH_WITH_CREDENTIALS`.

The experimental helper is separately compiled only when:

```text
OTCLIENT_TIBIA_RE_BUILD_EXPERIMENTAL_AUTH=ON
```

The default is `OFF`.

## Secret boundary

The Python controller does not accept email/password values. It accepts only an already-open descriptor to a sealed anonymous memfd, validates only descriptor metadata/seals/size, and passes the descriptor over Unix `SCM_RIGHTS`.

Synthetic tests use only reserved fake values and prove that the receiver can still read the complete original frame, demonstrating that the Python client did not consume the payload before handoff.

The helper accepts one connection and one descriptor, validates exact frame shape/UTF-8/NUL bounds, then best-effort clears helper-owned byte/QString buffers after one invocation attempt.

A real credential producer is deliberately outside this task. Older `TIBIA_TEST_EMAIL` / `TIBIA_TEST_PASSWORD` environment injection is not an accepted producer for the native-login prompt.

## Exact native fence

```text
client=15.32.df7b29
size=51965216
sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
game_client_vptr=0x3076908
class=tibia::client::TGameClient
local_qmeta_method_count=44
cold_auth_method_id=17
signature=onRequestLoginWithCredentials(QString,QString)
cold_auth_target_offset=0xd06850
fence=488b5110488b71084883c4485b5de92d389eff0f1f440000488bbfa009000048
```

The target address is a runtime fence only. The helper invokes the named method through Qt on the object's owning thread; it exposes no direct-address or arbitrary-method RPC.

## Validation markers expected

```text
NATIVE_AUTH_TEST_CREDENTIALS=synthetic_only
NATIVE_AUTH_OFFICIAL_CLIENT_EXECUTED=false
NATIVE_AUTH_RUNTIME_ACCESS=none
NATIVE_AUTH_DEFAULT_BUILD_MUTATION_SURFACE=ABSENT
NATIVE_AUTH_STABLE_BRIDGE_BLOB=UNCHANGED
NATIVE_AUTH_EXPERIMENTAL_BUILD=PASS
NATIVE_AUTH_FORM_UI_USED=false
NATIVE_AUTH_SECRET_ENVIRONMENT_USED=false
NATIVE_AUTH_CLIENT_EXECUTED=false
```

Physical runtime use remains separately serialized by the current Track A owner/admission contracts.
