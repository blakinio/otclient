---
task_id: OTC-20260815-track-a-p0-direct-position
status: waiting
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
  - RUNTIME lane / Draft PR #303 for a bounded live exact-client observation window
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
code_bearing_head: eec9f6fcb065dd7762fa098ad78d1661b0060bd3
invocation_started_at: 2026-08-15T14:05:00+02:00
last_progress_at: 2026-08-15T14:13:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: static-re
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 1
stall_warnings: 0
lease_released_at: 2026-08-15T14:13:00+02:00
claim_check: passed against open Draft PR #302, exact main@8fca1c3 and non-overlapping P0 owned paths; RUNTIME PR #303 was separately active and was not mutated during this P0 lease
last_checkpoint: docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260815-exact-elf-static-tplayerdata.md
next_action: resume the separately released RUNTIME task and repair its verified runner-selector mismatch; after RUNTIME creates a bounded live exact-client window, return to P0 for passive typed-owner/provider validation before any movement stimulus
---

# Objective

Recover and causally validate a direct standalone authoritative player-position read for the exact official native Linux client. This task remains distinct from the already accepted viewport-center derivation. Research output is Draft-only; canonical promotion belongs to coordinator PR #300.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Accepted starting boundary

### FACT

- historical exact-build structural map observations were produced on `synology-otclient-01`;
- exact-profile type leads include `TPlayerData`, `TGameserverGameSession`, `TPlayerProtocolMessageHandler`, `TGameClient` and storage types;
- exact-build `TPlayerData` primary vptr offset is `0x308ca70`;
- P0 runtime probing is read-only and never globally scans arbitrary process memory for XYZ triples.

### DERIVED

`(32546,32510,7) -> (32546,32509,7) -> (32546,32510,7)` remains only the accepted viewport-geometry-derived historical player transition. It is not a direct player field.

### UNKNOWN

A direct standalone authoritative player XYZ member/access path is not yet proven.

# Acceptance gate

- [x] exact SHA/size fenced before build-specific offsets are used;
- [x] candidate search provenance restricted to typed/structurally justified owners rather than a blind global XYZ scan;
- [ ] negative controls reject camera/map-origin/viewport/copy candidates where distinguishable;
- [ ] at least two live read observations demonstrate correct value stability/change semantics;
- [ ] direct value independently compared with structural world evidence;
- [ ] client/process survives live observation and any authorized reversible stimulus is restored;
- [x] direct-read hypothesis remains explicitly distinct from the DERIVED viewport-center coordinate;
- [x] no unrelated P0 read is promoted incidentally;
- [ ] exact final-head CI terminal before final Draft handoff.

# Side-effect budget

Current usage: **zero process-memory writes, zero movement stimuli, zero gameplay actions**. If movement is later strictly necessary, only one previously proven adjacent step plus inverse is permitted after immediately rechecking RUNTIME ownership. No attack, use, move-object, market, trade, forge or currency effects.

# Runtime prerequisite evidence — FACT

Run `31883422477` / job `95009054487` executed on `synology-otclient-01`, passed the exact client executable/size/SHA fence and then proved:

```text
TRACK_A_P0_PIDFILE_STALE=true
TRACK_A_P0_DISCOVERED_EXACT_TRACK_CLIENTS=0
TRACK_A_P0_ERROR=expected_one_live_exact_track_client
```

The job failed closed before `/proc/<pid>/mem` was opened. Direct XYZ therefore remained `INCONCLUSIVE/UNKNOWN`, not disproven. Durable evidence: `20260815-live-runtime-prerequisite.md`.

# Exact ELF static checkpoint — FACT

Push-triggered P0 execution was changed to a side-effect-free `static-elf-re` job. Live probing now requires explicit `workflow_dispatch` with `mode=live` and retains the serialized runtime gate.

Run `31883967070` / job `95010405800` at code-bearing head `eec9f6fcb065dd7762fa098ad78d1661b0060bd3` completed `SUCCESS` on runner id `21`, `synology-otclient-01`.

Key exact-binary results:

```text
TPlayerData primary vptr: 0x308ca70 (.data.rel.ro)
offset-to-top:            0
typeinfo:                 0x308b5b8
TPlayerData strings:      0x1ca2c30, 0x1ca2d78
bounded vptr xrefs:       0x843e20, 0x843f60, 0x8440b0, 0x8441f2, 0xefd13c
type-string xref:         0xd2ac7d -> 0x1ca2d78
playerPosition literal:   0x1cddd3f
```

The same broad static region contains `TWorldMapRenderProvider`, `TWorldMapViewport`, `IPlayerDataProvider` and `TPlayerData` RTTI/type strings. This is a materially stronger structural lead for live testing, but it is not runtime semantic proof. `objdump` was unavailable on the runner, so no method/member meaning is assigned to the xref addresses yet.

Full evidence: `docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260815-exact-elf-static-tplayerdata.md`.

# RUNTIME coordination observation — FACT

RUNTIME run `31883846172` / job `95010096196` requested `[self-hosted, otclient, synology]` and remained queued with `runner_id=0`. During that same interval, P0 static job `95010405800` requested `[otclient, synology]`, was assigned to `synology-otclient-01` and completed successfully. This proves runner reachability and makes the extra `self-hosted` label a concrete RUNTIME selector-mismatch candidate.

# Classification

### FACT

- exact client and `TPlayerData` structural provenance are reproducible;
- static analysis recovered `playerPosition` / `IPlayerDataProvider` / worldmap context without runtime or gameplay side effects;
- runner reachability is proven independently of the queued RUNTIME selector.

### INFERENCE

The next live P0 discriminator should prioritize the `IPlayerDataProvider` / `playerPosition` graph and independently decoded `TPlayerData` xrefs before scanning broader typed owner storage.

### UNKNOWN / INCONCLUSIVE

Direct authoritative player XYZ remains **UNKNOWN / INCONCLUSIVE**. The owner/accessor behind `playerPosition`, its backing storage, lifetime and discrimination from render/viewport/cache state require live exact-client observation.

# Real stop condition

P0 has exhausted useful side-effect-free work for this invocation without taking over RUNTIME. A live exact in-game process is required for the next semantic gate. The separate RUNTIME task has released its lease after a queued external run and can now be resumed safely by a new session after live-state revalidation.

# Resume condition

After RUNTIME supplies a bounded live exact-client observation window, perform passive provider/typed-owner reads first. Only if repeated passive reads cannot discriminate a candidate may the single allowed adjacent step plus inverse be considered.
