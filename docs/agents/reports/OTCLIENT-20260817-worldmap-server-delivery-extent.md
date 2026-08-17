# OTClient official-client RE — server-delivered worldmap extent

```yaml
report_date: 2026-08-17
repository: blakinio/otclient
task: OTC-20260817-track-a-worldmap-server-delivery-extent
pr: 473
base_main: f99ec371bafd0b9dbccb8fd6f4c8a3137e7d963b
prompt_contract: docs/agents/prompts/OTCLIENT_TIBIA_RE_WORLDMAP_MUTATION_DESIGN.md@1.1.0
execution_class: github_hosted
runtime_access: none
physical_runtime_used_by_this_task: false
client_bytes_modified_by_this_task: false
owner_funded_ai_api_used: false
```

## Result

The exact client proves that normal gameplay map payload families are received **server -> client** through dedicated `FullMap`, `FieldData`, directional row/column, floor-change and object-map mutation messages. The complete 160-name client -> server generated-message census contains no separately named aware-range/extent/viewport/full-map/width/height request.

That is not enough to prove who controls the delivered dimensions. Exact field recovery for generic outbound messages was not available through the validated raw-descriptor surface, and no accepted evidence proves that changing the client-local `18/14` pair changes the authoritative coordinate envelope arriving from the server. The server-delivery model and all larger/full-floor/multi-floor/whole-map maximum claims therefore remain `UNKNOWN` rather than being promoted from directionality or naming inference.

```text
SERVER_MAP_DELIVERY_MODEL=UNKNOWN
SERVER_LARGER_RECTANGLE_SUPPORTED=UNKNOWN
SERVER_FULL_FLOOR_DELIVERY_SUPPORTED=UNKNOWN
SERVER_MULTI_FLOOR_BULK_DELIVERY_SUPPORTED=UNKNOWN
SERVER_WHOLE_MAP_DELIVERY_SUPPORTED=UNKNOWN
MAX_SERVER_DELIVERABLE_EXTENT=UNKNOWN
```

This is a bounded research result, not a claim that larger or whole-map server delivery is impossible.

## Exact client fence

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

The accepted client-local geometry chain remains:

```text
hardcoded packed 18/14 @ 0x01cdd958
 -> TWorldmapProtocolMessageHandler constructor
 -> Handler+0xb0/+0xb4
 -> 0x00bc6350 snapshot+0x38
 -> Handler+0x10 TWorldMapStorage vslot12
 -> 0x00cc6cd0
 -> Storage+0x48/+0x4c
```

The accepted mutation-design work already proved the one-byte `[19,14]` startup canary mechanics. This task neither repeated nor extended client-byte mutation.

## Three distinct extent planes

### 1. Client Storage capacity

**FACT:** accepted static work proves extent-driven Storage bounds/eviction and no recovered fixed Storage/cache maximum.

**UNKNOWN:** a global safe Storage maximum.

### 2. Client render/interaction extent

**FACT:** Viewport has the accepted `18/14` default plus recomputation; RenderProvider and Picker retain fixed-32 clipping/index/transform dependencies that are separate from Storage.

**UNKNOWN:** a globally safe larger rendered/pickable extent without the coupled mutation/validation work already defined by the mutation-design package.

### 3. Server-delivered gameplay extent

**FACT:** this task proves inbound map-message directionality and bounded current-shape evidence below.

**UNKNOWN:** whether the server accepts, negotiates, derives or ignores a larger requested/client-local extent and what its maximum deliverable rectangle/floor set is.

No conclusion from plane 1 or 2 is promoted into plane 3.

## Exact generated-message census

Hosted run `32022209943`, job `95364071999`, exact producer head `553e447c0662892b0c1b9cab994c4545d09f22c8`, produced the complete generated-message inventory:

```text
TOTAL=349
CLIENT_TO_SERVER=160
SERVER_TO_CLIENT=189
```

Direct server -> client map families include:

```text
GameserverMessageFullMap
GameserverMessageFieldData
GameserverMessageLeftColumn
GameserverMessageRightColumn
GameserverMessageTopRow
GameserverMessageBottomRow
GameserverMessageTopFloor
GameserverMessageBottomFloor
GameserverMessageCreateOnMap
GameserverMessageChangeOnMap
GameserverMessageDeleteOnMap
GameserverMessageWorldEntered
```

The complete client -> server message-name set contains no generated name matching:

```text
aware
range
extent
viewport
fullmap
fielddata
width
height
```

