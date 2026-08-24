# Package D physical retry 3 — terminal runtime-admission evidence

```yaml
task: OTC-20260824-control-center-package-d-physical-retry-3
pull_request: 687
branch: runtime/OTC-20260824-control-center-package-d-physical-retry-3
trusted_main_at_admission: f868ac2bc642782a4443d167752591bda15710df
controller_preflight_head: e4677caeaaff97a8bab4d2a014daddd93a5db2d8
controller_preflight_run: 32724948938
controller_preflight_job: 97424027710
runtime_admission: BLOCKED
target_uniqueness: NOT_REACHED
gate_a: NOT_REACHED
rebind: NOT_REACHED
gate_b: NOT_REACHED
semantic_state: UNKNOWN
action: TURN_NOT_ATTEMPTED
physical_action_count: 0
ready_emitted: false
commit_emitted: false
possibly_dispatched: false
authoritative_confirmation: NOT_REACHED
result: BLOCKED_WITH_REASON
blocker: BLOCKED_NO_LEGAL_EXISTING_IN_GAME_LIFECYCLE
blocker_detail: REQUIRED_SEMANTIC_IN_GAME_DISCRIMINATOR_UNAVAILABLE
```

## Fresh repository and transport boundary

The retry started from `runtime_access: none` and did not accept any historical PID, XID, display, port, session, lease, registration generation or previous runtime observation as current authority.

Fresh GitHub preflight resolved `main` to `f868ac2bc642782a4443d167752591bda15710df` and PR #687 to the retry-3 branch. The exact current Official Tibia fence remained:

```text
version=15.32
size=52109920
sha256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
platform=official_native_linux_only
```

Fresh Remote Desktop Commander health proved Synology online. The existing runner container `otclient-synology-runner` was found cleanly stopped with restart policy `no`. A narrow restart of that existing container was performed; no runner token value, credential, SSH/DSM setting or authentication configuration was read, reused or modified. The runner advertised the expected safe identity `synology-otclient-01` with labels `otclient,synology`, and GitHub subsequently assigned the retry job to that exact runner, proving executor acquisition.

The first controller-preflight generation exposed a repository-local invocation defect: the canonical lease wrapper is mode `100644`, so direct execution failed with exit 126. The task repaired only the task-specific workflow to invoke the reviewed wrapper through `bash`; no Track A runtime implementation or authentication surface was modified.

## Successful controller-plane admission discovery

Run `32724948938`, job `97424027710`, completed successfully on exact head `e4677caeaaff97a8bab4d2a014daddd93a5db2d8` and runner `synology-otclient-01`.

The job created an isolated task worktree and reported:

```text
WORKTREE_ISOLATION=PASS
WORKTREE_HEAD=e4677caeaaff97a8bab4d2a014daddd93a5db2d8
CURRENT_MAIN_SHA=f868ac2bc642782a4443d167752591bda15710df
TRACK_A_CANONICAL_LEASE_STATUS=released
TRACK_A_CANONICAL_LEASE_GENERATION=19
CANONICAL_REGISTRATION=PRESENT
REG_SCHEMA_VERSION=1
REG_RUNTIME_ID=track-a-canonical-live
REG_REGISTRATION_GENERATION=2
REG_LEASE_GENERATION=19
REG_CLIENT_VERSION=15.32
REG_CLIENT_SIZE=52109920
REG_CLIENT_SHA256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
REG_STATE=UNKNOWN
LIVE_OFFICIAL_CLIENT_OBSERVATION=NOT_PERFORMED
OFFICIAL_CLIENT_MUTATION=NOT_PERFORMED
PHYSICAL_ACTION_COUNT=0
```

This proves current controller-plane state only. It does not prove Gate A, Gate B, target uniqueness or `IN_GAME`, and it grants no mutation authority.

## Semantic active-world blocker

Current reviewed `main` deliberately refuses to promote the available structural signals to `IN_GAME`:

- `.github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py` treats bridge `PING` plus the validated player-protocol, game-session and worldmap objects as structural presence only and returns semantic state `UNKNOWN`;
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`, `docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md` and `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md` record the 2026-08-20 exact-peer login-screen false positive and require a separately reviewed semantic/causal active-world discriminator;
- `tools/tibia_re_surveyor/player_state.py` exposes the current exact-build typed position reader as `CANDIDATE_PENDING_CAUSAL_E2E` and sets `semantic_promotion_allowed` to false;
- `docs/agents/CHANGELOG.md` states that semantic promotion for that typed reader remains disabled until post-merge owner-controlled movement differential proof;
- `docs/agents/contracts/MAP_OBSERVATION_V1.md` defines the normalized decoded-world contract and fixture validator, but does not itself provide runtime authority or a live action/state producer;
- the Package D contract requires current semantically proven `IN_GAME`; if current active-world state cannot be proved under legal authority, it requires fail-closed termination.

This task explicitly forbids movement and does not authorize credentials, login, 2FA or character selection. Therefore it cannot legally manufacture the missing semantic proof by moving, logging in, relogging or creating another session. A visual observation is not an authoritative substitute under the current Package D contract.

The required semantic discriminator is therefore unavailable within the task's existing reviewed primitives and authority. `UNKNOWN => REFUSE` applies before Gate A acquisition or any physical worker/READY/COMMIT path.

## Effect, dispatch and privacy accounting

```yaml
effect_budget:
  max_actions: 1
  max_movement_tiles: 0
  max_spells: 0
  max_consumables: 0
  max_items_moved: 0
  max_gold: 0
  max_tibia_coins: 0
  max_irreversible_changes: 0
consumed:
  actions: 0
  movement_tiles: 0
  spells: 0
  consumables: 0
  items_moved: 0
  gold: 0
  tibia_coins: 0
  irreversible_changes: 0
ready_emitted: false
commit_emitted: false
possibly_dispatched: false
official_client_access: NONE
credentials_accessed: false
login_attempted: false
character_selection_attempted: false
privacy_scan: PASS
```

There is no post-COMMIT ambiguity because COMMIT was never reached. No fallback turn exists and no physical action was sent.

## Terminal disposition

Retry 3 is terminal fail-closed as `BLOCKED_WITH_REASON` with blocker `BLOCKED_NO_LEGAL_EXISTING_IN_GAME_LIFECYCLE`, specifically because the required reviewed semantic `IN_GAME` discriminator is unavailable while all authority-expanding alternatives are forbidden by the task.

The infrastructure blocker from retry 2 was genuinely removed: Synology and `synology-otclient-01` were acquired and the isolated controller preflight passed. The remaining blocker is semantic authority, not executor availability.

Repository validation/audit/PR hygiene are closeout gates and cannot upgrade this blocked physical result. The task-specific preflight workflow is removed during closeout. No retry-4 is created by this task.
