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
- corrected processing graph `TProtocolClientMessageProcessor -> TGameserverNetworkPacketRawDataProcessor -> TGameserverDualConnection`;
- outer retained fields `+0xa00/+0xa08` -> `TProtocolClientMessageProcessor`, `+0xa10/+0xa18` -> raw-data processor, `+0xc18/+0xc20` -> `TGameserverDualConnection`.

Accepted PR #301 adds one bounded retention fact for the same exact build:

```text
TProtocolClientMessageProcessor
 -> retained intermediate object (exact class UNKNOWN)
 -> retained shared TProtocolWriter
```

The same setup FDE constructs/retains `TGameserverDualConnection` separately at outer `+0xc18/+0xc20`.

### INFERENCE

Combining the accepted retention fact with the independently accepted processing graph supports:

```text
writer_location_relative_to_dualconnection = UPSTREAM_ON_TPROTOCOLCLIENTMESSAGEPROCESSOR_BRANCH
```

This is graph-relative inference, not proof of a direct `TGameserverDualConnection -> TProtocolWriter` member.

### DISPROVEN / SUPERSEDED

Do not revive without direct contradictory proof:

- `clientMessageReadyToProcess -> owner+0x88 -> 0xb5b880` as gameplay endpoint;
- `0xb46bd0` as binary gameplay-frame sink;
- `0xc33259` as network/gameplay binary sink;
- stale `TProtocolWriter` RTTI `0x3080700`.

### NOT_PROVEN / UNKNOWN

- direct `TGameserverDualConnection -> TProtocolWriter` member/reference: NOT_PROVEN;
- exact class identity of intermediate vptr `0x2f69e30`: UNKNOWN;
- gameplay serialization/framing order: UNKNOWN;
- compression/encryption/sequence transformation boundary: UNKNOWN;
- final binary socket/QIODevice egress: UNKNOWN;
- causal controlled/local harness proof: UNKNOWN;
- relationship of historical `0x3084c70 -> +0xd0 -> 0xb40630` writer-family lead to canonical `TProtocolWriter`: UNKNOWN.

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

Only the corrected historical native-Linux procedure is retained as `REVALIDATION_REQUIRED` at `docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/accepted-historical-login-procedure.md`. Coordinator evidence `20260815-login-update-revalidation.md` further corrects the stale assumption that a newer child binary is currently required: exact fenced client reconstruction and later live-world evidence used the same SHA. Current login/restart stability still requires fresh runtime proof.

**PR #304 — item-level quantitative coverage baseline.**

Reviewed exact Draft head `43a60bd96cc644b656b200c9edbfb75578b330b6`; exact-head CI `31882010038` completed `SUCCESS`. Exact accepted source blobs are copied under coordinator evidence at `coverage-audit/source-snapshot/`, with a separate promotion boundary. Inventory completeness is not semantic completion.

Accepted quantitative baseline:

```yaml
protocol_identifier_inventory: 349/349          # inventory only
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

**PR #301 — P2 writer retention provenance.**

Reviewed exact final Draft head: `50e2d95c7dc8b0759eb6233a3751f73434958e88`.

Validation:

- source semantic run `31883231486` / job `95008610322` = SUCCESS;
- final source provenance run `31883456870` = SUCCESS;
- final required PR CI `31883459362` = SUCCESS;
- changed paths confined to declared research roots;
- unresolved review threads: `0`;
- reviewed historical source artifact `9229609330` is verified by ZIP SHA-256 `bc5604ffbcf7e75a6b00dad227aefaa0036ea4792efb61ce85de488b6877782c` before the discriminator runs.

Promoted boundary:

```yaml
TProtocolClientMessageProcessor_retains_writer_branch: FACT
writer_intermediate_class: UNKNOWN
writer_relative_to_DualConnection: INFERENCE_UPSTREAM_ON_CLIENT_PROCESSOR_BRANCH
direct_DualConnection_writer_member: NOT_PROVEN
framing_order: UNKNOWN
transform_boundary: UNKNOWN
final_binary_egress: UNKNOWN
causal_local_harness: UNKNOWN
P2_complete: false
```

Exact reviewed evidence/result/reproducer/workflow blobs are copied unchanged under:

`docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/p2-writer-ownership/source-snapshot/`

with the coordinator boundary at:

`docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/p2-writer-ownership/PROMOTION_BOUNDARY.md`.

### RETURN_FOR_EVIDENCE

**PR #295 — map-observation ownership correction.**

Still not promotable: material unresolved review findings and Track B ownership collision remain.

### LIVE REVALIDATION REQUIRED

**PR #302 — direct player position.**

The previous statement that run `31880617510` remained queued is stale: that run is now cancelled and #302 advanced to at least `ab22e9c495daea050f45e90b3e38b78062539d59`. Coordinator must refetch the current exact task/head/runs before assigning a new disposition. No newer P0 semantic result is promoted by this report yet.

**PR #303 — restart/relogin reacquisition.**

Earlier live semantic execution had not run. #303 includes fail-closed observer-cleanup hardening (`4bd5cbc47fbfd816a6ab5dd66b57c88b3ff981f4`) and durable evidence, but that is safety evidence only. Because the P0 serialized-lane state changed, current #303 runtime state must be re-fetched before retaining the old blocker classification.

### REJECT / SUPERSEDE

- **PR #289** — broad stale continuation branch; superseded P2 model and unresolved safety findings. Bounded positive/negative evidence was retained before closure.
- **PR #296** — stale lifecycle draft after its valid archive correction was integrated as a bounded current-main coordinator slice.
- **PR #277** — stale Oteryn-dependent Track A continuation handover; unique negative runtime history retained.
- **PR #280 as an active Track A dependency only** — broader infrastructure PR remains separately owned/open; Track A does not wait on it.

## Current lane state

```yaml
P2_NETWORK:
  source_pr: 301
  disposition: ACCEPT_WITH_EDITS
  retention_fact: accepted
  completion: partial
  remaining: framing_transform_order_final_binary_egress_causal_harness
P0_STATE:
  pr: 302
  disposition: REVALIDATION_REQUIRED
  old_queued_blocker: stale
P1_BRIDGE:
  source_pr: 283 closed unmerged after ACCEPT
  integration: present on PR 300
  completion: partial
RUNTIME:
  pr: 303
  disposition: REVALIDATION_REQUIRED
  cleanup_safety_repair: evidence_only
COVERAGE_AUDIT:
  source_pr: 304 closed unmerged after ACCEPT_WITH_EDITS
  coordinator_snapshot: present
```

## Completion state

Track A is **not COMPLETE/100%**.

Material open programme gates are:

1. P2 transformation/framing order, final binary egress and causal harness;
2. authoritative P0 direct player/state reads with semantic discrimination;
3. live bridge authority/session epoch and restart/relogin read reacquisition;
4. A3/A4 action parity with authoritative before/after state;
5. full message/QMeta semantic classification beyond bounded inventories;
6. finite item-level P0/P1 read-field denominator where currently `UNKNOWN/UNKNOWN`;
7. final exact-head integration validation, PR hygiene and programme closeout.

The coordinator must preserve these UNKNOWNs rather than converting inventory completeness or partial ownership provenance into a false completion claim.
