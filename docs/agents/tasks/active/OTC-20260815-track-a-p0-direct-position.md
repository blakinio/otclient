---
task_id: OTC-20260815-track-a-p0-direct-position
status: waiting
agent: ChatGPT
session_id: chatgpt-p0-static-re-20260815-1707
session_role: researcher
session_rotation_count: 2
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
  - RUNTIME lane / Draft PR #303 for a bounded live exact-client observation window
blocks:
  - live semantic validation requires a bounded exact Track A in-game process owned by RUNTIME; P0 will not duplicate login/restart paths
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
code_bearing_head: a3068a6a9460525cb1946186cf439caf7832e176
invocation_started_at: 2026-08-15T17:07:00+02:00
last_progress_at: 2026-08-15T17:14:00+02:00
lease_released_at: 2026-08-15T17:14:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: static-accessor-re
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
claim_check: rotation 2 used only P0 owned paths while independently active RUNTIME #303 remained untouched
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260815-exact-elf-static-tplayerdata.md
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260815-player-position-static-graph.md
next_action: after RUNTIME supplies a bounded live exact-client in-game process window, run the existing passive typed-owner/provider probe and prioritize the exact playerPosition code site 0x8367c1; only if passive repeated reads remain insufficient may the one previously-proven adjacent step plus inverse be considered after rechecking RUNTIME authority
---

# Objective

Recover and causally validate a direct standalone authoritative player-position read for the exact official native Linux client. This task remains distinct from the already accepted viewport-center derivation. Research output is Draft-only; canonical promotion belongs to coordinator PR #300.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
TPlayerData_primary_vptr: 0x308ca70
```

# Acceptance gate

- [x] exact SHA/size fenced before build-specific offsets are used;
- [x] candidate search provenance restricted to typed/structurally justified owners rather than a blind global XYZ scan;
- [ ] negative controls reject camera/map-origin/viewport/copy candidates where distinguishable;
- [ ] at least two live read observations demonstrate correct value stability/change semantics;
- [ ] direct value independently compared with structural world evidence;
- [ ] client/process survives live observation and any authorized reversible stimulus is restored;
- [x] direct-read hypothesis remains explicitly distinct from the DERIVED viewport-center coordinate;
- [x] no unrelated P0 read is promoted incidentally;
- [ ] fresh PID/relogin stability is proven;
- [ ] exact final-head CI terminal green before final Draft handoff.

# Side-effect budget

Current usage: **zero process-memory writes, zero movement stimuli, zero gameplay actions, zero live attach in rotation 2**. If movement is later strictly necessary, only one previously-proven adjacent step plus inverse is permitted after immediately rechecking RUNTIME ownership. No attack, use, move-object, market, trade, forge or currency effects.

# Retained runtime prerequisite evidence — FACT

Run `31883422477` / job `95009054487` executed on `synology-otclient-01`, passed the exact client executable/size/SHA fence and proved no live exact Track A client existed at that time:

```text
TRACK_A_P0_PIDFILE_STALE=true
TRACK_A_P0_DISCOVERED_EXACT_TRACK_CLIENTS=0
TRACK_A_P0_ERROR=expected_one_live_exact_track_client
```

The job failed closed before `/proc/<pid>/mem` was opened. Direct XYZ therefore remained `INCONCLUSIVE/UNKNOWN`, not disproven.

# Exact ELF structural provenance — FACT

Prior successful static run `31883967070` / job `95010405800` established the exact `TPlayerData` vtable/type neighborhood. Rotation 2 then extended the same side-effect-free path in run `31892019505` / job `95029600292` at code-bearing head `a3068a6a9460525cb1946186cf439caf7832e176`; the static job, `luacheck` and `cppcheck` all completed `SUCCESS`, while live jobs were explicitly skipped.

The exact primary property anchor is:

```text
playerPosition literal: 0x1cdde3f
unique bounded code site: 0x8367c1 -> 0x1cdde3f (RIP-relative LEA)
```

This corrects the earlier transcription `0x1cddd3f`.

Relocation-backed type-name relationships retained for live discrimination:

```text
0x3089b78 -> 0x1cddd20  TWorldMapRenderProvider
0x308b598 -> 0x1ce1b60  TWorldMapViewport
0x308b5b0 -> 0x1ce1ba0  IPlayerDataProvider
0x308b5c0 -> 0x1ce1bd0  TPlayerData
```

The local primary-property neighborhood contains `%1,%2,%3`, `playerPosition`, `characterName`, `worldName` and render/status properties. A second substring at `0x1d2a937` is part of `playerPositionChanged` in a Cyclopedia-map context (`onPlayerPositionChanged`, `TWorldMapCoordinate`, `onPlayerPositionWasUpdated`) and is retained as a negative/control context rather than a direct-field claim.

The task-local GDB exists but the rotation-2 bounded static disassembly invocation lacked the toolroot runtime library path and failed on `libpython3.12.so.1.0`. This is a tooling detail only; no live attach occurred, and no method/member offset is invented from the failed disassembly.

Durable evidence: `docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260815-player-position-static-graph.md`.

# Historical derived movement — DERIVED only

```text
(32546,32510,7) -> (32546,32509,7) -> (32546,32510,7)
```

This remains accepted viewport/world structural evidence only. It is not a direct player field.

# Classification

### FACT

- exact client / `TPlayerData` structural provenance is reproducible;
- `playerPosition` primary literal and a unique bounded code site are now exact-file anchored;
- provider/worldmap/TPlayerData RTTI relationships are exact-relocation anchored;
- Cyclopedia `playerPositionChanged` is separately identifiable as a control context;
- no live or gameplay side effect was used to obtain these facts.

### INFERENCE

The next live discriminator should prioritize storage/provider paths associated with `0x8367c1` and `IPlayerDataProvider`/`TPlayerData` before broader typed-owner candidate enumeration.

### UNKNOWN / INCONCLUSIVE

Direct authoritative player XYZ is still **UNKNOWN / INCONCLUSIVE**. Backing member/accessor offset, encoding, causal semantics, negative-control discrimination and fresh PID/relogin stability require live exact-client observation.

# Resume condition

RUNTIME / Draft PR #303 is independently active and has already cleared its workflow-quality PR CI gate. Resume P0 only when that lane provides a bounded live exact Track A in-game observation window or releases a correctly-owned integration mechanism that lets this read-only probe execute while its client is alive. Do not duplicate RUNTIME login/restart ownership.
