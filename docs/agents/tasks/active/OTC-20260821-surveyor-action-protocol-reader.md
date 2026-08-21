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
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
gui_input_authorized: false
process_control_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
base_main: 079d6b814a13b1984a0c0ed36def66919238d8f4
branch: feat/OTC-20260821-surveyor-action-protocol-reader
selected_gap: action_protocol_typed_reader
selection_reason: current physical collect-all after auth-session closeout reports 9 gaps; world_minimap rank 1 overlaps active PRs 475/593, so action_protocol rank 2 is the highest-value non-overlapping gap
physical_e2e_required: true
physical_e2e_result: NOT_RUN
---

# Surveyor v2 — action protocol typed reader

## Objective

Implement the next fail-closed Surveyor typed reader for `TIBIA-RE-ACTION-PROTOCOL` on the exact current official Linux client while preserving Track A read-only boundaries.

## Current authority

This implementation phase is repository-only (`runtime_access: none`). No new runtime observation is authorized by this task record yet. A separate explicit read-only admission checkpoint is required before physical acceptance, with target identity and uniqueness freshly revalidated by the physical workflow before process memory is opened.

## Safety boundary

No login/logout/relogin, credentials, GUI/gameplay input, process control, attach/debug/injection, process-memory writes, client/container restart, target-network mutation, item/economy action or local-model use is authorized. Runtime observation may occur only after a current Track A read-only admission checkpoint and must fail closed on identity/fence ambiguity.

## Semantic boundary

The reader may expose only exact typed runtime structure proven by exact-current-build RTTI/vtable evidence and live read-only object identity. It must not claim packet serialization, protocol opcode semantics, action execution, or `IN_GAME` state from structural presence alone. `semantic_promotion_allowed=false` is mandatory.

## Baseline

The latest completed physical Surveyor artifact from run `32478932597` reports 169 canonical rows, 12 aliases, 9 missing typed readers and privacy PASS. This is selection evidence only, not current runtime admission. `action_protocol_typed_reader` is rank 2 with canonical priority 65 and 16 affected unresolved rows. `world_minimap_typed_reader` is rank 1 but overlaps active #475/#593 and is therefore deferred under the selection rule.

## Existing structural evidence

Merged static S9 evidence (`OTC-20260818-track-a-s9-action-control-static-census`) proves the action-control catalogue and the concrete type `tibia::game::TPlayerProtocolMessageHandler` for its exact historical build, while leaving action-layer-to-protocol connection and per-action serialized messages UNKNOWN. The new implementation resolves current-build RTTI/vptr dynamically and must preserve that semantic boundary.
