---
task_id: OTC-20260818-native-cold-auth-qmeta
status: completed
agent: ChatGPT
session_role: coordinator_closeout
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: discovery
phase: closed
branch: research/OTC-20260818-native-cold-auth-qmeta
base_branch: main
updated: 2026-08-18T08:08:00+02:00
risk: high
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
implementation_pr: 505
implementation_head: 1a9bfb06e8f1ff1fa60784158f97545de70b338d
implementation_merge_commit: 17cc0dc1bf29c440cc08e443bdce98e4dde7be5d
coordinator_review_comment: 5324285273
ownership_released: true
research_status: PROMOTED_STATIC_CONTRACT
---

# Terminal result

PR #505 was independently coordinator-reviewed, marked ready only after the bounded static result was complete, and squash-merged after branch protection produced and passed a new ready-state `CI / Required` generation.

The promoted fact is intentionally narrow and exact-build-specific:

```text
client_version=15.32.df7b29
client_size=51965216
client_sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
qmeta_class=tibia::client::TGameClient
qmeta_method=onRequestLoginWithCredentials(QString,QString)
InvokeMetaMethod_id=17
static_metacall=0xd06260
method17_dispatch_target=0xd06850
instruction_fence=488b5110488b71084883c4485b5de92d389eff0f1f440000488bbfa009000048
```

The second executable table found in the same static-metacall region remains a negative control because its own dispatch range is only `0..4`; it is not the full 44-method `TGameClient` dispatcher.

This promotion does **not** claim account authentication, 2FA completion, character activation or `IN_GAME`. Runtime use still requires fresh exact process/PIE/fence proof, unique live `tibia::client::TGameClient`, Qt-thread affinity and protected transient credential ingress. The preferred runtime consumer uses Qt's named invocation machinery rather than an arbitrary direct-call RPC.

Credential values remain forbidden in textual bridge IPC, argv, environment variables, logs, artifacts and plaintext temporary files. The older `TIBIA_TEST_*` environment handoff used by PR #475 generations is not accepted for the native-login prompt.

# Validation and promotion

```text
static_proving_run=32104348691 / job 95610768376 SUCCESS
cleaned_head=38e216bacabe4f96cd0b4468d6db040c38b6839c
cleaned_head_native_discriminator=32104887420 SUCCESS
cleaned_head_track_a_governance=32104887441 SUCCESS
cleaned_head_ci=32104887681 SUCCESS
final_head=1a9bfb06e8f1ff1fa60784158f97545de70b338d
final_head_native_discriminator=32105128472 SUCCESS
final_head_track_a_governance=32105128481 SUCCESS
final_head_ci=32105128646 SUCCESS
ready_state_required_ci=32105494322 SUCCESS
review_threads=0
coordinator_outcome=ACCEPT
merge_commit=17cc0dc1bf29c440cc08e443bdce98e4dde7be5d
runtime_e2e=NOT_APPLICABLE_WITH_REASON static runtime_access:none task
```

# Closeout

```yaml
result: DONE
static_native_cold_auth_contract_promoted: true
form_ui_used: false
client_executed_by_task: false
runtime_access: none
runtime_ownership_claimed: false
ownership_released: true
blocker: none
next_action: implement a separately owned bounded native AUTH_WITH_CREDENTIALS consumer on the existing runtime bridge with protected non-env/non-argv credential ingress; do not start physical auth while another Track A runtime owner is active
```
