# OTCLIENT Track A — economy/account panel static census

Date: 2026-08-19  
Task: `OTC-20260819-track-a-economy-panels-static-census`  
Source Draft: PR #546  
Promotion: PR #547  
Track: `official-client-re`  
Execution: repository-only static evidence review (`runtime_access: none`)

## Result

The bounded G24-G31 static census is accepted with coordinator edits after fresh falsification of the source and promotion claims.

Exact S1 binary:

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
generated_messages_total: 349
client_to_server: 160
server_to_client: 189
received_message_strings: 189
protocol_handler_type_xrefs: 47
```

The raw S1 registries independently confirm transport-name surfaces for Market, Store/coin transactions, Daily Reward, Reward Wall/resting, Character Info/Blessings/Premium, Character Trade and generic modal/client-check flows. No dedicated World Transfer/Main Character Change generated-message mapping was identified in the bounded review.

## Provenance correction

The source Draft and initial promotion text claimed that `docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md` used a conflicting digest. Fresh verification disproves that claim.

The capability census at both `a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb` and source head `54dca602dfa38f1cc347716cf0f701b22c3fe6e9` records:

```text
e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

PR #293 records the same historical researched binary. There is no retained SHA conflict in those authoritative sources.

Accordingly, the capability-census economy/account UI/controller observations remain usable as **same-exact-build static report leads**. They are not upgraded to live semantics, normal call-path proof, ABI proof, transaction confirmation, or server-side effects.

## Handler evidence

Fresh re-read of `protocol-handler-code-xrefs.tsv` confirms exact S1 direct code-to-type-string xrefs for Cyclopedia, Daily Reward, Blessings, Premium, server modal dialog, Market, Store and Character Trade protocol-handler types. Every retained row has `semantic_dispatcher_edge_proven=false`; no message-specific dispatcher address is claimed.

## Runtime/safety

This static subtask has `runtime_access: none`, `mutation_authorized: false`, and `physical_e2e_required: false`. Promotion does not depend on a current physical-runtime reachability claim and performs no official-client runtime work.

No login, credential use, GUI input, process control, gameplay or economy/account transaction-producing action is part of this static promotion.

## Validation

Corrected source exact head `54dca602dfa38f1cc347716cf0f701b22c3fe6e9`:

```yaml
source_changed_files: 2
source_scope_only: true
Track_A_governance_run: 32219366592
Track_A_governance_result: success
CI_run: 32219366648
CI_result: success
source_admission_repair_verified: true
```

Shared matrix/checklist Draft PR #536 remains untouched.

## Remaining UNKNOWN

```yaml
generated_message_to_concrete_handler_dispatch: UNKNOWN
outgoing_dispatch_and_wire_encoding: UNKNOWN
handler_to_controller_storage_edges: UNKNOWN
live_GUI_state_and_confirmation_boundaries: UNKNOWN
G30_dedicated_transport_mapping: UNKNOWN
server_side_transaction_effects: NOT_TESTED
```

The **static census subtask** is complete once PR #547 is merged and source Draft PR #546 is closed unmerged as superseded. The full canonical `TIBIA-RE-ECONOMY-PANELS` runtime mission remains separate future work.