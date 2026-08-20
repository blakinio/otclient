---
task_id: OTC-20260820-local-model-single-residency-policy
status: ready
agent: ChatGPT
project_lane: otclient
lane: governance
track_id: local-ai-tooling
task_kind: documentation_policy
phase: closeout
risk: low
branch: docs/OTC-20260820-local-model-single-residency-policy
base_branch: main
created: 2026-08-20T13:13:00+02:00
updated: 2026-08-20T13:26:00+02:00
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
owned_paths:
  - AGENTS.md
  - docs/agents/contracts/LOCAL_MODEL_SINGLE_RESIDENCY_V1.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260820-local-model-single-residency-policy.md
---

# Local model single-residency policy

## Goal

Make the owner's resource rule repository-wide and fail closed: on one physical host/GPU pool, at most one local Ollama model may be resident or actively inferencing at a time.

## Acceptance criteria

- [x] Root `AGENTS.md` requires the rule for all future local-model work.
- [x] A normative contract defines preflight, switching, unload and failure behavior.
- [x] The rule is discoverable in the module catalogue and changelog.
- [x] Documentation/static validation and exact-head CI pass.
- [ ] PR is squash-merged and task ownership is released.

## Scope and non-effects

Documentation/governance only. This task does not load a model, run inference, touch the official client, consume credentials, grant Track A authority, or merge the blocked Ollama PoC PR #615.

## Reuse

PR #615 already implements a compatible `MAX_ONE_LOADED_MODEL` lifecycle on its blocked PoC branch. This task promotes only the durable repository-wide policy, not the unfinished PoC.

## Validation checkpoint

- implementation head `4219958c842d930a00a8871edd5391557f9aef3e`: `git diff --check` PASS;
- exact-head CI, Track A agent runtime governance and Track A canonical live governance: PASS;
- fresh independent read-only local-model review: PASS, P0/P1/P2 NONE, PR comment `5355217629`;
- resource hygiene: one review model only with `keep_alive=0`; follow-up `ollama ps` empty.

next_action: publish this ready checkpoint, obtain exact-head checks/review on the new task-only delta, then squash-merge PR #625 and archive/release ownership.
