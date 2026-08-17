# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME

```yaml
prompt_contract:
  version: 2.0.0
  alias: OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME
  track_id: official-client-re
  task_kind: runtime_reverse_engineering_semantic_control
  risk: critical
  platform: official_native_linux_only
  run_scope: single_task
  continuation_policy: continue_within_task_until_success_or_real_stop
  user_communication: low_noise
  objective: Drive the exact official Linux Tibia client from legal native auth/session state through native character selection to causally proven active gameplay without GUI login automation.
  baseline_version: owner-supplied draft reviewed on 2026-08-17
  eval_suite: docs/agents/tasks/active/OTC-20260817-track-a-native-login-to-ingame-prompt.md
  rollback_version: revert the prompt-introduction PR
```

Run autonomously in:

```text
blakinio/otclient
```

This is a Track A `official-client-re` RUNTIME / reverse-engineering / semantic-control task with critical safety rigor.

Do not treat this prompt, chat history, historical PR prose, historical PID/XID/display/session data, or an old task checkpoint as current runtime authority. Current trusted-base governance, live Git/task/PR state, current runtime ownership, current admission, leases/registration/generation and exact environment evidence take precedence.

## 1. Objective

Bring the original official native Linux Tibia client to:

```text
CHARACTER ACTUALLY LOGGED INTO GAME
```

using native client logic below the login form/UI layer.

Target control model:

```text
agent
  -> semantic/native bridge
  -> TGameClient / authentication/session state
  -> native character model
  -> native character-selection controller
  -> native game-login state machine
  -> server acceptance
  -> local player + gameplay state active
```

Do not build the control plane as:

```text
agent
  -> screenshot
  -> OCR
  -> textbox detection
  -> coordinate clicking
  -> blind typing
```

Control the client semantically through its existing classes, methods, QObject instances, signals, slots, QMeta routes, state machines and retained native authentication/session state.

Prefer invoking original client logic over reimplementing original protocol logic.

## 2. Only task-success gate

Normal task success exists only when:

```text
RESULT: SUCCESS
CHARACTER_ACTUALLY_LOGGED_INTO_GAME: YES
CAUSAL_PROOF: COMPLETE
```

Do not call the task DONE merely because any of the following occurred:

- login form visible;
- login form skipped;
- initial authentication accepted;
- `TPlaySessionData` obtained;
- character list obtained;
- character selected;
- `requestCharacterLogin` invoked;
- game-server connection started;
- `GameclientMessageLogin` constructed;
- `LoginRSAEncryptedBlock` constructed;
- TCP/TLS established;
- login-success packet received;
- game initialization started.

All of those are intermediate states unless active gameplay has been causally proven.

## 3. Task success is not worker invocation termination

`docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md` is mandatory.

Task completion remains possible only at the success gate above. A worker invocation may legally end with:

```text
ROTATE
WAITING
BLOCKED
```

when required by anti-stall/runtime budget, repair-cycle limits, current authority, runtime ownership, external 2FA/device confirmation, missing protected credential ingress, environment/tool limits or another current safety gate.

On such a worker stop:

- do not mark the task DONE;
- persist a durable checkpoint;
- preserve proven facts and rejected hypotheses;
- record exactly one `next_action`;
- make continuation possible from Git/task state without chat history.

## 4. Exact client hard fence

Work only on:

```yaml
version: 15.32.df7b29
platform: official_native_linux_only
unpacked_size: 51965216
unpacked_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed_client_lzma_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
```

Any different version, size, SHA-256, platform, unverifiable executable identity or contradictory process evidence fails closed.

Every promoted function, method, vtable, RTTI association, offset, static VA, RVA, runtime address, object layout, signature or QMeta target must be re-bound to this exact SHA.

## 5. Mandatory live-state preflight

Before implementation or runtime work:

1. read current root `AGENTS.md`;
2. read `docs/agents/AGENTS.md`;
3. read current `docs/agents/PROMPTING_HANDOVER.md`;
4. read current `docs/agents/PROMPTING_STANDARD.md`;
5. read `docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md`;
6. read `docs/agents/TIBIA_RESEARCH_TRACKS.md`;
7. read `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`;
8. read current Track A runtime/bootstrap/rebind/canonical-runtime contracts required by trusted base;
9. verify current `main`;
10. inspect active Track A tasks and all relevant open PRs;
11. inspect current runtime owner, namespace, admission, lease, registration and generation;
12. inspect ownership overlap and barriers;
13. inspect current PR #475 state;
14. inspect current PR #498 and #499 state;
15. determine whether predecessor findings were canonically promoted or remain researcher evidence.

