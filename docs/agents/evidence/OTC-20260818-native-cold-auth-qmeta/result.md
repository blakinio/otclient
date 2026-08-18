# Native cold-auth QMeta result

Status: **DRAFT / NOT PROMOTED**  
Task: `OTC-20260818-native-cold-auth-qmeta`  
PR: `#505`  
Exact task head validated: `d0c1360b649fd8c4a92587b7713644c49162694c`  
Workflow run/job: `32104348691 / 95610768376` — **SUCCESS**

## Safety boundary

```text
FORM_UI_USED=false
OCR_USED=false
IMAGE_MATCHING_USED=false
COORDINATE_CLICK_USED=false
BLIND_TAB_RETURN_USED=false
RUNTIME_ACCESS=none
CLIENT_EXECUTED=false
SYNLOGY_RUNTIME_USED=false
CREDENTIAL_ACCESS=false
SESSION_ACCESS=false
```

The workflow downloaded the exact official native Linux client into the disposable GitHub-hosted runner, verified both packed and unpacked identities, analyzed it statically, and did not execute the client or persist raw client bytes as a repository artifact.

## Exact client fence

```text
version: 15.32.df7b29
packed client.lzma sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
unpacked size: 51965216
unpacked sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Observed:

```text
COLD_AUTH_EXACT_PACKED_SHA=PASS
COLD_AUTH_EXACT_CLIENT_SHA=PASS
COLD_AUTH_CLIENT_EXECUTED=false
COLD_AUTH_RUNTIME_ACCESS=none
```

## FACT — exact TGameClient QMeta method

The exact QMeta object is:

```text
class: tibia::client::TGameClient
method_count: 44
signal_count: 6
static_metacall: 0xd06260
```

`onRequestLoginWithCredentials` is uniquely present as:

```text
method metadata index / InvokeMetaMethod id: 17
argc: 2
flags: 0x8
return type id: 0x2b = void
argument type ids: 0x0a, 0x0a = QString, QString
signature: void onRequestLoginWithCredentials(QString, QString)
```

Exact workflow markers:

```text
COLD_AUTH_TGAMECLIENT_QMETA_IDENTITY=PASS
COLD_AUTH_METHOD_NAME=onRequestLoginWithCredentials
COLD_AUTH_METHOD_META_INDEX=17
COLD_AUTH_ARGC=2
COLD_AUTH_METHOD_FLAGS=0x8
COLD_AUTH_RAW_PARAM_TYPE_IDS=0x2b,0xa,0xa
COLD_AUTH_ARG_TYPES=QString,QString
COLD_AUTH_RETURN_TYPE=void
```

## FACT — InvokeMetaMethod dispatch target

Two executable relative jump-table candidates exist in the scanned `qt_static_metacall` region, but only one is the full 44-method `TGameClient` dispatcher.

Accepted dispatcher:

```text
call guard: test esi,esi                  # QMetaObject::InvokeMetaMethod == 0
range guard: cmp edx,0x2b                # valid method ids 0..43
jump-table LEA: 0xd0626a
jump table: 0x1d6dea0
method 17 target: 0xd06850
```

Exact 32-byte target fence:

```text
488b5110488b71084883c4485b5de92d389eff0f1f440000488bbfa009000048
```

Workflow markers:

```text
COLD_AUTH_INVOKE_DISPATCH_ROLE=PROVEN_BY_CALL_AND_FULL_RANGE_GUARDS
COLD_AUTH_DISPATCH_LEA=0xd0626a
COLD_AUTH_DISPATCH_TABLE=0x1d6dea0
COLD_AUTH_DISPATCH_TARGET=0xd06850
COLD_AUTH_TARGET_EXECUTABLE=true
COLD_AUTH_TARGET_INSTRUCTION_FENCE=488b5110488b71084883c4485b5de92d389eff0f1f440000488bbfa009000048
COLD_AUTH_STATIC_DISCRIMINATOR=PASS
```

### Negative control

A second executable table begins at `0xd0692a`, but its own dispatcher is guarded by `cmp edx,4`; it is therefore a separate five-entry meta dispatcher and is not the 44-method `TGameClient` `InvokeMetaMethod` table. It produced target `0xd0aede` for synthetic index 17 only because the earlier broad table scanner intentionally read 44 relative entries for falsification. The full-range guard rejects it.

## Runtime implication — not yet runtime proof

This result supplies the exact static contract required by the native-login prompt for cold authentication below the form:

```text
unique live tibia::client::TGameClient instance
  -> owning Qt event-loop thread
  -> qt_static_metacall(this, InvokeMetaMethod, 17, argv)
  -> argv[1] = valid QString email object
  -> argv[2] = valid QString password object
  -> original native account-authentication state machine
```

The target code begins by loading `_a[2]` and `_a[1]`, consistent with the generated QMeta wrapper for two `QString` arguments. Runtime use still requires fresh exact-process/PIE rebinding, live object provenance, Qt thread-affinity proof, protected transient secret ingress, and current Track A runtime authority. This static task does not claim that those runtime gates have passed.

## Result

```text
NATIVE_COLD_AUTH_QMETA_CONTRACT=PROVEN_STATIC_EXACT_SHA
FORMLESS_COLD_AUTH_ENTRY_AVAILABLE=YES_STATIC_CONTRACT
ACCOUNT_AUTHENTICATION_PERFORMED=false
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=false
```
