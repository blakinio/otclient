# OTCLIENT-TIBIA-RE Track A coverage / contradiction / missing-proof audit refresh

## Status

```yaml
task: OTC-20260816-track-a-coverage-audit-refresh
lane: COVERAGE-AUDIT
researcher_delivery: draft_only
snapshot_main: cbc6388e8607bb92120281a9a15148577994d3a6
snapshot_time: 2026-08-17T09:41:00+02:00
audit_result: FAIL_MATERIAL_GAPS_OPEN
programme_complete: false
material_findings_open: 5
high_findings_open: 3
medium_findings_open: 2
runtime_access: none
physical_e2e: NOT_APPLICABLE_WITH_REASON
```

This refresh answers coordinator finding comment `5313208545` on Draft PR #390. It restates the audit from current `main@cbc6388e8607bb92120281a9a15148577994d3a6`, consumes merged P2 coordinator promotion #450, and refreshes live P0, RUNTIME and worldmap heads without promoting Draft-only lane evidence into canonical programme truth.

## Authority and nonclaims

This audit is GitHub/repository evidence work only. It did not use Synology, inspect/start an official client, attach to process memory, access canonical lease/registration/session state, or observe X11/VNC/network/login/gameplay directly.

Exact historical installed-client fence used by Track A evidence:

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

Current-main canonical RUNTIME task remains `raw-xres-helper-hosted-ready` and explicitly records `exact_client_pid_ownership_of_viewable_xid: UNKNOWN`, `raw_xres_helper_implementation_validated: false`, and `physical_identity_retry_authorized: false`. Live source PR #447 has validated the pure raw-XRes helper, but coordinator promotion PR #448 is still open; Draft evidence is not treated as trusted-main implementation.

## Accepted historical quantitative baseline

Closed-unmerged PR #304 head `43a60bd96cc644b656b200c9edbfb75578b330b6` remains the accepted bounded denominator source. Its machine-readable registry package is still absent from current main.

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

Current-main searches again found no canonical `capabilities.jsonl`, `protocol_messages.jsonl` or `runtime_types.jsonl` files.

## Current-main / live-state delta

### P1 promotion gap remains resolved

Coordinator promotion PR #414 merged as `070a066488d22126483e13fc8a08b17df5090918`; source #372 is closed superseded. Live attached-session correlation, restart/relogin stability and authoritative runtime values remain RUNTIME-owned and unproven.

### RUNTIME helper is validated in Draft, not yet promoted

Trusted main still contains canonical task phase `raw-xres-helper-hosted-ready`. The current live dependency has advanced:

- source PR #447 head `32c61120b9086904b328e7b4aa50526d64bef807` validated a pure QueryVersion/QueryClientIds(LocalClientPid) byte codec with deterministic fixtures;
- coordinator promotion PR #448 head `08f7c2e7946a2283f5d0a4f5c68ab4eb589b197b` is open and not merged;
- exact resource-to-official-client PID ownership therefore remains UNKNOWN on trusted main;
- physical identity retry remains forbidden until the helper is promoted and a fresh separately admitted RUNTIME discriminator exists.

The live RUNTIME blocker remains exact resource-to-official-client PID ownership, not generic graphics startup.

### Exact-static evidence production is no longer a material staging blocker

P0 producer #435 is merged on main and proves the task-scoped exact-fence → sanitized-source → GitHub-hosted decode pattern without promoting semantic player XYZ. This remains sufficient to close the former material exact-static staging gap.

Worldmap producers have advanced further in live Draft closeout:

- #437 head `3b6942ba543fec499d43c0697debfe80eb19471a` is Ready/terminal-closeout, promoting durable exact-static evidence only;
- #446 head `be0149bf59226194001ce24cda2743dbb6492bca` is Ready/terminal-closeout, promoting durable downstream exact-static evidence only.

Neither open producer is treated as merged current-main truth.

### P0 direct authoritative XYZ remains unproven

