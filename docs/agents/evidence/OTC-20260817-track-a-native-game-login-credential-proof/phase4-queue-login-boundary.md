# Phase 4 — exact TProtocolMessageQueue login boundary

Task: `OTC-20260817-track-a-native-game-login-credential-proof`  
PR: `#499`  
Execution: exact-SHA GitHub-hosted static analysis, `runtime_access: none`

## Validation

```text
workflow commit: 3ffd72a78a8acb96b9cca234cc2d996597999903
run: 32061008870
job: 95482058462
result: SUCCESS
marker: GAMELOGIN_QUEUE_QMETA_PROBE=PASS
```

Exact packed/unpacked SHA and all no-runtime/no-secret safety markers passed.

## FACT — exact queue QMeta methods

Recovered class:

```text
tibia::protocol::TProtocolMessageQueue
method_count: 355
static-metacall jump table: 0x1d8bd6c
```

Relevant exact cases:

```text
#24  receivedLoginSuccessMessage(GameserverMessageLoginSuccess)          -> 0xdf766e
#38  receivedLoginChallengeMessage(GameserverMessageLoginChallenge)      -> 0xdf8c69
#39  receivedLoginErrorMessage(GameserverMessageLoginError)              -> 0xdf8c93
#58  receivedLoginAdviceMessage(GameserverMessageLoginAdvice)            -> 0xdf8fb1
#59  receivedLoginWaitMessage(GameserverMessageLoginWait)                -> 0xdf8fdb
#148 receivedReadyForSecondaryConnectionMessage(...)                     -> 0xdf704f
#196 sendLogin(GameclientMessageLogin)                                    -> 0xdf6be2
#198 sendEnterWorld(GameclientMessageEnterWorld)                          -> 0xdf6c04
#310 sendSecondaryLogin(GameclientMessageSecondaryLogin)                  -> 0xdf7da5
```

## FACT — corrected consumer boundary

`sendLogin @ 0xdf6be2` is a QMeta case thunk:

```asm
mov rsi, qword ptr [rcx + 8]
...
jmp 0xbd36a0
```

Therefore the exact native boundary is now:

```text
TProtocolMessageQueue::sendLogin(GameclientMessageLogin)
  -> 0xdf6be2
  -> 0xbd36a0
```

This upgrades the PR #498 `0xbd36a0` lead: it is not merely an unknown generic adapter. It is the exact queue-side consumer path for an already-constructed `GameclientMessageLogin` object.

`sendSecondaryLogin @ 0xdf7da5` analogously jumps to `0xbf3990`.

## FACT — adapter structure matches the proven nested RSA block

`0xbd36a0` receives the incoming message pointer in `rsi` and copies/inspects its protobuf has-bits and field storage. It also manages a nested allocated object whose cleanup destroys five length-delimited fields at:

```text
+0x18
+0x20
+0x28
+0x30
+0x38
```

and frees an object of size `0x48`.

That exact storage shape matches the independently proven `LoginRSAEncryptedBlock` object:

```text
5 x length-delimited fields at +0x18,+0x20,+0x28,+0x30,+0x38
2 x scalar fields at +0x40,+0x44
object extent through 0x48
```

The adapter also copies the `GameclientMessageLogin` scalar storage region beginning at input `+0x30` and conditionally handles input has-bits before invoking the receiver virtual slot `+0x68`.

## FACT — producer is upstream of this boundary

Because QMeta method #196 accepts a fully typed `GameclientMessageLogin` argument, the credential-producing writes occur before `TProtocolMessageQueue::sendLogin`. The queue adapter can copy/transform/encrypt the message but does not establish the original semantic source of its fields.

Therefore value provenance must now be recovered from the producer/emitter that constructs `GameclientMessageLogin`, not from string proximity or from the queue consumer alone.

## UNKNOWN

```text
which function constructs/populates GameclientMessageLogin
which upstream native object supplies each field
which LoginRSAEncryptedBlock field carries authentication/session material
whether an account-password-bearing object contributes to any field
```

## Next discriminator

On the exact SHA, recover:

1. full `TLoginProtocolMessageHandler` QMeta signatures/targets;
2. direct executable call xrefs to `TLoginProtocolMessageHandler::sendLoginMessage @ 0xcf2950`;
3. direct call xrefs to generated constructors `GameclientMessageLogin @ 0x17838c0` and `LoginRSAEncryptedBlock @ 0x1783450`;
4. RIP-relative vptr identity references for `0x30c84a0` / `0x30c8428` where useful;
5. bounded disassembly only around resulting producer callsites.

The goal is to move from a proven wire schema to producer provenance without runtime escalation.