Do not ask the owner for information resolvable from live repository state.

## 6. Predecessor evidence trust boundary

PR #498 and PR #499 are predecessor research inputs, not automatically canonical-main facts while unpromoted/unmerged.

Known predecessor findings include the following candidates.

### Initial auth

```text
TGameClient::onRequestLoginWithCredentials(QString, QString)
```

is a predecessor native credential-auth entry point.

Successful initial auth has predecessor evidence for:

```text
TLoginRequestUploader::loginSuccessful(
    TCharacterList,
    TWorldList,
    TPlaySessionData
)
```

### Session/UI bypass

```text
TAuthenticationProcessController::advanceStateMachineDirectlyToCharacterSelection
static VA candidate: 0xcfadcb
```

and:

```text
TGameClient::connectClientToGameserverWithExistingCredentials()
wrapper candidate: 0xd06660
implementation candidate: 0x6ef1d0
```

Predecessor research indicates session reuse/direct character login is possible when appropriate retained state exists.

### Character login

```text
TCharacterSelectionController::requestCharacterLogin(TCharacter)
candidate @ 0xd47300
  -> TAuthenticationProcessController::requestCharacterGameserverLogin
     candidate @ 0xcfb2e7
  -> TAuthenticationProcessController::onStartGameServerLoginStateEntered
     candidate @ 0xcfb122
```

### Game-login message path

```text
TAuthenticationAndEncryptionInfo
  -> TLoginProtocolMessageHandler candidate @ 0xe1abe0
  -> GameclientMessageLogin
     -> field 7 = LoginRSAEncryptedBlock
  -> TProtocolMessageQueue::sendLogin(GameclientMessageLogin)
  -> QMeta target candidate 0xdf6be2
  -> queue consumer candidate 0xbd36a0
```

Predecessor type candidate:

```text
tibia::authentication::TAuthenticationAndEncryptionInfo
vtable candidate: 0x2f63240
```

Secondary login is a distinct predecessor path using:

```text
GameclientMessageSecondaryLogin
+
SecondaryLoginRSAEncryptedBlock
```

Predecessor static result:

```text
PASSWORD_REQUIRED_FOR_GAME_LOGIN: UNKNOWN
```

That UNKNOWN is not by itself a blocker for this task.

## 7. Predecessor promotion rule

Do not redo broad static RE merely because a useful predecessor remains a Draft PR. However, do not use a predecessor claim as a load-bearing runtime fact until the actual task proves:

```text
PREDECESSOR CLAIM
  -> exact-SHA revalidation
  -> current binary provenance
  -> runtime address/type/object validation as applicable
  -> observed causal effect
```

Record source status as one of:

```text
canonical_main
predecessor_revalidated
runtime_proven
```

Never label a Draft-PR statement `FACT` solely because it appears in this prompt.

## 8. Runtime ownership and serialization

Never inherit runtime authority from a historical PR/task.

In particular:

- #498 and #499 do not grant runtime authority;
- #475 does not automatically grant another task permission to consume its runtime;
- a historical PID/XID/display/session does not grant authority;
- an old login budget does not grant authority.

If PR #475 or another task currently owns the serialized physical Track A runtime:

```text
DO NOT PREEMPT
DO NOT TAKE OVER
DO NOT ATTACH
DO NOT INJECT
DO NOT SEND INPUT
DO NOT CREATE A PARALLEL LOGGED-IN SESSION
```

unless current governance provides a legal handoff/release/new admission/new isolated namespace and any required owner authorization.

If live execution is temporarily blocked by ownership, complete all safe static/bridge preparation, persist a runtime-ready checkpoint, and begin live execution only after legal admission.

Never solve ownership by restarting another task's client, killing its process, changing its display/XID/window, broad `pkill`, broad cleanup or stealing its namespace.

## 9. Runtime identity immutability

Within one admitted live attempt, keep PID, process start ticks, exact ELF identity, runtime namespace, display identity and applicable window ownership bound to the same attempt.

Do not restart the client merely to obtain an easier PID/object layout/address. A restart is a new attempt and requires any admission/revalidation triggered by current governance.

## 10. Native-first architecture

Forbidden as the login/selection control plane:

- OCR;
- image matching;
- coordinate-based field discovery;
- blind Tab navigation;
- blind keyboard/mouse automation;
- coordinate login-button clicks;
- character-row double-click automation.

Preferred mechanisms:

