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
last_progress_at: 2026-08-17T18:50:20+02:00
ci_checks_for_current_head: 1
ci_check_generation: phase1
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 1
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
next_action: run phase2 bounded static discriminator for exact QObject receiver provenance and concrete existing-credentials/connect/session targets without runtime/login/secret access
---

# Track A — native authentication/session flow (static)

## Objective

Recover the exact-client native authentication/session control and credential lifecycle required by the owner's `OTS_NATIVE_AUTH_SESSION_RESEARCH_AGENT` charter, without automating UI and without bypassing server authentication.

Required final artifact: `docs/research/native-client/NATIVE_AUTH_SESSION_FLOW.md`.

Required final decisions:

```text
CAN_SKIP_LOGIN_FORM: YES | NO | PARTIAL
CAN_SKIP_PASSWORD_ENTRY: YES | NO | PARTIAL
CAN_REUSE_SESSION: YES | NO | UNKNOWN
PASSWORD_REQUIRED_FOR_GAME_LOGIN: YES | NO | UNKNOWN
DIRECT_CHARACTER_LOGIN_POSSIBLE: YES | NO | UNKNOWN
```

## Exact-client fence

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official native Linux only
```

## Accepted starting chain

```text
TLoginProtocolMessageHandler::sendLoginMessage PMF 0xcf2950
 -> QObject connect 0x7d564f
 -> QSlotObject trampoline 0x7d4220
 -> adapter/delegator 0xbd36a0
 -> receiver virtual slot +0x68
```

`0xcf2ca0` is a Qt static-metacall case. `0xbd36a0` is a delegator, not a proven final serializer.

Known transition leads:

```text
TAuthenticationProcessController::requestCharacterGameserverLogin     0xcfb2e7
TAuthenticationProcessController::onStartGameServerLoginStateEntered  0xcfb122
TCharacterSelectionController::requestCharacterLogin                  0xd47300
TGameClient::connectClientToGameserverWithExistingCredentials         0xd06660
TGameClient::onConnectClientToGameserver                               0xd06810
TGameClient::onGameSessionConnected                                    0xd066e0
TGameserverLoginProcessController::onGameserverTCPConnectionConnected  0xcfa0e0
```

Promoted exact-SHA primary vptr lead: `TGameClient 0x3076908`.

## Safety boundary

`runtime_access: none` remains binding. This task does not inherit or consume PR #475's physical worldmap runtime/login budget. No live process/X11 observation or mutation; no login/relogin/game action; no process memory/debugger/input/OCR/screen automation; no credentials/cookies/tokens/session values/secret payloads; no full executable upload; no owner-funded Codex/OpenAI/API.

The Synology job may only exact-fence the retained executable and stage small bounded file-backed byte windows. Source-side disassembly and semantic classification are forbidden. Decode is GitHub-hosted.

## Phase 1 checkpoint

Durable evidence:

`docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/phase1-existing-credentials-chain.md`

Exact execution:

```text
workflow head: 053a5717a6d9306f70c80e61164e144e4143d075
run:           32047266485
source job:    95437930193  SUCCESS
hosted job:    95437962909  SUCCESS
```

Source safety markers prove exact file fence PASS, `runtime_access=none`, process/X11/login/secret/disassembly/semantic-classification all false, full client upload false, bounded file windows only.

### FACT — primary TGameClient +0x68 result

```text
TGameClient primary vptr: 0x3076908
TGameClient typeinfo:     0x3070398
primary-vptr +0x68:       0x6cc7b0
```

`0x6cc7b0` is a large construction-heavy routine initializing many object members/callback structures, not a proven login serializer.

### INFERENCE — rejected receiver shortcut

Confidence: high.

The promoted primary `TGameClient` vptr cannot be used as proof that `0xbd36a0`'s receiver is the desired login serializer object. Exact receiver provenance must be recovered from the connection setup rather than guessed from this vptr.

### FACT — concrete wrapper implementation targets

```text
connectClientToGameserverWithExistingCredentials 0xd06660 -> 0x6ef1d0
onGameSessionConnected                            0xd066e0 -> 0x6ee130
onConnectClientToGameserver                       0xd06810 -> 0x6fe480
```

### FACT — character-selection structure

`requestCharacterLogin @ 0xd47300` reads selected state at offsets `+0x50` (word), `+0x54` (dword), `+0x58` (dword/mode), passes the first two through `0x858a50`, then moves a three-qword result into storage referenced by `r12`. Exact field meanings and `r12` identity remain unknown.

### FACT — auth state transition

`requestCharacterGameserverLogin @ 0xcfb2e7` sets dispatch/state value `5` before jumping to the common authentication-controller transition route. Semantic meaning beyond the named method boundary remains unassigned.

## Context checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-17T18:50:20+02:00
head_before_checkpoint_commit: f24f66a03fc00418514c52199dab1f667bf1e5c5
branch: docs/OTC-20260817-track-a-auth-session-flow-static
pr: 498
status: investigating
proven:
  - exact client fence
  - 0xbd36a0 virtual delegation through receiver +0x68
  - primary TGameClient vptr +0x68 resolves to 0x6cc7b0
  - existing-credentials/connect/session wrappers resolve to 0x6ef1d0 / 0x6fe480 / 0x6ee130
  - phase1 workflow source and hosted jobs both succeeded
inferences:
  - primary TGameClient vptr is insufficient to identify the 0xbd36a0 receiver; connection provenance is required
unknown:
  - exact 0xbd36a0 receiver identity/vptr
  - semantics of 0x6ef1d0 / 0x6fe480 / 0x6ee130
  - semantics of 0x858a50 and r12 destination
  - final game-login serializer/fields
  - initial account-auth request/response
  - session credential/lifetime
  - password participation after initial auth
  - reconnect/logout/change-character credential behavior
first_failure:
  marker: none
  evidence: none
rejected_hypotheses:
  - primary TGameClient vptr +0x68 directly proves the 0xbd36a0 final game-login serializer
changed_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-auth-session-flow-static.md
  - docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/phase1-existing-credentials-chain.md
  - .github/workflows/tibia-official-client-re-auth-session-static.yml
validation:
  - run: 32047266485
    source_job: 95437930193 SUCCESS
    hosted_job: 95437962909 SUCCESS
blockers: []
next_action: phase2 bounded static discriminator for QObject receiver provenance, 0x6ef1d0, 0x6fe480, 0x6ee130, 0x858a50 and enclosing character-selection provenance
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 2
  session_id: auth-session-static-20260817T184421+0200
  session_started_at: 2026-08-17T18:44:21+02:00
  checkpointed_at: 2026-08-17T18:50:20+02:00
  last_progress_at: 2026-08-17T18:50:20+02:00
  phase: phase2-receiver-and-existing-credentials-implementations
  exact_head_before_checkpoint_commit: f24f66a03fc00418514c52199dab1f667bf1e5c5
  pull_request: 498
  completed_runs: [32047266485]
  active_operation: update temporary workflow to stage phase2 exact-fenced file windows
  external_run_ids: []
  operation_started_at: null
  wait_deadline_at: null
  check_generation: phase2-pending
  checks_used: 1
  status: active
  safe_to_resume: true
  resume_condition: PR #498 ownership remains unchanged and runtime_access remains none
  next_action: run phase2 bounded static discriminator for exact QObject receiver provenance and concrete existing-credentials/connect/session targets
```
