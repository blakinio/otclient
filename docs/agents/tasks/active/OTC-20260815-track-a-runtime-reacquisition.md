---
task_id: OTC-20260815-track-a-runtime-reacquisition
status: ready
agent: unassigned_draft_only_researcher
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime-research
phase: restart-relogin-reacquisition
branch: research/OTC-20260815-track-a-runtime-reacquisition
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-runtime-reacquisition
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-runtime-reacquisition.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/**
  - .github/workflows/tibia-official-client-re-runtime-reacquisition.yml
  - .github/scripts/tibia-official-client-re-runtime-reacquisition.sh
depends_on:
  - coordinator-retained exact-build structural world evidence
  - historical login procedure in PR #290 as untrusted/revalidation-required input only
  - PR #283 bridge evidence as reference only; no ownership of its paths
blocks: []
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
---

# Objective

Prove or disprove restart/relogin/reacquisition stability for the already-established Track A exact-build structural world read path, without repeating basic world-entry or one-off movement proof as the hypothesis.

# Dispatch contract

```yaml
TASK_ID: OTC-20260815-track-a-runtime-reacquisition
TASK_RECORD: docs/agents/tasks/active/OTC-20260815-track-a-runtime-reacquisition.md
PROJECT_LANE: otclient
LANE: RUNTIME
BASE_MAIN: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
BRANCH: research/OTC-20260815-track-a-runtime-reacquisition
WORKTREE: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-runtime-reacquisition
OWNED_PATHS:
  - docs/agents/tasks/active/OTC-20260815-track-a-runtime-reacquisition.md
  - docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/**
  - .github/workflows/tibia-official-client-re-runtime-reacquisition.yml
  - .github/scripts/tibia-official-client-re-runtime-reacquisition.sh
DEPENDENCIES:
  - exact-build structural world evidence retained by coordinator PR #300
  - PR #290 procedure is evidence input only, not authority
  - PR #283 bridge/profile evidence is reference-only
```

Research output is DRAFT-ONLY. Promotion belongs to coordinator PR #300.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
runner: synology-otclient-01
```

# Starting facts and safety corrections

- later exact-build evidence proves `synology-otclient-01` has executed Track A jobs; old #280/#281 'no self-hosted runner available' checkpoints are not current facts;
- a single live structural world observer + reversible transition was previously proven for this exact build;
- historical login/session procedure in #290 is `REVALIDATION_REQUIRED`, not current runtime proof;
- rejected #289 contains a material safety finding: credentials must **not** be job-scoped into persistent child process environments;
- rejected #289 also demonstrates that shared X display sockets/locks must never be deleted without task ownership proof.

# Hypothesis

A task-owned Track A runtime can be restarted and, when protected credentials are available through repository secrets, relogged into the world such that the structural world observer/read path is deterministically reacquired without reusing stale PID/PIE/object state.

# Required discrimination

Test at least two generations of runtime identity when authorized state exists:

```text
generation N structural IN_GAME/read proof
-> clean task-owned client/observer teardown
-> fresh client start/login under the same isolated task namespace
-> fresh PID/PIE/profile/observer acquisition
-> generation N+1 structural IN_GAME/read proof
```

If credentials or safe login prerequisites are unavailable, stop with an exact evidence-backed WAITING/BLOCKED classification; do not fabricate restart stability from process-only checks.

# Credential and namespace rules

- credentials may exist only as protected secret inputs to the minimal login helper invocation;
- do not define credentials at job scope;
- explicitly ensure persistent X/DBus/client/observer processes are launched without credential values in their environments;
- never print, persist, OCR, artifact, or inspect credential values;
- task must use only its own display/socket/state/PID files and verify ownership before cleanup;
- do not touch Track B runtime/state/display/ports/processes.

# Acceptance gate

- [ ] exact client SHA/size rechecked on every generation;
- [ ] fresh PID and PIE base proven after restart; no stale address reuse;
- [ ] WARP/SOCKS confinement verified, with no direct client TCP and no client UDP where the canonical login model requires it;
- [ ] structural `IN_GAME`/world state proved independently of keypress/socket existence;
- [ ] structural observer/read path reacquired after at least one clean restart/relogin cycle, or an exact prerequisite blocker recorded;
- [ ] persistent child environments verified free of credential variables;
- [ ] task-owned namespace cleanup cannot delete another task's display/socket/state;
- [ ] no gameplay action beyond what is strictly required for safe read discrimination;
- [ ] exact-head CI terminal before Draft handoff.

# Side-effect budget

Login/session recovery and clean process restart only. No market/trade/forge/currency effects. Movement is not part of the hypothesis and should not be repeated unless a single reversible step is necessary solely to distinguish live structural world state; if used, verify inverse restoration.

# Deliverable

Draft PR only with the task-scoped workflow/helper and sanitized evidence. Preserve failures and unavailable credentials/prerequisites as explicit WAITING/BLOCKED results rather than weakening the gate.
