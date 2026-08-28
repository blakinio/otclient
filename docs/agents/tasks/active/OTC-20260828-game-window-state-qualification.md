---
task_id: OTC-20260828-game-window-state-qualification
status: implementing
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: reverse_engineering_runtime
phase: tdd_red
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

Historical absolute RTTI/vptr RVAs are evidence only and must not be embedded in the reader. Runtime resolution must reuse exact-current ELF relocation/RTTI logic.

# TDD contract

1. RED first: focused hosted unit tests require the missing qualification reader and its fail-closed helpers.
2. GREEN: add only the minimal reader needed to satisfy the tests.
3. Add a separately tested runtime-workflow contract; PR execution remains hosted/repository-only.
4. Before readiness: `py_compile`, focused unit tests, YAML parse, workflow contract, `git diff --check`, Track A governance, stale-RVA/forbidden-surface scan, and exact changed-scope review.

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

PR #754 is the live trusted-base prerequisite for the current exact-client canonical fence. Its hosted RED is already proven; until that repair reaches trusted `main`, this task remains repository-only and any live observation is refused.

next_action: obtain hosted RED for the focused missing game-window-state qualification reader before adding production implementation.
