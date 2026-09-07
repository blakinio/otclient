---
task_id: OTC-20260907-native-login-proven-secret-ingress
status: implementing
agent: ChatGPT
session_id: native-login-proven-secret-ingress-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: native_login_secret_ingress_repair
phase: implementation_green_pending
branch: fix/OTC-20260907-native-login-proven-secret-ingress
base_branch: main
base_main: 6df3000baaaef13556984f0d23cc5f1012e6a8c6
execution_mode: chatgpt
execution_class: repository_only
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
mutation_authorized: false
physical_e2e_required: false
implementation_authorized: true
credentials_allowed: none
secret_values_logged: false
parent_task: OTC-20260906-native-login-physical-executor
depends_on:
  - OTC-20260905-control-center-native-login-start
blocks:
  - OTC-20260906-native-login-physical-executor
owned_paths:
  - .github/workflows/track-a-native-login-be4f48-proven.yml
  - .github/workflows/track-a-native-login-proven-secret-ingress-contract.yml
  - .github/scripts/track_a_native_login_be4f48_proven.py
  - tools/tibia_runtime_bridge/native_login_secret_ingress.py
  - tests/tools/tibia_runtime_bridge/test_native_login_proven_secret_ingress_contract.py
  - docs/agents/tasks/active/OTC-20260907-native-login-proven-secret-ingress.md
modules_touched:
  - Track A current be4f48 proven native-login executor
reuses:
  - PR #599 physically proven no-kill native relogin flow
  - PR #607 permanent bounded secret-ingress operator
  - PR #553 machine-local encrypted Synology secret vault
  - current be4f48 auth/character/runtime helpers
  - canonical lease/rebind/Gate B transitions
---

# OTC-20260907 — restore proven native-login secret ingress

## Objective

Remove the unproductive sidecar/relay credential transport from the current be4f48 physical-login critical path and reuse the physically proven #599/#607 bounded secret-ingress shape while preserving current exact-current helpers and canonical admission.

## Evidence and correction

- #599 physically proved native auth -> one native character -> CONFIRM_UNIQUE -> structural IN_GAME with `SECOND_SECRET_ATTEMPT=false`.
- #607 preserved the working ingress shape: credentials exist only in one bounded `secret-ingress` process invoked through `docker exec -e <name>`; values are not present in argv/logs and are unset immediately.
- #553 physically seeded a persistent encrypted vault on `synology-otclient-01` under `/work`.
- #963-#968 sidecar attempts repeatedly failed before credential access because the runner/Kasm topology does not provide the assumed cross-container FD/socket seam.
- Draft #969 was closed unmerged and the sidecar/relay repair chain is no longer on the critical path.

## Implemented design

1. Preserve the existing exact-current be4f48 replacement, helper sockets, auth/character helpers, canonical lease/rebind/recovery/Gate B and causal `gameWindowState` qualification.
2. Add Kasm-local `native_login_secret_ingress.py` to the trusted-main helper bundle.
3. The Synology worker decrypts the existing local encrypted vault only for the authorized auth operation and gives email/password only to the environment of one `docker exec`; Docker argv contains only the two environment variable names.
4. The Kasm-local ingress immediately pops both variables, disables core/dumpability, constructs the bounded credential frame, moves it to a fully sealed anonymous memfd, zeroes the mutable frame, and passes only that descriptor to the exact-current auth helper over its existing Unix socket using `SCM_RIGHTS`.
5. The corrected physical workflow uses a new explicit `/track-a-native-login-be4f48-proven PRECHECK|EXECUTE` trigger, so the historical sidecar workflow is not invoked.
6. No credentials are admitted in browser/API, CLI argv, task/PR text, logs, evidence or persistent plaintext files. No second credential-bearing attempt is allowed.
7. PR head remains repository-only. Physical qualification occurs only after merge and fresh PRECHECK.

## TDD

RED head `10c8b5df3ca4e6a90f69babb6ebdefa0e993dfb3`: dedicated run `34084566806`, job `101626028724`, failed with 12 expected assertions because the new ingress/worker/corrected workflow did not yet exist. No self-hosted physical execution or credential access occurred.

## Acceptance

- exact-current ingress fenced to `15.32.be4f48` / `52105824` / `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`;
- corrected physical workflow has no sidecar/proc-root/shm relay dependency;
- one auth attempt is local vault -> bounded `docker exec` ingress -> sealed memfd -> `SCM_RIGHTS`;
- raw credential values cannot be printed or placed in argv;
- exact-head hosted checks GREEN and PR-head self-hosted physical jobs SKIPPED;
- after merge: fresh PRECHECK -> one EXECUTE -> character_count=1 -> CONFIRM_UNIQUE -> causal IN_GAME or one exact new blocker.
