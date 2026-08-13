# OTC-20260727 — Tibia Linux runner analysis

## Status

`active_cv_bootstrap_structural_world` — `OTCLIENT-TIBIA-RE` continues on PR #48. Exact current-client runtime, WARP login identity, Worldmap decoding boundary, protocol/action/state catalogues and a non-GDB Qt integration primitive are proven. The current live experiment starts the client normally, uses non-OCR visual differencing only to bootstrap the already-proven account/character flow, and accepts `IN_GAME` only from decoded ordered-map records after bootstrap.

This is an operational research task. Temporary `.github/workflows/tibia-*` files are evidence scaffolding and are not product code.

## Ownership and authority

```yaml
repository: blakinio/otclient
branch: ci/OTC-20260727-tibia-linux-runner-analysis
pr: 48
programme: OTCLIENT-TIBIA-RE
external_runtime_evidence: blakinio/Oteryn-Platform@ops/oteryn-tibia-client-analysis-20260811 read-only only
canonical_oteryn_staging: out_of_scope
owner_funded_codex_api: forbidden_without_separate_owner_authorization
test_account_actions_secrets: authorized_only_through_existing_task_workflow_runtime
```

## Exact client/runtime — PROVEN

```yaml
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed_client_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
package_entries: 1634
asset_entries: 7094
packed_minimap_subareas: 209
```

Run `31626946078`, job `94215664628`, proved complete runtime reconstruction with `FAILED_ASSET_LOAD_COUNT=0`. Software Mesa/llvmpipe + lavapipe is the known-good hosted renderer path. `QT_XCB_GL_INTEGRATION=none` is rejected.

## WARP/account login service — PROVEN

Run `31647827166`, job `94285373954`, through verified changed WARP egress:

```text
HTTPS_STATUS=200
HAS_SESSION=true
HAS_PLAYDATA=true
HAS_CHARACTERS=true
HAS_WORLDS=true
```

The accepted request identity uses `clientversion=15.32.df7b29`, `clienttype=2` and the current 64-character asset version. Secret/account/session values were not persisted.

## Worldmap structural boundary — PROVEN

```text
FullMap        0xcec8d0
FieldData      0xcd3190
Create         0xcecc70
Change         0xcecf40
Delete         0xcd4e20
ordered map    0x19a8a80
capture point  0x19a8ea3
Worldmap qmeta 0x3087800
string data    0x1cd8a54
metadata       0x1cd8820
static call    0xdf2a60
```

QMetaObject layout: `string +0x8`, `metadata +0x10`, `static_metacall +0x18`.

Read-only same-hash Oteryn evidence proves 83 live ordered map records with real x/y/z over z6/z7. `raw28/raw30` semantics remain `UNKNOWN`.

## Static login/session discovery — PROVEN

Runs:

- QMeta recovery `31649792368`, job `94291373444`: PASS
- method-owner index `31650684531`, job `94294137219`: PASS
- auth inventory `31652067802`, job `94298391194`: PASS

Important semantic owners:

```text
TCharacterSelectionController qmeta=0x2f656a0 static=0xd46550
TAuthenticationProcessController qmeta=0x3073920 static=0xcfabb0
TLoginRequestUploader qmeta=0x2f657e0 static=0xcfb5a0
TGameserverLoginProcessController qmeta=0x30cdc60 static=0xcf9da0
TGameClient qmeta=0x2f61ea0 static=0xd06260
IGameSession qmeta=0x30790a0 static=0xd26400
TGameserverGameSession qmeta=0x2f765a0 static=0xd215c0
```

**DISPROVEN:** critical QMetaObjects were missing. The original filter mixed methods owned by different QMetaObjects.

**DERIVED CORRECTION:** QMeta static-dispatch targets prove semantic ownership but are not proven normal runtime call sites. Absence of a breakpoint on those wrappers is not evidence that the semantic state did not occur.

## Static action/protocol catalogue — PROVEN for exact binary

- capability QMeta run `31651155741`, job `94295569820`: PASS — 494 relevant methods, 460 direct qmeta dispatch targets;
- generated protocol inventory `31651220862`, job `94295767215`: PASS — 240 GameclientMessage + 550 GameserverMessage symbols, 142 capability-related;
- signature inventory `31651501473`, job `94296624884`: PASS;
- high-level action inventory `31651684700`, job `94297172395`: PASS — 1004 high-level action methods;
- structural read/state inventory `31652393473`, job `94299386259`: PASS — 121 targeted read/update methods.

