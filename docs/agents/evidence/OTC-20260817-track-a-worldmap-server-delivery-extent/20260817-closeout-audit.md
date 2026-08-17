# OTC-20260817 — independent closeout audit: server-delivered worldmap extent

```yaml
audit_date: 2026-08-17
repository: blakinio/otclient
task: OTC-20260817-track-a-worldmap-server-delivery-extent
pr: 473
audit_base: f99ec371bafd0b9dbccb8fd6f4c8a3137e7d963b
audited_head: 5a1f42ebb8b0eac061229f08774f87c16def2511
prompt_contract: docs/agents/prompts/OTCLIENT_TIBIA_RE_WORLDMAP_MUTATION_DESIGN.md@1.1.0
execution_class: github_hosted
runtime_access: none
material_findings: 0
resolved_findings: 1
result: PASS
```

## Audit method

This audit re-read the current durable diff and the v1.1.0 server-delivered-map acceptance rather than treating the researcher summary as proof. It checked the final classifications against the direct exact-client evidence and tested for common overclaims: inferring server capability from client Storage/render capacity, treating message names as field schemas, treating `TopFloor`/`BottomFloor` as whole-floor proof, treating adjacent-floor retained observations as one atomic bulk message, or interpreting absence in a filtered protocol list as a global absence claim.

At the audited head, comparison against `main@f99ec371bafd0b9dbccb8fd6f4c8a3137e7d963b` contains only durable task/report/evidence files. The temporary GitHub-hosted producer was removed before this audit.

## Acceptance audit

### Required result flags

**PASS.** The report and task persist exactly:

```text
SERVER_MAP_DELIVERY_MODEL=UNKNOWN
SERVER_LARGER_RECTANGLE_SUPPORTED=UNKNOWN
SERVER_FULL_FLOOR_DELIVERY_SUPPORTED=UNKNOWN
SERVER_MULTI_FLOOR_BULK_DELIVERY_SUPPORTED=UNKNOWN
SERVER_WHOLE_MAP_DELIVERY_SUPPORTED=UNKNOWN
MAX_SERVER_DELIVERABLE_EXTENT=UNKNOWN
```

The prompt explicitly permits `UNKNOWN` where direct evidence cannot prove a stronger value. No unsupported `false`, `true`, fixed-protocol or server-driven value is substituted.

### Storage / render / server-delivery separation

**PASS.** The final report has three independent extent planes: client Storage, rendered/interactive extent, and server-delivered gameplay extent. No local capacity conclusion is promoted into a server-delivery capability claim.

### Exact message directionality

**PASS.** Run `32022209943`, job `95364071999`, producer head `553e447c0662892b0c1b9cab994c4545d09f22c8`, retained artifact `9285763750`, gives the complete generated-message-name census: 349 total, 160 client->server and 189 server->client. `GameserverMessageFullMap`, `FieldData`, directional row/column, floor and object-map mutation families are inbound/server->client.

The report correctly limits the outbound negative result to generated-message names: no client->server generated name contains `aware|range|extent|viewport|fullmap|fielddata|width|height`. It does not claim that generic outbound messages lack relevant fields.

### Generic outbound field / negotiation boundary

**PASS.** The final targeted descriptor probe, run `32022973229`, job `95366330613`, producer head `ae5778d1f8b0e79b77bfa68c14692a3d599b25c5`, completed successfully and retained artifact `9286040543`. It validates the raw descriptor parser against exact `Coordinate{x,y,z:uint32}` but does not recover exact descriptors for `Extent`, generic outbound targets, or the map-delivery server messages.

The final result therefore preserves `OUTBOUND_GENERIC_MESSAGE_EXTENT_FIELD_CENSUS=NOT_RECOVERED` and `SERVER_MAP_DELIVERY_MODEL=UNKNOWN`. It does not infer absence from a failed recovery surface.

### Parser/network maximum

**PASS.** The task/report preserve the accepted earlier `network_payload_extent_ceiling=NOT_RECOVERED` boundary and do not invent a maximum. `MAX_SERVER_DELIVERABLE_EXTENT=UNKNOWN` is the only supported value from the authorized static evidence.

### Larger rectangle / whole floor / multi-floor / whole map

**PASS.** The report does not convert `FullMap`, `TopFloor`, `BottomFloor`, row/column names or local cache/minimap capability into unsupported server capability. Re-inspected retained strip data is explicitly bounded as baseline-consistent observation, not an atomic packet trace. All four capability flags remain `UNKNOWN`.

### Runtime discriminator

**PASS.** The report defines one separately authorized causal experiment that compares baseline exact client versus the already-designed first `[19,14]` mutation while measuring the authoritative inbound envelope before Storage, generic outbound serialization, and Storage/render/picker separately. It includes negative control, rollback and stop criteria. The current task does not execute that experiment.

### Authorization / trust / safety

**PASS.** No physical runtime/login/relogin was performed by this task; no official client bytes were modified; no raw client was committed; Synology was not used as static-analysis fallback; no owner-funded Codex/OpenAI API/paid AI quota was used; third-party OTClient behavior was not promoted as official-server proof.

### Temporary resource cleanup

**PASS.** `.github/workflows/track-a-worldmap-server-delivery-static.yml` was removed at commit `174def652ae494f337897d79996ec7c8a47408cf`. The audited diff contains no workflow file or proprietary client bytes.

### E2E classification

**PASS.** `NOT_APPLICABLE_WITH_REASON` is consistent with task metadata (`e2e_required=false`, `RUNTIME_ACCESS=none`) and with the prompt's separate-authorization boundary for physical mutation/runtime validation. The static task closes with direct `UNKNOWN` values; it does not claim runtime validation of a larger-map feature.

## Resolved finding

### F-01 — stale descriptor status in first census evidence

**Severity:** low/documentation consistency.

The first message-census evidence still said `OUTBOUND_GENERIC_MESSAGE_EXTENT_FIELD_CENSUS: pending_descriptor_probe` and described the descriptor producer as future work after that producer had already completed.

**Resolution:** commit `07c2056129db2fc93dafe3cbd311f3bc3be90f39` reconciled the file to `NOT_RECOVERED`, linked the completed targeted descriptor boundary and moved the remaining discriminator to the separately authorized physical experiment.

**Status:** resolved before this audit.

## Falsification attempts with no material finding

- Tried to derive `SERVER_DRIVEN` from inbound directionality: rejected because direction is not control semantics.
- Tried to derive `FIXED_PROTOCOL` from current 18-wide retained rows: rejected because one observed baseline does not prove a protocol maximum.
- Tried to derive `SERVER_MULTI_FLOOR_BULK_DELIVERY_SUPPORTED=true` from adjacent `z=6/z=7` observations: rejected because the retained TSV lacks atomic message boundaries.
- Tried to derive `SERVER_FULL_FLOOR_DELIVERY_SUPPORTED=true` from `TopFloor`/`BottomFloor` names: rejected because names do not establish payload extent.
- Tried to derive `SERVER_WHOLE_MAP_DELIVERY_SUPPORTED=false` from absence of evidence: rejected because bounded negative evidence is not a global impossibility proof.
- Tried to infer generic outbound field absence from raw descriptor non-recovery: rejected because the validated parser did not recover those exact protocol descriptors.

## Audit conclusion

```text
MATERIAL_FINDINGS=0
RESOLVED_FINDINGS=1
AUDIT_RESULT=PASS
```

The static server-delivery research package is internally consistent with prompt v1.1.0 and the repository trust/authorization boundaries. Remaining `UNKNOWN` values are evidence-bounded outputs. The next gate is exact-head changed-file/CI/review verification, not additional static evidence production.
