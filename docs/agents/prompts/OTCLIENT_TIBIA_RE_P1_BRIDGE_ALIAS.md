# OTCLIENT-TIBIA-RE P1-BRIDGE alias

```yaml
alias_prompt_contract_version: 1.0.0
alias: OTCLIENT-TIBIA-RE-P1
track_id: official-client-re
lane: P1-BRIDGE
researcher_delivery: draft_only
default_execution_class: github_hosted
default_runtime_access: none
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
```

## Resolution

This alias is an additive lane preset. Load current repository governance plus:

```text
docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_RESEARCH_COORDINATION.md
docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
```

Resolve live `main`, current coordinator state, active Track A tasks, Draft PRs and ownership before claim/resume. Use only a concrete current P1 dispatch/task or a bounded P1 READY item from current durable programme state after overlap checks.

Owner invocation:

```text
Uruchom OTCLIENT-TIBIA-RE-P1 autonomicznie.
```

## Lane preset

Focus on the stable read-only bridge/API, runtime identity/readiness/health, reacquisition, stale-state rejection, recovery semantics and deterministic integration tests.

Default to GitHub-hosted implementation/tests with `runtime_access: none`: unit/integration tests, lifecycle simulation, stale-registration simulation, headless/Xvfb startup integration and deterministic bridge tooling.

Real attach/reacquisition/restart/relogin proof belongs to RUNTIME. P1 may consume durable RUNTIME evidence but must not bootstrap, login, restart, kill, reconfigure or take over the canonical physical session as an implementation shortcut. If canonical identity is unavailable, fail closed rather than guess a PID/display/session.

The Synology physical topology is one persistent canonical desktop + stable owner-visible VNC + one reusable client/session. Bridge code must be compatible with worker/session turnover without requiring that physical desktop/client to be recreated for each P1 run.

Historical `:98`, `6082`, PID/session or a reachable VNC endpoint are not sufficient identity. Any live bridge claim requires fresh authoritative target evidence under the applicable admission boundary.

## Delivery boundary

Research/implementation output is `DRAFT_NOT_PROMOTED`. Persist tests, failures and exact evidence in the assigned task/Draft PR. Coordinator review is required before merge/promotion.

Keep Track B and PR #303-owned runtime surfaces outside mutation/live-observation authority. Do not use owner-funded Codex/OpenAI API/paid AI quota without exact current owner authorization.
