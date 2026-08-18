---
task_id: OTC-20260818-native-cold-auth-qmeta
status: ready
agent: ChatGPT
session_id: chatgpt-native-cold-auth-qmeta-20260818-r3
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
updated: 2026-08-18T07:50:00+02:00
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
  - PR #475 GameClient QMeta constants (DRAFT dependency)
depends_on:
  - blakinio/otclient#498
  - blakinio/otclient#475
blocks: []
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed_client_lzma_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
context_pressure: medium
context_growth: stable
context_score: 6
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one bounded exact-SHA QMeta discriminator with independent paths and no runtime ownership
validation_level: focused
invocation_started_at: 2026-08-18T07:20:00+02:00
last_progress_at: 2026-08-18T07:50:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft-final-evidence
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Objective

Recover the exact Qt/QMeta invocation contract for:

```text
TGameClient::onRequestLoginWithCredentials(QString, QString)
```

for `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME`, specifically to authenticate through original native client logic **without using the login form**.

Form automation is outside the solution: no OCR, image matching, coordinate clicks, blind Tab/Return or GUI-field operation.

# Final exact-SHA static result

Exact proving head before evidence-only closeout commit:

```text
d0c1360b649fd8c4a92587b7713644c49162694c
```

Workflow:

```text
run: 32104348691
job: 95610768376
conclusion: SUCCESS
```

Directly observed markers:

```text
COLD_AUTH_EXACT_PACKED_SHA=PASS
COLD_AUTH_EXACT_CLIENT_SHA=PASS
COLD_AUTH_CLIENT_EXECUTED=false
COLD_AUTH_RUNTIME_ACCESS=none
COLD_AUTH_QMETA_CLASS=tibia::client::TGameClient
COLD_AUTH_QMETA_METHOD_COUNT=44
COLD_AUTH_QMETA_SIGNAL_COUNT=6
COLD_AUTH_METHOD_NAME=onRequestLoginWithCredentials
COLD_AUTH_METHOD_META_INDEX=17
COLD_AUTH_ARGC=2
COLD_AUTH_METHOD_FLAGS=0x8
COLD_AUTH_RAW_PARAM_TYPE_IDS=0x2b,0xa,0xa
COLD_AUTH_ARG_TYPES=QString,QString
COLD_AUTH_RETURN_TYPE=void
COLD_AUTH_INVOKE_DISPATCH_ROLE=PROVEN_BY_CALL_AND_FULL_RANGE_GUARDS
COLD_AUTH_DISPATCH_LEA=0xd0626a
COLD_AUTH_DISPATCH_TABLE=0x1d6dea0
COLD_AUTH_DISPATCH_TARGET=0xd06850
COLD_AUTH_TARGET_EXECUTABLE=true
COLD_AUTH_TARGET_INSTRUCTION_FENCE=488b5110488b71084883c4485b5de92d389eff0f1f440000488bbfa009000048
COLD_AUTH_NEGATIVE_CONTROL_OTHER_EXECUTABLE_TABLES=1
COLD_AUTH_STATIC_DISCRIMINATOR=PASS
```

## FACT

For exact official native Linux client `15.32.df7b29` / SHA `e6c244bd...`, `tibia::client::TGameClient::onRequestLoginWithCredentials(QString,QString)` is QMeta `InvokeMetaMethod` id `17`. The full 44-method dispatcher is selected by `QMetaObject::Call == 0` plus method range `0..43`, and method 17 dispatches to static VA `0xd06850`.

The second executable table observed in the static-metacall region is rejected as a negative control because its own dispatcher range is only `0..4` (`cmp edx,4`), not the `TGameClient` 44-method range (`cmp edx,0x2b`).

## Runtime boundary still required

This task intentionally does not execute authentication. A later RUNTIME-authorized consumer must still prove current exact process identity, PIE/load-bias rebinding, runtime instruction bytes, unique live `tibia::client::TGameClient` object provenance, Qt thread affinity and protected transient construction/cleanup of the two `QString` credentials before invoking the original QMeta route. It must not invoke success callbacks or synthesize authentication/session state.

Durable evidence:

`docs/agents/evidence/OTC-20260818-native-cold-auth-qmeta/result.md`

# Validation / audit boundary

- focused exact-SHA discriminator: PASS on `d0c1360b...`;
- runtime E2E: `NOT_APPLICABLE_WITH_REASON` — this worker is `runtime_access:none` and only proves the static QMeta contract;
- independent promotion audit: still required by coordinator before canonical promotion;
- final evidence-only exact-head repository/governance CI: pending after this checkpoint commit.

# Checkpoint

```yaml
checkpoint_version: 4
status: ready
last_completed_step: exact-SHA static cold-auth QMeta contract passed, including method id 17, two QString arguments, unique full-range InvokeMetaMethod dispatch target 0xd06850 and instruction fence
blockers: []
next_action: observe the final evidence-only exact-head checks once; if green, hand PR #505 to the coordinator for independent review/promotion without merging it from this researcher session
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 3
  session_id: chatgpt-native-cold-auth-qmeta-20260818-r3
  session_started_at: 2026-08-18T07:45:00+02:00
  checkpointed_at: 2026-08-18T07:50:00+02:00
  last_progress_at: 2026-08-18T07:50:00+02:00
  phase: final_evidence_closeout
  exact_head: pending-evidence-commit
  pull_request: 505
  active_operation: none
  external_run_ids: [32104348691]
  operation_started_at: null
  wait_deadline_at: null
  check_generation: draft-final-evidence
  checks_used: 0
  status: ready
  safe_to_resume: true
  resume_condition: final evidence-only head exists
  next_action: inspect final exact-head checks once and hand the Draft PR to the coordinator if green
```
