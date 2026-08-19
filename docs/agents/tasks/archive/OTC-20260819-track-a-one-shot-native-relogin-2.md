---
task_id: OTC-20260819-track-a-one-shot-native-relogin-2
status: completed
phase: closed
session_role: released
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: bounded_runtime_login
branch: runtime/OTC-20260819-track-a-one-shot-native-relogin-2
base_branch: main
runtime_access: ephemeral_isolated
runtime_owner_task: null
runtime_namespace: docker:otclient-track-a-kasmvnc/display:1
ownership_released: true
credentials_allowed: false
gui_input_authorized: false
---

# Result
`RESULT=SUCCESS`

Fresh bounded native relogin succeeded on exact official-client build size `52109920`, SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`.

Physical proof: GitHub Actions run `32260043115`, successful rerun job `96091716174`.

The single owner-authorized credential ingress returned `NATIVE_AUTH_INGRESS=PASS_WITH_PROCESS_HANDOFF`; credential values were masked/not logged and `SECOND_SECRET_ATTEMPT=false`.

The corrected no-kill path preserved the authenticated client process after handoff. `CLIENT_TERMINATED_BY_WORKFLOW=false`, bridge and character socket peer provenance matched replacement PID `19590`, `HANDOFF_HELPER_PROVENANCE=PASS`, `NATIVE_CHARACTER_COUNT=1`, and native `CONFIRM_UNIQUE` returned `NATIVE_CHARACTER_CONFIRM=PASS`.

Final fresh causal proof reported `CHARACTER_ACTUALLY_LOGGED_INTO_GAME=YES`, `CAUSAL_PROOF=COMPLETE`, and `STRUCTURAL_IN_GAME=PASS` with validated hits equal to one for `player_protocol_handler`, `gameserver_game_session`, and `worldmap_handler`.

# Root cause and durable decision
The prior failure was self-inflicted: post-auth helper restore sent `SIGTERM` to the authenticated replacement client and relaunched it, destroying the valid session at character selection. The durable rule is: after successful native auth handoff, never terminate/restart the replacement client merely to restore instrumentation. Preserve the live process and use only helper sockets whose `SO_PEERCRED` provenance matches that exact PID; otherwise fail closed.

The temporary credential-bearing workflow used for this bounded validation was removed before promotion.