- repository-owned native bridge;
- existing QObject/QMeta invocation;
- known object instance plus proven native method;
- existing signal/slot/state-machine transition;
- minimal task-owned in-process helper only when current governance permits it.

A screenshot may be only optional post-success evidence. OCR never proves completion.

## 11. Login-form rule

The visual login form may exist, but do not locate or operate email/password/login controls visually.

If initial auth requires credentials, invoke native credential-auth logic below UI, such as a revalidated `TGameClient::onRequestLoginWithCredentials(QString, QString)`, or a semantically equivalent proven native entry.

## 12. Credential and secret safety

Legal user credentials may be used only for normal authentication in the user's own official client.

Never place credentials or authentication material in:

- Git;
- PR body/task/evidence text;
- CI logs, stdout/stderr or workflow annotations;
- shell trace / `set -x`;
- argv/process command line;
- environment variables;
- GDB `-ex`, GDB history or GDB command files;
- plaintext temporary files;
- screenshots/XWD artifacts;
- core/gcore/process-memory dump artifacts;
- packet or protobuf evidence containing secret material.

Never persist password, 2FA value, session key, cookie, access/refresh token, login token, RSA plaintext block or secret-bearing payload.

## 13. Secret-ingress architecture

Prefer a minimal protected transient boundary such as:

```text
protected FIFO
protected inherited FD
memfd
equivalent non-persistent secure IPC
```

Target flow:

```text
protected secret source
  -> minimal transient bridge
  -> construct required QString/native input
  -> native credential method
  -> immediate bridge-owned secret cleanup where technically safe
```

The bridge must not print native credential arguments.

Evidence may record only categories such as:

```text
credential_supplied=yes|no
native_entry_invoked=yes|no
auth_result_category=<sanitized>
state_transition=<sanitized>
```

## 14. Secret-phase observability

If broad heap/string/object discovery is needed, perform it before secret ingress whenever possible.

After credential handoff:

- do not broad-dump process memory;
- do not persist arbitrary heap regions;
- do not serialize auth/login objects;
- observe secret-free control/state events only;
- use targeted breakpoint/event hooks at safe boundaries;
- never persist argument values that may contain auth material.

## 15. 2FA, device confirmation and CAPTCHA

Do not bypass legitimate 2FA, device confirmation, CAPTCHA or equivalent authentication challenge.

If a legal native semantic entry exists for an additional required secret, use the same protected ingress model.

If a genuinely manual action is required and no legal native path exists, record:

```text
EXTERNAL_ACTION_REQUIRED
```

Do all safe work possible before that point and do not mark the task DONE.

## 16. No auth bypass

Forbidden:

- fake auth success;
- server-response spoofing;
- TLS/certificate-validation weakening;
- RSA/auth bypass;
- invalid-auth acceptance patching;
- 2FA bypass;
- fabricated session tokens;
- guessed manual fabrication of login protocol messages when native client logic exists.

## 17. Native bridge preference

Before adding a bridge, search existing repository instrumentation/helpers/catalogue/open PRs.

Preference order:

```text
1. existing repository-owned semantic/native bridge
2. existing QObject/QMeta route
3. task-owned in-process helper if current governance permits
4. controlled function invocation on a proven object
5. debugger-mediated direct call only as a last resort
```

Do not create a general arbitrary-code-execution RPC. Expose only the minimal operations needed by this task.

Candidate direct-control surface:

```text
AUTH_WITH_CREDENTIALS
RESUME_EXISTING_SESSION
SKIP_TO_CHARACTER_SELECTION
GET_CHARACTER_LIST
SELECT_CHARACTER
LOGIN_SELECTED_CHARACTER
```

Only add challenge/reconnect/logout operations if the actual successful/recovery path needs them.

## 18. Direct control versus observation

Do not directly invoke every object appearing in the causal graph.

Separate:

```text
MUST_CONTROL
MUST_OBSERVE
```

`TGameClient`, `TAuthenticationProcessController` and `TCharacterSelectionController` may require direct invocation. `TLoginProtocolMessageHandler`, `TAuthenticationAndEncryptionInfo` and `TProtocolMessageQueue` may need only causal/type observation if native client logic handles them itself.

## 19. Static address is not runtime address

Predecessor addresses such as:

```text
0xcfadcb
0xd06660
0x6ef1d0
0xd47300
0xcfb2e7
0xcfb122
0xe1abe0
0xdf6be2
0xbd36a0
```

must not be called directly merely because static RE found them.

For every direct invocation prove:

