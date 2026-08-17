# OTCLIENT-TIBIA-RE Track A coverage / contradiction / missing-proof audit refresh

## Status

```yaml
task: OTC-20260816-track-a-coverage-audit-refresh
lane: COVERAGE-AUDIT
researcher_delivery: draft_only
snapshot_main: 55803133a5abe8b1e75e4660da1d2b84b154ab9a
snapshot_time: 2026-08-17T08:25:00+02:00
audit_result: FAIL_MATERIAL_GAPS_OPEN
programme_complete: false
material_findings_open: 6
high_findings_open: 3
medium_findings_open: 3
runtime_access: none
physical_e2e: NOT_APPLICABLE_WITH_REASON
```

This refresh answers coordinator `RETURN_FOR_EVIDENCE` on Draft PR #390. It preserves the bounded #304 denominator baseline, replaces superseded live-state conclusions with current-main evidence, and does not promote Draft-only lane evidence into canonical programme truth.

## Authority and nonclaims

This audit is GitHub/repository evidence work only. It did not use Synology, start or inspect an official client, attach to a process, observe X11/VNC/network/login/gameplay state, or access canonical lease/registration/session state.

Exact historical installed-client fence used by accepted Track A evidence:

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

The post-#405 graphics/X11/XRes work is isolated or support evidence unless a promoted record explicitly states otherwise. A raw viewable XID, QRhi/Vulkan initialization, GLX availability, or client-alive observation is not a canonical registration, PID ownership, `IN_GAME`, accepted movement, restart stability, or gameplay semantic proof.

## Accepted historical quantitative baseline

Closed-unmerged PR #304 head `43a60bd96cc644b656b200c9edbfb75578b330b6` remains the accepted bounded item-level denominator package. Its registries are still not present on current `main`, so it remains a provenance source rather than a canonical current-main registry.

| Metric | Numerator / denominator | Percentage | Boundary |
|---|---:|---:|---|
| generated protocol identifiers inventoried | 349 / 349 | 100% | identifier inventory only |
| generated protocol directions assigned | 349 / 349 | 100% | 189 inbound + 160 outbound |
| direct QMeta links in bounded protocol registry | 27 / 349 | 7.736% | not semantic completion |
| generated protocol semantic/family support | UNKNOWN / 349 | UNKNOWN | E51 still required |
| protocol-handler QMeta bounded inventory | 47 / 47 | 100% | bounded subset only |
| raw direct Qt selected inventory | 2184 / 2184 | 100% | semantic classification UNKNOWN / 2184 |
| selected legacy QObject connect edges | 40 / 41 | 97.561% | selected subset only |
| high-information GameAction sender metaobjects | 29 / 31 | 93.548% | one mismatch + one unresolved historically |
| P0 top-level requirement groups inventoried | 16 / 16 | 100% | group inventory only |
| P0 item-level read/action denominator | UNKNOWN / UNKNOWN | UNKNOWN | normalized registry absent |
| P1 global field/evidence denominator | UNKNOWN / UNKNOWN | UNKNOWN | normalized registry absent |
| restart-validated global capability denominator | 0 / UNKNOWN | not computable | normalized denominator absent |

Historical P0 group-stage distribution remains:

```yaml
INVENTORIED: 7
STRUCTURALLY_IDENTIFIED: 6
SEMANTICALLY_SUPPORTED: 1
UNKNOWN: 2
```

These values are not global semantic/read/action completion percentages.

## Current-main delta since coordinator RETURN_FOR_EVIDENCE

### P1 is now promoted on current main

Coordinator promotion PR #414 merged as `070a066488d22126483e13fc8a08b17df5090918`. Source PR #372 is closed superseded. The accepted P1 implementation/profile/test blobs are therefore no longer an unpromoted producer gap.

The promotion does **not** prove a live attached session, restart/relogin stability, authoritative runtime field values, or `session-status` correlation. Those remain RUNTIME-owned and are counted under the live semantic/restart finding rather than as a separate P1 promotion finding.

