---
task_id: OTC-20260817-track-a-auth-session-flow-static
status: completed
session_role: released
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: static_reverse_engineering
phase: closed
source_pr: 498
source_branch: docs/OTC-20260817-track-a-auth-session-flow-static
source_head: 43438bb8ed42841c8a9f5bc2d0e76d05b466a958
source_disposition: closed_unmerged_superseded
coordinator_review: 4971599610
coordinator_decision: ACCEPT_WITH_EDITS
open_material_findings_after_repair: 0
historical_exact_client_version: 15.32.df7b29
historical_exact_client_size: 51965216
historical_exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
historical_packed_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
source_final_static_run: 32057651024
source_governance_run: 32058753745
source_governance_result: FAILURE_DELIVERY_ONLY
source_workflow_promoted: false
promotion_base: 5a1c3f448b850fa388275f5b7af7be9218e132ff
promotion_pr: 585
promotion_head: a125dfedc515d3c87499b3800a3c5704880b501e
promotion_merge: 0130493ca364cd6eaf2637c1945c0f25ad2cf137
promotion_merge_method: squash
promotion_changed_paths: 9
promotion_ahead_by: 3
promotion_behind_by: 0
promotion_ci_run: 32248049388
promotion_ci_result: SUCCESS
promotion_review: 4971626535
promotion_review_threads_open: 0
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gui_input_authorized: false
gameplay_allowed: false
transaction_authorized: false
physical_e2e_required: false
ownership_released: true
---

# Native auth/session static flow — terminal archive

## Terminal disposition

The bounded historical auth/session static task is complete and ownership is released. Source PR #498 was closed unmerged as superseded after clean coordinator promotion #585 squash-merged as `0130493ca364cd6eaf2637c1945c0f25ad2cf137`.

## Evidence boundary

All addresses, PMFs, QMeta tables, vptrs and disassembly facts are fenced to historical exact official Linux client `15.32.df7b29 / 51965216 / e6c244bd...`. They are not addresses for the later current client `ed5469...`.

Accepted bounded conclusions remain:

```text
CAN_SKIP_LOGIN_FORM: PARTIAL
CAN_SKIP_PASSWORD_ENTRY: PARTIAL
CAN_REUSE_SESSION: YES (architectural/native retained-state path)
PASSWORD_REQUIRED_FOR_GAME_LOGIN: UNKNOWN
DIRECT_CHARACTER_LOGIN_POSSIBLE: YES, conditional on valid retained auth/play-session state
```

Persistence storage, expiry/refresh policy, exact game-login credential fields, and password presence/absence in internal serialization remain unknown at this historical static boundary.

## Delivery repair

The source's runtime-sensitive static workflow was not promoted because source governance run `32058753745` correctly rejected it without a branch-bound active admission task. Canonical promotion contains only durable docs/evidence/archive material.

Promotion head `a125dfedc515d3c87499b3800a3c5704880b501e` passed generic CI `32248049388`, had zero review threads, `behind_by=0`, and exact-head promotion review `4971626535`.

No runtime, credential use, login, GUI input, gameplay, transaction or client mutation occurred during coordinator audit/promotion/closeout.
