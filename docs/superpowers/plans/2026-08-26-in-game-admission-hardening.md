# In-Game Admission Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent any guarded movement `READY`/`COMMIT` and any direct causal-worker dispatch when the canonical official-client runtime does not have proven `IN_GAME` state.

**Architecture:** Add a movement-specific semantic admission check inside the canonical `guarded-dispatch` path before `READY`, using only canonical registration/probe state. Add the same fail-closed requirement inside the player-state causal worker as defense in depth. Do not invent a new `IN_GAME` producer: current adoption evidence remains `UNKNOWN`, so movement stays blocked until a separately proven `IN_GAME` source exists.

**Tech Stack:** Python 3 `unittest`, GitHub Actions, Track A canonical transition/lease/probe infrastructure.

**Spec:** `docs/agents/tasks/active/OTC-20260826-in-game-admission-hardening.md`

## Global Constraints

- Base/source of truth: protected `main@8a9315e1cd621a5b868010deeec2578266547663` or newer only after explicit re-resolution.
- `runtime_access:none`; no official-client observation, credentials, login/relogin, restart, character selection, GUI/gameplay input, process-memory write, or client mutation.
- `UNKNOWN`, `LOGIN`, `CHARACTER_SELECT`, or `DISCONNECTED` must never permit a movement `READY`.
- Current `existing_runtime_adoption_v1` evidence is not `IN_GAME` authority; `BRIDGE_3_OF_3*` and `NO_STRUCTURAL_BRIDGE` remain unproven.
- No semantic-promotion claim and no physical retry are part of this task.
- TDD: failing regression before production change; exact-head tests/audit/CI before merge.

---

### Task 1: Reproduce the pre-READY admission bug

**Files:**
- Modify: `.github/scripts/test_tibia_official_client_re_canonical_live_transition.py`
- Test: `.github/scripts/test_tibia_official_client_re_canonical_live_transition.py`

**Interfaces:**
- Consumes: `_guarded_dispatch(...)`, canonical `runtime-registration.json` and fresh probe manifest.
- Produces: regression proving a `move` request with `state='UNKNOWN'` must fail before `_emit_guarded_ready()`.

- [ ] **Step 1: Write the failing test**

Add a focused test that supplies matching canonical registration/manifest with `state='UNKNOWN'`, a valid one-tile `move` request, and spies on `_emit_guarded_ready` / `_run_guarded_worker`.

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 .github/scripts/test_tibia_official_client_re_canonical_live_transition.py`

Expected RED: the current implementation reaches `_emit_guarded_ready()` instead of raising the new movement admission error.

- [ ] **Step 3: Implement minimal canonical gate**

Add a small helper invoked after each fresh `_probe_reg(...)` that, for `request['kind'] == 'move'`, requires both registration and manifest `state == 'IN_GAME'`. Reject before `READY` otherwise. Do not weaken `_manifest()` adoption semantics or manufacture `IN_GAME`.

- [ ] **Step 4: Run test to verify it passes**

Run the canonical transition suite and confirm the new UNKNOWN regression passes with no existing regression failures.

- [ ] **Step 5: Commit**

Commit the canonical pre-READY gate and its regression as one TDD slice.

### Task 2: Harden the causal worker against direct/bypassed invocation

**Files:**
- Modify: `.github/scripts/test_tibia_official_client_re_player_state_causal_worker.py`
- Modify: `.github/scripts/tibia-official-client-re-player-state-causal-worker.py`

**Interfaces:**
- Consumes: `validate_registration(data)` used by `execute_once()` and external preflight callers.
- Produces: worker refuses `UNKNOWN` registration before tool/read/dispatch; test fixtures use an explicit `IN_GAME` registration shape for positive unit paths.

- [ ] **Step 1: Write the failing test**

Add a regression asserting the exact retry-4-style `existing_runtime_adoption_v1` registration with `state='UNKNOWN'` is rejected by `validate_registration()` and `execute_once()` returns `REFUSED/effect_count=0` without calling the dispatch function.

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 .github/scripts/test_tibia_official_client_re_player_state_causal_worker.py`

Expected RED: current `validate_registration()` accepts `UNKNOWN`.

- [ ] **Step 3: Implement minimal worker gate**

Change the semantic fence from accepting `UNKNOWN` to requiring `IN_GAME`. Preserve exact PID/XRes/client/runtime-locator checks. Current adoption-v1 manifests remain incapable of proving `IN_GAME` under canonical probe policy, so real movement remains fail-closed until a future trusted proof path exists.

- [ ] **Step 4: Run test to verify it passes**

Run the worker, timeout-contract and dispatch-boundary suites. Confirm no dispatch occurs for UNKNOWN.

- [ ] **Step 5: Commit**

Commit the worker defense-in-depth and test adjustments.

### Task 3: Cross-boundary validation and durable evidence

**Files:**
- Create: `docs/agents/evidence/OTC-20260826-in-game-admission-hardening/root-cause-and-repair.md`
- Modify: `docs/agents/tasks/active/OTC-20260826-in-game-admission-hardening.md`

**Interfaces:**
- Consumes: Tasks 1-2 implementation and retry-4 evidence.
- Produces: durable root-cause proof, exact tests/runs, and terminal safety statement.

- [ ] **Step 1: Run focused suites**

Run canonical transition, Kasm adoption probe, player-state worker, causal timeout-contract, causal dispatch-boundary, Track A governance, and `git diff --check`.

- [ ] **Step 2: Verify the negative policy explicitly**

Prove with tests that `UNKNOWN` movement cannot reach `READY`, and direct worker invocation cannot reach dispatch.

- [ ] **Step 3: Record evidence**

Document the proven data-flow bug: adoption probe `UNKNOWN` -> canonical guarded-dispatch identity-only fence -> worker accepted `UNKNOWN`; record the two-layer repair and explicitly state that no new `IN_GAME` producer was invented.

- [ ] **Step 4: Independent audit and exact-head CI**

Open a PR, perform a fresh exact-head review, require Track A governance and repository `CI / Required` PASS.

- [ ] **Step 5: Merge/archive/release**

Merge only the audited exact head, archive the task, release ownership, finalize archive metadata, and verify active task removal on final `main`.