### RUNTIME moved from graphics startup failure to exact X11 resource-identity frontier

The old #390 xkbcomp-era snapshot is obsolete. Current promoted chain includes the following bounded facts:

- coordinator-required #415 evidence established, in an isolated task-owned display, that Xvfb advertised no GLX extension while Qt discovered/loaded bundled `xcb_glx`, then reported neither GLX nor EGL enabled; Vulkan initialized and no visible window appeared through 35 seconds. This was never canonical-runtime proof.
- graphics/DRI work subsequently promoted a contained Xvfb DRI-provider repair (#429/#430) and isolated client revalidation (#431/#432/#434), removing the earlier missing-GLX environment condition without claiming canonical success.
- admission reconciliation #436 merged as `b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4`, making the already-promoted bootstrap transaction governable while still forbidding blind retry.
- accepted post-RHI raw-X11 evidence (#438, promoted through #444) proves a raw viewable `1920x1080` XID `0x00c00011` while normal xdotool named-visible search remains zero; exact official-client PID ownership of that XID is still UNKNOWN.
- XRes child evidence (#442/#443) proved the convenience `libxcb-res`/`libXRes` helpers are unavailable while contained `XResproto` protocol definitions are present.
- coordinator promotion #444 merged the independently audited raw-X11/XRes evidence; lifecycle #445 moved the canonical task to `raw-xres-helper-hosted-ready` and archived the child tasks.

Current canonical task on `main@55803133...` explicitly requires a **GitHub-hosted raw-XRes QueryVersion/QueryClientIds encoder/parser** before another physical identity attempt. Physical client retry, canonical bootstrap retry, canonical window-identity relaxation, credentials, login and gameplay are currently forbidden.

Therefore the current blocker is no longer generic Xvfb/GLX startup. It is exact resource-to-PID ownership of the proven raw viewable X11 window, followed by separately admitted canonical/runtime semantic proof.

### Task-scoped exact-static evidence production is now proven

Old #390 finding `reusable GitHub-hosted exact installed-client staging unavailable` is materially narrowed.

Draft producer #437 proves a governance-compliant task-scoped pattern:

```text
physical read-only exact-client source window staging
→ sanitized artifact only
→ GitHub-hosted disassembly/recovery/validation
→ no raw client upload
→ no client execution/mutation
```

For worldmap, source run `31972743782` / job `95227595548` produced bounded exact windows, and hosted run `31972915689` validated the sanitized artifact. Consumer #367 explicitly marks its prior exact-static staging blocker resolved and has already recovered direct RTTI/object identity, correcting the historical 18x14 object to exact `TWorldMapStorage`.

This does **not** establish one canonical reusable full-binary hosted staging service. P0 still needs a separate compliant bounded producer for its missing `TCyclopediaMapStorage`/player-observer code windows. The systemic finding is therefore downgraded from HIGH to MEDIUM: a compliant production pattern exists, but it remains task-scoped and non-canonical.

### P0 direct authoritative XYZ remains open

P0 Draft #302 head `8812e58d6fc84b39460dd5a1c9de960d20c5b55b` still classifies direct authoritative player XYZ as `UNKNOWN / INCONCLUSIVE`.

New retained evidence improves the static route: exact metadata around `TCyclopediaMapStorage` includes `onPlayerPositionChanged`, `playerPositionChanged`, `TWorldMapCoordinate`, `onPlayerCreatureAddedToGameSession`, weak `TCreature`, `pPlayer`, and `onPlayerPositionWasUpdated`. The candidate observer chain is DERIVED; exact offsets/accessors are still UNKNOWN. The older `0x8367c1` body remains unstaged.

The next static discriminator is a compliant sanitized exact-client bundle for the Cyclopedia player-observer windows. Physical XYZ/world correlation, negative controls, PID identity and restart/relogin remain RUNTIME-owned and unavailable until the canonical identity path is proven.

### P2 structural chain remains partial Draft evidence

P2 Draft #310 head `9b99b6b4bda2cf01e8fadcd8a00a6827de35d825` is exact-head green and still supports only:

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

No Draft P2 evidence is promoted here. Final transport semantics remain incomplete.

### Viewport/worldmap static RE advanced materially but remains incomplete

Draft #367 head `a69179e5cf4681a9d41014a562a0bfd0d1cd9ffb` now consumes #437 and proves exact identities for `TWorldmapProtocolMessageHandler`, `TWorldMapStorage` and its counted control block; direct Storage constructor/writer/reader coverage proves the 18x14 values live inside exact Storage extent state, not Viewport.

It remains `MORE_STATIC_RE_NEEDED`: upstream slot-12 source, RenderProvider clipping/culling, Camera projection/scale, Picker transforms, fixed allocation/loop/mask/packing sites and a safe patch-site graph are still missing. This is programme research incompleteness, not a reason to reopen the old staging blocker.

### Durable coordinator checkpoint is still stale

`docs/agents/tasks/active/OTC-20260816-track-a-promotion-coordination.md` on current main still records `base_main: ddf7dd...`, old #357/#358/#360/#356 barrier state and stale P1/runtime conclusions. Live Git and the current canonical RUNTIME task override it.

This remains a material governance/continuation risk because a worker reading the durable coordinator task without fresh Git reconciliation can select obsolete blockers.

## Current open material findings

### AUD-COV-001 — HIGH — canonical item-level coverage registry absent from current main

Current-main search still finds no canonical `capabilities.jsonl`, `protocol_messages.jsonl` or `runtime_types.jsonl` package.

**Impact:** coverage cannot be deterministically recomputed from canonical current-main state; narrative percentages can drift from the accepted bounded baseline.

**Next discriminator:** coordinator-promote or regenerate provenance-preserving current-main registries plus validator, retaining UNKNOWN/DISPROVEN/SUPERSEDED entries.

### AUD-COV-002 — HIGH — required semantic denominators remain incomplete

E51 full 349-message family/semantic classification, E52 full Tibia-owned QMeta/runtime classification, P0 item-level read/action denominator and P1 global field/evidence denominator remain absent.

**Impact:** identifier/subset inventory can still be confused with programme semantic completion.

**Next discriminator:** execute E51 and E52 against the canonical registry, then materialize normalized P0/P1 item registries without deleting UNKNOWN rows.

### AUD-COV-003 — MEDIUM — action/QMeta denominator conflict `612` vs historical `1004`

The durable capability census still states these came from different inventory/filter definitions and are not directly comparable.

**Impact:** action coverage percentages remain ambiguous.

**Next discriminator:** reconstruct/deprecate the historical 1004 definition with provenance, then version one named denominator.

### AUD-COV-004 — HIGH — current canonical live semantic/restart proof remains unavailable

Promoted isolated evidence has advanced from graphics startup through raw-X11/XRes resource identity, but exact resource-to-official-client PID ownership is still UNKNOWN and no current canonical Gate-B/registered-session semantic proof is promoted.

**Impact:** authoritative current `IN_GAME`, player XYZ causality, live bridge correlation, accepted actions and restart/relogin stability cannot be counted as complete.

**Next discriminator:** implement/validate the hosted raw-XRes QueryVersion/QueryClientIds helper required by the current canonical task; then perform a separately admitted physical resource-to-PID identity discriminator. Only after direct identity proof may canonical/runtime semantic experiments resume.

### AUD-COV-005 — MEDIUM — exact-client evidence production remains task-scoped rather than canonical/reusable

#437 proves a compliant bounded producer pattern and resolves the old claim that no lawful exact-static production route exists. However there is no single canonical reusable full-binary hosted staging mechanism; each new missing window still requires explicit bounded producer ownership/provenance.

**Impact:** P0 and other static consumers can still wait on producer work even though the process is now known and feasible.

**Next discriminator:** standardize the sanitized exact-window producer contract or dispatch the smallest task-scoped producer for each missing consumer window; never fall back to repeated guessed CDN fetches or generic unauthorized Synology static analysis.

### AUD-COV-007 — MEDIUM — durable coordinator checkpoint materially stale

The canonical coordinator task still advertises `ddf7dd...` and pre-#414/pre-#445 barriers.

**Impact:** repository-resolved continuation can choose obsolete work unless every invocation independently reconstructs live Git.

**Next discriminator:** refresh the durable coordinator checkpoint from current main and name current P0 #302, P2 #310, viewport #367/#437, promoted P1 #414, and RUNTIME raw-XRes frontier.

## Resolved / materially reclassified since prior #390 handoff

| Prior state | Current disposition |
|---|---|
| AUD-COV-006 P1 accepted semantics not promoted | `RESOLVED`: coordinator PR #414 merged; #372 closed superseded |
| AUD-COV-005 no reusable/legal exact-static path | `RECLASSIFIED MEDIUM`: #437 proves task-scoped sanitized producer + hosted validation pattern; not yet canonical/global |
| xkbcomp/Xvfb startup as current RUNTIME blocker | `SUPERSEDED`: later DRI/raw-X11/XRes evidence moved frontier to resource-to-PID identity |
| #415 no-GLX isolated result as latest graphics state | `HISTORICAL_ACCEPTED`: later DRI repair/revalidation and post-RHI raw-X11 evidence supersede it as the latest frontier |

Previously resolved findings remain resolved: #360 transition implementation defect, #356 QLibrary source-validator defect, and stale #363 viewport prompt lifecycle.

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
| 8 | P0 direct authoritative XYZ | P0 static + RUNTIME | bounded Cyclopedia observer-window producer, then causal live XYZ/world/negative controls after identity proof |
| 9 | structural current `IN_GAME` + live P1 correlation | RUNTIME + promoted P1 | bounded proof only after identified canonical session exists |
| 10 | restart/relogin stability | RUNTIME + P0/P1 | fresh PID/PIE/session reacquisition and repeated semantic correlation |
| 11 | P2 framing/sequence/compression/encryption/final egress | P2 | continue one exact stage at a time from current sanitized evidence |
| 12 | action/QMeta denominator normalization | COVERAGE-AUDIT/QMeta | reconcile 612 vs 1004 provenance |
| 13 | viewport downstream patch graph | viewport #367 + exact-static producer | Storage upstream + RenderProvider/Camera/Picker/fixed-bound windows before any mutation design |

## Campaign completeness verdict

```yaml
protocol_identifier_inventory_complete: true
protocol_direction_inventory_complete: true
protocol_semantic_coverage_complete: false
full_qmeta_runtime_denominator_complete: false
p0_group_requirement_inventory_complete: true
p0_item_level_read_action_denominator_complete: false
p0_direct_authoritative_xyz_proven: false
p1_semantic_implementation_promoted: true
p1_live_session_correlation_proven: false
p2_structural_chain_partial: true
p2_framing_sequence_compression_encryption_egress_complete: false
exact_static_task_scoped_producer_pattern_proven: true
exact_static_canonical_global_staging_available: false
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
    medium: 3
  p1_promotion_gap_resolved: true
  exact_static_staging_gap_downgraded: true
  inventory_vs_semantic_boundary_preserved: true
  draft_findings_promoted_to_global_truth: false
  isolated_runtime_promoted_to_canonical: false
e2e:
  result: NOT_APPLICABLE_WITH_REASON
  reason: documentation/evidence-only COVERAGE-AUDIT with runtime_access none; physical E2E belongs to separately admitted RUNTIME work
```

## Researcher delivery boundary

This package remains `DRAFT_NOT_PROMOTED`. Coordinator review must independently choose `ACCEPT | ACCEPT_WITH_EDITS | RETURN_FOR_EVIDENCE | REJECT/SUPERSEDE`. The researcher does not merge or change global programme truth.