---
task_id: OTC-20260817-track-a-auth-session-flow-static
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: docs/OTC-20260817-track-a-auth-session-flow-static
base_branch: main
base_main: 8a5fcfd72f2554261eef91a2129c9cc076e730ea
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-auth-session-flow-static.md
  - docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/**
  - docs/research/native-client/NATIVE_AUTH_SESSION_FLOW.md
  - .github/workflows/tibia-official-client-re-auth-session-static.yml
modules_touched: []
reuses:
  - main exact-client Track A evidence and canonical reports
  - PR #284 read-only official 15.32 game-login oracle at 69f9f0fa6dd390e57a11d828508753f7e45988ce
  - main TGameClient primary-vptr profile 0x3076908
  - PR #497 exact-fenced file-only source staging pattern without overlapping its owned paths
depends_on:
  - main@8a5fcfd72f2554261eef91a2129c9cc076e730ea
blocks: []
policy_version: 2
prompting_standard_version: 2.1
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: terminal_only
decomposition_decision: phased
validation_level: focused
execution_class: github_hosted
source_staging_class: exact_fenced_file_only_nonsemantic
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
  type: protocol
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: internal_only
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
invocation_started_at: 2026-08-17T18:44:21+02:00
last_progress_at: 2026-08-17T18:44:21+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
next_action: stage exact-fenced bounded TGameClient/auth/character/game-login code and vtable windows, decode only on GitHub-hosted Linux, and resolve the primary receiver vtable+0x68 target without runtime/login/secret access
---

# Track A — native authentication/session flow (static)

## Objective

Recover the exact-client native authentication/session control and credential lifecycle far enough to answer the owner's `OTS_NATIVE_AUTH_SESSION_RESEARCH_AGENT` charter without automating the UI and without bypassing server authentication.

The desired proof chain is:

```text
startup
 -> credential/session source
 -> authentication entry point
 -> auth request/response
 -> session state
 -> character list
 -> character selection
 -> game-server login
 -> authenticated game session
```

This task starts strictly as static/artifact reverse engineering. It does not inherit or consume PR #475's physical worldmap login/runtime budget.

## Trusted acceptance inventory

The task is not complete until evidence supports the final report at `docs/research/native-client/NATIVE_AUTH_SESSION_FLOW.md`, including:

```text
CAN_SKIP_LOGIN_FORM: YES | NO | PARTIAL
CAN_SKIP_PASSWORD_ENTRY: YES | NO | PARTIAL
CAN_REUSE_SESSION: YES | NO | UNKNOWN
PASSWORD_REQUIRED_FOR_GAME_LOGIN: YES | NO | UNKNOWN
DIRECT_CHARACTER_LOGIN_POSSIBLE: YES | NO | UNKNOWN
```

It must also identify, or explicitly leave `UNKNOWN`:

- the lowest safe programmatic entry point below the login UI;
- credential source and lifecycle for email/account, password, OTP/2FA, device/session state and saved-login state;
- auth transport/request/response boundary;
- session/token/ticket creation, storage, consumption, refresh/expiry/destruction;
- character-list acquisition and selected-character transition;
- the exact game-server login credential family and whether plaintext password participates;
- reconnect behavior;
- logout/change-character/session-expiry behavior.

No field meaning may be inferred only from conventional Tibia/OTClient/Canary behavior. Comparators are interpretation aids, not proof of the official Linux client.

## Accepted exact-client inputs

### FACT — exact binary fence

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

### FACT — corrected primary game-login signal chain

Promoted Track A evidence consumed read-only by Track B records:

```text
TLoginProtocolMessageHandler::sendLoginMessage signal PMF 0xcf2950
 -> QObject connect at 0x7d564f
 -> QSlotObject trampoline 0x7d4220
 -> captured slot PMF 0xbd36a0
 -> receiver virtual slot +0x68
```

`0xcf2ca0` is a Qt static-metacall case and `0xbd36a0` is an adapter/delegator. Neither is proven to be the final wire serializer.

Known exact-SHA transition leads:

```text
TAuthenticationProcessController::requestCharacterGameserverLogin     0xcfb2e7
TAuthenticationProcessController::onStartGameServerLoginStateEntered  0xcfb122
TCharacterSelectionController::requestCharacterLogin                  0xd47300
TGameClient::connectClientToGameserverWithExistingCredentials         0xd06660
TGameClient::onConnectClientToGameserver                               0xd06810
TGameClient::onGameSessionConnected                                    0xd066e0
TGameserverLoginProcessController::onGameserverTCPConnectionConnected  0xcfa0e0
```

### FACT — reusable exact-SHA class lead

Current `main` consolidated Track A evidence identifies primary vptr candidate:

```text
TGameClient 0x3076908
```

This is a static exact-binary lead only; the task must prove whether it is the receiver behind the `0xbd36a0 -> vslot +0x68` route before assigning semantics.

## Safety boundary

Forbidden in this task phase:

- any official-client process/X11 observation or mutation;
- login, relogin, character selection or game action;
- use of PR #475 runtime/session budget;
- process memory, debugger attach, input injection, OCR, xdotool, screen/pixel automation;
- printing, copying, persisting or uploading credentials, cookies, tokens, session keys or secret-bearing packet payloads;
- full proprietary executable upload;
- owner-funded Codex/OpenAI/API use.

Permitted source-side work is only exact-fenced file-backed bounded byte staging from the retained exact executable, with no source-side disassembly or semantic classification. Semantic decode runs on GitHub-hosted Linux.

## Initial hypotheses

```text
H1: the primary sendLoginMessage receiver can be identified from an exact known vtable and its +0x68 slot without runtime access.
H2: connectClientToGameserverWithExistingCredentials is downstream of already-established authentication/session state and therefore exposes the most direct static route to determine what the game login consumes.
H3: requestCharacterLogin/requestCharacterGameserverLogin form the character-selection handoff into the existing-credentials game-login path.
H4: initial account authentication, persisted-session recovery and reconnect may be separate state-machine routes and must not be collapsed without direct evidence.
```

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-17T18:44:21+02:00
head: PENDING_FIRST_TASK_COMMIT
branch: docs/OTC-20260817-track-a-auth-session-flow-static
pr: none
status: investigating
context_routes:
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-login-recovery-import.md
  - PR #284 tools/tibia-global-login-lab/evidence/official-1532-game-login-oracle.md
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-auth-session-flow-static.md
  - docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/**
  - docs/research/native-client/NATIVE_AUTH_SESSION_FLOW.md
  - .github/workflows/tibia-official-client-re-auth-session-static.yml
proven:
  - exact client fence is version 15.32.df7b29 / size 51965216 / sha256 e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  - sendLoginMessage is a Qt signal and the proven path reaches adapter 0xbd36a0 then receiver virtual slot +0x68
  - TGameClient primary-vptr candidate 0x3076908 exists in promoted exact-SHA evidence
derived:
  - static exact-fenced work can proceed independently of PR #475 physical runtime
unknown:
  - exact primary receiver behind adapter 0xbd36a0
  - final game-login serializer and ordered public/pre-secret fields
  - initial account-auth request and response parser
  - session credential type/storage/lifetime
  - password participation after initial auth
  - reconnect and character-switch credential behavior
conflicts:
  - none
first_failure:
  marker: none
  evidence: none
rejected_hypotheses:
  - 0xcf2ca0 is the final game-wire serializer: disproven by exact Qt metacall classification
  - 0xbd36a0 is already proven as final serializer: disproven by its proven virtual delegation through receiver+0x68
changed_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-auth-session-flow-static.md
validation:
  - command: repository/live-state/governance preflight
    result: PASS
    evidence: main 8a5fcfd72f2554261eef91a2129c9cc076e730ea; no overlapping Track A auth/session PR found
blockers:
  - none
next_action: stage exact-fenced bounded TGameClient/auth/character/game-login code and vtable windows, decode only on GitHub-hosted Linux, and resolve the primary receiver vtable+0x68 target without runtime/login/secret access
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 1
  session_id: auth-session-static-20260817T184421+0200
  session_started_at: 2026-08-17T18:44:21+02:00
  checkpointed_at: 2026-08-17T18:44:21+02:00
  last_progress_at: 2026-08-17T18:44:21+02:00
  phase: static-receiver-and-existing-credentials-chain
  exact_head: PENDING_FIRST_TASK_COMMIT
  pull_request: none
  active_operation: stage bounded exact-client file windows and hosted decode
  external_run_ids: []
  operation_started_at: null
  wait_deadline_at: null
  check_generation: draft
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: branch and task ownership remain unchanged and runtime_access remains none
  next_action: stage exact-fenced bounded TGameClient/auth/character/game-login code and vtable windows, decode only on GitHub-hosted Linux, and resolve the primary receiver vtable+0x68 target without runtime/login/secret access
```
