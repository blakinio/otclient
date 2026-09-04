---
task_id: OTC-20260904-be4f48-sendlogin-receiver-identity
status: implementing
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: red_pending
branch: research/OTC-20260904-be4f48-sendlogin-receiver-identity
base_branch: main
base_main: f7a471c2cc7ab7fd53afacc8a7458eeefb96ad97
created: 2026-09-04T10:28:00+02:00
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
owned_paths:
  - .github/workflows/tibia-official-client-re-be4f48-sendlogin-receiver-identity.yml
  - tools/tibia_re_be4f48_sendlogin_receiver_identity/**
  - docs/agents/tasks/active/OTC-20260904-be4f48-sendlogin-receiver-identity.md
  - docs/agents/evidence/OTC-20260904-be4f48-sendlogin-receiver-identity/**
  - docs/superpowers/plans/2026-09-04-be4f48-sendlogin-receiver-identity.md
modules_touched: []
reuses:
  - merged coordinator promotion #876 / merge 44a35365e38b9483b9c43aff4c36c2379fdbfb3e
  - closed source PR #875 only as discovery input, never as promotion authority
blocks:
  - clean coordinator promotion before any Track B decision
---

# Objective

Resolve only the exact class/ownership identity of the receiver object used by the proved `QObject::connectImpl` call at `0x7c6b9f`:

```text
receiver provenance = [entry-rdi-derived-rbx+0x88]
```

Then prove or reject the complete sender/receiver pair and causal binding from `TLoginProtocolMessageHandler::sendLoginMessage` to the QSlot carrying adapter `0xbd3050`.

# Exact fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

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

# Starting authority

Promoted facts from #876:

```text
sender=TLoginProtocolMessageHandler
signal=sendLoginMessage
connectImpl=0x7c6b9f
adapter=0xbd3050
receiver_provenance=[entry-rdi-derived-rbx+0x88]
receiver_identity=UNKNOWN
```

# TDD state

Initial head intentionally omits `receiver_identity.py`. The repository-only contract must fail before WARP metadata/client materialization. After RED is proven, add only the minimal exact-fenced bounded analyzer.

# Anti-loop

No global QObject/QMeta/connect sweep, no queue signal `0xbf` scope, no runtime, no Track B mutation. Stop at the first non-unique ownership/type edge.

next_action: open Draft PR and require the task-specific workflow to prove repository-only RED before exact-client materialization.
