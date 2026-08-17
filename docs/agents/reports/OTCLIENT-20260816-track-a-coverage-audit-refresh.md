# OTCLIENT-TIBIA-RE Track A coverage / contradiction / missing-proof audit refresh

## Status

```yaml
task: OTC-20260816-track-a-coverage-audit-refresh
lane: COVERAGE-AUDIT
researcher_delivery: draft_only
snapshot_main: 8212765956a9bfafd2d8a7687440c02716c87170
snapshot_time: 2026-08-17T09:47:00+02:00
audit_result: FAIL_MATERIAL_GAPS_OPEN
programme_complete: false
material_findings_open: 5
high_findings_open: 3
medium_findings_open: 2
runtime_access: none
physical_e2e: NOT_APPLICABLE_WITH_REASON
```

This refresh answers coordinator finding comment `5313208545` on Draft PR #390. It consumes merged P2 promotion #450 and both terminal worldmap producer merges #437/#446, plus current live P0, RUNTIME and worldmap consumer heads. Draft-only evidence remains distinct from trusted-main programme truth.

## Authority and nonclaims

This audit used GitHub/repository evidence only. It did not use Synology, execute/inspect an official client, access process memory, canonical runtime state, X11/VNC/network/login/gameplay, or owner-funded Codex/OpenAI API quota.

Exact historical installed-client fence:

```yaml
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official native Linux
```

Current audit nonclaims:

```yaml
current_canonical_display: UNKNOWN
current_canonical_vnc_endpoint: UNKNOWN
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
current_canonical_gate_b: NOT_PROVEN
current_structural_in_game: NOT_PROVEN
```

Trusted-main canonical RUNTIME task remains `raw-xres-helper-hosted-ready`. Source #447 validates a pure raw-XRes helper, but promotion #448 remains open/unmerged; exact XID→official-client PID ownership and physical identity retry remain unresolved/forbidden.

## Accepted historical quantitative baseline

Closed-unmerged PR #304 head `43a60bd96cc644b656b200c9edbfb75578b330b6` remains the accepted bounded denominator source.

| Metric | Numerator / denominator | Percentage | Boundary |
|---|---:|---:|---|
| generated protocol identifiers inventoried | 349 / 349 | 100% | identifier inventory only |
| generated protocol directions assigned | 349 / 349 | 100% | 189 inbound + 160 outbound |
| direct QMeta links in bounded protocol registry | 27 / 349 | 7.736% | not semantic completion |
| generated protocol semantic/family support | UNKNOWN / 349 | UNKNOWN | E51 still required |
| protocol-handler QMeta bounded inventory | 47 / 47 | 100% | bounded subset only |
| raw direct Qt selected inventory | 2184 / 2184 | 100% | semantic classification UNKNOWN / 2184 |
| selected legacy QObject connect edges | 40 / 41 | 97.561% | selected subset only |
| high-information GameAction sender metaobjects | 29 / 31 | 93.548% | historical bounded subset |
| P0 top-level requirement groups inventoried | 16 / 16 | 100% | group inventory only |
| P0 item-level read/action denominator | UNKNOWN / UNKNOWN | UNKNOWN | normalized registry absent |
| P1 global field/evidence denominator | UNKNOWN / UNKNOWN | UNKNOWN | normalized registry absent |
| restart-validated global capability denominator | 0 / UNKNOWN | not computable | normalized denominator absent |

Fresh current-main searches found no canonical `capabilities.jsonl`, `protocol_messages.jsonl` or `runtime_types.jsonl` files.

## Current-main / live-state delta

### P1 promotion gap remains resolved

Coordinator promotion #414 merged as `070a066488d22126483e13fc8a08b17df5090918`; source #372 is closed superseded. Live session correlation and restart/relogin stability remain unproven.

### RUNTIME helper is validated in Draft, not yet promoted

- source #447 head `32c61120b9086904b328e7b4aa50526d64bef807` validates QueryVersion and QueryClientIds(LocalClientPid) codec behavior with deterministic fixtures;
- coordinator promotion #448 head `08f7c2e7946a2283f5d0a4f5c68ab4eb589b197b` remains open and unmerged;
- trusted main therefore still lacks the validated helper implementation;
- exact resource-to-official-client PID ownership remains UNKNOWN;
- physical identity retry remains forbidden until helper promotion and fresh separate RUNTIME admission.

### Exact-static production is promoted and no longer a material staging gap

P0 producer #435 already promoted the compliant task-scoped sanitized exact-static pattern.

Worldmap exact-static producers are now both on trusted main:

- #437 merged as `f753b5aa94e9aeb6b5554fd5bb827823bda80256`, promoting exact identity/storage/handler evidence and archive state;
- #446 merged as current `main@8212765956a9bfafd2d8a7687440c02716c87170`, promoting downstream RenderProvider/Picker/Camera bounded evidence and archive state.

One-shot producer tooling was removed in the terminal trees; no client-byte mutation is authorized.

### P0 direct authoritative XYZ remains unproven

