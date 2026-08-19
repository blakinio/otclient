---
task_id: OTC-20260819-track-a-current-client-fence-advance
status: validating
agent: ChatGPT
session_id: chatgpt-track-a-fence-advance-20260819
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: governance_fence_advance
phase: final_exact_head_ci_and_independent_audit
branch: docs/OTC-20260819-track-a-current-client-fence-advance
base_branch: main
base_main: 82e5f435c3aa4172115bf7f6a0cd7a5cc6da3d50
risk: high
updated: 2026-08-19T09:22:11+02:00
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_class: github_hosted
runner: github
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
preliminary_independent_audit_head: 7c1c3658a9525761faba5a31c67e2e2f52e08957
preliminary_independent_audit_result: PASS
preliminary_independent_audit_material_findings_open: 0
preliminary_independent_audit_context: fresh_detached_worktree_deterministic_falsifier
preliminary_independent_audit_trust_worker_summary: false
preliminary_independent_audit_implementation_authorized: false
preliminary_independent_audit_public_package_refetch: PASS
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
owned_paths:
  - docs/agents/tasks/active/OTC-20260819-track-a-current-client-fence-advance.md
  - docs/agents/evidence/OTC-20260819-track-a-current-client-fence-advance/**
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_RESEARCH_COORDINATION.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_AGENT_PROMPTS.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_AGENT_PROMPT_EVAL.md
  - docs/agents/CHANGELOG.md
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/test_track_a_agent_runtime_governance.py
  - .github/workflows/track-a-canonical-live-governance.yml
reuses:
  - PR #550 current Kasm process identity evidence
  - PR #544 independently audited current-package static/runtime identity evidence
  - merged Track A runtime admission/bootstrap/canonical governance
read_only_overlap:
  - historical exact-build evidence and reports remain immutable historical provenance
  - tools/tibia_runtime_bridge/profiles/tibia-15.32.df7b29.json remains historical and is not promoted to the current build
  - PR #528 native-login current-build work remains separately owned
  - PR #550 remains blocked until this governance change is independently audited and merged
acceptance:
  - independently prove the public current Linux package unpacked size/SHA before changing the fence
  - advance only current-runtime identity governance/enforcement to the proven package; do not rewrite historical evidence
  - preserve fail-closed behavior for the old build, wrong-size/wrong-SHA/unknown builds and stale ABI/offset/helper reuse
  - do not grant login, credential, GUI input, gameplay, process-control, transaction or mutation authority
  - update deterministic governance checks and prompt-eval cases for the new current fence
  - run focused tests plus exact-head GitHub CI/governance
  - require fresh independent post-implementation audit before merge
  - after merge, do not use the new authority in this same invocation; PR #550 must re-admit from a later invocation on the updated trusted base
provenance_precheck:
  official_url_role: current Linux client package source
  packed_size: 10214529
  packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
  unpacked_size: 52109920
  unpacked_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
  elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
  embedded_version_token: '15.32'
  raw_client_retained: false
old_runtime_fence:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
new_runtime_fence:
  version: '15.32'
  size: 52109920
  sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
last_completed_step: exact-head 651944994... passed the fresh deterministic validator, and full diff review then found only closeout prose hygiene: stale adoption-time heading, changelog placement and missing EOF newline; these are corrected in the final candidate without changing fence semantics
local_validation: git diff --check PASS; Track A static governance PASS; Python py_compile PASS; normalized bash syntax PASS; YAML parse PASS
next_action: freeze this task-only checkpoint update as the final candidate head, require exact-head GitHub CI/Track A governance plus a repeat fresh-context validator on that exact SHA, then mark PR #555 Ready and squash-merge only if main freshness/review hygiene remain clean
---

# Track A current official-client fence advance

This task advances only the **current live-runtime identity fence** after direct public-package provenance proved the exact current Linux executable. It does not reinterpret old static evidence and does not make historical addresses, QMeta offsets, ABI assumptions or helper profiles valid for the new binary.

The governance change cannot expand this task's own authority. Even after merge, live consumers must re-read trusted `main` and re-admit in a later invocation before using the new fence.
