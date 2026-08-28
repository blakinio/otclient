# Track A gameWindowState read-only admission alignment

Date: 2026-08-28
Task: `OTC-20260828-game-window-state-qualification`
PR: #756

## Scope

This evidence covers only the repository/workflow alignment required to admit the already-merged bounded `TGameWindowController::gameWindowState` reader as a fresh `runtime_access: read_only` observation.

It does **not** claim any live `gameWindowState` observation, causal phase result, `IN_GAME` promotion, client mutation, GUI/input action, login, character selection, gameplay, packet payload capture, environment retention, or process-memory write.

`IN_GAME_CLAIMED=false`

`semantic_promotion_performed=false`

## Trusted base

The branch was created from protected `main` at:

`76515d605f7a76eebe25af0fd0dd68781f086f88`

That base already contains:

- PR #750 static exact-current `gameWindowState` proof;
- PR #755 bounded reader/tests/workflow preparation;
- PR #754 canonical exact-client fence repair.

Current exact-client fence used by the workflow:

- version `15.32.75d4a0`;
- size `52105824`;
- SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`.

Canonical admission authority consulted from trusted main:

`docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`

The deterministic validator further establishes that a repository task checkpoint declaring `runtime_access: read_only` is valid only with currently proven target uniqueness. Historical evidence therefore cannot be used to persist a future `target_uniqueness: PROVEN` value.

## TDD RED

Final test-only RED head:

`1c0b14e5178f63997905761aba781db731b4938d`

GitHub Actions:

- workflow run `33192009392`;
- job `98919581462` (`Read-only gameWindowState contract`);
- conclusion `failure` in `Validate focused reader and workflow contracts`;
- live qualification job `98919583031` was `skipped`.

The RED asserted that the pre-existing workflow incorrectly treated canonical Gate A / generation rebind / Gate B as read-only requirements and lacked the bounded fresh target/admission contract.

## Governance correction during GREEN

An intermediate attempt persisted `runtime_access: read_only` with `target_uniqueness: UNKNOWN`. Track A governance correctly rejected that state: a persisted read-only live-observation checkpoint must already have `target_uniqueness: PROVEN`.

The final design therefore leaves the repository checkpoint at:

- `runtime_access: none`;
- runtime owner / namespace / canonical registration / target uniqueness `NOT_APPLICABLE`;
- Gate A / generation rebind / Gate B / bootstrap `NOT_APPLICABLE`;
- `mutation_authorized: false`.

The trusted-main workflow then performs a bounded fresh admission sequence and persists a mode-0600 runner-local admission record **before** `/proc/<pid>/mem` can be opened. The emitted record contains:

- `runtime_access: read_only`;
- this task as `runtime_owner_task`;
- namespace `track-a-game-window-state-validation`;
- `canonical_registration: PRESENT`;
- canonical gates `NOT_APPLICABLE`;
- `target_uniqueness: PROVEN`;
- `mutation_authorized: false`;
- exact client fence plus exact PID/start identity and trusted-main SHA.

Admission fails closed on missing/unsafe registration files, malformed lease state, a fresh unexpired lease owned by another task, stale runtime locator, incomplete Docker inventory, any unverifiable official-looking candidate, any wrong-fence candidate, non-unique candidate count, or mismatch with the registered PID/start/container.

No GUI/window-title probe is used by this workflow.

## GREEN evidence before this evidence-only commit

GREEN implementation head:

`67ec3bd6ca80e571485156971a6ee2b71dbb9693`

Focused workflow:

- run `33192741679`;
- job `98922084760` (`Read-only gameWindowState contract`) = `SUCCESS`;
- step `Validate focused reader and workflow contracts` = `SUCCESS`;
- live qualification job `98922086020` = `skipped`.

Track A governance:

- run `33192741482`;
- job `98922083324` (`Fresh admission behavior audit`) = `SUCCESS`;
- job `98922083704` (`Deterministic admission-policy audit`) = `SUCCESS`.

The focused unit suite also enforces:

- dynamic RTTI/vptr resolution and absence of historical absolute RTTI/vptr authorities (`0x30c2250`, `0x30c3488`, `0x30b6ba0`, `0xd28890`, `0x4d7dc0`);
- exact `object + 0x60` member authority only;
- `/proc/<pid>/mem` opened with `os.O_RDONLY | os.O_CLOEXEC`;
- bounded QString length/payload mapping checks;
- no ptrace, process-memory write, environment read, gdb, uprobe, tracefs, xdotool or pyautogui surface;
- no arbitrary `OTHER` text/hash retention;
- unconditional `in_game_claimed=false` and `semantic_promotion_performed=false`.

## Runtime status

No live qualification was executed by PR #756. The pull-request live job remained skipped. Therefore:

- `LOGIN_SCREEN`: not observed by #756;
- `CHARACTER_SELECT`: not observed by #756;
- `WORLD`: not observed by #756;
- `WORLD_EXIT`: not observed by #756;
- causal validation: `NOT_PERFORMED`;
- semantic promotion: `NOT_PERFORMED`.

The next operation, only after final exact-head checks and trusted-main merge, is a fresh runtime admission followed by one continuous owner-driven phase traversal.
