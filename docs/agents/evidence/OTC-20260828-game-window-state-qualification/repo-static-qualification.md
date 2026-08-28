# OTC-20260828 gameWindowState qualification — repository/static evidence

This evidence is repository-only. No official-client runtime was observed from PR #755 and no live semantic promotion is claimed.

## Source of truth and scope

- Fresh protected `main` at task start: `6a6a6a7a8c39fd017993ef7db1179872dc6bc521` (merged PR #750).
- Successor PR: #755, `feat/OTC-20260828-game-window-state-qualification`.
- Live trusted-base prerequisite: draft PR #754 must update the canonical exact-client fence before any qualification run.
- Runtime authority during all evidence below: `runtime_access: none`, `mutation_authorized: false`.

## TDD evidence

### Reader RED

PR #755 exact head `1298c45b0b8f617b13185d323ddc3f14367e62aa`:

- workflow run `33180004226`;
- job `98878538440`;
- expected failure: `GAME_WINDOW_STATE_QUALIFICATION_IMPLEMENTATION_MISSING`.

The production reader did not exist at this point.

### Reader GREEN

After adding the minimal reader and correcting only a test-loader defect, PR #755 exact head `fb60b9bddc953dc5ba95e66d3a70800b7efc2b08` produced hosted focused PASS in job `98879368447`.

### Runtime-workflow RED

PR #755 exact head `edf7ff6555431d940d8b68b22f9386e10f00a052`:

- workflow run `33180486179`;
- job `98880158316`;
- all 16 reader unit tests passed first;
- expected workflow-contract failure: `WORKFLOW_CONTRACT_MISSING:issue_comment:`.

### Full-admission gate RED

Review then found that registration/PID/fence checks alone were insufficient for fresh live admission. A focused contract was added first.

PR #755 exact head `c7b96959887850205896f44d83bd20e4ff3f74d3`:

- workflow run `33181095725`;
- job `98882169128`;
- all 16 reader unit tests passed first;
- expected failure: `WORKFLOW_CONTRACT_MISSING:GATE_A_REQUIRED=PASS`.

### Repository/static GREEN

PR #755 exact head `73260d05405dda4209dc7f10b2610b1dc88b3a9a`:

- `Track A game window state qualification` run `33181191504`: `SUCCESS`;
- focused contract job `98882499693`: `SUCCESS`;
- `Track A agent runtime governance` run `33181191572`: `SUCCESS`;
- `CI` run `33181191530`: `SUCCESS`;
- live qualification job on the pull-request event: `SKIPPED` as required.

The focused job executes:

- `py_compile` for the reader and focused tests;
- 16 focused reader unit tests;
- runtime-workflow contract;
- YAML parse;
- `git diff --check`.

The workflow contract additionally requires a later trusted-main live task to prove `runtime_access: read_only`, Gate A PASS, generation rebind PASS or NOT_REQUIRED, Gate B PASS, target uniqueness PROVEN, exact canonical current-client fence PASS, exact PID/start identity and canonical registration before `/proc/<pid>/mem` can be opened.

## Bounded reader contract

`.github/scripts/track_a_game_window_state_qualification.py`:

- dynamically resolves the exact-current primary vptr from RTTI/ELF relocations through existing Track A resolvers;
- scans only a bounded single `[heap]` mapping for the resolved vptr and requires exactly one `TGameWindowController`;
- re-verifies PID start ticks, executable identity and object vptr around observation;
- opens `/proc/<pid>/mem` with `O_RDONLY | O_CLOEXEC` only;
- reads exactly the statically proven 24-byte `QString` member at `object + 0x60` and at most 32 UTF-16 code units from its validated readable payload mapping;
- classifies only `EMPTY`, `INGAME`, `OTHER`, or fail-closed `UNKNOWN`;
- retains known text/hash only for the known `INGAME` or empty semantic values; arbitrary `OTHER` text is not retained;
- emits only sanitized state-change/heartbeat JSONL with `in_game_claimed=false` and `semantic_promotion_performed=false`;
- contains no historical absolute RTTI/vptr authority.

## Live status

`LIVE_GAME_WINDOW_STATE_CAUSAL_VALIDATION` is **not performed** by this evidence.

No evidence in this file establishes canonical `IN_GAME`. The required causal sequence remains:

```text
LOGIN_SCREEN        != INGAME
CHARACTER_SELECT    != INGAME
WORLD               == INGAME
WORLD_EXIT          != INGAME
```

Owner interaction is not requested until PR #754 is trusted-main GREEN, PR #755 is merged, and a separate fresh read-only runtime admission has proven all gates for one exact process.
