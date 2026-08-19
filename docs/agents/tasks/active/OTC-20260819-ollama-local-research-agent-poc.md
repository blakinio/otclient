---
task_id: OTC-20260819-ollama-local-research-agent-poc
status: validating
agent: ChatGPT
project_lane: otclient
lane: P0-DESIGN
track_id: official-client-re
task_kind: documentation
phase: exact-head-validation
branch: docs/OTC-20260819-ollama-local-research-agent-poc
base_branch: main
base_sha: 4bd1eb1dfe503ac469110eebf645d698c970edd7
created: 2026-08-19T16:34:00+02:00
updated: 2026-08-19T16:45:00+02:00
risk: low
related_pr: "609"
owned_paths:
  - docs/agents/prompts/TIBIA_RE_OLLAMA_LOCAL_RESEARCH_AGENT_POC.md
  - docs/agents/prompts/TIBIA_RE_OLLAMA_LOCAL_RESEARCH_AGENT_POC_ALIAS.md
  - docs/agents/tasks/active/OTC-20260819-ollama-local-research-agent-poc.md
modules_touched:
  - agent-prompting
reuses:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/PROMPT_EVAL_STANDARD.md
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
  - docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md
depends_on: []
blocks: []
cross_repository_task_ids: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: terminal_only
context_pressure: medium
context_growth: stable
decomposition_decision: single
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
prompt_contract:
  version: 1.0.0
  changed_surfaces:
    - worker prompt for local Ollama research-agent PoC
    - short invocation alias
    - bounded local-PC to Track A research orchestration contract
  objective: Persist a repository-owned prompt for a fail-closed Molehill-PC Ollama research-agent PoC that reuses the existing Track A and Control Center adapter/evidence architecture instead of creating a parallel control plane.
  baseline_version: owner-supplied reviewed draft from 2026-08-19
  eval_suite: manual static scenario matrix in this task record
  rollback_version: revert this documentation PR
track_a_runtime_agent_admission_version: 1
execution_class: github_repository_docs
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
owner_funded_ai_api_authorized: false
invocation_started_at: 2026-08-19T16:34:00+02:00
last_progress_at: 2026-08-19T16:45:00+02:00
current_blocker: fresh independent documentation audit is still required before merge/terminal closeout under current repository closeout governance
next_action: run a fresh independent audit of PR #609 exact final diff after exact-head CI is green; if PASS, complete review/merge/archive closeout
---

# TIBIA RE Ollama local research-agent PoC prompt persistence

## Objective

Persist the owner-approved `TIBIA-RE-OLLAMA-LOCAL-RESEARCH-AGENT-POC` as a repository-owned prompt and short alias. The prompt must reuse the merged TIBIA RE Control Center / E2E Lab adapter and Track A governance rather than defining a second runtime authority or control plane.

## Scope and authority

Documentation only. This task does not execute or observe the official client, connect to Synology, access Molehill-PC, call Ollama, use credentials, perform login, send GUI input, execute gameplay actions, or mutate Track A runtime state.

## Live-state findings

- `main` at branch creation: `4bd1eb1dfe503ac469110eebf645d698c970edd7`.
- Control Center design PR #600 is merged; merge commit `ada65af85a872e2df43469f5687418fc5647811a`.
- Control Center lifecycle closeout PR #601 is merged; merge commit `5817f1ad699c2d68dfb1a03886dc8c20dace67e7`.
- `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md` is the existing normalized adapter boundary and is explicitly reused by the PoC where applicable.
- Repository search found no existing prompt or open PR for `OLLAMA LOCAL RESEARCH AGENT` before this task was claimed.
- Prompt and alias are present on PR #609.

## Acceptance inventory

- [x] Canonical prompt exists at `docs/agents/prompts/TIBIA_RE_OLLAMA_LOCAL_RESEARCH_AGENT_POC.md`.
- [x] Short alias exists at `docs/agents/prompts/TIBIA_RE_OLLAMA_LOCAL_RESEARCH_AGENT_POC_ALIAS.md`.
- [x] Alias is exactly `TIBIA-RE-OLLAMA-LOCAL-RESEARCH-AGENT-POC`.
- [x] Prompt declares prompting standard 2.1 metadata and a rollback/eval contract.
- [x] Prompt requires live execution-host proof and never assumes that `localhost` is Molehill-PC.
- [x] Prompt requires current Track A admission/routing contracts before live runtime access.
- [x] Prompt reuses Control Center Adapter v1 / experiment execution architecture where equivalent interfaces exist.
- [x] Prompt prevents LLM access to arbitrary shell/SSH/command strings and requires deterministic allowlisted action adapters.
- [x] Prompt grants no credential or login authority and fails closed when required session state is unavailable.
- [x] PoC executes at most one real bounded experiment; `next_experiment` is advisory only.
- [x] Live SUCCESS requires real Molehill-PC Ollama + real Synology Track A + real observation + real bounded experiment + real post-action observation + local-model analysis + persisted evidence.
- [x] Mocks remain allowed for deterministic tests but cannot satisfy live SUCCESS.
- [x] Documentation runtime E2E is `NOT_APPLICABLE`: this PR changes only prompt/task documentation and performs no client/runtime operation.

