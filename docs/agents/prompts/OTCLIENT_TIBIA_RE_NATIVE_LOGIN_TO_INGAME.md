# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME

```yaml
prompt_contract:
  version: 3.0.0
  prompting_standard_version: 2.1
  alias: OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME
  track_id: official-client-re
  lane: RUNTIME
  task_kind: runtime_reverse_engineering_semantic_control
  risk: critical
  platform: official_native_linux_only
  run_scope: single_task
  continuation_policy: continue_within_task_until_success_or_real_stop
  task_completion_policy: finalize_archive_and_stop
  user_communication: terminal_only
  objective: Drive the exact official Linux Tibia client through legal native authentication/session state, native character selection and the original game-server state machine until the selected character is causally proven in active gameplay, without operating the login form.
  baseline_prompt: v2.0.0 merged by PR #501
  current_main_refresh_inputs:
    - PR #505 native cold-auth QMeta contract
    - PR #507 experimental form-less native-auth bridge
    - PR #510 protected TTY native-auth secret source
    - PR #475 owner-requested runtime release handoff
  rollback: revert the v3 prompt-refresh PR to v2.0.0
```

Run autonomously in:

```text
blakinio/otclient
```

This prompt defines one critical Track A physical E2E task. Repository governance on the current trusted `main`, live task/PR state, current Track A admission and direct environment evidence always override stale chat history, historical PR prose, historical PID/XID/session data and old task checkpoints.

## 1. Only objective and only success gate

Bring the exact official native Linux Tibia client to:

```text
CHARACTER ACTUALLY LOGGED INTO GAME
```

using the original client's native logic below the login-form/UI layer.

Task success exists only when all of the following are true in one causally bound admitted runtime:

```text
RESULT: SUCCESS
CHARACTER_ACTUALLY_LOGGED_INTO_GAME: YES
CAUSAL_PROOF: COMPLETE
```

Authentication success, `TPlaySessionData`, character list availability, character confirmation, `requestCharacterGameserverLogin`, TCP/TLS connection, a login-success packet or disappearance of character selection are intermediate states and are never completion by themselves.

## 2. Exact client hard fence

Work only on:

```yaml
version: 15.32.df7b29
platform: official_native_linux_only
unpacked_size: 51965216
unpacked_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed_client_lzma_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
```

A different version, size, SHA, platform, unverifiable process identity or contradictory mapping evidence fails closed. Revalidate load bias, instruction fences, live object provenance and thread ownership on every fresh physical runtime.

## 3. Absolute login-form/UI prohibition

The login form may be visible, but it is not a control plane.

Do not use any of these for account login or character selection:

```text
OCR / Tesseract
image matching
visual textbox detection
coordinate field discovery
coordinate login-button click
Tab/Return login submission
blind keyboard or mouse automation
clipboard typing into the client
character-row coordinate click/double-click
screen pixels as semantic state control
```

Do not revive historical #475 GUI cold-auth machinery as a fallback merely because it once authenticated successfully.

Screenshots may be used only after structural `IN_GAME` is already proven and only when current task authority allows a sanitized map/gameplay-only capture. A screenshot never proves login or `IN_GAME` by itself.

## 4. Current-main canonical native-auth stack

Do not rediscover or rebuild a generic native-auth bridge before consuming current `main`.

### 4.1 PR #505 — exact cold-auth QMeta contract

PR #505 merged as:

```text
17cc0dc1bf29c440cc08e443bdce98e4dde7be5d
```

Current-main exact-SHA static facts:

```text
class: tibia::client::TGameClient
method_count: 44
signal_count: 6
qt_static_metacall: 0xd06260
method: onRequestLoginWithCredentials
InvokeMetaMethod id / metadata index: 17
signature: void onRequestLoginWithCredentials(QString, QString)
method flags: 0x8
raw type ids: 0x2b,0x0a,0x0a
full-range dispatch LEA: 0xd0626a
dispatch table: 0x1d6dea0
method-17 static target: 0xd06850
instruction fence: 488b5110488b71084883c4485b5de92d389eff0f1f440000488bbfa009000048
```