This proves only that there is no **separately named generated outbound message** for those concepts. It does not prove that `GameclientMessageLogin`, `GameclientMessageSecondaryLogin`, `GameclientMessageClientDetails`, `GameclientMessageEnterWorld` or `GameclientMessageSetClientOptions` contain no relevant field.

Durable evidence:

`docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-extent/20260817-complete-message-census.md`

## Handler / map-description linkage

Accepted prior exact disassembly remains directly relevant:

- research-labelled `FullMap` handler: static `0x00cec8d0` in recovered range `0x00cec790..0x00cecaa0`;
- map-description path: `0x019a8a80`, recovered range `0x019a89c0..0x019a9000`;
- the FullMap path consumes three adjacent event integers, multiplies two by exactly `32`, persists a paired tuple in owner state, and passes the floor-like comparison into map-description processing;
- map-description processing uses descriptor-side `+0x38/+0x3c/+0x40` as multiplicative/divisor grid parameters plus coordinate bases and a floor-dependent transform before worldmap Storage consumption.

**FACT:** the exact client has a real protocol-event -> map-description geometry -> worldmap Storage path.

**UNKNOWN:** the exact source field names/units, arbitrary width/height semantics and any maximum accepted value.

Canonical predecessor:

`docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260816-exact-handler-disassembly-recovery.md`

## Exact descriptor boundary

The bounded protocol-descriptor producer used three non-identical hypotheses and stopped after the task repair budget rather than broadening indefinitely.

Successful final probe:

```yaml
run: 32022973229
job: 95366330613
head: ae5778d1f8b0e79b77bfa68c14692a3d599b25c5
result: success
artifact: 9286040543
artifact_sha256: a7bba32855e73c6b2a29c5dfae4da04e0498bcae985b37de91ef79658dac6281
```

It validated the raw descriptor parser against an exact serialized `shared.proto` descriptor:

```text
Coordinate.x = optional uint32 field 1
Coordinate.y = optional uint32 field 2
Coordinate.z = optional uint32 field 3
```

It did not recover raw top-level descriptors for `Extent`, the target generic client messages, or the `FullMap`/row/column/floor server messages. The only bounded printable `tibia.protobuf.protocol` neighborhood is a concatenated generated-type/name table, not the same inline raw FileDescriptorProto layout as `shared.proto`.

Therefore:

```text
PROTOCOL_COORDINATE_TYPES=x/y/z uint32 PROVEN
PROTOCOL_EXTENT_FIELD_SCHEMA=UNKNOWN
OUTBOUND_GENERIC_NEGOTIATION_FIELDS=UNKNOWN
```

Durable evidence:

`docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-extent/20260817-targeted-descriptor-boundary.md`

## Retained normal strip observation

No new runtime was used. Re-inspection of retained GitHub artifact `9227370490` (`track-a-persistent-provenance-dump`, run `31821458677`) gives 90 stored strip observations: 72 on `z=7`, 18 on `z=6`. Two dense captured `z=7` rows each span exactly 18 unique X coordinates (`32537..32554`).

This is consistent with the independent client-local baseline width `18`. Adjacent-floor observations also occur, but the retained TSV is not an atomic packet/message trace; it cannot prove that several floors arrived in one bulk server message.

Durable evidence:

`docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-extent/20260817-retained-strip-observation.md`

## Direct acceptance matrix

| Question | Result | Basis |
|---|---|---|
| Is `18x14` proven client-local geometry? | **YES** | accepted constructor -> handler -> Storage chain |
| Is a named outbound aware-range/extent request present? | **NO in complete message-name census** | all 160 client -> server generated names inspected |
| Are normal map payload families server -> client? | **YES** | exact `GameserverMessage*` census and registrations |
| Is any generic outbound extent/range field ruled out? | **NO** | exact target protocol descriptors not recovered |
| Does changing client `18/14` alone make server send more? | **UNKNOWN** | no accepted causal IN_GAME trace |
| Larger authoritative rectangle supported? | **UNKNOWN** | no direct larger inbound envelope proof |
| Complete Z-level/floor supported? | **UNKNOWN** | `TopFloor`/`BottomFloor` names are not whole-floor proof |
| Multi-floor bulk beyond normal visibility supported? | **UNKNOWN** | adjacent-floor observations lack atomic message boundary |
| Whole map/world dataset supported through gameplay connection? | **UNKNOWN** | no direct evidence; local cache/minimap capability excluded |
| Maximum server-deliverable extent? | **UNKNOWN** | no exact bound recovered |

