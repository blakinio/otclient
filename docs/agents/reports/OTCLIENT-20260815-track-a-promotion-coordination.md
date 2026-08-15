# Track A promotion/integration coordination — 2026-08-15

Coordinator task: `OTC-20260815-track-a-promotion-coordination`  
Coordinator PR: `#300`  
Repository: `blakinio/otclient`  
Canonical base at coordinator claim: `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`

## Scope

This report is the campaign promotion ledger for Track A (`official-client-re`). It records promotion dispositions from direct GitHub/task/check/artifact inspection. Researcher PR prose and workflow success are treated as evidence inputs, not semantic authority. Track B remains outside Track A mutation authority.

## Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

Build-specific promotions below apply only to this fence unless a later current-client identity/profile is independently proven.

## Canonical P2 boundary from merged PR #299

### FACT

`main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45` contains the bounded PR #299 reconciliation and durable reproducers proving for the exact build:

- `TGameserverTCPConnection` QMeta/type ownership;
- two concrete QTcpSocket construction/member-store paths;
- direct RTTI association of receiver vptr `0x3084b38` with `TGameserverTCPConnection`;
- concrete socket member at receiver `+0x10`;
- `TProtocolWriter : TIODeviceWriter` RTTI relationship.

### DISPROVEN / SUPERSEDED

Do not promote again:

- `clientMessageReadyToProcess -> owner +0x88 -> 0xb5b880` as the gameplay endpoint;
- `0xb46bd0` as binary Tibia gameplay-frame sink;
- `0xc33259` as network/gameplay binary sink.

### UNKNOWN

P2 remains open for:

1. concrete ownership/reference path from `TGameserverDualConnection` into the actual writer object;
2. gameplay serialization/framing order;
3. compression/encryption/sequence transformation boundary;
4. final binary socket/QIODevice egress;
5. causal controlled local/custom-harness proof.

Queued run `31825417040` (`Track A final socket write resolution`) is still observed `queued` with no update since 2026-08-14. Do not launch a conceptual duplicate merely to bypass it. A distinct next P2 hypothesis should instead trace `TGameserverDualConnection -> TProtocolWriter/TIODeviceWriter` construction/dispatch ownership.

## PR disposition ledger

### PR #289 — `ci/OTC-20260813-official-client-re-continuation`

**Disposition: REJECT/SUPERSEDE as a whole-branch integration candidate.**

Verified reasons:

- head `c04ff82918f954af019ab533bf6af0792dc730bf` is a stale, broad branch with 461 commits and 208 changed files relative to its old base;
- its active task still promotes the now-disproven `0xb5b880` outbound convergence model;
- exact-head CI run `31839506387` failed (`Fast Checks / Syntax and workflow validation` failed at `actionlint`, therefore `CI / Required` failed);
- three material P1 review threads remain unresolved:
  - credentials exported to persistent child processes;
  - unconditional deletion of temporary X11 display sockets without ownership proof;
  - canonical package update path lacks restore-on-failure rollback;
- merged PR #299 already demonstrated the required policy pattern: extract/rebuild bounded evidence slices from current main rather than merge #289 history wholesale.

Closing/superseding #289 must not erase unique evidence. Individual bounded claims remain eligible for independent promotion below.

#### Accepted bounded evidence from #289 — structural reversible world transition

**ACCEPT as runtime/world-state evidence, not as A3/A4 action parity.**

Direct coordinator cross-check of run `31806312967`, job `94785974126` established:

- runner is `synology-otclient-01`;
- workflow hard-checks exact client SHA-256 `e6c244...ff7fe` before the probe;
- task-owned official-client and persistent observer processes are alive and ownership-marked;
- stimulus sent `Up`, then inverse `Down`;
- structural map-strip counts changed `0 -> 33 -> 88`;
- log contains decoded ordered records with concrete `(x,y,z,stack)` values;
- forward floor-7 strip includes `x=32537..32554, y=32502, z=7` and inverse floor-7 strip includes the same 18-column range at `y=32516, z=7`;
- client/observer survived through the inverse step;
- the associated artifact `9221332209` contains three XWD snapshots with digest `sha256:bd4be5b2f9d6cebf19fff6bdfa3677ad57c00ae4a376987f32b42e8a27907a4a`.

Promotion boundary:

```yaml
world_transition: FACT
one_tile_north_then_south_restoration: FACT_from_structural_strip_geometry
player_xyz_32546_32510_7: DERIVED_from_fixed_viewport_geometry
standalone_player_position_member: UNKNOWN
action_input_path: xdotool_keyboard
A3_server_confirmed_bridge_action: NOT_PROVEN
A4_bridge_reference_parity: NOT_PROVEN
restart_relogin_stability_for_this_read: NOT_PROVEN
```

