# TIBIA-RE Ollama local research-agent PoC alias

```yaml
alias_prompt_contract_version: 1.0.0
canonical_prompt_contract_version: 1.0.0
alias: TIBIA-RE-OLLAMA-LOCAL-RESEARCH-AGENT-POC
track_id: official-client-re
lane: RUNTIME
risk: high
runtime_access: current_task_must_classify_before_live_work
local_ollama_authorized: true
owner_funded_ai_api_authorized: false
direct_codex_spark_authorized: false
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
programme_boundary: exact_local_ollama_research_agent_poc_and_required_closeout_only
user_communication: terminal_only
```

Owner invocation:

```text
Uruchom TIBIA-RE-OLLAMA-LOCAL-RESEARCH-AGENT-POC autonomicznie.
```

or:

```text
Kontynuuj TIBIA-RE-OLLAMA-LOCAL-RESEARCH-AGENT-POC autonomicznie.
```

Resolve the command through live repository state and load the current governing `AGENTS.md` hierarchy, current Track A runtime/admission/KasmVNC/hybrid-routing/experiment contracts, current Control Center / E2E Lab architecture and:

```text
docs/agents/prompts/TIBIA_RE_OLLAMA_LOCAL_RESEARCH_AGENT_POC.md
```

Do not reconstruct the task from chat history.

This alias authorizes use of the user's **local Ollama installation on the verified Molehill-PC execution path** for this PoC. It does not authorize OpenAI API, Codex, hosted code review, another paid/limited owner-funded AI service, or any AI-service credential.

This alias grants no credential, login, GUI-input, process-control, gameplay or Track A mutation authority by itself. Before any live Track A operation, classify and persist the current `runtime_access` admission required by repository governance. Any required admission/identity/action gate that is not currently proven fails closed.

The worker must reuse the existing `TIBIA RE Control Center / E2E Lab` and `TIBIA_RE_CONTROL_CENTER_ADAPTER_V1` interfaces where equivalent surfaces exist. Do not create a second runtime authority, second Scenario Engine or parallel action/evidence contract merely for Ollama.

The PoC performs at most one real bounded experiment. `next_experiment` is advisory only and must not execute recursively during this task.

Normal success requires the real live chain:

```text
Molehill-PC local Ollama
-> local orchestrator
-> Synology Track A
-> admitted real observation
-> schema-valid local-model analysis
-> deterministic bounded real experiment
-> real post-action observation
-> local-model comparison
-> persisted reproducible evidence
```

Mocks may support deterministic tests but cannot satisfy live `SUCCESS`.

If Molehill-PC execution, Ollama, required Track A session/admission, deterministic action capability or any other required live link cannot be proven, return `PARTIAL` or `FAIL` with the exact blocker rather than widening authority or fabricating completion.
