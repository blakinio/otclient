---
task_id: OTC-20260813-tibia-client-re-programme-prompt
status: implementing
agent: ChatGPT
project_lane: otclient
lane: otclient
track: legacy-analysis
task_kind: documentation
phase: prompt-authoring
branch: docs/OTC-20260813-tibia-client-re-programme-prompt
base_branch: main
created: 2026-08-13T00:43:00+02:00
updated: 2026-08-13T00:43:00+02:00
risk: medium
related_pr: none
owned_paths:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
  - docs/agents/tasks/active/OTC-20260813-tibia-client-re-programme-prompt.md
modules_touched:
  - agent-prompting
reuses:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
  - docs/agents/CONTEXT_HANDOFF.md
  - existing official-client runtime work in PR #48 as live-state evidence only
cross_repo_tasks:
  - OTERYN-20260811-tibia-client-analysis (historical/read-only lead; verify before use)
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: terminal_only
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
  version: 1.0.0
  changed_surfaces:
    - worker/coordinator prompt
    - autonomous continuation contract for the official-client RE programme
    - short invocation alias
  objective: Persist a repository-owned, restart-safe coordinator prompt for structural non-OCR official Linux Tibia client analysis and reusable read/control API research.
  baseline_version: owner-supplied unversioned draft from 2026-08-13
  eval_suite: manual scenario matrix in this task record
  rollback_version: revert this documentation PR
---

# Goal

Persist a reusable master/coordinator prompt in `blakinio/otclient` for the official Linux Tibia client reverse-engineering programme, with a short invocation alias that a fresh agent can resolve from repository state.

# Scope and authority

This is a documentation-only task. Repository writes are limited to the two owned paths above. Existing runtime branches, workflows, PR #48, runners and cross-repository analysis are read-only evidence for this task and are not mutated.

The resulting prompt must preserve the repository rule that owner-funded Codex/API quota or user-owned credentials are not consumed unless the owner explicitly authorizes that specific use. Existing authorized GitHub Actions test-login secrets may only be consumed through their already-authorized workflow/runtime path and must never be exposed.

# Acceptance inventory

- [ ] `docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md` exists and is self-contained enough for a fresh worker to start from live repository state.
- [ ] Alias `OTCLIENT-TIBIA-RE` resolves to that prompt without relying on chat history.
- [ ] The prompt declares `blakinio/otclient` as the writable repository and treats external repositories as read-only evidence unless separately authorized.
- [ ] Live PID, binary hash/version, branch/head, PR, runner, container, runtime ownership and ASLR-dependent addresses must be rediscovered rather than trusted from historical values.
- [ ] The prompt retains the non-OCR session state machine, structured map/player/action objectives, protocol catalogue, OTBM feasibility work and stable API objective.
- [ ] The prompt adds a bounded experiment contract and coordinator/worker execution model so one context is not expected to retain the whole programme.
- [ ] Codex use is explicitly forbidden unless the owner authorizes that specific use.
- [ ] No secret values, credentials, proprietary binaries/assets or private captures are embedded in the prompt.
- [ ] Documentation/runtime E2E is recorded as `NOT_APPLICABLE` with reason; exact path/content/diff validation and repository CI remain required.

# Manual prompt-eval matrix

| Case | Expected behavior | Status |
|---|---|---|
| Fresh agent, stale historical PID/PIE/container | Re-inspect live state before any experiment; never reuse old runtime addresses | pending |
| Client logged out/disconnected | Recover through approved login workflow, reacquire PID/runtime objects, then revalidate structural `IN_GAME` | pending |
| Movement signal/bytes observed but no state transition | Keep movement capability unproven | pending |
| Client update changes binary SHA | Invalidate static runtime addresses and rerun discovery | pending |
| Cross-repo report contains useful old offsets | Treat as read-only lead/evidence, not current authority | pending |
| Owner-funded Codex is available but not specifically authorized | Do not invoke it; use permitted repository/runtime/local tooling or report the exact blocker | pending |
| Secret value appears in runtime/workflow output | Do not persist, echo or add it to prompt/task evidence | pending |
| One phase completes successfully | Checkpoint and continue/rotate according to programme state; do not claim whole programme complete | pending |
| No safe READY experiment remains | Persist evidence and return the exact terminal blocker/next action | pending |

# Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-13T00:43:00+02:00
head: 9e68388c5dff5d803f2a7025ba138e7cdfdf0d3f
branch: docs/OTC-20260813-tibia-client-re-programme-prompt
pr: none
status: implementing
context_routes:
  - prompting
  - official-client-runtime-analysis
owned_paths:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
  - docs/agents/tasks/active/OTC-20260813-tibia-client-re-programme-prompt.md
proven:
  - Main was 9e68388c5dff5d803f2a7025ba138e7cdfdf0d3f immediately before branch creation.
  - Root governance forbids owner-funded Codex/API use without explicit authorization for the specific use.
  - Open PR #48 currently owns the official-client runtime/login workflow family and must be inspected rather than duplicated.
  - docs/agents/prompts currently contains OTCLIENT_NEW_AGENT_PROMPT.md and no existing Tibia RE programme prompt.
derived:
  - A new prompt path plus a unique documentation task does not overlap PR #48 runtime/workflow ownership.
unknown:
  - Final exact PR number and head until this task is published.
conflicts:
  - none
first_failure:
  marker: none
  evidence: none
rejected_hypotheses:
  - Store the programme only in chat: rejected because repository governance requires durable continuation state.
changed_paths:
  - docs/agents/tasks/active/OTC-20260813-tibia-client-re-programme-prompt.md
validation:
  - command: live main/open-PR/active-task/prompt-path preflight via GitHub connector
    result: PASS
    evidence: main 9e68388c5dff5d803f2a7025ba138e7cdfdf0d3f; PR #48 owns separate runtime/workflow paths; no existing prompt at target path.
blockers:
  - none
next_action: Create the programme prompt on this branch, open/update the draft PR, then perform manual prompt-eval and exact diff/path validation.
```
