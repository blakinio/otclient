---
task_id: OTC-20260906-native-login-physical-executor
status: implementing
agent: ChatGPT
session_id: native-login-physical-executor-20260906
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: physical_native_login_execution
phase: canonical_lease_executable_repair
branch: fix/OTC-20260906-native-login-lease-invocation
base_branch: main
created: 2026-09-06T17:35:00+02:00
updated_at: 2026-09-06T20:12:00+02:00
base_main: 330ef9d9bb11ddff5428d2a93123f194fa7f67d1
policy_version: 2
prompting_standard_version: 2.1
execution_mode: chatgpt
execution_reason: trusted-main canonical replacement, one-shot vault native login, unique character confirmation, and exact-current causal IN_GAME qualification
execution_class: persistent_physical_runtime
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
runtime_access: canonical_reuse_or_mutation
runtime_owner_task: OTC-20260906-native-login-physical-executor
runtime_namespace: canonical-live-runtime
physical_runtime_locator: synology:otclient-track-a-kasmvnc:display-1
canonical_registration: PRESENT
canonical_lease_generation: UNKNOWN
registration_lease_generation: UNKNOWN
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: REQUIRED_NOT_PROVEN
gate_b: REQUIRED_NOT_PROVEN
bootstrap: NOT_APPLICABLE
target_uniqueness: UNKNOWN
mutation_authorized: false
persistent_session_role: canonical_runtime_mutator
physical_e2e_required: true
implementation_authorized: true
credentials_allowed: machine_local_vault_one_shot_only
secret_values_logged: false
gui_input_authorized: false
process_control_authorized: true
physical_action_budget: bounded_exact_pid_replacement_and_native_login
run_scope: bounded_current_be4f48_native_login
continuation_policy: continue_until_real_stop
task_completion_policy: merge_then_physical_qualification
parent_task: OTC-20260905-control-center-native-login-start
owned_paths:
  - .github/workflows/track-a-native-login-be4f48-physical.yml
  - .github/scripts/track_a_native_login_be4f48_physical.py
  - .github/scripts/tibia-official-client-re-canonical-live-lease
  - tools/tibia_runtime_bridge/container_native_login_client.py
  - tools/tibia_runtime_bridge/native_login_fd_sidecar.py
  - tests/tools/tibia_runtime_bridge/test_native_login_physical_executor_contract.py
  - docs/agents/tasks/active/OTC-20260906-native-login-physical-executor.md
modules_touched:
  - Track A canonical runtime
  - Track A native auth bridge
  - Track A current causal IN_GAME qualification
reuses:
  - .github/scripts/tibia-official-client-re-canonical-live-lease
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
  - tools/tibia_runtime_bridge/profiles/tibia-15.32.be4f48.json
  - tools/tibia_runtime_bridge/experimental_auth.cpp
  - tools/tibia_runtime_bridge/experimental_character_control_current.cpp
  - tools/tibia_runtime_bridge/secret_vault.py
  - .github/scripts/track_a_game_window_state_qualification.py
depends_on:
  - OTC-20260906-be4f48-live-state-binding
  - OTC-20260906-native-login-vault-auth
blocks:
  - OTC-20260905-control-center-native-login-start
---

# OTC-20260906 — native-login physical executor

## Objective

Execute the smallest trusted-main canonical path that replaces the single exact-current `15.32.be4f48` official client with an instrumented exact-current instance, consumes the machine-local encrypted credential vault at most once through a sealed memfd, confirms a character only when the native character model proves exactly one entry, and establishes causal `gameWindowState == "INGAME"` before leaving the authenticated client running.

## Authority freeze

The branch and PR are repository-only. No self-hosted physical job may run PR-head code. Physical PRECHECK/EXECUTE is available only after merge through an owner comment and must check out exact trusted `main` and prove it still equals remote `main`.

Before any mutation, the live workflow must freshly acquire the canonical lease, perform any required generation rebind, prove Gate B and revalidate the same invariants inside the whole-lifetime `guard-run` critical section. A PID handoff or replacement is reconciled only through the existing `stale-registration-recovery` contract and a newer lease generation.

The task record deliberately remains fail-closed before physical execution: authoritative canonical registration is already `PRESENT`, but live lease generations are `UNKNOWN`, Gate A/B are not yet proven, target uniqueness is `UNKNOWN`, and `mutation_authorized` remains `false`. The trusted-main physical workflow establishes those transient facts at execution time; this branch does not pre-claim them.

## Secret boundary

Credential plaintext is forbidden from GitHub Secrets, workflow env, argv, stdin, task/evidence text and logs. The executor may consume only the existing machine-local encrypted vault and may perform at most one credential-bearing auth attempt.

Fresh runtime inventory proved that the GitHub runner itself is containerized, has no shared mount with Kasm and cannot see the host PID namespace. Therefore the former direct runner `memfd -> nsenter` path is not executable on the current topology.

