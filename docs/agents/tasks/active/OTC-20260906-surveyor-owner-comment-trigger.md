---
task_id: OTC-20260906-surveyor-owner-comment-trigger
status: implementing
agent: ChatGPT
session_id: surveyor-owner-comment-trigger-20260906
session_role: implementer
project_lane: otclient
lane: RUNTIME-P1-BRIDGE
track_id: official-client-re
task_kind: implementation
phase: implementation
branch: ci/OTC-20260906-surveyor-owner-comment-trigger
base_branch: main
created: 2026-09-06T13:53:00Z
updated_at: 2026-09-06T13:53:00Z
base_main: 71209b8e0433834c5c91ae92fbeb608f4ed830b3
policy_version: 2
prompting_standard_version: 2.1
execution_mode: chatgpt
execution_reason: add the smallest trusted-main owner-comment entrypoint to the existing dynamic-current-fence Surveyor read-only preflight
execution_class: github_hosted
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
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
physical_e2e_required: false
implementation_authorized: true
run_scope: bounded
continuation_policy: continue_until_real_stop
context_pressure: low
context_growth: stable
context_score: 4
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one existing workflow entrypoint plus one focused contract test
owned_paths:
  - .github/workflows/track-a-surveyor-v2-readonly.yml
  - tests/tools/tibia_re_surveyor/test_owner_comment_trigger_contract.py
  - docs/agents/tasks/active/OTC-20260906-surveyor-owner-comment-trigger.md
modules_touched:
  - Track A Surveyor v2 read-only workflow
reuses:
  - .github/workflows/track-a-surveyor-v2-readonly.yml
  - .github/scripts/test_track_a_qt_ingame_comment_trigger_contract.py owner-comment safety pattern
depends_on:
  - OTC-20260905-control-center-native-login-start
blocks:
  - OTC-20260905-control-center-native-login-start
cross_repository_task_ids: []
next_action: prove focused owner-comment contract test RED before changing the Surveyor workflow
---

# OTC-20260906 — Surveyor owner-comment trigger

## Objective

Add the smallest owner-only `issue_comment` entrypoint to the existing Track A Surveyor v2 read-only workflow so the current native-login task can invoke a fresh dynamic-current-fence Synology preflight through trusted `main` without creating a PR-controlled self-hosted workflow or using token-based Actions dispatch.

## Required behavior

- preserve existing `workflow_dispatch` support;
- accept owner comments only on pull requests;
- require the exact command prefix `/track-a-surveyor-v2-readonly ONE_SHOT_SURVEYOR_READ_ONLY ` followed by one safe runtime task ID;
- parse and validate the runtime task ID before any runtime observation;
- reuse the existing Surveyor read-only body unchanged after request resolution;
- keep `contents: read`, no `actions: write`, no `/dispatches`, no `GH_TOKEN`;
- do not add mutation, login, character-selection, gameplay, credential, process-control or canonical authority.

## Validation plan

1. focused contract test RED on the test-only head;
2. minimal workflow implementation;
3. focused Surveyor tests GREEN;
4. exact-head CI / Track A governance / self-hosted boundary checks;
5. full diff and review hygiene audit;
6. Ready + protected squash merge.
