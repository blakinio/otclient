---
task_id: OTC-20260817-track-a-auth-session-flow-static
status: completed
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: finalized-static
branch: docs/OTC-20260817-track-a-auth-session-flow-static
base_branch: main
base_main: 8a5fcfd72f2554261eef91a2129c9cc076e730ea
related_pr: "blakinio/otclient#498"
risk: medium
created: 2026-08-17
updated: 2026-08-17
owned_paths:
  - docs/agents/tasks/archive/OTC-20260817-track-a-auth-session-flow-static.md
  - docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/**
  - docs/research/native-client/NATIVE_AUTH_SESSION_FLOW.md
  - .github/workflows/tibia-official-client-re-auth-session-static.yml
reuses:
  - main exact-client Track A evidence and canonical reports
  - historical same-SHA Track A QMeta/static inventories from PR #48
  - PR #284 read-only official 15.32 game-login oracle at 69f9f0fa6dd390e57a11d828508753f7e45988ce
policy_version: 2
prompting_standard_version: 2.1
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
validation_level: focused
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
mutation_authorized: false
promotion_authority: coordinator_only
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
charter_result: PARTIAL
---

# Track A — native authentication/session flow (static)

## Goal

Recover the official Linux Tibia `15.32.df7b29` authentication/session control flow far enough to identify safe below-UI entry points, post-auth state ownership, character-selection/game-login transitions and reconnect behavior without live runtime, credentials or secret capture.

## Completion result

The authorized static discovery scope is **completed**. The wider `OTS_NATIVE_AUTH_SESSION_RESEARCH_AGENT` charter remains **PARTIAL**, because exact field-level native proof of the game-login credential and exact persisted-session expiry/refresh implementation require evidence outside this task's `runtime_access: none` authority.

Final research artifact:

`docs/research/native-client/NATIVE_AUTH_SESSION_FLOW.md`

Final synthesis evidence:

`docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/phase6-final-auth-session-synthesis.md`

## Final decisions

```text
STATUS: PARTIAL
CAN_SKIP_LOGIN_FORM: PARTIAL
CAN_SKIP_PASSWORD_ENTRY: PARTIAL
CAN_REUSE_SESSION: YES
PASSWORD_REQUIRED_FOR_GAME_LOGIN: UNKNOWN
DIRECT_CHARACTER_LOGIN_POSSIBLE: YES
BEST_BYPASS_ENTRY_POINT: TAuthenticationProcessController::advanceStateMachineDirectlyToCharacterSelection @ 0xcfadcb, conditional on valid retained auth/play-session state
SESSION_CREDENTIAL: tibia::login::TPlaySessionData; native SessionKey/sessionkey concept proven, exact field/persistence/expiry mapping UNKNOWN
```

For cold auth without valid retained state, the safe below-UI boundary is `TGameClient::onRequestLoginWithCredentials(QString,QString)` followed by the client's legitimate auth/2FA/device-confirmation state machine.

## Acceptance criteria

- [x] Exact-client fence maintained for every promoted native claim.
- [x] Login UI/state-machine boundary identified without UI automation.
- [x] Native direct-to-character-selection shortcut identified.
- [x] Initial auth success boundary and `TPlaySessionData` identified.
- [x] Character-selection → game-login controller boundaries identified.
- [x] `connectClientToGameserverWithExistingCredentials` identified as a zero-argument native boundary.
- [x] `TProtocolMessageQueue` proven as the receiver in the corrected login-message connection chain.
- [x] Reconnect/error control surface identified, including routes to character selection and login dialog.
- [x] Password requirement for native game login evaluated without overclaiming; result remains `UNKNOWN` because field-level proof is absent.
- [x] Required final report and durable evidence produced.
- [x] No runtime/login/secret/process/X11 access was used.
- [x] Remaining proof requiring greater authority is isolated to a new, separately admitted task rather than silently expanding this task.

## Proven facts

1. Exact client:
   `15.32.df7b29`, size `51965216`, SHA256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
2. `TAuthenticationProcessController::advanceStateMachineDirectlyToCharacterSelection @ 0xcfadcb` is a zero-argument native state-machine entry.
3. `onLoginStateMachineStartedShortcutToCharacterSelection @ 0xcfad8b` is an explicit native shortcut route.
4. `TLoginRequestUploader::loginSuccessful` receives `TCharacterList`, `TWorldList`, and `tibia::login::TPlaySessionData`.
5. Native login schema includes `stayLoggedInByDefault`, `devicecookie`, `trusteddevicetoken`, `playdata`, `sessionkey` / `SessionKey` and the official `loginservice.php` endpoint.
6. `TGameClient::connectClientToGameserverWithExistingCredentials()` is zero-argument; wrapper `0xd06660` resolves to implementation `0x6ef1d0`.
7. `TCharacterSelectionController::requestCharacterLogin(TCharacter) @ 0xd47300` feeds the native game-login transition surface.
8. Corrected login-message chain reaches `[enclosing+0x88]`, proven as `tibia::protocol::TProtocolMessageQueue` via QMeta `0x3085b60`.
9. `TGameSessionDisconnectReactionController` explicitly handles session/game disconnect, login errors/challenges/waits, ping timeouts and fallback to either character selection or login dialog.
10. Exact static protobuf/type inspection proves `GameclientMessageLogin` / `LoginRSAEncryptedBlock` families exist but does not prove whether plaintext password is a field or source value.

## Rejected hypotheses / overclaims

- `0xcf2ca0` is not the implementation PMF for `sendLoginMessage`; it is a Qt static-metacall case.
- `0xbd36a0` is not a proven final serializer; it is an adapter/delegator.
- `0x858a50` is not credential transport; it is UI/status formatting.
- Static proximity of `Password` or `SessionKey` strings to protobuf type names is not sufficient to infer native field membership.
- The static task does not claim `PASSWORD_REQUIRED_FOR_GAME_LOGIN=NO`.

## Validation

### Final full static synthesis

```text
commit: b465d3fcaa888b4d871f5070cfaf9dc9999c8523
workflow run: 32057651024
job: 95471381728
result: SUCCESS
```

Key markers:

```text
AUTHSESSION_FINAL_EXACT_PACKED_SHA=PASS
AUTHSESSION_FINAL_EXACT_CLIENT_SHA=PASS
AUTHSESSION_RUNTIME_ACCESS=none
AUTHSESSION_LOGIN_PERFORMED=false
AUTHSESSION_SECRET_ACCESS=false
AUTHSESSION_PROCESS_X11_OBSERVATION=false
AUTHSESSION_RAW_CLIENT_UPLOADED=false
AUTHSESSION_FINAL_STATIC_SYNTHESIS=PASS
```

### Final game-login schema discriminator

```text
commit: b62002215e900df653418c48255f08c8c02b4e10
workflow run: 32058203684
job: 95473127456
result: SUCCESS
```

Key markers:

```text
AUTHSESSION_SCHEMA_EXACT_CLIENT_SHA=PASS
AUTHSESSION_RUNTIME_ACCESS=none
AUTHSESSION_LOGIN_PERFORMED=false
AUTHSESSION_SECRET_ACCESS=false
AUTHSESSION_SCHEMA_STATIC_PROBE=PASS
```

## Remaining unknowns

- exact `TPlaySessionData` field layout;
- exact persistent store / launcher/keyring handoff path;
- session expiry/refresh/destruction policy;
- exact `GameclientMessageLogin` / `LoginRSAEncryptedBlock` credential fields;
- whether plaintext password participates in game-server login;
- exact cold-start persisted-character preselection path.

These unknowns are not blockers for closing this **static discovery task**. They are blockers for promoting the wider research charter from `PARTIAL` to `DONE`.

## Follow-up admission boundary

If full charter completion is required, create a new Track A task with explicit minimal runtime admission. It must be separate from PR #475's worldmap runtime budget, must redact secrets at source, and must capture only field/provenance/consumer identity—not credential values.

## Final checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-17T21:05:00+02:00
branch: docs/OTC-20260817-track-a-auth-session-flow-static
pr: 498
status: completed
context_routes:
  - docs/research/native-client/NATIVE_AUTH_SESSION_FLOW.md
  - docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/phase6-final-auth-session-synthesis.md
owned_paths:
  - docs/agents/tasks/archive/OTC-20260817-track-a-auth-session-flow-static.md
  - docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/**
  - docs/research/native-client/NATIVE_AUTH_SESSION_FLOW.md
  - .github/workflows/tibia-official-client-re-auth-session-static.yml
proven:
  - native direct-to-character-selection shortcut exists
  - successful account auth returns TPlaySessionData with character/world data
  - native game connection has zero-argument existing-credentials entry
  - TProtocolMessageQueue receiver identity is proven
  - reconnect controller has explicit character-selection/login-dialog fallback routes
derived:
  - valid retained native state can bypass the visual login form without bypassing authentication
unknown:
  - exact native game-login credential field contract
  - exact persisted-session expiry/refresh/store implementation
conflicts: []
first_failure:
  marker: none
  evidence: none
rejected_hypotheses:
  - password absence inferred from protobuf/string proximity
  - 0xbd36a0 treated as final serializer
changed_paths:
  - docs/research/native-client/NATIVE_AUTH_SESSION_FLOW.md
  - docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/phase1-existing-credentials-chain.md
  - docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/phase2-connection-and-existing-credentials.md
  - docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/phase3-provenance-and-corrections.md
  - docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/phase4-enclosing-connection-setup.md
  - docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/phase5-protocol-message-queue-identity.md
  - docs/agents/evidence/OTC-20260817-track-a-auth-session-flow-static/phase6-final-auth-session-synthesis.md
  - .github/workflows/tibia-official-client-re-auth-session-static.yml
validation:
  - command: GitHub Actions run 32057651024 / job 95471381728
    result: PASS
    evidence: AUTHSESSION_FINAL_STATIC_SYNTHESIS=PASS on exact client SHA
  - command: GitHub Actions run 32058203684 / job 95473127456
    result: PASS
    evidence: AUTHSESSION_SCHEMA_STATIC_PROBE=PASS on exact client SHA
blockers: []
next_action: none for this static task; full-charter runtime proof requires a new separately admitted task
```

## Completion

- Static task status: `completed`
- Wider charter result: `PARTIAL`
- PR: `#498`
- Runtime access consumed: none
- Secrets accessed: none
- Archived at: `docs/agents/tasks/archive/OTC-20260817-track-a-auth-session-flow-static.md`
