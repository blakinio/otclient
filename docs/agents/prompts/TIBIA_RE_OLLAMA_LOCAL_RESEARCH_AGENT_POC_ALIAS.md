# TIBIA-RE Ollama local research-agent PoC alias

```yaml
alias_prompt_contract_version: 1.1.0
canonical_prompt_contract_version: 1.1.0
alias: TIBIA-RE-OLLAMA-LOCAL-RESEARCH-AGENT-POC
track_id: official-client-re
lane: RUNTIME
risk: high
runtime_access: current_task_must_classify_before_live_work
local_ollama_authorized: true
owner_funded_ai_api_authorized: false
direct_codex_spark_authorized: false
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
programme_boundary: exact_local_ollama_research_agent_poc_and_required_closeout_only
user_communication: low_noise
```

Owner invocation:

```text
Uruchom TIBIA-RE-OLLAMA-LOCAL-RESEARCH-AGENT-POC autonomicznie.
```

or:

```text
Kontynuuj TIBIA-RE-OLLAMA-LOCAL-RESEARCH-AGENT-POC autonomicznie.
```

Resolve the command from live repository state and load the current governing `AGENTS.md` hierarchy, current trusted-base Track A/runtime/admission/KasmVNC/hybrid-routing/experiment contracts, current trusted-base Control Center contracts/implementation state, and:

```text
docs/agents/prompts/TIBIA_RE_OLLAMA_LOCAL_RESEARCH_AGENT_POC.md
```

Do not reconstruct the task from chat history. Open Drafts and historical runtime facts are discovery input only, not authority or executable capability.

This alias authorizes use of the user's **local Ollama installation on the verified Molehill-PC execution path** for this PoC. It does not authorize OpenAI API, Codex, hosted code review, another owner-funded AI service, or AI-service credentials.

This alias grants no credential, login, GUI-input, process-control, gameplay or Track A mutation authority by itself. Before any live Track A operation, classify and persist the current `runtime_access` admission required by trusted-base governance. Any required admission/identity/action gate that is not proven fails closed.

Before runtime-integrating implementation, enforce the canonical prompt's hard readiness gate. Design-only Control Center contracts do not satisfy executable observation/action/evidence prerequisites. Do not build a parallel Control Center merely to make this PoC pass.

For the first PoC, the local model does not construct action parameters. The deterministic harness fully materializes a micro-allowlist of at most three canonical candidate actions plus `NO_ACTION`; Ollama may select only `candidate_id`. Three proposal-only trials on the same frozen evidence bundle must agree 3/3 before the single permitted real action can be considered for dispatch.

The PoC performs at most one real bounded state-changing experiment. `next_experiment` is advisory only and never executes recursively in this task.

Normal technical success requires the real chain:

```text
verified Molehill-PC local Ollama
-> bounded local orchestrator
-> canonical approved Synology transport
-> admitted canonical Track A
-> real structured observation
-> frozen evidence + candidate hashes
-> 3/3 schema-valid proposal consensus
-> fresh policy/authority/precondition validation
-> one bounded canonical real action
-> real post-action observation
-> structured local-model conclusion
-> deterministic no-LLM baseline/value comparison
-> secret-safe reproducible evidence
```

Mocks may support deterministic tests but cannot satisfy live `SUCCESS`.

The final result must separate:

```text
POC_TECHNICAL_RESULT=PASS|FAIL
RESEARCH_VALUE_VERDICT=SUPPORTED_FOR_THIS_CASE|NOT_SUPPORTED_FOR_THIS_CASE|INCONCLUSIVE
```

One successful PoC must not be generalized into a claim that Ollama accelerates TIBIA-RE overall.

If Molehill-PC execution, Ollama, trusted-base executable prerequisites, required Track A session/admission, deterministic action capability or any other required live link cannot be proven, return `PARTIAL` or `FAIL` with the exact blocker rather than widening authority or fabricating completion.