Exact action families:

```text
TPlayerProtocolMessageHandler qmeta=0x30852a0 static=0xd1a920
  N/E/S/W, diagonals, GoPath, Rotate N/E/S/W, Stop, Cancel
TCreaturesGameActionHandler qmeta=0x3085060 static=0xd16340
  Attack, Follow
TGenericGameActionHandler qmeta=0x3085020 static=0xdcb990
  UseObject, MoveObject
TUseWithGameActionHandler qmeta=0x3085120 static=0xdc4480
  UseTwoObjects, UseOnCreature
TChatGameActionHandler qmeta=0x30851a0 static=0xcff5b0
  Talk
TContainerProtocolMessageHandler qmeta=0x3084fe0 static=0xd1e000
  Close/Up/Seek/Action plus incoming inventory/container handlers
```

High-level surfaces include `attackCreature(qint64)`, `followCreature(qint64)`, `useOnCreature(qint64)`, channel/private/NPC message methods, container methods and turn/movement controllers.

Important read/update families include `TCreature`, `TCreatureStorage`, `TCyclopediaMapStorage`, `TCooldownStorage`, `TPlayerData`, `TPlayerSkillStats`, `THitpointManabarController`, `TPlayerInventoryAndStatusController`, `TStatusBarController`, `TContainerStorage`, `TInventoryContainer`, `TMinimapController`, `TWorldmapProtocolMessageHandler` and `TProtocolMessageQueue`.

## Same-hash native action lead — read-only evidence

The Oteryn runtime independently proved a live `TPlayerProtocolMessageHandler` object with vptr offset `0x308a008` and native movement/rotation bodies:

```text
N 0xee2cd0  E 0xee2d50  S 0xee2dd0  W 0xee2e50
NE 0xee2ed0 SE 0xee2f50 SW 0xee2fd0 NW 0xee3050
Stop 0xee30d0 Cancel 0xee3150
Rotate N/E/S/W 0xee31d0/0xee3250/0xee32d0/0xee3350
```

Client survival and socket-byte changes were proven there, but authoritative OTClient-owned before/after position remains `UNKNOWN`.

Raw-file vptr scanner run `31652312282`, job `94299139890`, failed without useful evidence. Do not repeat the identical scanner.

## Phase 9 stable bridge — PROVEN primitive

Experiment:

```yaml
workflow: .github/workflows/tibia-hosted-preload-qobject-probe.yml
commit: 1e04782d624a478338c633ee27d06064e13b2d3c
run: 31653375069
job: 94302324521
result: PASS
```

The exact official client was launched with a temporary `LD_PRELOAD` Qt6 helper and no credentials. It proved:

```text
PRELOAD_CONSTRUCTOR=true
QUEUED_SCAN=true
QOBJECT_SCAN_COUNT=8
QT_PRELOAD_BRIDGE_THREAD_INVOCATION_PROVEN=true
```

Therefore **PROVEN:** a non-GDB injected helper can execute queued code on the real client Qt event loop without permanently patching CipSoft files.

The helper's `QCoreApplication::findChildren<QObject*>()` scans found only 6–7 ordinary descendants and zero target Tibia classes (`QOBJECT_MATCHED_CLASS_ROWS=0`). Therefore **DISPROVEN:** the game handlers can be discovered simply as QCoreApplication QObject children.

**DERIVED bridge architecture:** retain `LD_PRELOAD` + Qt-thread invocation, add Unix-domain IPC, and resolve target objects through semantic static/runtime references, registries, vptrs/RTTI/signatures and structural validation rather than QObject child traversal.

## Live world-entry experiments and rejected hypotheses

Runs `31650884938`, `31651611051`, `31652180172` proved that old UI marker `FIRST_CHARACTER_ACTIVATED` and QMeta wrapper-hit absence were not valid structural state evidence.

GDB-from-start run `31652573423`, job `94299916593`, proved real local SOCKS auth traffic but not world entry. Decoded-map GDB-from-start run `31653056907`, job `94301369226`, reached zero map records despite auth traffic and bounded row activation.

