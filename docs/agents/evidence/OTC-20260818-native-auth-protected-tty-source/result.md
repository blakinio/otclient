# Protected TTY native-auth source result

Status: **IMPLEMENTATION / NOT RUNTIME PROVEN**  
Task: `OTC-20260818-native-auth-protected-tty-source`  
PR: `#510`

## Objective

Close the root secret-ingress gap for `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME` without using or automating the Tibia login form and without placing credentials in Git, argv, environment variables, logs, screenshots or plaintext files.

## Implemented boundary

```text
controlling Linux /dev/tty
  -> ECHO/ECHONL disabled
  -> required-mlock mutable account/password buffers
  -> RLIMIT_CORE=0 + PR_SET_DUMPABLE=0
  -> anonymous MFD_ALLOW_SEALING memfd
  -> exact length-prefixed credential frame
  -> F_SEAL_SEAL|F_SEAL_SHRINK|F_SEAL_GROW|F_SEAL_WRITE
  -> merged experimental_auth_client.auth_with_credentials_fd()
  -> exact PeerIdentityExpectation verification
  -> SCM_RIGHTS
  -> merged one-shot native-auth helper
```

No real credential or official-client process was used by this repository task.

## Runtime identity hardening

The non-secret runtime identity input is fail-closed:

- absolute path only;
- opened once with `O_RDONLY|O_NOFOLLOW|O_CLOEXEC`;
- validated with `fstat` as a regular file owned by the effective UID;
- group/world writable metadata rejected;
- JSON bounded to 4096 bytes;
- `(dev, ino, size, mtime_ns, ctime_ns)` must remain unchanged across the read;
- exact client version/size/SHA required:

```text
version=15.32.df7b29
size=51965216
sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

The downstream experimental auth client independently revalidates the actual Unix peer PID/start ticks/boot identity/executable before sending the credential descriptor.

## TTY / secret safety

- `/dev/tty` is the only secret-entry source;
- no stdin/getpass/env/argv/credential-file fallback;
- both account identifier and password are entered with terminal echo disabled;
- terminal attributes are restored in a nested `finally`, even if the cosmetic trailing-newline write fails;
- secret bytes are read directly into preallocated mutable buffers;
- `mlock` is required; failure aborts before secret use;
- mutable helper buffers are zeroed before unlock/release;
- credential memfd is anonymous and fully sealed before descriptor handoff;
- result output is allowlisted/sanitized and does not serialize credential/session fields.

## Component validation

Implementation/proving head before final evidence-only descendant:

```text
feb20e5acc0578ea1c8adb8a4964e393057d129b
```

Exact-head component runs:

```text
Track A protected TTY native-auth source
  run 32113217521 / job 95636990428 = SUCCESS
Track A native auth bridge validation
  run 32113217507 = SUCCESS
Track A agent runtime governance
  run 32113217564 = SUCCESS
repository CI
  run 32113217691 = in_progress at evidence freeze
```

Protected-TTY job stages all passed:

```text
merged native-auth dependency exact-blob fence = SUCCESS
synthetic pseudo-TTY + memfd tests = SUCCESS
unsafe-source fail-closed pattern audit = SUCCESS
real credential access = false
official client executed = false
runtime access = none
form UI used = false
```

An earlier repository CI generation on head `027afb000e171d6a7dce7b09cbf8dd36d1fcc984` failed only actionlint/ShellCheck `SC2251` on top-level `! grep` validation guards. Repair cycle 1 converted those guards to explicit `if grep ...; then exit 1; fi`; no secret/runtime acceptance rule was weakened.

## Fresh security audit

Material findings discovered and repaired before final freeze:

1. terminal restoration could be skipped if writing the cosmetic trailing newline failed — repaired with nested `finally`;
2. identity metadata used path-level check/stat/read operations with a TOCTOU window — repaired by one `O_NOFOLLOW` descriptor plus before/after `fstat` binding;
3. identity metadata lacked owner/write-mode checks — current effective UID and non-group/world-writable are now mandatory;
4. workflow negative greps triggered actionlint `SC2251` — repaired without weakening predicates.

Current audit result:

```text
FORM_UI_USED=false
OCR_USED=false
IMAGE_MATCHING_USED=false
COORDINATE_CLICK_USED=false
BLIND_TAB_RETURN_USED=false
STDIN_SECRET_FALLBACK=false
SECRET_ENV_INGRESS=false
SECRET_ARGV_INGRESS=false
PLAINTEXT_SECRET_FILE_INGRESS=false
REAL_CREDENTIAL_ACCESS=false
OFFICIAL_CLIENT_EXECUTED=false
RUNTIME_ACCESS=none
OPEN_MATERIAL_FINDINGS=0
```

## Physical runtime boundary

This task deliberately does not touch the current physical Track A runtime. PR #475 remains the known serialized owner inside its declared V24 no-secret/no-login observer window. Current push-run terminal state cannot be proven through the available connector, so takeover remains fail-closed.

A later RUNTIME invocation must freshly prove legal ownership/admission, exact current runtime identity and current #475 terminal/namespace cleanup before using this source.

## Non-claims

```text
PROTECTED_ROOT_SECRET_SOURCE_IMPLEMENTED=true
NATIVE_AUTH_INVOCATION_PERFORMED=false
ACCOUNT_AUTHENTICATION_PERFORMED=false
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=false
CAUSAL_PROOF=NOT_YET
```
