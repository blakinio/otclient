# OTCLIENT-TIBIA-RE Surveyor v2 next non-overlap gap alias

```yaml
alias_prompt_contract_version: 1.0.0
alias: OTCLIENT-TIBIA-RE-SURVEYOR-V2-NEXT-NONOVERLAP-GAP-CONTINUE
repository: blakinio/otclient
track_id: official-client-re
canonical_prompt: docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_NEXT_NONOVERLAP_GAP_CONTINUE.md
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
```

Resolve this alias only from live `blakinio/otclient` state.

Read the canonical prompt above in full, then refresh current `main`, current Surveyor `--collect-all`, active/archived tasks, open PRs, ownership, exact client/runtime identity and Track A admission state before selecting work.

Do not hard-code the historical remaining-gap count or the next reader. Select the highest-value safe non-overlapping typed-reader gap from live state.

While current world/minimap ownership or active work overlaps that family, including PR #475 / PR #593 or their successors, exclude it from selection rather than creating competing work.

This alias grants no login, credential, gameplay input, process-control, process-memory write, network mutation, second-session, local-model or owner-funded AI authority.

Owner invocation:

```text
Kontynuuj OTCLIENT-TIBIA-RE-SURVEYOR-V2-NEXT-NONOVERLAP-GAP-CONTINUE autonomicznie.
```
