---
task_id: OTC-20260903-be4f48-sendlogin-sender-peer
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: red
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
  - exact-current peer target 0xd052a0 and connection helper 0x4d8670 from promoted evidence
depends_on:
  - PR #866 merged promotion
  - PR #867 archived lifecycle
blocks:
  - clean coordinator promotion combining this lane with the independent final-writer lane before any Track B decision
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

Fail closed if the public package fence moves. Addresses below are valid only under that exact fence.

# Promoted starting anchors

```text
sendLogin_qmeta_target=0xde82a2
sendLogin_adapter_target=0xbd3050
sendLogin_adapter_fde=0xbd3050..0xbd34dd
adapter_reference_site=0x7c6b34
adapter_reference_owner_fde=0x7c6700..0x7cc933
connection_peer_target=0xd052a0
connection_helper_target=0x4d8670
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

The official client may be materialized only transiently inside the bounded GitHub-hosted static workflow after the RED contract becomes GREEN. It must be deleted before artifact upload; only deterministic sanitized structural JSON may be uploaded.

# Ownership / overlap check

At claim time trusted `main` is `a35bbacd475a31ce52736ccbc3b5e837626def66`. PR #865 is closed unmerged as consumed. PR #284 is open Draft and is a read-only cross-track hold for this task. No open PR returned by the live repository search claims the `OTC-BE4F48-SENDLOGIN-SENDER-PEER` alias or the unique paths owned above.

A local git worktree could not be created because the connected Remote Desktop endpoint reports no available device. This task therefore uses a dedicated GitHub branch as the isolation boundary; no local filesystem state is shared or assumed.

# TDD / bounded discriminator

1. RED: repository-only contract must fail before exact-client materialization because the focused peer-owner analyzer does not exist.
2. GREEN-1: add the smallest exact-fenced analyzer that reports peer FDE ownership, tail-transfer shape, RTTI/vtable memberships, constructor/vtable address-point xrefs, bounded direct callers, connection callsite argument provenance, and helper direct-call symbols.
3. Run once on the exact client and inspect sanitized output.
4. If the output gives one mechanically testable owner/direction hypothesis, add at most one narrow evidence-derived discriminator. Otherwise stop as `SOURCE_BLOCKER` at the first missing ownership/direction edge.
5. Never broaden into whole-binary BFS, a generic architecture crawler, runtime observation, OCR/Vision, final-writer analysis, or Track B mutation.

# Acceptance

Positive completion requires all of:

- exact current client fence proven;
- peer callable identity bound to a concrete current owner/class/function role;
- sender/receiver direction proven from callsite-local static dataflow or an equivalent exact-current source contract;
- causal relation to the proved `sendLogin` adapter established;
- independent static cross-check agrees;
- exact-head CI/governance and scoped static checks pass;
- `git diff --check` passes;
- PR #284 remains unchanged.

Scientific `UNKNOWN` is terminal when the bounded discriminator cannot prove one of those edges.

# Current state

```text
trusted_main=a35bbacd475a31ce52736ccbc3b5e837626def66
phase=RED_SETUP
runtime_access=none
official_service_e2e_count=0
track_b_pr_284_modified=false
terminal_result=PENDING
```

next_action: create the repository-only RED contract and early Draft PR; verify the RED failure occurs before any exact-client package download.