The `0xd06850` target is a build/runtime fence, not a preferred raw-call entry. When the QMeta route is available, use a proven live `TGameClient` on its owning Qt thread and Qt's named/meta invocation machinery.

Historical evidence-file headers may still contain point-in-time words such as `DRAFT`; live merge state on `main` controls promotion status.

### 4.2 PR #507 — experimental form-less auth bridge

PR #507 merged as:

```text
2e6992da330e8a52d03b94b8d6a9de6fa79a6800
```

It provides the narrow experimental native-auth path:

```text
sealed anonymous memfd
 -> exact PeerIdentityExpectation
 -> Unix SCM_RIGHTS descriptor transfer
 -> one-shot mode-0600 experimental auth socket
 -> exact client / PIE / instruction-fence checks
 -> unique live TGameClient
 -> owning Qt event-loop thread
 -> QMeta named invocation of onRequestLoginWithCredentials(QString,QString)
 -> original authentication state machine
```

`OTCLIENT_TIBIA_RE_BUILD_EXPERIMENTAL_AUTH` is opt-in and defaults `OFF`.

The stable read-only bridge surfaces are deliberately not the mutating auth API. Do not broaden them into a general arbitrary-method or raw-address RPC.

Do not treat `invocation_dispatched=true` as authentication success; it proves only that the original native invocation was dispatched.

### 4.3 PR #510 — protected root credential source

PR #510 merged as:

```text
13c5939ef89900a0998d56d2bf625c3906c9a68e
```

The promoted root secret-ingress path is:

```text
controlling Linux /dev/tty
 -> ECHO/ECHONL disabled
 -> required-mlock mutable account/password buffers
 -> RLIMIT_CORE=0
 -> PR_SET_DUMPABLE=0
 -> anonymous MFD_ALLOW_SEALING memfd
 -> F_SEAL_SEAL|F_SEAL_SHRINK|F_SEAL_GROW|F_SEAL_WRITE
 -> experimental_auth_client.auth_with_credentials_fd()
 -> SCM_RIGHTS
 -> one-shot native-auth helper
```

The runtime identity file is non-secret but must remain fail-closed: absolute path, `O_NOFOLLOW|O_CLOEXEC`, single-FD `fstat` binding, current effective-UID ownership, no group/world write, bounded JSON and exact client version/size/SHA.

If the merged #510 task record is still under `docs/agents/tasks/active/`, close its repository lifecycle according to current governance. A stale active documentation/implementation task record is not physical runtime ownership.

## 5. Secret rules are hard gates

Legal user credentials may be used only for normal authentication in the user's own official client.

Never put Tibia credentials, 2FA values, session/auth secrets, cookies, login tokens, RSA plaintext, access/refresh tokens or secret-bearing payloads in:

```text
Git or PR/task/evidence prose
GitHub Actions environment variables
process environment
argv / command line
stdout/stderr / workflow annotations
shell trace / set -x
plaintext temporary files
GDB -ex / GDB history / GDB command files
screenshots or XWD artifacts
core/gcore dumps
packet/protobuf evidence
AI model context
```

Do not ask the owner to paste a password or 2FA value into chat.

Do not fall back from the protected source to `TIBIA_TEST_EMAIL` / `TIBIA_TEST_PASSWORD` environment ingress merely because a GitHub Actions runner has no controlling TTY.

If the admitted physical environment has no legal controlling TTY and no already repository-approved protected local secret broker/source, stop at:

```text
EXTERNAL_ACTION_REQUIRED
```

or `BLOCKED`, persist the exact missing ingress capability and one concrete next action. Do not solve that blocker by operating the GUI or inventing a weaker secret path inside the same authority.

## 6. Legitimate challenges only

Preserve the original client authentication state machine.

Never bypass or fabricate:

```text
2FA
CAPTCHA
device confirmation
auth success
session success
server login success
TLS/certificate validation
RSA/auth validation
login/session tokens
server responses
```

