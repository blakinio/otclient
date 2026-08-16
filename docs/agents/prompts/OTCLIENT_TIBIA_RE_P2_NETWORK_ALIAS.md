# OTCLIENT-TIBIA-RE P2-NETWORK alias

```yaml
alias_prompt_contract_version: 1.0.0
alias: OTCLIENT-TIBIA-RE-P2
track_id: official-client-re
lane: P2-NETWORK
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

Resolve live `main`, the current coordinator state, active Track A tasks, open Draft PRs and ownership before claiming work. Use only a concrete current P2 dispatch/task; if none exists, select a bounded P2 READY item only from current durable coordinator/programme state after overlap checks.

Owner invocation:

```text
Uruchom OTCLIENT-TIBIA-RE-P2 autonomicznie.
```

## Lane preset

Focus on final gameplay egress, writer ownership, serialization, framing, sequence, compression/encryption ordering, connection state and the exact downstream byte path.

Prefer GitHub-hosted static/deterministic work: exact-binary analysis, source/tooling, parsers, registries, synthetic/local harnesses, workflow validation and bounded tests. Persist `runtime_access: none` at claim/resume unless a separately reviewed admission explicitly changes it.

If a claim needs a real persistent-client stimulus or physical byte observation, request a bounded RUNTIME experiment and consume its durable evidence. Do not take over display/input/login/session ownership and do not create a second logged-in Track A Global session.

The Synology physical resource is one persistent canonical desktop/client/session shared serially through RUNTIME. P2 must not restart, logout, bootstrap, clean or reconfigure it merely because a new P2 worker starts.

Historical `:98`, `6082`, PID/session or old runtime addresses remain discovery leads only. Current physical identity requires the canonical admission model and fresh evidence.

## Delivery boundary

Research output is `DRAFT_NOT_PROMOTED`. Open/update only the assigned Draft PR and task evidence. Do not merge or promote conclusions into canonical programme knowledge; coordinator review is required.

Keep Track B and PR #303 runtime surfaces outside mutation/live-observation authority. Do not use owner-funded Codex/OpenAI API/paid AI quota without exact current owner authorization.
