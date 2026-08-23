# Package D physical retry — terminal runtime admission evidence

Task: `OTC-20260823-control-center-package-d-physical-retry`
PR: `#685`
Admission trusted main: `daaf939fc6e3d98686de38d5dadecde2c68b3c8d`
Branch: `runtime/OTC-20260823-control-center-package-d-physical-retry`

## Terminal disposition

```text
RUNTIME_ADMISSION=BLOCKED
TARGET_UNIQUENESS=BLOCKED
GATE_A=N/A
REBIND=N/A
GATE_B=N/A
ACTION=NOT_ATTEMPTED
PHYSICAL_ACTION_COUNT=0
PHYSICAL_RESULT=BLOCKED_WITH_REASON
AUTHORITATIVE_CONFIRMATION=N/A
NO_RETRY=true
BLOCKER=BLOCKED_TRACK_A_RUNTIME_EXECUTOR_NOT_ACQUIRED
```

## Fresh admission boundary

This retry did not inherit any PID, display, XID, runtime ID, registration generation, lease generation, prior `IN_GAME`, prior runtime SHA, or previous Package D runtime result as current authority.

The branch was created from fresh `main@daaf939fc6e3d98686de38d5dadecde2c68b3c8d`; the same SHA was re-read from current `main` immediately before the bounded physical admission attempt. A new task record and Draft PR #685 were created and active-task/open-PR ownership overlap was checked before live work.

The required task-specific physical executor could not be acquired during the bounded admission attempt:

- task workflow run `32659364967` for head `ad14f56e41cff98e8b9f438e6025dc0343107660` remained `pending` and exposed no job after two bounded job-state reads;
- after aligning the task workflow to the trusted repository's canonical Synology runner labels `[otclient, synology]`, fresh task workflow run `32659479168` for head `32c9e99665e9d8e16b59df351312b3ec388e0c2f` also remained `pending` at the bounded current-state check;
- both Remote Desktop Commander devices named `Synology` were freshly observed `offline` in the bounded transport check;
- the installed read-only `synology oteryn` connector returned an MCP gateway `404` on a fresh `nas_info` call;
- an isolated local clone/worktree fallback was attempted only for repository isolation, not runtime access, and the sandbox could not resolve `github.com`; it therefore created no worktree and performed no runtime operation.

The temporary workflow's first executable step on the physical runner would have created a detached isolated task worktree at the exact PR head. Because no job was acquired, that step never ran. No weaker checkout or shared physical worktree was substituted.

## Fail-closed admission result

No live Official Tibia observation was performed. In particular, this invocation did not inspect a current Official Tibia process, PID, process start identity, executable path, display, window, runtime namespace contents, or current client semantic state.

Because the permitted physical executor was not acquired, this invocation could not freshly read the canonical state root and therefore did **not** claim whether `runtime-registration.json` is present or absent. `runtime_access` remains `none`; no canonical bootstrap/adoption/reuse/rebind authority was asserted.

Consequently all of the following current facts remain unproven and are refused rather than guessed:

- canonical registration presence/generation;
- controller lease generation and registration/lease generation equality;
- current exact client PID/start identity;
- current exact version/size/SHA identity;
- display/window ownership;
- conflicting or unverifiable target candidates;
- Gate A;
- generation rebind applicability/result;
- Gate B;
- target uniqueness;
- active-world semantic authority;
- adapter mutation capability.

`UNKNOWN = REFUSE` therefore terminates the physical slice before any authority acquisition or guarded dispatch.

## Dispatch and side-effect accounting

Declared budget remained:

```text
max_actions=1
max_movement_tiles=0
max_spells=0
max_consumables=0
max_items_moved=0
max_gold=0
max_tibia_coins=0
max_irreversible_changes=0
```

No Control Center action budget was consumed. No external Track A mutation guard, canonical `input.lock`, guarded-dispatch `READY`, `COMMIT`, or worker invocation occurred. The one permitted semantic `turn` was not attempted. There was no fallback movement and no second attempt.

```text
PHYSICAL_ACTION_COUNT=0
BUDGET_ACTIONS_CONSUMED=0
STOP_CONTROL_GENERATION_MUTATED=false
POST_COMMIT_UNCERTAINTY=false
POSSIBLY_DISPATCHED=false
```

No authoritative confirmation is applicable because there was no physical dispatch.

## Adapter / request evidence

Package D implementation was reused from trusted main; no second controller, registration system, lease manager, or alternate authority path was created.

Because admission failed before semantic execution reservation, there is intentionally no action request hash, READY evidence, COMMIT decision, runtime/session identity, or adapter execution generation for a dispatched action. Recording synthetic values for those fields would misrepresent the fail-closed path. The semantic candidate remained `turn` with finite effect bound `(actions=1, movement_tiles=0, spells=0, consumables=0, items_moved=0, gold=0, tibia_coins=0, irreversible_changes=0)`.

## Privacy / secret safety

No credentials, 2FA, token contents, arbitrary process memory, packet payloads, private chat, raw screenshots, or secret-bearing runtime handles were read or persisted. The controller lease status/registration metadata workflow never executed on the physical runner. Repository evidence contains only GitHub/runtime-transport identifiers required to explain the admission blocker.

```text
PRIVACY_SCAN=PASS
CREDENTIALS_ACCESSED=false
LOGIN_ATTEMPTED=false
OFFICIAL_CLIENT_ACCESS=NONE
MUTATION_AUTHORIZED=false
```

## Closeout rule

The exact terminal blocker is `BLOCKED_TRACK_A_RUNTIME_EXECUTOR_NOT_ACQUIRED`. It is not converted into a target/physical PASS. A later retry, if desired, must be a different newly admitted task; this task performs no retry and releases all ownership at closeout.
