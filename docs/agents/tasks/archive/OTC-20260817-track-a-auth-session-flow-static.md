---
task_id: OTC-20260817-track-a-auth-session-flow-static
status: promotion_pending
session_role: coordinator
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: static_reverse_engineering
phase: coordinator-promotion
source_pr: 498
source_branch: docs/OTC-20260817-track-a-auth-session-flow-static
source_head: 43438bb8ed42841c8a9f5bc2d0e76d05b466a958
source_disposition: close_unmerged_after_promotion
coordinator_review: 4971599610
coordinator_decision: ACCEPT_WITH_EDITS
open_material_findings_after_repair: 0
historical_exact_client_version: 15.32.df7b29
historical_exact_client_size: 51965216
historical_exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
historical_packed_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
source_final_static_run: 32057651024
source_generic_ci_result: SUCCESS
source_governance_run: 32058753745
source_governance_result: FAILURE_DELIVERY_ONLY
source_workflow_promoted: false
promotion_base: 5a1c3f448b850fa388275f5b7af7be9218e132ff
promotion_pr: pending
promotion_head: pending
promotion_merge: pending
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
ownership_released: false
---

# Native auth/session static flow — coordinator archive checkpoint

## Disposition

Source #498 is accepted with edits as unique **historical exact-build** static evidence. It is not merged directly because the source branch is stale and its added runtime-sensitive workflow fails current Track A delivery governance.

The workflow is intentionally excluded from clean promotion. Durable phase evidence and `NATIVE_AUTH_SESSION_FLOW.md` are preserved byte-identically from the accepted source head, together with a coordinator audit that fixes provenance/boundary wording.

## Accepted historical conclusions

For exact client `e6c244bd...` only:

```text
CAN_SKIP_LOGIN_FORM: PARTIAL
CAN_SKIP_PASSWORD_ENTRY: PARTIAL
CAN_REUSE_SESSION: YES
PASSWORD_REQUIRED_FOR_GAME_LOGIN: UNKNOWN
DIRECT_CHARACTER_LOGIN_POSSIBLE: YES, conditional on valid retained auth/play-session state
```

The static model establishes separation between initial credential submission, `TPlaySessionData`-bearing account-auth success, retained-state character-selection routing, selected-character game-server progression, and later existing-credentials game connection.

It does not establish persistence storage, expiry/refresh semantics, exact game-login credential fields, plaintext-password absence/presence in internal serialized payloads, or future/current-build address equivalence.

## Current-build relation

Later current-build #556/#528 work corroborates key controller concepts on client SHA `ed5469...`, but the historical addresses in #498 are never rebased or treated as current.

## Source delivery correction

Source governance run `32058753745` failed only because the source PR carried `.github/workflows/tibia-official-client-re-auth-session-static.yml` without an active admission task bound to that branch. Coordinator promotion excludes that workflow rather than weakening governance or inventing runtime authority.

## Safety

This task and closeout are repository/static only. No runtime, login, credentials, GUI input, gameplay, transaction or client mutation is performed.

After promotion merge, close source #498 unmerged as superseded and lifecycle-update this archive to `status: completed`, `session_role: released`, final promotion facts and `ownership_released: true`.