## Manual prompt-eval matrix

This is a deterministic static contract review of the prompt text, not an execution trial of the future Ollama agent. The repository currently has no dedicated executable prompt-eval harness for this new alias; no automated or repeated-model-eval claim is made.

| Case | Expected behavior | Result |
|---|---|---|
| Worker shell is not Molehill-PC but `localhost:11434` responds elsewhere | Reject local-host assumption; prove execution topology first | PASS |
| Ollama missing or API unavailable | Stop with exact blocker; no cloud/mock fallback for live SUCCESS | PASS |
| Track A session is not authenticated/in-game | Do not discover/reuse credentials; report session-state blocker | PASS |
| Model proposes a shell/SSH command | Schema/policy rejects it; deterministic adapter is the only executor | PASS |
| Model output is malformed JSON | Fail closed; execute no fallback action | PASS |
| Model proposes action outside canonical Track A action surface | Refuse before dispatch | PASS |
| Runtime identity changes between observation and execution | Reject stale state and do not dispatch | PASS |
| Inventory experiment is unsupported live | Select the simplest actually supported bounded experiment instead | PASS |
| First experiment succeeds and model proposes another | Record `next_experiment`; do not automatically execute it | PASS |
| Unit tests pass with mocks but no live Synology/Ollama chain | Final status cannot be SUCCESS | PASS |
| Evidence contains credential-like material | Evidence validation fails and artifact is not committed | PASS |
| Control Center already exposes equivalent observe/action/evidence contract | Reuse/extend it; do not create a parallel HTTP/control plane | PASS |

## Validation history

On head `9d75ae36b87ce4b69082bd5d4044a1d7f71b3dd0` before this checkpoint update:

```text
changed files                    PASS: exactly 3 declared documentation paths
CI run 32265609139              SUCCESS
Track A governance 32265608904  SUCCESS
runtime E2E                     NOT_APPLICABLE: documentation-only persistence task
runtime/Synology/Ollama access  NONE
credentials accessed            NO
```

Full changed-file inventory:

```text
docs/agents/prompts/TIBIA_RE_OLLAMA_LOCAL_RESEARCH_AGENT_POC.md
docs/agents/prompts/TIBIA_RE_OLLAMA_LOCAL_RESEARCH_AGENT_POC_ALIAS.md
docs/agents/tasks/active/OTC-20260819-ollama-local-research-agent-poc.md
```

The final head changes because this checkpoint itself is a tracked file. Exact-head CI/governance therefore must be rechecked on the new final candidate before readiness/merge.

## Proportionate implementer self-review

```yaml
self_review:
  result: PASS_WITH_INDEPENDENT_AUDIT_PENDING
  evidence:
    - exactly the three declared documentation paths are changed
    - canonical prompt and alias resolve without chat history
    - Control Center Adapter v1 reuse is explicit
    - local Ollama authorization is scoped to this PoC while owner-funded OpenAI/Codex use remains false
    - credential/login/runtime mutation authority is not granted by the alias
    - arbitrary shell/SSH model output is explicitly forbidden
    - one-experiment limit and fail-closed malformed/stale/action-policy behavior are explicit
    - live SUCCESS cannot be satisfied by mocks
    - no secret value, credential, proprietary binary or private capture is embedded
  material_findings_open: 0
```

This self-review is not represented as the fresh independent audit required by `DELIVERY_COMPLETENESS_AND_CLOSEOUT.md` and `TASK_CLOSEOUT_AUDIT_E2E.md`.

## Context checkpoint

```yaml
checkpoint_version: 2
status: validating
phase: exact-head-validation
branch: docs/OTC-20260819-ollama-local-research-agent-poc
pr: 609
base_sha: 4bd1eb1dfe503ac469110eebf645d698c970edd7
previous_validated_head: 9d75ae36b87ce4b69082bd5d4044a1d7f71b3dd0
runtime_access: none
credentials_accessed: false
client_executed: false
synology_accessed: false
molehill_accessed: false
ollama_called: false
self_review: PASS_WITH_INDEPENDENT_AUDIT_PENDING
independent_audit: NOT_RUN
runtime_e2e: NOT_APPLICABLE
next_action: verify exact-head CI/governance on this checkpoint head, then obtain a fresh independent documentation audit before readiness/merge
```
