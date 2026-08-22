# TIBIA RE Control Center Package B alias

```yaml
alias_prompt_contract_version: 1.0.0
canonical_prompt_contract_version: 1.0.0
alias: OTCLIENT-TIBIA-RE-CONTROL-CENTER-PACKAGE-B
repository: blakinio/otclient
track_id: official-client-re
lane: P2-CONTROL-API
risk: medium
runtime_access: none
official_client_access: false
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
control_api_listener: loopback_only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
```

Owner invocation:

```text
Uruchom OTCLIENT-TIBIA-RE-CONTROL-CENTER-PACKAGE-B autonomicznie.
```

or:

```text
Kontynuuj OTCLIENT-TIBIA-RE-CONTROL-CENTER-PACKAGE-B autonomicznie.
```

Resolve from live repository state. Load the governing `AGENTS.md` hierarchy and execute:

```text
docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_PACKAGE_B_PARALLEL_AGENT.md
```

This alias authorizes only the Package B slice defined by the canonical prompt: secured loopback Control API v1, persistent request/safety state, browser UI, CLI and fake-adapter execution through the existing Package A semantic path.

It grants no Official Tibia runtime access, credentials, login, gameplay, KasmVNC interaction, process observation/mutation or Track A mutation authority. Real Official Tibia mutation remains Package D under a separate future admitted task.

Package B may run concurrently with the Package C and Package D-preparation workers only after fresh active-task/open-PR/path-overlap checks and separate task/branch/worktree claims. Never share branches/worktrees or race shared paths.
