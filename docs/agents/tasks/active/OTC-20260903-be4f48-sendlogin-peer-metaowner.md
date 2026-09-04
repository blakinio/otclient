---
task_id: OTC-20260903-be4f48-sendlogin-peer-metaowner
status: blocked
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: terminal
branch: ai/OTC-20260903-be4f48-sendlogin-peer-metaowner
base_branch: main
base_main: 446eb643d6ef24dc996a410df812393e19800973
created: 2026-09-03T19:11:13+02:00
updated_at: 2026-09-04T06:50:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
mutation_authorized: false
implementation_authorized: true
worktree_state: UNAVAILABLE_CONNECTOR_ONLY_NO_REMOTE_DEVICE
policy_version: 2
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
decomposition_decision: single
validation_level: exact-current-static
session_rotation_count: 0
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 1
invocation_started_at: 2026-09-04T06:34:00+02:00
last_progress_at: 2026-09-04T06:50:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: final-documentation-pending
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
owned_paths:
  - .github/workflows/tibia-official-client-re-be4f48-sendlogin-peer-metaowner.yml
  - tools/tibia_re_be4f48_sendlogin_peer_metaowner/**
  - docs/agents/tasks/active/OTC-20260903-be4f48-sendlogin-peer-metaowner.md
  - docs/agents/evidence/OTC-20260903-be4f48-sendlogin-peer-metaowner/**
  - docs/superpowers/plans/2026-09-03-be4f48-sendlogin-peer-metaowner.md
modules_touched: []
depends_on:
  - PR #871 merged promotion
  - PR #873 merged alias registration
blocks:
  - clean coordinator promotion must consume this source blocker before any new receiver-identity task is admitted
---

# Objective

Resolve only the exact-current `15.32.be4f48` source boundary registered as `OTC-BE4F48-SENDLOGIN-PEER-METAOWNER`:

```text
static QMetaObject anchor 0x30b68a0 + signal index 0
-> exact peer class/metaobject owner
-> actual bounded Qt connection primitive and sender/receiver direction
-> causal relation to TProtocolMessageQueue::sendLogin adapter, iff uniquely proven
```

This lane remained source-only and never modified Track B PR #284.

# Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

# Terminal decision

```text
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=SENDER_RECEIVER_ENDPOINT_IDENTITY_NOT_PROVEN
```

The task materially advanced beyond the promoted blocker, but the positive acceptance gate requires both endpoint identities and a complete causal binding. The receiver class identity remains `UNKNOWN`, so no positive completion or Track B delta is claimed.

# Exact-current accepted facts

```text
peer_target=0xd052a0
peer_static_metaobject=0x30b68a0
peer_owner_identity=tibia::authentication::TLoginProtocolMessageHandler
peer_signal_index=0
peer_signal_name=sendLoginMessage
actual_qt_connection_callsite=0x7c6b9f
actual_qt_connection_primitive=QObject::connectImpl(...)
sender_endpoint_identity=tibia::authentication::TLoginProtocolMessageHandler
receiver_endpoint_identity=UNKNOWN
sendlogin_adapter_target=0xbd3050
sendlogin_adapter_bound_to_connection=true
sendlogin_causal_binding_proven=false
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
```

Selected exact construction block:

```text
previous_connectImpl=0x7c6b07
adapter_reference=0x7c6b34 -> 0xbd3050
peer_reference=0x7c6b40 -> 0xd052a0
allocator=0x7c6b5e -> operator new(unsigned long)
selected_connectImpl=0x7c6b9f
```

Hidden-sret is proven from the exact ELF rather than assumed:

```text
0x7c6b69 mov rdi,rbp
0x7c6b9f call QObject::connectImpl
0x7c6ba8 mov rdi,rbp
0x7c6bab call QMetaObject::Connection::~Connection()
```

Formal argument mapping after the hidden return-storage pointer:

```text
rsi=sender
rdx=signal
rcx=receiver
r8=slotPtr
r9=slotObject
stack0=connectionType
stack8=types
stack16=senderMetaObject
```

Exact dataflow proves the peer signal, sender metaobject and adapter-bearing QSlotObject are all inputs to the selected `connectImpl`. The receiver is exactly sourced from an entry-object field `[rbx+0x88]`, but its class is not established by this bounded task.

# TDD and source evidence

Repository-only REDs before any client materialization:

```text
initial: run=33783290711 job=100741903966 head=df2d291073ab6c6b3a716d40639d94fad3550226
v3 ABI: run=33837464949 job=100912796002 head=c86500f8d110bac43c582738213e5ea1458c3d30
sret audit: run=33837902877 job=100914066665 head=64472af5ebca95c116198010dc343387a6f2cb15
```

Final exact-current source run:

```text
run=33838135600
job=100914746055
source_head=6174d44df2017bc5a435de0e843ee824520a12a5
conclusion=SUCCESS
artifact=9923975240
digest=sha256:e96c91c2b8bf408c06ff829ac25d48d39595f719a275e7361886cea93cb7d8ff
```

# Audit

Fresh validator role performed whole-diff falsification against the original acceptance and exact run evidence.

```text
finding=SRET-001
severity=material-medium
issue=hidden-sret shift was initially modeled but not independently proven from exact ELF
remediation=required exact same-rbp return-storage -> QMetaObject::Connection destructor proof
verification=run 33838135600 PASS
audit_result=PASS_AFTER_REMEDIATION
material_findings_open=0
```

The receiver identity is not an audit defect: it is the explicit terminal source boundary and is fail-closed as `UNKNOWN`.

# E2E / safety

```text
E2E=NOT_APPLICABLE
reason=static source discriminator; official-client execution/login/runtime observation explicitly forbidden
runtime_access=none
official_client_executed=false
login_performed=false
credentials_used=false
secret_access=false
process_memory_access=false
packet_capture=false
official_service_e2e_count=0
raw_client_uploaded=false
track_b_pr_284_modified=false
```

# Durable evidence

- `docs/agents/evidence/OTC-20260903-be4f48-sendlogin-peer-metaowner/result.json`
- `docs/agents/evidence/OTC-20260903-be4f48-sendlogin-peer-metaowner/20260904-source-result.md`
- source PR `#875`

# Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 2
  session_id: chatgpt-20260904T063400+0200
  session_started_at: 2026-09-04T06:34:00+02:00
  checkpointed_at: 2026-09-04T06:50:00+02:00
  last_progress_at: 2026-09-04T06:50:00+02:00
  phase: terminal-source-blocker
  source_analysis_head: 6174d44df2017bc5a435de0e843ee824520a12a5
  pull_request: 875
  active_operation: final exact-head documentation/governance qualification
  external_run_ids: [33838135600]
  check_generation: final-documentation-pending
  checks_used: 0
  status: blocked
  safe_to_resume: true
  resume_condition: source evidence remains unchanged and PR #875 remains dedicated to this task
  next_action: qualify the final documentation head, then hand off SOURCE_BLOCKER to a clean coordinator promotion
```

next_action: qualify the final documentation head, then hand off `SOURCE_BLOCKER` to a clean coordinator promotion that keeps Track B PR #284 unchanged and closes PR #875 unmerged as consumed.
