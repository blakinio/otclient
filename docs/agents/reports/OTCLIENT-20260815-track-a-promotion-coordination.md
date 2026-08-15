# Track A promotion/integration coordination — 2026-08-15

Coordinator task: `OTC-20260815-track-a-promotion-coordination`  
Coordinator PR: `#300`  
Repository: `blakinio/otclient`  
Canonical base for this campaign slice: `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`

## Scope and trust boundary

This is the campaign promotion ledger for Track A (`official-client-re`), official native Linux Tibia client only. Research worker prose, PR comments and workflow colour are evidence inputs, not semantic authority. Track B remains outside Track A mutation authority.

## Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

Build-specific claims below apply only to this fence unless a later exact identity is independently proven.

## Canonical P2 boundary

### FACT

Merged PR #299 establishes for the exact build:

- `TGameserverTCPConnection` QMeta/type/RTTI ownership;
- concrete `QTcpSocket*` member construction at receiver `+0x10`;
- `TProtocolWriter : TIODeviceWriter` RTTI relationship;
- corrected outbound chain reaches `TGameserverDualConnection`.

### DISPROVEN / SUPERSEDED

Do not revive without direct contradictory proof:

- `clientMessageReadyToProcess -> owner+0x88 -> 0xb5b880` as gameplay endpoint;
- `0xb46bd0` as binary gameplay-frame sink;
- `0xc33259` as network/gameplay binary sink;
- stale `TProtocolWriter` RTTI `0x3080700`.

### UNKNOWN

- concrete `TGameserverDualConnection -> actual writer` ownership/reference/dispatch edge;
- gameplay serialization/framing order;
- compression/encryption/sequence transformation boundary;
- final binary socket/QIODevice egress;
- causal controlled/local harness proof.

## Promotion dispositions

### ACCEPT

**PR #283 — bounded read-only runtime bridge implementation.**

Source PR was closed unmerged at `d93ccb34f66af7d3198a50a46e706b4f902ae637`. Coordinator independently verified the exact implementation/runtime evidence, source exact-head CI and zero unresolved review threads, then rebuilt the exact accepted tool/test blobs under `tools/tibia_runtime_bridge/**` and `tests/tools/tibia_runtime_bridge/**` on #300.

Promotion boundary:

```yaml
read_only_bridge_implementation: ACCEPT
exact_build_profile_rediscovery: FACT
logged_out_zero_marker_fail_closed: FACT
session_status_live_authority: DERIVED/UNKNOWN until structural live correlation
authoritative_player_position: UNKNOWN
restart_relogin_stability: UNKNOWN
write_action_api: NOT_IMPLEMENTED
P1_complete: false
```

**Bounded runtime/world-state evidence from rejected PR #289.**

Run `31806312967`, job `94785974126` remains accepted for the exact-build reversible structural world transition. It proves a structural transition and restoration under normal client input, not A3/A4 bridge action parity. Standalone absolute player position remains unproven; viewport-derived XYZ remains DERIVED.

### ACCEPT_WITH_EDITS

**PR #279 — fail-closed worldmap reconstruction tooling.**

Source PR was closed unmerged at `04356aa9c042ce19d9d8431b91f18567e410a5e5`. The accepted fail-closed tool/test slice was rebuilt on current-main #300. Real official-client capture coverage, complete appearance-role mapping, complete client-ID -> OTB mapping, spawn definitions and complete binary OTBM remain UNKNOWN.

**PR #290 — historical login/session recovery procedure.**

Only the corrected historical native-Linux procedure is retained as `REVALIDATION_REQUIRED` at `docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/accepted-historical-login-procedure.md`. OCR is limited to historical character-selection bootstrap; it is not world-semantic evidence. Current login/restart stability requires fresh runtime proof.

**PR #304 — item-level quantitative coverage baseline.**

Reviewed exact Draft head: `43a60bd96cc644b656b200c9edbfb75578b330b6`. Exact-head CI run `31882010038` completed `SUCCESS`, changed paths are task-owned, and there are no unresolved inline review threads.

Coordinator independently checked the load-bearing exact-build source evidence:

- protocol-surface run `31787489302` / job `94726575137` on `synology-otclient-01` rechecked the exact client SHA and emitted the full `189` inbound + `160` outbound identifier inventory plus the independent `47` handler literal census;
- QMeta census run `31790619327` / job `94736463933` recovered all `47` protocol-handler QMeta records under the relocation-backed structural gate;
- Qt callsite census run `31799755489` / job `94764705414` counted `2078` direct `connectImpl`, `41` legacy connect and `65` disconnectImpl callsites = `2184`, while explicitly leaving semantic ownership UNKNOWN.

The reviewed registry validator enforces record-ID uniqueness, allowed classifications, registered provenance references, message-list decode/hash/count/uniqueness, selected-set denominators, percentage arithmetic and retained `DISPROVEN/SUPERSEDED` evidence. Its boundary is internal registry integrity; it does not cryptographically regenerate every compressed record from every historical source log.

