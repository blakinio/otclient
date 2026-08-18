---
task_id: OTC-20260818-native-cold-auth-qmeta
status: validating
agent: ChatGPT
session_id: chatgpt-native-cold-auth-qmeta-20260818
session_role: researcher
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: discovery
phase: validate
execution_mode: github_only
execution_reason: exact-SHA deterministic QMeta recovery does not require serialized physical runtime
branch: research/OTC-20260818-native-cold-auth-qmeta
base_branch: main
base_main: bd167a8a9b4192b3c87c21423e2af37e897f5e79
related_pr: 505
updated: 2026-08-18T07:39:00+02:00
risk: high
implementation_authorized: true
research_status: DRAFT_NOT_PROMOTED
promotion_authority: coordinator_only
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
mutation_authorized: false
owned_paths:
  - .github/workflows/track-a-native-cold-auth-qmeta.yml
  - docs/agents/tasks/active/OTC-20260818-native-cold-auth-qmeta.md
  - docs/agents/evidence/OTC-20260818-native-cold-auth-qmeta/**
modules_touched: []
reuses:
  - PR #498 exact-SHA auth/session static evidence (DRAFT dependency)
  - PR #475 GameClient QMeta constants at head 135c808d40934e3f9dfafe8cb0efb83aade92858 (DRAFT dependency)
depends_on:
  - blakinio/otclient#498
  - blakinio/otclient#475@135c808d40934e3f9dfafe8cb0efb83aade92858
blocks: []
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed_client_lzma_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
context_pressure: medium
context_growth: stable
context_score: 6
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one bounded exact-SHA QMeta discriminator with independent paths and no runtime ownership
validation_level: focused
invocation_started_at: 2026-08-18T07:20:00+02:00
last_progress_at: 2026-08-18T07:39:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft-repair-1
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Objective

Recover, on the exact official native Linux client and without executing it, the Qt/QMeta invocation contract for:

```text
TGameClient::onRequestLoginWithCredentials(QString, QString)
```

This is strictly for `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME` cold authentication **without operating the login form**.

Forbidden target mechanisms remain OCR, screenshots as control input, coordinate clicks, blind Tab/Return, image matching or other form automation.

# Trust boundary

PR #498 and PR #475 are predecessor/research inputs. Load-bearing values are revalidated on the exact packed/unpacked SHA before promotion.

This task does not touch the official-client process, Synology runner, VNC observer, X11, credentials, sessions or login budget.

# Run 1 — exact result

PR #505 head `f4f7c903a30046ebf78ee884d8dc7658ed68d534`:

```text
workflow_run=32103383778
job=95608065258
result=FAIL
COLD_AUTH_EXACT_PACKED_SHA=PASS
COLD_AUTH_EXACT_CLIENT_SHA=PASS
COLD_AUTH_CLIENT_EXECUTED=false
COLD_AUTH_RUNTIME_ACCESS=none
COLD_AUTH_QMETA_CLASS=tibia::client::TGameClient
COLD_AUTH_QMETA_METHOD_COUNT=44
COLD_AUTH_QMETA_SIGNAL_COUNT=6
first_error=AssertionError: tibia::client::TGameClient
```

Classification: the failure was the worker's exact class-name assertion (`TGameClient`) being shorter than the exact QMeta class identity (`tibia::client::TGameClient`). It occurred before method enumeration. It is not evidence against the native cold-auth method.

# Repair 1

Commit `767d9f1bd38b7a35125105bc6ba86f0c486bfcbf` changes only the exact class identity assertion to:

```text
tibia::client::TGameClient
```

No semantic threshold or exact-client fence was weakened.

# Acceptance

Persist DRAFT evidence with:

```text
EXACT_PACKED_SHA=PASS
EXACT_CLIENT_SHA=PASS
TGAMECLIENT_QMETA_IDENTITY=PASS|FAIL
COLD_AUTH_METHOD_NAME=onRequestLoginWithCredentials
COLD_AUTH_METHOD_META_INDEX=<integer|UNKNOWN>
COLD_AUTH_ARGC=2|UNKNOWN
COLD_AUTH_ARG_TYPES=<QString,QString|UNKNOWN>
COLD_AUTH_METHOD_FLAGS=<value|UNKNOWN>
COLD_AUTH_DISPATCH_TARGET=<va|UNKNOWN>
COLD_AUTH_TARGET_EXECUTABLE=true|false|UNKNOWN
COLD_AUTH_TARGET_INSTRUCTION_FENCE=<hex|UNKNOWN>
CLIENT_EXECUTED=false
RUNTIME_ACCESS=none
```

Fail closed on SHA mismatch, inconsistent QMeta tables, ambiguous dispatch target, or missing method.

# Negative controls

- No live process-memory scan or client startup.
- No Synology/runtime use.
- No credentials or secrets.
- No method index inferred from historical UI behavior.
- No `onGameSessionConnected` / `onGameSessionLoginSuccessful` success shortcut.

# Checkpoint

```yaml
checkpoint_version: 2
status: validating
last_completed_step: exact-SHA run 1 isolated a namespaced-class assertion defect and repair 1 corrected only that parser assertion
blockers: []
next_action: inspect the first exact-head cold-auth discriminator result produced after this checkpoint commit and either persist the exact QMeta contract or apply at most one new evidence-based repair
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 1
  session_id: chatgpt-native-cold-auth-qmeta-20260818
  session_started_at: 2026-08-18T07:20:00+02:00
  checkpointed_at: 2026-08-18T07:39:00+02:00
  last_progress_at: 2026-08-18T07:39:00+02:00
  phase: validate_exact_qmeta_after_namespaced_class_repair
  exact_head: 767d9f1bd38b7a35125105bc6ba86f0c486bfcbf
  pull_request: 505
  active_operation: none
  external_run_ids: [32103383778, 32103555614]
  operation_started_at: null
  wait_deadline_at: null
  check_generation: draft-repair-1
  checks_used: 2
  status: ready
  safe_to_resume: true
  resume_condition: a fresh exact-head discriminator result exists after the checkpoint commit
  next_action: inspect that result and continue from its first material finding
```
