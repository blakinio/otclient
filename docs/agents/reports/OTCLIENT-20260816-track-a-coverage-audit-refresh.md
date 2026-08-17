# OTCLIENT-TIBIA-RE Track A coverage / contradiction / missing-proof audit refresh

## Status

```yaml
task: OTC-20260816-track-a-coverage-audit-refresh
lane: COVERAGE-AUDIT
current_registry_integration_task: OTC-20260817-track-a-canonical-coverage-registry
current_registry_integration_pr: 454
snapshot_main_before_registry_integration: 103d50277bc339760bdb531d89f8ec34cdd090cc
audit_result: FAIL_MATERIAL_GAPS_OPEN
programme_complete: false
material_findings_open: 4
high_findings_open: 2
medium_findings_open: 2
runtime_access: none
physical_e2e: NOT_APPLICABLE_WITH_REASON
```

This is the current coordinator-maintained coverage audit after canonicalization of the accepted #304 machine-readable registry in PR #454. When this report is on `main`, `AUD-COV-001` is resolved by the presence of the canonical registry, provenance/supersession data, current-main overlay and deterministic validator. The remaining four findings are independent and remain open.

## Authority and nonclaims

The registry baseline is exact accepted evidence from closed Draft #304, head `43a60bd96cc644b656b200c9edbfb75578b330b6`, fenced to official native Linux Tibia:

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Canonical entry points live under:

`docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/`

The baseline is intentionally immutable and historical. `current-main-overlay.json` carries programme-state changes so historical `next` values and earlier runtime/P2 wording are not mistaken for current authority.

Current runtime nonclaims remain:

```yaml
current_canonical_display: UNKNOWN
current_canonical_vnc_endpoint: UNKNOWN
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
current_canonical_gate_b: NOT_PROVEN
current_structural_in_game: NOT_PROVEN
```

## Canonical quantitative boundary

| Metric | Numerator / denominator | Meaning |
|---|---:|---|
| generated protocol identifiers | 349 / 349 | inventory only; 189 inbound + 160 outbound |
| generated protocol directions | 349 / 349 | structural metadata only |
| direct inbound QMeta links | 27 / 349 | bounded structural links |
| generated-message semantic support | UNKNOWN / 349 | E51 remains required |
| protocol-handler QMeta inventory | 47 / 47 | bounded handler subset |
| raw direct Qt callsites | 2184 / 2184 | raw callsite inventory |
| raw direct Qt semantics | UNKNOWN / 2184 | semantic classification incomplete |
| selected legacy QObject connect edges | 40 / 41 | selected subset |
| high-information GameAction sender metaobjects | 29 / 31 | selected subset; 1 mismatch + 1 unresolved |
| P0 top-level requirement groups | 16 / 16 | group registry only |
| P0 item-level live-read coverage | UNKNOWN / UNKNOWN | normalized denominator absent |
| bridge-v1 discovery targets | 7 / 7 | implementation inventory only |
| P1 item-level field/evidence coverage | UNKNOWN / UNKNOWN | normalized denominator absent |
| restart/relogin stability | UNKNOWN / 1 | not yet proven |

No `100%` value in this table is a global semantic-completion claim.

## Current-main overlay

### P2

Merged promotion #450 establishes the bounded downstream chain:

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

### Worldmap

The static dependency graph is promoted. Mutation-design PR #452 and its archive #453 are also on trusted main at snapshot `103d50277bc339760bdb531d89f8ec34cdd090cc`.

```yaml
STATIC_PATCH_GRAPH_READY: true
MUTATION_DESIGN_READY: true
SAFE_MUTATION_PROVEN: false
PHYSICAL_VALIDATION_EXECUTION_AUTHORIZED: false
client_byte_mutation_authorized: false
```

### P0 / RUNTIME

P0 direct authoritative XYZ remains `UNKNOWN / INCONCLUSIVE` pending separately admitted physical correlation after exact resource/PID identity.

Raw-XRes source #447 is validated. Promotion #448 remains open/unmerged at this snapshot (head `cbf19367a5f6aeab2916839f4af32a07030bd55c`), therefore trusted main does not yet have the helper and exact XID→official-client PID ownership remains `UNKNOWN`.

