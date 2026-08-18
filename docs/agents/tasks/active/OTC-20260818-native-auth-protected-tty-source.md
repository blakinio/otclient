---
task_id: OTC-20260818-native-auth-protected-tty-source
status: ready
agent: ChatGPT
session_id: chatgpt-native-auth-protected-tty-20260818
session_role: implementer
project_lane: otclient
lane: P1-BRIDGE
track_id: official-client-re
task_kind: implementation
phase: final_exact_head
execution_mode: github_only
execution_reason: implement and validate a protected interactive secret source without touching the serialized physical runtime
branch: feat/OTC-20260818-native-auth-protected-tty-source
base_branch: main
base_main: ed09418b431c28087775b419f85bed404fa85d70
related_pr: 510
updated: 2026-08-18T09:50:00+02:00
risk: critical
implementation_authorized: true
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
mutation_authorized: false
research_status: IMPLEMENTATION_NOT_RUNTIME_PROVEN
ROUTING_CONTRACT: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
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
owned_paths:
  - tools/tibia_runtime_bridge/protected_auth_tty.py
  - tools/tibia_runtime_bridge/PROTECTED_AUTH_TTY.md
  - tests/tools/tibia_runtime_bridge/test_protected_auth_tty.py
  - .github/workflows/track-a-native-auth-protected-tty.yml
  - docs/agents/tasks/active/OTC-20260818-native-auth-protected-tty-source.md
  - docs/agents/evidence/OTC-20260818-native-auth-protected-tty-source/**
modules_touched:
  - tibia_runtime_bridge
reuses:
  - merged PR #505 native cold-auth QMeta contract
  - merged PR #507 experimental one-shot native-auth helper and SCM_RIGHTS client
blocks: []
context_pressure: low
context_growth: stable
context_score: 4
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one bounded protected secret-ingress helper plus deterministic no-secret tests
validation_level: full_component
invocation_started_at: 2026-08-18T09:32:00+02:00
last_progress_at: 2026-08-18T09:50:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft-final
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Objective

Provide the missing root secret source for `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME` without using the Tibia login form and without placing credentials in Git, argv, environment variables, logs, screenshots, packet evidence or plaintext temporary files.

```text
human operator on controlling Linux TTY
  -> hidden canonical-mode reads into required-mlock mutable buffers
  -> exact non-secret runtime identity
  -> anonymous sealed memfd frame
  -> merged experimental_auth_client.auth_with_credentials_fd()
  -> SCM_RIGHTS
  -> merged one-shot native-auth helper
```

This task does not read real credentials, execute the official client, log in, or touch PR #475's physical runtime.

# Final implementation boundary

`tools/tibia_runtime_bridge/protected_auth_tty.py` now provides:

- `/dev/tty` as the only secret input source;
- both account identifier and password captured with `ECHO|ECHONL` disabled;
- terminal restoration in nested `finally` even if the cosmetic trailing-newline write fails;
- preallocated mutable buffers that require `mlock` and are wiped before `munlock`;
- `RLIMIT_CORE=0` and `PR_SET_DUMPABLE=0` before secret entry;
- no stdin, getpass, credential argv, credential env, plaintext credential file or Tibia form fallback;
- anonymous `memfd_create(..., MFD_ALLOW_SEALING)` framing with `F_SEAL_SEAL|F_SEAL_SHRINK|F_SEAL_GROW|F_SEAL_WRITE`;
- exact-runtime identity JSON opened once with `O_NOFOLLOW|O_CLOEXEC`, owner/write-mode checks, bounded read and before/after `fstat` binding;
- exact official client fence `15.32.df7b29` / `51965216` / `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`;
- delegation only to the already-merged descriptor-only experimental auth client;
- allowlisted sanitized result fields only.

# Component validation

Exact proving implementation head:

```text
feb20e5acc0578ea1c8adb8a4964e393057d129b
```

Runs:

```text
Track A protected TTY native-auth source
  run 32113217521 / job 95636990428 = SUCCESS
Track A native auth bridge validation
  run 32113217507 = SUCCESS
Track A agent runtime governance
  run 32113217564 = SUCCESS
```

The protected-TTY job passed all stages:

```text
merged native-auth dependency exact-blob fence = SUCCESS
synthetic pseudo-TTY + memfd tests = SUCCESS
unsafe-source fail-closed pattern audit = SUCCESS
real credential access = false
official client executed = false
runtime access = none
form UI used = false
```

Repository CI run `32113217691` was still in progress when final evidence was prepared; final required CI must run on the frozen checkpoint descendant before promotion.

# Repair history

One repository-CI repair cycle was consumed. On earlier head `027afb000e171d6a7dce7b09cbf8dd36d1fcc984`, actionlint/ShellCheck rejected top-level negative `! grep` guards with `SC2251`. They were rewritten as explicit `if grep ...; then exit 1; fi` predicates without weakening the security contract.

# Fresh security audit

Material findings discovered during the final diff audit and repaired before freeze:

1. possible skipped TTY restoration if the trailing newline write failed;
2. identity-file path/stat/read TOCTOU;
3. missing identity owner and group/world-write checks;
4. actionlint-unsafe negative grep syntax in the validator.

Current audit:

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

Durable evidence:

`docs/agents/evidence/OTC-20260818-native-auth-protected-tty-source/result.md`

# Current physical-runtime boundary

PR #475 remains the last proven serialized physical owner on head `135c808d40934e3f9dfafe8cb0efb83aade92858`. Its V24 no-secret/no-login observer was declared to live for up to 360 minutes, and the latest durable reconciliation remains inside that window. The available connector cannot prove its push-run terminal state; therefore no runtime takeover, observation or mutation is authorized from this task.

# Non-claims

```text
PROTECTED_ROOT_SECRET_SOURCE_IMPLEMENTED=true
NATIVE_AUTH_INVOCATION_PERFORMED=false
ACCOUNT_AUTHENTICATION_PERFORMED=false
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=false
CAUSAL_PROOF=NOT_YET
```

# Checkpoint

```yaml
checkpoint_version: 3
status: ready
last_completed_step: protected TTY -> sealed memfd source passed exact-head component validation and fresh security audit with zero open material findings; final evidence persisted
blockers: []
next_action: inspect required checks on the frozen checkpoint-descendant head; if all pass, perform independent promotion review, mark PR #510 Ready and use protected merge without physical runtime execution
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 3
  session_id: chatgpt-native-auth-protected-tty-20260818
  session_started_at: 2026-08-18T09:32:00+02:00
  checkpointed_at: 2026-08-18T09:50:00+02:00
  last_progress_at: 2026-08-18T09:50:00+02:00
  phase: final_exact_head
  exact_head: 32a032474ac111eddab8f3c920ef07452faf9cab
  pull_request: 510
  active_operation: final exact-head validation
  external_run_ids: [32113217521, 32113217507, 32113217564, 32113217691]
  operation_started_at: 2026-08-18T09:50:00+02:00
  wait_deadline_at: null
  check_generation: draft-final
  checks_used: 0
  status: ready
  safe_to_resume: true
  resume_condition: PR #510 remains non-conflicting and runtime_access remains none
  next_action: inspect required checks on the frozen checkpoint-descendant head; if green, perform promotion review and Ready transition without physical runtime execution
```
