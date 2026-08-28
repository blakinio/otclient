# Exact-current `worldEntered` static anchor

Task: `OTC-20260828-current-qt-world-correlation`

Producer workflow run `33165852596`, job `98830952068`, exact PR head `0d444960e638158a2e6083d04ca6a0d0e0f005e3`, artifact `9683536921`.

Bounded `result.json` SHA-256: `64f476776746065802a07492260f7bf2431d91d191faa61941651f7c197b3130`.

## Exact source fence

The GitHub-hosted static workflow reused the repository's established WARP fetch path for:

`https://static.tibia.com/launcher/tibiaclient-linux-current/bin/client.lzma`

Both required fences passed before analysis:

- packed SHA-256 `075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f`;
- unpacked size `52105824` and SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`.

The client was not executed. Raw proprietary bytes were removed before artifact upload; only bounded JSON was uploaded.

## Recovered current QMeta identity

The resolver recovered `tibia::game::TPlayerProtocolMessageHandler` from current ELF stringdata + RELA-backed `staticMetaObject`, rather than using historical addresses.
Current recovered values:

```text
staticMetaObject        0x30b6ba0
stringdata              0x1cd1d04
metadata                0x1cd19c0
qt_static_metacall      0xd28460
dispatch LEA            0xd2846d
dispatch table          0x1d941e8
method count            22
signal count            22
worldEntered index      17
worldEntered argc       0
worldEntered flags      0x106
worldEntered case       0xd28890
case 64-byte SHA-256    d0267446d758dd324f8fb8417a3eaf013e49beb2c79a3d02322ba83e2980e7b1
```

The full 22-name method surface was recovered from the current metadata. `worldEntered` appeared exactly once, had zero arguments, and lay inside the `signal_count` range.

The dispatch table was not hard-coded. It was selected dynamically by the generated `InvokeMetaMethod` guard plus the full `edx <= method_count-1` range and the requirement that every table target resolve to executable code.

Historical addresses are materially different and therefore remain invalid as current lookup keys. The historical method index happened to also be `17`, but the current resolver derived that value independently from current metadata.

## Classification

This proves an exact-current **QMeta signal + generated dispatch-case anchor**. It does not yet prove that `0xd28890` is the normal runtime signal-emission entry used at world entry, because a generated `qt_static_metacall` case may delegate or tail-jump to the actual signal member implementation.
Therefore the next static step is to follow the current generated case structurally to the actual `worldEntered` signal member and prove its `QMetaObject::activate` relationship (or an equivalent direct semantic emission boundary). Only then is a read-only live observer justified.

```text
STATIC_QMETA_SIGNAL_IDENTITY=PROVEN
STATIC_GENERATED_DISPATCH_CASE=PROVEN
NORMAL_RUNTIME_SIGNAL_MEMBER=NOT_YET_PROVEN
RUNTIME_WORLD_ENTERED_EVENT=NOT_YET_OBSERVED
IN_GAME_CLAIMED=false
SEMANTIC_PROMOTION_PERFORMED=false
```

Safety: static-only `runtime_access=none`; no login, client execution, credentials, session secrets or packet payloads; no historical-address reuse; no proprietary binary retained.
