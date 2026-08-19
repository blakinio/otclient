---
task_id: OTC-20260817-track-a-native-game-login-credential-proof
status: completed
session_role: released
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: static_reverse_engineering
phase: closed
source_pr: 499
source_branch: docs/OTC-20260817-track-a-native-game-login-credential-proof
source_head: 6b814f90d4e6d72238651b48be0621dd4c9fa6f3
source_disposition: closed_unmerged_superseded
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
initial_promotion_pr: 588
initial_promotion_disposition: closed_unmerged_superseded_restack
promotion_base: c056a38aeecb3f88b9c8b140997933d23c51027f
promotion_pr: 589
promotion_head: f8cc6f3336670bcd5380c962a21397a66d235a68
promotion_merge: db5fdefbd205d5acdf31b0f5ebc893a2da7c357c
promotion_merge_method: squash
promotion_changed_paths: 8
promotion_ahead_by: 1
promotion_behind_by: 0
promotion_ci_run: 32248884463
promotion_ci_result: SUCCESS
promotion_review: 4971696699
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

# Native game-login credential flow — terminal archive

## Terminal disposition

The bounded historical native game-login credential/wire task is complete and ownership is released. Source PR #499 was closed unmerged as superseded after independently audited clean promotion #589 squash-merged as:

```text
db5fdefbd205d5acdf31b0f5ebc893a2da7c357c
```

Initial promotion #588 was closed unmerged when `main` advanced concurrently; #589 was rebuilt as one commit directly on the then-current `main@c056a38aeecb3f88b9c8b140997933d23c51027f` rather than relying on stale ancestry.

## Historical exact-build boundary

All addresses, vtables, producer offsets and protobuf implementation details are fenced to historical official Linux client:

```text
version token  15.32.df7b29
client size    51965216
client SHA256  e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

They are not current-build addresses for later `ed5469...`.

## Accepted structural wire/provenance result

For this exact historical binary:

- `GameclientMessageLogin` contains nested `LoginRSAEncryptedBlock` at field 7;
- bounded protobuf wire tag/types are recovered for the top-level login and nested RSA block;
- the native producer path is `TLoginProtocolMessageHandler` to `TProtocolMessageQueue::sendLogin(GameclientMessageLogin)`;
- producer state is sourced from `TAuthenticationAndEncryptionInfo` (historical vtable `0x2f63240`);
- secondary login is a structurally separate message/RSA-block family.

## Canonical semantic boundary

The source's conditional retained-state route is preserved without turning it into a universal login-bypass claim:

```text
DIRECT_TO_CHARACTER_SELECTION_ROUTE_FOR_VALID_RETAINED_STATE: YES
CAN_SKIP_LOGIN_FORM_GENERALIZED: PARTIAL
```

Credential-field semantics remain fail-closed:

```text
PASSWORD_REQUIRED_FOR_GAME_LOGIN: UNKNOWN
PASSWORD_PRESENT_IN_GAME_LOGIN: NOT_PROVEN
PASSWORD_ABSENT_FROM_GAME_LOGIN: NOT_PROVEN
```

No specific `LoginRSAEncryptedBlock` field is canonically renamed to email/account/password/session-token/device semantics. The causal mapping from `TPlaySessionData` through authentication state to a specific wire field remains unproven.

## Validation

Source exact-head validation:

```text
Track A governance       32066665095 = SUCCESS
CI                       32066665482 = SUCCESS
final provenance run     32066254378 = SUCCESS
```

Clean final promotion #589:

```text
head                     f8cc6f3336670bcd5380c962a21397a66d235a68
ahead_by                 1
behind_by                0
changed paths            8
CI                        32248884463 = SUCCESS
promotion review          4971696699
review threads            0
merge                     db5fdefbd205d5acdf31b0f5ebc893a2da7c357c
```

## Safety

The source, coordinator audit, clean promotion and lifecycle closeout are static/repository work only. No official-client execution, credential use, login, GUI input, gameplay, economy/account transaction, process-memory access or runtime mutation occurred during coordinator work.
