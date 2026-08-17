# OTCLIENT-TIBIA-RE Track A coverage / contradiction / missing-proof audit

## Status

```yaml
lane: COVERAGE-AUDIT
snapshot_main: ec75e2606f7f4ad834e4b6be968fb03bdbff55df
semantic_denominator_task: OTC-20260817-track-a-semantic-denominator-normalization
semantic_denominator_pr: 460
audit_result: FAIL_MATERIAL_GAPS_OPEN
programme_complete: false
material_findings_open: 3
high_findings_open: 1
medium_findings_open: 2
runtime_access: none
physical_e2e: NOT_APPLICABLE_WITH_REASON
```

The accepted #304 baseline remains immutable and exact-client fenced to official native Linux Tibia `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`. PR #454/#456 made that registry canonical; PR #460 adds finite denominator registries without rewriting baseline history or converting `UNKNOWN` into assumptions.

## Canonical quantitative boundary

```yaml
protocol_identifier_inventory: 349/349
protocol_direction_inventory: 349/349
E51 denominator: 349
protocol_semantic_support: UNKNOWN/349
protocol_direct_qmeta_structural_links: 27/349
E52 denominator: 642
full_tibia_qmeta_semantic_support: UNKNOWN/642
bounded_protocol_handler_subset: 47/47
direct_qt_callsite_inventory: 2184/2184
direct_qt_semantics: UNKNOWN/2184
P0 top_level_groups: 16/16 grouping_only
P0 item denominator: 180
P0_live_semantics: UNKNOWN/180
P1 discovery_target_subset: 7/7 implementation_subset
P1 item denominator: 28
P1_live_semantics: UNKNOWN/28
restart_relogin_stability: UNKNOWN/1
```

E51 is a complete denominator with deterministic lexical family normalization only; all 349 semantic states remain `UNKNOWN`. E52 comes from the full retained exact-client `tibia::` QMeta census run `31790507112`, job `94736106350`: 642 unique Tibia-owned records out of 708 structural records, with 66 non-Tibia records outside scope. The 642 rows partition into 303 `OTHER_QMETA`, 187 `CONTROLLER`, 77 `STORAGE`, 47 `HANDLER` and 28 `ACTION_HANDLER`; all semantic states remain `UNKNOWN`.

P0 normalizes the 16 programme headings into 180 individual read/state/action requirements. P1 normalizes the bridge contract into 28 individual identity/binding/read/discovery/health/lifecycle requirements. A finite denominator makes future coverage computable; it does not establish support.

## Current runtime / P0 frontier

Physical XRes resource ownership is no longer a missing prerequisite. PR #457 merged as `16c6fb695a85a6ba3a809fcf5b031ce4ac7e11fc`; run `32015479835`, job `95344000918` preserves a LocalClientPid reply matching the exact launched official-client PID. Identity archive #459 merged as `c55e3523e6e9d50df511e65dce9145a8f951a5f5`; helper client-base semantics were corrected by #461 at `1eb4a8edecba3966aa1e6155e241b404eb4d30cb`. PR #465 promoted the canonical raw-XRes window-identity integration as `f8e628a255a18ec92839bbb45ef0e3b40bef8605`.

PR #467 then performed the fresh post-#465 P0 controller-plane admission (run `32019313320`, job `95355423148`) and established the exact current blocker: canonical lease generation 7 is released and the authoritative runtime registration is `ABSENT`. No process/X11/client observation or mutation occurred. Therefore there is no legal existing canonical `IN_GAME` lifecycle for P0 to reuse, and P0-only bootstrap/login remains forbidden.

Current nonclaims/disposition:

```yaml
canonical_registration: ABSENT
canonical_lease_status: released
canonical_lease_generation: 7
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
current_canonical_gate_b: NOT_PROVEN
current_structural_in_game: NOT_PROVEN
P0_direct_authoritative_xyz: INCONCLUSIVE
P0_disposition: BLOCKED_NO_LEGAL_EXISTING_IN_GAME_LIFECYCLE
restart_relogin_stability: UNKNOWN
```

`AUD-COV-004` therefore remains open. Its next legal discriminator requires a separately authorized legitimate canonical lifecycle to exist and reach structurally verified `IN_GAME`; only then may a fresh RUNTIME admission and ownership/generation gates precede semantic experiments.

## P2 and worldmap boundaries

