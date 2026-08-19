# OTCLIENT Track A — economy/account panel static census

Date: 2026-08-19  
Task: `OTC-20260819-track-a-economy-panels-static-census`  
Source Draft: PR #546  
Promotion: PR #547  
Track: `official-client-re`  
Execution: repository-only static evidence review (`runtime_access: none`)

## Result

The bounded G24-G31 static census is accepted after fresh coordinator review and correction.

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

The exact S1 registries prove transport-name surfaces for Market, Store/coin transactions, Daily Reward, Reward Wall/resting, Character Info/Blessings/Premium, Character Trade and generic modal/client-check flows. No dedicated World Transfer/Main Character Change generated-message mapping was identified in the bounded review.

## Provenance correction

The historical capability census records corresponding UI/controller leads but its header SHA (`e6cfa9ff…`) conflicts with the historical binary SHA (`e6c244bd…`) recorded by PR #293 and its archived task. The promotion therefore treats those UI/controller observations as **version-fenced leads with unresolved digest provenance**, not exact-S1-hash proof.

This correction removes the unsupported same-exact-binary claim present in the initial source Draft.

## Handler evidence

Exact S1 direct code-to-type-string xrefs are retained for Cyclopedia, Daily Reward, Blessings, Premium, server modal dialog, Market, Store and Character Trade protocol-handler types. Every retained row has `semantic_dispatcher_edge_proven=false`; no message-specific dispatcher address is claimed.

## Runtime/safety

Fresh Remote Desktop Commander revalidation reports `synology-otclient-01` offline/unreachable. The task has `runtime_access: none` and `physical_e2e_required: false`, so physical runtime is not a completion gate.

No login, credential use, GUI input, process control, gameplay or economy/account transaction-producing action was performed.

## Validation

Corrected source exact head `54dca602dfa38f1cc347716cf0f701b22c3fe6e9`:

```yaml
source_changed_files: 2
source_scope_only: true
Track_A_governance_run: 32219366592
Track_A_governance_result: success
CI_run: 32219366648
CI_result: success
open_material_findings_after_correction: 0
```

Shared matrix/checklist Draft PR #536 remains untouched.

## Remaining UNKNOWN

```yaml
capability_census_digest_provenance: UNKNOWN
capability_UI_exact_S1_hash_identity: UNKNOWN
generated_message_to_concrete_handler_dispatch: UNKNOWN
outgoing_dispatch_and_wire_encoding: UNKNOWN
handler_to_controller_storage_edges: UNKNOWN
live_GUI_state_and_confirmation_boundaries: UNKNOWN
G30_dedicated_transport_mapping: UNKNOWN
server_side_transaction_effects: NOT_TESTED
```

`TIBIA-RE-ECONOMY-PANELS` is complete for its bounded static scope once PR #547 is merged and source Draft PR #546 is closed unmerged as superseded.
