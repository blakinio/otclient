# OTCLIENT-TIBIA-RE P0-STATE alias

```yaml
alias_prompt_contract_version: 1.0.0
alias: OTCLIENT-TIBIA-RE-P0
track_id: official-client-re
lane: P0-STATE
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

Resolve live `main`, current coordinator state, active Track A tasks, Draft PRs and ownership before claim/resume. Use only a concrete current P0 task or a bounded P0 READY item derived from current durable programme state after overlap checks.

Owner invocation:

```text
Uruchom OTCLIENT-TIBIA-RE-P0 autonomicznie.
```

## Lane preset

Focus on direct player/world/UI-backed semantic state, direct runtime storage, structural read candidates, resolvers, P0 registries and deterministic validation.

Default to GitHub-hosted static/deterministic discovery and `runtime_access: none`. Do not create a fresh official-client login/session merely to validate a candidate read.

When direct semantic/causal validation requires the real client, consume a bounded RUNTIME evidence request or use separately admitted non-conflicting `read_only` access only when non-invasiveness, explicit namespace/ownership and `target_uniqueness: PROVEN` are fresh. Ambiguity means refuse live observation.

The physical Synology topology is one persistent canonical desktop + owner-visible VNC + one reusable client/session. P0 is an evidence consumer, not the owner of that resource. A new P0 worker must never reset the desktop, VNC, login or client just to recreate context.

Historical `:98`, `6082`, PID/session and ASLR-dependent addresses are not current authority. Revalidate exact client fence and runtime identity before any live claim.

## Delivery boundary

Research output is `DRAFT_NOT_PROMOTED`. Persist exact facts/inferences/unknowns and negative controls in the assigned task/Draft PR; coordinator review is required before canonical promotion or merge.

Keep Track B and PR #303-owned runtime surfaces outside mutation/live-observation authority. Do not use owner-funded Codex/OpenAI API/paid AI quota without exact current owner authorization.
