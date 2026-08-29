# Agent short-command registry

This registry maps owner-facing programme aliases to repository-owned prompts or explicitly identified live task/PR entry points. Live repository governance, task ownership, authorization, CI and runtime evidence remain authoritative over this index.

| Alias | Canonical entry point | Purpose |
|---|---|---|
| `OTCLIENT-TIBIA-RE` | `docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md` | Continue Track A: official Linux Tibia client reverse engineering in `blakinio/otclient`. |
| `OTCLIENT-GLOBAL-LOGIN` | PR `#284`, branch `feat/OTC-20260813-tibia-global-login-lab`, task `docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md` on that branch | Continue Track B: make this OTClient fork authenticate to and enter official Tibia Global. |
| `OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE` | `docs/agents/prompts/OTCLIENT_TIBIA_GLOBAL_LOGIN_FINAL_CONTINUE.md` | Single-window Track B coordinator: continue Global Login and automatically run local Vision/Qwen post-processing in the same invocation when accepted secret-safe keyframes exist. |

## Invocation

```text
Uruchom OTCLIENT-TIBIA-RE autonomicznie.
Uruchom OTCLIENT-GLOBAL-LOGIN autonomicznie.
Uruchom OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE autonomicznie.
```

## `OTCLIENT-TIBIA-RE` resolution

1. read `docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md`;
2. read the base programme prompt it extends;
3. read repository-owned consolidated state/report evidence, including:
   - `docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md`;
   - `docs/agents/reports/OTCLIENT-20260813-tibia-re-login-recovery-import.md`;
   - `docs/agents/reports/OTCLIENT-20260813-tibia-re-external-evidence-manifest.md`;
4. inspect live `main`, active Track A tasks, open PRs, runner/runtime state and exact `next_action` values;
5. execute only Track A from durable OTClient state.

## `OTCLIENT-GLOBAL-LOGIN` resolution

1. read `docs/agents/TIBIA_RESEARCH_TRACKS.md` first;
2. resolve live PR `#284` and verify its current head branch is still `feat/OTC-20260813-tibia-global-login-lab` or use the live replacement recorded by repository state if it has become terminal/superseded;
3. read `docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md` from that exact live branch while PR #284 remains active;
4. inspect the PR's current changed files, checks, runtime evidence and exact `next_action`;
5. operate only on Track B owned paths/runtime namespace;
6. once PR #284 merges or is superseded, resolve Track B from the resulting `main` task/archive/replacement state rather than assuming the historical branch remains active.

## `OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE` resolution

1. read `docs/agents/prompts/OTCLIENT_TIBIA_GLOBAL_LOGIN_FINAL_CONTINUE.md` from fresh trusted `main`;
2. let that prompt resolve the live Track B PR/task exactly as `OTCLIENT-GLOBAL-LOGIN` does;
3. keep structural Track B work authoritative and do not trigger an E2E for screenshots;
4. when a future independently legal Track B E2E yields accepted secret-safe keyframes, run the merged local `tools/tibia-re-vision-benchmark` Qwen path automatically in the same invocation;
5. never ask the owner to open a second chat/window or manually launch the Vision benchmark merely to continue Track B.

A fresh worker must not invent a missing Track B task on `main`. While PR #284 is active, its exact branch/task path above is the resolvable durable entry point.

For all aliases, external Oteryn repositories, historical Oteryn runners and old containers are not normal continuation sources. Material continuation state must be recovered from or newly persisted in `blakinio/otclient`. If a required fact is absent there, classify it as `UNKNOWN` and research it inside the owning OTClient track.
