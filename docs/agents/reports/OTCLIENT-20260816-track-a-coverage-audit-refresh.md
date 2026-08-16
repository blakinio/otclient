# OTCLIENT-TIBIA-RE Track A coverage / contradiction / missing-proof audit refresh

## Status

```yaml
task: OTC-20260816-track-a-coverage-audit-refresh
lane: COVERAGE-AUDIT
researcher_delivery: draft_only
snapshot_main: 22089c5ca65228379c409dd33561a096eea00b16
snapshot_time: 2026-08-16T17:18:00+02:00
audit_result: FAIL_MATERIAL_GAPS_OPEN
programme_complete: false
material_findings_open: 7
high_findings_open: 4
medium_findings_open: 3
previous_material_findings: 9
previous_findings_resolved_or_superseded: 2
runtime_access: none
physical_e2e: NOT_APPLICABLE_WITH_REASON
```

This is a fresh-current-main replacement of the closed-unmerged Draft PR #369 package. It preserves the accepted bounded #304 denominator evidence, reconciles all material live Track A changes since the #369 snapshot, and does not promote Draft research into canonical programme truth.

## Scope and authority

This audit is repository/GitHub evidence work only. It did not use Synology, inspect a client process, display, VNC endpoint, network session, login state, process memory or gameplay state. Runtime facts below are consumed from durable RUNTIME evidence only.

Current runtime nonclaims remain:

```yaml
display_98_current_canonical_status: UNKNOWN
rfb_6082_current_backend_mapping: UNKNOWN
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
```

Exact historical installed-client fence used by accepted static evidence:

```yaml
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official native Linux
```

Green CI is execution evidence, not semantic/capability proof. Historical PR #303 runtime surfaces remain closed/superseded and are never current authority.

## Live snapshot

| Lane / concern | Live PR / state at snapshot | Exact head / promoted evidence | Audit classification |
|---|---|---|---|
| COVERAGE-AUDIT | #369 closed unmerged; this replacement package is being rebuilt from current main | old #369 head `17df0fdf5385aa7ab9f337afc012884cde716905` | old package historical only |
| P0 direct XYZ | #302 open Draft | `240bc48c8d0a1f9095c1aede331a08e0638772ae` | direct authoritative XYZ still UNKNOWN |
| P1 bridge | #372 open, non-Draft, current Git reports not mergeable | `fae521fdb3b84acfd2d13baaedc676142aabb10e`; exact-head CI/governance green | semantic implementation accepted, promotion freshness still incomplete |
| P2 consumer/transform | #310 open Draft | `e664b07e231fde68a0b801e11e4e4b9456dfdf3c` | substantial new Draft-only structural chain evidence |
| P2 hosted replay | #368 open Draft | `685fc996b097e49d2e5f75d6a9324ddf9cad3c45` | fixture integrity/internal consistency only; not hosted exact-binary proof |
| RUNTIME canonical E2E | #386 open Draft, blocked | `650a8cf376bd424a8a06b3a234bc7a8f41e23d5b` | registration absent; bootstrap failed before client launch/registration |
| RUNTIME support discriminator | #387 merged to main | merge/main `22089c5ca65228379c409dd33561a096eea00b16` | exact Xvfb failure localized to missing absolute `/usr/bin/xkbcomp` |
| RUNTIME support inventory | #388 open Draft | `0d3ac92a9cfd56854c860139fb83068adec443fd` | bounded read-only xkbcomp inventory in progress at snapshot |
| QLibrary source correlation | #377 merged + #378 archive merged | `0da52e479c0fb9c3c6b1063d1cb516c71bacb31b` / `c66e8b563f748e0595e3b7144c3fac3dc744c60c` | prior validator defect resolved for static/source scope |
| viewport/extent | #363 closed unmerged; #367 is the active Draft | #367 `554b689cf80f9115cfd14366780b0acfa8b31523` | lifecycle-staleness finding resolved; patch graph still incomplete |
| coordinator checkpoint | active task on main still records `ddf7dd...`, #357/#358/#360/#356-era barrier | current main is `22089c...` | stale durable coordinator checkpoint remains a material governance gap |

