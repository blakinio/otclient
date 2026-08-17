---
task_id: OTC-20260817-track-a-native-game-login-credential-proof
status: completed
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: finalized-static
execution_mode: github_actions
execution_reason: exact-SHA static protobuf/serializer reconstruction is deterministic disposable Track A P2 work and must remain off the physical runtime
branch: docs/OTC-20260817-track-a-native-game-login-credential-proof
base_branch: main
base_main: 8a5fcfd72f2554261eef91a2129c9cc076e730ea
related_pr: "#499"
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-native-game-login-credential-proof.md
  - docs/agents/tasks/archive/OTC-20260817-track-a-native-game-login-credential-proof.md
  - docs/agents/evidence/OTC-20260817-track-a-native-game-login-credential-proof/**
  - docs/research/native-client/NATIVE_GAME_LOGIN_CREDENTIAL_PROOF.md
  - .github/workflows/tibia-official-client-re-game-login-credential-proof.yml
modules_touched: []
reuses:
  - PR #498 exact-client auth/session static evidence and corrected native login queue boundary, read-only
  - historical same-SHA Track A QMeta/protobuf inventories already in blakinio/otclient
  - PR #284 official 15.32 Track B game-login oracle, read-only comparative evidence only
depends_on:
  - blakinio/otclient#498
blocks: []
cross_repo_tasks: []
policy_version: 2
prompting_standard_version: 2.1
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
decomposition_decision: single
decomposition_reason: one narrow exact-client schema/provenance question with one durable evidence product
context_pressure: medium
context_growth: stable
context_score: 9
estimate_confidence: high
validation_level: focused
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
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
owner_funded_ai_api_authorized: false
promotion_authority: coordinator_only
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
invocation_started_at: 2026-08-17T21:17:00+02:00
last_progress_at: 2026-08-17T22:22:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: finalizing
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
next_action: coordinator review/promotion of PR #499; any runtime semantic-provenance follow-up requires a new separately admitted task
---

# Track A — native game-login credential field proof

## Terminal outcome

The authorized `runtime_access:none` scope is complete and exhausted. The task recovered the exact native wire structure, producer, retained source type, and queue boundary without observing secret values or using the physical Track A runtime.

```text
AUTHORIZED_STATIC_TASK: COMPLETED
RESEARCH_RESULT: PARTIAL
GAME_LOGIN_MESSAGE_TYPE: GameclientMessageLogin
PROTECTED_LOGIN_BLOCK: LoginRSAEncryptedBlock in field 7
NATIVE_PRODUCER: TLoginProtocolMessageHandler @ 0xe1abe0
RETAINED_SOURCE_TYPE: TAuthenticationAndEncryptionInfo
RETAINED_SOURCE_VTABLE: 0x2f63240
PASSWORD_REQUIRED_FOR_GAME_LOGIN: UNKNOWN
PASSWORD_ABSENT_FROM_GAME_LOGIN: NOT PROVEN
PASSWORD_PRESENT_IN_GAME_LOGIN: NOT PROVEN
SECONDARY_LOGIN_RELATION: separate GameclientMessageSecondaryLogin + SecondaryLoginRSAEncryptedBlock
```

`UNKNOWN` is terminal for this static task: exact-client code proves that retained `TAuthenticationAndEncryptionInfo` values feed the game-login producer, but it does not statically prove the semantic origin of every retained value or a direct `TPlaySessionData -> TAuthenticationAndEncryptionInfo -> LoginRSAEncryptedBlock field` assignment.

The separate parent auth/session finding that the native login-form UI can be skipped through retained-state/session flow remains unaffected.

## Acceptance matrix

- [x] Exact client fence revalidated before promoted binary claims.
- [x] Recovered native field membership and complete wire structure for `GameclientMessageLogin` and `LoginRSAEncryptedBlock` from generated protobuf code.
- [x] Traced game-login message construction to native producer `TLoginProtocolMessageHandler @ 0xe1abe0`.
- [x] Identified exact retained source object type `TAuthenticationAndEncryptionInfo` and vtable `0x2f63240`.
- [x] Distinguished primary and secondary login message/RSA-block paths.
- [x] Recovered queue handoff `sendLogin -> 0xdf6be2 -> 0xbd36a0` and secondary equivalent.
- [x] Tested descriptor, direct-writer, QMeta-controller and final receiver-side provenance approaches fail-closed.
- [x] Resolved `PASSWORD_REQUIRED_FOR_GAME_LOGIN` to the strongest evidence-safe terminal value: `UNKNOWN`, with exact missing discriminator documented.
- [x] Persisted durable FACT / INFERENCE / UNKNOWN evidence and final report.
- [x] No credentials, cookies, tokens, session values, packet payloads, process memory, login, X11/runtime observation, input automation, raw executable upload, TLS weakening, auth/2FA bypass, or PR #475 runtime/session usage.

## Durable evidence

- `docs/agents/evidence/OTC-20260817-track-a-native-game-login-credential-proof/phase1-rtti-vtable-map.md`
- `docs/agents/evidence/OTC-20260817-track-a-native-game-login-credential-proof/phase2-protobuf-wire-schema.md`
- `docs/agents/evidence/OTC-20260817-track-a-native-game-login-credential-proof/phase3-complete-wire-tags.md`
- `docs/agents/evidence/OTC-20260817-track-a-native-game-login-credential-proof/phase4-queue-login-boundary.md`
- `docs/agents/evidence/OTC-20260817-track-a-native-game-login-credential-proof/phase5-final-auth-state-provenance.md`
- `docs/research/native-client/NATIVE_GAME_LOGIN_CREDENTIAL_PROOF.md`

Final narrow discriminator: workflow run `32066254378`, job `95498969337`, `SUCCESS`.

## Runtime boundary

```yaml
runtime_access: none
mutation_authorized: false
physical_e2e_required: false
```

PR #475 was not observed, attached to, mutated, logged through, or used as a session/runtime budget source.

A future runtime provenance experiment is outside this task and requires new explicit Track A admission. It must record only provenance/category/control-flow evidence, never secret values.