Read-only same-hash handover shows the successful world entry starts the client normally and attaches GDB only after the bootstrap session exists. Therefore **REJECTED:** starting the client under GDB is the preferred recovery/login path.

## Current live experiment

```yaml
experiment_id: OTC48-WORLD-ENTRY-003
workflow: .github/workflows/tibia-hosted-cv-bootstrap-structural-world.yml
head: 0f5912373e010d445e0589381f86e738f95d844b
run: 31653732464
status: running
objective: reproduce normal-start same-hash world bootstrap, then attach and prove decoded map records
bootstrap_evidence:
  - local screenshot difference only as non-OCR recovery aid, threshold >45000
  - login transition must be observed before character-row activation
  - local SOCKS game connection must remain sustained >=6 observations
  - reversible Right action must change viewport by >1000 pixels
semantic_acceptance:
  - GDB attaches only after bootstrap
  - base+0x19a8ea3 produces >=8 structurally valid decoded map records
  - zero direct TCP/UDP
  - only then STRUCTURAL_IN_GAME=true
```

Visual differences are not accepted as protocol/interface semantics; they only reproduce the proven bootstrap procedure before structural validation.

## Persistent self-hosted runtime recovery

PR #48 owns a persistent design on selector `[self-hosted, oteryn-staging]` with expected runner `oteryn-synology-staging`, container `otclient-tibia-login-analysis`, and state bind `/var/lib/oteryn-staging-state/tibia-linux-analysis`.

Read-only probe workflow `.github/workflows/tibia-synology-owned-runtime-state.yml`, run `31653611110`, is pending runner acceptance. Do not claim the runner/container available until a job actually starts.

## Safety invariants

- no OCR/Tesseract/image-to-text for login or semantic proof;
- no secret values in argv/logs/screenshots/repository/artifacts/chat;
- verify changed WARP egress before secret use;
- zero unintended direct TCP/UDP where required;
- no canonical staging mutation and no mutation of the separately owned Oteryn runtime;
- pixels/windows are bootstrap aids only, never semantic world-state evidence;
- leave the character idle once world entry is structurally proven until the next action experiment is explicitly bounded.

## Durable checkpoint

```yaml
checkpoint_version: 6
updated_at: 2026-08-13T02:19:00+02:00
branch: ci/OTC-20260727-tibia-linux-runner-analysis
pr: 48
head_before_checkpoint: 0f5912373e010d445e0589381f86e738f95d844b
status: investigating
proven:
  - exact full runtime and current WARP login-service identity
  - same-hash Worldmap decode boundary
  - exact Qt/protobuf action and state catalogues
  - non-GDB LD_PRELOAD helper executes queued work on the real Qt event loop
rejected_hypotheses:
  - critical QMetaObjects missing
  - FIRST_CHARACTER_ACTIVATED marker proves activation
  - lack of QMeta wrapper breakpoint proves auth state absent
  - GDB-from-start is the preferred world-entry recovery path
  - QCoreApplication QObject descendants contain the target game handlers
  - blind raw-qword vptr scanner
unknown:
  - current OTClient-owned structural IN_GAME session
  - authoritative player position in a current OTClient-owned live session
  - live before/after movement/action effects in that session
  - stable target-object resolver for the preload bridge
active_operations:
  - run: 31653732464
    workflow: tibia-hosted-cv-bootstrap-structural-world.yml
  - run: 31653611110
    workflow: tibia-synology-owned-runtime-state.yml
    state: awaiting self-hosted runner acceptance
safe_to_resume: true
next_action: reconcile terminal CV-bootstrap run once; on decoded IN_GAME immediately reacquire PID/PIE and prove authoritative player-position plus one reversible movement transition, while continuing preload target-object resolver work independently
```

## Continuation evidence — 2026-08-13 08:18 CEST

This section supersedes the stale `status: running`/`active_operations` values above while preserving the historical experiment description.

### CV-bootstrap world-entry result — terminal failure before login

Run `31653732464`, job `94303431126`, is terminal `failure`.

```yaml
failed_step: Reconstruct and start exact client normally
cv_bootstrap_login_step: skipped
post_bootstrap_structural_attach_step: skipped
semantic_world_evidence_produced: false
```