## Why the model is not promoted to SERVER_DRIVEN or FIXED_PROTOCOL

The server -> client direction of map payloads is proven. That does not identify the **extent-control model**.

`SERVER_DRIVEN` would require evidence that the server independently decides delivered dimensions rather than acting on a client-negotiated field. `FIXED_PROTOCOL` would require evidence that the relevant dimensions/strip counts are fixed by the wire contract rather than merely the current client/server implementation. The complete message-name census narrows the possibilities but does not rule out a field inside a generic outbound message.

The correct direct-evidence classification is therefore `UNKNOWN`.

## Bounded negative evidence

The following were searched and not promoted into global impossibility claims:

- complete 160-name client -> server generated-message inventory;
- exact `FullMap`/row/column/floor server message family inventory;
- exact-client protocol `Extent`/row/column/schema leads;
- validated raw descriptor surface and targeted descriptor anchors;
- accepted FullMap/map-description disassembly;
- retained normal worldmap strip observations;
- accepted prior parser/network ceiling search.

No evidence proves a larger/full-floor/whole-map server capability, but none proves a global prohibition either.

## Separately authorized causal runtime discriminator

A future physical Track A task can resolve the remaining model question without conflating server delivery with Storage/render growth.

### Authority required

```yaml
execution_class: physical_runtime
runtime_access: canonical_single_session
client_byte_mutation: separately_authorized_task_owned_copy_only
login_or_relogin: admission_required
owner_funded_ai_api: not_required
```

The current task does **not** have that authority.

### Baseline capture

On the exact unmodified client:

1. establish one admitted canonical IN_GAME session;
2. instrument inbound dispatch/handler entry for `FullMap`, `FieldData`, Left/RightColumn, Top/BottomRow and Top/BottomFloor before Storage mutation;
3. instrument the outbound generated-message enqueue/serialization boundary for generic login/client-details/options/enter-world messages sufficiently to identify whether any map-range/extent value is transmitted;
4. record decoded map-event coordinates/extents, floor set, element/tile counts and message/packet sizes;
5. execute one bounded, reproducible movement sequence that produces horizontal, vertical and floor-related map updates where safely available;
6. record the resulting authoritative inbound coordinate envelope separately from Storage and rendered/pickable envelopes.

### Mutated comparison

Using only the already-designed, separately authorized task-owned `[19,14]` copy and a fresh identity/restart as required by the mutation contract:

1. repeat the same capture surfaces and bounded movement sequence;
2. compare outbound generic-message fields byte-for-byte/semantically against baseline;
3. compare inbound server map coordinate envelope, strip widths/heights, floors and payload sizes against baseline;
4. compare Storage occupancy separately;
5. compare render/picker separately.

### Falsifiable outcomes

```text
A. outbound extent/range field/request changes with [19,14]
   -> direct evidence for NEGOTIATED or CLIENT_DRIVEN, depending on causality/request semantics.

B. outbound extent/range surface does not change, but authoritative inbound map envelope grows
   -> evidence that additional server data actually arrives; inspect the exact causal input before assigning SERVER_DRIVEN.

C. outbound extent/range surface and authoritative inbound envelope stay baseline while Storage/render envelope grows
   -> client can store/render a larger local area without receiving additional authoritative tiles; fixed/independent server delivery becomes the supported interpretation for that tested path.

D. login/session is rejected, payload parsing truncates, or handler bounds fail
   -> stop; preserve the smallest failure and do not infer a larger supported extent.
```

### Negative control

A Storage/render-only increase with **no increase in the pre-Storage authoritative inbound coordinate envelope** is explicitly a failure of the hypothesis “larger client extent causes additional server map data to arrive.”

### Rollback / stop

- restore the exact original client hash after the single mutation comparison;
- do not broaden beyond `[19,14]` in the first causal run;
- stop on crash, parser anomaly, identity mismatch, unexpected account/world side effect or admission failure;
- do not use a second uncontrolled session to manufacture comparison data.

## Completion of this research slice

The server-delivery research slice is complete at the static-evidence level because every required flag has a direct, non-invented value, including `UNKNOWN` where the exact client cannot decide the question through the authorized surface. The remaining causal distinction is isolated into one separately authorized physical runtime experiment rather than being silently executed here.

This report does **not** change the earlier mutation-design result and does **not** claim that a larger-map feature is runtime-validated.
