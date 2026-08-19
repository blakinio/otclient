# TIBIA-RE-AUTH-SESSION — coordinator audit plan

```yaml
task: OTC-20260819-track-a-auth-session-current-build-static
source_pr: 556
source_head: 411d0e287d08406c682ef063fb3f3f61341d9295
coordinator_base_main: e4357137e47836d67eb19ceb13a8e313f69bf778
runtime_access: none
client_execution: false
login: false
credentials: false
```

This plan was committed before consuming the terminal result of the strict coordinator discriminator.

## Pre-registered hypotheses

- `H1`: exact current `TGameClient::onRequestLoginWithCredentials` is QMeta index 17, role `METHOD`, params `void,QString,QString`, and the invoke switch binds index 17 to `0xd196f0`.
- `H2`: exact current `TGameClient::connectClientToGameserverWithExistingCredentials` is QMeta index 11, role `METHOD`, and the invoke switch binds index 11 to `0xd19500`.
- `H3`: `TLoginRequestUploader::loginSuccessful` is QMeta index 0 and role `SIGNAL`; any recovered target is classified only as a QMeta signal activation dispatch target, not a call-safe business implementation.
- `H4`: `TCharacterSelectionController::requestCharacterLogin` is QMeta index 0 and role `SIGNAL`; any recovered target is classified only as a QMeta signal activation dispatch target, not a call-safe business implementation.

## Strict control-flow discriminator

For each accepted target, the independent audit must recover exactly one current-build switch chain with all of:

```text
cmp edx, method_count - 1
RIP-relative LEA of table base
movsxd target, dword ptr [table_base + rdx*4]
add target, table_base
jmp target
```

The same table must contain executable entries for the complete QMeta method range and the selected index must resolve to the claimed exact-build target.

A class/method name or an executable-looking table alone is insufficient.

## Decision rule

- `ACCEPT_WITH_EDITS` if H1/H2 are independently confirmed, H3/H4 roles are confirmed, and no stronger contradictory evidence appears. Required edits: preserve signal-vs-method distinction and replace stale source wording that still describes #555 as an unmerged Draft with current trusted fence provenance #555/#561.
- `RETURN_FOR_EVIDENCE` if H1 or H2 fails strict binding or the current package identity no longer matches the trusted fence.
- `REJECT/SUPERSEDE` only if exact current evidence directly falsifies the bounded source claim or a stronger current producer already supersedes the package.

No live auth/session semantics, credentials, login success, `IN_GAME`, non-QMeta state-machine targets, or helper call safety can be promoted by this static audit.