The repair keeps the encrypted vault on Synology machine-local storage and never copies the vault key, certificate, CMS payload or credential plaintext into the Kasm filesystem. During owner-authorized EXECUTE only, after current Gate A/Gate B and a secret-free transport probe, one short-lived task-labelled transport sidecar may receive read-only bind mounts of the exact vault directory plus the exact trusted-main sidecar/vault helper files. That sidecar decrypts the vault once into a fully sealed anonymous memfd, enters only the Kasm mount namespace while already sharing its PID namespace, drops to the numeric `kasm-user` UID/GID in the existing namespace client, and hands only the sealed descriptor to the exact auth helper through `SCM_RIGHTS`. The sidecar is synchronous, non-persistent and does not launch a second official client.

A `PASS_WITH_PROCESS_HANDOFF` result remains fail-closed: the namespace client must explicitly return sanitized `fd_sent=true` after `sendmsg(SCM_RIGHTS)` before a fresh exact PID/start handoff can qualify. Ambiguous transport failure cannot be upgraded to success and never causes an automatic second secret attempt.

## Physical success

Success requires all of:

1. trusted-main current fence and unique canonical target;
2. a secret-free sidecar transport probe under current canonical authority before client replacement;
3. exact-PID controlled replacement with be4f48 bridge/auth/character helpers;
4. canonical recovery and Gate B for the replacement PID;
5. one successful native auth ingress with no retry;
6. native character state proves exactly one character and `CONFIRM_UNIQUE` dispatch succeeds;
7. exact-current read-only causal state observation after confirmation proves `gameWindowState == "INGAME"` on the admitted exact process;
8. authenticated canonical client remains running and no broad process cleanup is performed.

## TDD and validation evidence

Initial RED head `3cde9a55ead37a8035ef808b2de94d7711b6f040`:
- workflow run `34043036312`, job `101513088002`;
- 5 focused tests ran with exactly 2 errors because the worker and namespace FD client did not yet exist;
- the Synology physical job was skipped.

Fully green original executor head `1423b65ae97c783de84e7ba97591a1a9638616f0` was merged through PR #960 as protected `main` commit `65f6a96e099f77ce93ac5023456cf4a65c84b463`.

First merged PRECHECK `34046535436 / 101522467183` stopped before Synology because the standalone character helper had one `-Werror=unused-function`; PR #961 removed that dead helper and added an exact standalone compile gate, then merged as `09fe1e2ddd334b2e97d5e60f15ec5de4e9024ae7`.

Second merged PRECHECK `34046945750 / 101523685277` reached `synology-otclient-01`, exact trusted main and the helper bundle, then failed at `target_host_pid_namespace_not_visible`. The EXECUTE step was skipped; no vault decrypt, credential access, login or client mutation occurred.

Merged read-only IPC inventory PR #962 (`76f14ecc781f2b6dee17a27e692f9cfe1b6a574d`) was executed as run `34048659727`, job `101528184803`: `shared_mount_count=0`; runner and Kasm both use private PID/IPC modes; Kasm has no mounts; the runner has `/work`, `/runner` and `/var/run/docker.sock`; `credential_access=false`, `runtime_mutation=false`, `process_memory_access=false`. A fresh Remote Desktop Commander check also found the Synology host device offline, so direct host `nsenter` is not currently available.

Sidecar transport PR #963 merged as protected `main` `330ef9d9bb11ddff5428d2a93123f194fa7f67d1`. Trusted-main PRECHECK `34050218008 / 101532472331` passed exact current, target uniqueness, registration-current and sidecar metadata checks and terminated with `NATIVE_LOGIN_PHYSICAL_MUTATION=false` and `NATIVE_LOGIN_SECRET_ACCESS=false`.

The subsequent trusted-main EXECUTE `34050377214 / 101532897575` failed on the first canonical lease `acquire` with `Permission denied` when invoking `.github/scripts/tibia-official-client-re-canonical-live-lease`. This occurred before lease acquisition, Gate B, sidecar probe, client replacement, vault decrypt or credential send. Therefore runtime mutation remained false and the credential-bearing attempt count remains zero.

## Current repair

The canonical lease wrapper content is unchanged and its dedicated deterministic lease suite passes. Git tree inspection proved the wrapper blob was stored without an executable bit; replacing only its tree mode with `100755` produces a distinct tree while preserving the exact blob SHA. PR #964 is therefore a bounded executable-mode repair, not a lease semantics change.

This branch remains repository-only. After exact-head governance/lease/CI gates pass, merge the mode repair, rerun trusted-main PRECHECK, and only after PRECHECK PASS rerun owner-authorized EXECUTE. Because the prior EXECUTE stopped before vault access, that future run remains the first credential-bearing attempt.
