---
task_id: OTC-20260817-track-a-worldmap-mutation-design
status: ready
agent: ChatGPT
session_id: chatgpt-worldmap-mutation-design-20260817
session_role: mutation_design_coordinator
project_lane: otclient
lane: STATIC-RE
track_id: official-client-re
task_kind: discovery
phase: integrate
branch: docs/OTC-20260817-track-a-worldmap-mutation-design
base_branch: main
base_main: 2ad6565f6f598b15acaeb3d182a3ffb70d187ba6
pr: 452
created: 2026-08-17T10:39:00+02:00
updated: 2026-08-17T10:49:00+02:00
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
invocation_started_at: 2026-08-17T10:34:00+02:00
last_progress_at: 2026-08-17T10:49:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
result:
  STATIC_PATCH_GRAPH_READY: true
  MUTATION_DESIGN_READY: true
  OFFLINE_PATCH_PLAN_READY: true
  SAFE_MUTATION_PROVEN: false
  PHYSICAL_VALIDATION_CONTRACT_READY: true
  PHYSICAL_VALIDATION_EXECUTION_AUTHORIZED: false
  client_byte_mutation_authorized: false
  first_canary_recommendation: [19, 14]
validation:
  audit:
    result: PASS
    record: docs/agents/evidence/OTC-20260817-track-a-worldmap-mutation-design/20260817-final-audit.md
    material_findings_open: 0
    resolved_findings:
      - WM-MD-AUD-001
  e2e:
    result: NOT_APPLICABLE
    reason: documentation/design-only PR; no executable, official-client or runtime behavior is changed
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

## Terminal design result

The task has produced an exact reversible fail-closed mutation experiment design without executing or modifying the official client.

```yaml
shared_literal_va: 0x01cdd958
preimage_guard_16_hex: 120000000e0000000800000006000000
patchable_prefix_dwords: [18, 14]
trailing_guard_dwords_unchanged: [8, 6]
file_offset_rule: derive_from_exact_file_PT_LOAD_at_execution
canonical_source_patch_in_place: forbidden
first_canary_recommendation: [19,14]
first_canary_postimage_prefix_8_hex: 130000000e000000
first_canary_changed_bytes: 1
```

`[19,14]` is a one-axis causal canary recommendation, not a final desired extent. All accepted later-writer, capacity/network, RenderProvider-allocation and Camera unknowns remain explicit. No second patch site is authorized by this design.

## Durable records

- `docs/agents/evidence/OTC-20260817-track-a-worldmap-mutation-design/20260817-worldmap-mutation-design.md`
- `docs/agents/evidence/OTC-20260817-track-a-worldmap-mutation-design/20260817-final-audit.md`
- `docs/agents/reports/OTCLIENT-20260817-worldmap-mutation-design.md`

## Current admission

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

## Ready checkpoint

```yaml
status: ready
phase: integrate
branch: docs/OTC-20260817-track-a-worldmap-mutation-design
pr: 452
MUTATION_DESIGN_READY: true
SAFE_MUTATION_PROVEN: false
PHYSICAL_VALIDATION_CONTRACT_READY: true
PHYSICAL_VALIDATION_EXECUTION_AUTHORIZED: false
client_byte_mutation_authorized: false
audit_result: PASS
material_findings_open: 0
physical_e2e: NOT_APPLICABLE
blockers: []
next_action: verify exact final PR diff and review threads, obtain required exact-head CI for the ready PR generation, merge #452 if every gate passes, then archive this task and release ownership as lifecycle closeout.
```
