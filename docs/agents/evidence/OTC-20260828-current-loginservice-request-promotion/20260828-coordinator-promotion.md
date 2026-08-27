# Coordinator promotion — current loginservice request contract

Decision: **PASS_BOUNDED / ACCEPT_WITH_EDITS**.

This promotion was independently reconstructed from trusted `main@b359d583ba91ae45b0cac2c2fc94c0993d527ef7` and the final exact-current source run for PR #733. The source workflow/analyzer is intentionally not promoted.

## Primary evidence identity

```text
source PR             #733 (Draft, source-only)
source head           d278ae8e05e5f6a74c63b598d9d11e1c21f20b14
producer run          33127322903 = SUCCESS
producer job          98708447828 = SUCCESS
artifact              9668894065
artifact sha256       bd56db67ddb29e7e95915bfe13df10431afa016f3cbb369b42da096a700c876d
result.json sha256    43ec2cba35b22c4f8e651d7039c1b6aefd7047ee3cae8654e8af8acd21f392c9
```

Exact public client fence:

```text
version          15.32.75d4a0
packed sha256    075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
unpacked sha256  d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
unpacked size    52105824
```

Safety markers: `runtime_access=none`, `login_performed=false`, `secret_access=false`, `raw_client_uploaded=false`.

## Exact current request builder

The actual current login request `QJsonObject` builder is the exact FDE:

```text
0xe1e780..0xe1eb21
```

The coordinator distinguished it from the static QString initializer at `0x6130c0..0x613b27` by following exact-build QString storage xrefs into `QJsonObject::insert` calls.

The exact initializer binds the request-builder storages to these literals:

```text
0x31ba720 -> type
0x31ba740 -> login
0x31ba700 -> email
0x31ba6e0 -> password
0x31ba6c0 -> token
0x31ba6a0 -> deviceverificationcode
0x31ba600 -> emailcode
0x31ba5e0 -> stayloggedin
0x31ba5c0 -> devicecookie
0x31ba640 -> trusteddevicetoken
0x31ba660 -> loginconfirmationtoken
0x31ba680 -> loginconfirmationcode
0x31ba5a0 -> clienttype
0x31ba620 -> operatingsystem
0x31ba580 -> clientversion
0x31ba560 -> assetversion
```

Absolute addresses remain exact-build evidence only.

## Accepted unconditional request contract

Direct `QJsonObject::insert` dataflow in `0xe1e780..0xe1eb21` proves the normal current request always inserts:

```text
type = "login"
email = input QString at +0x00
password = input QString at +0x18
stayloggedin = input bool at +0xc0
devicecookie = input QString at +0xe0
clienttype = input integer at +0xf8
operatingsystem = QSysInfo::prettyProductName()
clientversion = input QString at +0x100
assetversion = input QString at +0x118
```

The key/value pair `type="login"` is a literal constant in the builder. `operatingsystem` is not a guessed string: the builder directly calls `QSysInfo::prettyProductName()` and inserts the returned QString under the exact `operatingsystem` key.

## Accepted conditional fields

The same exact builder inserts these only when the corresponding current QString state is present/non-null:

```text
token
deviceverificationcode
trusteddevicetoken
emailcode
loginconfirmationcode
loginconfirmationtoken
```

Therefore they must **not** be synthesized as empty/default request fields merely because their names exist in the binary.

Exact current literals `fromtimestamp`, `isreturner`, `showrewardnews`, and `viewedid` were also found, but their xrefs belong to separate JSON-building FDEs. They are not promoted as fields of this primary login request.

## Track B comparison

Track B's current HTTP producer/preflight already supplies:

```text
type=login
email
password
stayloggedin
devicecookie
clienttype
clientversion
assetversion
```

It does **not** supply `operatingsystem`.

Thus the independently proven current-exact delta is:

```yaml
TRACK_B_PRIMARY_LOGIN_REQUEST_MATCH: DISPROVEN_ONE_MANDATORY_FIELD
MISSING_UNCONDITIONAL_FIELD: operatingsystem
VALUE_SOURCE: QSysInfo::prettyProductName()
OPTIONAL_TOKEN_CODE_FIELDS_TO_SYNTHESIZE: NONE
FROMTIMESTAMP_RETURNER_REWARD_VIEWEDID_TO_ADD: REJECTED_NOT_PRIMARY_BUILDER
```

This is a material evidence-derived HTTP request change and is sufficient to authorize one bounded HTTP-only validation after Track B adds an equivalent non-empty Linux pretty-product-name value. It does not authorize an identical prior request retry.

## Claim boundary

This static task does not prove server-side acceptance rules or that the missing field is the sole cause of `errorCode=7`. It proves that Track B's request does not match the exact current official request builder and identifies the smallest current-exact mandatory delta. The next service call must test only that material delta and stop at the HTTP/session boundary before any game-login attempt.
