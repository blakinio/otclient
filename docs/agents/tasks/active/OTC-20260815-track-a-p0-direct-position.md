---
task_id: OTC-20260815-track-a-p0-direct-position
status: waiting
agent: track-a-p0-state-researcher
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
blocks:
  - self-hosted runtime job 95002559098 in run 31880617510 is queued with runner_id=0; direct runner inventory is unavailable through the current connector (HTTP 403)
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
claim_check: passed against open Draft PR #302, exact branch/head and non-overlapping owned paths before the waiting checkpoint mutation
last_checkpoint: evidence checkpoint committed at a8e0e74b1ae529a23476c25aba4b09173e872904; passive code-bearing run 31880617510 remains queued and has produced no runtime semantic result
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

- exact-build live structural map observations were produced on `synology-otclient-01`;
- a forward/inverse transition was structurally observed and restored;
- exact-profile type leads include `TPlayerData`, `TGameserverGameSession`, `TPlayerProtocolMessageHandler`, `TGameClient` and storage types from PR #283 evidence.

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

- [ ] exact SHA/size fenced before build-specific offsets are used;
- [ ] candidate provenance originates in a type/owner graph, not a blind global XYZ scan;
- [ ] negative controls reject camera/map-origin/viewport/copy candidates where distinguishable;
- [ ] at least two read observations demonstrate correct value stability/change semantics; if movement is used, only one bounded reversible step plus inverse is allowed;
- [ ] direct value is independently compared with structural map/world evidence;
- [ ] process/client survives the observation and, if a reversible stimulus is used, returns to the precondition state;
- [ ] direct read remains distinct from the existing DERIVED viewport-center coordinate;
- [ ] no HP/mana/identity or other P0 read is promoted incidentally without its own evidence;
- [ ] exact-head CI is terminal before Draft handoff.

# Side-effect budget

Prefer read-only runtime observation. If a state transition is strictly necessary for discrimination, use at most one previously proven reversible adjacent movement plus inverse and verify restoration. Do not use attack, use, move-object, market, trade, forge or currency effects.

# Current checkpoint

### FACT

- Draft PR #302 is open and remains Draft-only on `research/OTC-20260815-track-a-p0-direct-position` against `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`.
- The passive reproducer resolves the exact-build `TPlayerData` primary vptr from the accepted offset `0x308ca70`, scans only typed owner objects and one pointer hop for plausible position-shaped fields, and uses structural strip data only as an independent semantic oracle.
- The reproducer performs process reads only; it does not write process memory or issue gameplay input.
- GitHub Actions run `31880617510` was created for code-bearing head `7493983ca230c789f2d423cb073e036f4e29570e`. Required job `95002559098` remains queued with `runner_id=0`; it has not executed and has produced no runtime result.
- Standard PR CI for checkpoint head `180e4a12e7016a6bea0dc8bbfe34b59aa8204dd9` completed successfully in run `31880797651`.
- Durable execution evidence is recorded at `docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260815-passive-tplayerdata-probe.md`.

### UNKNOWN

- Current online/offline state of a matching self-hosted runner; direct runner inventory returned HTTP 403 through the available connector.
- Whether the live `TPlayerData` graph contains a direct authoritative position field.
- Repeatability and fresh-PID/relogin stability for a direct position read.

# Resume condition

Resume when run `31880617510` / job `95002559098` is assigned to a matching self-hosted runner. Inspect the exact logs before deciding whether passive evidence is sufficient or whether one bounded reversible movement plus inverse is necessary. Recheck RUNTIME-lane ownership before any stimulus.

# Deliverable

Draft PR only, containing the task-scoped reproducer/evidence and an explicit read-gate classification. Do not mutate PR #283 bridge paths or any Track B path/runtime.
