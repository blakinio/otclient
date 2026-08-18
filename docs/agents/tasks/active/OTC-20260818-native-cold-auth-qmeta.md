---
task_id: OTC-20260818-native-cold-auth-qmeta
status: waiting
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
updated: 2026-08-18T07:42:00+02:00
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
ci_checks_for_current_head: 2
ci_check_generation: draft-repair-1
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 1
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Objective

Recover the exact Qt/QMeta invocation contract for:

```text
TGameClient::onRequestLoginWithCredentials(QString, QString)
```

for `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME`, specifically to authenticate through original native client logic **without using the login form**.

Form automation is not an acceptable target mechanism: no OCR, image matching, coordinate clicks, blind Tab/Return or GUI-field operation.

# Verified progress

Run `32103383778` / job `95608065258` on PR #505 head `f4f7c903a30046ebf78ee884d8dc7658ed68d534` independently proved:

```text
COLD_AUTH_EXACT_PACKED_SHA=PASS
COLD_AUTH_EXACT_CLIENT_SHA=PASS
COLD_AUTH_CLIENT_EXECUTED=false
COLD_AUTH_RUNTIME_ACCESS=none
COLD_AUTH_QMETA_CLASS=tibia::client::TGameClient
COLD_AUTH_QMETA_METHOD_COUNT=44
COLD_AUTH_QMETA_SIGNAL_COUNT=6
```

The first failure was only the worker assertion expecting shortened class name `TGameClient`. Repair commit `767d9f1bd38b7a35125105bc6ba86f0c486bfcbf` changed that exact identity assertion to `tibia::client::TGameClient`; it did not weaken SHA, method or dispatch gates.

A subsequent metadata checkpoint head `ea4f5b693644337ca9946dcf2972d19350cfd08b` started exact-head discriminator run `32103641442`. Two ordinary observations were consumed while that run was still in progress, so this invocation must not poll the same head a third time.

# Acceptance

The next session must persist only directly proven values for:

```text
COLD_AUTH_METHOD_META_INDEX
COLD_AUTH_ARGC
COLD_AUTH_ARG_TYPES or UNKNOWN with raw IDs
COLD_AUTH_METHOD_FLAGS
COLD_AUTH_DISPATCH_TARGET
COLD_AUTH_TARGET_INSTRUCTION_FENCE
```

Ambiguity remains `UNKNOWN`. No live-client success callback may be invoked or fabricated to manufacture progress.

# Checkpoint

```yaml
checkpoint_version: 3
status: waiting
last_completed_step: repaired exact namespaced TGameClient QMeta identity and started exact-head static validation with no runtime/client execution
blockers:
  - current invocation consumed the ordinary two-check budget for head ea4f5b693644337ca9946dcf2972d19350cfd08b while run 32103641442 remained in progress
next_action: resolve current PR #505 head and inspect its terminal cold-auth QMeta discriminator result; if it passed, persist the exact method/dispatch contract, otherwise inspect the failed job once and apply only a new evidence-based repair
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 2
  session_id: chatgpt-native-cold-auth-qmeta-20260818
  session_started_at: 2026-08-18T07:20:00+02:00
  checkpointed_at: 2026-08-18T07:42:00+02:00
  last_progress_at: 2026-08-18T07:39:00+02:00
  phase: validate_exact_qmeta_after_namespaced_class_repair
  exact_head: ea4f5b693644337ca9946dcf2972d19350cfd08b
  pull_request: 505
  active_operation: workflow_wait
  external_run_ids: [32103641442]
  operation_started_at: 2026-08-18T07:39:00+02:00
  wait_deadline_at: null
  check_generation: draft-repair-1
  checks_used: 2
  status: waiting
  safe_to_resume: true
  resume_condition: cold-auth QMeta discriminator reaches a terminal result
  next_action: inspect that terminal result and continue from its first material finding
```
