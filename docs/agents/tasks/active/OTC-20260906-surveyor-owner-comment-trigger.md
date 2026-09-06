---
task_id: OTC-20260906-surveyor-owner-comment-trigger
status: validating
agent: ChatGPT
session_id: surveyor-owner-comment-trigger-20260906
session_role: validator
project_lane: otclient
lane: RUNTIME-P1-BRIDGE
track_id: official-client-re
task_kind: implementation
phase: validation
branch: ci/OTC-20260906-surveyor-owner-comment-trigger
base_branch: main
created: 2026-09-06T13:53:00Z
updated_at: 2026-09-06T13:59:00Z
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
next_action: verify final checkpoint exact-head CI and review hygiene, then Ready and protected squash merge
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

## Validation evidence

```yaml
tdd_red:
  head: 7d7934c719d8c01ddd5024148934e45ff69a6d59
  run: 34037643721
  job: 101498531845
  result: EXPECTED_FAILURE
  failing_test: test_owner_comment_trigger_is_actor_preserving_and_fail_closed
  cause: issue_comment trigger absent
implementation_head: 34aa3f345ffca2c5abfb29acf8c567de74d4879d
focused_surveyor:
  run: 34037902273
  result: PASS
  compile: PASS
  tests: PASS
  repository_only_collect_all: PASS
  whitespace: PASS
canonical_current_client_fence:
  run: 34037902202
  result: PASS
track_a_agent_runtime_governance:
  run: 34037902260
  result: PASS
self_hosted_pr_boundary:
  run: 34037902361
  result: PASS
full_diff_review:
  changed_paths: 3
  result: PASS
  unrelated_paths: 0
physical_runtime_touched: false
credentials_used: false
track_b_touched: false
```

## Final gate

This checkpoint-only commit changes the exact head. Required exact-head CI and all emitted affected checks must therefore pass again before Ready/merge. E2E is `NOT_APPLICABLE` for this repository-only trigger patch; the post-merge owner-comment invocation is a separate read-only physical preflight for the parent native-login task.
