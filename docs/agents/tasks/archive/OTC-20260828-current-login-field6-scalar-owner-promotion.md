---
task_id: OTC-20260828-current-login-field6-scalar-owner-promotion
status: completed
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: archived
branch: docs/OTC-20260828-current-login-field6-scalar-owner-promotion
related_pr: 752
base_branch: main
base_main: 7a7a7cc4d09dee08ea07f8c91144d8ac869111b7
created: 2026-08-28T15:25:00+02:00
completed: 2026-08-28T15:32:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
canonical_boot_epoch_recovery: NOT_APPLICABLE
canonical_recovery: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
physical_action_budget: 0
physical_action_count: 0
physical_e2e_required: false
implementation_authorized: false
owned_paths: []
modules_touched: []
---

# Archived promotion — current login field6 scalar-owner boundary

Terminal result: **DONE / PASS_BOUNDED_STATIC_VALUE_STILL_UNKNOWN**.

```text
source PR                    #751 CLOSED UNMERGED AS CONSUMED
source final head            a50a140cbdf4038921ed29e30cf0f53f8158bc27
scalar source run            33171560068 / 98849712747 = SUCCESS
scalar artifact              9686096894
focused source run           33174706577 / 98860195057 = SUCCESS
focused artifact             9687275655
source CI                    33174706753 = SUCCESS
source governance            33174706531 = SUCCESS
promotion PR                 #752 MERGED
promotion head               dc7092df2ad34ef0d6acc2f559dac9d82c85622b
promotion merge              6c1a135e81db7ccb0974ad7cf88be7c4f07088cf
promotion CI                 33175663803 = SUCCESS
promotion governance         33175663629 = SUCCESS
review threads               0
submitted reviews            0
```

The promoted result rejects every statically scalar `slot+0x60` candidate as a source for current login outer field6. In particular, `0xceddcb / edx=1` is exact-current worldmap QMeta traffic, not `TLoginProtocolMessageHandler` login traffic. The current login producer still writes outer field6 from producer input `edx`, but that runtime value remains `UNKNOWN_CURRENT_EXACT`.

No Track B payload mutation or official-service game E2E is authorized from this result. The successor must obtain fresh Track A runtime admission and observe only the input scalar `edx` at exact current producer entry `0xe25620`, without credentials/session values or packet payload capture.

next_action: NOT_APPLICABLE — promotion lifecycle complete; successor runtime observation owns the next evidence boundary.
