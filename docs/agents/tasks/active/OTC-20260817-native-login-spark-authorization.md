---
task_id: OTC-20260817-native-login-spark-authorization
status: implementing
agent: ChatGPT
project_lane: otclient
lane: DOCUMENTATION
track_id: official-client-re
task_kind: documentation
phase: persist_bounded_spark_authorization
branch: docs/OTC-20260817-native-login-spark-authorization
base_branch: main
base_sha: 097aa12a992cd4a303656d50cbab9e593079642a
created: 2026-08-17T23:14:00+02:00
updated: 2026-08-17T23:14:00+02:00
risk: medium
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
owner_funded_ai_api_authorized: true
owned_paths:
  - AGENTS.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME_ALIAS.md
  - docs/agents/tasks/active/OTC-20260817-native-login-spark-authorization.md
modules_touched:
  - agent-prompting
reuses:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME_ALIAS.md
  - docs/agents/PROMPT_EVAL_STANDARD.md
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: low
decomposition_decision: single
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
prompt_contract:
  version: 1.1.0
  changed_surfaces:
    - root agent AI authorization
    - native login-to-ingame short alias
  objective: Persist a standing bounded owner authorization allowing direct use of exactly gpt-5.3-codex-spark for OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME without expanding to other models, APIs, credentials, runtime authority or completion evidence.
  baseline_version: alias 1.0.0 and root AGENTS.md at main 097aa12a992cd4a303656d50cbab9e593079642a
  eval_suite: manual scenario matrix in this task record
  rollback_version: revert this documentation PR
---

# Goal

Make the owner's current authorization durable and unambiguous: workers executing `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME` may directly use exactly `gpt-5.3-codex-spark`, while all other AI/provider/model/credential restrictions remain unchanged.

# Authorization boundary

Allowed only for invocations resolved through the exact alias/task family `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME`:

- model: `gpt-5.3-codex-spark` only;
- purpose: bounded repository/code analysis, reverse-engineering assistance, implementation assistance, falsification and review inside the declared task;
- authentication: ChatGPT-managed Codex authentication or another repository-approved non-exported managed path;
- secrets: no owner API key export/use, no game credentials, session secrets, auth tokens, secret-bearing memory/packet material, or raw proprietary client binary to the model;
- authority: Spark never grants runtime ownership, login budget, mutation authority, admission PASS, promotion authority or completion evidence;
- fallback: no other model/provider/OpenAI API/hosted Code Review fallback without separate owner authorization.

# Acceptance inventory

- [ ] Root `AGENTS.md` contains a bounded standing exception for this exact alias and exactly `gpt-5.3-codex-spark`.
- [ ] Alias contract is bumped and explicitly identifies direct Spark authorization and its boundaries.
- [ ] Root generic owner-funded-AI prohibition remains intact for every other task/use.
- [ ] Central Spark pre-review authorization remains unchanged and distinct from this worker exception.
- [ ] No `OPENAI_API_KEY`, owner-supplied AI credential, other model/provider or hosted Code Review is authorized by implication.
- [ ] Spark output remains advisory and cannot replace exact-SHA/runtime evidence, audit, E2E, CI or merge gates.
- [ ] No live runtime/client/credential operation occurs in this documentation task.

# Manual eval matrix

| Case | Expected behavior | Status |
|---|---|---|
| Native-login alias worker wants `gpt-5.3-codex-spark` | Direct use allowed within bounded task scope | PENDING |
| Same worker wants a different Codex/model/provider | Refuse unless separately authorized | PENDING |
| Same worker wants OpenAI API / `OPENAI_API_KEY` | Refuse; not covered | PENDING |
| Same worker wants to send Tibia password/session secret/raw proprietary binary to Spark | Refuse | PENDING |
| Unrelated repository task wants direct Spark | Existing generic prohibition applies | PENDING |
| Spark says login worked but runtime causal proof is missing | Do not promote success | PENDING |
| Central Spark controller runs PR pre-review | Existing separate standing authorization remains valid | PENDING |

# Validation plan

1. Apply only the bounded root exception and alias delta.
2. Review full diff and changed-file inventory.
3. Mark manual eval PASS only after direct content inspection.
4. Require exact-head repository CI/governance before merge.
5. Runtime E2E: `NOT_APPLICABLE_WITH_REASON` — documentation/authorization only.

# Checkpoint

```yaml
checkpoint_version: 1
status: implementing
branch: docs/OTC-20260817-native-login-spark-authorization
base_main: 097aa12a992cd4a303656d50cbab9e593079642a
last_completed_step: task claimed with runtime_access none and bounded owner authorization scope
blockers: []
next_action: update root AGENTS.md and the native-login alias, then run prompt-policy falsification and exact-head validation
```
