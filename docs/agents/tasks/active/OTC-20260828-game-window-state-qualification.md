---
task_id: OTC-20260828-game-window-state-qualification
status: implementing
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: reverse_engineering_runtime
phase: blocked_fail_closed_current_target_mismatch
branch: docs/OTC-20260828-game-window-state-current-target-blocker
base_branch: main
base_main: 1d9e69ba1afb369dbef911771d240a9633ff6798
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
  - PR #772 merged canonical exact-current fence reconciliation PASS and authority release
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

PR #754 advanced the trusted exact-client fence to the same build used by the reader. PR #756 aligned the live workflow with `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`: repository state remains `none`; a fresh live invocation must explicitly transition to `read_only`, while canonical Gate A, generation rebind and Gate B remain `NOT_APPLICABLE` for that observation.

PR #772 later recorded a successful metadata-only canonical client-fence reconciliation and released its temporary `canonical_recovery` authority. The exact-current registration fence remained `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`, with semantic registration state `UNKNOWN`.

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

# Current terminal blocker

After PR #772 returned canonical recovery authority to `runtime_access: none`, a fresh owner trigger comment `5456931858` on PR #756 invoked memory-free preflight run `33204467524`, job `98961872769`, on `synology-otclient-01` at exact trusted main `1d9e69ba1afb369dbef911771d240a9633ff6798`.

The preflight freshly passed:

- trusted-main runtime-none checkpoint and current exact client fence;
- bounded qualification command validation;
- canonical registration structure/exact fence and current ownership check.

It then failed closed in `Re-prove global unique exact target` with exact error:

`REGISTERED_TARGET_NOT_CURRENT_UNIQUE_CANDIDATE`

The inventory gate tests singleton candidate count before this error can be emitted. Therefore the run proved exactly one exact-fenced official-client candidate was present, but the candidate did not match the canonical registration's current locator/PID/start identity. The registration supplied to that step was `otclient-track-a-kasmvnc / 1af4af4d67f5 / pid 13947 / start 51652120`.

The workflow stopped before fresh read-only admission, admission revalidation, logger READY reporting, resolver construction and every process-memory observation step. No replacement live identity is inferred or retained as authority.

Durable current execution evidence:

`docs/agents/evidence/OTC-20260828-game-window-state-qualification/20260828-live-preflight-current-target-blocker.md`

Canonical-live governance forbids ad-hoc editing of `runtime-registration.json`. Owner manual UI interaction is **not** requested because the logger is not READY.

Terminal result:

`LIVE_GAME_WINDOW_STATE_CAUSAL_VALIDATION=BLOCKED_FAIL_CLOSED`

`BLOCKER=REGISTERED_TARGET_NOT_CURRENT_UNIQUE_CANDIDATE`

`PROCESS_MEMORY_OBSERVATION_PERFORMED=false`

`READ_ONLY_ADMISSION_CREATED=false`

`IN_GAME_CLAIMED=false`

`semantic_promotion_performed=false`

The task remains `runtime_access: none`; the failed preflight created no reusable runtime authority that requires release.

next_action: under a separate fresh canonical-live governance admission, reconcile or re-admit the authoritative registration to the exact currently unique official-client container/PID/start identity without ad-hoc metadata edits; release that temporary authority; then rerun a new `PREFLIGHT_GAME_WINDOW_STATE_QUALIFICATION`. Only a fresh READY result may engage the owner for `LOGIN_SCREEN -> CHARACTER_SELECT -> WORLD -> WORLD_EXIT`.
