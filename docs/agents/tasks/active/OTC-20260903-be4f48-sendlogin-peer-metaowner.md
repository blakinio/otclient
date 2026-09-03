---
task_id: OTC-20260903-be4f48-sendlogin-peer-metaowner
status: implementing
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: implementation
branch: ai/OTC-20260903-be4f48-sendlogin-peer-metaowner
base_branch: main
base_main: 446eb643d6ef24dc996a410df812393e19800973
created: 2026-09-03T19:11:13+02:00
updated_at: 2026-09-03T19:14:15+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
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
persistent_session_role: none
physical_e2e_required: false
implementation_authorized: true
worktree_state: UNAVAILABLE_CONNECTOR_ONLY_NO_REMOTE_DEVICE
policy_version: 2
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one bounded exact-current static-metaobject and local Qt connection discriminator with shared evidence
validation_level: focused
session_rotation_count: 0
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 0
invocation_started_at: 2026-09-03T19:11:13+02:00
last_progress_at: 2026-09-03T19:14:15+02:00
ci_checks_for_current_head: 0
ci_check_generation: green-implementation
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
owned_paths:
  - .github/workflows/tibia-official-client-re-be4f48-sendlogin-peer-metaowner.yml
  - tools/tibia_re_be4f48_sendlogin_peer_metaowner/**
  - docs/agents/tasks/active/OTC-20260903-be4f48-sendlogin-peer-metaowner.md
  - docs/agents/evidence/OTC-20260903-be4f48-sendlogin-peer-metaowner/**
  - docs/superpowers/plans/2026-09-03-be4f48-sendlogin-peer-metaowner.md
modules_touched: []
reuses:
  - merged coordinator promotion PR #871 and alias-registration PR #873
  - closed source PR #869 only as promoted discovery evidence
  - exact-current static metaobject anchor 0x30b68a0 and signal index 0
  - exact sendLogin adapter target 0xbd3050 and bounded owner FDE 0x7c6700..0x7cc933
depends_on:
  - PR #871 merged promotion
  - PR #873 merged alias registration
blocks: []
---

# Objective

Resolve only the exact-current `15.32.be4f48` source boundary registered as `OTC-BE4F48-SENDLOGIN-PEER-METAOWNER`:

```text
static QMetaObject anchor 0x30b68a0 + signal index 0
-> exact peer class/metaobject owner
-> actual bounded Qt connection primitive and sender/receiver direction
-> causal relation to TProtocolMessageQueue::sendLogin adapter, iff uniquely proven
```

The task is source-only. It must not reopen the completed #869 analyzer family, must not reuse `0x4d8670` as a connection primitive, and must not modify Track B PR #284.

# Delivery classification

```yaml
feature_scope:
  type: contract_producer
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
complete_user_facing_feature: false
```

E2E is `NOT_APPLICABLE` because this task is a static source discriminator and explicitly forbids official-client execution/login/runtime observation. The integration boundary is the deterministic analyzer plus exact-current hosted static evidence.

# Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

Fence source: `docs/agents/contracts/TRACK_A_CURRENT_CLIENT_FENCE_V1.json` at trusted main `446eb643d6ef24dc996a410df812393e19800973`.

# Promoted starting facts

```text
sendLogin_adapter_target=0xbd3050
adapter_reference_site=0x7c6b34
adapter_reference_owner_fde=0x7c6700..0x7cc933
peer_target=0xd052a0
peer_fde=0xd052a0..0xd052c7
peer_role=QT_SIGNAL_BODY_CALLING_QMETAOBJECT_ACTIVATE
qmetaobject_activate_plt=0x4d7dc0
peer_static_metaobject_argument=0x30b68a0
peer_signal_index_argument=0
0x4d8670=operator new(unsigned long)
peer_owner_identity=UNKNOWN
actual_qt_connection_primitive=UNKNOWN
sender_endpoint_identity=UNKNOWN
receiver_endpoint_identity=UNKNOWN
sendlogin_causal_binding_proven=false
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
```

# Admission / safety

```text
runtime_access=none
official_client_execution=false
login=false
credentials=false
process_memory=false
packet_capture=false
OCR/Vision=false
official_service_e2e=false
raw_client_upload=false
track_b_pr_284_modified=false
```

The exact official Linux client may be materialized only transiently inside a bounded GitHub-hosted static workflow after the repository-only RED contract has been observed failing and then made GREEN. Raw client bytes must be deleted before artifact upload; only deterministic sanitized JSON may be retained.

# Ownership / overlap preflight

Trusted `main` is `446eb643d6ef24dc996a410df812393e19800973`. Open PR search for `be4f48` found only independent queue-drain PR #874; no open PR claims this alias or the owned paths above. Local worktree state is unavailable because the connected Remote Desktop endpoint has no device; the dedicated GitHub branch is the isolation boundary and no local filesystem state is assumed.

# TDD RED evidence

The repository-only contract was executed before any production analyzer existed:

```text
pr=#875
head=df2d291073ab6c6b3a716d40639d94fad3550226
run=33783290711
job=100741903966
job_conclusion=failure
failed_step=Validate repository-only peer metaowner contract
failure=AssertionError: peer_metaowner.py must exist
exact-client prepare=SKIPPED
client materialization=SKIPPED
sanitized-result validation=SKIPPED
artifact upload=SKIPPED
```

This is the required observed RED. Production implementation may now begin.

# Acceptance

Positive terminal result is legal only if static evidence uniquely proves all of:

```text
peer_owner_identity=<exact owner>
peer_signal_index=0
actual_qt_connection_primitive=<exact Qt primitive/callsite>
sender_endpoint_identity=<exact sender>
receiver_endpoint_identity=<exact receiver>
sendlogin_causal_binding_proven=true
terminal_result=SENDLOGIN_PEER_METAOWNER_AND_DIRECTION_PROVEN
```

Otherwise stop at the first missing causal edge with `terminal_result=SOURCE_BLOCKER`. No semantic signal name may be invented if Qt metadata does not uniquely provide it.

# TDD / validation contract

1. Repository-only RED observed and persisted above.
2. Add the minimal bounded analyzer and make the repository contract GREEN.
3. Run the hosted exact-current static discriminator behind the exact version/size/SHA guard.
4. Inspect sanitized evidence; allow only evidence-derived, bounded repairs/follow-ups within the same static-metaobject/local-connection fence.
5. Persist deterministic evidence and independently falsify any positive owner/direction claim.
6. Run exact-head required CI/governance checks and inspect the complete diff before terminal classification.

# Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 2
  session_id: chatgpt-20260903T191113+0200
  session_started_at: 2026-09-03T19:11:13+02:00
  checkpointed_at: 2026-09-03T19:14:15+02:00
  last_progress_at: 2026-09-03T19:14:15+02:00
  phase: implementation
  exact_head: df2d291073ab6c6b3a716d40639d94fad3550226
  pull_request: 875
  active_operation: none
  external_run_ids: [33783290711]
  operation_started_at: 2026-09-03T19:13:35+02:00
  wait_deadline_at: null
  check_generation: red-contract
  checks_used: 1
  status: active
  safe_to_resume: true
  resume_condition: RED evidence remains preserved and PR #875 remains dedicated to this task
  next_action: add the minimal bounded peer_metaowner.py analyzer and observe the repository contract GREEN before interpreting exact-client evidence
```

next_action: add the minimal bounded `peer_metaowner.py` analyzer and observe the repository contract GREEN before interpreting exact-client evidence.
