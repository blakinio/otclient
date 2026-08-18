# Experimental native account-auth helper

This helper is a deliberately separate, opt-in RUNTIME primitive for `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME`. It exists to invoke the exact official Linux client's original account-authentication method without operating the visual login form.

It is **not** part of the stable read-only runtime bridge API. The existing `otclient-tibia-runtime-bridge.so` remains unchanged and read-only.

## Build gate

Default build:

```sh
cmake -S tools/tibia_runtime_bridge -B /tmp/tibia-runtime-bridge
cmake --build /tmp/tibia-runtime-bridge --parallel
```

must not build the experimental helper.

Explicit opt-in build:

```sh
cmake -S tools/tibia_runtime_bridge -B /tmp/tibia-runtime-bridge-auth \
  -DOTCLIENT_TIBIA_RE_BUILD_EXPERIMENTAL_AUTH=ON
cmake --build /tmp/tibia-runtime-bridge-auth --parallel
```

adds:

```text
otclient-tibia-native-auth-experimental.so
```

Building the helper does not grant runtime authority. Loading it into the official client is invasive process instrumentation and remains RUNTIME-owned under current Track A admission/lease/identity governance.

## Exact client contract

The helper is fenced to:

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
game_client primary vptr offset: 0x3076908
Qt class: tibia::client::TGameClient
local QMeta method count: 44
cold-auth QMeta local method id: 17
method: onRequestLoginWithCredentials(QString,QString)
static method-17 target fence offset: 0xd06850
32-byte fence: 488b5110488b71084883c4485b5de92d389eff0f1f440000488bbfa009000048
```

These values are the promoted exact-SHA result from PR #505 and are rechecked at runtime before dispatch. The helper does not jump to `0xd06850`; it uses the address only as an exact-build/runtime instruction fence and invokes the named method through Qt on the object's owning thread.

## Credential boundary

Credential bytes must never be placed in:

- the textual Unix command;
- process arguments;
- environment variables;
- logs or workflow artifacts;
- screenshots;
- plaintext temporary files.

The controller API accepts an **already-open, sealed anonymous memfd**. It validates descriptor identity, bounded size and required seals without reading the credential payload, then passes the descriptor to the one-shot auth socket using Unix `SCM_RIGHTS`.

The memfd contains exactly one little-endian frame:

```text
u32 email_utf8_length
u32 password_utf8_length
email_utf8_bytes
password_utf8_bytes
```

Each value is `1..1024` bytes. The frame must have exact declared length, valid UTF-8 and no embedded NUL. The memfd must be sealed against write/grow/shrink and further seal changes before handoff.

This repository task intentionally does **not** implement the producer that obtains real credentials and fills the memfd. A later physical RUNTIME task must prove such a producer without first materializing credential values in env/argv/plaintext files.

## One-shot behavior

The experimental helper:

1. waits for Qt application availability;
2. verifies `/proc/self/exe` exact size and SHA before exposing its auth socket;
3. resolves the PIE base;
4. creates a mode-`0600` Unix socket at the non-secret `OTCLIENT_TIBIA_RE_AUTH_SOCKET` path;
5. accepts one same-UID connection;
6. accepts only command `AUTH_WITH_CREDENTIALS` and exactly one `SCM_RIGHTS` descriptor;
7. validates and reads the sealed memfd inside the helper;
8. schedules work onto the Qt application thread;
9. proves the method-17 instruction fence, unique `TGameClient`, exact class, exact local QMeta table/signature and thread affinity;
10. invokes `onRequestLoginWithCredentials` through Qt using two `QString` values;
11. best-effort wipes helper-owned raw/QString buffers;
12. closes all received descriptors and unlinks the auth socket after the single attempt.

A response with `invocation_dispatched=true` proves only that Qt accepted the original native method invocation. It is **not** proof of account authentication, 2FA completion, character login or `IN_GAME`. Those remain causal RUNTIME evidence gates.

## Experimental launcher

`experimental_auth_launcher.py` composes the separate auth helper beside the stable read-only bridge helper. It verifies the exact client SHA and requires distinct absolute read-only and auth socket paths. It does not accept credentials or credential paths.

The actual physical invocation remains forbidden until a separately admitted RUNTIME task owns the serialized Track A runtime and proves the protected memfd producer plus all current process/PIE/fence/object/thread gates.
