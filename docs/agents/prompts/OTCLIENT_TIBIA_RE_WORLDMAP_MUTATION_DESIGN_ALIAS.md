# OTCLIENT-TIBIA-RE worldmap mutation-design alias

```yaml
alias_prompt_contract_version: 1.0.0
alias: OTCLIENT-TIBIA-RE-WORLDMAP-MUTATION-DESIGN
track_id: official-client-re
lane: STATIC-MUTATION-DESIGN
execution_class: github_hosted_design
runtime_access: none_by_default
client_byte_mutation_authorized: false
owner_funded_ai_api_authorized: false
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
```

Owner invocation:

```text
Uruchom OTCLIENT-TIBIA-RE-WORLDMAP-MUTATION-DESIGN autonomicznie.
```

Resolve through live repository state and load `AGENTS.md`, current prompting/governance contracts, `docs/agents/prompts/OTCLIENT_TIBIA_RE_WORLDMAP_MUTATION_DESIGN.md`, and `docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md`. Locate merged #367/#437/#446, verify current `main`, search for an existing correct mutation-design task/PR, and reuse it rather than duplicate.

Objective: convert the accepted static dependency graph into a falsifiable, reversible design for increasing worldmap extent beyond 18×14. This alias does **not** authorize official-client byte mutation or physical runtime mutation. Do not redo completed broad RE; focus on candidate encodings, Viewport/RenderProvider/Camera/Picker/Storage/parser constraints, conservative parameter envelope, rollback, negative controls and physical validation design.

No owner-funded Codex/OpenAI API/paid AI quota may be consumed without exact current owner authorization.
