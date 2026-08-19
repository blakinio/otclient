---
task_id: OTC-20260819-track-a-auth-session-current-build-static
status: ready
agent: ChatGPT
project_lane: otclient
lane: RUNTIME
track: official-client-re
task_kind: reverse_engineering_protocol
phase: validate
branch: research/OTC-20260819-track-a-auth-session-current-build-static
base_branch: main
base_main: 82e5f435c3aa4172115bf7f6a0cd7a5cc6da3d50
current_main_observed: cf90b84442dda730bdab93d8aa9f3236b7532ad8
worktree: github-hosted-ephemeral:research/OTC-20260819-track-a-auth-session-current-build-static
created: 2026-08-19T09:34:30+02:00
updated: 2026-08-19T09:50:30+02:00
risk: medium
execution_mode: github-only
execution_reason: deterministic disposable exact-binary static analysis and repository delivery use GitHub connector plus GitHub-hosted Actions
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
context_pressure: medium
decomposition_decision: single
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
runtime_access: none
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
promotion_authority: coordinator_only
researcher_delivery: draft_pr_only
owned_paths:
  - .github/workflows/track-a-auth-session-current-build-static.yml
  - docs/agents/evidence/OTC-20260819-track-a-auth-session-current-build-static/**
  - docs/agents/tasks/active/OTC-20260819-track-a-auth-session-current-build-static.md
dependencies:
  - PR #555 current official-client fence advance; open Draft/read-only dependency, do not edit its paths
  - PR #528 native-login E2E; consume durable evidence only, do not edit or perform login
  - PR #498 historical auth/session static evidence; exact old-build evidence only
  - PR #499 historical game-login credential schema evidence; exact old-build evidence only
---

# TIBIA-RE-AUTH-SESSION — current-build static revalidation

## Objective

Revalidate the authentication/session structural surface against the exact current public official native-Linux Tibia binary (`size=52109920`, `sha256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`) without inheriting old addresses, credential authority, login authority, or canonical-runtime authority.

## Admission

```yaml
track_id: official-client-re
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
```

No Synology physical runtime, KasmVNC/X11, process memory, input, credentials, Secrets, session values, login, character selection, relogin, gameplay, package mutation, proxy mutation, or canonical lease/registration mutation was performed.

## Acceptance inventory

- [x] Verify packed fingerprint `10214529 / 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354` and unpacked fingerprint `52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8` before analysis.
- [x] Verify ELF build ID `d803d9695868713ef6ab0c3cf65f91212c9c6a62`.
- [x] Do not upload, commit, or retain proprietary raw client bytes.
- [x] Recover current-build `TGameClient` QMeta identity and `onRequestLoginWithCredentials(QString,QString)`.
- [x] Recover its current-build full-range dispatch target/instruction fence without reusing an old address.
- [x] Recover current-build QMeta targets for `loginSuccessful`, `connectClientToGameserverWithExistingCredentials`, and `requestCharacterLogin`.
- [x] Inventory targeted character/world/play-session/game-server-login/disconnect structural family; 19/19 target names present.
- [x] Mark historical #498/#499 addresses `SUPERSEDED_FOR_CURRENT_BUILD_UNLESS_REDISCOVERED`.
- [x] Persist sanitized evidence; no credential/session values and no raw binary.
- [x] Exact recovery-head workflow, repository CI, and Track A governance passed on `db0dc96afa5fadd02a151f6dc09d1f6b9a3b6411`.
- [x] Leave result in Draft PR #556; researcher does not merge or promote canonical coverage.

## Proven current-build facts

Successful static workflow `32228900775 / 95994337407` independently produced:

```text
AUTHSESSION_CURRENT_EXACT_CLIENT_SHA=PASS
AUTHSESSION_QMETA_OBJECTS_PARSED=194
AUTHSESSION_TGAMECLIENT_QMETA_COUNT=1
AUTHSESSION_TGAMECLIENT_STATIC_METAOBJECT=0x2f82be0
AUTHSESSION_TGAMECLIENT_STATIC_METACALL=0xd19100
AUTHSESSION_TGAMECLIENT_METHOD_COUNT=44
AUTHSESSION_TGAMECLIENT_SIGNAL_COUNT=6
AUTHSESSION_COLD_AUTH_METHOD=onRequestLoginWithCredentials
AUTHSESSION_COLD_AUTH_META_INDEX=17
AUTHSESSION_COLD_AUTH_ARGC=2
AUTHSESSION_COLD_AUTH_METHOD_FLAGS=0x8
AUTHSESSION_COLD_AUTH_RAW_PARAM_TYPE_IDS=0x2b,0xa,0xa
AUTHSESSION_COLD_AUTH_DISPATCH_LEA=0xd1910a
AUTHSESSION_COLD_AUTH_DISPATCH_TABLE=0x1d903c4
AUTHSESSION_COLD_AUTH_DISPATCH_TARGET=0xd196f0
AUTHSESSION_COLD_AUTH_TARGET_INSTRUCTION_FENCE=488b5110488b71084883c4485b5de93d609cff0f1f440000488bbfa009000048
AUTHSESSION_CURRENT_QMETA_TARGET_METHOD_HITS=3
AUTHSESSION_CURRENT_STRUCTURAL_STRING_TARGETS_PRESENT=19/19
AUTHSESSION_CURRENT_STATIC_DISCRIMINATOR=PASS
AUTHSESSION_CURRENT_BUILD_ID_FENCE=PASS
AUTHSESSION_RAW_CLIENT_RETAINED=false
```

Additional current-build QMeta targets:

```text
TLoginRequestUploader::loginSuccessful                         -> 0xd10200
TGameClient::connectClientToGameserverWithExistingCredentials -> 0xd19500
TCharacterSelectionController::requestCharacterLogin          -> 0xd52050
```

Durable evidence: `docs/agents/evidence/OTC-20260819-track-a-auth-session-current-build-static/current-build-static-result.md`.

## Classification

### FACT

- The exact current binary preserves the 44-method / 6-signal `tibia::client::TGameClient` QMeta shape.
- `onRequestLoginWithCredentials` remains method index 17 with two `QString` parameters and exact-build target `0xd196f0`.
- `loginSuccessful`, `connectClientToGameserverWithExistingCredentials`, and `requestCharacterLogin` have current-build QMeta dispatch targets recorded above.
- All 19 bounded structural auth/session target names are present.

### SUPERSEDED

Historical old-build addresses including `0xd06260`, `0xd06850`, `0xcfadcb`, `0xcfad8b`, `0xd06660`, `0x6ef1d0`, `0xd47300`, `0xcfb2e7`, and `0xcfb122` are not current-build addresses unless separately rediscovered.

### UNKNOWN

- exact current executable targets for non-QMeta methods such as `advanceStateMachineDirectlyToCharacterSelection`, `requestCharacterGameserverLogin`, and `onStartGameServerLoginStateEntered`;
- current `TPlaySessionData` / `TAuthenticationAndEncryptionInfo` field provenance and password requirement semantics;
- live object instances, vptr/runtime addresses, thread affinity, login success, character/world entry, causal `IN_GAME`, and restart/relogin stability.

## Safety evidence

```text
AUTHSESSION_RUNTIME_ACCESS=none
AUTHSESSION_CLIENT_EXECUTED=false
AUTHSESSION_LOGIN_PERFORMED=false
AUTHSESSION_SECRET_ACCESS=false
AUTHSESSION_RAW_CLIENT_UPLOADED=false
AUTHSESSION_RAW_CLIENT_RETAINED=false
```

PR #555 remains an independent Draft. This researcher does not advance trusted-base canonical runtime authority and does not authorize physical helper reuse by itself.

## Exact-head validation

Recovery head `db0dc96afa5fadd02a151f6dc09d1f6b9a3b6411` passed all three required validation classes:

```text
Track A agent runtime governance 32229510845 = SUCCESS
Track A current-build auth session static discriminator 32229510871 = SUCCESS
CI 32229511024 = SUCCESS
```

The branch remained mergeable, Draft PR #556 remained open, and current `main` was still `cf90b84442dda730bdab93d8aa9f3236b7532ad8` at the ready transition. The final ready-checkpoint commit changes only this task record; its exact-head check generation is the only remaining validation operation and must pass before coordinator promotion.

## Audit

```yaml
audit:
  type: proportionate researcher self-review
  changed_paths: 3
  declared_paths_match: true
  runtime_or_secret_side_effects: none
  unrelated_scope: none found
  review_threads_at_last_check: 0
  material_findings_open: 0
```

E2E: `NOT_APPLICABLE` — static repository research only; the official client was never executed.

## Context checkpoint

```yaml
checkpoint_version: 1
status: ready
phase: validate
branch: research/OTC-20260819-track-a-auth-session-current-build-static
draft_pr: 556
final_ready_head: pending-this-ready-checkpoint-commit
current_main_observed: cf90b84442dda730bdab93d8aa9f3236b7532ad8
facts:
  - Current-build cold-auth QMeta contract is statically re-proven on exact SHA ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8.
  - Current-build QMeta targets for loginSuccessful, connectClientToGameserverWithExistingCredentials, and requestCharacterLogin are recovered.
  - Recovery head db0dc96a passed task-owned static validation, Track A governance, and repository CI.
  - Raw proprietary client bytes were deleted and not uploaded.
  - No login/credential/runtime effects occurred.
unknown:
  - current non-QMeta state-machine target addresses and live/runtime semantics listed above.
blocker: none
next_action: Coordinator independently review Draft PR #556 and its durable evidence; accept, return for evidence, or supersede it under the parallel-research promotion contract. Do not self-merge from the researcher role.
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 2
  session_id: chatgpt-20260819-0950-auth-session
  session_started_at: 2026-08-19T09:50:00+02:00
  checkpointed_at: 2026-08-19T09:50:30+02:00
  last_progress_at: 2026-08-19T09:50:30+02:00
  phase: validate
  exact_head: pending-this-ready-checkpoint-commit
  pull_request: 556
  active_operation: final exact-head validation
  external_run_ids: []
  operation_started_at: 2026-08-19T09:50:30+02:00
  wait_deadline_at: 2026-08-19T10:35:30+02:00
  check_generation: final-ready
  checks_used: 0
  status: ready
  safe_to_resume: true
  resume_condition: final ready-head exact checks reach terminal conclusions.
  next_action: Inspect the final ready-head exact checks; if they all pass, freeze the researcher Draft with no further code/task mutation and hand it to the coordinator.
```