P0 #302 head `3ddf4f35e00cdfe899b4ce3daf716d71b4c3cce6` has consumed merged #435 and reports `WAITING_ON_RUNTIME_SEMANTIC_CONFIRMATION / DRAFT_NOT_PROMOTED`. Its static-input blocker is closed, but direct authoritative XYZ remains UNKNOWN / INCONCLUSIVE pending separately admitted physical correlation after resource/PID identity.

### P2 bounded downstream chain is promoted on main

Coordinator promotion #450 merged as `cbc6388e8607bb92120281a9a15148577994d3a6`; source #310 and producer #449 are archived/closed unmerged. Trusted-main evidence records:

```yaml
persistent_qbuffer_to_clientprocessor_this_plus_0x18: PROVEN
first_downstream_consumer: PROVEN:TProtocolClientMessageProcessor+0x10@0xc2df80
first_downstream_transform: PROVEN:TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
same_message_handoff_to_dualconnection_plus_0x80_plus_0x78: PROVEN
protocol_stage_order: PROVEN_PARTIAL
framing: UNKNOWN
sequence: UNKNOWN
compression: UNKNOWN
encryption: UNKNOWN
final_binary_egress: UNKNOWN
final_socket_ownership: UNKNOWN
```

This closes coordinator refresh findings `TACOORD-390-20260817-001` and `TACOORD-390-20260817-002`; it does not close any of the five programme-level findings below.

### Worldmap static dependency graph is READY in live consumer Draft with both producers promoted

Live #367 head `8f4fd11b63d4261f209e02063003e6d698039f71` reports:

```yaml
static_classification: STATIC_DEPENDENCY_GRAPH_RECOVERED
STATIC_PATCH_GRAPH_READY: true
MUTATION_DESIGN_READY: false
client_byte_mutation_authorized: false
remaining_static_blocker: NONE_FOR_STATIC_DEPENDENCY_DISCOVERY
```

Both producer inputs #437/#446 are now merged on trusted main. The consumer Draft graph covers packed `18/14` Handler source, Storage slot-12 propagation, dynamic Viewport geometry, RenderProvider fixed-32 clipping/indexing, Picker transforms and bounded Camera dependency evidence.

#367 itself remains Draft and is not silently promoted. Mutation design and physical validation remain separately authorized future work.

### Durable global coordinator checkpoint remains materially stale

Trusted main still contains `docs/agents/tasks/active/OTC-20260816-track-a-promotion-coordination.md` with `base_main: ddf7dd9408116fbeaca05bfeb69663f30f7cd34f` and obsolete global barriers. #450 added a correct P2-specific barrier but did not refresh the global coordinator task. AUD-COV-007 remains open.

## Current open material findings

### AUD-COV-001 — HIGH — canonical item-level coverage registry absent

No canonical `capabilities.jsonl`, `protocol_messages.jsonl` or `runtime_types.jsonl` package is present on `main@82127659...`.

**Impact:** coverage cannot be deterministically recomputed from canonical current-main state.

**Next discriminator:** coordinator-promote/regenerate provenance-preserving registries plus validator, retaining UNKNOWN/DISPROVEN/SUPERSEDED entries.

### AUD-COV-002 — HIGH — required semantic denominators remain incomplete

E51 full 349-message family/semantic classification, E52 full Tibia-owned QMeta/runtime classification, P0 item-level read/action denominator and P1 global field/evidence denominator remain absent.

**Impact:** inventory/subset completion can still be confused with semantic programme completion.

**Next discriminator:** execute E51/E52 against the canonical registry and materialize normalized P0/P1 item registries.

### AUD-COV-003 — MEDIUM — action/QMeta denominator conflict `612` vs historical `1004`

The durable census still records different inventory/filter definitions without one normalized versioned denominator.

**Impact:** action coverage percentages remain non-comparable.

**Next discriminator:** reconstruct/deprecate the historical 1004 definition with provenance, then version one named denominator.

### AUD-COV-004 — HIGH — canonical live semantic/restart proof remains unavailable

The raw-XRes helper is validated in #447 but not promoted on trusted main; direct resource-to-official-client PID ownership and a current canonical registered/Gate-B session remain unproven.

**Impact:** authoritative `IN_GAME`, direct XYZ causality, live P1 correlation, accepted actions and restart/relogin stability cannot be counted complete.

**Next discriminator:** finish current-main promotion #448 with exact-head gates; then create one separately admitted physical resource-to-PID discriminator. Canonical semantic experiments resume only after direct identity proof.

### AUD-COV-007 — MEDIUM — durable global coordinator checkpoint materially stale

The active coordinator task still advertises `ddf7dd...` and obsolete global barriers; lane-local P2 evidence does not repair the global record.

**Impact:** repository-resolved continuation can select stale work unless live Git is reconstructed every invocation.

**Next discriminator:** refresh the durable global coordinator task from current main while preserving lane-local accepted evidence and live open promotion dependencies.

## Resolved / reclassified since prior handoff

