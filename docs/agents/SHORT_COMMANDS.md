# Agent short-command registry

This registry maps owner-facing programme aliases to repository-owned prompts or explicitly identified live task/PR entry points. Live repository governance, task ownership, authorization, CI and runtime evidence remain authoritative over this index.

| Alias | Canonical entry point | Purpose |
|---|---|---|
| `OTCLIENT-TIBIA-RE` | `docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md` | Continue Track A: official Linux Tibia client reverse engineering in `blakinio/otclient`. |
| `OTCLIENT-GLOBAL-LOGIN` | PR `#284`, branch `feat/OTC-20260813-tibia-global-login-lab`, task `docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md` on that branch | Continue Track B: make this OTClient fork authenticate to and enter official Tibia Global. |
| `OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE` | `docs/agents/prompts/OTCLIENT_TIBIA_GLOBAL_LOGIN_FINAL_CONTINUE.md` | Single-window Track B coordinator with local Vision/Qwen post-processing when independently legal secret-safe keyframes exist. |
| `OTC-BE4F48-SENDLOGIN-PEER-METAOWNER` | `docs/agents/prompts/OTC_BE4F48_SENDLOGIN_PEER_METAOWNER.md` | Exact-current Track A source discriminator from `0x30b68a0`/signal 0 to peer owner and actual bounded Qt connection direction. |
| `OTC-BE4F48-QUEUE-DRAIN-CONSUMPTION` | `docs/agents/prompts/OTC_BE4F48_QUEUE_DRAIN_CONSUMPTION.md` | Exact-current Track A source discriminator from owned queue callback `0xbd2190` to causal consumption of the exact queued `GameclientMessage`. |

Historical consumed aliases:

- `OTC-BE4F48-SENDLOGIN-SENDER-PEER` was completed by source PR #869 and consumed by coordinator promotion #871. Do not relaunch it.
- `OTC-BE4F48-FINAL-LOGIN-WRITER` was completed by source PR #870 and consumed by coordinator promotion #871. Do not relaunch it.

## Invocation

```text
Uruchom OTCLIENT-TIBIA-RE autonomicznie.
Uruchom OTCLIENT-GLOBAL-LOGIN autonomicznie.
Uruchom OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE autonomicznie.
Uruchom OTC-BE4F48-SENDLOGIN-PEER-METAOWNER autonomicznie.
Uruchom OTC-BE4F48-QUEUE-DRAIN-CONSUMPTION autonomicznie.
```

The two current `OTC-BE4F48-*` aliases are intentionally independent and may be run in parallel by separate agents. Each worker must create its own task/branch/worktree and verify non-overlapping ownership. Neither alias authorizes Track B #284 mutation, runtime observation, official-client execution, OCR/Vision or official-service E2E.

## `OTCLIENT-TIBIA-RE` resolution

1. read `docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md`;
2. read the base programme prompt it extends;
3. inspect live `main`, active Track A tasks, open PRs, runner/runtime state and exact `next_action` values;
4. execute only Track A from durable OTClient state.

## `OTCLIENT-GLOBAL-LOGIN` resolution

1. read `docs/agents/TIBIA_RESEARCH_TRACKS.md` first;
2. resolve live PR `#284` and its exact active task on the live head branch;
3. inspect current changed files, checks, runtime evidence and exact `next_action`;
4. operate only on Track B owned paths/runtime namespace;
5. once #284 merges or is superseded, resolve Track B from resulting `main` state rather than assuming the historical branch remains active.

## `OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE` resolution

1. read `docs/agents/prompts/OTCLIENT_TIBIA_GLOBAL_LOGIN_FINAL_CONTINUE.md` from fresh trusted `main`;
2. let that prompt resolve live Track B state;
3. keep structural Track B evidence authoritative;
4. run local Vision/Qwen only when an independently legal Track B E2E already produced accepted secret-safe keyframes;
5. never trigger an E2E merely to obtain screenshots.

## `OTC-BE4F48-SENDLOGIN-PEER-METAOWNER` resolution

1. read `docs/agents/prompts/OTC_BE4F48_SENDLOGIN_PEER_METAOWNER.md` from fresh trusted `main`;
2. read `docs/agents/evidence/OTC-20260903-be4f48-post869-870-promotion/20260903-coordinator-promotion.md` and `result.json`;
3. verify no newer promotion supersedes the exact fence/boundary;
4. create a new independent source-only Track A task/branch/Draft PR;
5. resolve only the `0x30b68a0` peer-metaobject/actual-connection boundary; do not reuse `0x4d8670` as connection authority.

## `OTC-BE4F48-QUEUE-DRAIN-CONSUMPTION` resolution

1. read `docs/agents/prompts/OTC_BE4F48_QUEUE_DRAIN_CONSUMPTION.md` from fresh trusted `main`;
2. read the same post-#869/#870 coordinator promotion evidence;
3. verify no newer promotion supersedes the exact fence/boundary;
4. create a new independent source-only Track A task/branch/Draft PR;
5. resolve only causal consumption of the exact queued `GameclientMessage` by owned callback `0xbd2190`, following at most the next unique writer edge.

A fresh worker must not invent a missing Track B task on `main`. While PR #284 is active, its exact branch/task is the durable Track B entry point.

For all aliases, external Oteryn repositories, historical runners and old containers are not normal continuation sources. If a required fact is absent from current OTClient durable state, classify it as `UNKNOWN` and research it inside the owning track.