#### Historical #289 outgoing-payload consumer artifact

Run `31815819731` completed successfully and artifact `9225203231` exists with digest `sha256:e0ca5a09b4ad7ea57a78833ceefa737a8330db837aedfc4218efb53d9b126f86`. The coordinator downloaded and inspected it. It is **not promotable P2 evidence on the current model** because the experiment root is explicitly `SUBOBJECT_SLOT_B8=0xb5b880`, now superseded by PR #299. Preserve it as negative/historical evidence only.

### PR #283 — read-only runtime bridge

**Disposition: ACCEPT for the bounded read-only bridge implementation; P1 remains incomplete.**

Verified:

- changed paths are limited to `tools/tibia_runtime_bridge/**`, its tests, and its task record;
- exact implementation head `89e13819e6f53026b831b7e8e4c8fab228d1626c` is the code that passed the recorded exact-client E2E;
- direct `compare_commits(89e13819..., d93ccb34...)` proves the current PR head is two commits ahead and the only changed file after the validated implementation is the task Markdown;
- current exact PR head `d93ccb34f66af7d3198a50a46e706b4f902ae637` has successful CI run `31680615776`;
- there are no open review threads on PR #283;
- coordinator code inspection confirms exact-SHA launcher fencing, `LD_PRELOAD` bridge, dynamic PIE-base discovery, owner-mode `0600` Unix socket, read-only `PING`/`DISCOVER`, Qt-thread marshalling and relocation-aware primary-vptr recovery.

Promotion boundary:

```yaml
bridge_v1_read_only_implementation: ACCEPT
exact_build_profile_rediscovery: FACT_from_recorded_exact_e2e
logged_out_zero_marker_fail_closed: FACT_from_recorded_exact_e2e
live_session_status_authority: UNKNOWN
authoritative_player_position_via_bridge: UNKNOWN
write_action_api: OUT_OF_SCOPE_NOT_IMPLEMENTED
P1_complete: false
```

The branch is old and should not be merged wholesale if current-main rebuild is required. Integration must remain a bounded auditable slice.

### PR #279 — worldmap reconstruction pipeline

**Disposition: ACCEPT_WITH_EDITS.**

Verified:

- neutral fail-closed pipeline scope is separated from future real official-client capture;
- two independent high-severity audit findings were repaired rather than ignored;
- focused repaired suite reached 23/23, Python syntax validation passed, and synthetic `reconstruct -> compare -> plan-otbm` E2E passed on the repair evidence;
- current exact PR head `04356aa9c042ce19d9d8431b91f18567e410a5e5` has successful repository CI run `31681889560`;
- all PR review threads are resolved;
- task record is stale because it still says final exact-head CI is pending even though the coordinator verified that result.

Required edit before terminal integration: repair task lifecycle/checkpoint to record final exact-head CI and current integration/archive state. Acceptance is for tooling only; real appearance mappings, real official-client capture coverage and complete OTBM remain unproven.

### PR #295 — Track A map-observation ownership correction

**Disposition: RETURN_FOR_EVIDENCE/EDITS.**

The high-level correction (current producer should be official-client Track A, not open-source OTClient Track B) is directionally correct, but the PR cannot be accepted in its present state.

Verified blockers:

- four unresolved material review threads remain;
- P1 ownership collision: current main still has active task `OTC-20260813-map-observation-export` owning `docs/agents/contracts/MAP_OBSERVATION_V1.md`;
- the current main task is itself stale relative to merged PR #291, but it explicitly identifies itself as Track B and therefore is outside this Track A coordinator's mutation authority;
- revised contract weakens the previous separate-authorization wording for external Atlas consumption;
- revised contract weakens the unconditional raw-packet prohibition to only secret-bearing raw packets;
- revised contract drops the explicit `producer.protocol_version` non-negative-integer rule.

Required before promotion:

1. Track B authority must terminally reconcile/release the stale `OTC-20260813-map-observation-export` ownership;
2. restore blanket raw packet prohibition;
3. restore explicit non-negative integer `protocol_version` rule;
4. retain explicit separate authorization for external consumer transfer;
5. resolve all review threads and rerun exact-head CI.

### PR #292 — map observation recorder

**Not a Track A PR; no Track A disposition or mutation authority.**

Its task explicitly declares `track: otclient-global-login` / Track B and its implementation instruments open-source OTClient `ProtocolGame`/`Map`/`Tile`. It is only an overlap/dependency signal for #295 and must not be closed, promoted or rewritten by this coordinator.

### PR #296 — archived design lifecycle correction

