---
task_id: OTC-20260816-track-a-worldmap-exact-static-evidence
status: implementing
agent: ChatGPT
session_id: chatgpt-runtime-worldmap-static-producer-20260816
session_role: researcher_producer_under_coordinator_dispatch
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: evidence_staging
phase: worldmap-exact-static-evidence
branch: research/OTC-20260816-track-a-worldmap-exact-static-evidence
base_branch: main
base_main: b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4
current_main: b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260816-track-a-worldmap-exact-static-evidence
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
updated: 2026-08-16T22:58:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-worldmap-exact-static-evidence.md
  - docs/agents/evidence/OTC-20260816-track-a-worldmap-exact-static-evidence/**
  - .github/workflows/tibia-official-client-re-worldmap-exact-static-evidence.yml
  - .github/scripts/tibia-official-client-re-worldmap-exact-static-evidence.py
modules_touched: []
reuses:
  - PR #367 / OTC-20260816-track-a-worldmap-extent-static-re as consumer only; its branch is not owned by this producer
  - PR #405 / runtime v7 as historical client_window_missing evidence only
  - PR #431/#432/#434 isolated DRI revalidation as fresh post-v7 discriminator and exact-source fence proof
  - immutable exact-source selector in commit cb557da12ebb41c597340909b2db717ee59cdfe1
  - PR #435 source-staging contract as current read-only sanitizer precedent; its failed retained-run SOURCE_CLIENT path is not reused
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
depends_on:
  - exact retained native-Linux client file matching 15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  - no live/canonical runtime dependency
blocks:
  - PR #367 static continuation until fresh exact identity-window and geometry xref evidence is produced or a genuine INPUT_BLOCKED condition is proven
policy_version: 2
prompting_standard_version: 2.1
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_mode: github-actions
execution_class: github_hosted
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
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
owner_funded_ai_api_authorized: false
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
source_staging_exception:
  coordinator_approved: true
  reason: user-directed RUNTIME continuation requires physical exact-file evidence for PR #367; retained corpus lacks the requested bytes/xrefs, repeated direct hosted client retrieval is already forbidden by the consumer task, and the accepted Track A routing permits bounded read-only evidence staging when host-local exact material is the only admissible source
  source_executor: synology-otclient-01
  source_access: read_only_file_only
  source_runtime_access: none
  source_candidates:
    - /home/runner/_work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client
    - /work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client
  canonical_state_access: forbidden
  client_process_access: forbidden
  process_memory_access: forbidden
  x11_vnc_access: forbidden
  login_session_access: forbidden
  network_access: forbidden
  gameplay_access: forbidden
  raw_client_upload: forbidden
  client_byte_mutation: forbidden
  allowed_output: bounded sanitized text/json evidence only
  hosted_validation_executor: ubuntu-latest
consumer_contract:
  pr: 367
  task: OTC-20260816-track-a-worldmap-extent-static-re
  consumer_branch: research/OTC-20260816-track-a-worldmap-extent-static-re
  requested_identity_windows:
    - 0x030871c8..0x030871d7 for vptr 0x030871d8
    - 0x0308ce60..0x0308ce6f for vptr 0x0308ce70
    - 0x02f683c0..0x02f683cf for vptr 0x02f683d0
  requested_geometry_offsets:
    - +0x18
    - +0x1c
    - +0x30
    - +0x34
    - +0x48
    - +0x4c
  priority_values:
    - +0x48 = 18
    - +0x4c = 14
  follow_on_types:
    - TWorldMapViewport
    - TWorldMapStorage
    - TWorldMapRenderProvider
    - TWorldMapCamera
    - TWorldMapPicker
  required_output:
    - exact client version/size/SHA fence proof
    - exact bytes and qwords for all recoverable identity windows
    - relocation-aware vtable/typeinfo relationship and RTTI name when directly recoverable
    - bounded direct writer/read/xref evidence for requested geometry fields when directly recoverable
    - explicit UNKNOWN for any semantic identity or xref not directly proven
    - no raw executable/package or unbounded proprietary disassembly
  physical_confirmation_owner: RUNTIME
researcher_delivery: draft_only
WORLD_MAP_STATIC_EVIDENCE_READY: false
programme_complete: false
recovery_checkpoint:
  status: PREPARED_BEFORE_FIRST_RUNNER_JOB
  trusted_base: b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4
  runner_job_started: false
  source_run_id: NOT_STARTED
  source_job_id: NOT_STARTED
  first_hypothesis: select only the two exact-source candidates proven by #431's successful immutable harness, then verify size and SHA before any bounded read
  prohibited_repeat: do not retry PR #435 retained-run SOURCE_CLIENT path without a new discriminator
next_action: open Draft producer PR, add bounded ELF/RTTI/xref sanitizer plus hosted validator, execute one source-staging attempt, then persist exact sanitized evidence and coordinates for PR #367
---

# Track A world-map exact static evidence producer

This task is a read-only exact-client evidence producer for consumer PR #367. It does not own or modify the consumer branch, does not acquire canonical runtime authority, and does not start the official client.

The post-v7 discriminator is already established: #431 restored GLX and exact-client startup but still observed zero visible windows. Because the requested product is static ELF evidence, the approved path is to avoid the GUI gate entirely and read only a size/SHA-fenced retained exact file.

The first source hypothesis deliberately differs from failed PR #435 run 31971704065: that run bound one stale retained-run path and failed before ELF access. This producer instead uses only the two install candidates already exercised successfully by the immutable #431 harness, then performs bounded relocation-aware extraction.