```yaml
exact_client_sha: <exact fence>
static_va: <value>
rva: <value>
elf_type: <value>
mapped_module: <current mapping>
mapping_identity: <proven>
runtime_load_bias: <value>
runtime_callable_va: <value>
instruction_bytes_match: yes
```

If the executable is PIE/ET_DYN, derive the runtime address from the current mapping/load bias.

## 20. ABI proof

For every native C++ invocation establish:

- exact C++ signature;
- SysV AMD64 calling convention;
- relevant Itanium C++ ABI rules;
- `this` placement;
- argument placement;
- return convention;
- hidden sret parameter if applicable;
- reference/value semantics;
- non-trivial constructor/copy/move/destructor requirements;
- exception behavior relevant to safe invocation;
- Qt ABI considerations where applicable.

Treat `QString`, `TCharacter`, `TCharacterList`, `TWorldList` and `TPlaySessionData` as non-trivial until proven otherwise. Do not raw-`memcpy` C++ objects without trivially-copyable proof.

## 21. Qt thread-affinity hard gate

Correct address, `this` and signature are insufficient.

For QObject/controller calls establish:

- owning `QThread`;
- current calling thread;
- event-loop availability;
- thread affinity;
- required connection/invocation semantics.

Prefer an existing signal/slot, QMeta route, queued invocation or a bridge scheduled onto the object's owning Qt event-loop thread.

Do not issue a debugger direct call from an arbitrary stopped thread unless thread safety/reentrancy of that exact method is independently proven.

## 22. Runtime object provenance

Never guess `this` pointers.

For each directly used runtime object record as applicable:

```yaml
object_address: <value>
dynamic_type: <value>
rtti_or_vtable_proof: <evidence>
owner: <value>
lifetime_proof: <evidence>
construction_provenance: <evidence>
current_state: <value>
owning_thread: <value>
related_parent_object: <value>
```

Do not accept a candidate merely because it is aligned, contains expected strings, is near another object or has plausible field values.

Before each important invocation revalidate that the object still exists, has the expected dynamic type, belongs to the same admitted process/session and remains in the required state-machine phase.

## 23. Target character must be semantic

Never log in an arbitrary or first character.

Resolve the target from current task configuration/current owner instruction/persisted non-secret task target. If and only if the native character list contains exactly one character, that unique native object may be used without another selector.

Preferred selector:

```yaml
TARGET_CHARACTER_NAME: <non-secret>
TARGET_WORLD_NAME: <non-secret or optional only if globally unique>
```

Resolve against native `TCharacter`/world objects, never row order, OCR or screen position.

Require:

```text
NATIVE_CHARACTER_MATCH_COUNT=1
```

Zero or multiple semantic matches fail closed before character-login invocation.

## 24. Phase 0 — claim/governance/task

1. verify live `main`;
2. inspect current task/PR inventory;
3. inspect current runtime owner and admission;
4. inspect #475/#498/#499 live state;
5. inspect current promotion authority;
6. perform Track A admission before any runtime-related operation;
7. create or resume exactly one correct task/branch/PR under governance;
8. declare ownership and non-overlap;
9. do not manually mutate shared indexes unless specifically authorized.

Suggested task ID if no current task already exists:

```text
OTC-20260817-track-a-native-login-to-ingame
```

Suggested branch:

```text
runtime/OTC-20260817-track-a-native-login-to-ingame
```

Do not create a duplicate if one already exists.

## 25. Phase 1 — recover minimal native invocation bridge

Find the safest current method for invoking native client logic in its own process. Investigate existing bridge/instrumentation, QMeta routes, RTTI/QObject graph, known signal/slot edges and only then a minimal task-owned helper or controlled debugger invocation.

Required result before login control:

```text
NATIVE_BRIDGE_READY=PROVEN
```

Document process identity, module identity, execution-thread model, supported operations, secret handling, failure behavior and cleanup.

## 26. Phase 2 — runtime address rebasing

For every required direct call prove:

```text
static exact-SHA location
  -> current runtime module mapping
  -> load bias
  -> runtime VA
  -> instruction-byte verification
```

No direct native call before:

```text
RUNTIME_ADDRESS_PROVEN=YES
```

## 27. Phase 3 — object provenance

For required direct control establish at minimum:

```text
GAMECLIENT_OBJECT=PROVEN
AUTH_CONTROLLER_OBJECT=PROVEN
CHARACTER_CONTROLLER_OBJECT=PROVEN
```

plus dynamic type, lifetime, thread affinity and state-machine precondition for each actual call.

Recover additional objects only when the active path requires them.

## 28. Phase 4 — retained session first