## Accepted historical quantitative baseline

The only accepted machine-readable item-level coverage package remains closed-unmerged PR #304 head `43a60bd96cc644b656b200c9edbfb75578b330b6`, disposition `ACCEPT_WITH_EDITS_BOUNDED_INVENTORY_ONLY`. Its evidence may be used as a bounded historical denominator source, but because the registry files are not on current `main`, it is not a current canonical queryable coverage registry.

### Baseline denominator table

| Metric | Numerator / denominator | Percentage | Evidence class / boundary |
|---|---:|---:|---|
| generated protocol identifiers inventoried | 349 / 349 | 100% | bounded identifier inventory |
| generated protocol directions assigned | 349 / 349 | 100% | 189 inbound + 160 outbound |
| direct QMeta links in bounded protocol registry | 27 / 349 | 7.736% | not semantic completion |
| generated protocol semantic/family support | UNKNOWN / 349 | UNKNOWN | E51 still required |
| protocol-handler QMeta bounded inventory | 47 / 47 | 100% | bounded subset only |
| raw direct Qt selected inventory | 2184 / 2184 | 100% | semantic classification remains UNKNOWN / 2184 |
| selected legacy QObject connect edges | 40 / 41 | 97.561% | selected subset, not full runtime denominator |
| high-information GameAction sender metaobjects | 29 / 31 | 93.548% | 1 mismatch + 1 unresolved in historical package |
| P0 top-level requirement groups inventoried | 16 / 16 | 100% | group inventory only |
| P0 item-level read/action denominator | UNKNOWN / UNKNOWN | UNKNOWN | missing normalized item registry |
| restart-validated capability count | 0 / normalized-denominator-UNKNOWN | not computable | no global restart denominator |
| bridge-v1 implementation targets inventoried | 7 / 7 | 100% | implementation inventory, not live semantic authority |
| P1 global field/evidence coverage | UNKNOWN / UNKNOWN | UNKNOWN | normalized denominator absent |

Historical #304 stage distribution for the sixteen P0 requirement groups remains:

```yaml
INVENTORIED: 7
STRUCTURALLY_IDENTIFIED: 6
SEMANTICALLY_SUPPORTED: 1
UNKNOWN: 2
```

These are group labels, not proof that every read/action inside those groups is covered.

## Current deltas since the first #369 audit

### 1. Canonical bootstrap implementation defect was repaired and promoted

The previous audit correctly blocked on #360 findings. That specific defect state is obsolete. Replacement PR #371 repaired all four coordinator findings and merged as `d16091ca29ff7c9330115e9ce0fdbfb41646e0dc`; its archive/ownership closeout followed through #375.

Therefore the old claim `canonical bootstrap/rebind implementation is not promotion-safe` is no longer current.

However, this did **not** create a canonical runtime. Subsequent physical attempts remained fail-closed before registration.

### 2. Physical canonical runtime progressed to a precise support blocker, but still does not exist

RUNTIME #386 records:

```yaml
canonical_registration: ABSENT
canonical_lease_generation: 3
bootstrap: REQUIRED_NOT_PROVEN
gate_b: NOT_APPLICABLE
mutation_authorized: false
registration_published: false
client_launch_reached: false
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
```

Physical bootstrap run `31954637565` / job `95183271514` passed contained support-root preflight, acquired lease generation 3 and created its canonical-owned WARP profile, then failed `xvfb_socket_missing` before client launch, VNC registration, authoritative runtime registration or Gate B.

Merged isolated diagnostic #387 / run `31954834760` / job `95183766554` reduced that to exact evidence:

```text
/usr/bin/xkbcomp: not found
XKB: Failed to compile keymap
Keyboard initialization failed
```

