---
task_id: OTC-20260828-game-window-state-qualification
status: implementing
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: reverse_engineering_runtime
phase: repo_static_green
branch: feat/OTC-20260828-game-window-state-qualification
base_branch: main
base_main: 6a6a6a7a8c39fd017993ef7db1179872dc6bc521
created: 2026-08-28T16:20:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
runtime_access: none
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
credentials_allowed: false
login_allowed: false
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
physical_action_budget: 0
physical_action_count: 0
implementation_authorized: true
owned_paths:
  - .github/scripts/track_a_game_window_state_qualification.py
  - .github/scripts/test_track_a_game_window_state_qualification.py
  - .github/scripts/test_track_a_game_window_state_workflow_contract.py
  - .github/workflows/track-a-game-window-state-qualification.yml
  - docs/agents/tasks/active/OTC-20260828-game-window-state-qualification.md
  - docs/agents/evidence/OTC-20260828-game-window-state-qualification/**
modules_touched:
  - track-a-read-only-runtime-research
reuses:
  - .github/scripts/track_a_current_world_entered_anchor.py
  - .github/scripts/track_a_current_world_entered_durable_state.py
  - .github/scripts/track_a_current_qt_world_snapshot.py
depends_on:
  - PR #750 merged exact-current gameWindowState static proof
  - PR #754 canonical current-client fence repair before any live observation
blocks:
  - LIVE_GAME_WINDOW_STATE_CAUSAL_VALIDATION
---

# Objective

Build the smallest fail-closed read-only runtime qualification reader for exact-current `tibia::gamewindow::TGameWindowController::gameWindowState`, dynamically resolving the current RTTI/vptr and reading only the statically proven 24-byte `QString` member at `object + 0x60` plus its bounded payload.

The repository/static successor may be implemented and merged with `runtime_access: none`. It must not observe or touch a live official client from this branch. A separate fresh trusted-main admission is required before the merged runtime workflow may execute.

# Trusted static input

Merged PR #750 is the current source of static semantic evidence for official Linux client `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`:

- `TGameWindowController::gameWindowState : QString`, property index `2`;
- `gameWindowStateChanged`, signal index `4`;
- `QMetaObject::ReadProperty` dispatch (`Call == 1`);
- backing member `+0x60`, width `24` bytes;
- exact known semantic state `INGAME`, length `6`, semantic UTF-8 SHA-256 `c2fffc542eee743e8ff96c90698a369f8d0b075fe22bb411fca5b61ba8373d1e`;
- exact empty semantic state SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Historical absolute RTTI/vptr RVAs are evidence only and are not embedded in the reader. Runtime resolution reuses exact-current ELF relocation/RTTI logic.

# Repository/static qualification

TDD and hosted verification evidence is recorded at:

`docs/agents/evidence/OTC-20260828-game-window-state-qualification/repo-static-qualification.md`

The verified implementation provides:

- dynamic exact-current RTTI/vptr resolution;
- bounded single-heap object scan with exact uniqueness requirement;
- direct 24-byte backing `QString` read at the proven member offset;
- small bounded UTF-16 payload validation;
- `EMPTY` / `INGAME` / `OTHER` / fail-closed `UNKNOWN` semantics;
- sanitized continuous state-change and heartbeat JSONL;
- no arbitrary `OTHER` text retention;
- `in_game_claimed=false` and `semantic_promotion_performed=false` unconditionally;
- trusted-main live workflow gates for `runtime_access: read_only`, Gate A, required generation rebind, Gate B, target uniqueness, current-client fence, canonical registration and exact PID/start identity.

# Runtime acceptance after trusted-main merge

A later live qualification is valid only when a fresh admitted exact process is proven unique and non-conflicting. The owner manually performs the UI transitions; the agent performs no GUI/input/login/character/gameplay action.

Required causal phases on one process:

```text
LOGIN_SCREEN        != INGAME
CHARACTER_SELECT    != INGAME
WORLD               == INGAME
WORLD_EXIT          != INGAME
```

The qualification run must preserve:

```text
IN_GAME_CLAIMED=false
semantic_promotion_performed=false
```

Only after causal PASS and separate independent exact-head review may a later promotion PR change canonical `IN_GAME` semantics.

# Current blocker

PR #754 is the live trusted-base prerequisite for the current exact-client canonical fence. Until that repair reaches trusted `main`, this task remains repository-only and any live observation is refused.

The task intentionally remains `runtime_access: none`; no owner interaction is required yet.

next_action: complete fresh exact-head PR #755 verification and merge the repository/static successor if protected-main policy permits; then finish the #754 trusted-base fence repair and create a separate fresh read-only runtime admission before engaging the owner.
