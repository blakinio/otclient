---
task_id: OTC-20260821-surveyor-action-protocol-reader
status: implementing
phase: implement
agent: ChatGPT
project_lane: otclient
lane: P0-ACTION
track_id: official-client-re
task_kind: implementation
risk: medium
policy_version: 2
runtime_access: read_only
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: canonical-live-runtime
mutation_authorized: false
gui_input_authorized: false
process_control_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
base_main: 079d6b814a13b1984a0c0ed36def66919238d8f4
selected_gap: action_protocol_typed_reader
selection_reason: current physical collect-all after auth-session closeout reports 9 gaps; world_minimap rank 1 overlaps active PRs 475/593, so action_protocol rank 2 is the highest-value non-overlapping gap
physical_e2e_required: true
physical_e2e_result: NOT_RUN
---

# Surveyor v2 — action protocol typed reader

## Objective

Implement the next fail-closed Surveyor typed reader for `TIBIA-RE-ACTION-PROTOCOL` on the exact current official Linux client while preserving Track A read-only boundaries.

## Safety boundary

No login/logout/relogin, credentials, GUI/gameplay input, process control, attach/debug/injection, process-memory writes, client/container restart, target-network mutation, item/economy action or local-model use is authorized. Runtime observation may occur only through current Track A read-only admission and must fail closed on identity/fence ambiguity.

## Semantic boundary

The reader may expose only exact typed runtime structure proven by exact-current-build RTTI/vtable evidence and live read-only object identity. It must not claim packet serialization, protocol opcode semantics, action execution, or `IN_GAME` state from structural presence alone. `semantic_promotion_allowed=false` is mandatory.

## Baseline

Fresh physical Surveyor artifact from run `32478932597` reports 169 canonical rows, 12 aliases, 9 missing typed readers and privacy PASS. `action_protocol_typed_reader` is rank 2 with canonical priority 65 and 16 affected unresolved rows. `world_minimap_typed_reader` is rank 1 but overlaps active #475/#593 and is therefore deferred under the selection rule.

## Existing structural evidence

Merged static S9 evidence (`OTC-20260818-track-a-s9-action-control-static-census`) proves the exact action-control catalogue and the concrete type `tibia::game::TPlayerProtocolMessageHandler`, while leaving action-layer-to-protocol connection and per-action serialized messages UNKNOWN. The new reader must preserve that boundary.
