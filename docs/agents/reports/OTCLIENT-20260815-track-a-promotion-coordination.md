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

## Canonical P2 boundary

### FACT

Merged PR #299 establishes:

- `TGameserverTCPConnection` QMeta/type/RTTI ownership and its concrete `QTcpSocket*` member at receiver `+0x10`;
- canonical `TProtocolWriter : TIODeviceWriter` RTTI relation;
- processing graph `TProtocolClientMessageProcessor -> TGameserverNetworkPacketRawDataProcessor -> TGameserverDualConnection`;
- outer retained fields `+0xa00/+0xa08` -> `TProtocolClientMessageProcessor`, `+0xa10/+0xa18` -> raw-data processor, `+0xc18/+0xc20` -> `TGameserverDualConnection`.

Accepted PR #301 proves the bounded writer-retention relation:

```text
TProtocolClientMessageProcessor
 -> retained intermediate object
 -> retained shared TProtocolWriter
```

The writer branch is installed at outer `+0xa00/+0xa08`; `TGameserverDualConnection` is separately retained at outer `+0xc18/+0xc20`.

Accepted PR #305 sharpens the intermediate object:

```text
vptr = 0x2f69e30
offset-to-top = 0
Itanium typeinfo = 0x3080748
first virtual targets = 0x7de7f0, 0x7dfd60
semantic type name = UNKNOWN
separately allocated retained object = FACT
```

Typeinfo `0x3080748` differs from canonical `TProtocolWriter` RTTI `0x3080728` and `TIODeviceWriter` RTTI `0x3080718`.

### INFERENCE

Combining #301 with the independently accepted processing graph supports:

```text
writer_location_relative_to_dualconnection = UPSTREAM_ON_TPROTOCOLCLIENTMESSAGEPROCESSOR_BRANCH
```

#305 additionally bounds `0x7de7f0/0x7dfd60` as teardown-like from exact vptr-install/cleanup behavior. Neither inference is a direct-member, symbol-name or transform-stage claim.

### DISPROVEN / SUPERSEDED

- `clientMessageReadyToProcess -> owner+0x88 -> 0xb5b880` as gameplay endpoint;
- `0xb46bd0` as binary gameplay-frame sink;
- `0xc33259` as network/gameplay binary sink;
- stale `TProtocolWriter` RTTI `0x3080700`;
- treating `0x2f69e30` as merely a secondary/base address point of canonical `TProtocolWriter` based on adjacency. Distinct typeinfo plus separate object allocation/provenance reject that collapse.

### NOT_PROVEN / UNKNOWN

- direct `TGameserverDualConnection -> TProtocolWriter` member/reference: NOT_PROVEN;
- semantic name and inheritance/base relation for RTTI `0x3080748`: UNKNOWN;
- gameplay serialization/framing order: UNKNOWN;
- compression/encryption/sequence transformation boundary: UNKNOWN;
- final binary socket/QIODevice egress: UNKNOWN;
- causal controlled/local harness proof: UNKNOWN;
- relationship of historical `0x3084c70 -> +0xd0 -> 0xb40630` family to canonical writer branch: UNKNOWN. Its reviewed evidence remains structurally separate (`rtti=0`, no direct LEA provenance).

## Promotion dispositions

### ACCEPT

**PR #283 — bounded read-only runtime bridge implementation.**

Exact accepted tool/test blobs were rebuilt under `tools/tibia_runtime_bridge/**` and `tests/tools/tibia_runtime_bridge/**` after source PR closure. Exact-build profile rediscovery and logged-out fail-closed behavior are accepted. Live `session-status` authority, authoritative player position, restart/relogin stability and write/action API remain unproven.

**Bounded runtime/world-state evidence retained from rejected PR #289.**

Run `31806312967`, job `94785974126` remains accepted for one exact-build reversible structural world transition and restoration under normal client input. It is not A3/A4 bridge action parity and does not make viewport-derived XYZ a standalone authoritative player read.

### ACCEPT_WITH_EDITS

**PR #279 — fail-closed worldmap reconstruction tooling.**

Exact accepted tool/test slice rebuilt on current main. Real official-client capture coverage, complete appearance-role mapping, complete client-ID -> OTB mapping, spawn definitions and complete binary OTBM remain UNKNOWN.

**PR #290 — historical login/recovery procedure.**

Retained as `REVALIDATION_REQUIRED`. Coordinator evidence corrects stale updater assumptions but current login/restart stability still requires fresh runtime proof.

**PR #304 — bounded quantitative coverage baseline.**

Reviewed exact head `43a60bd96cc644b656b200c9edbfb75578b330b6`; CI `31882010038` SUCCESS. Exact accepted source snapshot is coordinator-owned under `coverage-audit/source-snapshot/`; source Draft closed unmerged. Inventory completeness is not semantic completion.

Accepted baseline:

```yaml
protocol_identifier_inventory: 349/349
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
p2_chain_closure_historical_registry: UNKNOWN/5
restart_relogin_stability: UNKNOWN/1
```

**PR #301 — P2 writer retention provenance.**

