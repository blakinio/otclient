---
task_id: OTC-20260818-native-auth-protected-tty-source
status: validating
agent: ChatGPT
session_id: chatgpt-native-auth-protected-tty-20260818
session_role: implementer
project_lane: otclient
lane: P1-BRIDGE
track_id: official-client-re
task_kind: implementation
phase: validate
execution_mode: github_only
execution_reason: implement and validate a protected interactive secret source without touching the serialized physical runtime
branch: feat/OTC-20260818-native-auth-protected-tty-source
base_branch: main
base_main: ed09418b431c28087775b419f85bed404fa85d70
related_pr: 510
updated: 2026-08-18T09:43:00+02:00
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
validation_level: component
invocation_started_at: 2026-08-18T09:32:00+02:00
last_progress_at: 2026-08-18T09:43:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: draft-component
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
- Secret input uses preallocated mutable buffers; helper requires `mlock`, wipes those buffers before release and disables core dumps/dumpability before reading secrets.
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

PR #475 remains the serialized physical owner on head `135c808d40934e3f9dfafe8cb0efb83aade92858`. Its V24 workflow deliberately holds a no-secret/no-login exact client plus view-only VNC observer for up to 360 minutes; the latest durable owner reconciliation is still inside that declared window. The connector cannot currently prove the push-workflow terminal state, so current ownership remains fail-closed and this task stays `runtime_access:none`.

# Current implementation

Draft PR #510 now contains:

- `protected_auth_tty.py`: hidden controlling-TTY capture into required-mlock mutable buffers, RLIMIT_CORE=0/PR_SET_DUMPABLE=0, exact runtime identity validation, sealed anonymous memfd construction and delegation to the merged descriptor-only auth client;
- `PROTECTED_AUTH_TTY.md`: security and physical-use boundary;
- `test_protected_auth_tty.py`: synthetic pseudo-TTY, exact identity, wipe, seal and sanitizer tests;
- `track-a-native-auth-protected-tty.yml`: GitHub-hosted no-secret validation with exact dependency-blob fences.

The first aggregate CI snapshot on implementation head `027afb000e171d6a7dce7b09cbf8dd36d1fcc984` observed:

```text
CI 32112655654 = pending
Track A native auth bridge validation 32112655421 = in_progress
Track A protected TTY native-auth source 32112655515 = in_progress
Track A agent runtime governance 32112655470 = in_progress
```

No physical runtime or credential operation occurred.

# Checkpoint

```yaml
checkpoint_version: 2
status: validating
last_completed_step: opened Draft PR #510 and implemented the protected controlling-TTY -> sealed memfd source plus synthetic validation workflow while leaving PR #475 runtime untouched
blockers: []
next_action: inspect one aggregate snapshot of checks on the checkpoint descendant head; on failure inspect only the first causal failing job, otherwise perform final diff/security audit and freeze final evidence
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 2
  session_id: chatgpt-native-auth-protected-tty-20260818
  session_started_at: 2026-08-18T09:32:00+02:00
  checkpointed_at: 2026-08-18T09:43:00+02:00
  last_progress_at: 2026-08-18T09:43:00+02:00
  phase: component_validation
  exact_head: 027afb000e171d6a7dce7b09cbf8dd36d1fcc984
  pull_request: 510
  active_operation: draft component CI
  external_run_ids: [32112655654, 32112655421, 32112655515, 32112655470]
  operation_started_at: 2026-08-18T09:41:00+02:00
  wait_deadline_at: null
  check_generation: draft-component
  checks_used: 1
  status: active
  safe_to_resume: true
  resume_condition: PR #510 remains non-conflicting and runtime_access remains none
  next_action: inspect one aggregate snapshot of the checkpoint-descendant checks; if green, perform final diff/security audit; if failed, inspect only the first causal failing job
```
