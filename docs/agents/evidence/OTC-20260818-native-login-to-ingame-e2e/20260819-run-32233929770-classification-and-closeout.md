# Run 32233929770 classification and PR #528 closeout checkpoint

Task: `OTC-20260818-native-login-to-ingame-e2e`  
PR: `#528`  
Date: `2026-08-19`

This checkpoint is sanitized. It contains no credential values, session secrets, screenshots, packet payloads, proprietary client bytes, or secret-bearing environment output.

## Repository state before closeout reconciliation

```text
live main=e4357137e47836d67eb19ceb13a8e313f69bf778
PR #528 head=5ff501a783956c114aaa2d911a16f3b72e21e82e
merge-base=066a5ba8b1811ef61d3aa8ac2ff3fc3601fe7b9d
ahead_by=158
behind_by=20
```

PR #528 remained the active usable owner and no replacement task or PR was created.

## Exact run/job classification

Workflow run `32233929770`, job `96009597899`, reached the bounded one-shot native-auth step after exact current-client/helper/runtime revalidation and helper-preloaded relaunch had succeeded.

The one-shot ingress terminated with:

```text
NATIVE_AUTH_RESPONSE_FAILED
```

Source inspection of `tools/tibia_runtime_bridge/current_sha_secret_ingress.cpp` establishes the ordering of this marker. It is emitted only after the ingress has already completed its secret-source non-empty/bounded checks, protected in-memory handling, memfd creation/write/sealing/identity checks, Unix-socket connection, same-UID and expected-PID peer validation, and `SCM_RIGHTS` descriptor send, then fails to receive the expected helper success response.

Therefore the concrete classification is:

```text
missing_or_empty_github_secret=RULED_OUT
secret_ingress_local_validation_failure=RULED_OUT_BEFORE_RESPONSE_PHASE
socket_peer_or_pid_mismatch=RULED_OUT
sealed_memfd_or_scm_rights_failure=RULED_OUT
current_auth_helper_response=LOST_ACROSS_NATIVE_PROCESS_HANDOFF
qmeta_terminal_response=NOT_RETURNED_TO_INGRESS_DUE_PROCESS_HANDOFF
runtime_object_or_thread_failure=NOT_OBSERVED
native_authentication_state_machine_failure=RULED_OUT_BY_LATER_CAUSAL_PROOF
ROOT_CAUSE=HELPER_IPC_RESPONSE_CHANNEL_LOST_ACROSS_NATIVE_PROCESS_HANDOFF
```

The marker is therefore a helper-response-channel failure, not evidence that the account authentication state machine failed.

## Causal E2E resolution

After the handoff, a later exact-client restart with the already-proven current-SHA helper set and **without another credential ingress** restored observation of the authenticated play session. On the exact current official client at PID `27368`, all required structural discriminators returned exactly one validated hit:

```text
player_protocol_handler=1
gameserver_game_session=1
worldmap_handler=1
```

The same proof point had the exact current official-client identity:

```text
size=52109920
sha256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
DISPLAY=:1
persistent_secret_environment=false
```

The durable result is:

```text
RESULT=SUCCESS_AT_PROOF_POINT
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=YES
CAUSAL_PROOF=COMPLETE
STRUCTURAL_IN_GAME=PASS_3_OF_3
SECOND_SECRET_ATTEMPT=NOT_PERFORMED
```

A later process handoff returned the client to the normal login state and all three discriminators were then zero on PID `11365`. This is recorded separately as `POST_HANDOFF_SESSION_STABILITY=FAIL_NOT_RETAINED`; it does not erase the already-proven login-to-world E2E event.

## Why the bounded credential step is not repeated

The current exact-client E2E event already has causal structural proof and the one-shot credential ingress has already been consumed once. Reusing the account Secrets solely to reproduce an already-proven event would repeat an experiment with a hard result and would add credential exposure without improving the success proof. No second credential attempt is authorized or required for closeout.

## Final-diff cleanup decision

The closeout reconciliation intentionally keeps only task-owned durable governance/evidence/current-SHA helper source needed to explain and reproduce the semantic implementation boundary. It removes branch-only restack debt and completed physical execution machinery from the final PR diff:

```text
S7/S8/S9 restacked documentation debt=REMOVE
three task-specific temporary native-login workflows=REMOVE
completed one-shot canonical teardown script=REMOVE
native-login sanitized evidence=KEEP
native-login prompt and KasmVNC access contract=KEEP
current-SHA gate/secret-ingress/character-control sources=KEEP
```

Temporary workflow removal is deliberate so later branch synchronization cannot retrigger obsolete runtime or credential-bearing operations.

## Remaining closeout gates

No live runtime mutation, credential access, login, character selection, gameplay action, screenshot capture, or process cleanup is part of this closeout phase.

After the clean reconciliation onto live `main`, completion still requires a fresh independent post-implementation audit on the exact reconciled head, exact-head required CI/governance, zero material review findings, final PR hygiene, then merge/archive/ownership release under repository policy. The existing successful physical E2E is retained and is not rerun merely for closeout.
