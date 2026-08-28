---
task_id: OTC-20260828-game-window-state-qualification
status: implementing
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: reverse_engineering_runtime
phase: runtime_workflow_prepared
branch: work/OTC-20260828-game-window-state-readonly-admission
base_branch: main
base_main: 76515d605f7a76eebe25af0fd0dd68781f086f88
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
  - PR #755 merged bounded reader/workflow preparation
  - PR #754 merged canonical current-client fence repair
blocks:
  - LIVE_GAME_WINDOW_STATE_CAUSAL_VALIDATION
---

# Objective

Qualify the smallest fail-closed read-only runtime reader for exact-current `tibia::gamewindow::TGameWindowController::gameWindowState`, dynamically resolving the current RTTI/vptr and reading only the statically proven 24-byte `QString` member at `object + 0x60` plus its bounded payload.

This repository checkpoint intentionally remains `runtime_access: none`. No current live target is claimed here and no `target_uniqueness: PROVEN` is fabricated from historical evidence. The trusted-main runtime workflow must perform a fresh admission transition and persist/emit a complete `runtime_access: read_only` record with `target_uniqueness: PROVEN` before it opens `/proc/<pid>/mem`.

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

The merged reader provides:

- dynamic exact-current RTTI/vptr resolution;
- bounded single-heap object scan with exact object uniqueness requirement;
- direct 24-byte backing `QString` read at the proven member offset;
- small bounded UTF-16 payload validation;
- `EMPTY` / `INGAME` / `OTHER` / fail-closed `UNKNOWN` semantics;
- sanitized continuous state-change and heartbeat JSONL;
- no arbitrary `OTHER` text retention;
- `in_game_claimed=false` and `semantic_promotion_performed=false` unconditionally.

PR #754 advanced the trusted exact-client fence to the same build used by the reader. PR #756 aligns the live workflow with `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`: repository state remains `none`; a fresh live invocation must explicitly transition to `read_only`, while canonical Gate A, generation rebind and Gate B remain `NOT_APPLICABLE` for that observation.

# Fresh live admission before process-memory observation

The trusted-main live workflow must fail closed unless all of the following are freshly true before opening `/proc/<pid>/mem`:

- this repository task checkpoint still declares `runtime_access: none`, no runtime owner/namespace/target claim, `mutation_authorized: false`, and all canonical control gates `NOT_APPLICABLE`;
- the authoritative canonical registration is present, exact-fenced to `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`, and provides a valid Docker runtime locator plus exact PID/start identity;
- no active canonical lease belongs to another task;
- a fresh bounded inventory across all running Docker containers finds exactly one `client` candidate, exact-fenced to the current build, and it is exactly the registered PID/start/container;
- only after that proof the workflow persists and validates a secret-free runtime admission record containing `runtime_access: read_only`, this task as `runtime_owner_task`, explicit namespace `track-a-game-window-state-validation`, canonical control gates `NOT_APPLICABLE`, `target_uniqueness: PROVEN`, and `mutation_authorized: false`;
- only after that complete admission record validates may the reader open `/proc/<pid>/mem` read-only.

Any missing/ambiguous registration, ownership conflict, stale locator, stale PID/start, mismatched executable, additional candidate, unreadable candidate, or invalid emitted admission fails closed before process-memory observation.

# Runtime acceptance

The owner manually performs the UI transitions; the agent performs no GUI/input/login/character/gameplay action. One continuous logger remains active across the sequence:

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

No repository/static prerequisite remains after #754 and #755. Live observation remains refused until #756 is trusted-main GREEN and a live invocation freshly persists/validates the read-only admission record described above. Owner interaction is not required until the continuous logger is actually ready to start from `LOGIN_SCREEN`.

next_action: finish PR #756 exact-head verification and merge if protected-main policy permits; then perform fresh trusted-main read-only admission and engage the owner only for the manual LOGIN_SCREEN -> CHARACTER_SELECT -> WORLD -> WORLD_EXIT sequence.
