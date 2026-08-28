---
task_id: OTC-20260828-current-prelogin-outbound-sequence
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: source_research
branch: research/OTC-20260828-current-prelogin-outbound-sequence
related_pr: 742
base_branch: main
base_main: 5ac2eef58ebcff2f0e00ec1de008d51f2cd1fe59
created: 2026-08-28T10:10:00+02:00
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
  - .github/workflows/tibia-official-client-re-current-prelogin-outbound-sequence.yml
  - tools/tibia_re_prelogin_outbound_sequence/**
  - docs/agents/tasks/active/OTC-20260828-current-prelogin-outbound-sequence.md
modules_touched: []
reuses:
  - PR #737 exact-current public Linux WARP/fence pattern
  - trusted-main current final writer/login schema/dispatch promotions
blocks:
  - Track B PR #284 next official-service E2E
---

# Current pre-login outbound sequence source research

## Objective

On exact public Linux Tibia `15.32.75d4a0`, recover the native outbound `GameclientMessage*` sequence around first game-server connection and `TProtocolMessageQueue::sendLogin`, bounded from socket/connect entry through the first server-message receive boundary. Determine whether messages such as `GameclientMessageClientDetails`, `GameclientMessageSetClientOptions`, `GameclientMessageEnterWorld`, `GameclientMessageSecondaryLogin`, or another concrete generated message are causally sent before any server login-success response.

## Triggering bounded evidence

Track B V6 run `33153487819`, exact build job `98790748187`, world-entry job `98791849013`, proved valid HTTP session/playdata, one selected world/character, game TCP/WARP setup and a 102-byte client login write but **zero server bytes**. The promoted `0x34` fallback handler was not exercised. Identical official-service retry is forbidden. A new game E2E is allowed only after exact-current static evidence proves a material outbound delta.

## Safety

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

1. Hard-fence exact current public package/client version, hashes and size.
2. Statically resolve first game-server connect/login producer and queue/writer callsites.
3. Enumerate only causally reachable concrete `GameclientMessage*` sends from connect through first receive boundary; preserve order only where static control flow proves it.
4. Classify each candidate as `PROVEN_BEFORE_FIRST_RECV`, `CONDITIONAL_BEFORE_FIRST_RECV`, or `NOT_PROVEN_BEFORE_FIRST_RECV`.
5. Upload sanitized structural JSON only; never execute or upload the proprietary client.

next_action: publish TDD RED contract, require hosted RED before package acquisition, then implement the smallest exact-current static outbound-sequence resolver