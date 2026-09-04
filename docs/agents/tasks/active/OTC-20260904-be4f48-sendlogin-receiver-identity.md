---
task_id: OTC-20260904-be4f48-sendlogin-receiver-identity
status: validating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: validate
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

Resolve only the exact class/ownership identity of the receiver object used by the proved `QObject::connectImpl` call at `0x7c6b9f` from receiver provenance `[entry-rdi-derived-rbx+0x88]`, then prove or reject the complete sender/receiver causal binding.

# Exact fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

# Terminal source result

```text
receiver_argument_stack_aware_proven=true
receiver_endpoint_provenance=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
receiver_field_read_count=165
receiver_field_write_count=0
receiver_endpoint_identity=UNKNOWN
complete_sender_receiver_pair_proven=false
sendlogin_causal_binding_proven=false
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=RECEIVER_FIELD_DEFINITION_OUTSIDE_SELECTED_CONNECTION_OWNER_FDE
```

The hidden-sret/stack-scratch ambiguity is resolved: the selected receiver argument reaches `connectImpl` from `[rbx+0x88]`. The selected owner FDE `0x7c6700..0x7cc933` contains no write that could define/type that field, so this lane stops here rather than broadening into global constructor/owner discovery.

# TDD / exact-head evidence

Initial repository-only RED run `33853813018` failed before package/client steps. A later stack-aware contract RED also failed before client materialization. Final exact-current run:

```text
SOURCE_HEAD=12070c649dd2e5e1f237fd524a3c48e7ca8375a0
SOURCE_RUN=33854810739 success
SOURCE_JOB=100965538997 success
ARTIFACT_ID=9929762469
ARTIFACT_DIGEST=sha256:eb9212da7acc41e0d67fc7c6a85740c846ac961faddf2ea0e79c49cdd684fd72
CI_RUN=33854811068 success
GOVERNANCE_RUN=33854810851 success
SELF_HOSTED_BOUNDARY_RUN=33854810677 success
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

# Anti-loop / next action

Do not extend #879 into a global field-owner/constructor sweep. Preserve the terminal blocker and wait for clean coordinator promotion together with the terminal queue-signal `0xbf` receiver result. Any later receiver-field owner discriminator must be newly admitted and bounded.

next_action: exact-head validate this terminal evidence; after #880 terminalizes, clean coordinator promotion should consume both source lanes and close #879 unmerged as consumed.
