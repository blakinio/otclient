---
task_id: OTC-20260815-track-a-p0-direct-position
status: active
agent: ChatGPT
session_id: chatgpt-p0-static-re-20260815-1405
session_role: researcher
session_rotation_count: 1
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: runtime-research
phase: p0-direct-player-position
branch: research/OTC-20260815-track-a-p0-direct-position
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-p0-direct-position
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p0-direct-position.md
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/**
  - .github/workflows/tibia-official-client-re-p0-direct-position.yml
  - .github/scripts/tibia-official-client-re-p0-direct-position.py
depends_on:
  - exact-build structural world evidence retained by coordinator PR #300
  - accepted read-only bridge evidence from PR #283 as read-only reference only; no ownership of its paths
  - RUNTIME lane / Draft PR #303 for a bounded live exact-client observation window when runtime state must be reacquired
blocks:
  - live semantic validation still requires a bounded exact Track A in-game process owned by RUNTIME; P0 will not duplicate login/restart paths
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
invocation_started_at: 2026-08-15T14:05:00+02:00
last_progress_at: 2026-08-15T14:05:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: static-re
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 1
stall_warnings: 0
claim_check: passed against open Draft PR #302, exact main@8fca1c3 and non-overlapping P0 owned paths; RUNTIME PR #303 is separately active and will not be mutated
last_checkpoint: live-runtime prerequisite evidence committed at 4a1700a534234f6a25e955e61855d56b78d056e6 after self-hosted runner recovery and zero-live-process discrimination
next_action: use the exact fenced ELF already present on synology-otclient-01 for side-effect-free static TPlayerData RE while RUNTIME #303 independently reacquires live state; do not share its branch/worktree or duplicate login/restart behavior
---

# Objective

Recover and causally validate a direct standalone authoritative player-position read for the exact official native Linux client. This task is intentionally distinct from the already accepted viewport-center derivation.

# Dispatch contract

```yaml
TASK_ID: OTC-20260815-track-a-p0-direct-position
TASK_RECORD: docs/agents/tasks/active/OTC-20260815-track-a-p0-direct-position.md
PROJECT_LANE: otclient
LANE: P0-STATE
BASE_MAIN: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
BRANCH: research/OTC-20260815-track-a-p0-direct-position
WORKTREE: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-p0-direct-position
OWNED_PATHS:
  - docs/agents/tasks/active/OTC-20260815-track-a-p0-direct-position.md
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/**
  - .github/workflows/tibia-official-client-re-p0-direct-position.yml
  - .github/scripts/tibia-official-client-re-p0-direct-position.py
DEPENDENCIES:
  - coordinator-retained exact-build structural map-strip movement evidence
  - PR #283 bridge/profile evidence is reference-only and remains separately owned
  - RUNTIME lane owns login/restart/relogin execution needed to create a fresh live process
```

Research output is DRAFT-ONLY. Canonical promotion belongs to coordinator PR #300.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Starting evidence

### FACT

- exact-build live structural map observations were produced historically on `synology-otclient-01`;
- a forward/inverse transition was structurally observed and restored;
- exact-profile type leads include `TPlayerData`, `TGameserverGameSession`, `TPlayerProtocolMessageHandler`, `TGameClient` and storage types from PR #283 evidence;
- exact-build `TPlayerData` primary vptr offset used by the bounded reproducer is `0x308ca70`.

### DERIVED

`(32546,32510,7) -> (32546,32509,7) -> (32546,32510,7)` is the accepted viewport-geometry-derived player transition for the historical exact-build run.

### UNKNOWN

A direct standalone player-position member/object read is not yet proven.

# Hypothesis

A stable exact-build object reachable from `TPlayerData`, the game session/client graph, or another structurally justified owner contains or references authoritative absolute player XYZ and can be independently correlated against structural world geometry without interpreting arbitrary memory triples as position.

# Required discrimination

The experiment must distinguish:

1. direct authoritative member/reference candidate that tracks structural position;
2. cached/viewport/camera/map-origin value that correlates but is not player state;
3. coincidental XYZ-shaped memory;
4. no stable direct position exposed by the tested graph.

# Acceptance gate

- [x] exact SHA/size is fenced before build-specific offsets are used by the workflow;
- [x] candidate search provenance is restricted to the typed `TPlayerData` owner and one pointer hop rather than a blind global XYZ scan;
- [ ] negative controls reject camera/map-origin/viewport/copy candidates where distinguishable;
- [ ] at least two read observations demonstrate correct value stability/change semantics; if movement is used, only one bounded reversible step plus inverse is allowed;
- [ ] direct value is independently compared with structural map/world evidence;
- [ ] process/client survives the observation and, if a reversible stimulus is used, returns to the precondition state;
- [x] the direct-read hypothesis remains explicitly distinct from the existing DERIVED viewport-center coordinate;
- [x] no HP/mana/identity or other P0 read is promoted incidentally without its own evidence;
- [ ] exact final-head CI is terminal before Draft handoff.

# Side-effect budget

Prefer read-only runtime observation. If a state transition is strictly necessary for discrimination, use at most one previously proven reversible adjacent movement plus inverse and verify restoration. Do not use attack, use, move-object, market, trade, forge or currency effects.

Current side-effect usage for this task: **zero process-memory writes, zero movement stimuli, zero gameplay actions**.

# Current checkpoint

## FACT — workflow and runner recovery

- Draft PR #302 remains Draft-only on `research/OTC-20260815-track-a-p0-direct-position` against `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`.
- The P0 reproducer is read-only and resolves the exact-build `TPlayerData` owner from primary vptr offset `0x308ca70`; it scans typed owner objects and one pointer hop for plausible position-shaped fields and keeps structural strip data as an independent oracle.
- Original run `31880617510` was stale in the serialized runtime queue. Its exact identity was fenced before a task-local recovery preflight cancelled only that run; it is no longer the blocker.
- Commit `6e1af63176b3451da0e82fb2751e5c5f50658c49` aligned the P0 runner selector with the labels proven on historical successful `synology-otclient-01` jobs.
- Run `31883178675` created and executed self-hosted job `95008500800` on runner id `21`, `synology-otclient-01`. The first actionable failure was historical PID `18102` from the shared PID file no longer existing.

## FACT — live-process discriminator

- Commit `29973501a14aefd14ef887161014190d270d5c0c` added a read-only stale-PID fallback that searches `/proc/[0-9]*` for processes matching both the exact executable path and `OTCLIENT_TIBIA_RE_TRACK=official-client-re`.
- Run `31883422477` / self-hosted job `95009054487` executed that discriminator on `synology-otclient-01` and reported:

```text
TRACK_A_P0_PIDFILE_STALE=true
TRACK_A_P0_DISCOVERED_EXACT_TRACK_CLIENTS=0
TRACK_A_P0_ERROR=expected_one_live_exact_track_client
```

- The job failed closed with exit code `3` before any `/proc/<pid>/mem` read because no eligible live process existed.
- Companion `luacheck` and `cppcheck` jobs for run `31883422477` completed successfully.
- Durable evidence is recorded in `docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260815-live-runtime-prerequisite.md`.

## INCONCLUSIVE / UNKNOWN

- Direct authoritative player XYZ remains **INCONCLUSIVE/UNKNOWN**, not disproven. The live typed-owner observation prerequisite was absent.
- The direct member offset/access path, lifetime, semantic change behavior and fresh-PID/relogin stability are unknown.
- Negative discrimination against camera/map-origin/viewport copies cannot be performed until a live typed-owner candidate exists.

# Parallel static RE lane — 2026-08-15 14:05 +02

### FACT

- RUNTIME / PR #303 is separately active under `session_id: chatgpt-runtime-researcher-20260815-1405`; P0 must not mutate or share that branch/worktree.
- The P0 self-hosted probe already proved the exact fenced ELF exists on `synology-otclient-01` even when no eligible live process exists.

### PLAN

Use only the exact on-runner ELF for static, side-effect-free analysis anchored at the relocation-backed `TPlayerData` primary vptr offset `0x308ca70`. The analysis may inspect ELF sections/relocations, strings, disassembly and code/data references that structurally reach the TPlayerData vtable/type neighborhood. It must not treat arbitrary coordinate-shaped immediates as semantic player position and must not promote runtime semantics without live validation.

# Real stop condition

Live semantic validation still requires a fresh exact Track A in-game process. Creating/logging in/restarting that process is owned by the separate RUNTIME lane / Draft PR #303, not by this P0 task. P0 may continue side-effect-free static exact-build RE in parallel, but it may not duplicate RUNTIME login/restart behavior.

# Resume condition

When RUNTIME ownership provides a bounded live exact-client observation window, first perform passive typed-owner reads using any statically narrowed candidate offsets/access paths. Use the one-step-plus-inverse movement allowance only if passive repeat observations cannot discriminate a candidate and RUNTIME ownership has been rechecked immediately beforehand.

# Deliverable

Draft PR only, containing the task-scoped reproducer/evidence and explicit read-gate classification. Do not mutate PR #283 bridge paths, PR #303 RUNTIME paths, or any Track B path/runtime.