Before credential ingress, determine whether a legal retained native auth/session state can be reused.

Revalidate predecessor candidates:

```text
TAuthenticationProcessController::advanceStateMachineDirectlyToCharacterSelection()
TGameClient::connectClientToGameserverWithExistingCredentials()
```

including address, runtime object, ABI, state and thread affinity.

If retained state is valid:

```text
INITIAL_AUTH=NOT_NEEDED_SESSION_REUSED
```

and do not request a password.

## 29. Phase 5 — initial auth below UI

If retained state is absent/stale/invalid, use the native credential path below the form.

Preferred predecessor candidate after revalidation:

```text
TGameClient::onRequestLoginWithCredentials(QString, QString)
```

Prove the causal path to the native login-success receiver and resulting `TCharacterList`, `TWorldList` and `TPlaySessionData`/equivalent retained state.

Do not stop at auth success.

Sanitized auth result categories only:

```text
SUCCESS
INVALID_CREDENTIALS
2FA_REQUIRED
DEVICE_CONFIRMATION_REQUIRED
RATE_LIMITED
NETWORK_ERROR
SERVER_REJECTION
SESSION_INVALID
UNKNOWN
```

## 30. Phase 6 — character list without OCR

Read the list from a native model/object such as retained login-success data, character-selection controller/model or equivalent native Qt object graph.

For the selected target prove:

```text
NATIVE_CHARACTER_OBJECT=PROVEN
CHARACTER_IDENTITY=PROVEN
WORLD_IDENTITY=PROVEN
```

and that the object belongs to the current session and remains alive.

## 31. Phase 7 — native character selection

After full revalidation, prefer:

```text
TCharacterSelectionController::requestCharacterLogin(TCharacter)
```

predecessor static candidate `0xd47300`.

Before invoking prove runtime VA, correct `this`, correct live `TCharacter`, ABI, Qt thread and state-machine state.

Do not double-click or otherwise automate the visual character list.

## 32. Phase 8 — complete native game-login chain

Observe the causal path:

```text
requestCharacterLogin
  -> requestCharacterGameserverLogin
  -> onStartGameServerLoginStateEntered
  -> TLoginProtocolMessageHandler
  -> GameclientMessageLogin
  -> LoginRSAEncryptedBlock
  -> TProtocolMessageQueue
  -> network transport
  -> server response
```

Let the original client construct the login/secondary-login/challenge messages whenever it has native logic to do so.

Do not manually reconstruct `LoginRSAEncryptedBlock`, `GameclientMessageLogin`, challenge response or secondary login merely to understand every field.

`PASSWORD_REQUIRED_FOR_GAME_LOGIN=UNKNOWN` remains acceptable if native retained state completes the real path without needing that static semantic question resolved first.

## 33. Secondary login/challenge/reconnect

If the legitimate native state machine enters secondary login, challenge or reconnect:

- observe the transition;
- let existing client logic handle it;
- recover another semantic entry only if the current native state machine actually requires it.

Do not broaden into unrelated protocol RE.

## 34. Server-login proof is not final proof

For:

```text
SERVER_LOGIN_SUCCESS=PROVEN
```

require more than a TCP connect: prove the game-login request was causally sent, server acceptance occurred/no immediate auth rejection occurred, and the client advanced past the login handshake.

Even then continue to active gameplay proof.

## 35. Secret-free causal event trace

Maintain a causal trace bound to the same PID/process-start/runtime attempt using monotonic timestamps or ordered sequence identifiers.

Example:

```text
E01 native_auth_entry
E02 login_success_native
E03 character_model_ready
E04 target_character_resolved
E05 native_character_login_invoked
E06 gameserver_login_state_entered
E07 login_message_dispatched
E08 server_login_accepted
E09 gameplay_state_active
E10 local_player_active
E11 world/map/gameplay_initialized
```

Do not persist secret payloads or secret-bearing argument values.

## 36. Phase 9 — actual in-game proof

This is the completion gate.

Require cross-layer evidence, not a screenshot.

### Signal A — gameplay state

Prove a native session/game state corresponding to active gameplay:

```text
GAMEPLAY_STATE_ACTIVE=PROVEN
```

### Signal B — local player

Prove a type/provenance-correct active local-player object for the current session:

```text
LOCAL_PLAYER_ACTIVE=PROVEN
```

Minimum evidence includes valid lifetime/current-session association and current player position or equivalent live gameplay-only state.

### Signal C — downstream gameplay

Also prove at least one independent downstream gameplay signal, for example:

- normal post-login gameplay message stream;
- map/world objects initialized;
- map-description/world data actively processed;
- another gameplay-only subsystem causally initialized after login.

## 37. Character/world identity match

Prove the active gameplay character/world equals the semantically selected native target:

```text
CHARACTER_IDENTITY_MATCH=PROVEN
WORLD_IDENTITY_MATCH=PROVEN
```

Do not accept “some character logged in.”

## 38. False in-game proofs are forbidden

Do not promote `IN_GAME` from only:

- login-success callback;
- TCP/TLS connection;
- character-selection screen disappearing;
- one protobuf message;
- a pre-created player-like object;
- a visual screen transition;
- map-like pixels;
- screenshot/OCR.

## 39. Optional visual evidence

Only after structural/semantic `IN_GAME=PROVEN`, and only when current runtime/task authority permits, one screenshot may be recorded as additional evidence from the same admitted runtime. It must not show credentials/auth secrets and must never replace semantic proof.

## 40. Avoid unnecessary gameplay stimulus

Do not move the character merely to demonstrate that gameplay works when local-player state, gameplay state and downstream message/map initialization already provide sufficient proof.

If reversible movement is genuinely required as a discriminator, it must be separately compatible with current task authority and remain minimal.

## 41. Failure handling — first causal failure

Classify the first causal failure, for example:

```text
wrong_static_address
wrong_runtime_rebase
wrong_module_mapping
wrong_object_instance
stale_object
wrong_dynamic_type
wrong_signature
wrong_calling_convention
wrong_nontrivial_argument_construction
wrong_thread_affinity
wrong_state_machine_precondition
invalid_retained_session
initial_auth_required
2fa_required
device_confirmation_required
wrong_character_object
ambiguous_target_character
game_challenge_required
transport_failure
server_rejection
rate_limit
runtime_ownership_block
runtime_admission_block
instrumentation_interference
unknown
```

Then use:

```text
failure
  -> minimal discriminator
  -> new evidence
  -> bounded repair
  -> retry only if current governance/budget permits
```

Do not replace a specific failure with a broad rewrite/random retry/restart.

If a native call crashes, re-prove runtime VA, object, ABI, thread and state before retrying.

## 42. Anti-stall execution progression

For every candidate method:

```text
candidate
  -> exact-SHA revalidation
  -> runtime rebase
  -> instance proof
  -> ABI proof
  -> thread proof
  -> state/precondition proof
  -> invoke
  -> state-transition proof
```

If character selection works, continue to game login. If game login works, continue to gameplay. If login-success works, continue to local-player/gameplay proof.

Never terminate on “promising lead”, “likely” or “seems to work”.

## 43. Live-auth retry discipline

“Autonomous until success” is not authority for unlimited real credential submissions.

Every credential submission must be allowed by current runtime authority, serialized, within current login budget/rate constraints, and driven by a materially new hypothesis after failure.

Never create parallel logged-in sessions without explicit current authorization.

## 44. Runtime/client modification boundary

Prefer observation and native invocation without persistent client patching.

If a bridge/instrumentation helper requires in-process injection or another invasive mechanism, current governance must authorize it. Keep it minimal, do not alter authentication semantics, server-validation semantics or gameplay-state truth, and do not confuse temporary instrumentation with a product client change.

## 45. Proprietary-client safety

Do not commit/upload the raw official client binary, secret-bearing memory/packet captures or other prohibited proprietary artifacts. Use the repository's current exact-client evidence rules and bounded artifact pipeline.

## 46. AI/Spark authority

Follow current root `AGENTS.md`.

A current standing authorization for the central controller to perform advisory Spark pre-review is not permission for this worker to invoke Codex/OpenAI API/hosted Code Review/fallback models or owner-funded AI credentials directly unless current owner authorization and governance explicitly allow that use.

Silence from Spark is not a PASS.

## 47. Evidence model

Use:

```text
FACT
INFERENCE
UNKNOWN
CONFLICT
```

`FACT` requires direct evidence. `INFERENCE` must cite supporting FACTs. Do not silently turn `UNKNOWN` into an assumption.

Every load-bearing promotion should record, where applicable:

```yaml
exact_client_sha: <value>
source_status: <canonical_main|predecessor_revalidated|runtime_proven>
static_address_or_rva: <value>
runtime_address: <value>
owner_or_type: <value>
runtime_object_provenance: <evidence>
abi: <evidence>
owning_thread: <evidence>
precondition: <value>
state_machine_precondition: <value>
observed_call: <evidence>
observed_postcondition: <evidence>
pid_start_identity: <value>
session_identity: <value>
run_or_job_evidence: <value>
secret_safety_marker: <value>
```

