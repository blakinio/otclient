# Agent short-command registry

This registry maps owner-facing programme aliases to repository-owned prompts or explicitly identified live task/PR entry points. Live repository governance, task ownership, authorization, CI and runtime evidence remain authoritative over this index.

| Alias | Canonical entry point | Purpose |
|---|---|---|
| `OTCLIENT-TIBIA-RE` | `docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md` | Continue Track A: official Linux Tibia client reverse engineering in `blakinio/otclient`. |
| `OTCLIENT-GLOBAL-LOGIN` | PR `#284`, branch `feat/OTC-20260813-tibia-global-login-lab`, task `docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md` on that branch | Continue Track B: make this OTClient fork authenticate to and enter official Tibia Global. |
| `OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE` | `docs/agents/prompts/OTCLIENT_TIBIA_GLOBAL_LOGIN_FINAL_CONTINUE.md` | Single-window Track B coordinator with local Vision/Qwen post-processing when independently legal secret-safe keyframes exist. |
| `OTC-BE4F48-SENDLOGIN-RECEIVER-FIELD-88-USE-SEMANTICS` | `docs/agents/prompts/OTC_BE4F48_SENDLOGIN_RECEIVER_FIELD_88_USE_SEMANTICS.md` | Exact-current Track A source discriminator for the immediate use/type semantics of the already-promoted sendLogin receiver object loaded from owner field `+0x88`. |
| `OTC-BE4F48-QUEUE-SIGNAL-BF-EXACT-XREF-CONNECT-SITE` | `docs/agents/prompts/OTC_BE4F48_QUEUE_SIGNAL_BF_EXACT_XREF_CONNECT_SITE.md` | Exact-current Track A exact-signal-reference discriminator for one downstream `clientMessageReadyToProcess(0xbf)` connect site/endpoint outside the exhausted queue-constructor-local path. |

Historical consumed aliases:

- `OTC-BE4F48-SENDLOGIN-SENDER-PEER` was completed by source PR #869 and consumed by coordinator promotion #871. Do not relaunch it.
- `OTC-BE4F48-FINAL-LOGIN-WRITER` was completed by source PR #870 and consumed by coordinator promotion #871. Do not relaunch it.
- `OTC-BE4F48-SENDLOGIN-PEER-METAOWNER` was completed by source PR #875 and consumed by coordinator promotion #876. Do not relaunch it.
- `OTC-BE4F48-QUEUE-DRAIN-CONSUMPTION` was completed by source PR #874 and consumed by coordinator promotion #876. Do not relaunch it.
- `OTC-BE4F48-SENDLOGIN-RECEIVER-IDENTITY` was completed by source PR #879 and consumed by coordinator promotion #881. Do not relaunch it.
- `OTC-BE4F48-QUEUE-SIGNAL-BF-RECEIVER` was completed by source PR #880 and consumed by coordinator promotion #881. Do not relaunch it.
- `OTC-BE4F48-SENDLOGIN-RECEIVER-FIELD-OWNER` was completed by source PR #884 and consumed by coordinator promotion #886. Do not relaunch it.
- `OTC-BE4F48-QUEUE-SIGNAL-BF-QSLOT-IDENTITY` was completed by source PR #885 and consumed by coordinator promotion #886. Do not relaunch it.
- `OTC-BE4F48-SENDLOGIN-CONNECTION-OWNER-TYPE` was completed by source PR #889 and consumed by coordinator promotion #891. Do not relaunch it.
- `OTC-BE4F48-QUEUE-SIGNAL-BF-RELAY-RECEIVER-TYPE` was completed by source PR #890 and consumed by coordinator promotion #891. Do not relaunch it.
- `OTC-BE4F48-SENDLOGIN-OWNER-EDGE-7E8F30-IDENTITY` was completed by source PR #894 and consumed by coordinator promotion #896. Do not relaunch it.
- `OTC-BE4F48-QUEUE-SIGNAL-BF-NEXT-RELAY-EDGE` was completed by source PR #895 and consumed by coordinator promotion #896. Do not relaunch it.

## Invocation

```text
Uruchom OTCLIENT-TIBIA-RE autonomicznie.
Uruchom OTCLIENT-GLOBAL-LOGIN autonomicznie.
Uruchom OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE autonomicznie.
Uruchom OTC-BE4F48-SENDLOGIN-RECEIVER-FIELD-88-USE-SEMANTICS autonomicznie.
Uruchom OTC-BE4F48-QUEUE-SIGNAL-BF-EXACT-XREF-CONNECT-SITE autonomicznie.
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

## `OTC-BE4F48-SENDLOGIN-RECEIVER-FIELD-88-USE-SEMANTICS` resolution

1. read `docs/agents/prompts/OTC_BE4F48_SENDLOGIN_RECEIVER_FIELD_88_USE_SEMANTICS.md` from fresh trusted `main`;
2. read `docs/agents/evidence/OTC-20260904-be4f48-post894-895-promotion/20260904-coordinator-promotion.md` and `result.json`;
3. verify no newer promotion supersedes the exact fence/boundary;
4. create a new independent source-only Track A task/branch/Draft PR;
5. start only from `sendLogin connectImpl@0x7c6b9f` and promoted receiver provenance `OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]`;
6. trace only the exact loaded field object's immediate use/ABI semantics and at most one object-tied vptr/QMeta/type edge;
7. do not rerun #884/#889/#894 owner/caller/callee identity work or perform a global `+0x88`/RTTI/QObject census.

## `OTC-BE4F48-QUEUE-SIGNAL-BF-EXACT-XREF-CONNECT-SITE` resolution

1. read `docs/agents/prompts/OTC_BE4F48_QUEUE_SIGNAL_BF_EXACT_XREF_CONNECT_SITE.md` from fresh trusted `main`;
2. read the same post-#894/#895 coordinator promotion evidence;
3. verify no newer promotion supersedes the exact fence/boundary;
4. create a new independent source-only Track A task/branch/Draft PR;
5. start only from exact `clientMessageReadyToProcess` identity/body `0xbd2190`, index `0xbf`, proven `TProtocolMessageQueue` receiver and exact `GameclientMessage` shared pair;
6. admit only exact-signal reference sites that can be causally tied to a `QObject::connectImpl` setup, then inspect at most one unique endpoint identity edge;
7. do not redo #885/#890/#895 constructor/QSlot/receiver work and do not open a generic global QObject/connect/socket/writer census.

A fresh worker must not invent a missing Track B task on `main`. While PR #284 is active, its exact branch/task is the durable Track B entry point.

For all aliases, external Oteryn repositories, historical runners and old containers are not normal continuation sources. If a required fact is absent from current OTClient durable state, classify it as `UNKNOWN` and research it inside the owning track.
