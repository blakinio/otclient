# OTCLIENT-TIBIA-RE Track A coverage / contradiction / missing-proof audit refresh

## Status

```yaml
task: OTC-20260816-track-a-coverage-audit-refresh
lane: COVERAGE-AUDIT
researcher_delivery: draft_only
snapshot_main: 8c9486e2c6109a7a39b564804c8acd707659b5e0
snapshot_time: 2026-08-17T08:31:00+02:00
audit_result: FAIL_MATERIAL_GAPS_OPEN
programme_complete: false
material_findings_open: 5
high_findings_open: 3
medium_findings_open: 2
runtime_access: none
physical_e2e: NOT_APPLICABLE_WITH_REASON
```

This refresh answers coordinator `RETURN_FOR_EVIDENCE` on Draft PR #390 and includes the main-advance that landed P0 Cyclopedia exact-client evidence in #435 during final validation. It preserves the accepted bounded #304 denominators, updates only live-state conclusions that changed, and does not promote Draft lane evidence into global programme truth.

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

Isolated graphics/X11/XRes evidence is not canonical registration, PID ownership, `IN_GAME`, accepted movement, restart stability or gameplay semantic proof.

## Accepted historical quantitative baseline

Closed-unmerged PR #304 head `43a60bd96cc644b656b200c9edbfb75578b330b6` remains the accepted bounded item-level denominator source. Its machine-readable registry package is still absent from current main.

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

Historical P0 group-stage distribution remains `7 INVENTORIED / 6 STRUCTURALLY_IDENTIFIED / 1 SEMANTICALLY_SUPPORTED / 2 UNKNOWN`; it is not item-level live coverage.

## Current-main delta

### P1 promotion gap is resolved

Coordinator promotion PR #414 merged as `070a066488d22126483e13fc8a08b17df5090918`; source #372 is closed superseded. The accepted P1 implementation/profile/test surface is therefore promoted.

Live attached-session correlation, restart/relogin stability and authoritative runtime values remain RUNTIME-owned and unproven. Those belong under the live semantic/restart finding, not a separate P1 promotion finding.

### RUNTIME is at raw XRes resource-to-PID identity frontier

The old xkbcomp-era #390 snapshot is obsolete. Current promoted chain includes:

