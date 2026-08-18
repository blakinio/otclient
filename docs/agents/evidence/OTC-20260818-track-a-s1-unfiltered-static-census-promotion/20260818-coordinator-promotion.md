# Track A S1 unfiltered static census — coordinator promotion

Date: 2026-08-18  
Source task: `OTC-20260818-track-a-s1-unfiltered-static-census`  
Source Draft: PR #509  
Source final head: `b381a2a614c503f3d021af98432df99a069305c7`  
Trusted integration base: `main@ed09418b431c28087775b419f85bed404fa85d70`  
Decision: **ACCEPT_WITH_EDITS**

## Independent review boundary

The coordinator reviewed the full final source diff, exact changed-path inventory, fresh producer artifact, independent #473 denominator control, current-main exact-build resolver output and the final source CI/governance graph.

The source diff is documentation/evidence only. It contains no workflow after finalization and no runtime/product mutation. It does not touch PR #475-owned paths or state.

## Promoted FACTS

Exact client:

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Generated protocol denominator:

```text
349 total
160 GameclientMessage*
189 GameserverMessage*
```

The fresh run's three registries are byte-identical to the independent #473 sanitized control.

Complete receive-method string surface:

```text
189 received*Message strings
188 exact generated-message/received-method stem matches
1 naming variant:
  GameserverMessageTrackQuestFlags
  receivedTrackedQuestFlagsMessage
```

Broad static selector breakdown:

```text
149 handle*
189 received*
204 on*
542 total broad candidate strings
```

Protocol-handler type/code surface:

```text
47 distinct *ProtocolMessageHandler class-name strings
with direct executable code-to-class-string xrefs
```

Current exact-build resolver:

```text
TGameClient                     0x3076908
TGameserverGameSession          0x3078ba0
TPlayerProtocolMessageHandler   0x308a008
TPlayerData                     0x308ca70
TContainerStorage               0x308a1a0
TCreatureStorage                0x308d078
TWorldmapProtocolMessageHandler 0x30871d8
```

All seven resolve uniquely on the exact client.

## Promoted inference / retained UNKNOWNs

The 188 exact stems plus one naming variant are strong static lexical evidence for a generated-message / `received*Message` naming correspondence, but the coordinator does **not** promote a concrete dispatch edge from names alone.

```yaml
GENERATED_MESSAGE_TO_RECEIVED_METHOD_NAME_ALIGNMENT: INFERENCE_STATIC_LEXICAL_ONLY
GENERATED_MESSAGE_TO_CONCRETE_HANDLER_DISPATCH: UNKNOWN
RECEIVED_METHOD_TO_HANDLER_OWNER: UNKNOWN
HANDLER_TO_STORAGE_CONTROLLER_EDGE: UNKNOWN
COMMON_UPSTREAM_INBOUND_DISPATCHER: UNKNOWN
RUNTIME_DELIVERY_OR_STATE_MUTATION: UNKNOWN
```

Many domain-specific handler types prove a broad partitioned handler **type surface**. They do not prove or disprove a shared upstream queue/router.

## Falsification / accepted edits

The coordinator accepts the research result only after the following source corrections:

1. **Family bucket rejection.** Temporary substring buckets were found semantically unsafe (`Mark` inside `Market`, `row` inside `Browse`) and excluded from promoted evidence.
2. **542-method overclassification repair.** The broad selector output is not called an inbound-handler denominator. It is explicitly `149 handle* + 189 received* + 204 on*`; the durable receive-method string denominator is 189.
3. **Shared dispatcher non-claim.** Domain-specific handler types are not used to infer that no common upstream dispatcher exists.

No material finding remains open after those edits.

## Producer / control evidence

Fresh producer:

```text
run      32112814216
job      95635760592
result   SUCCESS
artifact 9315562574
digest   sha256:583c8c217fa2eaa2411f79995473cd910b8803d8599f80574491ca27b8ab9860
```

Independent control:

```text
#473 run      32022209943
artifact      9285763750
digest        sha256:0f71be3021885f3f8881199c5f74839fca6c6c5081594fab48998298abaadbd6
```

Registry hashes:

```text
all 349              55f7cf2d6d4a63df6e24b8b156e38f1a2a64a9d6394357aa914661ab48fd983b
client -> server     621ecb7aa1a62aae559e8d793d1aebe9289d84811bc43c4339a7153458b553f0
server -> client     e642f661546c2e6e89ddcd77ac5e8aa9cd517408a309f95a3a367af943550d96
```

## Source exact-head validation

```text
source head b381a2a614c503f3d021af98432df99a069305c7
Track A governance 32114161352 = SUCCESS
  Fresh admission behavior audit 95639845377 = SUCCESS
  Deterministic admission audit   95639845470 = SUCCESS
CI 32114161531 = SUCCESS
  CI / Required                   95639907436 = SUCCESS
reviews                            0
unresolved review threads          0
main freshness                     PASS
```

## Safety / nonclaims

```yaml
runtime_access: none
client_executed: false
synology_used: false
x11_or_vnc_used: false
process_memory_used: false
credentials_used: false
login_performed: false
gameplay_performed: false
raw_client_committed_or_uploaded: false
pr475_runtime_observed: false
pr475_runtime_mutated: false
physical_e2e: NOT_APPLICABLE_STATIC_EXACT_FILE_DISCOVERY_ONLY
```

## Next frontier

This promotion does not create or consume a physical runtime task. The next independent static S2 frontier is player inbound dispatch:

```text
TPlayerProtocolMessageHandler
  -> PlayerDataCurrent / PlayerState / PlayerInventory / PlayerSkills
  -> exact QMeta/dispatch targets
  -> static TPlayerData ownership/mutation edge where provable
```

Creature, container and chat handler graphs remain subsequent static candidates. Worldmap semantics and native-login runtime remain outside this promotion while PR #475 owns those surfaces.
