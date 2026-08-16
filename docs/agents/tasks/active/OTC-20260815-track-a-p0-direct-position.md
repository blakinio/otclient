---
task_id: OTC-20260815-track-a-p0-direct-position
status: waiting
agent: ChatGPT
session_id: chatgpt-p0-presanitized-reuse-20260816
session_role: researcher
session_rotation_count: 5
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: runtime-research
phase: p0-direct-player-position
branch: research/OTC-20260815-track-a-p0-direct-position
base_branch: main
base_main: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
current_main: a1bab5e7197aba484ac72a4dbcb2d8fddeaeacc2
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-p0-direct-position
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
updated: 2026-08-16T19:49:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p0-direct-position.md
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/**
  - .github/workflows/tibia-official-client-re-p0-direct-position.yml
  - .github/scripts/tibia-official-client-re-p0-direct-position.py
reuses:
  - workflow artifact 9248797952 / sha256:04835ab0bac7ffc43e161e8b2118c90a3d2197f7011385a6758cd7706c93a584
  - exact structural anchors from code-bearing head a3068a6a9460525cb1946186cf439caf7832e176
  - workflow artifact 9252025461 / sha256:2a866247558b079944d81c9ad33bd4c5361c8144a7f367b273ab3bc19a080991
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_P0_STATE_ALIAS.md
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260816-hosted-staging-and-launcher.md
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260816-presanitized-p2-bundle-reuse.md
depends_on:
  - coordinator-approved compliant evidence staging for exact 15.32.df7b29 bin/client or a sufficiently narrow derived instruction window
  - alternatively owner-supplied exact installed packages/Tibia/bin/client matching the exact fence
  - durable physical semantic evidence from RUNTIME after canonical runtime gates permit it
blocks:
  - GitHub-hosted exact-binary materialization remains INPUT_BLOCKED by HTTP 403 after three materially distinct evidence-based strategies
  - newly reusable pre-sanitized exact-fence artifact 9252025461 contains P2 network-processor disassembly but not the missing 0x8367c1 instruction window
  - direct causal validation is WAITING because current trusted-main RUNTIME remains canonical-registration absent with no registered exact PID/session or Gate B proof
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
hosted_harness_head: 5b581a6a64edb9c05143a855dbfd1cb2fffea316
last_evidence_head: f851d32b23c8c47dc8e41145b98e49cea5e22ef3
ci_checks_for_current_head: 0
ci_check_generation: presanitized-reuse-checkpoint
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
context_reconstruction_attempts: 2
stall_warnings: 0
legacy_runtime_pr_303: CLOSED_SUPERSEDED_HISTORICAL_EVIDENCE_ONLY
runtime_provider_task: OTC-20260816-track-a-canonical-runtime-e2e
runtime_provider_state: BLOCKED_CANONICAL_REGISTRATION_ABSENT_NO_GATE_B
runtime_provider_last_observed_main: a1bab5e7197aba484ac72a4dbcb2d8fddeaeacc2
runtime_provider_last_physical_attempt_pr: 405
runtime_provider_last_physical_attempt_run: 31960965493
runtime_provider_last_physical_attempt_result: GOVERNANCE_INVALID_FAIL_CLOSED_CLIENT_WINDOW_MISSING
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
  launcher_equivalent_and_direct_ip:
    run: 31948567275
    job: 95168377109
    result: HTTP_403_DOMAIN_AND_TWO_RESOLVED_IPV4_INPUT_BLOCKED
    sanitized_artifact: 9263987119
owner_supplied_launcher:
  archive_size: 29477141
  archive_sha256: 04a87c801d3855f4da1b07e201dff1f79acc8528c57c984131c3a2a88cb60ea7
  bin_client_entries: 0
  launcher_size: 1460808
  launcher_sha256: a5fc6e8ee8246868263c438539a54ea045bd048a1bea45f968fc2f498b682ca0
  disposition: LAUNCHER_ONLY_NOT_EXACT_GAME_CLIENT
validation:
  coherent_harness_head: 41396384650c329dab7fc159867a8ffb2afa2e35
  hosted_harness_governance_run: 31948197816
  hosted_harness_governance_result: SUCCESS
  hosted_harness_repository_ci_run: 31948197910
  hosted_harness_repository_ci_result: SUCCESS
artifact_search:
  result: EXHAUSTED_NO_DIRECT_POSITION_INSTRUCTION_WINDOW
  checked_examples:
    - 9246756211
    - 9248797952
    - 9233690471
    - 9228921041
    - 9231716774
    - 9225203231
    - 9225585838
    - 9227370490
    - 9252114795
    - 9252025461
  latest_checked_artifact:
    id: 9252025461
    source_run: 31904696996
    digest: sha256:2a866247558b079944d81c9ad33bd4c5361c8144a7f367b273ab3bc19a080991
    exact_client_size: 51965216
    exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
    target_anchor_matches: 0
    disposition: VALID_EXACT_FENCE_BUT_WRONG_DISASSEMBLY_RANGES
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260816-presanitized-p2-bundle-reuse.md
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260816-github-hosted-replay.md
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260816-hosted-staging-and-launcher.md
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260815-player-position-static-graph.md
next_action: consume a coordinator-approved sanitized exact-client bundle that contains the bounded 0x8367c1 instruction window, or another compliant GitHub-hosted exact-client evidence source capable of producing that window; consume direct XYZ/world correlation and fresh-PID/relogin confirmation only from RUNTIME
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

P0 static/deterministic execution remains GitHub-hosted with `runtime_access: none`. P0 does not own Synology, X11/VNC, login/relogin, client process/session or physical input. RUNTIME is the only producer of physical causal/restart evidence. Historical `:98`, `6082`, PID/session and closed PR #303 surfaces are not current authority.

# Acceptance gate

- [x] exact SHA/size fence defined before build-specific offsets are used;
- [x] candidate provenance restricted to typed/structurally justified owners rather than a blind global XYZ scan;
- [x] direct-read hypothesis kept explicitly distinct from the DERIVED viewport-center coordinate;
- [x] current P0 workflow routed to `ubuntu-latest` / `runtime_access: none`; stale Synology/live jobs removed;
- [x] hosted package harness verifies manifest packed/unpacked hashes plus independent exact client fence and deletes proprietary inputs before artifact upload;
- [x] three materially distinct hosted staging hypotheses executed and classified without repeating an identical failure;
- [x] retained sanitized exact-client/static/runtime artifacts searched for an already-preserved `0x8367c1` instruction window;
- [x] newly identified exact-fence pre-sanitized artifact `9252025461` inspected and rejected as a P0 target source because its bounded disassembly ranges do not include `0x8367c1`;
- [ ] successful current exact-binary disassembly around `0x8367c1`;
- [ ] negative controls reject camera/map-origin/viewport/copy candidates where distinguishable;
- [ ] at least two live semantic observations demonstrate correct value stability/change semantics;
- [ ] direct value independently compared with structural world evidence;
- [ ] fresh PID/relogin stability is proven by RUNTIME evidence;
- [ ] exact final Draft-head CI terminal green after semantic evidence checkpoint.

# Retained exact-build structural evidence — FACT

Sanitized exact-client artifact `9248797952` / run `31892019505` preserves:

```text
playerPosition primary literal: 0x1cdde3f
bounded primary xrefs:          0x8367c1 / 0x8367c2
TWorldMapRenderProvider:         0x3089b78 -> 0x1cddd20
TWorldMapViewport:               0x308b598 -> 0x1ce1b60
IPlayerDataProvider:             0x308b5b0 -> 0x1ce1ba0
TPlayerData:                     0x308b5c0 -> 0x1ce1bd0
TPlayerData primary vptr:        0x308ca70
```

The full successful job log additionally preserves exact TPlayerData vtable targets including `0xd1cbd0`, `0xd2ac70`, `0xd2ef30`, `0x843e20`, `0x843f60` and later slots. Its GDB disassembly commands failed because the retained task-local GDB could not load `libpython3.12.so.1.0`; neither the original artifact nor later searched sanitized Track A artifacts contains a successful instruction body at `0x8367c1`. The backing member/accessor cannot be invented.

# Current hosted input evidence — FACT

Three distinct GitHub-hosted/no-runtime strategies failed before exact client bytes were obtained:

1. `31947502633` / `95165743019`: top-level archive, browser-like User-Agent + same-URL Referer -> HTTP 403; artifact `9263704543`;
2. `31948000086` / `95166976133`: launcher package `package.json.version` -> HTTP 403; artifact `9263837982`;
3. `31948567275` / `95168377109`: launcher-equivalent no-custom-UA request plus two current IPv4 `--resolve` fallbacks preserving TLS/SNI/Host -> domain 403 and both direct-IP paths 403; artifact `9263987119`.

Every attempt ran on `ubuntu-latest`, used `runtime_access:none`, failed before semantic analysis, and passed proprietary-input cleanup. The staging gate has reached its three-cycle repair limit; P0 will not invent a fourth HTTP-bypass attempt without materially new evidence.

The owner-supplied current Linux download is launcher-only: archive SHA-256 `04a87c801d3855f4da1b07e201dff1f79acc8528c57c984131c3a2a88cb60ea7`, no `bin/client`, launcher SHA-256 `a5fc6e8ee8246868263c438539a54ea045bd048a1bea45f968fc2f498b682ca0`. It was not executed.

## Reused pre-sanitized P2 bundle — FACT

Live PR #310 exposed preserved run `31904696996` / artifact `9252025461` as a compliant pre-sanitized exact-client evidence source. P0 downloaded and inspected that artifact during this continuation. Its own validation records the exact P0 size/SHA fence, but its retained disassembly is deliberately scoped to P2 processor/network ranges (`0x7dd630`, `0xc2df80`, `0xb47130`, `0xb56970`, connection edge `0x19716a3`). It has zero matches for `0x8367c1`, `0x8367c2`, `playerPosition`, `TPlayerData` or `0x1cdde3f`.

Therefore the artifact is valid evidence provenance but cannot recover the missing P0 member/accessor graph. Full durable record: `docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260816-presanitized-p2-bundle-reuse.md`.

# Historical source-package boundary — FACT

Historical closed RUNTIME PR #303 source shows that exact-client tasks verified and copied from `/home/runner/_work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia`. This is discovery/provenance only: P0 cannot use that Synology-local material as static fallback under the current hybrid routing contract. A coordinator-approved evidence-staging strategy is required.

# Current RUNTIME dependency — FACT

Trusted `main@a1bab5e7197aba484ac72a4dbcb2d8fddeaeacc2` still carries `docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md` as `blocked`. Its v7 checkpoint records `canonical_registration: ABSENT`, exact PID/session `NOT_REGISTERED`, Gate B not reached and `mutation_authorized: false`. Physical attempt PR #405/run `31960965493` reached client start but failed closed at `client_window_missing`; its mutation execution is explicitly governance-invalid and cannot be treated as authoritative runtime evidence. No direct-position discriminator has therefore been produced for P0 yet.

# Classification

### FACT

- exact client/TPlayerData structural provenance is retained;
- primary `playerPosition` string and xrefs are exact-file anchored;
- direct player XYZ is not yet proven;
- GitHub-hosted access to current official archive/package metadata is consistently blocked before exact bytes are delivered;
- the newly reusable exact-fence artifact `9252025461` is structurally valid but does not contain the target P0 instruction range;
- current RUNTIME has no registered exact PID/session and no Gate B proof;
- P0 has zero current physical runtime authority.

### UNKNOWN / INCONCLUSIVE

- direct authoritative player XYZ member/accessor offset;
- owning function and instruction semantics around `0x8367c1`;
- live discrimination against map/camera/viewport/copy candidates;
- repeatability and fresh PID/relogin stability.

# Side-effect budget

This continuation used zero Synology execution, zero process-memory reads/writes, zero gameplay stimuli, zero client/display/network observation, zero login/session actions and zero owner-funded AI/API quota. The reused P2 artifact contained sanitized evidence only; no proprietary client/package bytes were committed or uploaded by P0.