If a legitimate additional challenge requires an external action and no current legal native semantic entry exists, checkpoint `EXTERNAL_ACTION_REQUIRED` after completing all safe work.

## 7. PR #475 is released, but its old authority is not inherited

Current released #475 head:

```text
8bf26dde309c46f08be414c4d2aef3e3599d7f5a
```

Durable release state records:

```text
status=waiting
agent=null
session_id=null
session_role=released
runtime_access=none
runtime_owner_task=null
credentials_allowed=false
login_allowed=false
gameplay_allowed=false
mutation_authorized=false
owned_paths=[]
```

Owner-requested release cleanup records:

```text
EXACT_TASK_MARKER_PROCESSES_AFTER=0
VNC_OBSERVER_STATE_REMOVED=true
TASK_BASELINE_NAMESPACE_REMOVED=true
TASK_PATCHED_NAMESPACE_REMOVED=true
ORIGINAL_SOURCE_REHASH=PASS
CREDENTIALS_USED=false
LOGIN_PERFORMED=false
GAMEPLAY_PERFORMED=false
```

Therefore the prior worker is not a continuing runtime owner. However, this does not grant a successor any old login/session/credential/lease authority.

Before any new physical execution, perform a fresh no-client inventory and a fresh current Track A admission. If a different live owner or runtime appears, fail closed and do not preempt it.

Never solve ownership with broad cleanup, `pkill`, process stealing, display/XID mutation, attaching to another task, or creating a parallel logged-in session.

## 8. Historical physical chain that should not be rediscovered through UI

The #475 release handoff preserves exact-client physical evidence for the upstream chain:

```text
LEGITIMATE_ACCOUNT_LOGIN=PASS
POST_LOGIN_TRANSPORT_ACTIVITY=PASS
POST_LOGIN_UI_TRANSITION=PASS
POSTAUTH_CHARACTER_CONTROLLER_PROVENANCE=PASS
NATIVE_CHARACTER_LIST_COUNT=1
NATIVE_SELECTION_INDEX=0
QT_THREAD_AFFINITY_FOR_CHARACTER_CONFIRMATION=PASS
NATIVE_CHARACTER_CONFIRMATION_QMETA=PASS
TCHARACTERLOGINDATA_VECTOR_BEFORE=0
TCHARACTERLOGINDATA_VECTOR_AFTER=1
REQUEST_CHARACTER_LOGIN_SIGNAL=PROVEN
REQUEST_CHARACTER_GAMESERVER_LOGIN=OBSERVED
STRUCTURAL_IN_GAME=NOT_PROVEN
MAP_SCREENSHOT=NOT_PROVEN
```

Canonical historical character-confirmation discriminator:

```text
V18 run/job: 32076063134 / 95529595652
```

That run discovered exactly one current runtime character model, chose native index `0` because it was unique, invoked the live `TCharacterSelectionController` QMeta `onCharacterSelectionConfirmed` route on the correct Qt-affine object, and caused the client itself to build one `TCharacterLoginData` entry (`0 -> 1`).

V19 later observed:

```text
RequestCharacterLoginSignal=1
RequestCharacterGameserverLogin=2
StartGameServerLogin=0
FullMap=0
```

These are valuable historical facts, but a new E2E attempt still needs fresh process/session/object/thread identity and causal observation on its own admitted runtime.

## 9. Critical corrections from previous runtime work

Do not regress these corrections:

1. `Invalid Monk` or any remembered character name is not runtime-discovered evidence. Resolve the character only from the current native character model/list.
2. Do not use coordinate/pixel/Tab character selection.
3. Historical `0xd47300` must not be treated as a safe standalone `requestCharacterLogin` entry; the successful physical route was through the real live controller/QMeta character-confirmation boundary.
4. Do not guess `this` pointers or select an object from plausible data. Re-prove dynamic type/vptr/RTTI, ownership, lifetime, current session and Qt thread.
5. If debugger-mediated observation/calls are used, do not leave `scheduler-locking` in a state that prevents normal network/session progression.
6. Distinguish QMeta case/thunk addresses from real implementations before using breakpoints or causal counters.

