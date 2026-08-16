---
task_id: OTC-20260816-track-a-qlibrary-linux-resolution-hosted
status: validating
agent: ChatGPT
session_id: chatgpt-qlibrary-v2-20260816-1544
session_role: researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: discovery
phase: validate-source-correlation
branch: docs/OTC-20260816-track-a-qlibrary-linux-resolution-hosted-v2
base_branch: main
base_main: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
risk: low
updated: 2026-08-16T15:44:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-qlibrary-linux-resolution-hosted.md
  - docs/agents/reports/OTCLIENT-20260816-qlibrary-linux-resolution-source-correlated.md
  - .github/workflows/tibia-official-client-re-qlibrary-linux-resolution-hosted-v2.yml
modules_touched: []
reuses:
  - docs/agents/reports/OTCLIENT-20260816-filesystem-helper-resolver-static.md
  - historical exact-binary inventory from closed PR #354 only
  - official qt/qtbase v6.9.3 source
supersedes_pr: 356
depends_on: []
blocks: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
context_pressure: low
context_growth: stable
context_score: 5
estimate_confidence: high
decomposition_decision: single
decomposition_reason: bounded official-source correlation for one QLibrary absolute extensionless input
validation_level: focused
track_a_runtime_agent_admission_version: 1
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
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
historical_exact_qtcore_inventory:
  source_run: 31942882982
  source_job: 95154489699
  execution_class: historical_synology_inventory_only_no_repeat
  retained_path: bin/lib/libQt6Core.so.6
  size: 8789520
  sha256: 03ac3e4eb8730c2f6cbe6e3db9eb06c03477846eb3ac46ca2ebf19423270ffc5
  soname: libQt6Core.so.6
  static_version_string_set: [6.9.3]
source_pr_failure:
  pr: 356
  run: 31943243252
  job: 95155325324
  classification: VALIDATOR_DEFECT
  failed_expectation: searched for append-style .so construction not used by Qt 6.9.3
primary_source:
  qt_tag: v6.9.3
  qlibrary_unix_git_blob: afa96679a0db38f8f08ee9244175368e78c8d349
  qlibrary_unix_sha256: 9b9495f491b71e0fda0a9eff972298b118eb6f68488bb5da73f6e56c450f1a7e
  qlibrary_p_git_blob: ebc7c91d26e7af84262fe13900ffa2432335dc05
  qlibrary_p_sha256: 32d89e6dee9cbaab5777f98b0bc4dea8da45fffcb058604fdf35daa55efdc24e
result:
  classification: OFFICIAL_QT_6_9_3_SOURCE_CORRELATED
  haswell_false_potential_candidates:
    - <APPDIR>/BattlEye/BEClient
    - <APPDIR>/BattlEye/BEClient.so
    - <APPDIR>/BattlEye/libBEClient
    - <APPDIR>/BattlEye/libBEClient.so
  haswell_true_glibc_potential_candidates:
    - <APPDIR>/BattlEye/glibc-hwcaps/x86-64-v3/BEClient
    - <APPDIR>/BattlEye/glibc-hwcaps/x86-64-v3/BEClient.so
    - <APPDIR>/BattlEye/BEClient
    - <APPDIR>/BattlEye/BEClient.so
    - <APPDIR>/BattlEye/glibc-hwcaps/x86-64-v3/libBEClient
    - <APPDIR>/BattlEye/glibc-hwcaps/x86-64-v3/libBEClient.so
    - <APPDIR>/BattlEye/libBEClient
    - <APPDIR>/BattlEye/libBEClient.so
  actual_attempt_rule: runtime dlopen attempts are a prefix of the applicable potential list and stop at first success or, for absolute input, after a failed attempt whose path exists
  BEClient_so_generated: true
  BEClient_so_actually_attempted: UNKNOWN_RUNTIME_CONDITIONAL
  successful_mapping: UNKNOWN
acceptance:
  - use only official public qt/qtbase v6.9.3 for new semantic work
  - validate exact source file content hashes before parsing
  - validate .so suffix, lib prefix, absolute exact-first ordering, haswell/glibc prefix transform, loop order, dlopen construction and retry stop condition
  - distinguish potential generated candidates from actual conditional dlopen attempts
  - preserve actual successful mapping as UNKNOWN without runtime evidence
  - no Synology/proprietary semantic execution or BattlEye internal analysis
  - remove temporary hosted validator workflow before merge
validation:
  hosted_source_validator: PENDING
  track_a_governance: PENDING
  repository_ci: PENDING
  e2e: NOT_APPLICABLE_WITH_REASON
  e2e_reason: public-source static semantic correlation only
last_completed_step: corrected PR 356 validator defect against official Qt 6.9.3 source and persisted candidate-versus-attempt semantics
next_action: run hosted exact-source validator; if green, record evidence, remove temporary workflow, rerun final exact-head governance/CI and promote through coordinator
---

# Qt 6.9.3 QLibrary source-correlation task

The prior Draft #356 is replaced because its load-bearing validator encoded the wrong source spelling for the generic `.so` suffix. The replacement derives behavior from the exact official Qt 6.9.3 source and explicitly models the absolute-path retry stop condition, so generated candidate order is not confused with the runtime `dlopen` sequence.

No physical runtime, proprietary semantic probe, login/session state or anti-cheat internals are part of this task.