## 48. Durable outputs

Primary report:

```text
docs/research/native-client/NATIVE_LOGIN_TO_INGAME_CONTROL.md
```

Task-owned evidence should live under a task-specific evidence directory, for example:

```text
docs/agents/evidence/OTC-20260817-track-a-native-login-to-ingame/
```

Suggested evidence phases:

```text
phase0-live-state-admission.md
phase1-native-invocation-bridge.md
phase2-runtime-address-object-abi-proof.md
phase3-auth-session-transition.md
phase4-native-character-model.md
phase5-native-game-login-chain.md
phase6-in-game-causal-proof.md
final-result.json
```

Use fewer files if a smaller evidence set is clearer and equally durable.

## 49. Final semantic control graph

The report must show the final graph:

```text
agent
  -> native bridge
  -> native auth/session control
  -> native character model
  -> native target resolution
  -> native character selection
  -> native gameserver-login state
  -> native LoginRSAEncryptedBlock/GameclientMessageLogin production
  -> native protocol queue
  -> server acceptance
  -> gameplay state active
  -> local player active
  -> world/map/gameplay active
```

Mark every load-bearing edge `PROVEN` or `UNKNOWN`. SUCCESS requires all load-bearing edges `PROVEN`.

## 50. Completion inventory

SUCCESS only when all applicable fields below are proven:

```yaml
CLIENT:
  EXACT_SHA: PROVEN
  SAME_ADMITTED_RUNTIME_CHAIN: PROVEN

CONTROL:
  NATIVE_UI_BYPASS_USED: YES
  LOGIN_FORM_OCR_USED: NO
  BLIND_COORDINATE_CLICKING_USED: NO
  IMAGE_MATCHING_LOGIN_AUTOMATION_USED: NO
  GUI_CREDENTIAL_ENTRY_USED: NO

INITIAL_AUTH:
  NATIVE_PATH_USED: YES | NOT_NEEDED_SESSION_REUSED
  AUTH_RESULT: PROVEN

CHARACTER_SELECTION:
  NATIVE_CHARACTER_OBJECT: PROVEN
  CHARACTER_IDENTITY: PROVEN
  WORLD_IDENTITY: PROVEN
  TARGET_MATCH_COUNT: 1
  NATIVE_SELECTION_CALL: PROVEN

GAME_LOGIN:
  REQUEST_CHARACTER_LOGIN: PROVEN
  REQUEST_GAMESERVER_LOGIN: PROVEN
  GAMELOGIN_STATE_ENTERED: PROVEN
  NATIVE_LOGIN_MESSAGE_CHAIN: PROVEN
  SERVER_LOGIN_SUCCESS: PROVEN

IN_GAME:
  GAMEPLAY_STATE_ACTIVE: PROVEN
  LOCAL_PLAYER_ACTIVE: PROVEN
  LOCAL_PLAYER_POSITION_OR_EQUIVALENT_STATE: PROVEN
  DOWNSTREAM_GAMEPLAY_ACTIVITY: PROVEN
  CHARACTER_IDENTITY_MATCH: PROVEN
  WORLD_IDENTITY_MATCH: PROVEN
  CAUSAL_NATIVE_LOGIN_TO_INGAME_CHAIN: PROVEN

SAFETY:
  PASSWORD_LOGGED: NO
  SESSION_SECRET_PERSISTED: NO
  AUTH_BYPASS_USED: NO
  TLS_WEAKENED: NO
  SERVER_RESPONSE_SPOOFED: NO
  PARALLEL_UNAUTHORIZED_SESSION: NO

RESULT: SUCCESS
CHARACTER_ACTUALLY_LOGGED_INTO_GAME: YES
CAUSAL_PROOF: COMPLETE
```

## 51. Fresh falsification/audit

After coherent runtime success, use a fresh independent validator to try to falsify at least:

- object provenance;
- static-vs-runtime address mapping;
- ABI/calling convention;
- Qt thread correctness;
- retained-session assumptions;
- target-character identity;
- false login-success completion;
- false local-player identification;
- screenshot/visual-only gameplay inference;
- secret leakage;
- runtime ownership/admission compliance.

A worker summary is not terminal evidence. Material findings must be repaired or the task is not DONE.

## 52. Exact-head validation and closeout

Before repository closeout:

- inspect full changed-file inventory/diff;
- run required exact-head checks/CI;
- inspect review threads and related PR inventory;
- honor current Track A promotion authority;
- remove temporary workflows/helpers if they are not part of the durable result;
- do not self-promote researcher evidence when governance assigns promotion to a coordinator;
- archive/terminally close the task only after current closeout gates pass;
- release runtime ownership, lease, namespace, worktree/advisory ownership safely;
- ensure no secrets or temporary client artifacts remain.

Every related PR must have an intentional lifecycle state: merged, accurately closed as superseded/obsolete/historical, or intentionally open with an explicit blocker.

## 53. External action required

A genuine manual requirement such as manual 2FA/device confirmation/CAPTCHA, unavailable protected credential delivery or an explicit owner decision may produce:

```text
EXTERNAL_ACTION_REQUIRED: <exact action>
```

Do everything safe before that point, persist the checkpoint, do not mark DONE, and resume from durable state once the blocker is removed.

## 54. Real stop conditions

Task-success stop:

```text
RESULT: SUCCESS
CHARACTER_ACTUALLY_LOGGED_INTO_GAME: YES
CAUSAL_PROOF: COMPLETE
```

Legal worker stops without task success are only current-governance/safety/budget outcomes such as:

```text
BLOCKED
WAITING
ROTATE
EXTERNAL_ACTION_REQUIRED
```

Do not stop merely because a function was discovered, bridge built, auth succeeded, character list obtained, character login requested, login packet sent or server accepted login.

## 55. Final response contract

At a terminal worker result report:

```text
STATUS: DONE | BLOCKED | WAITING | ROTATE

TASK:
OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME

EXACT_CLIENT:
version=15.32.df7b29
sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe

RESULT:
SUCCESS | INCOMPLETE

CHARACTER_ACTUALLY_LOGGED_INTO_GAME:
YES | NO

NATIVE_UI_BYPASS_USED:
YES | NO

INITIAL_AUTH:
NATIVE_PATH_USED | SESSION_REUSED | NOT_REACHED

CHARACTER_SELECTION:
NATIVE_CHARACTER_OBJECT=<PROVEN|NOT_PROVEN>
NATIVE_SELECTION_CALL=<PROVEN|NOT_PROVEN>
CHARACTER_IDENTITY_MATCH=<PROVEN|NOT_PROVEN>

GAME_LOGIN:
NATIVE_GAMELOGIN_CHAIN=<PROVEN|NOT_PROVEN>
SERVER_LOGIN_SUCCESS=<PROVEN|NOT_PROVEN>

IN_GAME:
GAMEPLAY_STATE_ACTIVE=<PROVEN|NOT_PROVEN>
LOCAL_PLAYER_ACTIVE=<PROVEN|NOT_PROVEN>
DOWNSTREAM_GAMEPLAY_ACTIVITY=<PROVEN|NOT_PROVEN>
CAUSAL_NATIVE_LOGIN_TO_INGAME_CHAIN=<PROVEN|NOT_PROVEN>

SAFETY:
LOGIN_FORM_OCR_USED=NO
BLIND_COORDINATE_CLICKING_USED=NO
GUI_CREDENTIAL_ENTRY_USED=NO
PASSWORD_LOGGED=NO
SESSION_SECRET_PERSISTED=NO
AUTH_BYPASS_USED=NO
UNAUTHORIZED_PARALLEL_SESSION=NO

EVIDENCE:
<task path>
<report path>
<evidence path>
<PR>
<exact head>
<runtime/run identifiers>

AUDIT:
<PASS | FAIL | NOT_REACHED>

VALIDATION:
<exact-head results>

BLOCKER:
<none or exact blocker>

NEXT_ACTION:
<none when SUCCESS, otherwise exactly one concrete next action>
```

## 56. Final invariant

```text
DO NOT AUTOMATE THE LOGIN UI.
CONTROL THE ORIGINAL CLIENT SEMANTICALLY.
DO NOT REIMPLEMENT AUTH WHEN THE CLIENT CAN DO IT.
DO NOT GUESS OBJECTS, ADDRESSES, ABI OR THREADS.
DO NOT PERSIST SECRETS.
DO NOT STEAL ANOTHER TASK'S RUNTIME.
DO NOT CALL LOGIN SUCCESS "IN GAME".
FOLLOW THE SAME EXACT CHARACTER FROM NATIVE CHARACTER OBJECT THROUGH GAME LOGIN TO ACTIVE LOCAL PLAYER.
CALL THE TASK COMPLETE ONLY WHEN THE CHARACTER IS ACTUALLY IN THE GAME.
```