The contained Xvfb binary had zero unresolved dynamic libraries and exited rc=1 before its X11 socket existed. Main therefore now has `PROVEN_XVFB_START_FAILURE_XKBCOMP_ABSOLUTE_PATH_MISSING` evidence. #388 is the current bounded support-path inventory; no blind canonical bootstrap retry is justified until the support disposition is terminal.

### 3. P2 gained real structural chain evidence without solving hosted exact-client staging

Direct hosted rematerialization remains blocked. #374 ended `INPUT_BLOCKED`; #310 records multiple materially different hosted attempts and forbids another guessed/direct HTTP retry without new evidence.

The important improvement is that retained sanitized exact-fence artifact `9252025461` is now being consumed lawfully as a pre-sanitized evidence bundle. Draft #310 supports:

```yaml
retained_persistent_qbuffer_boundary: PROVEN_PREDECESSOR
first_downstream_consumer: PROVEN:TProtocolClientMessageProcessor+0x10@0xc2df80
first_downstream_transform: PROVEN:TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
same_message_handoff_to_TGameserverDualConnection: PROVEN
protocol_stage_order: PROVEN_PARTIAL
framing: UNKNOWN
sequence: UNKNOWN
compression: UNKNOWN
encryption: UNKNOWN
final_binary_egress: UNKNOWN
```

For one explicitly defined **coarse structural chain denominator** only:

```text
retained byte container
→ first consumer
→ first transform
→ dual-connection handoff
→ final binary egress
```

Draft evidence currently supports `4/5` milestones. This ratio is **DRAFT_EVIDENCE_ONLY**, is not a semantic protocol-coverage percentage, and is not promoted to canonical main until coordinator acceptance.

#368 separately replays a sanitized fixture on GitHub-hosted infrastructure. It can validate fixture integrity/internal consistency only; its historical source execution must remain quarantined as historical exact-binary evidence and must not be relabelled as current hosted exact-binary execution.

### 4. P0 hosted acquisition was exhausted cleanly; direct XYZ remains unknown

#302 executed three materially distinct GitHub-hosted staging strategies. All failed before receiving exact client bytes and all passed proprietary-input cleanup. The owner-supplied current Linux archive was proven to contain the launcher/updater, not the 51,965,216-byte installed game-client ELF.

Retained static evidence still includes `TPlayerData` vptr `0x308ca70`, `playerPosition` literal `0x1cdde3f` and bounded xrefs around `0x8367c1`, but the load-bearing instruction body/member/accessor graph is absent from retained sanitized artifacts. No member offset is promoted.

Result remains:

```yaml
direct_authoritative_player_xyz: UNKNOWN_INCONCLUSIVE
required_static_discriminator: exact instruction graph around 0x8367c1 / TPlayerData
required_physical_discriminator_after_candidate: RUNTIME-owned repeated causal observations + negative controls + restart/relogin
```

### 5. P1 semantic implementation improved, but promotion is still not terminal

Source PR #357 was closed superseded. Fresh-main replacement #372 replays the accepted semantic implementation and exact shared-index changes. Its current head `fae521fdb3b84acfd2d13baaedc676142aabb10e` has successful CI/governance runs, and `session-status` deliberately remains `DERIVED_UNTIL_LIVE_CORRELATION`.

At this audit snapshot #372 is still open and current Git reports it not mergeable after subsequent main movement. Therefore P1 is materially stronger than in the first audit, but it is not terminal/promoted/current-main fresh.

### 6. QLibrary validator finding is resolved for its static/source-correlation scope

The failed #356 validator is superseded. #377 merged the corrected Qt 6.9.3 source correlation and #378 archived the task.

Accepted boundary:

- client predecessor input ends in extensionless `BattlEye/BEClient`;
- official Qt 6.9.3 generates `BEClient.so` as a potential candidate in both relevant CPU branches;
- potential-name generation is not equivalent to actual `dlopen` attempts;
- actual attempted/successful runtime mapping and final mapped filesystem object remain `UNKNOWN`.

This closes the old audit defect about the incorrect source validator. It does not create live QLibrary mapping proof.

