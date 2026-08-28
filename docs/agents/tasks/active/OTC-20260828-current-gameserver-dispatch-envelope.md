---
task_id: OTC-20260828-current-gameserver-dispatch-envelope
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: source_research
branch: research/OTC-20260828-current-gameserver-dispatch-envelope
related_pr: 737
base_branch: main
base_main: 470d5bd285e29f9d3f24f70ff3fc5370e2990e2a
created: 2026-08-28T09:41:41+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
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
physical_e2e_required: false
implementation_authorized: false
owned_paths:
  - .github/workflows/tibia-official-client-re-current-gameserver-dispatch-envelope.yml
  - tools/tibia_re_gameserver_dispatch_envelope/**
  - docs/agents/tasks/active/OTC-20260828-current-gameserver-dispatch-envelope.md
modules_touched: []
reuses:
  - PR #729 exact-current public Linux client WARP/fence pattern
  - trusted-main current inbound XTEA/padding and GameserverMessage evidence
blocks:
  - Track B PR #284 next evidence-derived current-inbound parser change
---

# Current Gameserver dispatch-envelope source research

## Objective

Recover, on exact public Linux Tibia `15.32.75d4a0`, the static dispatch contract immediately after inbound XTEA/padding processing and before typed `GameserverMessage*` handling. Resolve current dispatch ID `0x34` to either a concrete protobuf subtype or an explicit unknown/fallback classification without running the official client, logging in, accessing secrets, process memory, packet payloads or gameplay.

## Triggering bounded evidence

Track B PR #284 exact run `33150944475`, world-entry job `98782709382`, produced a complete first decrypted application payload of length four. The structure-only lab classifier exposed no raw payload bytes and classified its first byte as decimal 52 (`0x34`); interpreting the complete payload directly as protobuf was structurally invalid. No identical E2E was retried. This Track A task researches the official Linux binary only and does not modify Track B.

## Safety / admission

```yaml
runtime_access: none
official_client_execution: false
login_performed: false
secret_access: false
process_memory_access: false
packet_capture: false
raw_client_uploaded: false
track_b_mutation: false
```

## Method

1. Reuse the already-audited GitHub-hosted WARP package acquisition pattern.
2. Hard-fence exact package/client version, hashes and size before analysis.
3. Statically recover the `GameserverMessage` dispatch reader, its byte-ID jump table, the `0x34` case, and the case metadata's Itanium RTTI/vtable identity.
4. Cross-check known IDs against exact-current login message types where the binary itself proves them.
5. Upload only sanitized structural JSON; delete the proprietary client before artifact upload.

## Invocation budget checkpoint

```yaml
invocation_started_at: 2026-08-28T09:15:00+02:00
last_progress_at: 2026-08-28T09:41:41+02:00
ci_state_checks_current_generation: 0
unchanged_external_state_checks: 0
identical_failure_retries: 0
repair_cycles_current_gate: 0
```

next_action: publish source-only RED contract, observe exact hosted RED before any analyzer implementation, then implement the smallest static resolver and run it on exact 15.32.75d4a0