## Resolved finding

### AUD-COV-001 — RESOLVED — canonical item-level coverage registry present

PR #454 promotes the accepted machine-readable baseline plus:

- exact source Git-blob fences in `canonical-manifest.json`;
- current programme state in `current-main-overlay.json`;
- current `coverage-summary.json` and `blockers.json`;
- retained `UNKNOWN` and `DISPROVEN/SUPERSEDED` records;
- permanent GitHub-hosted deterministic validation.

The resolution is limited to **registry availability and deterministic recomputability**. It does not prove semantic denominators or runtime semantics.

## Current open material findings

### AUD-COV-002 — HIGH — required semantic denominators remain incomplete

E51 full 349-message semantic/family classification, E52 full Tibia-owned QMeta/runtime classification, P0 item-level read/action denominator and P1 item-level field/evidence denominator remain incomplete.

**Next discriminator:** execute E51/E52 against the canonical registry and materialize normalized P0/P1 item registries while retaining explicit `UNCLASSIFIED/UNKNOWN` entries.

### AUD-COV-003 — MEDIUM — action/QMeta denominator conflict `612` vs historical `1004`

The two values come from different inventory/filter definitions and no single versioned denominator reconciles them.

**Next discriminator:** reconstruct/deprecate the historical `1004` definition with provenance, then version one named denominator.

### AUD-COV-004 — HIGH — canonical live semantic/restart proof remains unavailable

Raw-XRes helper source #447 is validated but promotion #448 is not merged at this snapshot. Direct resource→official-client PID identity, current Gate-B session semantics, authoritative `IN_GAME`, XYZ causality and restart/relogin stability remain unproven.

**Next discriminator:** finish current-main #448 promotion; then create one separately admitted physical resource-to-PID discriminator before canonical semantic experiments resume.

### AUD-COV-007 — MEDIUM — durable global coordinator checkpoint materially stale

The global promotion-coordinator task remains older than current live programme state; lane-local corrections do not replace a coherent global checkpoint.

**Next discriminator:** refresh the durable global coordinator task from current main while preserving accepted lane-local evidence and live dependencies.

## Missing-proof queue by information gain

1. E51 full 349-message semantic/family classification.
2. E52 full Tibia-owned QMeta/runtime denominator.
3. Normalize P0/P1 item-level denominators.
4. Reconcile action/QMeta `612` vs `1004` provenance.
5. Refresh global coordinator checkpoint.
6. Promote raw-XRes helper #448.
7. Prove exact XID→official-client PID identity under fresh RUNTIME admission.
8. P0 authoritative XYZ and structural `IN_GAME` / live P1 correlation.
9. Restart/relogin stability.
10. P2 framing/sequence/compression/encryption/final egress.
11. Worldmap physical validation only under separately authorized mutation/runtime work.

## Campaign completeness verdict

```yaml
canonical_machine_readable_coverage_registry_present: true
protocol_identifier_inventory_complete: true
protocol_direction_inventory_complete: true
protocol_semantic_coverage_complete: false
full_qmeta_runtime_denominator_complete: false
p0_item_level_read_action_denominator_complete: false
p1_item_level_field_evidence_denominator_complete: false
p2_bounded_downstream_chain_promoted: true
p2_transport_semantics_complete: false
worldmap_static_patch_graph_promoted: true
worldmap_mutation_design_ready: true
worldmap_safe_mutation_proven: false
canonical_raw_xres_helper_promoted: false
canonical_resource_to_pid_identity_proven: false
canonical_physical_runtime_semantics_proven: false
restart_relogin_stability_proven: false
programme_complete: false
```

## Audit / E2E classification

```yaml
audit:
  result: FAIL_MATERIAL_GAPS_OPEN
  material_findings_open: 4
  high: 2
  medium: 2
  AUD-COV-001: RESOLVED_BY_CANONICAL_REGISTRY
  inventory_vs_semantic_boundary_preserved: true
e2e:
  result: NOT_APPLICABLE
  reason: registry/evidence integration is repository-only; physical gameplay/runtime E2E belongs to separately admitted RUNTIME work
```
