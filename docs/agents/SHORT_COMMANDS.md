# Agent short-command registry

This registry maps owner-facing programme aliases to repository-owned prompts or explicitly identified live task/PR entry points. Live repository governance, task ownership, authorization, CI and runtime evidence remain authoritative over this index.

| Alias | Canonical entry point | Purpose |
|---|---|---|
| `OTCLIENT-TIBIA-RE` | `docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md` | Continue Track A: official Linux Tibia client reverse engineering in `blakinio/otclient`. |
| `OTCLIENT-GLOBAL-LOGIN` | PR `#284`, branch `feat/OTC-20260813-tibia-global-login-lab`, task `docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md` on that branch | Continue Track B: make this OTClient fork authenticate to and enter official Tibia Global. |
| `OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE` | `docs/agents/prompts/OTCLIENT_TIBIA_GLOBAL_LOGIN_FINAL_CONTINUE.md` | Single-window Track B coordinator: continue Global Login and automatically run local Vision/Qwen post-processing in the same invocation when accepted secret-safe keyframes exist. |
| `OTC-BE4F48-SENDLOGIN-SENDER-PEER` | `docs/agents/prompts/OTC_BE4F48_SENDLOGIN_SENDER_PEER.md` | Track A source-only exact-current discriminator for the sender-side peer/event and causal direction that binds native `TProtocolMessageQueue::sendLogin`. |
| `OTC-BE4F48-FINAL-LOGIN-WRITER` | `docs/agents/prompts/OTC_BE4F48_FINAL_LOGIN_WRITER.md` | Track A source-only exact-current discriminator from the proved `sendLogin` adapter to the final queue/TCP writer contract. |

## Invocation

```text
Uruchom OTCLIENT-TIBIA-RE autonomicznie.
Uruchom OTCLIENT-GLOBAL-LOGIN autonomicznie.
Uruchom OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE autonomicznie.
Uruchom OTC-BE4F48-SENDLOGIN-SENDER-PEER autonomicznie.
Uruchom OTC-BE4F48-FINAL-LOGIN-WRITER autonomicznie.
```

The two `OTC-BE4F48-*` aliases are intentionally independent and may be run in parallel by separate agents. Each worker must create its own task/branch/worktree and verify non-overlapping ownership before implementation. Neither alias authorizes Track B #284 mutation, runtime observation, official-client execution or official-service E2E.

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

## `OTC-BE4F48-SENDLOGIN-SENDER-PEER` resolution

1. read `docs/agents/prompts/OTC_BE4F48_SENDLOGIN_SENDER_PEER.md` from fresh trusted `main`;
2. read the promoted `15.32.be4f48` source-blocker evidence referenced by that prompt;
3. verify no newer promotion has superseded the exact-client fence or missing boundary;
4. create a new independent Track A source-only task/branch/Draft PR;
5. resolve only the sender-side peer/event identity and direction; do not expand into final-writer work or Track B mutation.

## `OTC-BE4F48-FINAL-LOGIN-WRITER` resolution

1. read `docs/agents/prompts/OTC_BE4F48_FINAL_LOGIN_WRITER.md` from fresh trusted `main`;
2. read the promoted `15.32.be4f48` source-blocker evidence and independent writer evidence referenced by that prompt;
3. verify no newer promotion has superseded the exact-client fence or missing boundary;
4. create a new independent Track A source-only task/branch/Draft PR;
5. resolve only the serialized queue-object -> final queue/TCP writer contract; do not expand into sender/peer work or Track B mutation.

A fresh worker must not invent a missing Track B task on `main`. While PR #284 is active, its exact branch/task path above is the resolvable durable entry point.

For all aliases, external Oteryn repositories, historical Oteryn runners and old containers are not normal continuation sources. Material continuation state must be recovered from or newly persisted in `blakinio/otclient`. If a required fact is absent there, classify it as `UNKNOWN` and research it inside the owning OTClient track.
