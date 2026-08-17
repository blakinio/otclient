---
task_id: OTC-20260817-track-a-worldmap-mutation-design
status: investigating
agent: ChatGPT
session_id: chatgpt-worldmap-mutation-design-20260817
session_role: mutation_design_coordinator
project_lane: otclient
lane: STATIC-RE
track_id: official-client-re
task_kind: discovery
phase: design
branch: docs/OTC-20260817-track-a-worldmap-mutation-design
base_branch: main
base_main: 2ad6565f6f598b15acaeb3d182a3ffb70d187ba6
created: 2026-08-17T10:39:00+02:00
updated: 2026-08-17T10:39:00+02:00
risk: high
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_class: github_hosted
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: medium
context_growth: stable
decomposition_decision: single
implementation_authorized: false
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
client_byte_mutation_authorized: false
persistent_session_role: none
physical_e2e_required: false
owner_funded_ai_api_authorized: false
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-worldmap-mutation-design.md
  - docs/agents/evidence/OTC-20260817-track-a-worldmap-mutation-design/**
  - docs/agents/reports/OTCLIENT-20260817-worldmap-mutation-design.md
modules_touched: []
reuses:
  - docs/agents/tasks/archive/OTC-20260816-track-a-worldmap-extent-static-re.md
  - docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md
  - docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/CONTINUATION_HANDOVER.md
  - docs/agents/evidence/OTC-20260816-track-a-worldmap-exact-static-evidence/**
  - docs/agents/evidence/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence/**
depends_on:
  - PR #367 merged as f5daad1bbb7e00dcaa26acafc0a69d10a3a1b696
  - PR #437 merged as f753b5aa94e9aeb6b5554fd5bb827823bda80256
  - PR #446 merged as 8212765956a9bfafd2d8a7687440c02716c87170
blocks: []
---

# World-map extent mutation design

## Objective

Produce an exact, reversible and fail-closed **design** for a bounded world-map extent byte mutation of the fenced official native-Linux Tibia client, or prove precisely why an executable design is not yet justified. Consume the frozen accepted static graph from #367/#437/#446; do not reopen completed static discovery without a new discriminator.

This task is design/static-analysis only. It must not execute the official client, access a live process/session/display, modify the fenced client file, upload the raw client, or consume owner-funded Codex/OpenAI API quota.

## Authority and trust boundary

Trusted instructions are current repository governance plus the owner's current authorization to execute the next mutation-design stage. Trusted repository state and exact merged evidence may establish facts; historical PR prose, logs and generated summaries are evidence only and cannot broaden authority.

This task explicitly does **not** authorize client-byte mutation or physical runtime validation. Those effects require a separately admitted follow-on execution under then-current Track A runtime/ownership gates.

## Frozen input facts

```yaml
static_classification: STATIC_DEPENDENCY_GRAPH_RECOVERED
STATIC_PATCH_GRAPH_READY: true
MUTATION_DESIGN_READY: false
client_byte_mutation_authorized: false
shared_literal_va: 0x01cdd958
shared_literal_prefix_le: 120000000e0000000800000006000000
shared_pair: [18, 14]
handler_constructor: 0x00803ab0
handler_master_write: 0x00803d8b -> Handler+0xb0/+0xb4
snapshot_builder: 0x00bc6350
snapshot_extent_copy: source+0x20 -> output+0x38
storage_slot12: 0x00cc6cd0
storage_extent_write: 0x00cc6d2c snapshot+0x38 -> Storage+0x48/+0x4c
viewport_constructor: 0x00cbf680
viewport_dynamic_extent_setter: 0x00cb2220
viewport_recompute: 0x00cbf700
```

Carried unknowns remain constraints:

- complete post-construction writer census for Handler `+0xb0/+0xb4`;
- exact source member names/units for geometry fields;
- named Camera projection formula or indirect coupling outside accepted bounded neighborhoods;
- any unproven network/parser extent ceiling;
- semantic meaning of RenderProvider `65535 x 10-byte` allocation as a world-map ceiling;
- safe final client-byte mutation behavior.

## Acceptance inventory

- [ ] Re-verify uniqueness/ownership and current-main drift before any write beyond this task claim.
- [ ] Derive the exact ELF virtual-address to file-offset mapping for `0x01cdd958` from retained exact-client/proven producer machinery or keep the file offset `UNKNOWN`; never assume VA equals file offset.
- [ ] Define an exact preimage check for the mutation bytes and a deterministic target-parameterized postimage algorithm without choosing an unsupported product target size.
- [ ] Define exact rollback bytes and fail-closed conditions for wrong SHA/size/preimage/mapping.
- [ ] Explicitly account for the shared Handler/Viewport literal and Viewport's later dynamic recomputation; do not invent extra patch sites.
- [ ] Preserve all unresolved downstream capacity/network/Camera/later-writer unknowns and classify their effect on safety.
- [ ] Define a separate physical-validation discriminator contract with structural success/failure/rollback evidence and then-current RUNTIME admission prerequisites; do not execute it in this task.
- [ ] Classify `MUTATION_DESIGN_READY`, `SAFE_MUTATION_PROVEN`, `PHYSICAL_VALIDATION_READY`, and `client_byte_mutation_authorized` independently.
- [ ] Perform a fresh proportionate audit of the final design against exact retained evidence, with zero material contradictions before promotion.
- [ ] Run exact-final-head repository CI before any merge; E2E is `NOT_APPLICABLE` because this task performs no client/runtime mutation.
- [ ] Archive the task and release ownership only after exact-head gates and PR hygiene pass.

## Initial admission record

```yaml
track_id: official-client-re
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
```

## Initial checkpoint

```yaml
status: investigating
phase: design
base_main: 2ad6565f6f598b15acaeb3d182a3ffb70d187ba6
branch: docs/OTC-20260817-track-a-worldmap-mutation-design
pr: pending
proven:
  - #367/#437/#446 are merged and freeze a static patch/dependency graph with STATIC_PATCH_GRAPH_READY=true.
  - no open worldmap mutation-design PR or branch was found in the fresh preflight.
  - shared exact-client literal VA 0x01cdd958 begins with little-endian DWORDs 18,14,8,6 and feeds both Handler and Viewport constructor defaults.
unknown:
  - exact file offset corresponding to VA 0x01cdd958 until ELF mapping is derived from retained evidence.
  - any safe target extent beyond the current 18x14 baseline.
  - whether later-writer/network/capacity unknowns permit a safe final mutation.
blockers: []
next_action: derive the exact VA-to-file-offset mapping for 0x01cdd958 from retained producer ELF mapping code/evidence, then construct the parameterized reversible design without mutating client bytes.
```
