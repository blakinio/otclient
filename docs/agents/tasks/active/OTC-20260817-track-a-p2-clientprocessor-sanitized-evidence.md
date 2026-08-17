---
task_id: OTC-20260817-track-a-p2-clientprocessor-sanitized-evidence
status: implementing
agent: ChatGPT
session_id: chatgpt-p2-clientprocessor-sanitized-evidence-20260817
session_role: researcher_producer_under_coordinator_dispatch
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: evidence_staging
phase: exact-client-object-identity-gap
branch: research/OTC-20260817-track-a-p2-clientprocessor-sanitized-evidence
base_branch: main
base_main: 8c9486e2c6109a7a39b564804c8acd707659b5e0
live_main_at_claim: 8c9486e2c6109a7a39b564804c8acd707659b5e0
risk: medium
created: 2026-08-17T09:10:00+02:00
updated: 2026-08-17T09:10:00+02:00
producer_pr: pending
consumer_pr: 310
consumer_task: OTC-20260815-track-a-p2-buffer-downstream-consumer
consumer_head_at_claim: 9b99b6b4bda2cf01e8fadcd8a00a6827de35d825
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-clientprocessor-sanitized-evidence.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-clientprocessor-sanitized-evidence/**
  - .github/scripts/tibia-official-client-re-p2-clientprocessor-sanitized-evidence.py
  - .github/workflows/tibia-official-client-re-p2-clientprocessor-sanitized-evidence.yml
modules_touched: []
reuses:
  - PR #310 / artifact 9252025461 as admitted prior targeted processor evidence, not as proof of the missing setup identity edge
  - PR #308 / artifact 9251725866 as coordinator-accepted retained persistent-QBuffer boundary
  - PR #446 source-sanitize -> hosted-decode method as a current bounded evidence-staging pattern only
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_RESEARCH_COORDINATION.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
depends_on:
  - exact official native-Linux client fence 15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  - PR #310 RETURN_FOR_EVIDENCE findings TACOORD-310-20260817-001 and TACOORD-310-20260817-002
blocks:
  - PR #310 coordinator promotion until this producer is independently reviewed
policy_version: 2
prompting_standard_version: 2.1
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: checkpoint_only
user_communication: low_noise
execution_mode: github-actions
execution_reason: bounded read-only exact-file source slicing only on the host-local source runner; all disassembly and semantic validation occur on GitHub-hosted runners
execution_class: github_hosted
runtime_access: none
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
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
owner_funded_ai_api_authorized: false
source_staging_exception:
  coordinator_approved: true
  owner_continuation_authorized: true
  reason: existing admitted bundles were independently checked and do not contain the load-bearing setup window; one narrow producer is therefore a real evidence need, not duplicate research. The owner's explicit prohibition on Synology static-analysis fallback is preserved because the source runner may only exact-fence and copy bounded file bytes; it performs no disassembly or semantic classification.
  source_executor: synology-otclient-01
  source_access: read_only_file_only
  source_runtime_access: none
  source_static_analysis: forbidden
  source_disassembly: forbidden
  source_semantic_classification: forbidden
  canonical_state_access: forbidden
  client_process_access: forbidden
  process_memory_access: forbidden
  x11_vnc_access: forbidden
  login_session_access: forbidden
  gameplay_access: forbidden
  raw_client_upload: forbidden
  client_byte_mutation: forbidden
  allowed_output: exact fence metadata plus bounded hex-encoded file windows only
  hosted_validation_executor: ubuntu-latest
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
feature_scope:
  type: contract_producer
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: partial_producer
requested_windows:
  setup_graph: 0x01970c80..0x019716c0
  required_setup_subset: 0x01970c80..0x019710b5
  invoker: 0x007dd630..0x007dd720
  client_processor: 0x00c2df80..0x00c2e080
  raw_processor: 0x00b47130..0x00b47320
  client_processor_vtable_address_point: 0x02f6a208
  raw_processor_vtable_address_point: 0x02f6a230
acceptance_inventory:
  - exact source size/SHA fence is re-proven before any byte read
  - source runner performs no disassembly, symbol resolution or semantic classification
  - bounded setup bytes include the persistent-QBuffer scratch reload and ClientMessageProcessor this+0x18 store
  - hosted decoding proves the same saved object pointer is stored into the actual ClientMessageProcessor member
  - hosted decoding binds ClientMessageProcessor vslot +0x10 to 0x00c2df80 and RawDataProcessor vslot +0x10 to 0x00b47130 using source-extracted vtable words
  - hosted decoding preserves same-stack-message ABI flow through ClientMessageProcessor then RawDataProcessor
  - hosted decoding verifies QIODevice::readAll target at 0x004ded50 and QByteArray mutation/assignment targets already present in admitted prior evidence
  - framing, sequence, compression, encryption and final binary egress remain UNKNOWN
  - no claim is promoted from generic Qt census, vtable adjacency, quarantined run 31944051248 or historical final-socket evidence
  - consumer-facing artifact contains no raw executable/package and no secret/private runtime data
researcher_delivery: draft_only
invocation_started_at: 2026-08-17T09:10:00+02:00
last_progress_at: 2026-08-17T09:10:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: producer-construction
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
e2e:
  result: NOT_APPLICABLE
  reason: static exact-client evidence producer only; no runtime behavior or client state is changed
next_action: create the narrow source-sanitize/hosted-decode workflow and run exactly one evidence generation; then independently review its consumer artifact before changing PR #310 disposition
---

# Track A P2 ClientMessageProcessor sanitized exact-client evidence

This producer exists only to close the exact object-identity gap recorded on consumer Draft PR #310. It must not broaden into framing, encryption, sequence or final socket research.
