# Agent short-command registry

This registry maps owner-facing programme aliases to repository-owned prompts or explicitly identified live task/PR entry points. Live repository governance, task ownership, authorization, CI and runtime evidence remain authoritative over this index.

| Alias | Canonical entry point | Purpose |
|---|---|---|
| `OTCLIENT-TIBIA-RE` | `docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md` | Continue Track A: official Linux Tibia client reverse engineering in `blakinio/otclient`. |
| `OTCLIENT-GLOBAL-LOGIN` | PR `#284`, branch `feat/OTC-20260813-tibia-global-login-lab`, task `docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md` on that branch | Continue Track B: make this OTClient fork authenticate to and enter official Tibia Global. |
| `OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE` | `docs/agents/prompts/OTCLIENT_TIBIA_GLOBAL_LOGIN_FINAL_CONTINUE.md` | Single-window Track B coordinator with local Vision/Qwen post-processing when independently legal secret-safe keyframes exist. |
| `OTC-BE4F48-SENDLOGIN-ADAPTER-BD3050-RECEIVER-SEMANTICS` | `docs/agents/prompts/OTC_BE4F48_SENDLOGIN_ADAPTER_BD3050_RECEIVER_SEMANTICS.md` | Exact-current Track A discriminator for the sendLogin adapter callable `0xbd3050` and whether its exact QSlot/adapter semantics uniquely bind the proven `+0x88` receiver to one receiver/member/slot identity. |
| `OTC-BE4F48-QUEUE-SIGNAL-BF-QMETA-INDEX-CONNECTION` | `docs/agents/prompts/OTC_BE4F48_QUEUE_SIGNAL_BF_QMETA_INDEX_CONNECTION.md` | Exact-current Track A discriminator for downstream connection registration using the exact `TProtocolMessageQueue` QMeta method index `0xbf`, without repeating exhausted body/name xrefs. |

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
- `OTC-BE4F48-SENDLOGIN-RECEIVER-FIELD-88-USE-SEMANTICS` was completed by source PR #899 and consumed by coordinator promotion #901. Do not relaunch it.
- `OTC-BE4F48-QUEUE-SIGNAL-BF-EXACT-XREF-CONNECT-SITE` was completed by source PR #900 and consumed by coordinator promotion #901. Do not relaunch it.

## Invocation

```text
Uruchom OTCLIENT-TIBIA-RE autonomicznie.
Uruchom OTCLIENT-GLOBAL-LOGIN autonomicznie.
Uruchom OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE autonomicznie.
Uruchom OTC-BE4F48-SENDLOGIN-ADAPTER-BD3050-RECEIVER-SEMANTICS autonomicznie.
Uruchom OTC-BE4F48-QUEUE-SIGNAL-BF-QMETA-INDEX-CONNECTION autonomicznie.
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

## `OTC-BE4F48-SENDLOGIN-ADAPTER-BD3050-RECEIVER-SEMANTICS` resolution

1. read `docs/agents/prompts/OTC_BE4F48_SENDLOGIN_ADAPTER_BD3050_RECEIVER_SEMANTICS.md` from fresh trusted `main`;
2. read `docs/agents/evidence/OTC-20260904-be4f48-post899-900-promotion/20260904-coordinator-promotion.md` and `result.json`;
3. verify no newer promotion supersedes the exact fence/boundary;
4. create a new independent source-only Track A task/branch/Draft PR;
5. start only from sendLogin `connectImpl@0x7c6b9f`, proven receiver field load `0x7c6b18`, and promoted adapter target `0xbd3050`;
6. derive exact adapter invocation ABI, then inspect only this connection's QSlot/adapter construction plus at most one unique adapter-internal receiver/member edge;
7. do not rerun #884/#889/#894/#899 owner/caller/callee/field-lifetime scans and do not open a global QSlot/QObject/vtable census.

## `OTC-BE4F48-QUEUE-SIGNAL-BF-QMETA-INDEX-CONNECTION` resolution

1. read `docs/agents/prompts/OTC_BE4F48_QUEUE_SIGNAL_BF_QMETA_INDEX_CONNECTION.md` from fresh trusted `main`;
2. read the same post-#899/#900 coordinator promotion evidence;
3. verify no newer promotion supersedes the exact fence/boundary;
4. create a new independent source-only Track A task/branch/Draft PR;
5. start only from exact queue static metaobject `0x30b73e0`, signal index `0xbf`, method row `0x1ce47c0`, owner `TProtocolMessageQueue` and exact signal identity;
6. admit only method-index/static-metacall/index-based connection-registration semantics causally bound to that exact tuple, then inspect at most one unique endpoint edge;
7. do not redo #885/#890/#895 constructor/QSlot work or #900 body/method/name xref enumeration, and do not open a global QObject/QMeta/connect/socket/writer census.

A fresh worker must not invent a missing Track B task on `main`. While PR #284 is active, its exact branch/task is the durable Track B entry point.

For all aliases, external Oteryn repositories, historical runners and old containers are not normal continuation sources. If a required fact is absent from current OTClient durable state, classify it as `UNKNOWN` and research it inside the owning track.