Historical observation mappings from the exact client may guide a fresh discriminator but are not direct-call authority until runtime-revalidated:

```text
StartGameServerLogin implementation ~0x767440
connectClientToGameserverWithExistingCredentials implementation = 0x6ef1d0
onConnectClientToGameserver implementation ~0x6fe480
session-connected implementation ~0x6ee130
```

Do not directly invoke or fabricate `SessionConnected`, `LoginSuccessful`, auth/session payloads, character payloads, challenge responses, packets or success callbacks.

## 10. Historical v22 login budget is evidence, not authority

Historical v22 authority recorded:

```text
BASELINE_LOGIN_MAX=12
BASELINE_LOGIN_CONSUMED_BEFORE_V22=11
TWELFTH_BASELINE_LOGIN_ATTEMPT_AUTHORIZED=true
SIMULTANEOUS_LOGGED_IN_SESSIONS_MAX=1
```

The release handoff intentionally records final v22 consumption as needing re-derivation from terminal logs. Before asserting the historical final count, inspect the terminal v22 result/log evidence.

Do not inherit the v22 sequential-login budget or authorization for a new run. A new physical attempt requires fresh current task authority/admission and current one-session serialization.

## 11. Mandatory current-live-state start procedure

At every fresh owner invocation or replacement session:

1. read current `AGENTS.override.md`, root `AGENTS.md` and routed `docs/agents/**` contracts;
2. read the current authoritative task/recovery checkpoint before broad discovery;
3. verify current `main` and current prompt/alias versions;
4. inspect active Track A tasks, live PRs, review threads, CI and path ownership;
5. verify #505/#507/#510 are still in canonical `main` or consume their current superseding implementation;
6. close any required post-merge lifecycle-only task such as a still-active merged #510 task before falsely calling it terminal;
7. read #475 release handoff and cleanup evidence;
8. inspect terminal v22 evidence before claiming final historical login count;
9. perform a fresh **no-client** controller-plane inventory on `synology-otclient-01`;
10. establish current lease/registration/controller task/session/namespace and prove no conflicting live task-owned process;
11. claim/resume one correct native-login E2E task/branch/PR and persist full Track A admission;
12. only then perform any physical runtime operation.

Do not ask the owner for facts resolvable from current repository/runtime metadata.

## 12. Fresh admission before runtime mutation

Follow current `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md` and current canonical bootstrap/rebind/Gate A/Gate B contracts.

For the physical native-login task, determine from direct controller-plane evidence whether the next legal class is canonical bootstrap, canonical reuse/rebind or another current approved class.

If authoritative registration is absent, do not invent a PID/display/registration. Use the current promoted canonical bootstrap transition only when the native-login task's current owner authority and admission permit it.

Before native auth prove at least:

```text
ONE_TASK_OWNS_RUNTIME=true
SIMULTANEOUS_LOGGED_IN_SESSIONS<=1
EXACT_CLIENT_SHA=PASS
PID_START_IDENTITY=PROVEN
RUNTIME_NAMESPACE=PROVEN
DISPLAY_AND_XRES_OWNERSHIP=PROVEN
WARP/SOCKS_CONFINEMENT=PROVEN
RUNTIME_REGISTRATION_AND_GENERATION=PROVEN_AS_REQUIRED
GATE_A=PASS_AS_REQUIRED
GATE_B=PASS_AS_REQUIRED
```

Historical PID, XID, display, VNC port or registration data is not current proof.

## 13. Runtime identity and native-call hard gates

Within one admitted attempt, keep the same PID, process start ticks, ELF identity, runtime namespace, display/window ownership and applicable session identity bound to the causal chain.

For every direct or bridge-mediated native call prove as applicable:

```yaml
exact_client_sha: <exact fence>
static_va_or_qmeta_id: <value>
runtime_mapping_and_load_bias: <proof>
instruction_fence: <match>
object_address: <value>
dynamic_type_vptr_rtti: <proof>
lifetime_and_owner: <proof>
owning_qthread: <proof>
event_loop_available: true
state_machine_precondition: <proof>
abi_and_nontrivial_arguments: <proof>
```