The logs prove WARP account/profile generation succeeded, but the step exited with code 1 before `NORMAL_EXACT_CLIENT_READY=true`. No account-login or character-selection action ran in this experiment. The exact failing subcommand inside the reused reconstruction/start sequence is **UNKNOWN** from the retained log; do not attribute this failure to login, UI geometry, character selection, or changed client identity.

### Relocation-aware primary-vptr recovery — PROVEN

Run `31654434331`, job `94305639119`, passed on the exact researched binary and recovered nine primary vptrs:

```text
TPlayerProtocolMessageHandler   0x308a008
TWorldmapProtocolMessageHandler 0x30871d8
TGameserverGameSession          0x3078ba0
TGameSessionBase                0x3084648
IGameSession                    0x30841c0
TPlayerData                     0x308ca70
TContainerStorage               0x308a1a0
TCreatureStorage                0x308d078
TGameClient                     0x3076908
```

This replaces the rejected blind raw-qword scanner as the preferred exact-binary resolver approach. The durable implementation lives in PR #283 under `tools/tibia_runtime_bridge/**`.

### Durable runtime bridge — PROVEN through exact-client no-credential E2E on head 39ff79ac

PR #283 is the separate stable Phase 9 bridge task. Run `31654701845`, job `94306484551`, validated exact bridge head `39ff79ac44a0a1010b4bcc8b8e3617525353df7e`:

```text
EXACT_BRIDGE_HEAD_VERIFIED=true
11 focused tests PASS
BRIDGE_STANDALONE_BUILD_PASS=true
COMPLETE_OFFICIAL_RUNTIME_LAYOUT_VERIFIED=true
EXACT_BRIDGE_VALIDATION_RUNTIME_READY=true
BRIDGE_SOCKET_MODE=600
EXACT_CLIENT_BRIDGE_E2E_PASS=true
```

`PING` resolved the PIE base; all profiled discovery commands returned valid bounded JSON; the exact client remained alive. In logged-out state:

```yaml
player_protocol_handler.validated_hits: 0
gameserver_game_session.validated_hits: 0
worldmap_handler.validated_hits: 0
in_game_candidate: false
evidence_level: DERIVED_UNTIL_LIVE_CORRELATION
```

That is correct fail-closed behavior. It is not yet proof of live `IN_GAME` marker correlation.

PR #283 current head at this checkpoint is `89e13819e6f53026b831b7e8e4c8fab228d1626c`, newer than the successful E2E head because it adds the durable relocation resolver and additional tests. Final exact-current-head validation remains required.

### Current upstream client identity — UNKNOWN, probe inconclusive

Run `31654893952`, job `94307092804`, failed during the fresh WARP download of:

```text
https://static.tibia.com/launcher/tibiaclient-linux-current/bin/client.lzma
```

WARP setup succeeded, but the job terminated before any of these markers were emitted:

```text
CURRENT_PACKED_SHA256
CURRENT_PACKED_SIZE
CURRENT_CLIENT_SHA256
CURRENT_CLIENT_SIZE
```

Therefore the probe gives **no evidence** that the official client changed and no evidence that it stayed identical. The current upstream SHA must be re-verified before treating historical offsets as current.

### Programme state after continuation

```yaml
checkpoint_version: 7
updated_at: 2026-08-13T08:18:00+02:00
branch: ci/OTC-20260727-tibia-linux-runner-analysis
pr: 48
status: investigating_runtime_recovery_and_live_bridge_correlation
proven:
  - exact researched client/runtime and WARP login-service identity
  - same-hash Worldmap decode boundary and 83-record read-only live sample
  - exact action/protocol/state catalogues
  - non-GDB Qt preload primitive
  - relocation-aware primary-vptr resolver on exact researched binary
  - durable bridge exact-client no-credential E2E on head 39ff79ac
rejected_hypotheses:
  - critical QMetaObjects missing
  - FIRST_CHARACTER_ACTIVATED marker proves activation
  - lack of QMeta wrapper breakpoint proves auth state absent
  - GDB-from-start preferred recovery path
  - QCoreApplication descendants contain target game handlers
  - blind raw-qword vptr scanning
latest_terminal_failures:
  - run: 31653732464
    scope: CV-bootstrap
    failure_boundary: runtime reconstruction/start before login
  - run: 31654893952
    scope: current-client identity
    failure_boundary: fresh client.lzma download before any hash output
unknown:
  - current upstream official-client SHA
  - current OTClient-owned structural IN_GAME session
  - live correlation of bridge session markers
  - authoritative player position
  - live before/after movement and other action effects
  - raw28/raw30 semantics
safe_to_resume: true
next_action:
  - first re-verify current upstream client identity with a bounded downloader that emits HTTP/curl diagnostics without secrets
  - if SHA is unchanged, isolate the CV-bootstrap reconstruction/start failure instead of repeating the full login workflow
  - if SHA changed, run durable relocation resolver against the new ELF and create a new exact-version profile
  - once structural IN_GAME is restored, correlate bridge session-status, read authoritative position, and prove one reversible movement transition before any write/action bridge API
```