### 7. Viewport continuation lifecycle finding is resolved; research itself remains incomplete

Old prompt PR #363 is closed unmerged. The active work is now #367 `OTC-20260816-track-a-worldmap-extent-static-re`, GitHub-hosted with `runtime_access:none` and no byte mutation.

#367 has recovered exact handler disassembly and useful descriptor/storage leads, but explicitly remains `MORE_STATIC_RE_NEEDED`. Missing fields/constructors/default writers, storage ownership/capacity, fixed allocations/loops/masks, render clipping/culling, camera coupling and picker transforms still prevent a patch-ready dependency graph.

The old stale-prompt governance defect is therefore resolved; viewport programme completeness is not.

## Material audit findings — current open set

### AUD-COV-001 — HIGH — canonical item-level coverage registry is still absent from current main

**FACT.** Current-main search finds no canonical `capabilities.jsonl`, `protocol_messages.jsonl` or `runtime_types.jsonl`. Current `docs/agents/evidence/` contains multiple promoted Track A evidence roots but not the #304 registry package.

**Impact:** quantitative coverage cannot be recomputed deterministically from current-main canonical state; workers can drift back to narrative/selected percentages.

**Smallest next action:** coordinator should promote or regenerate provenance-preserving machine-readable registries plus validator from current main, explicitly retaining #304 historical provenance and all UNKNOWN/DISPROVEN/SUPERSEDED states.

### AUD-COV-002 — HIGH — required semantic denominators remain incomplete

**FACT.** Identifier and selected-subset inventories are strong, but E51 full 349-message semantic/family classification, E52 full Tibia-owned QMeta/runtime classification, P0 item-level read/action denominator and P1 global field/evidence denominator remain absent.

**Impact:** inventory percentages can still be mistaken for campaign semantic completion.

**Smallest next action:** execute E51 and E52 against the canonical registry, then normalize P0/P1 item-level denominators without deleting UNKNOWN entries.

### AUD-COV-003 — MEDIUM — action/QMeta denominator conflict `612` versus historical `1004` remains unresolved

**FACT.** The durable capability census explicitly says the 612 high-level action method run and older 1004 figure came from different inventory/filter definitions until the older provenance is reconstructed.

**Impact:** action coverage percentages remain non-comparable.

**Smallest next action:** reconstruct the old 1004 inventory definition or deprecate it with explicit provenance, then choose one named denominator and version it.

### AUD-COV-004 — HIGH — canonical live semantic/restart proof remains unavailable

**FACT.** The bootstrap implementation itself is repaired, but no canonical registration has been published. #386 failed before client launch/registration; #387 proves missing absolute `/usr/bin/xkbcomp`; #388 is the current bounded support inventory. PID/session remain `NOT_REGISTERED`.

**Impact:** no current structural `IN_GAME`, bridge correlation, direct player semantic causality or restart/relogin stability can be promoted.

**Smallest next action:** finish #388 disposition, promote the minimal support fix if one is justified, then run exactly one fresh-current-main canonical bootstrap attempt under RUNTIME admission. Do not skip directly to login or semantic probes.

### AUD-COV-005 — HIGH — reusable GitHub-hosted exact installed-client staging remains unavailable

**FACT.** P0/P2/worldmap direct hosted retrieval paths are exhausted/blocked for the installed exact game-client ELF. The owner-supplied current Linux tarball is launcher-only. Sanitized exact-fence artifacts can advance selected questions, but they do not provide arbitrary missing instruction windows.

**Impact:** P0 `0x8367c1` and parts of the viewport/P2 graph can stall when the exact required window is absent from retained evidence.

**Smallest next action:** prefer existing sanitized exact-fence bundles when sufficient; otherwise establish one coordinator-approved provenance-preserving staging/export mechanism for narrowly requested sanitized instruction/data windows. Do not re-run equivalent guessed HTTP downloads or use Synology as a generic static fallback.

### AUD-COV-006 — MEDIUM — P1 is semantically accepted but still not terminal/promoted from the current main generation

