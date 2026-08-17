---
task_id: OTC-20260815-track-a-p0-direct-position
status: waiting
agent: ChatGPT
session_id: chatgpt-p0-consume-merged-cyclopedia-20260817
session_role: researcher
session_rotation_count: 6
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: runtime-research
phase: p0-runtime-semantic-confirmation
branch: research/OTC-20260815-track-a-p0-direct-position
base_branch: main
base_main: dbd9520e2f8cc5a26f556bffaae2a83e139615f9
current_main: 8c9486e2c6109a7a39b564804c8acd707659b5e0
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-p0-direct-position
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
updated: 2026-08-17T09:11:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p0-direct-position.md
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/**
  - .github/workflows/tibia-official-client-re-p0-direct-position.yml
  - .github/scripts/tibia-official-client-re-p0-direct-position.py
reuses:
  - workflow artifact 9248797952 / sha256:04835ab0bac7ffc43e161e8b2118c90a3d2197f7011385a6758cd7706c93a584
  - exact structural anchors from code-bearing head a3068a6a9460525cb1946186cf439caf7832e176
  - merged producer PR #435 / main commit 8c9486e2c6109a7a39b564804c8acd707659b5e0
  - final producer run 32000921225 / source head 40b5efd2f6371b8f5c0a00036084960ab66eefd0
  - final consumer artifact 9278368790 / track-a-p0-cyclopedia-sanitized-32000921225
  - docs/agents/evidence/OTC-20260816-track-a-p0-cyclopedia-sanitized-bundle/p0-cyclopedia-sanitized-evidence.md
  - docs/agents/evidence/OTC-20260816-track-a-p0-cyclopedia-sanitized-bundle/evidence-data.json
  - docs/agents/evidence/OTC-20260816-track-a-p0-cyclopedia-sanitized-bundle/selected-code-windows.txt
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260817-consume-merged-cyclopedia-evidence.md
depends_on:
  - RUNTIME establishment of exact physical client PID/resource identity under current admission
  - RUNTIME-owned bounded semantic XYZ/world correlation, negative controls and fresh-PID/relogin evidence
blocks: []
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
last_evidence_head: e588223b549a160d084694ed8b39b4e228508a41
ci_checks_for_current_head: 0
ci_check_generation: merged-cyclopedia-consumption-checkpoint
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 3
stall_warnings: 0
legacy_runtime_pr_303: CLOSED_SUPERSEDED_HISTORICAL_EVIDENCE_ONLY
static_input_blocker: CLOSED_BY_MERGED_PR_435
semantic_player_xyz_proven: false
runtime_provider_task: OTC-20260816-track-a-canonical-runtime-e2e
runtime_provider_state: RAW_XRES_HELPER_PROMOTION_PENDING
runtime_provider_hosted_helper_source_pr: 447
runtime_provider_hosted_helper_promotion_pr: 448
runtime_provider_physical_identity_retry_authorized: false
hosted_attempts:
  archive_referer:
    run: 31947502633
    result: HTTP_403_INPUT_BLOCKED
  package_manifest:
    run: 31948000086
    result: HTTP_403_INPUT_BLOCKED_AT_PACKAGE_VERSION
  launcher_equivalent_and_direct_ip:
    run: 31948567275
    result: HTTP_403_DOMAIN_AND_TWO_RESOLVED_IPV4_INPUT_BLOCKED
final_cyclopedia_producer:
  pr: 435
  merge_commit: 8c9486e2c6109a7a39b564804c8acd707659b5e0
  source_run: 32000921225
  source_head: 40b5efd2f6371b8f5c0a00036084960ab66eefd0
  artifact: 9278368790
  artifact_name: track-a-p0-cyclopedia-sanitized-32000921225
  accepted_zip_digest: sha256:49f48d4283e63dd613b32a99300dc86eb98d68d7d7f640ec621c72e854c30c87
  target_labels: 9
  direct_relocations: 4
  typeinfo_candidate: 0x3089a50
  vtable_address_point: 0x3089db0
  unique_rip_xrefs: 4
  disassembly_windows: 4
  hosted_validation: PASS
  runtime_access: none
  semantic_player_xyz_proven: false
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-p0-direct-position/20260817-consume-merged-cyclopedia-evidence.md
  - docs/agents/evidence/OTC-20260816-track-a-p0-cyclopedia-sanitized-bundle/p0-cyclopedia-sanitized-evidence.md
next_action: consume only a fresh RUNTIME-owned physical discriminator after exact client PID/resource identity is proven under current admission; require two or more direct-position observations correlated with independent structural world coordinates, negative controls, and fresh-PID/relogin repeatability before promoting authoritative XYZ
---

# Objective

Recover and causally validate a direct standalone authoritative player-position read for the exact official native Linux client, distinct from derived viewport/map/camera coordinates. Research output remains Draft-only; canonical promotion belongs to the Track A coordinator.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
TPlayerData_primary_vptr: 0x308ca70
```

# Routing boundary

P0 remains GitHub-hosted with `runtime_access:none`. It does not own Synology physical runtime, X11/VNC, login/relogin, process attach, input or gameplay mutation. RUNTIME is the exclusive physical causal/restart evidence provider.

# Acceptance gate

- [x] exact SHA/size fence defined before build-specific offsets are used;
- [x] candidate discovery is type/owner-graph constrained rather than a blind XYZ scan;
- [x] direct read remains distinct from the accepted DERIVED viewport-center coordinate;
- [x] P0 deterministic workflow is GitHub-hosted / no physical runtime;
- [x] failed direct GitHub-hosted CDN retrieval paths are exhausted without blind retry;
- [x] merged producer #435 supplies a compliant exact-client sanitized Cyclopedia RTTI/vtable/metadata/xref bundle on trusted main;
- [x] P0 consumed the merged #435 evidence and closed the generic static-input blocker;
- [ ] exact authoritative in-process XYZ storage/read semantics proven;
- [ ] negative controls reject camera/map-origin/viewport/copy candidates;
- [ ] at least two live observations demonstrate correct value stability/change semantics;
- [ ] direct value independently compared with structural world evidence;
- [ ] fresh PID/relogin stability proven by RUNTIME;
- [ ] exact final Draft-head CI green after the final semantic evidence checkpoint.

# Structural evidence — FACT

Retained exact-build evidence preserves `TPlayerData` primary vptr `0x308ca70`, `playerPosition` literal `0x1cdde3f`, its bounded xrefs `0x8367c1/0x8367c2`, and relocation-backed worldmap/player-provider type relationships.

Merged #435 now canonically adds the Cyclopedia structural route:

```text
TCyclopediaMapStorage typeinfo candidate  0x3089a50
TCyclopediaMapStorage vtable address point 0x3089db0
vtable typeinfo relocation slot            0x3089da8
code xrefs to vtable                        0x812952, 0x812e12, 0xeb0ea2
metadata xref                               0xd299ed -> 0x1d2a8d8
```

The exact client also contains the compact metadata neighborhood containing `TCyclopediaMapStorage`, `playerPositionChanged`, `TWorldMapCoordinate`, `onPlayerCreatureAddedToGameSession`, `weak_ptr<TCreature>`, `pPlayer`, and `onPlayerPositionWasUpdated`.

At `0xeb0ea2`, code installs the recovered vtable at `[rbx]` and initializes a large member-relative object graph. This is structural object-initializer evidence only.

# Classification

## FACT

- exact client fence is stable for all accepted P0 static evidence;
- the P0 static-input staging gap is closed by merged PR #435;
- the requested Cyclopedia/player metadata, RTTI/typeinfo/vtable graph, relocations and four unique code xrefs are on trusted main;
- P0 has no physical runtime authority;
- current RUNTIME has not yet produced the required semantic direct-position discriminator.

## STRUCTURAL_DERIVATION

The `0xeb0ea2` path is associated with a `TCyclopediaMapStorage` object initializer. The compact player-position metadata neighborhood is a valid route for further static discovery, but metadata locality alone does not identify callback implementations or player coordinate storage.

## UNKNOWN / INCONCLUSIVE

- authoritative live XYZ member/accessor and owning runtime object;
- executable implementations of the specific Cyclopedia position callbacks;
- live discrimination against map/camera/viewport/copy candidates;
- repeatability across movement and fresh PID/relogin.

# RUNTIME dependency

Current RUNTIME work has advanced beyond the older `client_window_missing` frontier. Raw X11 evidence proves a viewable full-display resource exists, but exact XID-to-official-client PID ownership is still unresolved. Hosted raw-XRes helper PR #447 has passed deterministic validation and coordinator promotion PR #448 is open. A physical identity retry remains unauthorized until promotion completes and a fresh separately admitted RUNTIME discriminator is created.

Once RUNTIME reaches that admitted state, P0 requires only the bounded physical discriminator documented in `20260817-consume-merged-cyclopedia-evidence.md`; P0 must not create a parallel runtime session.

# Side-effect budget

This continuation performed repository/GitHub evidence reads and P0 task/evidence updates only. It used no client execution, process-memory access, X11/VNC, login/session action, gameplay stimulus, raw proprietary-client upload or owner-funded Codex/OpenAI API quota.