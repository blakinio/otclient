---
task_id: OTC-20260816-track-a-p2-hosted-evidence-replay
status: validating
agent: ChatGPT
session_id: chatgpt-p2-replay-20260816-1424
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: validation
phase: validate
branch: research/OTC-20260816-track-a-p2-hosted-evidence-replay
base_branch: main
base_main: c932236af63069e36c71f43e47b2435532171180
risk: low
related_pr: null
updated: 2026-08-16T14:28:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-p2-hosted-evidence-replay.md
  - docs/agents/evidence/OTC-20260816-track-a-p2-hosted-evidence-replay/**
  - .github/workflows/tibia-official-client-re-p2-hosted-evidence-replay.yml
  - .github/scripts/tibia-official-client-re-p2-hosted-evidence-replay.py
modules_touched: []
reuses:
  - PR #310 historical P2 evidence only
  - run 31944051248 / job 95157306712 / artifact 9262800114
  - run 31904696996 / artifact 9252025461 for next-discriminator observation only
depends_on:
  - main@c932236af63069e36c71f43e47b2435532171180
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: deterministic replay of sanitized historical exact-build evidence requires no official-client binary, self-hosted runner or runtime state
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: milestone_and_terminal
validation_level: focused
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
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
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_research_only
provenance_boundary:
  source_run_31944051248: historical_exact_binary_evidence_quarantined_for_execution_routing
  source_artifact_zip_sha256: 30bd87d94088019b42fcf8504dfb6082af53b447547c544fec816e35b86407f3
  fixture_git_blob: eb856a17f01ab37fce94c09646918e7b01fbed6c
  current_hosted_replay_may_upgrade_exact_binary_provenance: false
  client_binary_in_fixture: false
acceptance:
  - hosted Ubuntu run proves fixture integrity/provenance and internal processor-chain consistency
  - preserve historical exact-binary result as historical, never relabel it current hosted exact-binary proof
  - preserve framing/sequence/compression/encryption/final_binary_egress UNKNOWN
  - identify next bounded discriminator as dual_precondition 0xb40370 / QIODevice::write 0xb4066b with direction UNKNOWN
  - no Synology, client execution, runtime/session/login/VNC or owner-funded AI/API use
historical_exact_chain:
  persistent_qbuffer_direct_readall: PROVEN
  first_downstream_consumer: PROVEN:TProtocolClientMessageProcessor+0x10@0xc2df80
  first_downstream_transform: PROVEN:TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
  same_message_handoff_to_dualconnection: PROVEN
  protocol_stage_order: PROVEN_PARTIAL
remaining_unknowns:
  framing: UNKNOWN
  sequence: UNKNOWN
  compression: UNKNOWN
  encryption: UNKNOWN
  final_binary_egress: UNKNOWN
active_operation: validate sanitized exact-build processor-chain evidence on GitHub-hosted execution, then use only the validated chain for the next static egress discriminator
next_action: run exact-head hosted replay; if green, inspect existing evidence around 0xb40370/0xb4066b and resolve direction/ownership before any egress classification
---

# P2 hosted evidence replay

This task removes the exact-client download blocker for **replay/correlation only**. It does not manufacture a new exact-binary execution claim.

The immutable fixture is a compact, non-proprietary transcription of the sanitized result emitted by historical exact-build run `31944051248`. That run verified the official Linux client size and SHA-256 and proved the processor chain, but its self-hosted execution is quarantined under current routing policy. The current hosted validator verifies only that the recorded evidence is internally coherent, pinned to the known source artifact, and still obeys all negative controls.

The next research discriminator is deliberately separate: historical artifact `9252025461` records a `QIODevice::write(QByteArray)` call at `0xb4066b` inside the `0xb40370` window. Its direction and owning device/socket are not yet proven, so it is not final egress evidence.
