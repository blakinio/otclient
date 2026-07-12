# Active Work Index

Last reviewed: 2026-07-12T12:40:00+02:00

Open PRs and current GitHub state are authoritative.

| PR | Branch | State | Area / reusable work | Primary paths | Coordination note |
|---:|---|---|---|---|---|
| [#4](https://github.com/blakinio/otclient/pull/4) | `docs/agent-handoff` | open | Existing repository handoff/governance | `AGENT_HANDOFF.md` | Reconcile with `docs/agents/**`; avoid contradictory rules. |
| [#3](https://github.com/blakinio/otclient/pull/3) | `test/client-test-foundation` | open | Reusable C++/Lua test support, builders, fixtures, loopback, presets | `tests/**`, `CMakePresets.json`, test workflows/docs | New tests should reuse this support, not create parallel harnesses. |

## Rules

- Add a row after publishing task branch/draft PR.
- Include reusable modules/test utilities/protocol/UI infrastructure introduced.
- Remove or supersede after merge/closure.
- Detailed execution state belongs in task record.
