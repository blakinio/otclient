# GitHub Secrets re-entry — generation-11 capability-loss checkpoint

Task: `OTC-20260818-native-login-to-ingame-e2e`  
Branch: `runtime/OTC-20260818-native-login-to-ingame-e2e-v3`  
Base: `main@066a5ba8b1811ef61d3aa8ac2ff3fc3601fe7b9d`

## FACT — GitHub Secrets are available without disclosure

Presence-only hosted workflow:

```text
run: 32128651952
job: 95684712657
NATIVE_LOGIN_SECRET_EMAIL_PRESENT=true
NATIVE_LOGIN_SECRET_PASSWORD_PRESENT=true
NATIVE_LOGIN_SECRET_EMAIL_SHAPE_VALID=true
NATIVE_LOGIN_SECRET_PASSWORD_SHAPE_VALID=true
NATIVE_LOGIN_SECRET_PAIR_READY=true
```

The canonical secret names are `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD`. GitHub masked their values. No credential value was printed, persisted, committed, or returned to ChatGPT.

## FACT — current-main physical authority was re-established

No-client current-main inventory:

```text
run: 32129188467
job: 95686335148
lease status: released
lease generation: 10
registration generation: 2
registration lease generation: 10
no client observation: true
```

Generation-11 rebind transaction:

```text
run: 32129321883
job: 95686751815
TRACK_A_CANONICAL_REBIND=PASS
TRACK_A_CANONICAL_GATE_B=PASS
lease generation: 11
registration generation: 3
registration lease generation: 11
PID: 2658
process start ticks: 66643010
display: :99
window: x11-window:12582929
remote view mapping: PROVEN
secret access: false
login performed: false
```

## FACT — native-auth helper can be built deterministically off-host

The physical Synology runner has no `cmake`; bounded local build probe `32129514948 / 95687339670` stopped before configuration and performed no client observation, client mutation, or secret access.

Hosted Linux build `32129906446 / 95688521351` succeeded from the repository source:

```text
helper: otclient-tibia-native-auth-experimental.so
sha256: e5cd3f4c42c35000dce7ed5736bdf646fdb179119817f726a86f9e9637a82777
size: 63728
artifact id: 9321784436
artifact zip sha256: cb87d6f0ee1b5e4eb4c096c368ea53d55274f479be5fdaedbf5c1f24bde76608
hosted secret access: false
```

The dependent Synology staging job `32129906446 / 95688788481` downloaded the artifact successfully, including matching artifact ZIP digest, but stopped before artifact verification/staging because the canonical raw lease token was absent:

```text
TRACK_A_CANONICAL_LEASE_ERROR=token_file_missing
```

Therefore the helper was not installed into task-local Synology state and the running client was not touched.

## FACT — exact capability-loss cause

A superseded generation-11 rebind workflow run `32129514869 / 95687604400` started after generation 11 had already been established. Its shell executed:

```text
rm -f "$token" "$worker"
```

before its fail-closed precheck. It then refused because the expected released-generation-10 / registration-2/10 state was no longer current:

```text
NATIVE_LOGIN_SECRET_REENTRY_REBIND_PRECHECK_DRIFT=
  lease.status,
  lease.generation,
  lease.controller_task,
  lease.controller_session,
  reg.registration_generation,
  reg.lease_generation,
  reg.source_run
```

No new lease acquisition, rebind, client mutation, login, or secret access occurred in that superseded run. Its precheck ordering nevertheless deleted the task-local raw capability token for the already-active generation-11 lease.

The durable lease stores only the SHA-256 digest of the random capability. The raw 256-bit token cannot be reconstructed from the durable state and must not be fabricated.

## FACT — direct public lease status after capability loss

Status probe `32130384212 / 95690011684` succeeded with no client observation and no secret access:

```json
{
  "runtime_id": "track-a-canonical-live",
  "schema_version": 1,
  "status": "active",
  "generation": 11,
  "controller_task": "OTC-20260818-native-login-to-ingame-e2e",
  "controller_session": "chatgpt-native-login-e2e-20260818-v3",
  "acquired_at": 1787050685,
  "renewed_at": 1787050685,
  "expires_at": 1787053385,
  "expired": false,
  "released_at": null,
  "takeover_from": null
}
```

The same run proved:

```text
NATIVE_LOGIN_LOST_TOKEN_PATH_PRESENT=false
NATIVE_LOGIN_LOST_TOKEN_CLIENT_OBSERVATION=false
NATIVE_LOGIN_LOST_TOKEN_SECRET_ACCESS=false
```

`1787053385` is `2026-08-18T11:43:05Z`, i.e. `2026-08-18T13:43:05+02:00` (`Europe/Warsaw`).

## Disposition

The current generation-11 lease is authoritative but its raw controller capability is unavailable. Until its expiry, no token-authenticated canonical mutation, rebind, release, Gate-B transition, runtime replacement, helper staging, or secret-bearing login is legal.

The canonical lease implementation supports stale takeover only after expiry and requires an explicit takeover reason. Therefore the next legal transition is:

```text
at/after 2026-08-18T13:43:05+02:00:
  1. verify current main and PR/task authority;
  2. verify lease generation 11 is expired and token path is still absent;
  3. verify registration remains generation 3 / lease generation 11;
  4. acquire one stale takeover with explicit reason identifying run 32129514869;
  5. require new lease generation 12;
  6. rebind registration 3/11 -> 4/12;
  7. immediate same-generation Gate B;
  8. only then resume helper staging/runtime replacement and the owner-authorized GitHub Secrets -> sealed memfd -> native-auth path.
```

No credential has been consumed yet and no login attempt has been made in this GitHub-Secrets continuation.
