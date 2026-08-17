---
task_id: OTC-20260817-track-a-native-game-login-credential-proof
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: investigate
execution_mode: github_actions
execution_reason: exact-SHA static protobuf/serializer reconstruction is deterministic disposable Track A P2 work and must remain off the physical runtime
branch: docs/OTC-20260817-track-a-native-game-login-credential-proof
base_branch: main
base_main: 8a5fcfd72f2554261eef91a2129c9cc076e730ea
related_pr: ""
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-native-game-login-credential-proof.md
  - docs/agents/evidence/OTC-20260817-track-a-native-game-login-credential-proof/**
  - docs/research/native-client/NATIVE_GAME_LOGIN_CREDENTIAL_PROOF.md
  - .github/workflows/tibia-official-client-re-game-login-credential-proof.yml
modules_touched: []
reuses:
  - PR #498 exact-client auth/session static evidence and corrected native login queue boundary, read-only
  - historical same-SHA Track A QMeta/protobuf inventories already in blakinio/otclient
  - PR #284 official 15.32 Track B game-login oracle, read-only comparative evidence only
depends_on:
  - blakinio/otclient#498
blocks:
  - final resolution of PASSWORD_REQUIRED_FOR_GAME_LOGIN in blakinio/otclient#498
cross_repo_tasks: []
policy_version: 2
prompting_standard_version: 2.1
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
decomposition_decision: single
decomposition_reason: one narrow exact-client schema/provenance question with one durable evidence product
context_pressure: medium
context_growth: stable
context_score: 9
estimate_confidence: medium
validation_level: focused
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
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
promotion_authority: coordinator_only
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
invocation_started_at: 2026-08-17T21:17:00+02:00
last_progress_at: 2026-08-17T21:18:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: discovery
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
next_action: create the early draft PR, then recover exact protobuf field/wire structure and value provenance for GameclientMessageLogin and LoginRSAEncryptedBlock without runtime or secret access
---

# Track A — native game-login credential field proof

## Goal

Resolve the last material UNKNOWN left by `OTC-20260817-track-a-auth-session-flow-static`: determine from the exact official Linux client whether the game-server `GameclientMessageLogin` / `LoginRSAEncryptedBlock` path consumes the account password, a post-auth session credential, or both.

This task does not implement an authentication bypass. It proves native field membership and value provenance so later integration can preserve the legitimate authentication, 2FA/device confirmation, game-server challenge, session and reconnect flows.

## Required decisions

```text
PASSWORD_REQUIRED_FOR_GAME_LOGIN: YES | NO | UNKNOWN
GAME_LOGIN_CREDENTIAL: <proven native object/field path or UNKNOWN>
LOGIN_RSA_FIELDS: <exact names/types/wire tags if proven>
SECONDARY_LOGIN_RELATION: <proven relation or UNKNOWN>
```

## Acceptance criteria

- [ ] Exact client fence is revalidated before every promoted binary claim.
- [ ] Recover field membership and wire structure of `GameclientMessageLogin` and `LoginRSAEncryptedBlock` from generated protobuf/serializer code or descriptor data; string proximity alone is insufficient.
- [ ] Trace the values written into the login message back to native producers such as `TPlaySessionData`, selected character/world data, challenge data, or a password-bearing object.
- [ ] Distinguish initial account-auth credentials from game-server login credentials.
- [ ] Resolve `PASSWORD_REQUIRED_FOR_GAME_LOGIN` only when exact native evidence proves YES or NO; otherwise retain UNKNOWN with the precise missing discriminator.
- [ ] Document secondary-login/challenge behavior far enough to avoid mistaking a later challenge credential for the initial account password.
- [ ] Persist durable FACT / INFERENCE / UNKNOWN evidence and a final report.
- [ ] No credentials, cookies, tokens, session values, packet payloads, process memory, login, X11/runtime observation, input automation, raw executable upload, TLS weakening, auth/2FA bypass, or owner-funded AI/API usage.

## Runtime admission

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

PR #475 owns the current physical Track A runtime lane. This task must not observe, attach to, mutate, login through, reuse, or consume that runtime/session budget.

## Starting exact-client evidence from PR #498

Read-only dependency facts, to be independently revalidated where promoted here:

```text
TLoginProtocolMessageHandler::sendLoginMessage PMF                    0xcf2950
TAuthenticationProcessController::advanceStateMachineDirectlyToCharacterSelection 0xcfadcb
TLoginRequestUploader::loginSuccessful -> TCharacterList, TWorldList, TPlaySessionData
TGameClient::connectClientToGameserverWithExistingCredentials         wrapper 0xd06660 -> impl 0x6ef1d0
TCharacterSelectionController::requestCharacterLogin                  0xd47300
TAuthenticationProcessController::requestCharacterGameserverLogin     0xcfb2e7
TAuthenticationProcessController::onStartGameServerLoginStateEntered  0xcfb122
```

Known exact-client protobuf families include:

```text
GameclientMessageLogin
LoginRSAEncryptedBlock
GameclientMessageSecondaryLogin
SecondaryLoginRSAEncryptedBlock
GameserverMessageLoginChallenge
```

The prior proximity probe did not prove field membership and therefore correctly left `PASSWORD_REQUIRED_FOR_GAME_LOGIN=UNKNOWN`.

## Evidence standard

- `FACT`: exact-client descriptor/code/xref/wire-tag/value-flow evidence on the fenced SHA.
- `INFERENCE`: explicit derivation from FACTs with confidence and falsifier.
- `UNKNOWN`: not resolved by current evidence.

Comparative OTClient/Canary/Track B evidence may support a hypothesis but cannot prove official-client native behavior.

## Context checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-17T21:18:00+02:00
head: task-claim-commit
branch: docs/OTC-20260817-track-a-native-game-login-credential-proof
pr: none
status: investigating
context_routes:
  - PR #498 read-only dependency evidence
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-native-game-login-credential-proof.md
  - docs/agents/evidence/OTC-20260817-track-a-native-game-login-credential-proof/**
  - docs/research/native-client/NATIVE_GAME_LOGIN_CREDENTIAL_PROOF.md
  - .github/workflows/tibia-official-client-re-game-login-credential-proof.yml
proven:
  - trusted-base main is 8a5fcfd72f2554261eef91a2129c9cc076e730ea
  - Track A static work is admitted with runtime_access none
  - PR #475 remains a separate physical runtime owner and is not available to this task
derived: []
unknown:
  - exact fields/tags/types of GameclientMessageLogin and LoginRSAEncryptedBlock
  - exact producer of the game-login credential bytes
  - whether account password participates in game-server login
  - secondary-login credential relation
conflicts: []
first_failure:
  marker: none
  evidence: none
rejected_hypotheses: []
changed_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-native-game-login-credential-proof.md
validation:
  - command: not-run
    result: NOT_RUN
    evidence: task just claimed
blockers: []
next_action: open draft PR and run an exact-SHA generated-protobuf structure probe that does not rely on string proximity
```