**FACT.** #372 has green exact-head CI/governance and preserves `DERIVED_UNTIL_LIVE_CORRELATION`, but remains open and is currently reported not mergeable after main advanced.

**Impact:** the canonical programme cannot count the P1 bridge as a terminal current-main producer; live correlation/restart remains separately RUNTIME-owned.

**Smallest next action:** coordinator should restack/replay #372 from current main if required by protection, verify unchanged accepted blobs/shared-index deltas, rerun exact-head required checks, merge, archive/release ownership, and preserve live-correlation nonclaims.

### AUD-COV-007 — MEDIUM — durable coordinator checkpoint on main is materially stale

**FACT.** `docs/agents/tasks/active/OTC-20260816-track-a-promotion-coordination.md` still records `main@ddf7dd...` and the old #357/#358/#360/#356 barrier. Live Git has since closed/superseded those exact states, merged #371/#377/#378 and advanced through runtime support diagnostics to `main@22089c...`.

**Impact:** a continuation worker resolving only the durable coordinator record can select obsolete blockers/PRs even though live Git is authoritative.

**Smallest next action:** coordinator refresh should rewrite the barrier from current live PR/task state, explicitly marking #360/#356/#357/#358/#363 historical/superseded and naming #372/#386/#388/#310/#302/#367 as current relevant work.

## Resolved / superseded audit findings from the first #369 package

| Previous finding | Current disposition |
|---|---|
| failed QLibrary #356 validator / actual source spelling defect | `RESOLVED_FOR_STATIC_SCOPE` through #377 + #378; actual runtime mapping remains UNKNOWN by design |
| stale viewport continuation #363 lifecycle metadata | `RESOLVED_FOR_ROUTING` because #363 is closed and #367 is the current static RE task; patch graph itself remains incomplete |
| #360 bootstrap implementation unsafe | `RESOLVED_IMPLEMENTATION_DEFECT` through #371/#375; physical runtime is still blocked independently by Xvfb/xkbcomp support |

The #360 issue is folded into current AUD-COV-004 rather than counted as an additional open finding: the remaining blocker is physical bootstrap support/runtime existence, not the old transition implementation defect.

## Negative and superseded evidence that must remain explicit

| Evidence / model | Required classification |
|---|---|
| historical `0xb5b880` P2 endpoint model | `DISPROVEN/SUPERSEDED` |
| `0xb46bd0` binary gameplay sink claim | `DISPROVEN/SUPERSEDED` |
| `0xc33259` network-sink claim | `DISPROVEN/SUPERSEDED` |
| stale `TProtocolWriter` RTTI `0x3080700` | `DISPROVEN/SUPERSEDED`; corrected exact evidence used `0x3080728` |
| PR #303 physical runtime surfaces | `CLOSED_SUPERSEDED`, historical evidence only |
| PR #304 branch | `CLOSED_UNMERGED`, accepted bounded denominator evidence only |
| PR #360 | `CLOSED_SUPERSEDED`; do not execute |
| PR #356 | `CLOSED_SUPERSEDED`; validator defect historical only |
| PR #357 | `CLOSED_SUPERSEDED_BY_372` |
| PR #358 | historical read-only runtime reconciliation; current physical task is #386/support chain |
| PR #363 | `CLOSED_SUPERSEDED`; current viewport work #367 |
| raw socket existence / byte deltas alone | insufficient for `IN_GAME` or server-accepted movement |
| green generic CI alone | execution evidence only, never semantic/capability proof |
| #368 hosted fixture replay | internal consistency only; not relabelled current hosted exact-binary execution |

## Missing-proof queue ordered by information gain