Reviewed final head `50e2d95c7dc8b0759eb6233a3751f73434958e88`. Semantic run `31883231486` / job `95008610322`, final provenance run `31883456870`, and required PR CI `31883459362` are SUCCESS; review threads `0`. Reviewed source artifact `9229609330` is ZIP-SHA fenced before the discriminator. Exact accepted evidence/result/reproducer/workflow blobs are under coordinator-owned `p2-writer-ownership/source-snapshot/` with a separate promotion boundary. Source Draft #301 was closed unmerged after coordinator CI `31883767739` SUCCESS.

Promoted #301 boundary:

```yaml
TProtocolClientMessageProcessor_retains_writer_branch: FACT
writer_relative_to_DualConnection: INFERENCE_UPSTREAM_ON_CLIENT_PROCESSOR_BRANCH
direct_DualConnection_writer_member: NOT_PROVEN
P2_complete: false
```

**PR #305 — distinct intermediate vtable/type structure.**

Reviewed exact final head `9329e338235b7f9997d74d4db5313f329662378b`.

Validation:

- semantic run `31884166982` / job `95010894063` = SUCCESS;
- durable-checkpoint task run `31884286098` = SUCCESS;
- durable-checkpoint PR CI `31884288165` = SUCCESS;
- final task-specific run `31884379539` / job `95011421555` = SUCCESS;
- final standard PR CI `31884381191`, including `CI / Required`, = SUCCESS;
- changed paths confined to task roots; review threads `0`;
- source artifacts `9231716774`, `9229609330`, `9229251044` are each ZIP-SHA fenced before parsing.

Promoted #305 boundary:

```yaml
intermediate_vptr_0x2f69e30: FACT
intermediate_typeinfo_0x3080748: FACT
separate_allocated_object_receives_vptr: FACT
simple_secondary_TProtocolWriter_interpretation: DISPROVEN
0x7de7f0_0x7dfd60_role: INFERENCE_TEARDOWN_LIKE
rtti_0x3080748_semantic_name: UNKNOWN
rtti_0x3080748_base_relation: UNKNOWN
first_writer_transform_boundary: UNKNOWN
framing_order: UNKNOWN
final_binary_egress: UNKNOWN
P2_complete: false
```

Exact reviewed source blobs are copied unchanged under coordinator-owned:

`docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/p2-writer-vtable-group/source-snapshot/`

with the coordinator boundary at:

`docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/p2-writer-vtable-group/PROMOTION_BOUNDARY.md`.

### RETURN_FOR_EVIDENCE

**PR #295 — map-observation ownership correction.**

Still not promotable: material unresolved review findings and Track B ownership collision remain.

### LIVE RUNTIME / P0 STATE

**PR #302 — direct player position.**

Old run `31880617510` is cancelled. Corrected self-hosted run `31883521701` / job `95009093099` executed on `synology-otclient-01` but found `TRACK_A_P0_MATCHING_LIVE_PIDS=0`. Direct authoritative player XYZ remains UNKNOWN, not disproven. P0 requires a live exact-client Track A process window.

**PR #303 — restart/relogin reacquisition.**

The runner selector issue was repaired far enough for run `31884181155` / job `95010941902` to execute on `synology-otclient-01`. It failed in bootstrap at:

```text
TRACK_A_RUNTIME_ERROR=upstream_wireproxy_unavailable
```

The failure is before client/login semantic execution. Cleanup completed with no task X11 residue. Therefore current runtime blocker is missing/unverifiable shared upstream Track A wireproxy state at the expected runtime path, not generic runner availability. #303 remains independently owned by an active researcher; no coordinator mutation is allowed while active.

### REJECT / SUPERSEDE

- #289 broad stale continuation branch; superseded P2 model and safety findings retained as bounded evidence;
- #296 stale lifecycle Draft after valid correction integration;
- #277 stale Oteryn-dependent continuation handover with unique negative history retained;
- #280 superseded only as an active Track A dependency; broader infrastructure remains separately owned/open.

## Current lane state

```yaml
P2_NETWORK:
  accepted:
    - PR301_writer_retention
    - PR305_distinct_intermediate_type_structure
  completion: partial
  remaining:
    - semantic_name_or_role_of_RTTI_0x3080748_if_needed
    - actual_serialization_framing_transform_order
    - final_binary_egress
    - causal_local_custom_harness
P0_STATE:
  pr: 302
  result: NO_MATCHING_LIVE_EXACT_CLIENT_PROCESS
  direct_player_position: UNKNOWN
P1_BRIDGE:
  source_pr: 283
  read_only_integration: accepted
  live_authority_session_epoch: UNKNOWN
RUNTIME:
  pr: 303
  active_researcher: true
  current_blocker: upstream_wireproxy_unavailable_before_client_start
  restart_relogin_stability: UNKNOWN
COVERAGE_AUDIT:
  source_pr: 304
  accepted_snapshot: present
```

## Completion state

Track A is **not COMPLETE/100%**.

Material open programme gates remain:

1. P2 actual transformation/framing order, final binary egress and causal harness;
2. authoritative P0 direct player/state reads with semantic discrimination;
3. live bridge authority/session epoch and restart/relogin read reacquisition;
4. A3/A4 action parity with authoritative before/after state;
5. semantic protocol/QMeta coverage beyond bounded inventories;
6. finite item-level P0/P1 read-field denominators where currently `UNKNOWN/UNKNOWN`;
7. final exact-head integration validation, PR hygiene and programme closeout.

UNKNOWNs must not be converted into completion percentages or inferred capabilities.
