# TIBIA-RE-AUTH-SESSION — coordinator strict result

```yaml
task: OTC-20260819-track-a-auth-session-current-build-static
source_pr: 556
source_head: 411d0e287d08406c682ef063fb3f3f61341d9295
audit_pr: 568
audit_head: 4d377f8088e07e68f3680558212f16e532201f70
strict_run: 32239540646
strict_artifact: 9360231314
github_artifact_digest: sha256:f81ab45076a2f31d7fa9bfc34793009a1a52347e4dd26ad6ce73225e274d12b7
independent_download_sha256: f81ab45076a2f31d7fa9bfc34793009a1a52347e4dd26ad6ce73225e274d12b7
strict_txt_sha256: a80f02c141ebd1aa2b26bf76e3fb7eca10458ee64797f3053d7c4742ed0dffc4
coordinator_review: 4970802493
coordinator_decision: ACCEPT_WITH_EDITS
open_material_findings_after_repair: 0
runtime_access: none
```

## Exact current build

The independent strict workflow fetched the public native-Linux package and failed closed on the canonical current fence:

```text
unpacked size   52109920
unpacked SHA256 ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
ELF build ID    d803d9695868713ef6ab0c3cf65f91212c9c6a62
```

The raw packed/unpacked client was deleted before the sanitized `strict.txt` artifact was uploaded.

## H1 / H2 — current TGameClient method bindings

The strict discriminator recovered one complete QMeta invoke switch for `tibia::client::TGameClient`:

```text
METHODS=44
SIGNALS=6
TABLE=0x1d903c4

0xd19104: cmp edx, 0x2b
0xd1910a: lea rsi, [rip + 0x10772b3]
0xd1911b: movsxd rax, dword ptr [rsi + rdx*4]
0xd1911f: add rax, rsi
0xd19122: jmp rax
```

The complete table contained executable targets for the full QMeta method range and proved:

```text
onRequestLoginWithCredentials
  index=17
  role=METHOD
  argc=2
  params=0x2b,0xa,0xa   # void, QString, QString
  target=0xd196f0

connectClientToGameserverWithExistingCredentials
  index=11
  role=METHOD
  argc=0
  params=0x2b
  target=0xd19500
```

Therefore H1 and H2 are `PASS` for this exact build.

These are exact-build QMeta dispatch targets. The static result does not prove live object provenance, thread affinity, call safety, authentication success, or game-world entry.

## H3 — loginSuccessful is a signal target

For `tibia::authentication::TLoginRequestUploader`:

```text
METHODS=9
SIGNALS=8
TABLE=0x1d8ffec

0xd0ffef: cmp edx, 8
0xd0fff4: lea rcx, [rip + 0x107fff1]
0xd10000: movsxd rax, dword ptr [rcx + rdx*4]
0xd10004: add rax, rcx
0xd10007: jmp rax

loginSuccessful
  index=0
  role=SIGNAL
  target=0xd10200
  flags=0x106
```

H3 is `PASS`. Canonical wording must call `0xd10200` a QMeta signal activation dispatch target, not a call-safe business implementation.

## H4 — requestCharacterLogin is a signal target

For `tibia::gamewindow::TCharacterSelectionController`:

```text
METHODS=26
SIGNALS=10
TABLE=0x1d98fe4

0xd51c8b: cmp edx, 0x19
0xd51c90: lea rcx, [rip + 0x104734d]
0xd51c99: movsxd rax, dword ptr [rcx + rdx*4]
0xd51c9d: add rax, rcx
0xd51ca0: jmp rax

requestCharacterLogin
  index=0
  role=SIGNAL
  target=0xd52050
  flags=0x6
```

H4 is `PASS`. Canonical wording must call `0xd52050` a QMeta signal activation dispatch target, not a call-safe business implementation.

## Coordinator classification

Source #556 is `ACCEPT_WITH_EDITS`.

Accepted current-build facts:

- exact current package identity above;
- one `TGameClient` QMeta object with 44 methods / 6 signals;
- `onRequestLoginWithCredentials(void,QString,QString)` index 17 -> exact-build QMeta method dispatch target `0xd196f0`;
- `connectClientToGameserverWithExistingCredentials()` index 11 -> exact-build QMeta method dispatch target `0xd19500`;
- `loginSuccessful` index 0 -> QMeta signal activation dispatch target `0xd10200`;
- `requestCharacterLogin` index 0 -> QMeta signal activation dispatch target `0xd52050`;
- source producer's 19/19 bounded auth/session structural-name presence, with names-only semantics for entries not independently target-bound.

Required edits applied by coordinator promotion:

1. distinguish QMeta `SIGNAL` targets from ordinary `METHOD` targets;
2. replace stale source lifecycle wording about #555 with current trusted fence provenance: #555 merge `2e572789a2bc4b64c5e906c4515c15c625f6bc9e` plus #561 closeout;
3. preserve all non-QMeta state-machine targets and live auth/session semantics as `UNKNOWN`.

## Not promoted

The following remain unresolved by this bounded static task:

- current executable targets for non-QMeta methods such as `advanceStateMachineDirectlyToCharacterSelection`, `requestCharacterGameserverLogin`, and `onStartGameServerLoginStateEntered`;
- `TPlaySessionData` / `TAuthenticationAndEncryptionInfo` field provenance and password requirement semantics;
- live object addresses, vptr instances, thread affinity, helper call safety;
- login success, character selection, game-server connection, causal `IN_GAME`, restart/relogin/session-retention stability.

No login, credentials, process-memory access, GUI input, gameplay or physical runtime operation occurred in the coordinator audit.
