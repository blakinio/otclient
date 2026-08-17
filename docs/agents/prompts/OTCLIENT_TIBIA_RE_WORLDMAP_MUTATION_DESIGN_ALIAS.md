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

## Resolution

Owner invocation:

```text
Uruchom OTCLIENT-TIBIA-RE-WORLDMAP-MUTATION-DESIGN autonomicznie.
```

Resolve this alias through current live repository state and load:

```text
AGENTS.md
docs/agents/PROMPTING_STANDARD.md
docs/agents/PROMPTING_HANDOVER.md
docs/agents/prompts/OTCLIENT_TIBIA_RE_WORLDMAP_MUTATION_DESIGN.md
docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md
```

Then locate merged #367 plus canonical producers #437 and #446, verify current `main`, search for an already active mutation-design task/PR, and reuse it if correct. Do not create a duplicate task merely because this alias is invoked in a fresh chat.

The phase objective is to convert the accepted static dependency graph into a complete, falsifiable, reversible mutation design for increasing worldmap extent beyond 18×14. The alias does **not** authorize modification of official Tibia client bytes or physical runtime mutation. Any transition from design to actual patch execution requires separate explicit authority under current repository governance.

Do not redo the completed general static RE from #367. Focus on exact candidate encodings, coupled Viewport/RenderProvider/Camera/Picker/storage/parser constraints, conservative parameter envelope, rollback, negative controls and physical validation design.

No owner-funded Codex/OpenAI API/paid AI quota may be consumed without exact current owner authorization.