| Priority | Missing proof | Owning lane / executor | Smallest falsifiable next step |
|---:|---|---|---|
| 1 | current canonical machine-readable coverage registries | COVERAGE-AUDIT + coordinator, GitHub-hosted | promote/regenerate `capabilities`, `protocol_messages`, `runtime_types`, provenance and validator from current main |
| 2 | full 349-message semantic/family classification | protocol/COVERAGE-AUDIT, GitHub-hosted | E51: each identifier gets family or explicit `UNCLASSIFIED` plus provenance |
| 3 | full Tibia-owned QMeta/runtime denominator | QMeta/COVERAGE-AUDIT, GitHub-hosted | E52: enumerate/classify every relevant type/controller/storage or ignored-with-reason |
| 4 | normalized P0/P1 item denominators | COVERAGE-AUDIT with lane owners | materialize each read/action/field item including UNKNOWN and restart status |
| 5 | current coordinator barrier | coordinator | replace stale `ddf7dd` checkpoint with live #372/#386/#388/#310/#302/#367 state |
| 6 | xkbcomp support disposition | RUNTIME support #388 | fixed-path/package inventory only; choose minimal support repair or explicit external blocker |
| 7 | canonical runtime registration + Gate B | RUNTIME | after promoted support fix, one fresh bootstrap; stop on first new fail-closed discriminator |
| 8 | P1 canonical promotion | coordinator + P1 | fresh-main replay/restack of accepted #372 surface, exact-head CI, merge/archive |
| 9 | direct authoritative player XYZ | P0 static + RUNTIME | recover `0x8367c1` member/accessor graph, then two+ passive live observations + world correlation + camera/viewport negative controls |
| 10 | structural current `IN_GAME` + live bridge correlation | RUNTIME + P1 consumer | after valid registered session, bounded structural proof without historical PID/display reuse |
| 11 | restart/relogin stability | RUNTIME with P0/P1 consumers | fresh PID/PIE/session, rediscover and reproduce same semantic read/bridge correlation |
| 12 | P2 final transform/framing/egress | P2 GitHub-hosted | continue from sanitized exact-fence evidence one stage at a time; keep framing/sequence/compression/encryption/egress UNKNOWN until direct evidence |
| 13 | normalized action/QMeta denominator | COVERAGE-AUDIT/QMeta | reconcile `612` vs `1004`, version one denominator |
| 14 | viewport patch/dependency graph | viewport #367, GitHub-hosted | finish extent/storage/protocol/render/camera/picker ownership and fixed-bound graph before mutation design |

## Campaign completeness verdict

```yaml
protocol_identifier_inventory_complete: true
protocol_direction_inventory_complete: true
protocol_semantic_coverage_complete: false
qmeta_handler_subset_inventory_complete: true
full_qmeta_runtime_denominator_complete: false
p0_group_requirement_inventory_complete: true
p0_item_level_read_action_denominator_complete: false
p1_semantic_implementation_available_in_draft: true
p1_promoted_current_main_terminal: false
p1_live_session_correlation_proven: false
p2_structural_chain_progress_draft_only: true
p2_framing_sequence_compression_encryption_egress_complete: false
canonical_physical_runtime_registered: false
restart_relogin_stability_proven: false
stable_live_bridge_semantics_proven: false
viewport_static_patch_graph_ready: false
programme_complete: false
```

## Audit and E2E classification

```yaml
audit:
  result: FAIL_MATERIAL_GAPS_OPEN
  open_findings:
    high: 4
    medium: 3
  resolved_or_superseded_since_previous_package: 2
  false_completion_claim_found: false
  inventory_vs_semantic_boundary_preserved: true
  historical_runtime_promoted_to_current: false
  negative_evidence_preserved: true
e2e:
  result: NOT_APPLICABLE_WITH_REASON
  reason: documentation/evidence-only COVERAGE-AUDIT with runtime_access none; physical E2E belongs exclusively to admitted RUNTIME work
```

## Researcher delivery boundary

This package is `DRAFT_NOT_PROMOTED`. The researcher may update denominators, contradictions, evidence references and missing-proof ordering, but may not merge or change global programme truth. Coordinator review must choose `ACCEPT | ACCEPT_WITH_EDITS | RETURN_FOR_EVIDENCE | REJECT/SUPERSEDE` before any promotion.