No Codex or owner-funded AI/API quota was used.

## Continuation evidence — 2026-08-13 12:10 CEST

### Current official-client identity — PROVEN unchanged

Hosted run `31674406184` at head
`cfaa7654352e2dbafc316f30aea9c787aaa64b8d` completed successfully through fresh
WARP and emitted:

```yaml
client_http_code: 200
packed_size: 10150849
packed_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
version_strings: "15.32"
```

This exactly matches the researched binary identity. The failed earlier run
`31654893952` is superseded for current-client identity only; it remains useful
as downloader-failure evidence. Existing exact-SHA profiles may therefore be
reused after live PID/PIE/object rediscovery.

### Dedicated runner reconciliation — WAITING

PR #48 current head is
`17b55cecb596ff0224201d85ea50e02cb1b67511`. Canonical bootstrap run
`31687610951`, job `94407259983`, remained `queued` at the bounded observation.
The older canonical bootstrap `31679097113`, migration run `31686590850`, and
broad `runs-on: self-hosted` probe `31643425060` also remain queued. No live
evidence proves that `synology-otclient-01` is online or accepting jobs.

PR #280 persists the already-reviewed deployment stack and one-time migration
workflow. The current environment exposes neither an authorized Synology/SSH
execution channel nor an available self-hosted GitHub Actions control-plane job,
so the runner cannot be recreated safely from this session.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-13T12:10:00+02:00
head: 17b55cecb596ff0224201d85ea50e02cb1b67511
branch: ci/OTC-20260727-tibia-linux-runner-analysis
pr: 48
status: blocked
context_routes:
  - official-client-runtime-analysis
  - dedicated-runner-migration
owned_paths:
  - docs/agents/tasks/active/OTC-20260727-tibia-linux-runner-analysis.md
proven:
  - current official-client identity is unchanged at e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe by run 31674406184
  - exact researched relocation-aware profiles remain applicable after live PID/PIE/object rediscovery
  - PR 48 canonical bootstrap is queued and has not been accepted by synology-otclient-01
derived:
  - live structural experiments can resume without a new exact-version profile once the dedicated runner is restored
unknown:
  - Synology host power and reachability state
  - repository registration state of synology-otclient-01
  - current official-client process/session/container state because no runner job can inspect it
  - structural IN_GAME, authoritative player position, and live action effects
conflicts:
  - owner handover says synology-otclient-01 is now working, while current GitHub jobs remain queued
first_failure:
  marker: no authorized execution path reaches the Synology host
  evidence: runs 31687610951, 31686590850, and 31643425060 remain queued
validation:
  - command: gh run view 31674406184 --repo blakinio/otclient --log
    result: PASS
    evidence: HTTP 200 and exact packed/client hashes above
  - command: gh run view 31687610951 --repo blakinio/otclient --json status,conclusion,jobs
    result: BLOCKED
    evidence: bootstrap job 94407259983 remains queued
rejected_hypotheses:
  - current official-client binary changed: disproven by run 31674406184
changed_paths:
  - docs/agents/tasks/active/OTC-20260727-tibia-linux-runner-analysis.md
blockers:
  - no authorized live Synology/SSH channel and no available self-hosted repository runner
next_action: restore one authorized Synology execution path, deploy PR 280's reviewed otclient-runner stack, then reconcile PR 48 run 31687610951 and inspect the official-client process/session structurally
```