| Prior state | Current disposition |
|---|---|
| AUD-COV-006 P1 not promoted | `RESOLVED`: #414 merged; #372 closed superseded |
| AUD-COV-005 no compliant exact-static evidence path | `RESOLVED_AS_MATERIAL_GAP`: #435/#437/#446 promote bounded sanitized evidence patterns |
| P2 #310 open/partial-only | `SUPERSEDED`: #450 merged bounded chain; framing/crypto/egress remain UNKNOWN |
| viewport static graph incomplete | `SUPERSEDED_IN_LIVE_DRAFT`: #367 has `STATIC_PATCH_GRAPH_READY=true`; mutation design false |
| raw-XRes helper not validated | `SUPERSEDED_IN_LIVE_DRAFT`: #447 validates helper; #448 promotion remains open |
| worldmap producers unpromoted | `RESOLVED`: #437 and #446 are now merged on trusted main |

## Missing-proof queue ordered by information gain

| Priority | Missing proof | Owner | Smallest next step |
|---:|---|---|---|
| 1 | canonical machine-readable coverage registry | COVERAGE-AUDIT + coordinator | promote/regenerate `capabilities`, `protocol_messages`, `runtime_types`, provenance, supersessions and validator |
| 2 | full 349-message semantic/family classification | protocol/COVERAGE-AUDIT | E51 classify every identifier or explicit `UNCLASSIFIED` |
| 3 | full Tibia-owned QMeta/runtime denominator | QMeta/COVERAGE-AUDIT | E52 enumerate/classify every relevant type/controller/storage or ignored-with-reason |
| 4 | normalized P0/P1 item denominators | COVERAGE-AUDIT + lane owners | materialize every read/action/field item including UNKNOWN/restart state |
| 5 | current global coordinator barrier | coordinator | replace stale `ddf7dd` active checkpoint with current live state |
| 6 | raw XRes helper promotion | RUNTIME/coordinator | restack/promote accepted #447 helper via #448 with current-main validation |
| 7 | exact XID -> official-client PID identity | RUNTIME physical | separately admitted discriminator after helper promotion |
| 8 | P0 direct authoritative XYZ | P0 + RUNTIME | bounded world/negative-control correlation after identity proof |
| 9 | structural current `IN_GAME` + live P1 correlation | RUNTIME + promoted P1 | bounded proof after identified canonical session exists |
| 10 | restart/relogin stability | RUNTIME + P0/P1 | fresh PID/PIE/session reacquisition and repeated semantic correlation |
| 11 | P2 framing/sequence/compression/encryption/final egress | P2 | continue one exact stage at a time from merged #450 evidence |
| 12 | action/QMeta denominator normalization | COVERAGE-AUDIT/QMeta | reconcile 612 vs 1004 provenance |
| 13 | worldmap consumer promotion / mutation boundary | coordinator + worldmap | independently review #367 against merged #437/#446, promote durable static graph if accepted, then use a separately authorized mutation-design/physical-validation task |

## Campaign completeness verdict

```yaml
protocol_identifier_inventory_complete: true
protocol_direction_inventory_complete: true
protocol_semantic_coverage_complete: false
full_qmeta_runtime_denominator_complete: false
p0_group_requirement_inventory_complete: true
p0_item_level_read_action_denominator_complete: false
p0_exact_static_cyclopedia_bundle_promoted: true
p0_direct_authoritative_xyz_proven: false
p1_semantic_implementation_promoted: true
p1_live_session_correlation_proven: false
p2_bounded_downstream_chain_promoted: true
p2_framing_sequence_compression_encryption_egress_complete: false
exact_static_task_scoped_producer_process_proven: true
worldmap_exact_static_identity_producer_promoted: true
worldmap_downstream_static_producer_promoted: true
worldmap_static_patch_graph_ready_in_live_draft: true
worldmap_static_patch_graph_promoted_to_main: false
worldmap_mutation_design_ready: false
canonical_raw_xres_helper_promoted: false
canonical_resource_to_pid_identity_proven: false
canonical_physical_runtime_semantics_proven: false
restart_relogin_stability_proven: false
stable_live_bridge_semantics_proven: false
programme_complete: false
```

## Audit / E2E classification

```yaml
audit:
  result: FAIL_MATERIAL_GAPS_OPEN
  open_findings:
    high: 3
    medium: 2
  p1_promotion_gap_resolved: true
  exact_static_staging_material_gap_resolved: true
  p2_bounded_chain_promoted: true
  worldmap_producer_chain_promoted: true
  inventory_vs_semantic_boundary_preserved: true
  draft_lane_evidence_promoted_without_merge: false
e2e:
  result: NOT_APPLICABLE_WITH_REASON
  reason: documentation/evidence-only COVERAGE-AUDIT with runtime_access none; physical E2E belongs to separately admitted RUNTIME work
```

## Researcher delivery boundary

This package remains `DRAFT_NOT_PROMOTED`. Coordinator review must choose `ACCEPT | ACCEPT_WITH_EDITS | RETURN_FOR_EVIDENCE | REJECT/SUPERSEDE`. The researcher does not self-promote global programme truth.
