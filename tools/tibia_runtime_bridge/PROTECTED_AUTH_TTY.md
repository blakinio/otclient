# Protected TTY secret source for native auth

This helper is the root secret-ingress boundary for the experimental form-less native authentication path. It is intentionally separate from the Tibia UI and from GitHub Actions secret/environment injection.

## Security contract

`protected_auth_tty.py` accepts no credential values or credential file paths. It reads the account identifier and password only from the controlling Linux `/dev/tty` with echo disabled.

Before secret entry it:

- rejects `TIBIA_TEST_EMAIL` / `TIBIA_TEST_PASSWORD` if present in the environment;
- disables core dumps;
- sets `PR_SET_DUMPABLE=0`;
- allocates small mutable secret buffers and requires `mlock` for them.

The two values are written directly into an anonymous `memfd_create(..., MFD_ALLOW_SEALING)` frame:

```text
u32 account_utf8_length
u32 password_utf8_length
account bytes
password bytes
```

The descriptor is sealed with:

```text
F_SEAL_SEAL | F_SEAL_SHRINK | F_SEAL_GROW | F_SEAL_WRITE
```

and passed to the already-merged `experimental_auth_client.auth_with_credentials_fd()` using `SCM_RIGHTS`.

The helper wipes its mutable TTY buffers before unlock/release. It prints only a small allowlisted result object such as `ok`, `command`, `invocation_dispatched`, `qmeta_method_id`, or a sanitized error category.

## Runtime identity

Physical use requires a non-secret absolute JSON file produced from the current admitted runtime. It must contain:

```json
{
  "boot_id_sha256": "<64 lowercase hex>",
  "pid": 123,
  "process_start_ticks": 456,
  "client_version": "15.32.df7b29",
  "client_size": 51965216,
  "client_sha256": "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
}
```

The file is identity metadata, not credential material. `experimental_auth_client` still revalidates the actual Unix peer and executable before sending the memfd.

## Physical invocation boundary

A future admitted RUNTIME session may run:

```sh
python3 -m tools.tibia_runtime_bridge.protected_auth_tty \
  --socket /absolute/task-owned/auth.sock \
  --identity-json /absolute/task-owned/runtime-identity.json
```

The command line contains no credential value. Both prompts are hidden on the controlling TTY.

If `/dev/tty` is unavailable the helper returns `EXTERNAL_INTERACTIVE_TTY_REQUIRED`. There is deliberately no fallback to stdin, environment variables, arguments, the Tibia login form, screenshots, OCR, clipboard automation or plaintext files.

## Non-claims

Building/testing this helper does not authenticate an account and does not authorize a runtime. Physical use still requires current Track A ownership/admission and the experimental auth helper from merged PR #507. Legitimate 2FA/device confirmation remains in the original client state machine.
