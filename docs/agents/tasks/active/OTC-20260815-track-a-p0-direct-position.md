---
task_id: OTC-20260815-track-a-p0-direct-position
status: waiting
agent: ChatGPT
session_id: chatgpt-p0-hosted-staging-20260816
session_role: researcher
session_rotation_count: 4
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: runtime-research
phase: p0-direct-player-position
branch: research/OTC-20260815-track-a-p0-direct-position
base_branch: main
base_main: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
current_main: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-p0-direct-position
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
updated: 2026-08-16
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p0-direct-position.md
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/**
  - .github/workflows/tibia-official-client-re-p0-direct-position.yml
  - .github/scripts/tibia-official-client-re-p0-direct-position.py
reuses:
  - workflow artifact 9248797952 / sha256:04835ab0bac7ffc43e161e8b2118c90a3d2197f7011385a6758cd7706c93a584
  - exact structural anchors from code-bearing head a3068a6a9460525cb1946186cf439caf7832e176
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_P0_STATE_ALIAS.md
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260816-hosted-staging-and-launcher.md
depends_on:
  - coordinator-approved legally and technically compliant GitHub-hosted-readable staging source for exact client 15.32.df7b29, or owner-supplied exact installed bin/client as input to an approved staging handoff
  - durable physical semantic evidence from RUNTIME PR #358 after current canonical runtime gates permit it
blocks:
  - GitHub-hosted exact-binary materialization is INPUT_BLOCKED by HTTP 403 before package bytes are available
  - direct causal validation is WAITING because RUNTIME #358 still has no admitted canonical exact-client session
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
execution_class: github_hosted
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
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
mutation_authorized: false
owner_funded_ai_api_authorized: false
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: low_noise
code_bearing_head: a3068a6a9460525cb1946186cf439caf7832e176
hosted_harness_head: 41396384650c329dab7fc159867a8ffb2afa2e35
last_evidence_head: 3a93b4bf7e22936e7430beb7c172a9e9e0c0d5fc
ci_checks_for_current_head: 0
ci_check_generation: staging-checkpoint
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 1
stall_warnings: 0
legacy_runtime_pr_303: CLOSED_SUPERSEDED
runtime_provider_pr: 358
runtime_provider_head: d78e42b955c27ee07fba783f5496588f34d29461
runtime_infra_pr: 360
runtime_infra_head: 1d64fab66650b1fcd58388ff5cf6f9a77a392dc4
hosted_staging_reference_pr: 310
hosted_attempts:
  archive_referer:
    run: 31947502633
    job: 95165743019
    result: HTTP_403_INPUT_BLOCKED
    sanitized_artifact: 9263704543
  package_manifest:
    run: 31948000086
    job: 95166976133
    result: HTTP_403_INPUT_BLOCKED_AT_PACKAGE_VERSION
    sanitized_artifact: 9263837982
owner_supplied_launcher:
  archive_size: 29477141
  archive_sha256: 04a87c801d3855f4da1b07e201dff1f79acc8528c57c984131c3a2a88cb60ea7
  bin_client_entries: 0
  launcher_size: 1460808
  launcher_sha256: a5fc6e8ee8246868263c438539a54ea045bd048a1bea45f968fc2f498b682ca0
  disposition: LAUNCHER_ONLY_NOT_EXACT_GAME_CLIENT
validation:
  hosted_harness_governance_run: 31948197816
  hosted_harness_governance_result: SUCCESS
  hosted_harness_repository_ci_run: 31948197910
  hosted_harness_repository_ci_result: SUCCESS
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260816-github-hosted-replay.md
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260816-hosted-staging-and-launcher.md
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260815-player-position-static-graph.md
next_action: obtain a compliant exact installed packages/Tibia/bin/client for version 15.32.df7b29; verify size 51965216 and SHA-256 e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe before any new disassembly, then recover the bounded 0x8367c1/TPlayerData instruction graph; consume causal/relogin confirmation only from RUNTIME
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

P0 static/deterministic execution remains GitHub-hosted with `runtime_access: none`. P0 does not own Synology, X11/VNC, login/relogin, client process/session or physical input. RUNTIME is the only producer of physical causal/restart evidence.

Historical `:98`, `6082`, PID/session and closed PR #303 surfaces are not current authority.

# Acceptance gate

- [x] exact SHA/size fence defined before build-specific offsets are used;
- [x] candidate provenance restricted to typed/structurally justified owners rather than a blind global XYZ scan;
- [x] direct-read hypothesis kept explicitly distinct from the DERIVED viewport-center coordinate;
- [x] current P0 workflow routed to `ubuntu-latest` / `runtime_access: none`; stale Synology/live jobs removed;
- [x] hosted package harness verifies manifest packed/unpacked hashes plus the independent exact client fence and deletes proprietary inputs before artifact upload;
- [ ] successful current hosted exact-binary disassembly around `0x8367c1`;
- [ ] negative controls reject camera/map-origin/viewport/copy candidates where distinguishable;
- [ ] at least two live semantic observations demonstrate correct value stability/change semantics;
- [ ] direct value independently compared with structural world evidence;
- [ ] fresh PID/relogin stability is proven by RUNTIME evidence;
- [ ] exact final Draft-head CI terminal green after the semantic evidence checkpoint.

# Retained exact-build structural evidence — FACT

Sanitized artifact `9248797952` from exact-client run `31892019505` preserves:

```text
playerPosition primary literal: 0x1cdde3f
bounded primary code lead:      0x8367c1 -> 0x1cdde3f
TWorldMapRenderProvider:         0x3089b78 -> 0x1cddd20
TWorldMapViewport:               0x308b598 -> 0x1ce1b60
IPlayerDataProvider:             0x308b5b0 -> 0x1ce1ba0
TPlayerData:                     0x308b5c0 -> 0x1ce1bd0
TPlayerData primary vptr:        0x308ca70
```

The same artifact contains no successful instruction window for `0x8367c1`; its bounded GDB commands failed and proprietary machine-code bytes were not retained. The backing member/accessor cannot be invented from these anchors.

# Current hosted input evidence — FACT

Two materially distinct current P0 hosted strategies have failed before receiving exact client bytes:

1. run `31947502633` / job `95165743019`: top-level official Linux archive with browser-like User-Agent and same-URL Referer -> HTTP 403; sanitized artifact `9263704543`; cleanup PASS;
2. run `31948000086` / job `95166976133`: launcher-native `tibiaclient-linux-current/package.json.version` path -> HTTP 403 before manifest retrieval; sanitized artifact `9263837982`; cleanup PASS.

The owner then supplied the current official Linux download archive. Static inspection proves it is launcher-only: archive SHA-256 `04a87c801d3855f4da1b07e201dff1f79acc8528c57c984131c3a2a88cb60ea7`, no `bin/client`, launcher `Tibia/Tibia` SHA-256 `a5fc6e8ee8246868263c438539a54ea045bd048a1bea45f968fc2f498b682ca0`. The launcher itself was not executed and no agreement/credential/session action was performed.

Full evidence: `docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260816-hosted-staging-and-launcher.md`.

# Harness validation — FACT

The final dormant hosted staging harness at `41396384650c329dab7fc159867a8ffb2afa2e35` passed normal Track A governance run `31948197816` and repository CI run `31948197910`. The harness supports raw or 32-byte-prefixed LZMA only under manifest and independent exact-fence verification. Task-only checkpoint edits no longer trigger another external download attempt.

# Classification

### FACT

- exact client/TPlayerData structural provenance above is retained;
- the primary `playerPosition` literal and bounded code lead are exact-file anchored;
- direct player XYZ is not yet proven;
- current GitHub-hosted access to the official archive and package-version endpoint is blocked before exact bytes are available;
- the owner-supplied archive is launcher-only, not the installed game client;
- current P0 uses zero physical runtime authority.

### UNKNOWN / INCONCLUSIVE

- direct authoritative player XYZ member/accessor offset;
- owning function and instruction semantics around `0x8367c1`;
- live discrimination against map/camera/viewport/copy candidates;
- repeatability and fresh PID/relogin stability.

# Side-effect budget

This continuation used zero Synology execution, zero process-memory reads/writes, zero gameplay stimuli, zero client/display/network observation, zero login/session actions and zero owner-funded AI/API quota. Proprietary owner-supplied and transient download material was not committed or uploaded to GitHub.