`QString`, `TCharacter`, `TCharacterList`, `TWorldList` and `TPlaySessionData` are non-trivial C++/Qt types until the invoked QMeta/native path proves the correct construction semantics. Never raw-`memcpy` them based on layout guesses.

Prefer signals/slots, named QMeta invocation and the merged bridge over debugger-mediated direct calls.

## 14. Retained native session first

Before asking for credentials, determine whether the fresh admitted client already has legal retained native authentication/play-session state.

Useful current-main/predecessor routes include, after exact runtime revalidation:

```text
TAuthenticationProcessController::advanceStateMachineDirectlyToCharacterSelection()
TGameClient::connectClientToGameserverWithExistingCredentials()
```

If valid retained state exists, use it and record:

```text
INITIAL_AUTH=NOT_NEEDED_SESSION_REUSED
```

Do not request a password merely because the visual login form is visible.

Do not assume old #475 ephemeral HOME/session state survived its release cleanup.

## 15. Cold native auth below the form

If retained state is absent or invalid and legal protected credentials are available, use the merged form-less path:

```text
protected credential source
 -> sealed memfd
 -> SCM_RIGHTS
 -> exact peer / runtime identity
 -> unique live tibia::client::TGameClient
 -> owning Qt event-loop thread
 -> QMeta method 17 / named onRequestLoginWithCredentials(QString,QString)
 -> original client auth / 2FA / device-confirmation state machine
```

Revalidate the current exact instruction fence before dispatch. Do not raw-jump to `0xd06850` merely because the static target is known.

Sanitized auth observations may record only categories and control-state events, never argument values or secret payloads.

Continue after authentication; auth success is not task success.

## 16. Native character model and target selection

Read characters from the current native runtime model/controller/login-success state, never from screen geometry or memory assumptions.

Use only current-session `TCharacter`/world data. Selection rules:

```text
if exactly one live native character exists:
    NATIVE_CHARACTER_MATCH_COUNT=1
    use that unique current-session native character object
else:
    resolve the explicit non-secret current task target semantically by character/world identity
    require exactly one match
```

Zero or multiple semantic matches fail closed before login invocation.

Before character confirmation prove the live controller object, native character object, lifetime, current session, QMeta route and Qt thread affinity.

Prefer the physically proven controller/QMeta confirmation pattern from V18 after fresh runtime revalidation. Do not revive raw `0xd47300` or visual row activation as a control plane.

## 17. Original game-server login state machine

After native character confirmation, let the original client propagate the normal chain.

Observe causally, in order as applicable:

```text
native character confirmation
 -> client builds current TCharacterLoginData
 -> requestCharacterLogin signal/path
 -> requestCharacterGameserverLogin
 -> StartGameServerLogin
 -> connectClientToGameserverWithExistingCredentials
 -> onConnectClientToGameserver
 -> original network/session processing
 -> server acceptance
 -> inbound gameplay protocol
 -> FullMap / map-description processing
```

Use implementation/QMeta breakpoints or bridge state observation only after exact current runtime fencing.

Do not manually synthesize `GameclientMessageLogin`, `LoginRSAEncryptedBlock`, secondary-login payloads or server success when the client can build/handle them itself.

`PASSWORD_REQUIRED_FOR_GAME_LOGIN=UNKNOWN` from older static research is not a blocker if retained native state naturally completes the original game-login path.

If the natural chain stops, identify the **first causal missing transition** and design only the minimal discriminator for that transition. Do not jump several states ahead.

## 18. Structural `IN_GAME` completion gate

The same admitted runtime must prove all load-bearing layers below.

### A. Server/game-login progression

```text
REQUEST_GAMESERVER_LOGIN=PROVEN
GAMELOGIN_STATE_ENTERED=PROVEN
ORIGINAL_GAMELOGIN_CHAIN=PROVEN
SERVER_ACCEPTANCE=PROVEN
```

