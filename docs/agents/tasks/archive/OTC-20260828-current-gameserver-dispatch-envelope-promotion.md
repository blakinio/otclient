---
task_id: OTC-20260828-current-gameserver-dispatch-envelope-promotion
status: completed
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: archived
branch: docs/OTC-20260828-current-gameserver-dispatch-envelope-promotion
related_pr: 738
base_branch: main
base_main: 470d5bd285e29f9d3f24f70ff3fc5370e2990e2a
created: 2026-08-28T09:47:00+02:00
completed: 2026-08-28T09:53:29+02:00
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
owned_paths: []
modules_touched: []
---

# Archived promotion — current Gameserver dispatch envelope

Terminal result: **DONE / PASS_BOUNDED**.

```text
source PR             #737 CLOSED UNMERGED AS CONSUMED
source head           5273d52e0fdd3f0e2c212f633fb8e406409851ff
source run            33152704802 = SUCCESS
source job            98788182962 = SUCCESS
source artifact       9678356574
artifact sha256       9bb4f18d2d684b4a7a0f5c9254367fdfc9786c633890b2beb5fe324c421aa918
result.json sha256    eabcb9445cdafd699fb266ee94b4aca9a1b006170007cbefe682b7a6579d3764
promotion PR          #738 MERGED
promotion head        409c62c49943d74aab7fe4508d982a5cc58e1855
promotion merge       5a08ea4834b2bb6eb81ba65de7f22331658de9ef
Track A governance    33153046812 = SUCCESS
CI / Required         98789351627 = SUCCESS
review threads        0
```

Promoted exact-current controls are `0x14 -> GameserverMessageLoginError`, `0x17 -> GameserverMessageLoginSuccess`, and `0x1f -> GameserverMessageLoginChallenge`. Dispatch `0x34` is bounded to `UNKNOWN_FALLBACK` with no concrete `GameserverMessage*` type; its user-facing meaning, payload schema, and downstream semantic callback remain `UNKNOWN`.

Track B PR #284 may consume only the structural consequence from trusted main: current 15.32 Global `0x34` must not enter the legacy opcode-52 parser. The source analyzer/workflow remains intentionally unmerged and no runtime/login/secret/process-memory/raw-client evidence was promoted.

next_action: NOT_APPLICABLE — lifecycle complete; Track B #284 owns the consuming implementation.
