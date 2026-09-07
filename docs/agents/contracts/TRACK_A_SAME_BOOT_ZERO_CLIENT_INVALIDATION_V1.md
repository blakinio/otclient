# Track A same-boot zero-client invalidation v1

```yaml
contract_id: TRACK_A_SAME_BOOT_ZERO_CLIENT_INVALIDATION_V1
recovery_mode: same_boot_zero_client_invalidation_v1
runtime_access: canonical_recovery
credentials_allowed: false
login_allowed: false
process_control_authorized: false
```

## Purpose

This contract defines one narrow **metadata-only** recovery for an authoritative canonical registration whose exact registered process died on the **same host boot** and where fresh fail-closed inventory proves that no official client remains. It exists for failed transactional replacement/startup cases; it is not rebind, stale-registration recovery with a live replacement, prior-boot invalidation, or bootstrap.

The transition may only make the authoritative registration absent. It MUST NOT launch, stop, signal, attach to, inject into, log in, select a character, send GUI input, inspect process memory, access credentials, or create another official-client process. After successful invalidation, creation is a separate **create-new canonical bootstrap** under a fresh bootstrap admission and lease.

## Required admission and authority

Execution is owner-triggered from exact trusted `main` on `synology-otclient-01`. The recovery task MUST declare `runtime_access: canonical_recovery`, `recovery_mode: same_boot_zero_client_invalidation_v1`, `credentials_allowed: false`, `login_allowed: false`, and `process_control_authorized: false`.

Before the invalidator runs, the workflow MUST acquire and validate a **newer canonical lease generation** for the recovery task. The invalidator MUST execute inside canonical lease `guard-run`; the guard supervisor holds `canonical-live-runtime/coordination.lock` continuously while validating the lease and while the metadata transition executes. The invalidator MUST verify that the active public lease identity and generation still match the guarded task/session and that `registration.lease_generation < current_lease_generation`.

## Fresh proof required under guard

The exact trusted-main Kasm bootstrap worker is reused as a read-only zero-client oracle. Under the held canonical guard it MUST freshly prove all of the following:

- one expected Kasm container and display;
- exact current package version/size/SHA;
- complete official-client candidate inventory with `candidate_count == 0`;
- no Tibia main window with `main_window_count == 0`;
- current boot identity is available;
- the registered PID/start identity is no longer present;
- the authoritative registration remains a private regular mode-0600 file;
- the registration exact client fence remains the current fence;
- **registration boot identity MUST equal current boot identity**;
- the registration has not changed since it was first read;
- the active recovery lease has not changed.

Any unreadable, ambiguous, mismatched, official-looking, reused-PID, lease-drift, registration-drift, container-drift, display-drift, window, candidate, or fence condition fails closed.

## Commit rule

Only after all required proof passes may the transition atomically rename `runtime-registration.json` to a private task-evidence tombstone inside the canonical state directory and fsync the directory. The authoritative path must then be absent. The tombstone preserves the original registration plus invalidation provenance; it is evidence, not authority and MUST NOT be renamed back into place by an operator.

This is a reviewed transition, not a manual edit of registration state. No caller may synthesize or rewrite PID, start ticks, boot identity, lease generation, display, runtime locator, candidate fingerprint, or client fence to make the proof pass.

## Postcondition and next transition

Success proves only:

```text
canonical_registration=ABSENT
candidate_count=0
main_window_count=0
credential_accessed=false
client_process_mutation=false
```

The recovery lease is then released. A separate canonical bootstrap task must freshly acquire bootstrap authority and use the existing reviewed `kasm-bootstrap` create-new transition. Normal canonical reuse or native-login PRECHECK is forbidden until create-new has committed and revalidated a new authoritative registration.

## Explicit non-authority

This contract does not authorize credentials, auth, login, relogin, character confirmation, gameplay, GUI input, process signals, restart, debugger attach, process-memory access, second-client creation before registration absence, manual registration replacement, prior-boot invalidation, Gate A bypass, Gate B bypass, or protected-main changes outside ordinary PR/CI/merge policy.