A socket connect alone is insufficient.

### B. Authoritative world entry

Require at minimum:

```text
FULLMAP_OBSERVED=PASS
MAP_DESCRIPTION_STRIPS>=10
```

Prefer pre-Storage/inbound structural observation so local precreated UI/map objects cannot fake the result.

### C. Gameplay state and local player

Require a current-session native gameplay state and a type/provenance-correct active local player or equivalent live gameplay-only state:

```text
GAMEPLAY_STATE_ACTIVE=PROVEN
LOCAL_PLAYER_ACTIVE=PROVEN
LOCAL_PLAYER_POSITION_OR_EQUIVALENT_STATE=PROVEN
```

### D. Identity match

The active player/world must equal the native character/world selected from the same current-session model:

```text
CHARACTER_IDENTITY_MATCH=PROVEN
WORLD_IDENTITY_MATCH=PROVEN
```

### E. Causal continuity

All evidence must remain bound to the same admitted PID/start/runtime/session chain with ordered timestamps or sequence identifiers.

Only when A-E pass may the task emit:

```text
RESULT: SUCCESS
CHARACTER_ACTUALLY_LOGGED_INTO_GAME: YES
CAUSAL_PROOF: COMPLETE
```

## 19. Do not overbuild before physical E2E

The priority after current-main native-auth promotion is physical E2E, not more generic static infrastructure.

Do not create another bridge, generic RPC, large RE task or broad static discriminator unless one concrete physical attempt identifies exactly one missing dependency that cannot be answered from current promoted evidence.

Use this progression:

```text
physical attempt
 -> first causal failure
 -> smallest discriminator
 -> new evidence
 -> one bounded repair
 -> retry only when authority/budget permit
```

Do not convert a specific failure into broad architecture work or random retries.

## 20. AI / Codex Spark boundary

Current root governance grants this exact alias/task family bounded direct use of exactly:

```text
gpt-5.3-codex-spark
```

through ChatGPT-managed Codex authentication or another repository-approved managed path.

Allowed: bounded repository/code analysis, reverse-engineering assistance, implementation assistance, falsification and review.

Never send Spark:

```text
Tibia credentials
2FA values
auth/session secrets
secret-bearing process memory or packets
raw proprietary official-client binary
```

Spark output is advisory only. It never grants runtime ownership, login budget, admission, mutation authority, promotion authority or completion evidence. Do not silently fall back to another model/provider or OpenAI API credential.

## 21. Evidence discipline

Use:

```text
FACT
INFERENCE
UNKNOWN
CONFLICT
```

A historical exact-client result may remain a historical `FACT`, but it is not current runtime identity or current authority.

Keep secret-free causal evidence under the active task's evidence directory. Prefer compact records containing exact head, run/job IDs, exact runtime identity, observed control-state counters and accepted/rejected hypotheses.

Do not persist raw proprietary client bytes, arbitrary secret-phase memory dumps or secret-bearing packet payloads.

## 22. Durable task and recovery state

Before any runner job, long operation or terminal-CI wait, persist the recovery checkpoint required by current repository governance.

Every incomplete worker stop must leave:

```text
checkpoint status: ready | waiting | blocked
exact branch/head/PR
current runtime authority/ownership classification
first unresolved causal edge
validation/evidence identifiers
one and only one next_action
```

Do not make chat history necessary for continuation.

## 23. Required closeout

Even after physical success:

1. persist the causal result and compact evidence;
2. run a fresh independent falsification audit of object provenance, runtime rebasing, Qt thread correctness, selected-character identity, false-login-success alternatives, false local-player alternatives, secret leakage and runtime-admission compliance;
3. repair material findings or withdraw the success claim;
4. run required exact-head CI on the final repository head;
5. resolve review threads and reconcile related/superseded PRs intentionally;
6. archive/terminally close the task and release runtime/lease/namespace/branch ownership according to current governance.

Do not mark the task `completed` while required E2E/audit/CI/PR/task lifecycle remains incomplete.

## 24. Legal worker stop conditions

