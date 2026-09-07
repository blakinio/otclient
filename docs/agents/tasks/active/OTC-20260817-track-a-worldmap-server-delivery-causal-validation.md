---
task_id: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
status: waiting
agent: null
session_id: null
session_role: released
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: released_successor_re_admission_required
branch: runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation
base_branch: main
updated: 2026-08-18T09:40:00+02:00
risk: critical
related_pr: 475
runtime_access: none
runtime_owner_task: null
runtime_namespace: null
PHYSICAL_E2E_REQUIRED: true
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
mutation_authorized: false
client_byte_mutation_authorized: false
owner_authorization_source: historical_current_conversation_only
owner_authorization_text: "dokoncz zadanie"
owner_authorization_scope: historical only; all prior sequential-login/runtime authority is released by owner-requested session handoff and must not be inherited by a successor without fresh admission/ownership and then-current owner/governance authority
owner_funded_ai_api_authorized: false
owned_paths: []
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
release_handoff: docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-causal-validation/20260818-session-release-handoff.md
launch_budget:
  baseline_ephemeral_login_max_historical: 12
  baseline_ephemeral_login_consumed_before_v22_durable_authority: 11
  baseline_ephemeral_login_consumed_final: UNKNOWN_REDERIVE_FROM_TERMINAL_V22_LOGS
  patched_ephemeral_login_max_historical: 1
  patched_ephemeral_login_consumed: 0
  simultaneous_logged_in_sessions_max: 1
safety:
  direct_unapproved_egress: forbidden
  warp_socks_required: true
  raw_client_commit_or_upload: forbidden
  credentials_in_logs_or_artifacts: forbidden
  screenshots_or_ocr_artifacts: map_only_post_structural_screenshot_authorized
  ocr: forbidden
  transient_xwd_only: true
  screenshot_source_xwd_must_be_deleted: true
  screenshot_login_or_character_selection: forbidden
  broad_process_cleanup: forbidden
  canonical_source_patch_in_place: forbidden
  rollback_required: true
  coordinate_character_selection_control: forbidden
  current_session_runtime_use: forbidden_until_fresh_successor_admission
ci_check_generation: released_handoff_v40
---

# Objective

Reach the real game world on the exact official Linux client, prove `IN_GAME` structurally with pre-Storage `FullMap` plus at least 10 map-description strip records, persist one cropped map-only screenshot, then perform the single task-owned baseline `[18,14]` versus patched `[19,14]` causal comparison of authoritative server-delivered map data.

The objective is **not completed**.

# Owner-requested session release

The owner explicitly requested that the current agent save its work and release tasks/runtime/session state so another agent can continue without being blocked.

Therefore this checkpoint releases:

```text
CURRENT_AGENT_OWNERSHIP=NONE
CURRENT_SESSION_ID=NONE
CURRENT_RUNTIME_AUTHORITY=NONE
CURRENT_CREDENTIAL_AUTHORITY=NONE
CURRENT_LOGIN_AUTHORITY=NONE
CURRENT_GAMEPLAY_AUTHORITY=NONE
CURRENT_MUTATION_AUTHORITY=NONE
OWNED_PATHS=[]
```

PR #475 remains Draft. This task remains under `tasks/active` with status `waiting` because the research objective is unresolved; it is not archived or marked complete.

# Durable handoff

Read first:

`docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-causal-validation/20260818-session-release-handoff.md`

That handoff records the physically proven account-login and native single-character confirmation chain, the v19 downstream signal boundary, the QMeta/thunk corrections, the v20-v22 conservative authority history, VNC observer findings, unresolved `FullMap` boundary, and the current-main drift that a successor must consume before resuming.

# Proven state retained for successor

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

V18 physical run `32076063134 / 95529595652` is the canonical character-confirmation discriminator.

V19 established the downstream boundary with observed native request-character and request-character-gameserver activity but no accepted structural `FullMap` result.

# Critical corrections

- `Invalid Monk` is not a runtime-discovered fact and must not be used as a target assumption.
- Coordinate/pixel/Tab character-selection control is closed.
- Historical `0xd47300` must not be treated as a safe standalone `requestCharacterLogin` entry.
- QMeta/static-metacall must use a proven live object, correct ABI/argv, exact relocated address/instruction fence and Qt thread affinity.
- GDB scheduler locking must be restored before normal network/session progression.
- QMeta case/thunk addresses must be distinguished from real implementations when observing state progress.

# Current-main drift

Before resuming, successor must re-read current `main`. Since this branch's runtime work began, canonical main gained newer native-auth work including:

```text
PR #505 / 17cc0dc1bf29c440cc08e443bdce98e4dde7be5d  native cold-auth QMeta research
PR #506 / ed6202216886ec31d432e4e7dec56b47626f10c4  closeout/release
PR #507 / 2e6992da330e8a52d03b94b8d6a9de6fa79a6800  experimental form-less native auth bridge
PR #508 / ed09418b431c28087775b419f85bed404fa85d70  bridge closeout/release
```

A successor should consume/revalidate this newer promoted work instead of repeating the old form/UI credential-entry path unless the new bridge is proven inapplicable to the exact runtime.

# Current wider causal result

```text
SERVER_MAP_DELIVERY_MODEL=UNKNOWN
PATCH_CAUSES_ADDITIONAL_AUTHORITATIVE_MAP_DATA=UNKNOWN
BASELINE_AUTHORITATIVE_INBOUND_EXTENT=UNKNOWN
PATCHED_AUTHORITATIVE_INBOUND_EXTENT=UNKNOWN
OUTBOUND_EXTENT_NEGOTIATION_CHANGE=UNKNOWN
STORAGE_EXTENT_CHANGE=UNKNOWN
RENDER_PICKER_EXTENT_CHANGE=UNKNOWN
```

No patched comparison is permitted before a fresh successor-owned baseline reaches structural `IN_GAME` and records the authoritative inbound baseline extent.

# Successor admission contract

A future agent must not inherit any live session or login authority from this checkpoint. It must:

1. read current main and this release handoff;
2. re-read terminal v18-v22 logs before asserting final login-budget consumption;
3. perform fresh no-client/task-namespace inventory on `synology-otclient-01`;
4. acquire fresh task/runtime ownership and then-current admission;
5. prove one-session uniqueness and exact-client/XID/WARP/GDB gates anew;
6. use runtime-discovered character data only;
7. prefer current-main native auth bridge work when exact fences permit;
8. complete only on `FullMap + >=10 strips + post-structural exact-window screenshot`;
9. only then run the one task-owned `[19,14]` causal comparison.

# Checkpoint

```yaml
checkpoint_version: 40
status: waiting
phase: released_successor_re_admission_required
agent: null
session_id: null
runtime_access: none
runtime_owner_task: null
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
mutation_authorized: false
owned_paths: []
structural_in_game: false
map_screenshot: false
last_completed_step: persisted full current-session handoff and released repository/runtime ownership at owner request
blockers:
  - fresh successor admission and runtime ownership required
  - successor must consume current-main native auth bridge drift before continuing
next_action: successor re-reads current main plus handoff, re-derives terminal v22 consumption from logs, performs fresh no-client inventory, claims ownership, and resumes from the post-character-confirmation game-server state-machine boundary
```
