# Agent short-command registry

This registry maps owner-facing programme aliases to repository-owned prompts or explicitly identified live task/PR entry points. Live repository governance, task ownership, authorization, CI and runtime evidence remain authoritative over this index.

| Alias | Canonical entry point | Purpose |
|---|---|---|
| `OTCLIENT-TIBIA-RE` | `docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md` | Continue Track A: official Linux Tibia client reverse engineering in `blakinio/otclient`. |
| `OTCLIENT-GLOBAL-LOGIN` | PR `#284`, branch `feat/OTC-20260813-tibia-global-login-lab`, task `docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md` on that branch | Continue Track B: make this OTClient fork authenticate to and enter official Tibia Global. |
| `OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE` | `docs/agents/prompts/OTCLIENT_TIBIA_GLOBAL_LOGIN_FINAL_CONTINUE.md` | Single-window Track B coordinator with local Vision/Qwen post-processing when independently legal secret-safe keyframes exist. |
| `OTC-BE4F48-SENDLOGIN-CONNECTION-OWNER-TYPE` | `docs/agents/prompts/OTC_BE4F48_SENDLOGIN_CONNECTION_OWNER_TYPE.md` | Exact-current Track A source discriminator for the class/type identity of the selected sendLogin connection-owner object and, only if uniquely implied, its `+0x88` receiver field. |
| `OTC-BE4F48-QUEUE-SIGNAL-BF-RELAY-RECEIVER-TYPE` | `docs/agents/prompts/OTC_BE4F48_QUEUE_SIGNAL_BF_RELAY_RECEIVER_TYPE.md` | Exact-current Track A source discriminator for the receiver class/relay role at `clientMessageReadyToProcess(0xbf) -> connectImpl@0xbe2eee`, with at most one next unique relay edge. |

Historical consumed aliases:

- `OTC-BE4F48-SENDLOGIN-SENDER-PEER` was completed by source PR #869 and consumed by coordinator promotion #871. Do not relaunch it.
- `OTC-BE4F48-FINAL-LOGIN-WRITER` was completed by source PR #870 and consumed by coordinator promotion #871. Do not relaunch it.
- `OTC-BE4F48-SENDLOGIN-PEER-METAOWNER` was completed by source PR #875 and consumed by coordinator promotion #876. Do not relaunch it.
- `OTC-BE4F48-QUEUE-DRAIN-CONSUMPTION` was completed by source PR #874 and consumed by coordinator promotion #876. Do not relaunch it.
- `OTC-BE4F48-SENDLOGIN-RECEIVER-IDENTITY` was completed by source PR #879 and consumed by coordinator promotion #881. Do not relaunch it.
- `OTC-BE4F48-QUEUE-SIGNAL-BF-RECEIVER` was completed by source PR #880 and consumed by coordinator promotion #881. Do not relaunch it.
- `OTC-BE4F48-SENDLOGIN-RECEIVER-FIELD-OWNER` was completed by source PR #884 and consumed by coordinator promotion #886. Do not relaunch it.
- `OTC-BE4F48-QUEUE-SIGNAL-BF-QSLOT-IDENTITY` was completed by source PR #885 and consumed by coordinator promotion #886. Do not relaunch it.

## Invocation

```text
Uruchom OTCLIENT-TIBIA-RE autonomicznie.
Uruchom OTCLIENT-GLOBAL-LOGIN autonomicznie.
Uruchom OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE autonomicznie.
Uruchom OTC-BE4F48-SENDLOGIN-CONNECTION-OWNER-TYPE autonomicznie.
Uruchom OTC-BE4F48-QUEUE-SIGNAL-BF-RELAY-RECEIVER-TYPE autonomicznie.
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

## `OTC-BE4F48-SENDLOGIN-CONNECTION-OWNER-TYPE` resolution

1. read `docs/agents/prompts/OTC_BE4F48_SENDLOGIN_CONNECTION_OWNER_TYPE.md` from fresh trusted `main`;
2. read `docs/agents/evidence/OTC-20260904-be4f48-post884-885-promotion/20260904-coordinator-promotion.md` and `result.json`;
3. verify no newer promotion supersedes the exact fence/boundary;
4. create a new independent source-only Track A task/branch/Draft PR;
5. start only from connection-owner FDE `0x7c6700..0x7cc933`, its `ENTRY_ARG:rdi` object and the promoted `[entry-rdi-derived-rbx+0x88]` receiver field;
6. use only bounded in-FDE or one unique identity-preserving vtable/RTTI/QMeta/type edge to type the owner; do not repeat #884's zero-result direct-caller scan;
7. only if owner identity makes the route unique may the `+0x88` receiver type be classified.

## `OTC-BE4F48-QUEUE-SIGNAL-BF-RELAY-RECEIVER-TYPE` resolution

1. read `docs/agents/prompts/OTC_BE4F48_QUEUE_SIGNAL_BF_RELAY_RECEIVER_TYPE.md` from fresh trusted `main`;
2. read the same post-#884/#885 coordinator promotion evidence;
3. verify no newer promotion supersedes the exact fence/boundary;
4. create a new independent source-only Track A task/branch/Draft PR;
5. start only from `connectImpl@0xbe2eee`, receiver `ENTRY_ARG:rdi`, exact QSlot callable `0xbd2190`, and the causally carried exact `GameclientMessage` shared pair;
6. resolve the receiver object/class and whether the connection is a signal relay; do not redo #885's QSlot construction analysis;
7. only if unique may one next identity-preserving `clientMessageReadyToProcess` relay edge be followed; no global Qt/socket/writer census.

A fresh worker must not invent a missing Track B task on `main`. While PR #284 is active, its exact branch/task is the durable Track B entry point.

For all aliases, external Oteryn repositories, historical runners and old containers are not normal continuation sources. If a required fact is absent from current OTClient durable state, classify it as `UNKNOWN` and research it inside the owning track.
