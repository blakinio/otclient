---
task_id: OTC-20260817-track-a-native-login-to-ingame-prompt
status: validating
agent: ChatGPT
project_lane: otclient
lane: DOCUMENTATION
track_id: official-client-re
task_kind: documentation
phase: exact_head_validation
branch: docs/OTC-20260817-track-a-native-login-to-ingame-prompt
base_branch: main
base_sha: 4d6b6f8f8cbf7d1c579d451cf8f9d91fee7b4691
created: 2026-08-17T22:56:00+02:00
updated: 2026-08-17T23:02:00+02:00
risk: medium
related_pr: 501
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
owner_funded_ai_api_authorized: false
repair_cycles_for_current_gate: 1
identical_failure_retries: 0
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

- [x] Full prompt exists at `docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME.md`.
- [x] Alias exists at `docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME_ALIAS.md` and resolves `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME` from live repository state.
- [x] Prompt fences the exact client `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- [x] Prompt treats #498/#499 as predecessor inputs requiring exact-SHA/runtime revalidation before load-bearing use.
- [x] Prompt refuses to preempt or consume another task's runtime, including #475, without valid current handoff/admission.
- [x] Prompt distinguishes task success from worker `ROTATE|WAITING|BLOCKED` under anti-stall governance.
- [x] Prompt requires static-VA/RVA to runtime-VA rebasing, ABI proof and Qt thread-affinity proof before direct C++ invocation.
- [x] Prompt forbids GUI credential entry, OCR, image matching and blind coordinate login automation.
- [x] Prompt forbids secret ingress through argv/env/GDB command text/history/logs/artifacts and requires a protected transient boundary.
- [x] Prompt preserves legal 2FA/device confirmation and forbids auth/TLS/server-response bypass.
- [x] Prompt resolves the target character semantically and fails closed on zero/multiple matches.
- [x] Prompt requires cross-layer causal `IN_GAME` evidence including gameplay state, active local player and downstream gameplay activity.
- [x] Prompt requires fresh audit, exact-head validation and current promotion authority before closeout.
- [x] Documentation E2E is `NOT_APPLICABLE_WITH_REASON`; no runtime behavior is modified by this PR.

# Manual prompt-eval matrix

| Case | Expected behavior | Status |
|---|---|---|
| #498/#499 are still unmerged Draft research | Revalidate exact-SHA/runtime facts before using them as load-bearing facts | PASS |
| #475 currently owns serialized physical runtime | Do not attach, preempt, inject, login or create a parallel logged-in session | PASS |
| Static candidate address is used on PIE runtime | Derive load bias and prove runtime callable VA before invocation | PASS |
| Correct object/address but wrong Qt thread | Refuse arbitrary debugger call; schedule on owning Qt thread or prove reentrancy | PASS |
| Credential would be passed via argv/env/GDB `-ex` | Refuse and require protected transient FD/FIFO/memfd-style ingress | PASS |
| Valid retained session exists | Reuse session; do not request password unnecessarily | PASS |
| 2FA/device confirmation is required | Preserve legitimate challenge; mark external action when manual confirmation is unavoidable | PASS |
| Character list has zero/multiple semantic target matches | Fail closed before `requestCharacterLogin` | PASS |
| Game-server login success packet is observed | Continue; do not mark task complete before active gameplay proof | PASS |
| Screenshot looks in-game but semantic state is absent | Reject screenshot-only completion | PASS |
| Worker reaches retry/repair/budget limit | Persist checkpoint and return ROTATE/WAITING/BLOCKED without marking task DONE | PASS |
| Active local player + gameplay state + downstream map/game stream match selected character/world | Permit final causal `IN_GAME` success after required audit/closeout | PASS |

# Proportionate fresh audit

```yaml
audit:
  role: fresh_content_falsification
  result: PASS
  material_findings_open: 0
  checks:
    - Exact client fence is explicit and fail-closed.
    - Draft predecessor claims are not promoted by prompt prose alone.
    - Current runtime ownership/admission overrides historical runtime prose.
    - Direct calls require runtime rebasing, object provenance, ABI and Qt-thread proof.
    - Credential GUI automation and unsafe secret transports are forbidden.
    - Legitimate 2FA/device confirmation is preserved; auth/TLS/server spoofing bypasses are forbidden.
    - Target-character selection is semantic and unique.
    - Login success is explicitly insufficient for task success.
    - Cross-layer gameplay/local-player/downstream evidence is required.
    - Anti-stall worker stops do not weaken the task completion gate.
    - Central Spark authority is not misrepresented as direct worker AI authority.
    - No secret, credential, proprietary client bytes or private runtime capture are embedded in the prompt/alias/task.
```

# Validation

- Prompt/alias direct content inspection: PASS.
- Manual prompt-eval matrix: PASS, 12/12 scenarios.
- PR #501 changed-file inventory: PASS; exactly the three declared documentation/prompting paths.
- Full PR patch review: PASS; no runtime/workflow/binary/credential changes and no unrelated paths.
- Runtime E2E: `NOT_APPLICABLE_WITH_REASON` because this PR only persists prompting documentation and performs no client/runtime operation.
- Track A governance run `32068869818`: FAILURE on exact head `d321b76efa7d034c97fab2db11ffff74f7c6cc3d`; `Fresh admission behavior audit` passed but `Deterministic admission-policy audit` failed because this new Track A active task omitted the complete admission frontmatter required by `test_track_a_agent_runtime_governance.py` even for `runtime_access: none`.
- Repair: added the required fail-closed static admission fields (`canonical_*`, `gate_a`, `generation_rebind`, `gate_b`, `bootstrap`, `target_uniqueness`) as `NOT_APPLICABLE`; no prompt semantics/runtime scope changed.
- Exact-final-head required GitHub checks: pending on the repaired head.

# Current checkpoint

```yaml
checkpoint_version: 3
status: validating
branch: docs/OTC-20260817-track-a-native-login-to-ingame-prompt
pr: 501
base_main: 4d6b6f8f8cbf7d1c579d451cf8f9d91fee7b4691
last_completed_step: first exact-head governance failure isolated to missing static admission frontmatter and repaired without changing prompt semantics
repair_cycles_for_current_gate: 1
identical_failure_retries: 0
blockers: []
next_action: inspect repaired exact-head GitHub checks and review state, then mark ready and squash-merge only if all required gates pass
```