The exact accepted source blobs are copied unchanged under:

`docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/coverage-audit/source-snapshot/`

with the coordinator promotion boundary at:

`docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/coverage-audit/PROMOTION_BOUNDARY.md`

Accepted quantitative baseline:

```yaml
protocol_identifier_inventory: 349/349          # 189 inbound + 160 outbound; inventory only
protocol_direct_qmeta_links: 27/349
generated_message_semantic_support: UNKNOWN/349
protocol_handler_qmeta_records: 47/47
direct_qt_connection_raw_census: 2184/2184
direct_qt_connection_semantic_classification: UNKNOWN/2184
legacy_qobject_connect_edges: 40/41
high_information_gameaction_sender_metaobjects: 29/31
p0_top_level_requirement_registry: 16/16
p0_live_read_coverage: UNKNOWN/UNKNOWN
bridge_v1_profile_target_inventory: 7/7
p1_overall_field_evidence_coverage: UNKNOWN/UNKNOWN
p2_chain_closure: UNKNOWN/5
restart_relogin_stability: UNKNOWN/1
```

None of the 100% inventory rows is programme-semantic completion.

### RETURN_FOR_EVIDENCE

**PR #295 — map-observation ownership correction.**

Still not promotable: material unresolved review findings and Track B ownership collision remain.

**PR #301 — P2 writer ownership.**

Current reviewed head `29ca506501efc716330a80ab2b96eaf9bbe3d4d5` contains only the approved dispatch/task contract. No evidence report, reproducer or executed hypothesis exists yet. Required next evidence is the exact-client `TGameserverDualConnection -> TProtocolWriter/TIODeviceWriter` ownership/dispatch discriminator without reviving superseded sink models.

**PR #302 — direct player position.**

Current reviewed head `e45b126923495b209c08a77e9a3db96b44ad71a4` contains a bounded read-only typed `TPlayerData` probe, but material runtime run `31880617510` / job `95002559098` remains queued on the serialized self-hosted lane. No direct-position semantic result exists.

**PR #303 — restart/relogin reacquisition.**

Runtime semantic execution remains blocked behind #302. During the current campaign rotation, #303 was additionally hardened fail-closed so a surviving task-owned GDB observer prevents task-root deletion. Code-bearing safety-repair head: `4bd5cbc47fbfd816a6ab5dd66b57c88b3ff981f4`; task checkpoint head after durable evidence update: `2b6350abeb4de37180247c585b90bd1e4c0a9d0f`. This is cleanup safety evidence only, not restart/relogin semantic proof.

### REJECT / SUPERSEDE

- **PR #289** — broad stale continuation branch; superseded P2 model and unresolved safety findings. Bounded positive/negative evidence was retained before closure.
- **PR #296** — stale lifecycle draft after its valid archive correction was integrated as a bounded current-main coordinator slice.
- **PR #277** — stale Oteryn-dependent Track A continuation handover; unique negative runtime history retained.
- **PR #280 as an active Track A dependency only** — broader infrastructure PR remains separately owned/open; Track A does not wait on it.

## Current lane state

```yaml
P2_NETWORK:
  pr: 301
  disposition: RETURN_FOR_EVIDENCE / DISPATCH_READY
  semantic_result: none
P0_STATE:
  pr: 302
  disposition: RETURN_FOR_EVIDENCE
  blocker: run 31880617510 / job 95002559098 queued
P1_BRIDGE:
  source_pr: 283 closed unmerged after ACCEPT
  integration: present on PR 300
  completion: partial
RUNTIME:
  pr: 303
  disposition: RETURN_FOR_EVIDENCE
  blocker: serialized behind P0; no self-hosted reacquire semantic job executed
  cleanup_safety_repair: integrated only on Draft #303, not a semantic capability
COVERAGE_AUDIT:
  source_pr: 304
  disposition: ACCEPT_WITH_EDITS
  exact_source_head: 43a60bd96cc644b656b200c9edbfb75578b330b6
  source_ci: 31882010038 SUCCESS
  coordinator_snapshot: present
```

## Completion state

Track A is **not COMPLETE/100%**.

Material open programme gates are:

1. P2 writer ownership, transform/framing order, final egress and causal harness;
2. authoritative P0 direct player/state reads with semantic discrimination;
3. live bridge authority/session epoch and restart/relogin read reacquisition;
4. A3/A4 action parity with authoritative before/after state;
5. full message/QMeta semantic classification beyond the now-canonical bounded inventories;
6. finite item-level P0/P1 read-field denominator where currently `UNKNOWN/UNKNOWN`;
7. final exact-head integration validation, PR hygiene and programme closeout.

The coordinator must preserve these UNKNOWNs rather than converting inventory completeness into a false completion claim.
