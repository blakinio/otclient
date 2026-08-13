# Agent short-command registry

This registry maps owner-facing programme aliases to repository-owned prompts. Live repository governance, task ownership, authorization, CI and runtime evidence remain authoritative over this index.

| Alias | Canonical prompt | Purpose |
|---|---|---|
| `OTCLIENT-TIBIA-RE` | `docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md` | Continue the official Linux Tibia reverse-engineering programme in `blakinio/otclient` using the dedicated OTClient runner and durable repository state. |

## Invocation

```text
Uruchom OTCLIENT-TIBIA-RE autonomicznie.
```

Resolution procedure:

1. read the canonical prompt listed above;
2. read the base programme prompt it extends;
3. read the repository-owned consolidated state/report evidence, including:
   - `docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md`;
   - `docs/agents/reports/OTCLIENT-20260813-tibia-re-login-recovery-import.md`;
   - `docs/agents/reports/OTCLIENT-20260813-tibia-re-external-evidence-manifest.md`;
4. inspect live `main`, active tasks, open PRs, runner/runtime state and exact `next_action` values;
5. execute the programme from durable state rather than chat memory;
6. do not invent a task named `OTCLIENT-TIBIA-RE.md`, a branch named `agent/otclient-tibia-re`, or a required `workflow_dispatch` endpoint.

External Oteryn repositories, historical Oteryn runners and old containers are evidence sources only for this alias unless the owner separately authorizes work there. Material continuation state must be persisted or indexed in `blakinio/otclient` before return/rotation.
