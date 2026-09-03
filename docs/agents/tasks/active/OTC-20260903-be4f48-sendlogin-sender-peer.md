---
task_id: OTC-20260903-be4f48-sendlogin-sender-peer
status: blocked
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: terminal
branch: research/OTC-20260903-be4f48-sendlogin-sender-peer
base_branch: main
base_main: a35bbacd475a31ce52736ccbc3b5e837626def66
created: 2026-09-03T18:03:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
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
physical_e2e_required: false
implementation_authorized: true
worktree_state: UNAVAILABLE_CONNECTOR_ONLY_NO_REMOTE_DEVICE
owned_paths:
  - .github/workflows/tibia-official-client-re-be4f48-sendlogin-sender-peer.yml
  - tools/tibia_re_be4f48_sendlogin_sender_peer/**
  - docs/agents/tasks/active/OTC-20260903-be4f48-sendlogin-sender-peer.md
  - docs/agents/evidence/OTC-20260903-be4f48-sendlogin-sender-peer/**
  - docs/superpowers/plans/2026-09-03-be4f48-sendlogin-sender-peer.md
modules_touched: []
reuses:
  - promoted exact-current source evidence from PR #866 / merge 4bf27c0ffb376d789df78a6c78930b3d5f1dfb93
  - closed source PR #865 code/evidence only as discovery input, never as promotion authority
  - exact-current peer target 0xd052a0 and promoted helper target 0x4d8670 from promoted evidence
depends_on:
  - PR #866 merged promotion
  - PR #867 archived lifecycle
blocks:
  - clean coordinator promotion must correct the 0x4d8670 helper interpretation before any Track B decision
---

# Objective

Resolve only the first exact-current `15.32.be4f48` source boundary promoted by PR #866: identify the sender-side native peer/event and sender/receiver direction for the connection that causally binds `tibia::protocol::TProtocolMessageQueue::sendLogin`.

Do not reopen the completed #865 analyzer architecture, do not investigate the final queue/TCP writer lane, and do not modify Track B PR #284.

# Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

Trusted `main` remained `a35bbacd475a31ce52736ccbc3b5e837626def66` through terminal evidence persistence.

# Promoted starting anchors

```text
sendLogin_qmeta_target=0xde82a2
sendLogin_adapter_target=0xbd3050
sendLogin_adapter_fde=0xbd3050..0xbd34dd
adapter_reference_site=0x7c6b34
adapter_reference_owner_fde=0x7c6700..0x7cc933
connection_peer_target=0xd052a0
promoted_connection_helper_target=0x4d8670
peer_qmeta_candidates=[]
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
official_service_e2e=false
raw_client_upload=false
track_b_pr_284_modified=false
```

The official client was materialized only transiently inside bounded GitHub-hosted static workflow runs after repository-only RED contracts became GREEN. Raw/packed client bytes were deleted before artifact upload; only deterministic sanitized JSON was uploaded.

# Ownership / overlap

At claim time trusted `main` was `a35bbacd475a31ce52736ccbc3b5e837626def66`. PR #865 was closed unmerged as consumed. PR #284 remained a read-only cross-track hold. No live open PR search found another claim for this alias or these owned paths.

A local git worktree could not be created because the connected Remote Desktop endpoint reported no available device. A dedicated GitHub branch/PR was therefore the isolation boundary; no local filesystem state was shared or assumed.

# TDD evidence

Initial repository-only RED:

```text
run=33776945999
job=100720910769
head=6295381433c38949ae8af0ab51468243bf827274
repository-only contract=FAIL
exact-client prepare=SKIPPED
client materialization=SKIPPED
```

The one permitted PLT follow-up also had an independent repository-only RED:

```text
run=33777802812
job=100723755748
head=56d4684105118ff7e50a1503ffcc3e514754691e
repository-only contract=FAIL
exact-client prepare=SKIPPED
client materialization=SKIPPED
```

# Exact source runs

Stage 1:

```text
run=33777474194
job=100722673198
head=12af7ca291bc88ea4868a6abfcb32efb9b6a4248
conclusion=SUCCESS
artifact=9902213010
digest=sha256:6a0d3d3fdec009c009c8ed359a45bca85119d16fc1e2a2155e672ce698ac66b3
```

One bounded evidence-derived PLT discriminator:

```text
run=33778038445
job=100724556224
source_head=df9febe6f2817a606093898318595982222f056c
conclusion=SUCCESS
artifact=9902452300
digest=sha256:cbe454857fd778f0d989918553f8c999d80ab3dd0c866bcbcd638f3b78ffef89
```

# Accepted facts

The peer callable is exact and tiny:

```text
peer_target=0xd052a0
peer_fde=0xd052a0..0xd052c7
instruction_count=9
peer_direct_call_site=0xd052bd
peer_direct_callee=0x4d7dc0
peer_static_metaobject_argument=0x30b68a0
peer_signal_index_argument=0
```

The direct callee `0x4d7dc0` is a `.plt` stub whose relocation resolves to:

```text
mangled=_ZN11QMetaObject8activateEP7QObjectPKS_iPPv
demangled=QMetaObject::activate(QObject*, QMetaObject const*, int, void**)
peer_role=QT_SIGNAL_BODY_CALLING_QMETAOBJECT_ACTIVATE
```

This proves that `0xd052a0` is a Qt signal body. It does not prove the class owner or direction of the specific connection to the `sendLogin` adapter.

The promoted helper target `0x4d8670` is also a `.plt` stub, but it resolves exactly to:

```text
mangled=_Znwm
demangled=operator new(unsigned long)
role=ALLOCATOR_OPERATOR_NEW
```

Therefore `0x4d8670` is not a Qt connection primitive and cannot be used as sender/receiver direction authority.

# Withheld / fail-closed facts

```text
peer_owner_identity=UNKNOWN
sender_endpoint_identity=UNKNOWN
receiver_endpoint_identity=UNKNOWN
actual_qt_connection_primitive=UNKNOWN
sendlogin_causal_binding_proven=false
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
safe_track_b_delta=NOT_PROVEN
```

The one permitted follow-up was consumed by exact PLT symbol resolution. No third discriminator, broad call graph, runtime observation, final-writer analysis, OCR/Vision, credentials, official-service E2E, or Track B mutation was attempted.

# Evidence package

- `docs/agents/evidence/OTC-20260903-be4f48-sendlogin-sender-peer/result.json`
- `docs/agents/evidence/OTC-20260903-be4f48-sendlogin-sender-peer/20260903-source-result.md`

# Current state

```text
trusted_main=a35bbacd475a31ce52736ccbc3b5e837626def66
source_head=df9febe6f2817a606093898318595982222f056c
source_pr=#869
phase=TERMINAL_SOURCE_BLOCKER
peer_role=QT_SIGNAL_BODY_CALLING_QMETAOBJECT_ACTIVATE
peer_owner_identity=UNKNOWN
promoted_connection_helper_role=ALLOCATOR_OPERATOR_NEW
sender_endpoint_identity=UNKNOWN
receiver_endpoint_identity=UNKNOWN
sendlogin_causal_binding_proven=false
pre_login_sequence_advanced=false
runtime_access=none
official_service_e2e_count=0
track_b_pr_284_modified=false
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=PROMOTED_HELPER_TARGET_IS_ALLOCATOR_NOT_A_CONNECTION_PRIMITIVE
```

next_action: hand off to a clean coordinator promotion. The coordinator should preserve the newly proven signal role, correct the helper interpretation, and keep Track B PR #284 unchanged. Any later source task must start from a newly admitted bounded question such as the exact peer static-metaobject anchor `0x30b68a0` or the actual Qt connection primitive; it must not reuse `0x4d8670` as direction authority.
