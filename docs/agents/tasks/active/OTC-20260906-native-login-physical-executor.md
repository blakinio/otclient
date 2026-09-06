---
task_id: OTC-20260906-native-login-physical-executor
status: validating
agent: ChatGPT
session_id: native-login-physical-executor-20260906
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: physical_native_login_execution
phase: validation
branch: runtime/OTC-20260906-native-login-physical-executor
base_branch: main
created: 2026-09-06T17:35:00+02:00
updated_at: 2026-09-06T18:10:00+02:00
base_main: f3b93c85dec6e8c290eaa12266ca97bbce8514a4
policy_version: 2
prompting_standard_version: 2.1
execution_mode: chatgpt
execution_reason: trusted-main canonical replacement, one-shot vault native login, unique character confirmation, and exact-current causal IN_GAME qualification
execution_class: persistent_physical_runtime
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
runtime_access: canonical_reuse_or_mutation
runtime_owner_task: OTC-20260906-native-login-physical-executor
runtime_namespace: canonical-live-runtime
physical_runtime_locator: synology:otclient-track-a-kasmvnc:display-1
canonical_registration: PRESENT
canonical_lease_generation: UNKNOWN
registration_lease_generation: UNKNOWN
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: REQUIRED_NOT_PROVEN
gate_b: REQUIRED_NOT_PROVEN
bootstrap: NOT_APPLICABLE
target_uniqueness: UNKNOWN
mutation_authorized: false
persistent_session_role: canonical_runtime_mutator
physical_e2e_required: true
implementation_authorized: true
credentials_allowed: machine_local_vault_one_shot_only
secret_values_logged: false
gui_input_authorized: false
process_control_authorized: true
physical_action_budget: bounded_exact_pid_replacement_and_native_login
run_scope: bounded_current_be4f48_native_login
continuation_policy: continue_until_real_stop
task_completion_policy: merge_then_physical_qualification
parent_task: OTC-20260905-control-center-native-login-start
owned_paths:
  - .github/workflows/track-a-native-login-be4f48-physical.yml
  - .github/scripts/track_a_native_login_be4f48_physical.py
  - tools/tibia_runtime_bridge/container_native_login_client.py
  - tests/tools/tibia_runtime_bridge/test_native_login_physical_executor_contract.py
  - docs/agents/tasks/active/OTC-20260906-native-login-physical-executor.md
modules_touched:
  - Track A canonical runtime
  - Track A native auth bridge
  - Track A current causal IN_GAME qualification
reuses:
  - .github/scripts/tibia-official-client-re-canonical-live-lease
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
  - tools/tibia_runtime_bridge/profiles/tibia-15.32.be4f48.json
  - tools/tibia_runtime_bridge/experimental_auth.cpp
  - tools/tibia_runtime_bridge/experimental_character_control_current.cpp
  - tools/tibia_runtime_bridge/secret_vault.py
  - .github/scripts/track_a_game_window_state_qualification.py
depends_on:
  - OTC-20260906-be4f48-live-state-binding
  - OTC-20260906-native-login-vault-auth
blocks:
  - OTC-20260905-control-center-native-login-start
---

# OTC-20260906 — native-login physical executor

## Objective

Execute the smallest trusted-main canonical path that replaces the single exact-current `15.32.be4f48` official client with an instrumented exact-current instance, consumes the machine-local encrypted credential vault at most once through a sealed memfd, confirms a character only when the native character model proves exactly one entry, and establishes causal `gameWindowState == "INGAME"` before leaving the authenticated client running.

## Authority freeze

The branch and PR are repository-only. No self-hosted physical job may run PR-head code. Physical PRECHECK/EXECUTE is available only after merge through an owner comment and must check out exact trusted `main` and prove it still equals remote `main`.

Before any mutation, the live workflow must freshly acquire the canonical lease, perform any required generation rebind, prove Gate B and revalidate the same invariants inside the whole-lifetime `guard-run` critical section. A PID handoff or replacement is reconciled only through the existing `stale-registration-recovery` contract and a newer lease generation.

The task record deliberately remains fail-closed before physical execution: authoritative canonical registration is already `PRESENT`, but live lease generations are `UNKNOWN`, Gate A/B are not yet proven, target uniqueness is `UNKNOWN`, and `mutation_authorized` remains `false`. The trusted-main physical workflow establishes those transient facts at execution time; this branch does not pre-claim them.

## Secret boundary

Credential plaintext is forbidden from GitHub Secrets, workflow env, argv, stdin, task/evidence text and logs. The executor may consume only the existing machine-local encrypted vault. The vault remains host-only: it is decrypted once on the trusted runner into a fully sealed anonymous memfd, and only that inherited descriptor crosses into the Kasm namespaces through `nsenter`; the namespace-side process drops to the numeric `kasm-user` UID/GID before handing the descriptor to the exact auth helper through SCM_RIGHTS. No private key, CMS vault, or plaintext credential is copied into Kasm. No second credential attempt is permitted.

## Physical success

Success requires all of:

1. trusted-main current fence and unique canonical target;
2. exact-PID controlled replacement with be4f48 bridge/auth/character helpers;
3. canonical recovery and Gate B for the replacement PID;
4. one successful native auth ingress with no retry;
5. native character state proves exactly one character and `CONFIRM_UNIQUE` dispatch succeeds;
6. exact-current read-only causal state observation after confirmation proves `gameWindowState == "INGAME"` on the admitted exact process;
7. authenticated canonical client remains running and no broad process cleanup is performed.

## TDD and validation evidence

RED head `3cde9a55ead37a8035ef808b2de94d7711b6f040`:
- workflow run `34043036312`, job `101513088002`;
- 5 focused tests ran with exactly 2 errors because the worker and container-side FD client did not yet exist;
- the Synology physical job was skipped.

Implementation checkpoint `dc16166c2d591256ebbc9141293e0153eaa34eae`:
- focused physical-executor contract: 5/5 PASS;
- Python compilation reached successfully;
- workflow run `34044317122`, job `101516525874` then failed only in Track A runtime governance because the task frontmatter used non-schema `canonical_registration: REQUIRED_CURRENT`;
- self-hosted PR boundary run `34044317179` was SUCCESS;
- no physical job or secret access ran from PR head.

The current checkpoint corrects only that admission metadata mismatch: `canonical_registration: PRESENT`, canonical namespace `canonical-live-runtime`, unknown transient generations, pending gates, unknown uniqueness and `mutation_authorized: false` until trusted-main physical execution proves the live values.
