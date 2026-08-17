---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: validating
agent: ChatGPT
session_id: chatgpt-raw-xres-helper-promotion-20260817
session_role: promotion_integration_coordinator
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: coordinator-promotion-raw-xres-wire
branch: feat/OTC-20260817-track-a-raw-xres-helper-promote
base_branch: main
base_main: 55803133a5abe8b1e75e4660da1d2b84b154ab9a
risk: high
updated: 2026-08-17T08:56:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
  - .github/scripts/tibia-official-client-re-xres-wire.py
  - .github/scripts/test_tibia_official_client_re_xres_wire.py
  - .github/workflows/tibia-official-client-re-xres-wire.yml
modules_touched:
  - track-a-xres-wire-helper
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-xres-window-identity.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-xres-support-inventory.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: coordinator independently reviewed source Draft #447, found and resolved one fail-closed ambiguity before terminal source closeout, and verified the final source head with dedicated hosted tests, Track A governance, repository CI and zero review threads. This branch is an exact conflict-free source tree replay on trusted main plus coordinator checkpoint metadata. No physical runtime access is authorized by this promotion.
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
validation_level: heavy
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
runner: github-hosted
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
physical_e2e_required: true
owner_funded_ai_api_authorized: false
source_review:
  source_pr: 447
  source_final_head: 32c61120b9086904b328e7b4aa50526d64bef807
  coordinator_decision: ACCEPT
  source_merge_tree: 56b1a50be3194b0c11bfda0ee1a502f33cef923e
  replay_seed_commit: 0a6709deec8082221323286a20b416ea8e9a606a
  material_findings_open: 0
  hardening_finding: one-spec QueryClientIds extraction originally ignored unrelated extra records
  hardening_resolution: nonempty one-spec result must contain exactly one record total
  hardening_fixture: test_rejects_extra_non_target_record_even_with_target
source_validation:
  semantic_helper_head: 06c6f18fc4a8920428ca353173b0596758a0190a
  semantic_dedicated_run: 32001448940
  semantic_dedicated_job: 95302425720
  semantic_dedicated_result: SUCCESS
  deterministic_tests: 33
  deterministic_tests_passed: 33
  purity_contract: XRES_WIRE_PURE_TRANSPORT_FREE_PASS
  source_final_dedicated_run: 32001585699
  source_final_dedicated_job: 95302804376
  source_final_dedicated_result: SUCCESS
  source_final_governance_run: 32001585708
  source_final_governance_result: SUCCESS
  source_final_repository_ci_run: 32001585992
  source_final_required_ci_job: 95303113378
  source_final_required_ci_result: SUCCESS
  source_review_threads_open: 0
implementation:
  helper_path: .github/scripts/tibia-official-client-re-xres-wire.py
  helper_blob: ce5992bc1171eef9f24a71dfc97da728f18627a9
  test_path: .github/scripts/test_tibia_official_client_re_xres_wire.py
  dedicated_workflow: .github/workflows/tibia-official-client-re-xres-wire.yml
  query_version_encoder: PASS
  query_version_reply_parser: PASS
  query_client_ids_encoder: PASS
  query_client_ids_reply_parser: PASS
  local_client_pid_extractor: PASS
  transport_free: true
  exactly_one_record_for_one_spec_required: true
classification:
  primary: PROVEN_HOSTED_RAW_XRES_WIRE_CODEC_FAIL_CLOSED_AND_TRANSPORT_FREE_WITH_33_DETERMINISTIC_FIXTURES
evidence:
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/20260817-raw-xres-wire-hosted.md
safety:
  canonical_bootstrap_retry_authorized: false
  canonical_window_identity_relaxation_authorized: false
  physical_identity_retry_authorized_before_promotion_merge: false
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  track_b_access: false
forbidden:
  - Synology/Xvfb/official-client execution from this promotion branch
  - network/socket/X11 connection in helper tests
  - canonical lease/registration/session observation or mutation
  - credentials, login or gameplay
  - canonical bootstrap retry
  - canonical window identity relaxation before direct physical XID-to-PID proof
  - Track B and historical PR #303 runtime surfaces
acceptance:
  - exact source tree replayed without manual code rewrite
  - source dedicated validation and purity PASS
  - source Track A governance PASS
  - source CI Required PASS
  - source review threads zero
  - coordinator material findings zero
  - promotion exact-head dedicated workflow PASS
  - promotion Track A governance PASS
  - promotion repository CI Required PASS pre-ready and ready-state
  - no physical runtime access occurs
last_completed_step: source #447 final head passed dedicated raw-XRes validation, Track A governance and repository CI; coordinator decision is ACCEPT and the exact source merge tree is replayed linearly on trusted main for promotion
next_action: validate promotion exact head, mark ready, protected auto-merge, close #447 superseded, then freshly admit a separate task-owned isolated physical XRes PID-identity discriminator using the promoted helper; canonical bootstrap and window-identity relaxation remain forbidden until that physical proof succeeds.
---

# Track A canonical runtime E2E — raw-XRes helper promotion

This promotion makes the pure wire codec durable on trusted main. It does not itself prove physical resource ownership or authorize canonical startup.
