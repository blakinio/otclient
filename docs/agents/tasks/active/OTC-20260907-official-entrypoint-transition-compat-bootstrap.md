---
task_id: OTC-20260907-official-entrypoint-transition-compat-bootstrap
status: ready
agent: ChatGPT
session_id: official-entrypoint-transition-compat-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: canonical_runtime_bootstrap
phase: transition_compatibility_and_live_admission
branch: fix/OTC-20260907-official-entrypoint-transition-compat
base_branch: main
base_main: ef6301df117700ca4170d40c922bc94175a146d1
execution_mode: github_actions_owner_comment
execution_class: synology_physical_runtime
persistent_session_role: canonical_runtime_owner
physical_e2e_required: true
runtime_access: canonical_bootstrap
runtime_owner_task: OTC-20260907-official-entrypoint-transition-compat-bootstrap
runtime_namespace: canonical-live-runtime
canonical_registration: ABSENT
canonical_lease_generation: UNKNOWN
registration_lease_generation: NOT_APPLICABLE
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: PASS
target_uniqueness: UNKNOWN
mutation_authorized: true
bootstrap_mode: create_new
bootstrap_attempt_limit: 1
credentials_allowed: false
login_allowed: false
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: true
network_payload_capture_allowed: false
process_memory_access_allowed: false
physical_action_budget: 1
physical_action_count: 0
precheck_attempt_limit: 1
execute_attempt_limit: 1
implementation_authorized: true
live_runtime_authorization_source: OWNER_CHAT_20260907_CORRECTIVE_TRACK_A_PR_AND_CONTINUATION
parent_task: OTC-20260907-official-linux-entrypoint-bootstrap
depends_on:
  - OTC-20260907-official-linux-entrypoint-bootstrap
canonical_scope_contract: TRACK_A_CANONICAL_KASM_RUNTIME_SCOPE_V1
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-transition-scoped.py
  - .github/workflows/track-a-canonical-kasm-bootstrap-retry-v2.yml
  - tests/tools/tibia_runtime_bridge/test_canonical_kasm_bootstrap_retry_v2_contract.py
  - docs/agents/tasks/active/OTC-20260907-official-linux-entrypoint-bootstrap.md
  - docs/agents/tasks/active/OTC-20260907-official-entrypoint-transition-compat-bootstrap.md
modules_touched:
  - track_a_canonical_live_transition_scoped
  - track_a_kasm_official_entrypoint_bootstrap
reuses:
  - tibia-official-client-re-canonical-live-transition.py
  - tibia-official-client-re-kasm-bootstrap-worker-compatible.py
  - track-a-canonical-kasm-bootstrap-retry-v2.yml
blocks:
  - exact_current_official_client_restoration
  - official_login_world_entry_wire_capture
---

# Official-entrypoint transition compatibility bootstrap

