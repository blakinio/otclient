# TIBIA RE Control Center Package C alias

```yaml
alias_prompt_contract_version: 1.0.0
canonical_prompt_contract_version: 1.0.0
alias: OTCLIENT-TIBIA-RE-CONTROL-CENTER-PACKAGE-C
repository: blakinio/otclient
track_id: official-client-re
lane: P3-SURVEYOR-INTEGRATION
risk: medium
runtime_access: none
official_client_access: false
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
network_listener_allowed: false
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
```

Owner invocation:

```text
Uruchom OTCLIENT-TIBIA-RE-CONTROL-CENTER-PACKAGE-C autonomicznie.
```

or:

```text
Kontynuuj OTCLIENT-TIBIA-RE-CONTROL-CENTER-PACKAGE-C autonomicznie.
```

Resolve from live repository state. Load the governing `AGENTS.md` hierarchy and execute:

```text
docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_PACKAGE_C_PARALLEL_AGENT.md
```

This alias authorizes only the Package C read-only Surveyor integration defined by the canonical prompt: pin the accepted current Surveyor producer/schema/interface, validate and consume its outputs, and normalize them into the existing Control Center read models.

It grants no physical Surveyor collection, Official Tibia runtime access, Docker/KasmVNC observation, process access, credentials, login, gameplay input, mutation or Track A authority. Missing/incompatible Surveyor producer state fails closed rather than being guessed or implemented inside Package C.

Package C may run concurrently with Package B and Package D preparation only after fresh active-task/open-PR/path-overlap checks and separate task/branch/worktree claims. Never share branches/worktrees or race shared paths.
