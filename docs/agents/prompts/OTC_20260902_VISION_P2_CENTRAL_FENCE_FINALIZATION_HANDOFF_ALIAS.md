# OTC Vision P2 Central Fence Finalization — Alias

```yaml
alias: OTC-VISION-P2-CENTRAL-FENCE-FINALIZE
canonical_prompt: docs/agents/prompts/OTC_20260902_VISION_P2_CENTRAL_FENCE_FINALIZATION_HANDOFF.md
repository: blakinio/otclient
role: finalizer_and_coordinator
continuation_policy: autonomous_until_terminal_or_real_external_stop
anti_loop: strict
```

## Owner invocation

```text
Uruchom OTC-VISION-P2-CENTRAL-FENCE-FINALIZE autonomicznie.
```

Resume existing centralization branch and Vision P2 PR chain. Do not restart discovery, open duplicate tasks/PRs, or create new architecture unless a concrete gate proves it necessary. Fresh GitHub/repository state overrides checkpoint SHAs.
