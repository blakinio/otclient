---
task_id: OTC-20260828-current-game-login-pre-success-promotion
status: completed
agent: ChatGPT
session_role: released
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: archived
branch: docs/OTC-20260828-current-game-login-pre-success-promotion
related_pr: 747
base_branch: main
base_main: e7f710b04da8c6f3adae43a019c44a6acb4a2866
created: 2026-08-28T11:36:00+02:00
completed: 2026-08-28T11:43:42+02:00
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

# Archived promotion — current game-login pre-success outbound

Terminal result: **DONE / PASS_BOUNDED_NO_IMPLEMENTABLE_VALUE_DELTA**.

```text
source PR            #743 CLOSED UNMERGED AS CONSUMED
source head          1342423c6fe4ef675f4b0b0cdc39ae012089f20e
source workflow      33159660190 = SUCCESS
source job           98810772742 = SUCCESS
source artifact      9681208967
artifact sha256      c3fabb53fb82d1f466a82c508bfb1be9502061dc9e96737e0f33171a8415247c
result.json sha256   1c1748bbcd0cfe3410111ac3eb3f70563d6695d858cf007e8d07263adf1a472f
source CI            33159660423 = SUCCESS
source governance    33159660171 = SUCCESS
promotion PR         #747 MERGED
promotion head       fcc26d55c12001991e540fb58b4c88c241385644
promotion CI         33160447038 = SUCCESS
promotion governance 33160446901 = SUCCESS
promotion merge      2209cc052b98ebcbb4fe652c569af7c2c4b0114a
review threads       0
review submissions   0
```

Promoted exact-current fact: outer `GameclientMessageLogin.field6` is structurally present and sourced from producer input `edx`, but its runtime value and semantic name remain UNKNOWN. Nested fields `1/2/5/6/7` have structural AuthInfo source references; field 2 is conditional. Bounded direct/RIP, named auth graph, owner-field and exact Qt connection-thunk discriminators did not recover the field-6 value.

No Track B mutation or official-service game E2E is authorized by this result. The consuming blocker is `CURRENT_GAME_LOGIN_FIELD6_VALUE_STILL_UNKNOWN`.

next_action: NOT_APPLICABLE — lifecycle complete; Track B #284 owns the blocked consumer checkpoint.