P0 #302 head `3ddf4f35e00cdfe899b4ce3daf716d71b4c3cce6` has already consumed merged producer #435 and now explicitly reports:

```text
WAITING_ON_RUNTIME_SEMANTIC_CONFIRMATION / DRAFT_NOT_PROMOTED
```

The former static-input blocker is closed. Direct authoritative XYZ remains `UNKNOWN / INCONCLUSIVE` because physical causal correlation requires a proven exact-client resource/PID identity and separately admitted RUNTIME execution.

### P2 bounded downstream chain is now promoted on main

The prior #390 statement that #310 was merely a partial open Draft is superseded.

Coordinator promotion #450 merged as current `main@cbc6388e8607bb92120281a9a15148577994d3a6`. Source #310 and one-shot producer #449 are archived and closed unmerged. Current-main durable evidence now promotes the bounded chain:

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

This resolves coordinator findings `TACOORD-390-20260817-001` and `TACOORD-390-20260817-002` for the current refresh. It does not close any of this audit's five material programme findings.

### Worldmap static dependency discovery is READY in live Draft, not promoted mutation design

Live #367 head `f381cd657642ce592b2cbbc95783813ae72fcf6a` now reports:

```yaml
static_classification: STATIC_DEPENDENCY_GRAPH_RECOVERED
STATIC_PATCH_GRAPH_READY: true
MUTATION_DESIGN_READY: false
client_byte_mutation_authorized: false
remaining_static_blocker: NONE_FOR_STATIC_DEPENDENCY_DISCOVERY
```

The recovered Draft graph includes the hardcoded packed `18/14` Handler source, Storage slot-12 propagation, dynamic Viewport geometry, RenderProvider fixed-32 clipping/indexing and Picker fixed-32 transforms. Camera has exact identity/layout plus a bounded negative result for a direct extent edge.

This corrects the prior report's `STATIC_PATCH_GRAPH_READY=false` statement. It does not claim that #367 or producer closeouts #437/#446 are merged, nor that mutation design or physical validation is authorized.

### Durable global coordinator checkpoint remains materially stale

Current main still contains `docs/agents/tasks/active/OTC-20260816-track-a-promotion-coordination.md` with `base_main: ddf7dd9408116fbeaca05bfeb69663f30f7cd34f` and old P1/RUNTIME/P2 barriers.

Merged #450 added a current P2-specific barrier at:

`docs/agents/evidence/OTC-20260816-track-a-promotion-coordination/20260817-p2-network-barrier-update.md`

That fixes P2 local continuation but does not refresh the global coordinator task. AUD-COV-007 therefore remains open.

## Current open material findings

### AUD-COV-001 — HIGH — canonical item-level coverage registry absent from current main

No canonical `capabilities.jsonl`, `protocol_messages.jsonl` or `runtime_types.jsonl` package is present on `main@cbc6388e...`.

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

The raw-XRes helper is validated in source Draft #447, but trusted main still lacks the promoted helper and direct resource-to-official-client PID proof. No current canonical Gate-B/registered-session semantic proof is promoted.

**Impact:** authoritative `IN_GAME`, direct XYZ causality, live P1 correlation, accepted actions and restart/relogin stability cannot be counted complete.

**Next discriminator:** finish coordinator promotion #448 onto current main with current-main freshness and exact-head checks; then create one separately admitted physical resource-to-PID discriminator. Only after direct identity proof may canonical semantic experiments resume.

### AUD-COV-007 — MEDIUM — durable global coordinator checkpoint materially stale

The active coordinator task still advertises `ddf7dd...` and obsolete global barriers. The new #450 P2 barrier is lane-local only.

**Impact:** repository-resolved continuation can select stale work unless every invocation reconstructs live Git.

**Next discriminator:** refresh the durable coordinator task from current main, preserving lane-local accepted barriers and live open promotion dependencies.

## Resolved / reclassified since prior #390 handoff

