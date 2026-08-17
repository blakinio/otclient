# OTCLIENT-TIBIA-RE Track A coverage / contradiction / missing-proof audit refresh

## Status

```yaml
task: OTC-20260816-track-a-coverage-audit-refresh
lane: COVERAGE-AUDIT
current_registry_integration_task: OTC-20260817-track-a-canonical-coverage-registry
current_registry_integration_pr: 454
snapshot_main_before_registry_integration: d9529da35ada6ab2a7bf4d2e70205cc0dd7b14ab
audit_result: FAIL_MATERIAL_GAPS_OPEN
programme_complete: false
material_findings_open: 4
high_findings_open: 2
medium_findings_open: 2
runtime_access: none
physical_e2e: NOT_APPLICABLE_WITH_REASON
```

This is the coordinator-maintained audit after canonicalization of the accepted #304 machine-readable registry in PR #454. When this report is on `main`, `AUD-COV-001` is resolved by the canonical registry, provenance/supersession data, current-main overlay and deterministic validator. Four independent material findings remain.

## Authority and registry boundary

The immutable quantitative baseline comes from closed Draft #304 at exact head `43a60bd96cc644b656b200c9edbfb75578b330b6`, coordinator-disposed `ACCEPT_WITH_EDITS` as bounded inventory/provenance evidence only. Exact client fence:

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

Canonical files live under `docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/`. Historical baseline blobs are byte-for-byte fenced in `canonical-manifest.json`; programme-state changes live in `current-main-overlay.json`. Historical `next` fields are evidence, not current routing authority.

No inventory percentage is global semantic completion.

## Canonical quantitative boundary

| Metric | Numerator / denominator | Meaning |
|---|---:|---|
| generated protocol identifiers | 349 / 349 | inventory only; 189 inbound + 160 outbound |
| generated protocol directions | 349 / 349 | structural metadata only |
| direct inbound QMeta links | 27 / 349 | bounded structural links |
| generated-message semantic support | UNKNOWN / 349 | E51 required |
| protocol-handler QMeta inventory | 47 / 47 | bounded handler subset |
| raw direct Qt callsites | 2184 / 2184 | raw callsite inventory |
| raw direct Qt semantics | UNKNOWN / 2184 | incomplete |
| selected legacy QObject connect edges | 40 / 41 | selected subset |
| high-information GameAction sender metaobjects | 29 / 31 | selected subset; 1 mismatch + 1 unresolved |
| P0 top-level requirement groups | 16 / 16 | group registry only |
| P0 item-level live-read coverage | UNKNOWN / UNKNOWN | normalized denominator absent |
| bridge-v1 discovery targets | 7 / 7 | implementation inventory only |
| P1 item-level field/evidence coverage | UNKNOWN / UNKNOWN | normalized denominator absent |
| restart/relogin stability | UNKNOWN / 1 | not proven |

## Current-main overlay

### P2

Merged #450 proves the bounded downstream processor chain through `TProtocolClientMessageProcessor`, `TGameserverNetworkPacketRawDataProcessor` and the same-message handoff to `TGameserverDualConnection`; stage order is `PROVEN_PARTIAL`. Framing, sequence, compression, encryption, final binary egress and final socket ownership remain `UNKNOWN`.

### Worldmap

The static graph, mutation-design PR #452 and archive #453 are promoted. Current boundary:

```yaml
STATIC_PATCH_GRAPH_READY: true
MUTATION_DESIGN_READY: true
SAFE_MUTATION_PROVEN: false
PHYSICAL_VALIDATION_EXECUTION_AUTHORIZED: false
client_byte_mutation_authorized: false
```

### RUNTIME / P0

Raw-XRes helper promotion #448 is now merged as `d9529da35ada6ab2a7bf4d2e70205cc0dd7b14ab`. That resolves the hosted-helper promotion dependency but **does not** prove exact XID→official-client PID ownership or canonical runtime semantics.

Current nonclaims remain:

```yaml
current_canonical_display: UNKNOWN
current_canonical_vnc_endpoint: UNKNOWN
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
current_canonical_gate_b: NOT_PROVEN
current_structural_in_game: NOT_PROVEN
```

The next RUNTIME discriminator is one fresh separately admitted physical XRes resource→PID identity check using the promoted helper. Canonical bootstrap retry, window-identity relaxation, credentials/login/gameplay remain unauthorized until the governing runtime task admits them. P0 direct authoritative XYZ remains `UNKNOWN / INCONCLUSIVE` pending physical identity and bounded causal correlation.

## Resolved finding

### AUD-COV-001 — RESOLVED — canonical item-level coverage registry present

PR #454 promotes:

- canonical `capabilities.jsonl`, `protocol_messages.jsonl`, `runtime_types.jsonl`;
- exact #304 provenance and retained `DISPROVEN/SUPERSEDED` / `UNKNOWN` evidence;
- exact source Git-blob fences;
- current-main overlay and current coverage summary;
- permanent GitHub-hosted deterministic validator workflow.

This resolves **registry availability and deterministic recomputability only**. It does not resolve semantic denominator or runtime findings.

## Current open material findings

### AUD-COV-002 — HIGH — required semantic denominators remain incomplete

E51 full 349-message semantic/family classification, E52 full Tibia-owned QMeta/runtime classification, P0 item-level read/action denominator and P1 item-level field/evidence denominator remain incomplete.

**Next discriminator:** execute E51/E52 against the canonical registry and materialize normalized P0/P1 item registries while retaining explicit `UNCLASSIFIED/UNKNOWN` entries.

### AUD-COV-003 — MEDIUM — action/QMeta denominator conflict `612` vs historical `1004`

The values come from different inventory/filter definitions and no single versioned denominator reconciles them.

**Next discriminator:** reconstruct/deprecate the historical `1004` definition with provenance, then version one named denominator.

### AUD-COV-004 — HIGH — canonical live semantic/restart proof remains unavailable

The hosted raw-XRes helper is now promoted, but direct resource→official-client PID identity, a current registered/Gate-B session, authoritative `IN_GAME`, direct XYZ causality, live P1 correlation and restart/relogin stability remain unproven.

**Next discriminator:** create one fresh separately admitted physical resource→PID discriminator using the promoted helper. Canonical semantic experiments resume only after direct identity proof.

### AUD-COV-007 — MEDIUM — durable global coordinator checkpoint materially stale

The global promotion-coordinator task remains older than current programme state; lane-local corrections do not replace a coherent global checkpoint.

**Next discriminator:** refresh the durable global coordinator task from current main while preserving accepted lane evidence and live dependencies.

## Missing-proof queue by information gain

1. E51 full 349-message semantic/family classification.
2. E52 full Tibia-owned QMeta/runtime denominator.
3. Normalize P0/P1 item-level denominators.
4. Reconcile action/QMeta `612` vs `1004` provenance.
5. Fresh physical XRes XID→official-client PID identity under RUNTIME admission.
6. Refresh global coordinator checkpoint.
7. P0 authoritative XYZ and structural `IN_GAME` / live P1 correlation.
8. Restart/relogin stability.
9. P2 framing/sequence/compression/encryption/final egress.
10. Worldmap physical validation only under separately authorized mutation/runtime work.

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
canonical_raw_xres_helper_promoted: true
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
