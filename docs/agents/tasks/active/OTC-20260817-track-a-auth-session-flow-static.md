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
pull_request: 498
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
last_progress_at: 2026-08-17T18:45:54+02:00
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

## Objective and acceptance

Recover the exact-client native authentication/session control and credential lifecycle required by the owner's `OTS_NATIVE_AUTH_SESSION_RESEARCH_AGENT` charter, without automating UI and without bypassing server authentication.

Required final artifact: `docs/research/native-client/NATIVE_AUTH_SESSION_FLOW.md`.

The task is not complete until evidence supports or explicitly leaves `UNKNOWN`/`PARTIAL` for:

```text
CAN_SKIP_LOGIN_FORM: YES | NO | PARTIAL
CAN_SKIP_PASSWORD_ENTRY: YES | NO | PARTIAL
CAN_REUSE_SESSION: YES | NO | UNKNOWN
PASSWORD_REQUIRED_FOR_GAME_LOGIN: YES | NO | UNKNOWN
DIRECT_CHARACTER_LOGIN_POSSIBLE: YES | NO | UNKNOWN
```

It must also cover the lowest safe below-UI entry point, credential source/lifecycle, auth request/response, session creation/storage/consumption/expiry, character-list and selection flow, game-server login credential, reconnect, logout and change-character behavior.

## Exact-client starting facts

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official native Linux only
```

Corrected proven game-login signal route:

```text
TLoginProtocolMessageHandler::sendLoginMessage PMF 0xcf2950
 -> QObject connect 0x7d564f
 -> QSlotObject trampoline 0x7d4220
 -> adapter/delegator 0xbd36a0
 -> receiver virtual slot +0x68
```

`0xcf2ca0` is a Qt static-metacall case and `0xbd36a0` is not proven to be the final wire serializer.

Exact-SHA transition leads:

```text
TAuthenticationProcessController::requestCharacterGameserverLogin     0xcfb2e7
TAuthenticationProcessController::onStartGameServerLoginStateEntered  0xcfb122
TCharacterSelectionController::requestCharacterLogin                  0xd47300
TGameClient::connectClientToGameserverWithExistingCredentials         0xd06660
TGameClient::onConnectClientToGameserver                               0xd06810
TGameClient::onGameSessionConnected                                    0xd066e0
TGameserverLoginProcessController::onGameserverTCPConnectionConnected  0xcfa0e0
```

Promoted exact-SHA vptr lead: `TGameClient 0x3076908`.

## Safety boundary

This task remains `runtime_access: none`. It does not inherit or consume PR #475's physical worldmap runtime/login budget. It must not observe/mutate a live client, process memory or X11; perform login/relogin/game actions; use debugger/input/OCR/screen automation; persist credentials/tokens/session values/secret payloads; upload the full executable; or use owner-funded Codex/OpenAI/API.

The Synology source job may only exact-fence the retained executable and stage small bounded file-backed byte windows. Source-side disassembly and semantic classification are forbidden; decode belongs on GitHub-hosted Linux.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-17T18:45:54+02:00
head: f48e62d8eff7ad0a1708e3440c086e8346ab3b71
branch: docs/OTC-20260817-track-a-auth-session-flow-static
pr: 498
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
  - exact client fence above
  - sendLoginMessage reaches adapter 0xbd36a0 then receiver virtual slot +0x68
  - TGameClient primary-vptr candidate 0x3076908 is promoted exact-SHA evidence
  - PR #498 is the dedicated Draft lane for this task
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
  - 0xcf2ca0 is final serializer: disproven by Qt metacall classification
  - 0xbd36a0 is already proven final serializer: disproven by virtual delegation
changed_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-auth-session-flow-static.md
validation:
  - command: live repository/governance/overlap preflight
    result: PASS
    evidence: main 8a5fcfd72f2554261eef91a2129c9cc076e730ea; open PR inventory checked; no overlapping Track A auth/session PR
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
  checkpointed_at: 2026-08-17T18:45:54+02:00
  last_progress_at: 2026-08-17T18:45:54+02:00
  phase: static-receiver-and-existing-credentials-chain
  exact_head: f48e62d8eff7ad0a1708e3440c086e8346ab3b71
  pull_request: 498
  active_operation: stage bounded exact-client file windows and hosted decode
  external_run_ids: []
  operation_started_at: null
  wait_deadline_at: null
  check_generation: draft
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: PR #498/branch ownership remains unchanged and runtime_access remains none
  next_action: stage exact-fenced bounded TGameClient/auth/character/game-login code and vtable windows, decode only on GitHub-hosted Linux, and resolve the primary receiver vtable+0x68 target without runtime/login/secret access
```