| Prior state | Current disposition |
|---|---|
| AUD-COV-006 P1 not promoted | `RESOLVED`: #414 merged; #372 closed superseded |
| AUD-COV-005 no compliant exact-static evidence path | `RESOLVED_AS_MATERIAL_GAP`: #435 promoted a compliant bounded pattern |
| P2 #310 open/partial-only | `SUPERSEDED`: #450 merged bounded P2 chain; framing/crypto/egress still UNKNOWN |
| viewport static graph incomplete | `SUPERSEDED_IN_LIVE_DRAFT`: #367 now reports `STATIC_PATCH_GRAPH_READY=true`; mutation design still false |
| raw-XRes helper not yet implemented/validated | `SUPERSEDED_IN_LIVE_DRAFT`: #447 validates helper; #448 promotion remains open |
| xkbcomp/Xvfb current RUNTIME blocker | `SUPERSEDED`: current frontier remains resource-to-PID identity |

## Missing-proof queue ordered by information gain

| Priority | Missing proof | Owner | Smallest next step |
|---:|---|---|---|
| 1 | canonical machine-readable coverage registry | COVERAGE-AUDIT + coordinator | promote/regenerate `capabilities`, `protocol_messages`, `runtime_types`, provenance, supersessions and validator from current main |
| 2 | full 349-message semantic/family classification | protocol/COVERAGE-AUDIT | E51 classify every identifier or explicit `UNCLASSIFIED` |
| 3 | full Tibia-owned QMeta/runtime denominator | QMeta/COVERAGE-AUDIT | E52 enumerate/classify every relevant type/controller/storage or ignored-with-reason |
| 4 | normalized P0/P1 item denominators | COVERAGE-AUDIT + lane owners | materialize every read/action/field item including UNKNOWN/restart state |
| 5 | current global coordinator barrier | coordinator | replace stale `ddf7dd` active checkpoint with current live state |
| 6 | raw XRes helper promotion | RUNTIME/coordinator | restack/promote accepted #447 helper via #448 with current-main exact-head validation |
| 7 | exact XID -> official-client PID identity | RUNTIME physical | separately admitted resource-to-PID discriminator after helper promotion |
| 8 | P0 direct authoritative XYZ | P0 + RUNTIME | execute bounded world/negative-control correlation only after identity proof |
| 9 | structural current `IN_GAME` + live P1 correlation | RUNTIME + promoted P1 | bounded proof only after identified canonical session exists |
| 10 | restart/relogin stability | RUNTIME + P0/P1 | fresh PID/PIE/session reacquisition and repeated semantic correlation |
| 11 | P2 framing/sequence/compression/encryption/final egress | P2 | continue one exact stage at a time from merged #450 evidence |
| 12 | action/QMeta denominator normalization | COVERAGE-AUDIT/QMeta | reconcile 612 vs 1004 provenance |
| 13 | worldmap promotion / mutation-design boundary | coordinator + worldmap | terminally review #367/#437/#446, promote durable static graph if accepted, then use a separately authorized mutation-design/physical-validation task |

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
canonical_raw_xres_helper_promoted: false
canonical_resource_to_pid_identity_proven: false
canonical_physical_runtime_semantics_proven: false
restart_relogin_stability_proven: false
stable_live_bridge_semantics_proven: false
worldmap_static_patch_graph_ready_in_live_draft: true
worldmap_static_patch_graph_promoted_to_main: false
worldmap_mutation_design_ready: false
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
  inventory_vs_semantic_boundary_preserved: true
  draft_lane_evidence_promoted_without_merge: false
e2e:
  result: NOT_APPLICABLE_WITH_REASON
  reason: documentation/evidence-only COVERAGE-AUDIT with runtime_access none; physical E2E belongs to separately admitted RUNTIME work
```

## Researcher delivery boundary

This package remains `DRAFT_NOT_PROMOTED`. Coordinator review must choose `ACCEPT | ACCEPT_WITH_EDITS | RETURN_FOR_EVIDENCE | REJECT/SUPERSEDE`. The researcher does not merge or change global programme truth.
