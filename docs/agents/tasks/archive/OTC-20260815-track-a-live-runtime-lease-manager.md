---
task_id: OTC-20260815-track-a-live-runtime-lease-manager
status: completed
agent: ChatGPT
session_id: null
session_role: terminal-closeout
session_rotation_count: 8
project_lane: otclient
lane: track-a-runtime-governance
track_id: official-client-re
task_kind: implementation
phase: completed
branch: docs/OTC-20260815-track-a-live-runtime-lease-manager-cancellation-closeout
base_branch: main
base_main: 8828150617d68247be2074b330f4d954e508307b
risk: high
related_pr: 321
created: 2026-08-15T22:04:00+02:00
updated: 2026-08-16T07:27:00+02:00
lease_expires_at: null
lease_released_at: 2026-08-16T07:27:00+02:00
stale_takeover_count: 2
owned_paths: []
modules_touched:
  - track-a-runtime-governance
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: completed
task_completion_policy: completed
user_communication: terminal_only
implementation_authorized: false
last_progress_at: 2026-08-16T07:27:00+02:00
final_implementation_head: d5bff95997e82d4ac5180d0e9c1b85dae8a3c7dd
final_main_merge: 8828150617d68247be2074b330f4d954e508307b
semantic_run: 31928876589
semantic_unit_job: 95120629666
semantic_selfhosted_job: 95120629639
semantic_state: success
audit_run: 31928876589
audit_job: 95120629610
audit_state: pass
repository_ci_run: 31928918002
repository_ci_required_job: 95120881462
repository_ci_state: success
review_threads: 0
e2e_result: NOT_APPLICABLE
stop_reason: completed
next_action: reconcile final bootstrap/governance documentation to manager main 8828150617d68247be2074b330f4d954e508307b, repair PR #311 generation-rebinding P1, then exact-head validate and protected-merge PR #311
---

# Objective

Provide the final fail-closed canonical-live controller manager/supervisor whose production `guard-run` serializes the complete lifetime of a guarded mutation tree even when the foreground process group is cancelled.

# Terminal implementation — FACT

PR #321 repaired the post-closeout P1 discovered by fresh PR #311 review after PR #319. The caller now blocks `SIGHUP`, `SIGINT`, `SIGQUIT` and `SIGTERM` across supervisor fork setup; the lock-owning Linux child-subreaper installs non-terminating handlers before restoring the inherited mask; cancellation pending before the supervisor existed is relayed fail-closed. The guarded command still receives no flock descriptor because it is launched with `close_fds=True`.

If foreground process-group cancellation kills the caller while a guarded descendant deliberately ignores `SIGTERM`, the supervisor survives, continues owning `coordination.lock`, and releases serialization only after the primary command and all adopted/orphaned descendants have exited. The deterministic regression proves this behavior by failing nonblocking flock acquisition while the signal-ignoring child remains alive and succeeding only after guarded lifetime ends.

PR #321 exact implementation head `d5bff95997e82d4ac5180d0e9c1b85dae8a3c7dd` protected-merged as main `8828150617d68247be2074b330f4d954e508307b`.

# Final validation — FACT

Exact head `d5bff95997e82d4ac5180d0e9c1b85dae8a3c7dd`:

```text
semantic run 31928876589
unit 95120629666 SUCCESS
isolated Synology 95120629639 SUCCESS
fresh independent acceptance audit 95120629610 SUCCESS
repository CI run 31928918002 SUCCESS
CI / Required 95120881462 SUCCESS
```

PR #321 had zero unresolved review threads at merge. Runtime E2E is `NOT_APPLICABLE`: this manager repair is exercised through OS process/flock semantics and isolated state; launching or logging into Tibia is outside authorization and unnecessary for the acceptance boundary.

# Closeout history — FACT

- PR #312 merged the initial manager.
- PR #313 merged concurrency hardening.
- PR #317 merged normal-launcher descriptor-last-close hardening.
- PR #316 merged the first out-of-band child-subreaper supervisor.
- PR #319 was a valid fresh closeout for the then-known PR #316 implementation, but a later PR #311 review exposed an additional process-group cancellation P1; therefore #319 is superseded as the final Track A manager closeout.
- PR #321 repaired that P1 and is the final manager implementation represented by this archive.
- Stale/superseded PR #314 closeout evidence was not reused.

# Ownership / takeover — FACT

Before PR #321 work, the prior manager task on `main` was archived with `session_id: null`, `lease_expires_at: null` and an explicit released lease. There was no genuinely active manager owner to race. The task was reopened on a dedicated branch for the post-closeout regression; `stale_takeover_count` was not incremented because this was a new finding after a released terminal session, not a stale concurrent lease takeover. This closeout releases ownership again.

# Safety / non-claims

- No Tibia client launch, login, input, attach, signal or runtime mutation was performed.
- No credentials were used and no production canonical registration was created.
- `:98`, `6082`, PID and session remain `UNKNOWN` / `NOT_REGISTERED` without direct evidence.
- Exact client fence remains `15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- PR #303 runtime-owned paths/processes and Track B were untouched.
- No branch protection, lease/identity gate or host-security boundary was weakened.
- No owner-funded Codex/OpenAI API or paid AI quota was used.

# Closeout

```yaml
closeout:
  implementation_complete: true
  outcome_verified: true
  audit:
    result: PASS
    validator: fresh GitHub-hosted acceptance-audit job 95120629610
    material_findings_open: 0
  e2e:
    result: NOT_APPLICABLE
    reason: manager acceptance is OS process/flock supervision; live Tibia mutation is outside authorization
  final_ci:
    head: d5bff95997e82d4ac5180d0e9c1b85dae8a3c7dd
    result: PASS
    required_checks:
      - CI / Required job 95120881462
  pull_requests:
    implementation_pr: blakinio/otclient#321
    implementation_pr_terminal: true
    unresolved_review_threads: 0
    prior_closeout_pr: blakinio/otclient#319 superseded by later P1
  task_status: completed
  ownership_released: true
  stale_closeout_reused: false
```
