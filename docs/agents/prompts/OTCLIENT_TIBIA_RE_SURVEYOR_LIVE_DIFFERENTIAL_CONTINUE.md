# OTCLIENT-TIBIA-RE-SURVEYOR-LIVE-DIFFERENTIAL-CONTINUE

Repository:

```text
https://github.com/blakinio/otclient
```

Mode: autonomous continuation of Track A Surveyor live differential research from current live repository/runtime state.

## Primary objective

Continue the currently in-progress live differential validation of Surveyor v2 against the owner's already-running, already-logged-in official Tibia client on Synology. Determine which real client state changes are and are not represented by current Surveyor typed outputs, then use those measured gaps to drive the next smallest P0 typed-reader implementation task.

Do not restart this programme from scratch and do not trust stale chat state, historical SHAs, PIDs, screenshots, task summaries or prior `IN_GAME` conclusions as current authority.

## Mandatory bootstrap

Before doing substantial work:

1. fetch and inspect current `main`;
2. read root and applicable `AGENTS.md` files;
3. read current Track A runtime admission/governance, KasmVNC access, Surveyor operator and prompting/continuation contracts;
4. read `docs/agents/evidence/OTC-20260820-surveyor-live-differential/handoff.md`;
5. inspect current active tasks, open overlapping PRs, canonical lease/registration state and current runtime ownership;
6. revalidate the target container, display, exact current client PID/size/SHA, single visible Tibia window and target uniqueness before relying on the physical runtime;
7. treat `BRIDGE_3_OF_3` strictly as structural object-presence evidence, never standalone gameplay-state proof.

## Current durable handoff state

The owner was already in the game world and did not need to log in for this testing session.

Three read-only snapshots were collected:

```text
idle baseline: /tmp/tibia-re-baseline-1787232278
movement:      /tmp/tibia-re-move-1787232435
backpack open: /tmp/tibia-re-backpack-1787232581
```

Observed session values, discovery-only until revalidated:

```text
runtime container: otclient-track-a-kasmvnc
display: :1
client PID: 19590
client size: 52109920
client SHA-256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
visible window id: 27262999
Surveyor coverage rows: 169
aliases: 12/12
missing typed readers: 11
privacy: PASS
bridge structural counts: 1/1/1
```

Measured semantic differential results after removing timestamp-only fields:

```text
BASE_VS_MOVE_SEMANTIC_DIFF_FILES=0
BASE_VS_BACKPACK_SEMANTIC_DIFF_FILES=0
MOVE_VS_BACKPACK_SEMANTIC_DIFF_FILES=0
```

This means current Surveyor output did not expose a semantic delta for either:

- moving the player approximately 3-5 tiles;
- opening the main backpack and leaving it open.

Treat these as proven typed-reader/semantic-coverage gaps.

## Continuation procedure

Continue with one owner-controlled action at a time. The agent remains read-only.

Preferred next sequence:

1. ask the owner to perform one low-risk, reversible UI action only;
2. immediately collect a fresh Surveyor `--collect-all` snapshot;
3. compare every common JSON document against the prior snapshot and idle baseline, excluding timestamp-only fields;
4. record exact changed files/fields, or exact zero-delta result;
5. repeat only while each experiment adds information;
6. if repeated UI actions still yield zero semantic deltas, stop collecting redundant observations and pivot into the highest-value P0 typed-reader implementation suggested by `missing-readers.json` plus the proven movement/backpack gaps.

Candidate remaining owner actions, one at a time:

- open/close a distinct UI panel expected to map to `UI-SETTINGS` or `FEATURES`;
- open/minimize a minimap-related panel without moving;
- change battle-list selection without attacking;
- change active chat tab/channel without sending a message.

Do not request logout, relog or restart merely to continue this research.

## Runtime and safety constraints

The agent must not:

- type credentials or read/copy credential values;
- log in, log out, relog or select a character;
- inject keyboard/mouse gameplay input;
- move the character or manipulate inventory on behalf of the owner;
- attack, trade, buy, sell or perform economy actions;
- restart, stop, kill, signal, attach to, debug or inject into the official client;
- mutate canonical lease/registration state without a separately admitted task that explicitly authorizes that transition;
- use local Ollama or any other local AI model for this continuation unless the owner explicitly changes that instruction.

Owner-performed manual gameplay/UI actions are allowed when the owner is explicitly participating in the differential test.

## Research decision rule

The goal is not to maximize the number of manual tests. The goal is to identify the smallest set of missing typed readers that unlock useful live semantic state.

Prioritize P0 implementation when one of these is true:

- a real user-visible state change produces zero Surveyor semantic delta;
- an alias exists but only contains static/structural evidence and no useful live state;
- `missing-readers.json` points to a reader that would explain multiple measured gaps;
- another manual experiment would be redundant with already proven zero-delta behavior.

For any implementation task, start with static resolver/parser and hosted deterministic tests. Use physical runtime only for the exact semantic claim that cannot be proven hosted.

## Validation and closeout

Do not claim success because a snapshot ran, an alias file exists or a reader compiles.

For any implemented reader:

1. add focused deterministic tests;
2. add hosted regression coverage;
3. run exact-head CI/governance;
4. obtain fresh audit appropriate to task risk;
5. merge through PR, never direct-to-main;
6. perform a fresh owner-controlled live differential proving the expected semantic field now changes for the target action;
7. update durable evidence/task records;
8. release any runtime ownership/lease introduced by the task;
9. make related PRs/tasks intentionally terminal.

## Stop conditions

Continue autonomously until one of these is true:

- the bounded differential slice is fully measured and its resulting P0 reader task is terminally implemented/validated/merged;
- a real authority/safety/ownership blocker prevents further work;
- a manual owner action is required for the next differential, in which case ask for exactly one action and wait without doing unrelated runtime mutation;
- context/tool limits make further execution unsafe.

Do not stop merely at analysis, a zero-delta observation, an opened PR, green CI or a proposed reader.
