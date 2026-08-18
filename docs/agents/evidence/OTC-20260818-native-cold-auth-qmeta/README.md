# Native cold-auth QMeta evidence

Status: **DRAFT / NOT PROMOTED**

Task: `OTC-20260818-native-cold-auth-qmeta`

This namespace contains only deterministic static evidence for the exact official native Linux Tibia client. It must not contain credentials, session material, raw proprietary client bytes, process-memory data, screenshots, or runtime observations.

The objective is strictly **login without using the visual login form**. GUI control, OCR, coordinate clicks, blind Tab/Return and image matching are forbidden as the target mechanism.

The worker must independently verify:

```text
packed client.lzma sha256 = 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
unpacked size             = 51965216
unpacked sha256           = e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Primary question:

```text
What exact QMeta method index, argument contract, static dispatch target and instruction fence implement
TGameClient::onRequestLoginWithCredentials(QString, QString)?
```

This boundary is intended to replace cold-auth form operation with original native client logic below the UI. Any unresolved ambiguity remains `UNKNOWN`.
