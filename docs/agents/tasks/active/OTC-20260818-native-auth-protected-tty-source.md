---
task_id: OTC-20260818-native-auth-protected-tty-source
status: implementing
agent: ChatGPT
session_id: chatgpt-native-auth-protected-tty-20260818
session_role: implementer
project_lane: otclient
lane: P1-BRIDGE
track_id: official-client-re
task_kind: implementation
phase: implement
execution_mode: github_only
execution_reason: implement and validate a protected interactive secret source without touching the serialized physical runtime
branch: feat/OTC-20260818-native-auth-protected-tty-source
base_branch: main
base_main: ed09418b431c28087775b419f85bed404fa85d70
updated: 2026-08-18T09:32:00+02:00
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
validation_level: focused
invocation_started_at: 2026-08-18T09:32:00+02:00
last_progress_at: 2026-08-18T09:32:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Objective

Provide the missing root secret source for `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME` without using the Tibia login form and without placing credentials in Git, argv, environment variables, logs, screenshots, packet evidence or plaintext temporary files.

The protected path is:

```text
human operator on controlling Linux TTY
  -> hidden canonical-mode reads into mutable locked buffers
  -> exact non-secret Gate-B identity JSON
  -> anonymous memfd frame
  -> full Linux seals
  -> existing experimental_auth_client.auth_with_credentials_fd()
  -> SCM_RIGHTS
  -> merged one-shot native-auth helper
```

This repository task does not read real credentials, does not execute the official client, does not log in and does not touch PR #475's current physical runtime.

# Hard constraints

- CLI accepts no email/password values, credential paths, environment-secret names or plaintext secret files.
- Real secret entry is only from `/dev/tty`; both account identifier and password are entered with terminal echo disabled.
- Secret input uses preallocated mutable buffers; helper best-effort locks those pages with `mlock`, wipes them before release and disables core dumps/dumpability before reading secrets.
- Build the credential frame directly into an anonymous `memfd_create(..., MFD_ALLOW_SEALING)` descriptor; no plaintext staging file.
- Require `F_SEAL_SEAL|F_SEAL_SHRINK|F_SEAL_GROW|F_SEAL_WRITE` before handoff.
- Load only non-secret runtime identity from an explicit absolute JSON path and require exact client `15.32.df7b29`, size `51965216`, SHA `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- Refuse execution when legacy `TIBIA_TEST_EMAIL` or `TIBIA_TEST_PASSWORD` exists in the process environment.
- Call only the already-merged bounded experimental auth FD client. No general RPC and no direct target-address invocation.
- Print only sanitized helper result categories; never echo or serialize input secret bytes.
- If `/dev/tty` is unavailable, fail closed with `EXTERNAL_INTERACTIVE_TTY_REQUIRED`; do not fall back to stdin, env, argv, GUI form automation or files.

# Acceptance

GitHub-hosted tests use synthetic values only and must prove:

- identity JSON exact-fence validation;
- environment-secret fail closed;
- pseudo-TTY echo is disabled during capture and terminal attributes are restored afterward;
- synthetic secret bytes enter a preallocated mutable buffer and are wiped after use;
- generated memfd frame has exact little-endian lengths/payload and all required seals;
- source has no `input()`, `getpass`, stdin secret path, credential-value CLI args or plaintext secret-file API;
- physical official client, Synology runtime and real credentials are not used.

# Current physical-runtime boundary

PR #475 remains the serialized physical owner on head `135c808d40934e3f9dfafe8cb0efb83aade92858`; its V24 workflow deliberately holds a no-secret/no-login client/VNC observer for up to 360 minutes. This task is `runtime_access:none` and must not observe, attach to, stop, inject into or otherwise mutate that runtime.

# Checkpoint

```yaml
checkpoint_version: 1
status: implementing
last_completed_step: live-state preflight confirmed PR #475 is still inside its V24 ownership window and merged #507 leaves protected root credential acquisition as the remaining safe-prep frontier
blockers: []
next_action: open a Draft PR and implement the no-secret protected TTY -> sealed memfd producer with deterministic pseudo-TTY/memfd tests
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 1
  session_id: chatgpt-native-auth-protected-tty-20260818
  session_started_at: 2026-08-18T09:32:00+02:00
  checkpointed_at: 2026-08-18T09:32:00+02:00
  last_progress_at: 2026-08-18T09:32:00+02:00
  phase: implementation
  exact_head: ed09418b431c28087775b419f85bed404fa85d70
  pull_request: none
  active_operation: none
  external_run_ids: []
  operation_started_at: null
  wait_deadline_at: null
  check_generation: draft
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: task branch remains non-conflicting and runtime_access remains none
  next_action: open Draft PR and implement protected_auth_tty.py plus synthetic tests
```