- coordinator-required #415 isolated evidence: Xvfb advertised no GLX extension; Qt discovered/loaded bundled `xcb_glx`, then reported neither GLX nor EGL enabled; Vulkan initialized; no visible window through 35 seconds. This remains isolated/non-canonical historical evidence.
- contained DRI provider repair and revalidation (#429/#430, #431/#432/#434) removed the earlier missing-GLX environment condition without proving canonical success.
- admission reconciliation #436 merged as `b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4`, keeping blind retry forbidden.
- accepted post-RHI raw X11 evidence proves a raw viewable `1920x1080` XID `0x00c00011` while normal xdotool named-visible search is zero; exact official-client PID ownership remains UNKNOWN.
- XRes evidence proved convenience `libxcb-res`/`libXRes` helpers unavailable but contained `XResproto` wire definitions present.
- coordinator promotion #444 merged the audited raw-X11/XRes chain; #445 archived child tasks and moved the canonical task to `raw-xres-helper-hosted-ready`.

Current canonical task requires a **GitHub-hosted QueryVersion/QueryClientIds encoder/parser** before any new physical identity attempt. Physical identity retry, canonical bootstrap retry, window-identity relaxation, credentials, login and gameplay are forbidden until that hosted helper is validated and separately admitted.

The live blocker is therefore exact resource-to-official-client PID ownership, not generic graphics startup.

### Exact-static evidence production is now a proven promoted process, not a material staging blocker

The old finding that no compliant exact-static evidence path exists is resolved.

Worldmap producer #437 proved a bounded process:

```text
read-only exact-client source-window staging
→ sanitized artifact only
→ GitHub-hosted disassembly/recovery/validation
→ no raw client upload
→ no client execution/mutation
```

Consumer #367 used that producer and explicitly resolved its prior exact-static staging blocker.

During this audit's final validation, P0 producer closeout #435 merged as `8c9486e2c6109a7a39b564804c8acd707659b5e0`. It promotes the final sanitized Cyclopedia structural bundle for consumer #302:

- source run `32000921225` SUCCESS;
- hosted validation SUCCESS;
- artifact `9278368790`, digest `sha256:49f48d4283e63dd613b32a99300dc86eb98d68d7d7f640ec621c72e854c30c87`;
- 9 target labels, 0 missing;
- 4 direct relocations;
- one typeinfo candidate `0x3089a50`;
- vtable address point `0x3089db0`;
- 4 unique RIP xrefs and 4 hosted disassembly windows.

The bundle explicitly states `SEMANTIC_PLAYER_XYZ_PROVEN=false`. Thus static evidence delivery is proven and promoted, while semantic XYZ remains open. A generalized full-binary hosted service is no longer required to unblock current static lanes and is removed from the material finding set.

### P0 direct authoritative XYZ remains unproven, but its static bundle is now on main

P0 #302 still classifies direct authoritative XYZ as `UNKNOWN / INCONCLUSIVE`; its branch has not yet consumed newly merged #435.

The Cyclopedia route now has promoted exact-client structural evidence on main, but it still proves structure/metadata only. Physical XYZ/world correlation, negative controls, exact client PID/session identity, repeatability and fresh-PID/relogin stability remain solely RUNTIME-owned.

The next P0 action is no longer "obtain a compliant bundle"; it is **consume promoted #435 and determine what exact semantic/member/accessor inference is justified**, keeping physical confirmation separate.

### P2 remains partial Draft evidence

P2 #310 head `9b99b6b4bda2cf01e8fadcd8a00a6827de35d825` remains Draft-only and supports:

```yaml
persistent_qbuffer_to_readAll: PROVEN
first_downstream_consumer: PROVEN:TProtocolClientMessageProcessor+0x10@0xc2df80
first_downstream_transform: PROVEN:TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
same_message_handoff_to_dual_connection: PROVEN
protocol_stage_order: PROVEN_PARTIAL
framing: UNKNOWN
sequence: UNKNOWN
compression: UNKNOWN
encryption: UNKNOWN
final_binary_egress: UNKNOWN
```

No framing/crypto/egress completion is promoted here.

### Viewport/worldmap advanced materially but is not patch-ready

Draft #367 head `a69179e5cf4681a9d41014a562a0bfd0d1cd9ffb` consumes #437 and directly identifies exact `TWorldmapProtocolMessageHandler`, `TWorldMapStorage` and counted Storage control block. The historical 18x14 object is corrected to exact Storage extent state, not Viewport.

Remaining work includes the upstream Storage slot-12 source, RenderProvider clipping/culling, Camera projection/scale, Picker transforms, fixed allocation/loop/mask/packing sites and a safe patch-site graph. `STATIC_PATCH_GRAPH_READY=false` remains correct.

### Durable coordinator checkpoint remains materially stale

`docs/agents/tasks/active/OTC-20260816-track-a-promotion-coordination.md` on current main still records `base_main: ddf7dd...`, old #357/#358/#360/#356 barriers and pre-#414/pre-#445 conclusions.

Live Git overrides it, but the durable mismatch remains a material continuation risk.

## Current open material findings

### AUD-COV-001 — HIGH — canonical item-level coverage registry absent from current main

Current-main search still finds no canonical `capabilities.jsonl`, `protocol_messages.jsonl` or `runtime_types.jsonl` package.

**Impact:** coverage cannot be deterministically recomputed from canonical current-main state.

**Next discriminator:** coordinator-promote/regenerate provenance-preserving registries plus validator, retaining UNKNOWN/DISPROVEN/SUPERSEDED entries.

### AUD-COV-002 — HIGH — required semantic denominators remain incomplete

E51 full 349-message family/semantic classification, E52 full Tibia-owned QMeta/runtime classification, P0 item-level read/action denominator and P1 global field/evidence denominator remain absent.

**Impact:** inventory/subset completion can still be confused with semantic programme completion.

**Next discriminator:** execute E51/E52 against the canonical registry and materialize normalized P0/P1 item registries.

### AUD-COV-003 — MEDIUM — action/QMeta denominator conflict `612` vs historical `1004`

The durable census still states these came from different inventory/filter definitions.

**Impact:** action coverage percentages remain non-comparable.

**Next discriminator:** reconstruct/deprecate the historical 1004 definition with provenance, then version one named denominator.

### AUD-COV-004 — HIGH — canonical live semantic/restart proof remains unavailable

Promoted isolated evidence has advanced to raw X11 resource identity, but exact resource-to-official-client PID ownership remains UNKNOWN and no current canonical Gate-B/registered-session semantic proof is promoted.

**Impact:** authoritative `IN_GAME`, direct XYZ causality, live P1 correlation, accepted actions and restart/relogin stability cannot be counted complete.

**Next discriminator:** implement/validate the hosted raw-XRes QueryVersion/QueryClientIds helper; then perform one separately admitted physical resource-to-PID identity discriminator. Only after direct identity proof may canonical semantic experiments resume.

### AUD-COV-007 — MEDIUM — durable coordinator checkpoint materially stale

The coordinator task still advertises `ddf7dd...` and obsolete barriers.

**Impact:** repository-resolved continuation can select stale work unless every invocation reconstructs live Git.

**Next discriminator:** refresh the durable coordinator checkpoint from current main, including promoted P1 #414, current RUNTIME raw-XRes frontier, P0 #302 + merged producer #435, P2 #310 and viewport #367/#437.

## Resolved / reclassified since prior #390 handoff

| Prior state | Current disposition |
|---|---|
| AUD-COV-006 P1 not promoted | `RESOLVED`: #414 merged; #372 closed superseded |
| AUD-COV-005 no compliant exact-static evidence path | `RESOLVED_AS_MATERIAL_GAP`: #437 proved the process; #435 promoted the same pattern for P0 |
| xkbcomp/Xvfb current RUNTIME blocker | `SUPERSEDED`: current frontier is raw X11 resource-to-PID identity |
| #415 isolated no-GLX result as latest graphics state | `HISTORICAL_ACCEPTED`: later DRI/post-RHI evidence is the current frontier |

Previously resolved #360 transition, #356 QLibrary-validator and #363 viewport-prompt findings remain resolved.

## Missing-proof queue ordered by information gain

| Priority | Missing proof | Owner | Smallest next step |
|---:|---|---|---|
| 1 | canonical machine-readable coverage registry | COVERAGE-AUDIT + coordinator | promote/regenerate `capabilities`, `protocol_messages`, `runtime_types`, provenance, supersessions and validator from current main |
| 2 | full 349-message semantic/family classification | protocol/COVERAGE-AUDIT | E51 classify every identifier or explicit `UNCLASSIFIED` |
| 3 | full Tibia-owned QMeta/runtime denominator | QMeta/COVERAGE-AUDIT | E52 enumerate/classify every relevant type/controller/storage or ignored-with-reason |
| 4 | normalized P0/P1 item denominators | COVERAGE-AUDIT + lane owners | materialize every read/action/field item including UNKNOWN/restart state |
| 5 | current coordinator barrier | coordinator | replace stale `ddf7dd` checkpoint with current live state |
| 6 | raw XRes encoder/parser | RUNTIME hosted phase | deterministic QueryVersion/QueryClientIds encoder/parser + positive/negative/truncated/oversized/wrong-version fixtures |
| 7 | exact XID -> official-client PID identity | RUNTIME physical | separately admitted resource-to-PID discriminator after helper validation |
| 8 | P0 direct authoritative XYZ | P0 + RUNTIME | consume promoted #435, recover justified structural/member semantics, then live XYZ/world/negative controls after identity proof |
| 9 | structural current `IN_GAME` + live P1 correlation | RUNTIME + promoted P1 | bounded proof only after identified canonical session exists |
| 10 | restart/relogin stability | RUNTIME + P0/P1 | fresh PID/PIE/session reacquisition and repeated semantic correlation |
| 11 | P2 framing/sequence/compression/encryption/final egress | P2 | continue one exact stage at a time |
| 12 | action/QMeta denominator normalization | COVERAGE-AUDIT/QMeta | reconcile 612 vs 1004 provenance |
| 13 | viewport downstream patch graph | viewport #367 | Storage upstream + RenderProvider/Camera/Picker/fixed-bound windows before any mutation design |

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
p2_structural_chain_partial: true
p2_framing_sequence_compression_encryption_egress_complete: false
exact_static_task_scoped_producer_process_proven: true
canonical_resource_to_pid_identity_proven: false
canonical_physical_runtime_semantics_proven: false
restart_relogin_stability_proven: false
stable_live_bridge_semantics_proven: false
viewport_static_patch_graph_ready: false
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
  inventory_vs_semantic_boundary_preserved: true
  isolated_runtime_promoted_to_canonical: false
e2e:
  result: NOT_APPLICABLE_WITH_REASON
  reason: documentation/evidence-only COVERAGE-AUDIT with runtime_access none; physical E2E belongs to separately admitted RUNTIME work
```

## Researcher delivery boundary

This package remains `DRAFT_NOT_PROMOTED`. Coordinator review must choose `ACCEPT | ACCEPT_WITH_EDITS | RETURN_FOR_EVIDENCE | REJECT/SUPERSEDE`. The researcher does not merge or change global programme truth.