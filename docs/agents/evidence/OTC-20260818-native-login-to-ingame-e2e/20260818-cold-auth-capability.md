# Native-login protected cold-auth capability boundary

Task: `OTC-20260818-native-login-to-ingame-e2e`

This checkpoint records the non-secret capability test performed after the current native character-selection model was proven empty and initial authentication therefore could not be legitimately skipped.

## Provenance

```text
HEAD=0f8c6e505fa9350f92ea9029f74969524c4f08de
RUN=32127178186
JOB=95680214790
RUNNER=synology-otclient-01
RESULT=SUCCESS
```

Before testing any cold-auth prerequisite, the workflow re-proved current governance, renewed the same controller authority without changing generations, and reran same-generation Gate B:

```text
TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true
TRACK_A_CANONICAL_LEASE_RENEW=true
TRACK_A_CANONICAL_LEASE_GENERATION=10
TRACK_A_CANONICAL_LEASE_EXPIRES_AT_EPOCH=1787051807
TRACK_A_CANONICAL_XRES_ADAPTER=PASS
TRACK_A_CANONICAL_GATE_B=PASS
TRACK_A_CANONICAL_LEASE_GENERATION=10
```

## Direct capability facts

The already-promoted protected credential producer imports successfully on the runner, but the GitHub Actions execution context has no real controlling terminal:

```text
NATIVE_LOGIN_COLD_AUTH_PROTECTED_PRODUCER_IMPORT=PASS
NATIVE_LOGIN_COLD_AUTH_CONTROLLING_TTY=false
NATIVE_LOGIN_COLD_AUTH_TTY_ERRNO=6
```

Linux errno `6` is `ENXIO`; opening `/dev/tty` therefore proved that this Actions job had no controlling TTY. The probe did not allocate a pseudo-terminal and did not read or write `/dev/tty`.

The currently admitted official-client process also was not launched through the experimental native-auth launcher and therefore does not have the one-shot helper preloaded or an auth socket already present:

```text
NATIVE_LOGIN_COLD_AUTH_HELPER_LOADED=false
NATIVE_LOGIN_COLD_AUTH_SESSION_AUTH_SOCKET_PRESENT=false
NATIVE_LOGIN_COLD_AUTH_SESSION_AUTH_SOCKET_COUNT=0
```

The helper path is launch-time by design: `tools/tibia_runtime_bridge/experimental_auth_launcher.py` places `otclient-tibia-native-auth-experimental.so` into `LD_PRELOAD` and supplies `OTCLIENT_TIBIA_RE_AUTH_SOCKET` before starting the exact client. The current canonical worker was intentionally bootstrapped without those launch-time additions.

## Secret boundary

No account material was requested or accessed:

```text
NATIVE_LOGIN_COLD_AUTH_SECRET_REQUESTED=false
NATIVE_LOGIN_COLD_AUTH_SECRET_READ=false
NATIVE_LOGIN_COLD_AUTH_METHOD_INVOKED=false
NATIVE_LOGIN_COLD_AUTH_LOGIN_PERFORMED=false
```

The same lease remained valid after the capability probe:

```text
TRACK_A_CANONICAL_LEASE_VALIDATE=true
TRACK_A_CANONICAL_LEASE_GENERATION=10
```

## Classification

```text
FACT: the running client has no reusable current native character model.
FACT: cold authentication is therefore required before this process can reach native character selection.
FACT: the current GitHub Actions execution context has no real controlling /dev/tty.
FACT: the current official-client process has no preloaded experimental native-auth helper and no auth socket.
FACT: the protected producer itself is present/importable.
FACT: no credential, OTP, login or GUI action was attempted.
BLOCKER_CLASS=EXTERNAL_ACTION_REQUIRED
```

The repository contract forbids replacing the missing real controlling TTY with Actions secrets/environment variables, stdin/getpass, a pseudo-TTY, plaintext files or GUI credential entry. It also forbids asking for credentials in chat.

A future continuation must first create a freshly admitted auth-helper-enabled exact-client runtime through the promoted launch-time helper path, then expose only the task-owned auth socket/identity fence to a human operator on a **real controlling Linux `/dev/tty`**. The human may enter account/password there; secret bytes must remain local and flow only through the sealed-memfd/SCM_RIGHTS path. If 2FA is subsequently required, the same no-chat/no-log local-secret rule applies to whatever exact native 2FA path is then proven.

## One-shot cleanup

The cold-auth capability workflow was removed immediately after the successful non-secret probe:

```text
WORKFLOW_REMOVAL_COMMIT=bfe1267af1c56f60731b9feac46c50955ad92299
```