**Disposition: ACCEPT_WITH_EDITS / integrate current-main equivalent, then supersede draft.**

Direct comparison shows current main still records `archive_closeout_state: pending_archive_pr_merge` even though PR #294 is already merged. #296 correctly changes that to `merged_and_terminal`, records the final independent-audit/remediation state, exact-head required CI and ownership release. Exact head `7f3775cdf9d805b86db63f0068302777fa3d2367` has successful CI run `31784425205`.

No research or runtime claim changes. A coordinator current-main integration copy is preferable to promoting the stale draft merely to trigger another review lifecycle.

### PR #290 — Track A live-session/login handover

**Disposition: pending final bounded review; unique historical procedure evidence exists.**

The draft contains a precise historical login/session recovery procedure, explicitly limits OCR to character-selection bootstrap rather than world semantics, preserves WARP/SOCKS confinement and records several rejected assumptions. Its runtime claims are version-fenced or marked revalidation-required/owner-observed. Before promotion, reconcile it against later #289 structural runtime evidence and current canonical task ownership so duplicated/stale runtime instructions do not become authoritative.

### PR #277 — older official-client runtime handover

**Disposition: pending supersession check.**

Single task-document draft predates the canonical 2026-08-13 state import and #290. It should be closed as superseded only after verifying that no unique non-secret claim is absent from the later canonical report/handover.

### PR #280 / #281 — dedicated-runner migration and self-hosted probe

**Disposition: pending current-state revalidation; historical 'no runner available' blocker is superseded as a current fact.**

Their checkpoints recorded queued self-hosted runs on 2026-08-12/13. Later verified run `31806312967` executed successfully on `synology-otclient-01`, so the old 'no available self-hosted runner' conclusion cannot remain current. Infrastructure design may still contain reusable files; reconcile exact current-main runner state before accepting/closing these drafts.

## Quantitative coverage checkpoint

The #289 exact-build coverage baseline is retained as a bounded census checkpoint, not a final coverage gate:

```yaml
protocol_identifier_inventory:
  numerator: 349
  denominator: 349
  percent: 100.0
  meaning: unique named inbound/outbound message identifier inventory only
protocol_handler_qmeta_records:
  numerator: 47
  denominator: 47
  percent: 100.0
  meaning: inventoried relocation-backed ProtocolMessageHandler QMeta records
legacy_qobject_connect_edges:
  numerator: 40
  denominator: 41
  percent: 97.5609756098
high_information_gameaction_sender_metaobjects:
  numerator: 29
  denominator: 31
  percent: 93.5483870968
direct_qt_connection_semantic_classification:
  numerator: UNKNOWN
  denominator: 2184
generated_message_semantic_classification:
  numerator: UNKNOWN
  denominator: 349
p0_live_read_coverage:
  numerator: UNKNOWN
  denominator: UNKNOWN
```

The repository-defined final requirement for item-level `capabilities.jsonl`, `protocol_messages.jsonl`, `runtime_types.jsonl` plus terminal P0 experiment/read/action coverage is not satisfied by these inventory percentages.

## Lane readiness after reconciliation

### P2-NETWORK

READY only for a **distinct** hypothesis rooted in the merged #299 model: recover concrete writer ownership/virtual dispatch from `TGameserverDualConnection` into `TProtocolWriter/TIODeviceWriter`. Do not rerun the queued final-socket-write experiment or the superseded `0xb5b880` consumer search.

### P0-STATE

READY after #289 broad ownership is terminally released. Preferred first hypothesis: recover a direct standalone authoritative player-position member (likely beginning from version-fenced `TPlayerData`/session/storage leads), with no movement/action side effect. This is distinct from the already-proven DERIVED viewport-center position.

### P1-BRIDGE

Occupied by accepted-but-unintegrated PR #283. Do not dispatch a duplicate bridge implementation. Next research hypothesis after integration is live `session-status` correlation + authoritative read endpoint, with bundled official-client Qt runtime and restart/relogin reacquisition.

### RUNTIME

READY after #289 broad ownership is terminally released. Distinct goal: restart/relogin/reacquisition stability of the already-proven structural world observer/read path; do not repeat basic login bootstrap or movement-strip experiment unchanged.

### COVERAGE-AUDIT

READY after #289 broad evidence ownership is terminally released. It should materialize canonical item-level protocol/QMeta/P0 registries and exact denominators from existing durable evidence, then enumerate concrete missing experiments instead of claiming global percentages from selected subsets.

## Current non-completion statement

Track A is **not COMPLETE/100%**. P2 framing/final egress, authoritative direct P0 reads, live bridge authority/reacquisition, A3/A4 semantic action parity, item-level quantitative coverage and final closeout gates remain open.
