---
task_id: OTC-20260815-track-a-live-runtime-lease-manager
status: completed
agent: ChatGPT
session_id: null
session_role: postmerge-closeout
session_rotation_count: 4
project_lane: otclient
lane: track-a-runtime-governance
track_id: official-client-re
task_kind: implementation
phase: closed
branch: docs/OTC-20260815-track-a-live-runtime-lease-manager-closeout
base_branch: main
base_main: f6fa2264904c6ffb3734d4a63e1edbb29260fcc1
risk: medium
related_prs:
  - 312
  - 313
created: 2026-08-15T22:04:00+02:00
updated: 2026-08-15T23:19:14+02:00
lease_released_at: 2026-08-15T23:19:14+02:00
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
completion_commit: f6fa2264904c6ffb3734d4a63e1edbb29260fcc1
semantic_run: 31908930698
semantic_unit_job: 95070957976
semantic_selfhosted_job: 95070958055
semantic_state: success
final_ci_run: 31909015855
final_ci_required_job: 95071316202
final_ci_state: success
review_threads_remaining: 0
stop_reason: completed
next_action: none
---

# Objective

Provide and safely promote the authoritative cooperative controller lease manager required before Track A may reuse one canonical live official-client runtime across sequential agents.

# Terminal result — FACT

The manager is on `main` and the post-merge concurrency remediation is on `main` at:

`f6fa2264904c6ffb3734d4a63e1edbb29260fcc1`

Production entrypoint:

`./.github/scripts/tibia-official-client-re-canonical-live-lease`

Authoritative state:

`/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime`

The implementation provides serialized `acquire`, `renew`, `validate`, `release`, redacted `status`, and `guard-run`; fixed production state path; task-local token confinement; atomic mode-0600 state; digest-only shared token state; explicit stale takeover reason; generation fencing; expiry validation; and a guarded mutation path whose child retains the same flock if the guard parent terminates.

# Post-merge remediation — FACT

PR #312 originally merged as `3575cc0c0a0b4efbcd9fc860d3226002fe40e70f`. Two material P1 review findings were then raised:

1. a surviving `guard-run` child could outlive the parent-held flock;
2. time was sampled before potentially blocking on the flock.

PR #313 repaired both. The corrected manager now passes the live flock descriptor into the guarded child and samples time only after lock acquisition for all time-sensitive operations.

Durable evidence:

`docs/agents/evidence/OTC-20260815-track-a-live-runtime-lease-manager/20260815-postmerge-p1-remediation.md`

# Validation — FACT

Independent remediation validation:

```text
run=31908930698 SUCCESS
head=2d548c67c0b0d9e39c5d8a51cd72fd1bba878d9a
unit_job=95070957976 SUCCESS
isolated_selfhosted_job=95070958055 SUCCESS
```

Final PR #313 repository validation:

```text
head=e5c1addad5cbfc9673c157ef7390639961046640
ci_run=31909015855 SUCCESS
ci_required_job=95071316202 SUCCESS
review_threads=0
reviews_requesting_changes=0
merge_commit=f6fa2264904c6ffb3734d4a63e1edbb29260fcc1
```

The two post-merge P1 review threads on merged PR #312 were resolved only after PR #313 reached `main`.

Runtime E2E is `NOT_APPLICABLE_WITH_REASON`: the lease manager deliberately does not start, stop, log in, control, attach to, or otherwise mutate the Tibia client. Its applicable E2E boundary is serialized lease behavior through the real CLI plus isolated Synology validation, all without touching the production canonical state.

# Safety / non-claims

- Production canonical-live state was not created or mutated by validation.
- No Tibia client process, login/session, input, display, VNC/noVNC endpoint, attach, signal, or gameplay state was mutated.
- `:98` is not canonicalized by this task.
- PR #303/#309 runtime-owned paths/processes and Track B were untouched.
- No owner-funded Codex/OpenAI API or paid AI quota was invoked by this task continuation.

# Acceptance inventory

- [x] authoritative serialized lease primitive implemented;
- [x] fixed production authority path enforced;
- [x] task-local capability token confinement enforced;
- [x] concurrent acquisition serialization proven;
- [x] stale takeover and generation fencing proven;
- [x] expired renew/validate/release rejected;
- [x] guarded child cannot outlive serialization if guard parent terminates;
- [x] expiry is rechecked after lock acquisition;
- [x] unit and isolated Synology validation PASS;
- [x] exact-final-head required CI PASS;
- [x] zero unresolved material review findings;
- [x] PR #312 merged;
- [x] PR #313 merged;
- [x] post-merge P1 threads resolved;
- [x] ownership released by this archive closeout.

# Follow-up boundary

This task only delivers the authoritative lease primitive. PR #311 remains responsible for the canonical-live policy/ADR reconciliation. No canonical display or live Tibia session is established by this task.
