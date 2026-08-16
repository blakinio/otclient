---
task_id: OTC-20260815-track-a-p0-direct-position
status: waiting
agent: ChatGPT
session_id: chatgpt-p0-hosted-replay-20260816-1425
session_role: researcher
session_rotation_count: 3
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: runtime-research
phase: p0-direct-player-position
branch: research/OTC-20260815-track-a-p0-direct-position
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
current_main: ce9997304e4b771b6243395bf0c3a6084f32a7dc
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-p0-direct-position
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
updated: 2026-08-16T14:25:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p0-direct-position.md
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/**
  - .github/workflows/tibia-official-client-re-p0-direct-position.yml
  - .github/scripts/tibia-official-client-re-p0-direct-position.py
reuses:
  - workflow artifact 9248797952 / sha256:04835ab0bac7ffc43e161e8b2118c90a3d2197f7011385a6758cd7706c93a584
  - exact structural anchors from code-bearing head a3068a6a9460525cb1946186cf439caf7832e176
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_P0_STATE_ALIAS.md
depends_on:
  - coordinator-approved legally and technically compliant GitHub-hosted-readable staging source for exact client 15.32.df7b29
  - durable physical semantic evidence from RUNTIME PR #358 after current canonical runtime gates permit it
blocks:
  - hosted exact-binary disassembly is INPUT_BLOCKED by the same staging dependency demonstrated by P2 PR #310
  - live semantic validation is WAITING because RUNTIME PR #358 still has canonical_registration ABSENT, bootstrap REQUIRED_UNIMPLEMENTED, target_uniqueness UNKNOWN and mutation_authorized false
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
execution_class: github_hosted
runtime_access: none
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
mutation_authorized: false
owner_funded_ai_api_authorized: false
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: low_noise
code_bearing_head: a3068a6a9460525cb1946186cf439caf7832e176
invocation_started_at: 2026-08-16T14:25:00+02:00
last_progress_at: 2026-08-16T14:25:00+02:00
lease_released_at: 2026-08-16T14:25:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: github-hosted-replay
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
legacy_runtime_pr_303: CLOSED_SUPERSEDED
runtime_provider_pr: 358
runtime_provider_head: d78e42b955c27ee07fba783f5496588f34d29461
runtime_infra_pr: 360
runtime_infra_head: 1d64fab66650b1fcd58388ff5cf6f9a77a392dc4
hosted_staging_reference_pr: 310
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260816-github-hosted-replay.md
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260815-player-position-static-graph.md
next_action: after a coordinator-approved compliant GitHub-hosted-readable staging source for the exact fenced client exists, run one bounded hosted disassembly around 0x8367c1 and structurally justified TPlayerData/IPlayerDataProvider neighbors; consume any physical semantic confirmation only from durable RUNTIME evidence
---

# Objective

Recover and causally validate a direct standalone authoritative player-position read for the exact official native Linux client, distinct from the already accepted DERIVED viewport-center coordinate. Research output is Draft-only; canonical promotion belongs to the Track A coordinator.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
TPlayerData_primary_vptr: 0x308ca70
```

# Current routing boundary

P0 runs static/deterministic work on GitHub-hosted infrastructure with `runtime_access: none`. P0 does not own the physical Synology desktop, VNC, login or client session. Any physical confirmation is produced by RUNTIME and consumed here as durable evidence.

The old P0 workflow still contains historical Synology jobs from the prior task generation. They are not authorized execution paths for this invocation and were not triggered by the 2026-08-16 replay. Historical `:98`, `6082`, PID/session and PR #303 runtime surfaces are not current authority.

# Acceptance gate

- [x] exact SHA/size fenced before build-specific offsets are used;
- [x] candidate search provenance restricted to typed/structurally justified owners rather than a blind global XYZ scan;
- [ ] negative controls reject camera/map-origin/viewport/copy candidates where distinguishable;
- [ ] at least two live semantic observations demonstrate correct value stability/change semantics;
- [ ] direct value independently compared with structural world evidence;
- [ ] client/process survives physical observation and any separately authorized reversible stimulus is restored;
- [x] direct-read hypothesis remains explicitly distinct from the DERIVED viewport-center coordinate;
- [x] no unrelated P0 read is promoted incidentally;
- [ ] fresh PID/relogin stability is proven by RUNTIME evidence;
- [ ] exact final-head CI terminal green before final Draft handoff.

# Structural evidence retained — FACT

The exact-build sanitized artifact from workflow run `31892019505`, artifact `9248797952`, preserves:

```text
playerPosition literal: 0x1cdde3f
unique bounded code site: 0x8367c1 -> 0x1cdde3f
TWorldMapRenderProvider: 0x3089b78 -> 0x1cddd20
TWorldMapViewport:       0x308b598 -> 0x1ce1b60
IPlayerDataProvider:     0x308b5b0 -> 0x1ce1ba0
TPlayerData:             0x308b5c0 -> 0x1ce1bd0
TPlayerData vptr:        0x308ca70
```

The same artifact records failed bounded GDB disassembly at `0x8367c1` and all attempted neighboring targets; it does not contain proprietary machine-code bytes. The exact owning function/member offset therefore cannot be recovered from that artifact alone.

Durable replay: `docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260816-github-hosted-replay.md`.

# Current blockers — FACT

RUNTIME PR #358 currently proves only canonical lease/registration absence and classifies bootstrap as required but unimplemented; it has not supplied a live exact-client observation window. Runtime-infra PR #360 remains Draft/not promoted.

P2 PR #310 independently demonstrated that the current compliant GitHub-hosted exact-client materialization path is blocked: one attempt failed DNS resolution for `download.tibia.com`, the next received HTTP 403 from `static.tibia.com`, and Synology static fallback is forbidden. P0 therefore cannot produce a fresh hosted exact-binary instruction window until a compliant staging source exists.

# Classification

### FACT

- exact client / `TPlayerData` structural provenance is retained;
- `playerPosition` primary literal and bounded code site are exact-file anchored;
- provider/worldmap/TPlayerData RTTI relationships are relocation anchored;
- no current live or physical side effect was used by this replay;
- the current compliant hosted exact-binary input is unavailable;
- the current canonical runtime is not registered and P0 has no physical ownership.

### UNKNOWN / INCONCLUSIVE

Direct authoritative player XYZ remains **UNKNOWN / INCONCLUSIVE**. Backing member/accessor offset, instruction semantics, causal discrimination against camera/map/viewport copies, repeatability and restart/relogin stability still require new evidence.

# Side-effect budget

Current 2026-08-16 replay usage: **zero Synology execution, zero process-memory reads/writes, zero gameplay stimuli, zero client/display/network observation, zero login/session actions**.
