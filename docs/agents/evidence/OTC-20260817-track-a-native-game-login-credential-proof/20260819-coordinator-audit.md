# Native game-login credential flow — coordinator audit

Date: 2026-08-19  
Source PR: #499  
Source head: `6b814f90d4e6d72238651b48be0621dd4c9fa6f3`  
Coordinator review: `4971650428`  
Decision: **ACCEPT_WITH_EDITS**

## Historical exact-build fence

All source addresses, vtables, producer offsets and protobuf implementation details are accepted only for historical official Linux client:

```text
version token  15.32.df7b29
client size    51965216
client SHA256  e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed SHA256  496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
```

None is a current-build address for later `ed5469...`.

## Independent producer verification

Exact source-head governance and CI are green. Final provenance producer run `32066254378` completed successfully and re-fenced the historical packed/client identities before analysis. It emitted:

```text
FINAL_PROVENANCE_EXACT_CLIENT_SHA=PASS
FINAL_PROVENANCE_RUNTIME_ACCESS=none
FINAL_PROVENANCE_LOGIN_PERFORMED=false
FINAL_PROVENANCE_SECRET_ACCESS=false
FINAL_AUTHINFO_VTABLE=0x2f63240
FINAL_PLAYSESSION_RECEIVER_PROBE=PASS
```

## Accepted wire/provenance facts

For this exact build:

- native `GameclientMessageLogin` contains nested `LoginRSAEncryptedBlock` at field 7;
- recovered top-level wire shape has fields 1/2/3 varint, 4/5 length-delimited, 6 varint, 7 length-delimited nested message;
- recovered `LoginRSAEncryptedBlock` wire shape has fields 1/2/5/6/7 length-delimited and 3/4 varint;
- native producer path is owned by `TLoginProtocolMessageHandler` and feeds `TProtocolMessageQueue::sendLogin(GameclientMessageLogin)`;
- producer values are sourced from `TAuthenticationAndEncryptionInfo` (historical vtable `0x2f63240`);
- secondary login uses a distinct `GameclientMessageSecondaryLogin` / `SecondaryLoginRSAEncryptedBlock` family.

These are structural wire/provenance facts, not semantic field-name recovery.

## Required semantic correction

The source research prose includes a practical statement equivalent to:

```text
CAN_SKIP_LOGIN_FORM: YES when suitable valid retained state exists
```

That is too broad if read as a generalized capability. Canonical interpretation is:

```text
DIRECT_TO_CHARACTER_SELECTION_ROUTE_FOR_VALID_RETAINED_STATE: YES
CAN_SKIP_LOGIN_FORM_GENERALIZED: PARTIAL
```

This matches the accepted parent #498 boundary: the binary has a native retained-state route, but cold-start/preselection/persistence/expiry breadth is not completely proven.

## Preserved UNKNOWNs

The following are explicitly **not proven**:

- semantic names of individual RSA-block fields;
- which wire field is email/account/password/session token/device data;
- causal mapping `TPlaySessionData field -> TAuthenticationAndEncryptionInfo field -> specific LoginRSAEncryptedBlock field`;
- password presence in game login;
- password absence from game login;
- whether a valid retained play session eliminates every need for a plaintext password in all internal paths.

Therefore:

```text
PASSWORD_REQUIRED_FOR_GAME_LOGIN: UNKNOWN
PASSWORD_PRESENT_IN_GAME_LOGIN: NOT_PROVEN
PASSWORD_ABSENT_FROM_GAME_LOGIN: NOT_PROVEN
```

Wire tag/type recovery must not be renamed into credential semantics without a new causal proof.

## Source ancestry

At coordinator review source #499 was `behind_by=50` against current main. Direct merge is inappropriate; clean current-main promotion carries accepted exact source evidence/research plus this correction audit and a terminal archive.

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
