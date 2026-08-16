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
updated: 2026-08-16T23:13:30+02:00
producer_pr: 437
producer_head: d8d0ae7016636b2addb130b8a744584b83b5f7a2
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-worldmap-exact-static-evidence.md
  - docs/agents/evidence/OTC-20260816-track-a-worldmap-exact-static-evidence/**
  - .github/workflows/tibia-official-client-re-worldmap-exact-static-evidence.yml
  - .github/workflows/tibia-official-client-re-worldmap-exact-static-hosted-recovery.yml
  - .github/scripts/tibia-official-client-re-worldmap-exact-static-evidence.py
  - .github/scripts/tibia-official-client-re-worldmap-exact-static-evidence-v2.py
  - .github/scripts/tibia-official-client-re-worldmap-exact-static-evidence-v3.py
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
validation_state:
  prior_runtime_governance_run: 31972398445
  prior_runtime_governance_conclusion: success
  prior_ci_run: 31972398548
  prior_ci_conclusion: success
  source_v2_run: 31972743782
  source_v2_job: 95227595548
  source_v2_conclusion: success
  source_v2_artifact_id: 9270235755
  source_v2_artifact_name: track-a-worldmap-exact-static-source-31972743782
  source_v2_artifact_sha256: 039d22fe5f88a07784c4ddc32cf6b1d9c2d07a34e90ed5902ffd21d3acd5735b
  hosted_v2_job: 95227676658
  hosted_v2_conclusion: failure
recovery_checkpoint:
  status: HOSTED_REPORT_ORDERING_FAILURE_SOURCE_EVIDENCE_PRESERVED
  trusted_base: b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4
  first_source_run_id: 31972285354
  first_source_job_id: 95226438379
  first_source_failure: silent precondition exit before selector; analyzer not executed
  discriminator_run_id: 31972499618
  discriminator_job_id: 95226977563
  discriminator_result: candidate_1_exact_source_present_and_fenced_but_source_disassembler_missing
  exact_source_candidate_index: 1
  exact_source_regular: true
  exact_source_symlink: false
  exact_source_size: 51965216
  exact_source_sha_match: true
  objdump_available_on_source: false
  llvm_objdump_available_on_source: false
  source_v2_identity_windows_recovered: 3
  source_v2_direct_vptr_xrefs:
    0x02f683d0: 2
    0x030871d8: 4
    0x0308ce70: 3
  source_v2_bounded_code_windows: 49
  source_v2_bounded_raw_bytes: 52992
  hosted_failure: WORLD_MAP_STATIC_V2_REFUSED=SOURCE_REPORT_NONDETERMINISTIC
  hosted_failure_scope: derived Markdown ordering only; exact JSON fence/identity/code-window checks completed before this guard and the raw client was not present on the hosted runner
  canonical_runtime_touched: false
  client_process_started: false
  client_bytes_mutated: false
  prohibited_repeat: do not repeat the same source-disassembler failure or redo GUI/window v7; recover hosted validation from the already sanitized source artifact when possible
next_action: use a bounded hosted-only recovery job against source artifact 9270235755, relaxing only the derived Markdown ordering guard while preserving all preceding exact JSON/policy/window checks, then persist enriched evidence for PR #367
---

# Track A world-map exact static evidence producer

This task is a read-only exact-client evidence producer for consumer PR #367. It does not own or modify the consumer branch, does not acquire canonical runtime authority, and does not start the official client.

Post-v7 GUI evidence (#431/#432/#434) is deliberately not repeated. Run `31972499618`, job `95226977563`, proved candidate `1` is the exact regular non-symlink file and also proved no source-side objdump/llvm-objdump exists.

V2 source run `31972743782`, job `95227595548`, then succeeded without any source disassembler: exact fence passed, all three identity windows were recovered, nine direct vptr xrefs were decoded, 49 bounded code windows totaling 52,992 raw bytes were sanitized, and source artifact `9270235755` was uploaded. Hosted job `95227676658` downloaded that artifact with the raw client absent and failed only at the derived Markdown deterministic-order guard (`SOURCE_REPORT_NONDETERMINISTIC`) before bounded disassembly. The preserved source artifact is therefore the preferred recovery input; no identical physical failure is being retried.