P2 retains the merged bounded processor chain and `PROVEN_PARTIAL` stage order. Framing, sequence, compression, encryption, final binary egress and final socket ownership remain `UNKNOWN`.

Worldmap static graph and mutation design are promoted. The separately authorized physical canary task is archived on main via #466. It proved bounded offline patch/startup/rollback but observed no handler canary in its no-login startup window: `NO_HANDLER_CANARY_OBSERVED_BOUNDED`. Therefore causal propagation and safe mutation remain unproven and no additional physical launch is authorized by this coverage task.

## Resolved findings

### AUD-COV-001 — RESOLVED — canonical machine-readable registry

PR #454/#456 promoted the exact source-fenced baseline, provenance/supersessions, current overlay and reusable validator.

### AUD-COV-002 — RESOLVED — finite semantic denominators materialized

PR #460 materializes:

- `protocol_message_semantics.jsonl`: 349/349 generated identifiers;
- `runtime_type_semantics.jsonl`: 642/642 retained Tibia-owned QMeta records;
- `p0_items.jsonl`: 180/180 normalized P0 requirements;
- `p1_items.jsonl`: 28/28 normalized P1 requirements.

Hosted generation run `32017799293`, job `95350885329`, artifact `9284175545`, digest `sha256:cf2fb874e39af2465de76445347a118077893d9bbf213b69809b793ed4d7f577` passed deterministic generation and artifact validation. Independent inspection matched the digest, counts, unique IDs, protocol 189/160 split, 27 direct QMeta links and full QMeta provenance. Integrated validator run `32018548728`, job `95353113344` passed the complete candidate tree.

Resolution is **denominator completeness only**. Protocol semantics remain `UNKNOWN/349`, full QMeta semantics `UNKNOWN/642`, P0 live semantics `UNKNOWN/180`, and P1 live semantics `UNKNOWN/28`.

## Current open material findings

### AUD-COV-003 — MEDIUM — action/QMeta denominator definition conflict `612` vs historical `1004`

The values represent different historical inventory/filter definitions and remain non-comparable.

**Next discriminator:** reconstruct/deprecate the historical `1004` definition with provenance and version one named denominator against the current 612 inventory.

### AUD-COV-004 — HIGH — current canonical live semantic/restart proof unavailable

Identity tooling and historical isolated resource→PID proof are promoted, but #467 proves the authoritative canonical registration is currently absent. No legal existing `IN_GAME` lifecycle can be reused, so authoritative player/world semantics, direct XYZ, live P1 correlation and restart/relogin stability remain unproven.

**Next discriminator:** wait for a separately authorized legitimate canonical lifecycle to exist and reach structurally verified `IN_GAME`; then perform fresh RUNTIME admission and ownership/generation gates before semantic experiments. Do not bootstrap/login solely for P0.

### AUD-COV-007 — MEDIUM — durable global coordinator checkpoint materially stale

The global promotion-coordinator checkpoint is older than current promoted lane state.

**Next discriminator:** refresh it from current main without discarding accepted lane evidence or current blockers.

## Campaign completeness verdict

```yaml
canonical_machine_readable_coverage_registry_present: true
protocol_denominator_complete: true
protocol_semantic_coverage_complete: false
full_qmeta_runtime_denominator_complete: true
full_qmeta_runtime_semantics_complete: false
p0_item_level_denominator_complete: true
p0_live_semantics_complete: false
p1_item_level_denominator_complete: true
p1_live_semantics_complete: false
physical_resource_to_exact_client_pid_identity_proven_for_historical_run: true
canonical_raw_xres_window_identity_integration_promoted: true
canonical_registration_current: false
canonical_current_runtime_semantics_proven: false
p2_transport_semantics_complete: false
worldmap_mutation_design_ready: true
worldmap_physical_canary_executed: true
worldmap_causal_propagation_proven: false
programme_complete: false
```

## Audit / E2E classification

```yaml
audit:
  result: FAIL_MATERIAL_GAPS_OPEN
  material_findings_open: 3
  high: 1
  medium: 2
  AUD-COV-001: RESOLVED_BY_CANONICAL_REGISTRY
  AUD-COV-002: RESOLVED_BY_FINITE_DENOMINATORS
  denominator_complete_not_semantic_complete: true
e2e:
  result: NOT_APPLICABLE
  reason: deterministic repository coverage/denominator integration; physical gameplay/runtime E2E belongs to separately admitted RUNTIME work
```
