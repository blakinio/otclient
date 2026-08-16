# OTCLIENT-TIBIA-RE COVERAGE-AUDIT alias

```yaml
alias_prompt_contract_version: 1.0.0
alias: OTCLIENT-TIBIA-RE-AUDIT
track_id: official-client-re
lane: COVERAGE-AUDIT
researcher_delivery: draft_only
default_execution_class: github_hosted
default_runtime_access: none
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: false
```

## Resolution

This alias is an additive audit-lane preset. Load current repository governance plus:

```text
docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_RESEARCH_COORDINATION.md
docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
```

Resolve live `main`, current coordinator state, active tasks, Draft PRs, exact evidence heads and ownership before claim/resume.

Owner invocation:

```text
Uruchom OTCLIENT-TIBIA-RE-AUDIT autonomicznie.
```

## Lane preset

Focus on quantitative coverage, protocol/QMeta/P0/P1 denominator checks, evidence indexing, contradiction/supersession review, missing-proof inventory and campaign completeness falsification.

Run on GitHub-hosted infrastructure with `runtime_access: none`. Consume durable RUNTIME artifacts/reports and other lane Draft evidence. Do not take the Synology physical session merely to refresh coverage numbers.

When an audit gap genuinely requires new physical evidence, specify the smallest falsifiable discriminator and request a bounded RUNTIME experiment. The one persistent Synology desktop + owner-visible VNC + canonical client/session remains under serialized RUNTIME ownership and must not be recreated per audit worker.

Never promote historical `:98`, `6082`, PID/session, old offsets or old CI as current runtime truth. Distinguish inventory completeness from semantic proof and green execution from capability proof.

## Delivery boundary

Output is `DRAFT_NOT_PROMOTED`. Persist exact denominators, evidence references, contradictions, unknowns and recommended bounded next experiments. Coordinator review is required before global coverage/programme state changes or merge.

Keep Track B and PR #303 runtime surfaces outside mutation/live-observation authority. Do not use owner-funded Codex/OpenAI API/paid AI quota without exact current owner authorization.
