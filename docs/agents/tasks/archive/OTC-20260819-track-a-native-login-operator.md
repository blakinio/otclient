---
task_id: OTC-20260819-track-a-native-login-operator
status: completed
session_role: released
project_lane: otclient
lane: RUNTIME_TOOLING
track_id: official-client-re
task_kind: permanent_operator
branch: ci/OTC-20260819-track-a-native-login-operator
base_branch: main
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
ownership_released: true
---

# Result
Promoted the physically proven PR #599 no-kill native login sequence into permanent trusted-main operator `.github/workflows/track-a-native-login.yml` and documented it in `docs/agents/operators/TRACK_A_NATIVE_LOGIN.md`.

The workflow supports owner-only manual dispatch and an exact owner-authored GitHub connector command on PR #599. It exact-fences the current official Linux client, keeps credentials confined to one bounded ingress step, never kills/restarts the authenticated replacement client after handoff, verifies helper socket `SO_PEERCRED`, fails closed unless exactly one character exists, uses native `CONFIRM_UNIQUE`, and requires fresh structural IN_GAME 3/3.

The operator intentionally does not recreate a missing/stale one-shot auth listener. That is a separate pre-auth runtime mutation requiring fresh Track A admission; a preflight failure occurs before secret access.

# Validation
Exact implementation head `fed64a28dc37d59938441b38aeea79fd67317b4f` passed:
- CI run `32264044331` = SUCCESS, including yamllint and pinned actionlint;
- Track A agent runtime governance run `32264044146` = SUCCESS;
- Track A canonical live governance run `32264043985` = SUCCESS.

No physical login and no credential use occurred during this implementation task. The permanent operator must still be dispatched only after fresh runtime admission and fresh owner one-shot authorization.
