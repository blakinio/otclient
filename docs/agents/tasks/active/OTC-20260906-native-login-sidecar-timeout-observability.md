---
task_id: OTC-20260906-native-login-sidecar-timeout-observability
status: implementing
agent: ChatGPT
session_id: native-login-sidecar-timeout-observability-20260906
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: native_login_transport_observability_repair
phase: contract_red
branch: fix/OTC-20260906-native-login-sidecar-timeout-observability
base_branch: main
created: 2026-09-06T23:20:00+02:00
updated_at: 2026-09-06T23:20:00+02:00
base_main: 6df3000baaaef13556984f0d23cc5f1012e6a8c6
execution_mode: chatgpt
execution_class: repository_only
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
mutation_authorized: false
physical_e2e_required: false
implementation_authorized: true
credentials_allowed: none
secret_values_logged: false
run_scope: bounded_secret_free_sidecar_timeout_observability
continuation_policy: continue_until_real_stop
task_completion_policy: merge_then_parent_physical_qualification
parent_task: OTC-20260906-native-login-physical-executor
owned_paths:
  - .github/scripts/track_a_native_login_be4f48_physical.py
  - tests/tools/tibia_runtime_bridge/test_native_login_physical_executor_contract.py
  - docs/agents/tasks/active/OTC-20260906-native-login-sidecar-timeout-observability.md
modules_touched:
  - Track A native-login sidecar process observability
reuses:
  - tools/tibia_runtime_bridge/native_login_fd_sidecar.py
  - .github/scripts/track_a_native_login_be4f48_physical_base.py
depends_on:
  - OTC-20260906-native-login-physical-executor
blocks:
  - OTC-20260906-native-login-physical-executor
---

# OTC-20260906 — native-login sidecar timeout observability

## Objective

Preserve bounded secret-free sidecar evidence when `docker run` itself exceeds the worker timeout, without logging raw stderr, host paths, credentials or arbitrary exception text.

## Live evidence

Trusted-main EXECUTE `34060567519 / 101560313624` on `6df3000baaaef13556984f0d23cc5f1012e6a8c6` passed PRECHECK, lease generation 50, canonical rebind and Gate B, then failed before the secret-free relay probe produced an artifact with `sidecar_probe_process_failed`.

The log proves `NO_SECRET_ACCESS_BEFORE_SIDECAR_PROBE=true`. The sanitized artifact is again 383 bytes / one file, so replacement, vault decrypt, auth, character confirmation and causal IN_GAME were not reached. Credential-bearing auth attempt count remains `0`.

## Root cause boundary

The public worker currently calls the base `_run()` helper for sidecar `docker run`. Base `_run()` converts `subprocess.TimeoutExpired` into generic `PhysicalError(command_failed:docker)`, discarding any partial allowlisted stdout from the sidecar. The public wrapper then reports only `sidecar_probe_process_failed`.

## Repair design

1. Add a probe-only runner in the public overlay using the same clean environment and command.
2. On normal completion, behavior is unchanged.
3. On `TimeoutExpired`, inspect only partial stdout; if its final line is a valid sidecar JSON response with an allowlisted static error, surface `sidecar_probe_client_<code>`.
4. Otherwise surface static `sidecar_probe_process_timeout`.
5. Never serialize timeout exception text or raw stderr.
6. Keep auth execution, secret handling, replacement and character logic unchanged.
7. PR head remains repository-only; self-hosted physical jobs stay skipped.

## Acceptance

- TDD RED demonstrates main lacks timeout/partial-stdout preservation;
- timeout without valid allowlisted stdout becomes `sidecar_probe_process_timeout`;
- timeout with valid allowlisted partial stdout preserves only the static sidecar error code;
- raw stderr and exception strings remain absent;
- exact-head hosted CI GREEN; PR-head physical jobs SKIPPED;
- after merge, parent may run a fresh PRECHECK and one EXECUTE because credential-bearing attempt count remains 0.
