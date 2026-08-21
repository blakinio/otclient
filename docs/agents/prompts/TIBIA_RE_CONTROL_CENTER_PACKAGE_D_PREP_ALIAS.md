# TIBIA RE Control Center Package D preparation alias

```yaml
alias_prompt_contract_version: 1.0.0
canonical_prompt_contract_version: 1.0.0
alias: OTCLIENT-TIBIA-RE-CONTROL-CENTER-PACKAGE-D-PREP
repository: blakinio/otclient
track_id: official-client-re
lane: P4-OFFICIAL-ADAPTER-PREP
risk: medium
runtime_access: none
official_client_access: false
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
network_listener_allowed: false
real_package_d_runtime_authorized: false
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
```

Owner invocation:

```text
Uruchom OTCLIENT-TIBIA-RE-CONTROL-CENTER-PACKAGE-D-PREP autonomicznie.
```

or:

```text
Kontynuuj OTCLIENT-TIBIA-RE-CONTROL-CENTER-PACKAGE-D-PREP autonomicznie.
```

Resolve from live repository state. Load the governing `AGENTS.md` hierarchy and execute:

```text
docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_PACKAGE_D_PREP_PARALLEL_AGENT.md
```

This alias authorizes only the runtime-independent preparation phase for future Package D: current-source Track A reuse mapping, action/evidence readiness matrix, finite-effect/confirmation design, future admission checklist, and optional hard-disabled typed adapter skeleton with deterministic no-dispatch tests.

It explicitly does **not** authorize real Package D execution. No Official Tibia runtime/container/KasmVNC/process/window/memory access, credentials, login, gameplay input, canonical lease/registration/Gate transition or physical mutation may occur under this alias, even if a logged-in client is currently available.

Package D preparation may run concurrently with Package B and Package C only after fresh active-task/open-PR/path-overlap checks and separate task/branch/worktree claims. Never share branches/worktrees or race shared paths. Real Package D must be started later under a separate fresh runtime-sensitive task and then-current Track A admission.
