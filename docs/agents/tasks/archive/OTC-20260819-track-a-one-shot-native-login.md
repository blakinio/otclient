---
task_id: OTC-20260819-track-a-one-shot-native-login
status: completed
session_role: released
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: bounded_runtime_login
source_pr: 598
source_branch: runtime/OTC-20260819-track-a-one-shot-native-login
runtime_access: ephemeral_isolated
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: docker:otclient-track-a-kasmvnc/display:1
target_uniqueness: PROVEN
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
credentials_consumed_once: true
secret_values_logged: false
gui_input_authorized: false
second_secret_attempt_performed: false
physical_run: 32255003447
physical_job: 96074639743
native_auth_result: PASS_WITH_PROCESS_HANDOFF
native_character_count: 1
native_character_confirm: PASS
character_actually_logged_into_game: true
causal_proof: COMPLETE
structural_in_game: PASS_3_OF_3
live_recheck_pid: 23415
live_recheck_client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
live_recheck_player_protocol_handler_hits: 1
live_recheck_gameserver_game_session_hits: 1
live_recheck_worldmap_handler_hits: 1
ownership_released: true
---

# Track A one-shot native login — terminal archive

## Result

The owner-authorized bounded one-shot native login completed successfully on the unique KasmVNC runtime namespace. Credential values were never printed or committed, and no GUI credential entry, OCR, image matching, coordinate input, blind keyboard/mouse automation, Tab/Enter submission, TLS weakening, authentication bypass or fabricated server response was used.

```text
RESULT=SUCCESS
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=YES
CAUSAL_PROOF=COMPLETE
STRUCTURAL_IN_GAME=PASS
SECOND_SECRET_ATTEMPT=false
```

The successful physical workflow was run `32255003447`, job `96074639743`. Before secret access it revalidated the exact current client and helper runtime. The bounded ingress reached the known native process-handoff condition and was accepted as `NATIVE_AUTH_INGRESS=PASS_WITH_PROCESS_HANDOFF`; no credential retry occurred.

After the native handoff, helper instrumentation was restored without credentials. The current native character model reported exactly one character and `CONFIRM_UNIQUE` succeeded. Structural IN_GAME then passed all three required discriminators.

A subsequent read-only live bridge recheck on PID `23415` still proved the exact client SHA and exactly one validated hit for each of `player_protocol_handler`, `gameserver_game_session`, and `worldmap_handler`.

## Non-secret failure history

An earlier temporary workflow run `32254719391`/job `96073650923` and its automatically repeated pre-auth run failed before secret access because the workflow used non-dereferencing `stat -c` on `/proc/<pid>/exe`, yielding symlink size `0`. The exact executable itself remained valid. This was repaired with `stat -Lc`; neither failed pre-auth run consumed credentials.

## Closeout

Both credential-bearing temporary workflow files were removed from the final PR diff after execution. The one-shot secret budget is consumed and is not standing authorization for another login. Runtime task ownership is released while the currently running client is left undisturbed.