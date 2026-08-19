---
task_id: OTC-20260817-track-a-native-game-login-credential-proof
status: promotion_pending
session_role: coordinator
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: static_reverse_engineering
phase: coordinator-promotion
source_pr: 499
source_branch: docs/OTC-20260817-track-a-native-game-login-credential-proof
source_head: 6b814f90d4e6d72238651b48be0621dd4c9fa6f3
source_disposition: close_unmerged_after_promotion
coordinator_review: 4971650428
coordinator_decision: ACCEPT_WITH_EDITS
open_material_findings_after_repair: 0
historical_exact_client_version: 15.32.df7b29
historical_exact_client_size: 51965216
historical_exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
source_final_provenance_run: 32066254378
source_governance_run: 32066665095
source_governance_result: SUCCESS
source_ci_run: 32066665482
source_ci_result: SUCCESS
promotion_base: a85ef28b6f79b0f704378ebd1f7a4c5e6e7070dc
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

# Native game-login credential flow — coordinator archive checkpoint

## Disposition

Source #499 is accepted with edits as unique historical exact-build static evidence. Source history is stale, so accepted phase evidence/research is promoted through a clean current-main branch together with a coordinator semantic correction.

## Accepted historical result

For exact client `e6c244bd...` only:

- `GameclientMessageLogin` contains nested `LoginRSAEncryptedBlock` at field 7;
- exact wire tag/types for the top-level message and nested RSA block are structurally recovered;
- producer path is owned by `TLoginProtocolMessageHandler` and reaches `TProtocolMessageQueue::sendLogin(GameclientMessageLogin)`;
- producer state is sourced from `TAuthenticationAndEncryptionInfo`;
- secondary login is structurally separate.

The semantic identity of individual fields remains UNKNOWN. In particular:

```text
PASSWORD_REQUIRED_FOR_GAME_LOGIN: UNKNOWN
PASSWORD_PRESENT_IN_GAME_LOGIN: NOT_PROVEN
PASSWORD_ABSENT_FROM_GAME_LOGIN: NOT_PROVEN
```

## Coordinator correction

A native direct-to-character-selection route exists for suitable retained state, but generalized `CAN_SKIP_LOGIN_FORM` remains `PARTIAL`; the source prose must not be read as a universal `YES` across cold-start/persistence/expiry conditions.

## Current-build boundary

No source address/vtable/offset is reusable as a current-build address for `ed5469...`. Later current-build auth work may corroborate architecture but does not rebase these historical offsets.

## Safety

No runtime, login, credentials, GUI input, gameplay, transaction or client mutation is part of this static task/closeout.

After promotion merge, close #499 unmerged as superseded and lifecycle-update this archive to `completed/released` with final promotion facts and `ownership_released:true`.
