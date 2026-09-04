---
task_id: OTC-20260904-be4f48-queue-signal-bf-exact-xref-connect-site
alias: OTC-BE4F48-QUEUE-SIGNAL-BF-EXACT-XREF-CONNECT-SITE
status: completed
agent: ChatGPT
session_id: chatgpt-20260904T1649+0200
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: closeout
branch: ai/OTC-20260904-be4f48-queue-signal-bf-exact-xref-connect-site
base_branch: main
base_main: 73bf55043e1a46732b30fd0be537742b0ac6fed9
created: 2026-09-04T16:57:00+02:00
updated_at: 2026-09-04T17:04:46+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
execution_reason: exact-current source-only signal-reference discriminator; GitHub-hosted static analysis is sufficient and no live runtime is authorized
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
policy_version: 2
context_pressure: medium
context_growth: stable
context_score: 9
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one bounded exact-signal discriminator followed by at most one causally linked connect site and one endpoint identity edge
feature_scope:
  type: contract_producer
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
invocation_started_at: 2026-09-04T16:49:00+02:00
last_progress_at: 2026-09-04T17:04:46+02:00
repair_cycles_for_current_gate: 0
unchanged_state_checks: 0
identical_failure_retries: 0
context_reconstruction_attempts: 0
stall_warnings: 0
validated_implementation_head: 1970ea47d785387c43c2ff02372d1c038ff17702
validated_workflow_run: 33887179571
validated_workflow_job: 101069725044
terminal_result: SOURCE_BLOCKER
first_missing_boundary: NO_DOWNSTREAM_CONNECTIMPL_CAUSALLY_TIED_TO_EXACT_SIGNAL_REFERENCES
owned_paths:
  - .github/workflows/tibia-official-client-re-be4f48-queue-signal-bf-exact-xref-connect-site.yml
  - tools/tibia_re_be4f48_queue_signal_bf_exact_xref_connect_site/**
  - docs/agents/tasks/active/OTC-20260904-be4f48-queue-signal-bf-exact-xref-connect-site.md
  - docs/agents/evidence/OTC-20260904-be4f48-queue-signal-bf-exact-xref-connect-site/**
reuses:
  - coordinator promotion PR #896 / merge 71e1af0db234a4011689e51bdbcc0ee7d9ee97c8
  - archive PR #897 / merge 5bedd83b38b276f5b7691f7efe2ef5f91611f42f
  - alias registration PR #898 / main 73bf55043e1a46732b30fd0be537742b0ac6fed9
  - source PR #880 only for exact signal-body/metaobject derivation patterns
  - source PR #895 only for promoted queue receiver/self-relay facts and hidden-sret connectImpl ABI
consumes_parallel_task: false
depends_on: []
blocks:
  - clean coordinator promotion before any Track B protocol decision
last_completed_step: exact-current exact-signal discriminator reached a precise SOURCE_BLOCKER; sanitized evidence persisted
next_action: clean coordinator promotion of the precise exact-signal source blocker before admitting one new bounded source step
---

# Objective

Resolve the exact-current downstream `clientMessageReadyToProcess(0xbf)` connect site, if and only if an exact-signal-only reference discriminator proves exactly one causal `QObject::connectImpl` setup and at most one endpoint identity edge.

This task started only from the promoted signal identity/body and the already-proven `tibia::protocol::TProtocolMessageQueue` self-relay. It did not repeat constructor-local enumeration and did not widen into a generic QObject/connect/socket/writer census.

# Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

# Terminal finding

The exact-current hosted discriminator derived the queue static metaobject from the exact signal body rather than assuming an analyzer constant: `QMetaObject::activate@0xbd22c2` carries signal index `0xbf` and a statically derived metaobject at `0x30b73e0`. Decoding that Qt6 metaobject proves owner `tibia::protocol::TProtocolMessageQueue`, signal method row `0x1ce47c0`, signal-name storage `0x1ceda8e`, and signal name `clientMessageReadyToProcess`.

The exact-signal-only reference discriminator found exactly one signal-specific reference: `lea` at `0xbe2e86` to body `0xbd2190`, inside the already-consumed queue-constructor FDE `0xbe2a50..0xbe3086`. That reference is the promoted self-relay QSlot callable, not a source-signal descriptor for a new connection. Exact derived signal method/name storage yielded no additional signal-specific reference, no exact data-wrapper reference was found, and zero downstream `QObject::connectImpl` sites survived the causal exact-signal discriminator.

Therefore no unique downstream connect site or endpoint identity is statically proven under the admitted exact-signal fence. The task stops at the first precise source boundary rather than broadening to a global connect/QObject/QSlot/socket/writer census.

```text
EXACT_CLIENT_FENCE_PROVEN=true
QUEUE_SIGNAL=clientMessageReadyToProcess
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_BODY=0xbd2190
QUEUE_SIGNAL_ARGV1_IDENTITY=exact GameclientMessage shared pair
EXACT_SIGNAL_REFERENCE_COUNT=1
EXACT_SIGNAL_CONNECT_CANDIDATE_COUNT=0
NEXT_UNIQUE_RELAY_EDGE=UNKNOWN
NEXT_ENDPOINT_IDENTITY=UNKNOWN
NEXT_RELAY_IDENTITY_PRESERVED=false
QUEUE_SIGNAL_WRITER_IDENTITY=UNKNOWN
FINAL_QUEUE_WRITER_IDENTIFIED=false
FINAL_TCP_WRITER_IDENTIFIED=false
FINAL_WRITER_CONTRACT=UNKNOWN
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=NO_DOWNSTREAM_CONNECTIMPL_CAUSALLY_TIED_TO_EXACT_SIGNAL_REFERENCES
NEXT_ACTION=clean coordinator promotion of this precise exact-signal source blocker before admitting one new bounded source step
```

# TDD and validation

- RED: head `e6b5dbf2c6bcaade6c43687975eb540974bb266a`, run `33886790195`, job `101068426723`; the repository-only contract failed with `AssertionError: exact_xref_connect_site.py is missing: expected RED before client materialization`, and all exact-client preparation/materialization steps were skipped.
- GREEN: implementation head `1970ea47d785387c43c2ff02372d1c038ff17702`, run `33887179571`, job `101069725044`; repository contract, exact fence, transient exact-client source analysis, sanitized-result validation and sanitized artifact upload all passed.
- The same implementation head passed CI run `33887180008`, Track A runtime governance run `33887179569`, and Track A self-hosted PR boundary run `33887179516`.
- Raw exact-client bytes were deleted before artifact upload (`RAW_CLIENT_RETAINED=false`).
- Sanitized artifact: ID `9942365211`, SHA-256 `c8ed008428f2f59c3ae8e168b4faeb7f30964707b7436df849e58eda964b0eb8`.
- Durable sanitized evidence: `docs/agents/evidence/OTC-20260904-be4f48-queue-signal-bf-exact-xref-connect-site/result.json`.

# Safety

```text
runtime_access=none
official_client_execution=false
login=false
credentials=false
process_memory=false
packet_capture=false
ocr_vision=false
official_service_e2e=false
track_b_pr_284_modified=false
```

# Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-04T17:04:46+02:00
head: 1970ea47d785387c43c2ff02372d1c038ff17702
branch: ai/OTC-20260904-be4f48-queue-signal-bf-exact-xref-connect-site
pr: 900
status: completed
context_routes:
  - docs/agents/evidence/OTC-20260904-be4f48-queue-signal-bf-exact-xref-connect-site/result.json
owned_paths:
  - .github/workflows/tibia-official-client-re-be4f48-queue-signal-bf-exact-xref-connect-site.yml
  - tools/tibia_re_be4f48_queue_signal_bf_exact_xref_connect_site/**
  - docs/agents/tasks/active/OTC-20260904-be4f48-queue-signal-bf-exact-xref-connect-site.md
  - docs/agents/evidence/OTC-20260904-be4f48-queue-signal-bf-exact-xref-connect-site/**
proven:
  - exact current fence 15.32.be4f48 / 52105824 / 552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
  - queue static metaobject is derived from QMetaObject::activate signal body flow as 0x30b73e0
  - derived metaobject owner is tibia::protocol::TProtocolMessageQueue and signal index 0xbf names clientMessageReadyToProcess
  - exactly one signal-specific reference exists, body LEA 0xbe2e86 in the consumed queue-constructor self-relay context
  - zero downstream QObject::connectImpl candidates are causally tied to the exact signal discriminator
  - runtime_access=none and Track B PR #284 was not modified
unknown:
  - next unique relay/connect edge outside the admitted exact-signal discriminator
  - next endpoint identity
  - final queue/TCP writer contract
  - FIELD6_VALUE
conflicts: []
first_failure:
  marker: NO_DOWNSTREAM_CONNECTIMPL_CAUSALLY_TIED_TO_EXACT_SIGNAL_REFERENCES
  evidence: docs/agents/evidence/OTC-20260904-be4f48-queue-signal-bf-exact-xref-connect-site/result.json
rejected_hypotheses:
  - exact signal method/name/body reference evidence exposes one downstream connectImpl source connection under the admitted discriminator
changed_paths:
  - .github/workflows/tibia-official-client-re-be4f48-queue-signal-bf-exact-xref-connect-site.yml
  - tools/tibia_re_be4f48_queue_signal_bf_exact_xref_connect_site/test_contract.py
  - tools/tibia_re_be4f48_queue_signal_bf_exact_xref_connect_site/exact_xref_connect_site.py
  - docs/agents/tasks/active/OTC-20260904-be4f48-queue-signal-bf-exact-xref-connect-site.md
  - docs/agents/evidence/OTC-20260904-be4f48-queue-signal-bf-exact-xref-connect-site/result.json
validation:
  - command: focused GitHub Actions exact-client source discriminator
    result: PASS
    evidence: run 33887179571 / job 101069725044 on implementation head 1970ea47d785387c43c2ff02372d1c038ff17702
  - command: official-service E2E
    result: NOT_APPLICABLE
    evidence: source-only static discriminator; official client execution/login/E2E explicitly prohibited by task fence
blockers:
  - no downstream connectImpl site is causally tied to the exact signal references under the admitted exact-signal-only discriminator
next_action: clean coordinator promotion of this precise exact-signal source blocker before admitting one new bounded source step
```
