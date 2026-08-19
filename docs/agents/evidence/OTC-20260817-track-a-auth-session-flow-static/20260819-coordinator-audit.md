# Native auth/session flow — coordinator audit

Date: 2026-08-19  
Source PR: #498  
Source head: `43438bb8ed42841c8a9f5bc2d0e76d05b466a958`  
Coordinator review: `4971599610`  
Decision: **ACCEPT_WITH_EDITS**

## Exact historical fence

All source addresses, PMFs, QMeta tables, vptrs and disassembly claims are accepted **only** for the historical exact official Linux client:

```text
version token  15.32.df7b29
client size    51965216
client SHA256  e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed SHA256  496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
```

They are not current-build addresses for the later `ed5469...` client. Current-build #556/#528 evidence corroborates portions of the architecture but does not rebase historical offsets.

## Independent source-producer verification

The source final static producer run `32057651024` completed successfully and independently re-fenced the exact historical packed/client identities before emitting its synthesis. Its terminal markers include:

```text
AUTHSESSION_FINAL_EXACT_PACKED_SHA=PASS
AUTHSESSION_FINAL_EXACT_CLIENT_SHA=PASS
AUTHSESSION_FINAL_STATIC_SYNTHESIS=PASS
RUNTIME_ACCESS=none
LOGIN_PERFORMED=false
SECRET_ACCESS=false
RAW_CLIENT_UPLOAD=false
```

The producer reproduced the source QMeta rows and targets, including the authentication state-machine boundaries, login-uploader result, existing-credentials game connection route, selected-character route, login protocol surface and disconnect/reconnect controller surface.

## Accepted factual model

The historical exact build contains the following bounded architecture:

- initial credential-facing boundary `TGameClient::onRequestLoginWithCredentials(QString,QString)`;
- account-auth result `TLoginRequestUploader::loginSuccessful(TCharacterList,TWorldList,TPlaySessionData)`;
- a native zero-argument route to character selection through `TAuthenticationProcessController` when suitable retained state exists;
- selected-character handoff through `TCharacterSelectionController::requestCharacterLogin(...)`;
- game-server progression through `requestCharacterGameserverLogin` / `onStartGameServerLoginStateEntered`;
- zero-argument `TGameClient::connectClientToGameserverWithExistingCredentials()`;
- login-protocol message surface feeding a `TProtocolMessageQueue` receiver;
- explicit disconnect/reconnect reactions that can route either toward character selection or back to the login dialog.

The source's important corrections are accepted:

```text
0xcf2ca0 = Qt static-metacall case, not the implementation PMF for sendLoginMessage
0xbd36a0 = adapter/delegator, not a proven final serializer
0x858a50 = UI formatting path, not credential transport
0x88c2d0 = UI/localization path, not credential serialization
```

## Bounded conclusions

The source conclusion matrix remains intentionally conservative:

```text
CAN_SKIP_LOGIN_FORM: PARTIAL
CAN_SKIP_PASSWORD_ENTRY: PARTIAL
CAN_REUSE_SESSION: YES
PASSWORD_REQUIRED_FOR_GAME_LOGIN: UNKNOWN
DIRECT_CHARACTER_LOGIN_POSSIBLE: YES, conditional on valid retained play-session state and a selected character
```

`CAN_REUSE_SESSION=YES` is an architectural/native-control-path statement for this exact build. It is not a guarantee that every expired session is reusable, nor proof of disk/keyring persistence or refresh policy.

The following remain UNKNOWN at this historical static boundary:

- exact `TPlaySessionData` field layout;
- exact persistent store / launcher / keyring path;
- expiry / TTL / refresh policy;
- exact `GameclientMessageLogin` credential-field semantics;
- whether plaintext password participates in any internal game-login payload construction;
- cleanup/wipe timing for sensitive values;
- generalized cold-start preselection semantics.

## Source delivery defect

Exact source governance run `32058753745` failed because the PR changed:

```text
.github/workflows/tibia-official-client-re-auth-session-static.yml
```

without an active Track A admission task bound to the source branch. The failure is a repository-governance/delivery defect, not a falsification of the static evidence.

The coordinator repair is to **exclude that workflow from promotion entirely**. The accepted durable evidence and research synthesis do not need a runtime-sensitive workflow on `main`.

## Source ancestry

At coordinator review, source #498 was:

```text
merge base  8a5fcfd72f2554261eef91a2129c9cc076e730ea
ahead_by    26
behind_by   50
```

Direct source merge is therefore inappropriate. Clean promotion from current `main` carries only accepted historical evidence/research plus this audit and a coordinator archive.

## Safety

```yaml
runtime_access: none
client_executed: false
credential_use: false
login: false
gui_input: false
gameplay: false
transaction: false
process_memory_access: false
runtime_mutation: false
```

No owner secret or proprietary client binary is promoted by this closeout.
