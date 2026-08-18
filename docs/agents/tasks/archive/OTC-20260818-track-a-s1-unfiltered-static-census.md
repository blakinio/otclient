---
task_id: OTC-20260818-track-a-s1-unfiltered-static-census
status: completed
agent: ChatGPT
session_role: researcher_then_coordinator_review
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: archived
execution_mode: github_only
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
runtime_access: none
mutation_authorized: false
source_pr: 509
source_branch: research/OTC-20260818-track-a-s1-unfiltered-static-census
source_final_head: b381a2a614c503f3d021af98432df99a069305c7
base_main: ed09418b431c28087775b419f85bed404fa85d70
completed: 2026-08-18T10:08:00+02:00
risk: medium
owned_paths_released: true
---

# Terminal result

```yaml
RESEARCH_RESULT: COMPLETE
PROMOTION_DECISION: ACCEPT_WITH_EDITS
EXACT_CLIENT: 15.32.df7b29
EXACT_CLIENT_SIZE: 51965216
EXACT_CLIENT_SHA256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
PROTOCOL_MESSAGE_TOTAL: 349
CLIENT_TO_SERVER_MESSAGE_TOTAL: 160
SERVER_TO_CLIENT_MESSAGE_TOTAL: 189
RECEIVED_MESSAGE_STRING_TOTAL: 189
RECEIVED_EXACT_STEM_MATCHES: 188
RECEIVED_NAMING_VARIANTS: 1
PROTOCOL_MESSAGE_HANDLER_CLASS_XREFS: 47
COMMON_UPSTREAM_INBOUND_DISPATCHER: UNKNOWN
RUNTIME_ACCESS: none
PR475_RUNTIME_TOUCHED: false
```

## Accepted evidence

Fresh exact-client producer:

```text
run      32112814216
job      95635760592
result   SUCCESS
artifact 9315562574
digest   sha256:583c8c217fa2eaa2411f79995473cd910b8803d8599f80574491ca27b8ab9860
```

Independent #473 control:

```text
run      32022209943
artifact 9285763750
digest   sha256:0f71be3021885f3f8881199c5f74839fca6c6c5081594fab48998298abaadbd6
```

Fresh and control protocol registries are byte-identical:

```text
all 349                55f7cf2d6d4a63df6e24b8b156e38f1a2a64a9d6394357aa914661ab48fd983b
160 client -> server   621ecb7aa1a62aae559e8d793d1aebe9289d84811bc43c4339a7153458b553f0
189 server -> client   e642f661546c2e6e89ddcd77ac5e8aa9cd517408a309f95a3a367af943550d96
```

## Accepted classification

```yaml
FACT:
  generated_protocol_denominator: 349
  client_to_server_registry: 160
  server_to_client_registry: 189
  broad_candidate_method_strings: 542
  handle_prefixed_strings: 149
  received_message_strings: 189
  on_prefixed_strings: 204
  received_exact_stem_matches: 188
  received_naming_variants: 1
  protocol_handler_classes_with_direct_code_string_xref: 47
  exact_profile_vptr_targets_unique: 7

INFERENCE:
  generated_message_to_received_method_name_alignment: static_lexical_only
  native_protocol_handler_type_surface: domain_partitioned

UNKNOWN:
  generated_message_to_concrete_handler_dispatch
  received_method_to_handler_owner
  handler_to_storage_controller_mutation_edge
  common_upstream_inbound_dispatcher
  runtime_delivery_or_state_mutation
```

## Coordinator edits / falsification

Three overclaims were caught and repaired before promotion:

1. substring-only diagnostic family buckets (`Mark`/`Market`, `row`/`Browse`) were rejected as semantic evidence;
2. the broad 542-method set was split into `149 handle* + 189 received* + 204 on*`; only the exact 189 `received*Message` strings are retained as the inbound receive-method string denominator;
3. many domain-specific handler types were not used to infer absence of a common upstream router; that topology remains `UNKNOWN`.

## Source exact-head validation

Source final head `b381a2a614c503f3d021af98432df99a069305c7`:

```text
Track A agent runtime governance run 32114161352 = SUCCESS
  Fresh admission behavior audit      95639845377 = SUCCESS
  Deterministic admission-policy      95639845470 = SUCCESS
CI run 32114161531 = SUCCESS
  CI / Required                       95639907436 = SUCCESS
reviews = 0
unresolved review threads = 0
main freshness = PASS at ed09418b431c28087775b419f85bed404fa85d70
```

Physical E2E is `NOT_APPLICABLE`: the task performed static exact-file discovery only and did not execute or observe the official client.

## Safety / non-overlap

```yaml
synology_used: false
x11_or_vnc_used: false
process_memory_used: false
credentials_used: false
login_performed: false
gameplay_performed: false
raw_client_committed_or_uploaded: false
pr475_runtime_observed: false
pr475_runtime_mutated: false
```

The temporary producer workflow was removed before promotion.

## Next independent frontier

The highest-value non-runtime continuation while PR #475 owns native login/worldmap runtime is:

```text
TPlayerProtocolMessageHandler
  -> PlayerDataCurrent / PlayerState / PlayerInventory / PlayerSkills
  -> exact static QMeta/dispatch targets
  -> static TPlayerData owner/mutation edge where provable
```

Then creature, container and chat handler graphs may be resolved independently.
