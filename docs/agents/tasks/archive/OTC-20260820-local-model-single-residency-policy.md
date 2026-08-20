---
task_id: OTC-20260820-local-model-single-residency-policy
status: completed
agent: ChatGPT
project_lane: otclient
lane: governance
track_id: local-ai-tooling
task_kind: documentation_policy
phase: completed
risk: low
branch: docs/OTC-20260820-local-model-single-residency-policy
base_branch: main
created: 2026-08-20T13:13:00+02:00
updated: 2026-08-20T13:31:00+02:00
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
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
network_listener_allowed: false
official_client_access: false
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github_connector
owned_paths: []
policy_pr: 625
policy_merge_sha: 9b5dc168dc755c9749517ac7b3c2dc4fd08889e2
policy_final_head: 1a0dbcfd24b6e63ea02f0d5aa6afb610f734d0c3
---

# Local model single-residency policy — completed

## Result

Repository-wide policy is promoted on trusted `main` by squash-merged PR #625.

The invariant is now mandatory:

```text
one physical host/shared GPU pool
-> at most one resident or actively inferencing local model
```

Model switching is sequential and fail closed: unload the previous model, verify residency, then invoke the next model. UNKNOWN, different-model or multi-model residency blocks a new inference session.

## Terminal validation

- `git diff --check`: PASS;
- exact final head `1a0dbcfd24b6e63ea02f0d5aa6afb610f734d0c3`:
  - CI `32363866306`: SUCCESS;
  - Track A agent runtime governance `32363866157`: SUCCESS;
  - Track A canonical live governance `32363866234`: SUCCESS;
- fresh independent exact-head review: PASS, P0/P1/P2 NONE, PR comment `5355244251`;
- review threads: zero;
- main freshness before merge: `4b6e0bd37fb0fcb4c432936032881ed4089f23a0`, no drift;
- merge: PR #625 -> `9b5dc168dc755c9749517ac7b3c2dc4fd08889e2`;
- resource hygiene: one local review model at a time, `keep_alive=0`, final `ollama ps` empty.

## Non-effects

This task did not merge blocked PoC PR #615, did not promote any local model, and grants no model, credential, paid-quota, Track A, official-client, gameplay or merge authority.

All task ownership is released. No further action is required.
