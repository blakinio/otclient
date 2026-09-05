---
task_id: OTC-20260819-ollama-local-research-agent-poc-runtime
status: blocked
agent: ChatGPT
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: implementation
phase: closeout
branch: docs/OTC-20260819-ollama-local-research-agent-poc-runtime
base_branch: main
base_sha: f188d6a2a392e3b4607c428c9f3a8f46466b5cce
last_revalidated_main_sha: f188d6a2a392e3b4607c428c9f3a8f46466b5cce
risk: high
owned_paths:
  - docs/agents/tasks/active/OTC-20260819-ollama-local-research-agent-poc-runtime.md
  - docs/agents/evidence/OTC-20260819-ollama-local-research-agent-poc-runtime/**
  - tools/tibia_re_ollama_poc/**
  - tests/tools/tibia_re_ollama_poc/**
modules_touched:
  - tibia-re-ollama-poc-internal-harness
depends_on:
  - PR #628 Control Center Package A control-core reaching trusted main
  - separately authorized Control Center Package D official Track A mutation adapter reaching trusted main
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.1.0
execution_mode: hybrid
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
runtime_access: none
persistent_session_role: none
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
gui_input_authorized: false
process_control_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
local_ollama_authorized: true
owner_funded_ai_api_authorized: false
direct_codex_spark_authorized: false
implementation_status: PARTIAL
poc_technical_result: FAIL
research_value_verdict: INCONCLUSIVE
local_model_concurrency_policy: MAX_ONE_LOADED_MODEL
current_blocker: CONTROL_CENTER_EXECUTABLE_ACTION_PATH_NOT_READY
secondary_blocker: NONE
owner_reported_session_state: IN_GAME_CHARACTER_AND_WORLD
owner_session_report_verified_at_runtime: false
last_progress_at: 2026-08-20T15:04:22+02:00
next_action: after the canonical Control Center real-action dependency chain is trusted-main executable, freshly re-admit and verify the owner-established in-game Track A session, then rerun POC-001..020
---

# TIBIA-RE Ollama local research-agent PoC runtime closeout

## Live trusted-base revalidation

Trusted main is `f188d6a2a392e3b4607c428c9f3a8f46466b5cce`.

Control Center hardening PR #613 and lifecycle #627 are merged. Package A is still separately owned by Draft PR #628 and is not on trusted main. Its scope remains `runtime_access:none` and excludes the Official Tibia mutation adapter. Canonical `TIBIA_RE_CONTROL_CENTER_MVP.md` defines real official-client mutation as Package D under a separate fresh Track A task/admission.

Merged PR #629 proved that the historical `BRIDGE_3_OF_3 => IN_GAME` interpretation was a false positive: the exact client was visibly on the login form while all three structural bridge objects remained present. PR #631 then merged the owner-gated semantic-downgrade workflow. Read-only control-plane revalidation after that lifecycle shows canonical registration `state=UNKNOWN`, `state_evidence=BRIDGE_3_OF_3_SEMANTICS_UNPROVEN`, and the canonical lease released at generation 19.

At 2026-08-20 15:03 CEST the owner explicitly reported that they had manually logged into the character and entered the world. The agent did not use credentials, perform login, select a character, or send input. This removes the need for the PoC to create/authenticate the session itself. The report is retained as owner-provided current state, not as accepted structural POC evidence.

Because the first hard readiness prerequisite still fails before live Track A access, this continuation remains `runtime_access:none` and does not touch the official-client process merely to re-prove a later prerequisite.

## Hard readiness gate

```yaml
readiness:
  trusted_base_sha: f188d6a2a392e3b4607c428c9f3a8f46466b5cce
  normalized_observation_executable: true
  bounded_action_policy_executable: false
  dispatch_preflight_executable: false
  evidence_store_executable: false
  runtime_identity_fencing_executable: true
  stop_cancellation_semantics_executable: true
  chosen_experiment_supported: false
```

`CONTROL_CENTER_EXECUTABLE_ACTION_PATH_NOT_READY` is the only current terminal blocker for this invocation. Even after Package A, the real Official Tibia experiment needs the separately governed Package D adapter.

The previous `TRACK_A_REQUIRED_SESSION_STATE_UNAVAILABLE` blocker is cleared at the owner-action level: the owner has manually established the desired character/world session. Fresh Track A admission and machine-verifiable current-session proof are still required immediately before a future real experiment, but no agent login or credential authority is required to reach that point.

## Harness state

The branch retains the bounded runtime-independent Ollama harness: loopback-only endpoint, no cloud/pull fallback, exact model digest verification, strict proposal/conclusion JSON validation, frozen evidence/candidate hashes, exactly three proposal trials, secret rejection, deterministic `NO_ACTION` baseline, external-authority-only dispatch preflight, no shell/SSH/process/GUI/gameplay/credential capability for the model, and single-model residency/unload lifecycle.

Focused validation on the previously reconciled exact code is `25/25 PASS`, compileall PASS and `git diff --check` PASS. Historical model/runtime-independent evidence remains under this task evidence root. Such evidence cannot satisfy live POC-006..015.

## Acceptance inventory

```text
POC-001 FAIL     trusted-main executable real-action prerequisites incomplete
POC-002 PASS     Molehill-PC execution host proven
POC-003 PASS     local Ollama endpoint/version/model/digest proven
POC-004 PARTIAL  transport/read-only pieces exist; complete PoC path is not admitted
POC-005 PARTIAL  owner reports current character/world session; fresh admitted machine proof deferred until the first hard readiness gate passes
POC-006..015 NOT_RUN because the real-action readiness gate fails before legal experiment dispatch
POC-016 PARTIAL  blocker/model evidence durable; complete experiment envelope absent
POC-017 PASS     no secret/private chain-of-thought persisted
POC-018 PASS     this PoC continuation did not mutate the official client
POC-019 PASS     no shell/SSH/credential/login/unrestricted-gameplay capability exposed to the model
POC-020 PASS     technical FAIL and case-bounded INCONCLUSIVE verdict explicit
```

## Terminal invocation result

```text
STATUS=BLOCKED
IMPLEMENTATION_STATUS=PARTIAL
POC_TECHNICAL_RESULT=FAIL
RESEARCH_VALUE_VERDICT=INCONCLUSIVE
BLOCKER=CONTROL_CENTER_EXECUTABLE_ACTION_PATH_NOT_READY
SECONDARY_BLOCKER=NONE
```

The remaining blocker cannot legally be removed inside this task: the PoC prompt forbids implementing missing broad Control Center packages merely to unblock Ollama, Package A is separately owned, and Package D requires a separate Track A implementation/admission boundary. The owner-established live session is ready to be freshly revalidated once that execution path exists.