Trusted base is `ef6301df117700ca4170d40c922bc94175a146d1` (merged PR #981). The previous exact-current official-entrypoint task proved the new Linux entrypoint hypothesis through PRECHECK but its one EXECUTE attempt failed before process creation because the canonical transition reader still accepts only the historical direct-client bootstrap record shape.

Evidence carried forward from the immediately preceding task:

- PRECHECK run `34131050885`, job `101770990388`: PASS on trusted main, authoritative registration `ABSENT`, zero official game-client candidates/windows, exact current package `15.32.be4f48`, and one bounded top-level official Linux `Tibia` entrypoint.
- EXECUTE run `34131140019`, job `101771284041`: failed with `TRACK_A_CANONICAL_TRANSITION_ERROR=kasm_bootstrap_record_invalid` before process creation or credential access.
- Post-failure Surveyor run `34131763597`, job `101773293609`: authoritative registration still `ABSENT`, `TARGET_NAMESPACE_CLIENTS=0`; no exact client was left running.

The owner explicitly authorized one additional narrow corrective Track A PR and autonomous continuation on 2026-09-07. This task spends that authority only on making the existing scoped transition accept the exact launcher-bound record already emitted by PR #981, plus one fresh PRECHECK/EXECUTE admission after the correction reaches trusted `main`.

## Implementation boundary

Do not change Track B #284 and do not create a new recovery/bootstrap framework. Extend only `.github/scripts/tibia-official-client-re-canonical-live-transition-scoped.py` so the existing scoped Kasm transition:

1. preserves the historical bootstrap record schema and behavior unchanged;
2. additionally accepts exactly the PR #981 official-entrypoint PRECHECK record shape, including launcher path/dir/size/SHA/selection, with the fingerprint recomputed over the complete record;
3. additionally accepts exactly the PR #981 launch record shape, including `client_dir`, launcher identity and launch method `docker_exec_detached_official_linux_entrypoint`;
4. requires all launcher identity fields in the launch record to equal the preflight record and requires `client_dir` to be the exact parent of the exact package `client` path;
5. rejects partial/mixed/unknown launcher record shapes, unknown keys, wrong launch methods, invalid hashes, invalid path binding or preflight/launch launcher drift;
6. preserves all existing exact-client, container, display, registration, lease, probe, rollback and fail-closed checks.

Deterministic validation belongs on GitHub-hosted CI. No physical runtime operation is authorized from the PR head.

## Fresh PRECHECK / EXECUTE

Only after this corrective PR is reviewed, exact-head green and merged to current trusted `main`:

- one owner-triggered PRECHECK may re-prove registration absence, zero-client state, exact current package and one exact official Linux entrypoint without process creation;
- only after PRECHECK PASS on the same trusted main, one owner-triggered EXECUTE may perform one `kasm-bootstrap` transaction using the existing compatible worker and scoped transition;
- this task does not authorize credential access, login, character selection, GUI input or gameplay.

A successful EXECUTE must leave exactly one exact-current registered client and no conflicting launcher residue. Any failure must rollback only task-created exact identities and re-prove the original zero-client state.

## Implementation checkpoint

PR #982 implements only the scoped transition compatibility required by the #981 official-entrypoint worker. The historical record reader remains the fallback for legacy records; launcher-bound PRECHECK and LAUNCH records use exact key sets; the complete launcher-bound preflight fingerprint is recomputed; the launch method, `client_dir`, and every launcher identity field are bound back to PRECHECK; partial, mixed, drifted, unknown-key and wrong-method records remain fail-closed. Track B #284 is untouched.

Two PR-head validation failures were investigated and corrected rather than retried blindly:

- the legacy same-boot contract initially failed because a static registration-file safety test saw a new `read_text()` before the scoped registration reader's `lstat()`; the bootstrap-record reader was changed to `open()` plus `json.load()` so the historical registration read-order invariant remains intact;
- general CI then failed only because the rewritten workflow lacked a final newline; the file termination was corrected without changing runtime semantics.

The resulting reviewed implementation head `36374fa2fe7cce7a5c766943ddd6f8fe56fdd358` completed all exact-head validation successfully:

- Track A canonical Kasm official Linux entrypoint bootstrap run `34136148307`: success;
- Track A same-boot zero-client recovery v2 run `34136148340`: success;
- Track A agent runtime governance run `34136148297`: success;
- Track A self-hosted PR boundary run `34136148319`: success;
- CI run `34136148570`: success, including `CI / Required` job `101787885991`, syntax/workflow validation, Lua syntax, and informational static analysis.

At the Ready transition PR #982 was mergeable, had no submitted reviews, no unresolved review threads, and no requested changes. The task-record update containing this checkpoint is documentation-only and must itself receive exact-head validation before merge.

## Next action

After the documentation-only task-record head is exact-head green, re-check PR #982 changed paths and review state, squash-merge #982 to trusted `main`, refresh current `main`, then issue exactly one fresh `/track-a-official-entrypoint-transition-compat-bootstrap PRECHECK` on PR #975. Issue EXECUTE only if that PRECHECK passes on the same trusted main.