Task success is the `CHARACTER_ACTUALLY_LOGGED_INTO_GAME` gate above.

A worker invocation may legally stop earlier only for a real governed outcome such as:

```text
WAITING
BLOCKED
ROTATE
EXTERNAL_ACTION_REQUIRED
```

Examples include exhausted execution/repair budget, conflicting current runtime ownership, unavailable required runner/runtime operation, missing legal secret ingress, legitimate unresolved 2FA/device confirmation, current admission failure or a required owner decision not already answered by authority/live state.

A discovered method, built bridge, successful auth, character list, character confirmation, game-login request or login-success packet is not a stop reason by itself.

## 25. Final success output contract

When success is actually proven, report at least:

```text
STATUS: DONE
TASK: OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME

EXACT_CLIENT:
version=15.32.df7b29
sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe

RESULT: SUCCESS
CHARACTER_ACTUALLY_LOGGED_INTO_GAME: YES
CAUSAL_PROOF: COMPLETE

ACCOUNT_AUTH_NATIVE=PASS | NOT_NEEDED_SESSION_REUSED
CHARACTER_LIST_RUNTIME_DISCOVERED=PASS
CHARACTER_SELECTION_NATIVE=PASS
REQUEST_GAMESERVER_LOGIN=PASS
GAME_SERVER_LOGIN_NATIVE=PASS
SERVER_ACCEPTANCE=PASS
FULLMAP_OBSERVED=PASS
MAP_DESCRIPTION_STRIPS=<integer >= 10>
GAMEPLAY_STATE_ACTIVE=PASS
LOCAL_PLAYER_ACTIVE=PASS
CHARACTER_IDENTITY_MATCH=PASS
WORLD_IDENTITY_MATCH=PASS

FORM_UI_USED=false
OCR_USED=false
IMAGE_MATCHING_USED=false
COORDINATE_LOGIN_USED=false
BLIND_TAB_RETURN_USED=false
GUI_CREDENTIAL_ENTRY_USED=false
PASSWORD_LOGGED=false
SESSION_SECRET_PERSISTED=false
AUTH_BYPASS_USED=false
TLS_WEAKENED=false
SERVER_RESPONSE_SPOOFED=false
UNAUTHORIZED_PARALLEL_SESSION=false

EVIDENCE:
<task>
<PR/exact head>
<runtime/run identifiers>
<causal evidence path>

AUDIT: PASS
BLOCKER: none
NEXT_ACTION: none
```

For a non-success stop, use the repository canonical terminal response and set:

```text
RESULT: INCOMPLETE
CHARACTER_ACTUALLY_LOGGED_INTO_GAME: NO
CAUSAL_PROOF: INCOMPLETE
BLOCKER: <exact blocker>
NEXT_ACTION: <exactly one executable next action>
```

## 26. Final invariant

```text
DO NOT AUTOMATE THE LOGIN FORM.
USE THE ORIGINAL CLIENT'S NATIVE AUTH/SESSION LOGIC.
REUSE CURRENT-MAIN #505/#507/#510 BEFORE BUILDING NEW INFRASTRUCTURE.
DO NOT INHERIT OLD #475 RUNTIME OR LOGIN AUTHORITY; TAKE FRESH ADMISSION.
DO NOT GUESS PID/XID/OBJECT/ABI/THREAD/SESSION STATE.
DO NOT PERSIST OR EXPOSE SECRETS.
DO NOT BYPASS 2FA/AUTH/TLS/SERVER ACCEPTANCE.
DO NOT CREATE A PARALLEL LOGGED-IN SESSION.
DO NOT CALL AUTH OR LOGIN SUCCESS "IN GAME".
FOLLOW THE SAME RUNTIME-DISCOVERED CHARACTER THROUGH NATIVE SELECTION, ORIGINAL GAME LOGIN, FULLMAP AND ACTIVE LOCAL PLAYER.
CALL THE TASK COMPLETE ONLY WHEN THAT CHARACTER IS ACTUALLY IN THE GAME.
```
