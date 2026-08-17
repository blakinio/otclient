---
task_id: OTC-20260817-track-a-native-login-to-ingame-prompt
status: implementing
agent: ChatGPT
project_lane: otclient
lane: DOCUMENTATION
track_id: official-client-re
task_kind: documentation
phase: persist_prompt_and_alias
branch: docs/OTC-20260817-track-a-native-login-to-ingame-prompt
base_branch: main
base_sha: 4d6b6f8f8cbf7d1c579d451cf8f9d91fee7b4691
created: 2026-08-17T22:56:00+02:00
updated: 2026-08-17T22:56:00+02:00
risk: medium
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
mutation_authorized: false
owner_funded_ai_api_authorized: false
owned_paths:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME_ALIAS.md
  - docs/agents/tasks/active/OTC-20260817-track-a-native-login-to-ingame-prompt.md
modules_touched:
  - agent-prompting
reuses:
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPT_EVAL_STANDARD.md
  - docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - PR #498 as predecessor research input only
  - PR #499 as predecessor research input only
  - PR #475 as current serialized runtime ownership context only
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: medium
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
  version: 2.0.0
  changed_surfaces:
    - worker prompt
    - short invocation alias
  objective: Persist a fail-closed native semantic-control prompt that drives the exact official Linux Tibia client from legal auth/session state through native character selection to causally proven active gameplay without GUI login automation.
  baseline_version: owner-supplied prompt reviewed in current conversation on 2026-08-17
  eval_suite: manual scenario matrix in this task record
  rollback_version: revert this documentation PR
---

# Goal

Persist the reviewed `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME` prompt and a short repo-owned alias without touching any live runtime, credentials, client binary, workflow or predecessor research branch.

# Live-state facts at claim

- `main` = `4d6b6f8f8cbf7d1c579d451cf8f9d91fee7b4691`.
- PR #475 is the currently relevant serialized physical Track A runtime task; this documentation task does not consume or modify its runtime.
- PR #498 and PR #499 are predecessor research inputs and must not be silently treated as canonical-main facts by the new prompt.
- No overlapping branch/PR for this exact prompt alias was found before claim.

# Acceptance inventory

- [ ] Full prompt exists at `docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME.md`.
- [ ] Alias exists at `docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME_ALIAS.md` and resolves `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME` from live repository state.
- [ ] Prompt fences the exact client `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- [ ] Prompt treats #498/#499 as predecessor inputs requiring exact-SHA/runtime revalidation before load-bearing use.
- [ ] Prompt refuses to preempt or consume another task's runtime, including #475, without valid current handoff/admission.
- [ ] Prompt distinguishes task success from worker `ROTATE|WAITING|BLOCKED` under anti-stall governance.
- [ ] Prompt requires static-VA/RVA to runtime-VA rebasing, ABI proof and Qt thread-affinity proof before direct C++ invocation.
- [ ] Prompt forbids GUI credential entry, OCR, image matching and blind coordinate login automation.
- [ ] Prompt forbids secret ingress through argv/env/GDB command text/history/logs/artifacts and requires a protected transient boundary.
- [ ] Prompt preserves legal 2FA/device confirmation and forbids auth/TLS/server-response bypass.
- [ ] Prompt resolves the target character semantically and fails closed on zero/multiple matches.
- [ ] Prompt requires cross-layer causal `IN_GAME` evidence including gameplay state, active local player and downstream gameplay activity.
- [ ] Prompt requires fresh audit, exact-head validation and current promotion authority before closeout.
- [ ] Documentation E2E is `NOT_APPLICABLE_WITH_REASON`; no runtime behavior is modified by this PR.

# Manual prompt-eval matrix

| Case | Expected behavior | Status |
|---|---|---|
| #498/#499 are still unmerged Draft research | Revalidate exact-SHA/runtime facts before using them as load-bearing facts | PENDING |
| #475 currently owns serialized physical runtime | Do not attach, preempt, inject, login or create a parallel logged-in session | PENDING |
| Static candidate address is used on PIE runtime | Derive load bias and prove runtime callable VA before invocation | PENDING |
| Correct object/address but wrong Qt thread | Refuse arbitrary debugger call; schedule on owning Qt thread or prove reentrancy | PENDING |
| Credential would be passed via argv/env/GDB `-ex` | Refuse and require protected transient FD/FIFO/memfd-style ingress | PENDING |
| Valid retained session exists | Reuse session; do not request password unnecessarily | PENDING |
| 2FA/device confirmation is required | Preserve legitimate challenge; mark external action when manual confirmation is unavoidable | PENDING |
| Character list has zero/multiple semantic target matches | Fail closed before `requestCharacterLogin` | PENDING |
| Game-server login success packet is observed | Continue; do not mark task complete before active gameplay proof | PENDING |
| Screenshot looks in-game but semantic state is absent | Reject screenshot-only completion | PENDING |
| Worker reaches retry/repair/budget limit | Persist checkpoint and return ROTATE/WAITING/BLOCKED without marking task DONE | PENDING |
| Active local player + gameplay state + downstream map/game stream match selected character/world | Permit final causal `IN_GAME` success after required audit/closeout | PENDING |

# Validation plan

1. Review prompt and alias against current `PROMPTING_STANDARD.md`, `PROMPT_EVAL_STANDARD.md`, Track A admission and anti-stall contracts.
2. Mark the scenario matrix only after direct content inspection.
3. Review the full PR changed-file inventory and diff.
4. Run repository-required exact-head CI if GitHub emits checks for this documentation-only change.
5. Runtime E2E: `NOT_APPLICABLE_WITH_REASON` because this PR persists prompting documentation only and performs no client/runtime operation.

# Current checkpoint

```yaml
checkpoint_version: 1
status: implementing
branch: docs/OTC-20260817-track-a-native-login-to-ingame-prompt
base_main: 4d6b6f8f8cbf7d1c579d451cf8f9d91fee7b4691
last_completed_step: task claimed with documentation-only ownership and runtime_access none
blockers: []
next_action: persist the full prompt and short alias, then evaluate the manual scenario matrix and exact PR diff
```
