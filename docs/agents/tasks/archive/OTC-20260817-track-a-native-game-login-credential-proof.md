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
branch: docs/OTC-20260817-track-a-native-game-login-credential-proof
base_branch: main
base_main: 8a5fcfd72f2554261eef91a2129c9cc076e730ea
related_pr: "#499"
risk: medium
execution_class: github_hosted
runtime_access: none
physical_e2e_required: false
mutation_authorized: false
promotion_authority: coordinator_only
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
invocation_started_at: 2026-08-17T21:17:00+02:00
last_progress_at: 2026-08-17T22:22:00+02:00
completion_result: partial-research-terminal-static
next_action: coordinator review/promotion of PR #499; any runtime semantic-provenance follow-up requires a new separately admitted task
---

# Track A — native game-login credential field proof

## Completion record

The authorized static-only scope is complete and exhausted.

```text
AUTHORIZED_STATIC_TASK: COMPLETED
RESEARCH_RESULT: PARTIAL
GAME_LOGIN_MESSAGE_TYPE: GameclientMessageLogin                         FACT
PROTECTED_LOGIN_BLOCK: LoginRSAEncryptedBlock in field 7                FACT
NATIVE_PRODUCER: TLoginProtocolMessageHandler @ 0xe1abe0                FACT
RETAINED_SOURCE_TYPE: TAuthenticationAndEncryptionInfo                  FACT
RETAINED_SOURCE_VTABLE: 0x2f63240                                       FACT
SECONDARY_LOGIN_RELATION: separate message + RSA block                  FACT
PASSWORD_REQUIRED_FOR_GAME_LOGIN: UNKNOWN
PASSWORD_ABSENT_FROM_GAME_LOGIN: NOT PROVEN
PASSWORD_PRESENT_IN_GAME_LOGIN: NOT PROVEN
```

The exact-client producer consumes retained `TAuthenticationAndEncryptionInfo` values to construct the primary and secondary game-login messages. Static analysis did not recover a trustworthy semantic edge proving whether any retained value is the account password, a password-derived value, or exclusively post-auth/session/challenge material. The terminal `UNKNOWN` is therefore deliberate and evidence-safe.

The separate parent auth/session conclusion that the native login-form UI can be skipped when suitable retained authentication/session state exists is unaffected.

## Completed acceptance scope

- Exact version/size/SHA fence was revalidated for promoted binary claims.
- Generated protobuf code proved complete field/wire structure for `GameclientMessageLogin` and `LoginRSAEncryptedBlock`.
- Producer ownership and retained source RTTI/vtable were recovered.
- Primary and secondary login paths were distinguished.
- Queue handoff was recovered for both paths.
- Descriptor recovery, direct retained-field writer lookup, QMeta-controller recovery, and final receiver-side provenance were exercised fail-closed.
- The password question was resolved to the strongest evidence-safe terminal value, `UNKNOWN`, with the exact missing discriminator documented.
- No credential/session values, packet payloads, live login, process memory, X11 observation, TLS weakening, auth bypass, or PR #475 runtime/session were used.

## Durable evidence

- `docs/agents/evidence/OTC-20260817-track-a-native-game-login-credential-proof/phase1-rtti-vtable-map.md`
- `docs/agents/evidence/OTC-20260817-track-a-native-game-login-credential-proof/phase2-protobuf-wire-schema.md`
- `docs/agents/evidence/OTC-20260817-track-a-native-game-login-credential-proof/phase3-complete-wire-tags.md`
- `docs/agents/evidence/OTC-20260817-track-a-native-game-login-credential-proof/phase4-queue-login-boundary.md`
- `docs/agents/evidence/OTC-20260817-track-a-native-game-login-credential-proof/phase5-final-auth-state-provenance.md`
- `docs/research/native-client/NATIVE_GAME_LOGIN_CREDENTIAL_PROOF.md`

Final narrow discriminator: workflow run `32066254378`, job `95498969337`, `SUCCESS`.

Any further attempt to prove the semantic origin of the retained credential values is outside this task and requires a new Track A admission. It must not inherit PR #475 runtime authority and must never record secret values.
