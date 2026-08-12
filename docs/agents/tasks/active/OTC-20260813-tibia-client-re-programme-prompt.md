---
task_id: OTC-20260813-tibia-client-re-programme-prompt
status: validating
agent: ChatGPT
project_lane: otclient
lane: otclient
track: legacy-analysis
task_kind: documentation
phase: exact-head-validation
branch: docs/OTC-20260813-tibia-client-re-programme-prompt
base_branch: main
created: 2026-08-13T00:43:00+02:00
updated: 2026-08-13T00:52:00+02:00
risk: medium
related_pr: "282"
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

The resulting prompt preserves the repository rule that owner-funded Codex/API quota or user-owned credentials are not consumed unless the owner explicitly authorizes that specific use. Existing authorized GitHub Actions test-login secrets may only be consumed through their already-authorized workflow/runtime path and must never be exposed.

# Acceptance inventory

- [x] `docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md` exists and is self-contained enough for a fresh worker to start from live repository state.
- [x] Alias `OTCLIENT-TIBIA-RE` resolves to that prompt without relying on chat history once this PR is merged.
- [x] The prompt declares `blakinio/otclient` as the writable repository and treats external repositories as read-only evidence unless separately authorized.
- [x] Live PID, binary hash/version, branch/head, PR, runner, container, runtime ownership and ASLR-dependent addresses must be rediscovered rather than trusted from historical values.
- [x] The prompt retains the non-OCR session state machine, structured map/player/action objectives, protocol catalogue, OTBM feasibility work and stable API objective.
- [x] The prompt adds a bounded experiment contract and coordinator/worker execution model so one context is not expected to retain the whole programme.
- [x] Codex use is explicitly forbidden unless the owner authorizes that specific use.
- [x] No secret values, credentials, proprietary binaries/assets or private captures are embedded in the prompt.
- [x] Documentation/runtime E2E is `NOT_APPLICABLE`; this task changes only repository documentation/prompting and exposes no client runtime journey. Exact path/content/diff validation and repository CI remain required before merge.

# Manual prompt-eval matrix

| Case | Expected behavior | Status |
|---|---|---|
| Fresh agent, stale historical PID/PIE/container | Re-inspect live state before any experiment; never reuse old runtime addresses | PASS |
| Client logged out/disconnected | Recover through approved login workflow, reacquire PID/runtime objects, then revalidate structural `IN_GAME` | PASS |
| Movement signal/bytes observed but no state transition | Keep movement capability unproven | PASS |
| Client update changes binary SHA | Invalidate static runtime addresses and rerun discovery | PASS |
| Cross-repo report contains useful old offsets | Treat as read-only lead/evidence, not current authority | PASS |
| Owner-funded Codex is available but not specifically authorized | Do not invoke it; use permitted repository/runtime/local tooling or report the exact blocker | PASS |
| Secret value appears in runtime/workflow output | Do not persist, echo or add it to prompt/task evidence | PASS |
| One phase completes successfully | Checkpoint and continue/rotate according to programme state; do not claim whole programme complete | PASS |
| No safe READY experiment remains | Persist evidence and return the exact terminal blocker/next action | PASS |

# Proportionate documentation audit

```yaml
audit:
  phase: fresh-content-review
  result: PASS
  evidence:
    - PR #282 changed-file inventory contains exactly the two declared owned paths.
    - Full PR diff was reviewed against the owner-supplied programme objectives and current prompting/governance contracts.
    - The prompt contains no anti-tamper/anti-cheat stop rule requested for removal.
    - The prompt explicitly permits evidence-supported injected helper, ptrace/process-memory bridge and runtime hook designs within the controlled authorized environment.
    - Codex/API/owner-credential prohibition is explicit and consistent with current root AGENTS.md.
    - No secret value, credential, proprietary binary or private capture is embedded.
  material_findings_open: 0
```

# Validation

- Live-state preflight: PASS. `main` was `9e68388c5dff5d803f2a7025ba138e7cdfdf0d3f` at branch creation; PR #48 owns separate runtime/workflow paths.
- Prompt path/content review: PASS on commit `5d70675c99d63a142660ef4c7930e1d4b8639c2e`.
- Full changed-file inventory: PASS; only the prompt and this task record are changed.
- Full PR diff review: PASS; no unrelated runtime/workflow/asset/secret changes.
- Manual prompt-eval matrix: PASS, 9/9 scenarios.
- Runtime E2E: NOT_APPLICABLE because this is documentation/prompting only.
- Exact-final-head repository CI: pending after this checkpoint commit.

# Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-13T00:52:00+02:00
head: pending-this-checkpoint-commit
branch: docs/OTC-20260813-tibia-client-re-programme-prompt
pr: 282
status: validating
context_routes:
  - prompting
  - official-client-runtime-analysis
owned_paths:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
  - docs/agents/tasks/active/OTC-20260813-tibia-client-re-programme-prompt.md
proven:
  - The programme prompt exists on PR #282 and declares alias OTCLIENT-TIBIA-RE.
  - The prompt requires current live-state revalidation and forbids reuse of stale process/session addresses.
  - The prompt preserves the requested non-OCR structural programme, login recovery, evidence rules, phases, OTBM analysis and stable bridge goal.
  - The prompt explicitly forbids owner-funded Codex/API/credential use without specific owner authorization.
  - The full PR #282 diff contains only the two declared documentation paths.
  - Manual prompt evaluation passed all nine recorded scenarios.
  - The removed anti-tamper/anti-cheat blocker recommendation is not present in the prompt.
derived:
  - After merge to main, a fresh agent can resolve the short alias entirely from repository state without this chat.
unknown:
  - Exact-final-head CI conclusion until emitted checks complete.
conflicts:
  - none
first_failure:
  marker: none
  evidence: none
rejected_hypotheses:
  - Store the programme only in chat: rejected because durable repository state is required.
changed_paths:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
  - docs/agents/tasks/active/OTC-20260813-tibia-client-re-programme-prompt.md
validation:
  - command: manual prompt eval matrix
    result: PASS
    evidence: 9/9 cases above.
  - command: PR #282 changed-file and full-diff audit
    result: PASS
    evidence: exactly two declared documentation files; no unrelated changes.
  - command: runtime E2E
    result: NOT_APPLICABLE
    evidence: documentation/prompting task only; no client/runtime behavior changed.
  - command: exact-final-head repository CI
    result: NOT_RUN
    evidence: run/check graph must be observed after this checkpoint commit.
blockers:
  - none
next_action: Observe the exact-final-head required checks for PR #282, repair only a real task-related failure, then merge when all repository merge gates pass.
```
